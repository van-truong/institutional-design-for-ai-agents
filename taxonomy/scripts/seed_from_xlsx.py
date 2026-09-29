#!/usr/bin/env python3
"""Phase 1 seed: build primitives.csv, mechanisms.csv, pathologies.csv from the
original working spreadsheet (private; not in the repo).

Usage:  python3 taxonomy/scripts/seed_from_xlsx.py <path/to/2026-04-07_Sanctioning_taxonomy.xlsx>

Backbone = the 17 first-principles primitives. Each Overview-sheet mechanism is merged
into its matching first-principles instantiation, or added as a new record with an
explicitly assigned primitive (match=assigned). See taxonomy/PROTOCOL.md.
Reads the .xlsx with the standard library only (no openpyxl).
"""
import csv, difflib, os, re, sys, zipfile, xml.etree.ElementTree as ET

HERE = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.dirname(HERE)
NS = {"m": "http://schemas.openxmlformats.org/spreadsheetml/2006/main",
      "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships"}

# primitive -> (functions, channels, dilemmas, search terms) defaults; verified per record later
PRIM_DEFAULTS = {
 1:  ("monitoring", "epistemic", "second_order;extractive;contributive", '"reputation" OR "monitoring" OR "gossip" OR "audit log" OR transparency'),
 2:  ("sanctions;constraints", "social;constraint", "extractive;contributive", 'exclusion OR ostracism OR "partner selection" OR banning OR denylist'),
 3:  ("sanctions", "incentive", "extractive;contributive", 'punishment OR "costly punishment" OR fine OR penalty OR slashing'),
 4:  ("sanctions", "incentive", "contributive", 'reward OR subsidy OR praise OR "positive incentive"'),
 5:  ("sanctions", "incentive;normative", "extractive;contributive;repair", '"graduated sanction*" OR escalat* OR throttl* OR "back-off"'),
 6:  ("norms;constraints", "constraint;normative", "extractive;coordination", 'commitment OR pledge OR "rate limit*" OR "smart contract" OR deposit OR bond'),
 7:  ("sanctions", "social;incentive", "contributive;second_order", '"collective punishment" OR "group liability" OR "collective liability"'),
 8:  ("reputation", "social;incentive", "contributive;extractive", '"tit-for-tat" OR reciprocity OR "conditional cooperation" OR "win-stay"'),
 9:  ("adjudication;norms", "normative;social", "second_order;coordination", 'voting OR election OR legitimacy OR "democratic" OR "institutional choice"'),
 10: ("monitoring;repair", "epistemic;incentive", "second_order;repair;collusion", 'whistleblow* OR leniency OR confession OR disclosure OR apology'),
 11: ("repair", "restorative", "repair", 'restitution OR reintegration OR rehabilitation OR "restorative" OR forgiveness'),
 12: ("sanctions;norms", "social;normative", "second_order", 'metanorm OR "second-order punishment" OR "antisocial punishment" OR "punish non-punishers"'),
 13: ("adjudication", "restorative;normative", "repair;second_order", 'appeal OR arbitration OR mediation OR "dispute resolution" OR contestab*'),
 14: ("norms", "normative", "extractive;contributive", '"norm internali*" OR universali* OR "moral reasoning" OR "social norm"'),
 15: ("norms", "social", "coordination;contributive", 'imitation OR "strategy evolution" OR "cultural evolution" OR tournament'),
 16: ("constraints;sanctions", "incentive;constraint", "contributive;extractive;collusion", '"mechanism design" OR VCG OR "quadratic funding" OR auction OR "incentive compatible"'),
 17: ("repair;reputation", "social;restorative", "contributive;repair", '"mutual aid" OR solidarity OR "gift economy" OR timebank* OR cooperative'),
}
# pathology -> primitives it targets (from the 'Original Mechanism Targeted' column)
PATH_TO_PRIM = {1:[3,1,4], 2:[5,3], 3:[1,3], 4:[4,16], 5:[1], 6:[1], 7:[4,2], 8:[1],
                9:[1,3], 10:[1], 11:[3,12], 12:[9,3], 13:[3,5], 14:[2], 15:[3]}

# Overview mechanisms that are not the same as a first-principles instantiation.
# ("merge", "<substring of target instantiation>") folds into that record;
# ("assign", n) creates a new record under primitive n.
OVERRIDES = {
 "Voluntary public commitment": ("assign", 6),
 "Warning (1st violation)": ("merge", "Ostrom graduated sanctions"),
 "Escalating fine": ("merge", "Ostrom graduated sanctions"),
 "Collective punishment": ("merge", "Collective punishment"),
 "Liquidated damages": ("merge", "Pre-agreed contractual penalty"),
 "Civil law penalty clause": ("merge", "Pre-agreed contractual penalty"),
 "LD enforceable, penalty void": ("merge", "Pre-agreed contractual penalty"),
 "Cross-default (collective liability)": ("merge", "Cross-default"),
 "Carrot/stick choice (Andreoni)": ("assign", 4),
 "Moral hazard premium": ("assign", 16),
 "Fermi imitation (strategy copying)": ("merge", "Fermi imitation"),
 "TFT / WSLS (conditional)": ("merge", "Tit-for-Tat"),
 "Hard rate limit (API/bandwidth)": ("assign", 6),
 "Governance graph (institutional AI)": ("merge", "Governance graph"),
 "Restaking & correlated slash": ("assign", 3),
 "Token toxicity (network security)": ("merge", "Token toxicity"),
 "Timebanking (service credits)": ("merge", "Timebanking"),
 "Solidarity & mutual accountability": ("assign", 17),
 "Reputational indirect reciprocity": ("assign", 8),
 "Blockchain-based mutual aid DAO": ("assign", 17),
 "Repair": ("merge", "Material repair & restitution"),
 "Restitution": ("merge", "Material repair & restitution"),
 "Reintegration": ("merge", "Rehabilitation programme"),
 "Truth-telling": ("merge", "Truth & reconciliation"),
 "Rehabilitation after breach": ("merge", "Rehabilitation programme"),
}
FAMILY_FROM_SECTION = {"1": "social", "2": "formal", "3": "economic", "4": "technical", "5": "mutual_aid", "6": "restorative"}

def read_xlsx(path):
    z = zipfile.ZipFile(path)
    ss = [''.join(t.text or '' for t in si.iter('{%s}t' % NS['m']))
          for si in ET.fromstring(z.read('xl/sharedStrings.xml')).findall('m:si', NS)]
    wb = ET.fromstring(z.read('xl/workbook.xml'))
    rels = {r.get('Id'): r.get('Target') for r in ET.fromstring(z.read('xl/_rels/workbook.xml.rels'))}
    c2i = lambda c: sum((ord(ch) - 64) * 26 ** i for i, ch in enumerate(reversed(c))) - 1
    sheets = {}
    for sh in wb.find('m:sheets', NS):
        rows = []
        for row in ET.fromstring(z.read('xl/' + rels[sh.get('{%s}id' % NS['r'])])).iter('{%s}row' % NS['m']):
            d = {}
            for c in row.findall('m:c', NS):
                v = c.find('m:v', NS); t = c.get('t')
                d[c2i(re.match(r'[A-Z]+', c.get('r')).group())] = (
                    (ss[int(v.text)] if t == 's' and v is not None else (v.text if v is not None else '')) or '').strip()
            vals = [d.get(k, '') for k in range(max(d) + 1)] if d else []
            if any(vals): rows.append(vals)
        sheets[sh.get('name')] = rows
    return sheets

def records(rows):
    """Yield (section, description, header->value dict) for data rows."""
    sec = desc = hdr = None
    for vals in rows:
        filled = [v for v in vals if v]
        if len(filled) == 1 and re.match(r'^\d+\.\s', filled[0]): sec, desc = filled[0], None; continue
        if filled and filled[0] in ('#', 'Mechanism'): hdr = [re.sub(r'\s+', ' ', h.split('\n')[0]).strip() for h in vals]; continue
        if len(filled) == 1 and sec: desc = desc or filled[0]; continue
        if hdr and sec and len(filled) >= 2:
            yield sec, desc, {h: vals[i] for i, h in enumerate(hdr) if h and i < len(vals)}

def llm_status(text):
    t = text.lower().strip()
    if not t: return ''
    if t.startswith('✓') or 'directly tested' in t or re.match(r'^tested', t): return 'tested'
    if t.startswith(('partial', 'implicit')) or 'partially' in t: return 'partial'
    if t.startswith('discussed') or 'design recommendation' in t: return 'discussed'
    if t.startswith(('not', 'no ')) or 'not yet' in t or 'not tested' in t: return 'untested'
    return 'partial'

def family_from_domain(dom):
    d = dom.lower()
    if 'restorative' in d: return 'restorative'
    if 'solidarity' in d: return 'mutual_aid'
    if d.startswith(('technical', 'computational')): return 'technical'
    if d.startswith(('economic', 'behavioural')): return 'economic'
    if d.startswith(('social', 'cognitive', 'evolutionary')): return 'social'
    return 'formal'

def valence(v):
    v = v.lower()
    for k in ('punishment', 'reward', 'hybrid', 'structural'):
        if v.startswith(k[:4]): return k
    return v

def main(xlsx):
    S = read_xlsx(xlsx)
    fp = list(records(S['First Principles Taxonomy']))
    ov = list(records(S['Overview']))
    bad = list(records(S['Bad Effects of Sanctioning']))

    prims = {}
    for sec, desc, r in fp:
        n = int(sec.split('.')[0]); prims.setdefault(n, (re.sub(r'^\d+\.\s*', '', sec), desc or ''))
    mech = []; counter = {}
    for sec, desc, r in fp:
        n = int(sec.split('.')[0]); counter[n] = counter.get(n, 0) + 1
        fn, ch, dl, _ = PRIM_DEFAULTS[n]
        mech.append(dict(id=f"P{n:02d}-{counter[n]:02d}", name=r.get('Instantiation', ''), primitive_id=n,
            primitive=prims[n][0], discipline_family=family_from_domain(r.get('Domain', '')), domain=r.get('Domain', ''),
            valence=valence(r.get('P / R / S', '')), game_type=r.get('Game type', ''), functions=fn, channels=ch,
            dilemmas=dl, human_example='', key_references=r.get('Key references & examples', ''),
            llm_status=llm_status(r.get('LLM testing status', '')), llm_evidence=r.get('LLM testing status', ''),
            marl_status='', ai_analogue='', sources='first_principles', match='exact',
            precoded='functions;channels;dilemmas', verified='', notes=''))

    def find(sub):
        hits = [m for m in mech if sub.lower() in m['name'].lower()]
        return hits[0] if hits else None
    def fuzzy(name):
        best = max(mech, key=lambda m: difflib.SequenceMatcher(None, name.lower(), m['name'].lower()).ratio())
        a = set(re.findall(r'[a-z0-9]+', name.lower())); b = set(re.findall(r'[a-z0-9]+', best['name'].lower()))
        j = len(a & b) / max(1, len(a | b))
        return best if (j >= 0.34 or difflib.SequenceMatcher(None, name.lower(), best['name'].lower()).ratio() >= 0.62) else None

    merges = []
    for sec, desc, r in ov:
        name = r.get('Mechanism', ''); fam = FAMILY_FROM_SECTION.get(sec.split('.')[0], '')
        ex = r.get('Human world example') or r.get('Example / literature', '')
        ov_llm = r.get('Tested in multi-agent LLM systems?', '')
        rule = OVERRIDES.get(name)
        target = find(rule[1]) if rule and rule[0] == 'merge' else (None if rule else fuzzy(name))
        if target is not None:
            target['sources'] = 'overview;first_principles'
            target['match'] = 'exact' if name.lower() in target['name'].lower() else 'fuzzy'
            target['discipline_family'] = fam or target['discipline_family']
            if ex: target['human_example'] = (target['human_example'] + ' | ' if target['human_example'] else '') + ex
            if name.lower() not in target['name'].lower():
                target['notes'] = (target['notes'] + '; ' if target['notes'] else '') + f'merged Overview "{name}"'
            if not target['game_type']: target['game_type'] = r.get('What game structure does it apply to?', '')
            merges.append((name, target['name'], target['match']))
            continue
        n = rule[1] if rule else 1
        counter[n] = counter.get(n, 0) + 1; fn, ch, dl, _ = PRIM_DEFAULTS[n]
        mech.append(dict(id=f"P{n:02d}-{counter[n]:02d}", name=name, primitive_id=n, primitive=prims[n][0],
            discipline_family=fam, domain='', valence=valence(r.get('Does the mechanism cost the target or benefit them?', '')),
            game_type=r.get('What game structure does it apply to?', ''), functions=fn, channels=ch, dilemmas=dl,
            human_example=ex, key_references='', llm_status=llm_status(ov_llm), llm_evidence=ov_llm, marl_status='',
            ai_analogue='', sources='overview', match='assigned', precoded='functions;channels;dilemmas', verified='',
            notes='primitive assigned by judgment; verify' if rule else 'no override and no fuzzy match; defaulted to primitive 1; verify'))
        merges.append((name, f'NEW under primitive {n}', 'assigned'))

    mech.sort(key=lambda m: m['id'])
    cols = list(mech[0].keys())
    with open(os.path.join(OUT, 'mechanisms.csv'), 'w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=cols); w.writeheader(); w.writerows(mech)

    prim_paths = {n: [] for n in prims}
    for pid, targets in PATH_TO_PRIM.items():
        for n in targets: prim_paths[n].append(f"X{pid:02d}")
    with open(os.path.join(OUT, 'primitives.csv'), 'w', newline='') as f:
        w = csv.writer(f); w.writerow(['primitive_id', 'primitive', 'description', 'default_functions',
                                       'default_channels', 'default_dilemmas', 'search_terms', 'pathology_ids'])
        for n in sorted(prims):
            fn, ch, dl, q = PRIM_DEFAULTS[n]
            w.writerow([n, prims[n][0], prims[n][1], fn, ch, dl, q, ';'.join(prim_paths[n])])

    with open(os.path.join(OUT, 'pathologies.csv'), 'w', newline='') as f:
        w = csv.writer(f); w.writerow(['pathology_id', 'pathology', 'mechanisms_targeted', 'domain', 'failure_type',
                                       'game_type', 'llm_status', 'llm_evidence', 'key_references', 'primitive_ids'])
        for i, (sec, desc, r) in enumerate(bad, 1):
            w.writerow([f"X{i:02d}", r.get('Pathology', ''), r.get('Original Mechanism Targeted', ''), r.get('Domain', ''),
                        r.get('Failure Type', ''), r.get('Game Type', ''), llm_status(r.get('LLM Testing Status', '')),
                        r.get('LLM Testing Status', ''), r.get('Key References & Examples', ''),
                        ';'.join(str(n) for n in PATH_TO_PRIM.get(i, []))])

    with open(os.path.join(OUT, 'seed_merge_log.csv'), 'w', newline='') as f:
        w = csv.writer(f); w.writerow(['overview_mechanism', 'merged_into', 'match']); w.writerows(merges)
    print(f"primitives: {len(prims)}  mechanisms: {len(mech)}  pathologies: {len(bad)}  overview merges: "
          f"{sum(1 for m in merges if m[2] != 'assigned')}  new (assigned): {sum(1 for m in merges if m[2] == 'assigned')}")

if __name__ == '__main__':
    main(sys.argv[1])
