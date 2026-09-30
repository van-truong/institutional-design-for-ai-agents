#!/usr/bin/env python3
"""Build the verifier's work queue (verify_queue.csv) from the merged Phase 2 data.

Usage:  python3 taxonomy/scripts/build_verify_queue.py

Rows are ordered by priority (1 = check first):
  1  mechanisms placed by judgment (match=assigned); evidence that cites a paper key not in papers.csv
  2  mechanisms whose seed claims the search could not confirm; papers not confirmed from an opened page
     or named in a slice's to-verify notes; news incidents
  3  mechanisms whose llm_status changed from the seed
  4  everything else
Fill in `verdict` (ok / fix / drop) and `verifier_notes`; then copy initials + date into the
record's `verified` field in mechanisms.csv / papers.csv / incidents.csv.
"""
import csv, glob, io, json, os, re, subprocess

HERE = os.path.dirname(os.path.abspath(__file__)); TAX = os.path.dirname(HERE)
FLAG_WORDS = re.compile(r'mischaracteri|not supported|could not|cannot support|does not|no .{0,20}in the paper|unverified', re.I)

def read(name): return list(csv.DictReader(open(os.path.join(TAX, name))))

def seed_status():
    # Compare against the Phase 1 seed commit, not HEAD (HEAD already holds merged search results).
    try:
        git = lambda *a: subprocess.run(['git', *a], cwd=TAX, capture_output=True, text=True, check=True).stdout
        rev = git('log', '--format=%H', '--grep=seed', '--', 'mechanisms.csv').split()[-1]
        txt = subprocess.run(['git', 'show', f'{rev}:taxonomy/mechanisms.csv'], cwd=TAX, capture_output=True, text=True, check=True).stdout
        return {r['id']: r['llm_status'] for r in csv.DictReader(io.StringIO(txt))}
    except Exception:
        return {}

def main():
    mech, papers, inc = read('mechanisms.csv'), read('papers.csv'), read('incidents.csv')
    keys = {p['key'] for p in papers}
    slice_notes = ' '.join(json.load(open(g)).get('notes', '') for g in glob.glob(os.path.join(TAX, 'search_raw', 'G*.json')))
    seed = seed_status(); rows = []

    def add(pri, kind, rid, label, why, url, check):
        rows.append(dict(priority=pri, kind=kind, id=rid, label=label, why=why, url=url, check=check, verdict='', verifier_notes=''))

    for m in mech:
        ev = m['llm_evidence'] + ' ' + m['marl_evidence']
        cited = set(re.findall(r'\b[a-z]+\d{4}[a-z0-9]*\b', ev))
        dangling = sorted(cited - keys)
        why = []
        if m['match'] == 'assigned': why.append('primitive assigned by judgment')
        if dangling: why.append('evidence cites keys not in papers.csv: ' + ', '.join(dangling))
        pri = 1 if why else None
        if FLAG_WORDS.search(m['notes'].split('seed claims checked:')[-1]) and 'seed claims checked:' in m['notes']:
            why.append('seed claim not confirmed by search'); pri = pri or 2
        old = seed.get(m['id'])
        if old is not None and old != m['llm_status']:
            why.append(f'llm_status {old} -> {m["llm_status"]}'); pri = pri or 3
        if old is None and m['sources'] == 'search': why.append('added in Phase 2'); pri = 1
        add(pri or 4, 'mechanism', m['id'], m['name'], '; '.join(why) or 'routine',
            '', f'primitive fit; llm_status={m["llm_status"]} / marl_status={m["marl_status"]} supported by cited papers; '
                'functions/channels/dilemmas (pre-coded from primitive)')

    for p in papers:
        why = []
        if not p['located_via'].startswith('opened page') or 'abstract only' in p['located_via']:
            why.append(f'located via: {p["located_via"]}')
        if p['key'] in slice_notes or (p['arxiv_id'] and p['arxiv_id'] in slice_notes):
            why.append('named in slice to-verify notes')
        if len(p['groups'].split(';')) > 1: why.append('found by several slices: ' + p['groups'])
        pri = 2 if any(not w.startswith('found by') for w in why) else 4
        add(pri, f'paper ({p["track"]})', p['key'], f'{p["title"]} ({p["year"]}, {p["venue"]})', '; '.join(why) or 'routine',
            p['url'], f'title/authors/venue/year; finding: "{p["finding"][:160]}"; mapped to {p["mechanism_ids"]}')

    for i in inc:
        add(2, 'incident', i['key'], f'{i["date"]} {i["headline"]}', 'news track; unverified secondary reporting',
            i['url'], 'primary source exists and matches the summary; date; multi_agent flag')

    rows.sort(key=lambda r: (r['priority'], r['kind'] != 'mechanism', r['kind'], r['id']))
    out = os.path.join(TAX, 'verify_queue.csv')
    with open(out, 'w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
    by = {}
    for r in rows: by[(r['priority'], r['kind'].split(' ')[0])] = by.get((r['priority'], r['kind'].split(' ')[0]), 0) + 1
    print(f'{len(rows)} rows ->', out)
    for k in sorted(by): print(f'  priority {k[0]} {k[1]}: {by[k]}')

if __name__ == '__main__':
    main()
