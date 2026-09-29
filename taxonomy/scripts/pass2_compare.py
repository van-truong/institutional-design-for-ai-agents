#!/usr/bin/env python3
"""Pass 2: fold deductive recoding into instances.csv and measure agreement with pass 1.

Usage:  python3 taxonomy/scripts/pass2_compare.py   (after collapse_codes.py and build_configurations.py)

Pass 1 (open codes collapsed to mechanisms) and pass 2 (recoding against the codebook) were done by
different, independent coders. For each instance the script records both and flags disagreements.
Agreement is reported at the mechanism and theme level, as percent agreement and Cohen's kappa, over
instances that both passes coded as a single mechanism.
Outputs: instances.csv (pass-2 columns), coding/pass2_agreement.txt, coding/pass2_review.csv
(disagreements, misfits and proposed new/merged/split mechanisms, for the verifier).
"""
import collections, csv, glob, json, os

HERE = os.path.dirname(os.path.abspath(__file__)); TAX = os.path.dirname(HERE)

# Pass-2 decisions on individual instances (applied over the pass-2 code): instance -> (kind, mechanism, reason)
OVERRIDES = {
    'I0266': ('mechanism', 'M09', 'overseer prunes a flagged agent\'s links: quarantine, not agent partner choice (M10 split)'),
    'I0200': ('mechanism', 'M22', 'forwarding credit is paid by the system for a cooperative act, not mutual credit'),
    'I0381': ('mechanism', 'M66', 'gain came from telling agents sustainable thresholds (new M66)'),
    'I0025': ('configuration', 'M67', 'managerial model centres on capacity building (new M67), with monitoring and dispute resolution'),
    'I0209': ('mechanism', 'M35', 'output verification before acceptance is runtime interception'),
    'I0263': ('mechanism', 'M01', 'honeypot inducement is a monitoring technique'),
    'I0455': ('out_of_scope', '', 'resource abundance and aggression cost are environment parameters; tagging is an attack, not a sanction'),
    'I0469': ('out_of_scope', '', 'centrally trained channel access; not a social dilemma'),
}

def kappa(pairs):
    n = len(pairs)
    if not n: return float('nan'), float('nan')
    po = sum(a == b for a, b in pairs) / n
    ca, cb = collections.Counter(a for a, _ in pairs), collections.Counter(b for _, b in pairs)
    pe = sum(ca[k] * cb.get(k, 0) for k in ca) / n / n
    return po, (po - pe) / (1 - pe) if pe < 1 else float('nan')

def main():
    P2 = []
    for f in sorted(glob.glob(os.path.join(TAX, 'coding', 'pass2_batch[0-9].json'))): P2 += json.load(open(f))
    p2 = {p['instance_id']: p for p in P2}
    book = {r['mechanism_id']: r for r in csv.DictReader(open(os.path.join(TAX, 'codebook.csv')))}
    inst = {r['instance_id']: r for r in csv.DictReader(open(os.path.join(TAX, 'instances.csv')))}
    vpath = os.path.join(TAX, 'coding', 'disagreements.csv')
    VERIFIER = {v['instance_id']: v for v in csv.DictReader(open(vpath))} if os.path.exists(vpath) else {}
    VERIFIER = {k: v for k, v in VERIFIER.items() if v.get('decision', '').strip()}
    missing = sorted(set(inst) - set(p2))
    if missing: print(f'WARNING: {len(missing)} instances lack pass-2 codes')

    new = ['kind', 'mechanism_p2', 'secondary_p2', 'config_p2', 'fit', 'evidence_type', 'effect', 'agreement']
    cols = list(next(iter(inst.values())).keys()); cols += [c for c in new if c not in cols]
    mpairs, tpairs, review = [], [], []
    theme = lambda m: book[m]['theme_id'] if m in book else m
    for iid, r in inst.items():
        q = p2.get(iid)
        if not q: continue
        m1, m2 = r['mechanism_p1'], (q.get('mechanism_id') or '')
        r.update(kind=q.get('kind', ''), mechanism_p2=m2, secondary_p2=q.get('secondary_ids') or '',
                 config_p2=q.get('configuration_id') or '', fit=q.get('fit', ''),
                 evidence_type=q.get('evidence_type', ''), effect=q.get('effect') or '')
        r['mechanism'] = m2 if m2 in book else (m1 if q.get('kind') in ('mechanism', 'configuration') else '')
        if iid in OVERRIDES:
            r['kind'], r['mechanism'], _ = OVERRIDES[iid]
        v = VERIFIER.get(iid)
        if v:  # verifier decisions win over both passes
            d = v['decision'].strip()
            if d == 'p1': r['mechanism'] = m1
            elif d == 'p2': r['mechanism'] = m2
            elif d in ('phenomenon', 'out_of_scope'): r['kind'], r['mechanism'] = d, ''
            elif d in book: r['mechanism'] = d
            else: raise SystemExit(f'{iid}: bad verifier decision {d!r}')
            r['verified'] = v.get('verifier', 'VQT')
        single1 = m1 in book
        single2 = q.get('kind') == 'mechanism' and m2 in book
        if single1 and single2:
            mpairs.append((m1, m2)); tpairs.append((theme(m1), theme(m2)))
            r['agreement'] = 'same_mechanism' if m1 == m2 else ('same_theme' if theme(m1) == theme(m2) else 'differ')
        else:
            k1 = 'mechanism' if single1 else ('phenomenon' if r['code'] == '(phenomenon)' else 'configuration')
            r['agreement'] = 'same_kind' if k1 == q.get('kind') else f'kind:{k1}->{q.get("kind")}'
        flag = []
        if r['agreement'] in ('differ', 'same_theme') or r['agreement'].startswith('kind:'): flag.append(r['agreement'])
        if q.get('fit') in ('misfit', 'partial') and q.get('proposed_mechanism'): flag.append(q['fit'])
        if flag:
            review.append(dict(instance_id=iid, flag=';'.join(flag), title=r['title'][:90], discipline=r['discipline'],
                               pass1_code=r['code'], pass1_mechanism=m1, pass2_kind=q.get('kind', ''), pass2_mechanism=m2,
                               pass2_secondary=q.get('secondary_ids') or '', proposed=q.get('proposed_mechanism') or '',
                               note=q.get('note') or '', decision=''))
    with open(os.path.join(TAX, 'instances.csv'), 'w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=cols); w.writeheader(); w.writerows(inst.values())
    if review:
        with open(os.path.join(TAX, 'coding', 'pass2_review.csv'), 'w', newline='') as f:
            w = csv.DictWriter(f, fieldnames=list(review[0].keys())); w.writeheader(); w.writerows(review)

    # Recount the codebook from final codes (primary mechanism; secondary levers counted separately).
    rows = list(csv.DictReader(open(os.path.join(TAX, 'codebook.csv'))))
    for b in rows:
        for k in ('n_llm_tested', 'n_llm_proposed', 'n_marl_tested'): b.pop(k, None)
    fin = [r for r in inst.values() if r['kind'] in ('mechanism', 'configuration')]
    for b in rows:
        mid = b['mechanism_id']; rs = [r for r in fin if r['mechanism'] == mid]
        sec = [r for r in fin if mid in r['secondary_p2'].split(';') and r['mechanism'] != mid]
        nonseed = [r for r in rs if r['origin'] != 'seed']
        disc = collections.Counter(d for r in nonseed for d in r['discipline'].split(';') if d)
        # distinct studies (source keys) where the mechanism is the primary or a secondary lever
        art = lambda t, e: len({r['source_key'] for r in rs + sec if r['agent_type'] == t and r['evidence_type'] == e})
        b.update(n_instances=len(rs), n_secondary=len(sec), n_llm=sum(r['agent_type'] == 'llm' for r in rs),
                 n_marl=sum(r['agent_type'] == 'marl' for r in rs), n_seed=len(rs) - len(nonseed),
                 llm_tested_studies=art('llm', 'tested'), llm_proposed_studies=art('llm', 'proposed'), marl_tested_studies=art('marl', 'tested'),
                 n_disciplines=len(disc), disciplines=';'.join(f'{d}:{n}' for d, n in disc.most_common()),
                 disciplines_all=';'.join(f'{d}:{n}' for d, n in collections.Counter(
                     d for r in rs for d in r['discipline'].split(';') if d).most_common()))
    bcols = list(rows[0].keys())
    with open(os.path.join(TAX, 'codebook.csv'), 'w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=bcols); w.writeheader(); w.writerows(rows)

    po_m, k_m = kappa(mpairs); po_t, k_t = kappa(tpairs)
    C = lambda key: dict(collections.Counter(q.get(key) or '-' for q in P2))
    prop = [q for q in P2 if q.get('proposed_mechanism')]
    lines = [f'pass-2 coded: {len(P2)} of {len(inst)}',
             f'kind: {C("kind")}', f'fit: {C("fit")}', f'evidence_type: {C("evidence_type")}', f'effect: {C("effect")}',
             f'mechanism agreement (n={len(mpairs)}): {po_m:.1%}, kappa {k_m:.2f}',
             f'theme agreement (n={len(tpairs)}): {po_t:.1%}, kappa {k_t:.2f}',
             f'instances with a proposed new/merged/split mechanism: {len(prop)}',
             f'flagged for review: {len(review)} (coding/pass2_review.csv)',
             f'overrides applied: {len(OVERRIDES)}',
             'note: both passes were LLM coders; pass-2 coders saw codebook examples drawn from pass-1 native terms,',
             'so agreement is an upper bound on independent agreement, not human inter-rater reliability.']
    unused = sorted(set(book) - {q.get('mechanism_id') for q in P2} - {s for q in P2 for s in (q.get('secondary_ids') or '').split(';')})
    lines.append(f'mechanisms never used in pass 2: {unused or "none"}')
    open(os.path.join(TAX, 'coding', 'pass2_agreement.txt'), 'w').write('\n'.join(lines) + '\n')
    print('\n'.join(lines))

if __name__ == '__main__':
    main()
