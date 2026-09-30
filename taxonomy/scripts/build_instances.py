#!/usr/bin/env python3
"""Build instances.csv: one row per documented use of a mechanism in one source (protocol v0.2).

Usage:  python3 taxonomy/scripts/build_instances.py

Inputs (in taxonomy/):
  search_raw/I_*.json   cross-disciplinary instance slices (copied here from the search dir)
  papers.csv            artificial-agent studies; one instance per (paper, mapped mechanism)
  mechanisms.csv        seed human examples, kept as origin=seed (sensitizing only)
Instances get stable ids (I0001, ...) ordered by origin, then source key. On a rebuild, an instance already in
instances.csv (same origin, source key and seed match) keeps its id and coding columns; only its source fields
are refreshed. New instances get the next free ids and blank coding columns, for the next coding pass.
Source-field changes to coded instances are listed in coding/rebuild_changes.csv so their codes can be reviewed.
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
    path = os.path.join(TAX, 'instances.csv')
    old = list(csv.DictReader(open(path))) if os.path.exists(path) else []
    cols = list(old[0].keys()) if old else COLS
    key = lambda r: (r['origin'], r['source_key'], r['seed_match'])
    prior = {key(r): r for r in old}
    source_fields = [c for c in COLS if c not in ('instance_id', 'code', 'mechanism', 'coder_notes', 'verified')]
    changes, next_id = [], max([int(r['instance_id'][1:]) for r in old] or [0]) + 1
    added = []
    for r in rows:
        was = prior.pop(key(r), None)
        if was is None:
            r['instance_id'] = f'I{next_id:04d}'; next_id += 1; added.append(r['instance_id'])
            continue
        for c in source_fields:
            if was.get(c, '') != r[c]:
                changes.append(dict(instance_id=was['instance_id'], field=c, old=was.get(c, ''), new=r[c]))
        r.update({c: was[c] for c in cols if c not in source_fields})
    if prior: print('dropped (no longer in the sources):', sorted(r['instance_id'] for r in prior.values()))
    rows.sort(key=lambda r: r['instance_id'])
    with open(path, 'w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=cols, extrasaction='ignore', restval=''); w.writeheader(); w.writerows(rows)
    with open(os.path.join(TAX, 'coding', 'rebuild_changes.csv'), 'w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=['instance_id', 'field', 'old', 'new']); w.writeheader(); w.writerows(changes)
    print(len(changes), 'source-field changes to existing instances;', len(added), 'new instances',
          f'({added[0]}-{added[-1]})' if added else '')
    by = {}
    for r in rows: by[r['origin']] = by.get(r['origin'], 0) + 1
    print(len(rows), 'instances:', by)
    disc = {}
    for r in rows: disc[r['discipline']] = disc.get(r['discipline'], 0) + 1
    print('by discipline:', dict(sorted(disc.items(), key=lambda x: -x[1])))

if __name__ == '__main__':
    main()
