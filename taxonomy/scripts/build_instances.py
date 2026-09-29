#!/usr/bin/env python3
"""Build instances.csv: one row per documented use of a mechanism in one source (protocol v0.2).

Usage:  python3 taxonomy/scripts/build_instances.py

Inputs (in taxonomy/):
  search_raw/I_*.json   cross-disciplinary instance slices (copied here from the search dir)
  papers.csv            artificial-agent studies; one instance per (paper, mapped mechanism)
  mechanisms.csv        seed human examples, kept as origin=seed (sensitizing only)
Instances get stable ids (I0001, ...) ordered by origin, then source key.
Coding columns (code, mechanism, coder_notes) are left blank for the coding pass.
"""
import csv, glob, json, os, re

HERE = os.path.dirname(os.path.abspath(__file__)); TAX = os.path.dirname(HERE)
COLS = ['instance_id', 'origin', 'source_key', 'title', 'authors', 'year', 'venue', 'url', 'doi', 'arxiv_id',
        'discipline', 'field_of_use', 'agent_type', 'description', 'lever', 'who_acts', 'timing', 'valence',
        'evidence', 'pathology', 'seed_match', 'themes', 'located_via', 'code', 'mechanism', 'coder_notes', 'verified']
FAMILY_TO_DISCIPLINE = {'social': 'sociology', 'formal': 'law', 'economic': 'economics', 'technical': 'computer_science',
                        'mutual_aid': 'sociology', 'restorative': 'law'}

# Corrections to slice output, checked against the arXiv API (search_raw/ stays verbatim).
AUTHOR_FIXES = {'Adrian de Valois-Franklin et al.': 'Adrian de Valois-Franklin & Alex Bogdan',
                'J. de Curto et al.': 'J. de Curtò & I. de Zarzà'}

def clean(v):
    if v is None: return ''
    if isinstance(v, list): return ';'.join(map(str, v))
    return str(v)

def main():
    rows = []
    for g in sorted(glob.glob(os.path.join(TAX, 'search_raw', 'I_*.json'))):
        d = json.load(open(g))
        for i in d.get('instances', []):
            r = {c: clean(i.get(c)) for c in COLS}
            r['origin'] = d.get('slice', os.path.basename(g)[:-5])
            r['authors'] = AUTHOR_FIXES.get(r['authors'], r['authors'])
            rows.append(r)

    mech = {m['id']: m for m in csv.DictReader(open(os.path.join(TAX, 'mechanisms.csv')))}
    for p in csv.DictReader(open(os.path.join(TAX, 'papers.csv'))):
        for mid in [x for x in p['mechanism_ids'].split(';') if x] or ['']:
            if not mid and not p['themes']: continue
            rows.append(dict({c: '' for c in COLS}, origin='search_' + p['track'], source_key=p['key'], title=p['title'],
                             authors=p['authors'], year=p['year'], venue=p['venue'], url=p['url'], doi=p['doi'],
                             arxiv_id=p['arxiv_id'], discipline='ai_ml', field_of_use='multi-agent ' + p['track'],
                             agent_type=p['track'], description=p['how_tested'], evidence=p['finding'],
                             seed_match=mid, themes=p['themes'], located_via=p['located_via']))

    for m in mech.values():
        ex = m['human_example'].strip()
        if not ex: continue
        desc = ex.split('\n')[0].strip()
        refs = re.findall(r'https?://\S+', ex)
        rows.append(dict({c: '' for c in COLS}, origin='seed', source_key=m['id'], title=m['name'],
                         discipline=FAMILY_TO_DISCIPLINE.get(m['discipline_family'], ''), field_of_use=m['domain'],
                         agent_type='human', description=desc, valence=m['valence'], url=refs[0] if refs else '',
                         evidence=m['key_references'], seed_match=m['id'], located_via='seed spreadsheet'))

    order = {'seed': 9}
    rows.sort(key=lambda r: (order.get(r['origin'], 0), r['origin'], r['source_key'], r['seed_match']))
    for n, r in enumerate(rows, 1): r['instance_id'] = f'I{n:04d}'
    with open(os.path.join(TAX, 'instances.csv'), 'w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=COLS); w.writeheader(); w.writerows(rows)
    by = {}
    for r in rows: by[r['origin']] = by.get(r['origin'], 0) + 1
    print(len(rows), 'instances:', by)
    disc = {}
    for r in rows: disc[r['discipline']] = disc.get(r['discipline'], 0) + 1
    print('by discipline:', dict(sorted(disc.items(), key=lambda x: -x[1])))

if __name__ == '__main__':
    main()
