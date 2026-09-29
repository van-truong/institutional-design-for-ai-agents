#!/usr/bin/env python3
"""Phase 2 merge: fold search-slice results (JSON) into the taxonomy dataset.

Usage:  python3 taxonomy/scripts/merge_search.py <dir with G*.json and NEWS.json>

Writes / updates (in taxonomy/):
  papers.csv      de-duplicated artificial-agent studies (llm + marl tracks)
  search_log.csv  every query with screening counts (PRISMA-style flow)
  incidents.csv   news-track incidents (Phase 4)
  mechanisms.csv  llm_status / llm_evidence / marl_status / marl_evidence per mechanism
  search_raw/     verbatim copies of the input JSON (audit trail)
Search statuses replace seed statuses; the seed's prior evidence text is kept in notes.
"""
import csv, glob, json, os, re, shutil, sys

HERE = os.path.dirname(os.path.abspath(__file__)); TAX = os.path.dirname(HERE)

# Codebook additions suggested by the search (added after the seed; match=assigned, verify first).
ADDED_MECHANISMS = [dict(
    id='P04-06', name='Peer reward / gifting', primitive_id='4', primitive='Direct Benefit Provision (Reward)',
    discipline_family='economic', domain='Economic / interpersonal', valence='reward', game_type='PGG',
    functions='sanctions', channels='incentive', dilemmas='contributive',
    human_example='Group members pay a cost to transfer a reward to peers who contributed (reward treatment of lab public-goods games).',
    key_references='Andreoni et al. (2003) AER; Sefton, Shupp & Walker (2007) Economic Inquiry',
    llm_status='tested',
    llm_evidence='guzmanpiedrahita2025corrupted (SanctSim: agents pay 1 token to give +1 to a peer; LLMs enforce mainly through rewards).',
    marl_status='tested',
    marl_evidence='yang2020lio (learned peer incentives); willis2023transfer (minimal reward transfer); lupu2020gifting (partial, student abstract).',
    ai_analogue='Agents grant each other compute, budget, or priority credits from their own allocation.',
    sources='search', match='assigned', precoded='functions;channels;dilemmas', verified='',
    notes='Added in Phase 2 (G2 codebook gap): peer-to-peer monetary reward had no home in P04; P04-01 is praise/status and P04-02 is a central subsidy.')]
# Papers the slices mapped to a stand-in mechanism before the addition above: key -> (old id, new id).
PAPER_REMAP = {'yang2020lio': ('P04-02', 'P04-06'), 'lupu2020gifting': ('P04-02', 'P04-06'),
               'willis2023transfer': ('P04-02', 'P04-06'), 'guzmanpiedrahita2025corrupted': (None, 'P04-06')}
# Slices keyed some papers differently in their evidence text; rewrite to the papers.csv key.
KEY_ALIASES = {'guzman2025reasoning': 'guzmanpiedrahita2025corrupted', 'haupt2022formal': 'haupt2022contracts',
               'hua2023lopt': 'hua2025lopt', 'ng2026market': 'ngyisheng2026formal', 'piatti2024govsim': 'piatti2024cooperate',
               'rehm2026selfgovern': 'rehm2026certain', 'ueshima2023': 'ueshima2023deconstructing',
               'vinitsky2023cnm': 'vinitsky2023sanctions', 'warnakulasuriya2025evolution': 'warnakulasuriya2025punishment',
               'willis2025systems': 'willis2025will', 'wyse2026commitment': 'wyse2026contracts',
               'bracale2026institutional': 'syrnikov2026institutional', 'bracalesyrnikov2026institutional': 'syrnikov2026institutional',
               'gupta2026sociallearning': 'gupta2025social'}
EVIDENCE_EDITS = {'P04-02': ('marl_evidence', ' Peer rewards: yang2020lio, lupu2020gifting, willis2023transfer.', ' Peer rewards moved to P04-06.')}

def norm_title(t): return re.sub(r'[^a-z0-9]+', ' ', (t or '').lower()).strip()

def paper_key(p):
    for f in ('arxiv_id', 'doi'):
        v = (p.get(f) or '').strip().lower()
        if v and v != 'null': return f + ':' + re.sub(r'v\d+$', '', v)
    return 'title:' + norm_title(p.get('title'))

def main(src):
    groups = sorted(glob.glob(os.path.join(src, 'G*.json')))
    raw = os.path.join(TAX, 'search_raw'); os.makedirs(raw, exist_ok=True)
    papers, log, updates, tags = {}, [], {}, {}
    for g in groups:
        d = json.load(open(g)); gid = d.get('group', os.path.basename(g)[:-5])
        shutil.copy(g, os.path.join(raw, os.path.basename(g)))
        for q in d.get('queries', []):
            log.append(dict(group=gid, date_run=d.get('date_run', ''), source=q.get('source', ''), query=q.get('query', ''),
                            results_screened=q.get('results_screened', ''), included=q.get('included', '')))
        for p in d.get('papers', []):
            k = paper_key(p)
            if k in papers:
                e = papers[k]
                e['mechanism_ids'] = ';'.join(sorted((set(e['mechanism_ids'].split(';')) | set(p.get('mechanism_ids', []))) - {''}))
                e['groups'] = ';'.join(sorted(set(e['groups'].split(';')) | {gid}))
                e['themes'] = ';'.join(sorted((set(e['themes'].split(';')) | set(p.get('themes', []))) - {''}))
            else:
                papers[k] = dict(key=p.get('key', ''), title=p.get('title', ''), authors=p.get('authors', ''),
                                 year=p.get('year', ''), venue=p.get('venue', ''), url=p.get('url', ''),
                                 arxiv_id=p.get('arxiv_id') or '', doi=p.get('doi') or '', track=p.get('track', ''),
                                 mechanism_ids=';'.join(sorted(set(p.get('mechanism_ids', [])) - {''})),
                                 how_tested=p.get('how_tested', ''), finding=p.get('finding', ''),
                                 located_via=p.get('located_via', ''), groups=gid,
                                 themes=';'.join(sorted(set(p.get('themes', [])))), verified='')
        for t in d.get('existing_tags', []):
            tags.setdefault(t['key'], set()).update(t.get('themes', []))
        for u in d.get('mechanism_updates', []):
            for f in ('llm_evidence', 'marl_evidence'):
                u[f] = re.sub(r'\b[a-z]+\d{4}[a-z0-9]*\b', lambda k: KEY_ALIASES.get(k.group(), k.group()), u.get(f) or '')
            updates[u['id']] = u

    for e in papers.values():
        if e['key'] in tags:
            e['themes'] = ';'.join(sorted((set(e['themes'].split(';')) | tags[e['key']]) - {''}))
        if e['key'] in PAPER_REMAP:
            old, new = PAPER_REMAP[e['key']]
            e['mechanism_ids'] = ';'.join(sorted((set(e['mechanism_ids'].split(';')) - {old, ''}) | {new}))

    pcols = ['key', 'title', 'authors', 'year', 'venue', 'url', 'arxiv_id', 'doi', 'track', 'mechanism_ids',
             'how_tested', 'finding', 'located_via', 'groups', 'themes', 'verified']
    rows = sorted(papers.values(), key=lambda r: (str(r['year']), r['key']))
    with open(os.path.join(TAX, 'papers.csv'), 'w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=pcols); w.writeheader(); w.writerows(rows)
    with open(os.path.join(TAX, 'search_log.csv'), 'w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=['group', 'date_run', 'source', 'query', 'results_screened', 'included'])
        w.writeheader(); w.writerows(log)

    mpath = os.path.join(TAX, 'mechanisms.csv'); mech = list(csv.DictReader(open(mpath)))
    cols = list(mech[0].keys())
    if 'marl_evidence' not in cols: cols.insert(cols.index('marl_status') + 1, 'marl_evidence')
    have = {m['id'] for m in mech}
    mech += [dict(a) for a in ADDED_MECHANISMS if a['id'] not in have]
    added = {a['id'] for a in ADDED_MECHANISMS}
    missing = []
    for m in mech:
        m.setdefault('marl_evidence', '')
        if m['id'] in EVIDENCE_EDITS:
            f, old, new = EVIDENCE_EDITS[m['id']]
            if old in (updates.get(m['id']) or {}).get(f, ''): updates[m['id']][f] = updates[m['id']][f].replace(old, new)
        if m['id'] in added: continue
        u = updates.get(m['id'])
        if not u: missing.append(m['id']); continue
        seed_ev = m.get('llm_evidence', '')
        m['llm_status'] = u.get('llm_status', m['llm_status'])
        m['llm_evidence'] = u.get('llm_evidence', '')
        m['marl_status'] = u.get('marl_status', '')
        m['marl_evidence'] = u.get('marl_evidence', '')
        chk = u.get('seed_claims_checked', '')
        extra = '; '.join(x for x in [f'seed evidence: {seed_ev}' if seed_ev else '', f'seed claims checked: {chk}' if chk else ''] if x)
        if extra and 'seed evidence:' not in m['notes'] and 'seed claims checked:' not in m['notes']: m['notes'] = (m['notes'] + ' | ' if m['notes'] else '') + extra
    with open(mpath, 'w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=cols); w.writeheader(); w.writerows(mech)

    news = os.path.join(src, 'NEWS.json'); n_inc = 0
    if os.path.exists(news):
        shutil.copy(news, os.path.join(raw, 'NEWS.json'))
        inc = json.load(open(news)).get('incidents', []); n_inc = len(inc)
        icols = ['key', 'date', 'headline', 'summary', 'category', 'setting', 'multi_agent', 'systems_involved',
                 'source_outlet', 'url', 'additional_urls', 'institutional_angle', 'verified']
        with open(os.path.join(TAX, 'incidents.csv'), 'w', newline='') as f:
            w = csv.DictWriter(f, fieldnames=icols, extrasaction='ignore'); w.writeheader()
            for i in inc:
                i = dict(i); i['additional_urls'] = ';'.join(i.get('additional_urls') or []); i['verified'] = ''
                w.writerow(i)

    tracks = {t: sum(1 for r in rows if r['track'] == t) for t in ('llm', 'marl')}
    unknown = sorted(set(tags) - {r['key'] for r in rows})
    if unknown: print("existing_tags keys not in papers:", ', '.join(unknown))
    print(f"slices: {len(groups)}  queries: {len(log)}  papers: {len(rows)} {tracks}  "
          f"mechanisms updated: {len(mech) - len(missing)}/{len(mech)}  incidents: {n_inc}")
    if missing: print("NOT updated (no slice covered them):", ', '.join(missing))

if __name__ == '__main__':
    main(sys.argv[1])
