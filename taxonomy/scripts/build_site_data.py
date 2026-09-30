#!/usr/bin/env python3
"""Build docs/assets/taxonomy.json for the website's interactive taxonomy.

Reads taxonomy/codebook.csv (mechanisms and themes) and taxonomy/instances.csv (the coded sources),
and takes the family grouping, colors, and short labels from manuscript/scripts/gen_taxonomy.py so the
website and the paper's Fig. 4 stay in step.

Usage:  python3 taxonomy/scripts/build_site_data.py
"""
import csv, json, os, sys
from datetime import date

HERE = os.path.dirname(os.path.abspath(__file__)); TAX = os.path.dirname(HERE); ROOT = os.path.dirname(TAX)
sys.path.insert(0, os.path.join(ROOT, 'manuscript', 'scripts'))
from gen_taxonomy import FAMILIES, COLUMNS, SHORT, THEME_SHORT, breadth  # noqa: E402

OUT = os.path.join(ROOT, 'docs', 'assets', 'taxonomy.json')
TRACK = {'llm': 'llm', 'marl': 'marl'}


def link(r):
    for f, prefix in (('url', ''), ('doi', 'https://doi.org/'), ('arxiv_id', 'https://arxiv.org/abs/')):
        v = (r.get(f) or '').strip()
        if v and v.lower() != 'null':
            return v if f == 'url' else prefix + v
    return ''


def source(r):
    agent = (r['agent_type'] or '').split(';')[0]
    return dict(title=r['title'], authors=r['authors'], year=r['year'], venue=r['venue'], url=link(r),
                agent=TRACK.get(agent, 'other'), discipline=r['discipline'].replace('_', ' '),
                evidence=r.get('evidence_type', ''), seed=r['origin'] == 'seed')


def llm_status(r):
    if int(r['llm_tested_studies'] or 0): return 'tested'
    if int(r['llm_proposed_studies'] or 0): return 'proposed'
    return 'none'


def main():
    book = list(csv.DictReader(open(os.path.join(TAX, 'codebook.csv'))))
    inst = list(csv.DictReader(open(os.path.join(TAX, 'instances.csv'))))
    # Same rule as pass2_compare.py: instances coded as a mechanism or configuration, listed under their
    # primary mechanism and under each secondary lever.
    by_mech = {}
    fin = [r for r in inst if r['kind'] in ('mechanism', 'configuration') and r.get('title')]
    for r in fin:
        by_mech.setdefault(r['mechanism'], []).append((r, 'primary'))
    for r in fin:
        for mid in filter(None, (r.get('secondary_p2') or '').split(';')):
            if mid != r['mechanism']:
                by_mech.setdefault(mid, []).append((r, 'secondary'))
    order = {'llm': 0, 'marl': 1, 'other': 2}
    themes = {}
    for m in book:
        rows, seen = [], set()
        for r, role in by_mech.get(m['mechanism_id'], []):
            key = r['source_key'] or r['title']
            if key in seen: continue
            seen.add(key); rows.append(dict(source(r), secondary=role == 'secondary'))
        rows.sort(key=lambda s: (order[s['agent']], s['secondary'], s['seed'], -int(s['year']) if str(s['year']).isdigit() else 0))
        disciplines = sorted({d.split(':')[0].replace('_', ' ') for d in (m.get('disciplines_all') or m['disciplines']).split(';') if d})
        themes.setdefault(m['theme_id'], dict(id=m['theme_id'], name=THEME_SHORT.get(m['theme'], m['theme']), mechanisms=[]))
        themes[m['theme_id']]['mechanisms'].append(dict(
            id=m['mechanism_id'], name=m['mechanism'], short=SHORT.get(m['mechanism'], m['mechanism']),
            definition=m['definition'], llm=llm_status(m), n_llm_tested=int(m['llm_tested_studies'] or 0),
            breadth=breadth(m), disciplines=disciplines, sources=rows))
    families = [dict(id=f, label=lab, dark=dark, mid=mid, column=next(i for i, c in enumerate(COLUMNS) if f in c),
                     themes=[themes[t] for t in tids])
                for f, (lab, dark, mid, tids) in FAMILIES.items()]
    n_src = len({(s['title']) for f in families for t in f['themes'] for m in t['mechanisms'] for s in m['sources']})
    data = dict(generated=date.today().isoformat(), columns=COLUMNS,
                counts=dict(mechanisms=len(book), themes=len(themes), instances=len(fin),
                            corpus=sum(1 for r in inst if r.get('kind')),
                            sources=n_src),
                families=families)
    json.dump(data, open(OUT, 'w'), ensure_ascii=False, separators=(',', ':'))
    print(f"wrote {os.path.relpath(OUT, ROOT)}: {data['counts']}, {os.path.getsize(OUT)//1024} KB")


if __name__ == '__main__':
    main()
