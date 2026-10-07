#!/usr/bin/env python3
"""Build docs/assets/phenomena.json for the website's interactive group-level-phenomena section.

Groups the phenomenon-coded instances by type and substrate (human / MARL / LLM), with paper links, and attaches
documented real-world incidents to the failure types. Mirrors the paper's phenomena figure (gen_phenomena.py).
Usage:  python3 taxonomy/scripts/build_phenomena_data.py
"""
import csv, json, os

HERE = os.path.dirname(os.path.abspath(__file__)); TAX = os.path.dirname(HERE); ROOT = os.path.dirname(TAX)
OUT = os.path.join(ROOT, 'docs', 'assets', 'phenomena.json')

# phenomenon types: key, label, valence, one-line description (order = paper's figure)
TYPES = [
    ('comm_language', 'Emergent communication & language', 'neutral',
     'Agents invent signals, protocols, or a shared language without being given one.'),
    ('convention_coord', 'Conventions & coordination', 'neutral',
     'Groups settle on shared conventions, norms, or equilibria through repeated interaction.'),
    ('social_structure', 'Social structure: networks, hierarchy, roles', 'neutral',
     'Networks, hierarchies, elites, and roles emerge from who interacts with whom.'),
    ('culture', 'Culture, norms & individuality', 'neutral',
     'Cultures, individual identities, and transmitted behavior develop across a population.'),
    ('collective_intel', 'Collective intelligence & performance', 'neutral',
     'Group problem-solving that can exceed, or fall short of, the individual agents.'),
    ('economy', 'Emergent economy & resource use', 'neutral',
     'Markets, trade, bartering, and resource dynamics arise among agents (and people).'),
    ('cooperation', 'Spontaneous cooperation', 'beneficial',
     'Agents cooperate or act prosocially even when they could defect.'),
    ('conformity_bias', 'Conformity & collective bias', 'harmful',
     'Groups converge on biased or mistaken consensus, or amplify one another’s errors.'),
    ('collusion_deception', 'Collusion, deception & manipulation', 'harmful',
     'Agents coordinate against oversight, collude, or deceive one another or people.'),
    ('harm', 'Emergent harm: toxicity, fragility, breakout', 'harmful',
     'Toxic dynamics, fragile networks, or agents acting outside their intended scope.'),
]
# documented incidents (keys in incidents.csv) -> (phenomenon types, short display headline). Each carries its
# setting from incidents.csv (real_world, controlled_evaluation, researcher_demo) so the figure can tell live systems
# from tests. Human-directed misuse (e.g. the GTG-1002 espionage case) is left out: it did not emerge among agents.
INCIDENT_TYPES = {
    'emergence-collusion-sim': (['collusion_deception'], 'Agents coordinate to break containment'),
    'metr-redwood-agent-message-board': (['collusion_deception'], 'Agents ran a hidden message board to cheat an eval'),
    'servicenow-agent-to-agent-injection': (['collusion_deception'], 'Hijacked agent recruits more-privileged agents'),
    'openai-hf-intrusion-2026': (['harm'], 'Autonomous agents breached production infrastructure'),
    'openai-dsewiki-breakout': (['harm'], 'Agents hijacked a live website (breakout)'),
    'anthropic-multiagent-turf-wars': (['social_structure'], 'Multi-agent “turf wars” among agents with conflicting tasks'),
}


def link(r):
    for f, prefix in (('url', ''), ('doi', 'https://doi.org/'), ('arxiv_id', 'https://arxiv.org/abs/')):
        v = (r.get(f) or '').strip()
        if v and v.lower() != 'null':
            return v if f == 'url' else prefix + v
    return ''


def source(r):
    return dict(title=r['title'], authors=r['authors'], year=r['year'], venue=r['venue'], url=link(r),
                discipline=r['discipline'].replace('_', ' '))


def main():
    inst = {r['instance_id']: r for r in csv.DictReader(open(os.path.join(TAX, 'instances.csv')))}
    tags = {r['instance_id']: r for r in csv.DictReader(open(os.path.join(TAX, 'coding', 'phenomena_tags.csv')))}
    incs = {r['key']: r for r in csv.DictReader(open(os.path.join(TAX, 'incidents.csv')))}
    order = {'llm': 0, 'marl': 1, 'human': 2}

    types = []
    for key, label, valence, desc in TYPES:
        subs = {'human': [], 'marl': [], 'llm': []}
        for iid, t in tags.items():
            if t['phenomenon_type'] != key:
                continue
            r = inst[iid]
            sub = (r['agent_type'] or 'other')
            subs.setdefault(sub, []).append(source(r))
        for v in subs.values():
            v.sort(key=lambda s: -(int(s['year']) if str(s['year']).isdigit() else 0))
        incidents = [k for k, (tys, _) in INCIDENT_TYPES.items() if key in tys]
        types.append(dict(key=key, label=label, valence=valence, description=desc,
                          counts={s: len(subs.get(s, [])) for s in ('human', 'marl', 'llm')},
                          total=sum(len(v) for v in subs.values()),
                          sources={s: subs.get(s, []) for s in ('llm', 'marl', 'human')},
                          incidents=incidents))
    incidents = []
    for k, (tys, short) in INCIDENT_TYPES.items():
        r = incs.get(k, {})
        incidents.append(dict(key=k, short=short, year=(r.get('date', '') or '')[:4],
                              url=link(r) or r.get('url', ''), category=r.get('category', ''),
                              setting=r.get('setting', ''), types=tys))

    total = sum(t['total'] for t in types)
    data = dict(substrates=[['human', 'Humans'], ['marl', 'MARL agents'], ['llm', 'LLM agents']],
                valences=[['beneficial', 'beneficial'], ['neutral', 'neutral / surprising'], ['harmful', 'harmful']],
                types=types, incidents=incidents,
                counts=dict(total=total,
                            harmful=sum(t['total'] for t in types if t['valence'] == 'harmful'),
                            beneficial=sum(t['total'] for t in types if t['valence'] == 'beneficial')))
    json.dump(data, open(OUT, 'w'), ensure_ascii=False, separators=(',', ':'))
    print(f"wrote {os.path.relpath(OUT, ROOT)}: {total} phenomena across {len(types)} types, "
          f"{len(incidents)} incidents, {os.path.getsize(OUT)//1024} KB")
    build_informal({k for k, *_ in TYPES})


# Draft supplementary slice (taxonomy/phenomena_informal.csv, see coding/INFORMAL_SLICE.md): informal reports and
# automated systems outside AI research, kept as a separate evidence tier and shown on the website only when a
# visitor opts in. Proposed new types ("new:<name>") are passed through with their own labels.
OUT_INFORMAL = os.path.join(ROOT, 'docs', 'assets', 'phenomena_informal.json')
SUBSTRATE_LABEL = {'llm': 'LLM agents', 'marl': 'MARL agents', 'rl_other': 'RL pricing agents',
                   'abm': 'agent-based model', 'alife': 'artificial life', 'robots': 'robot swarm',
                   'bots_in_the_wild': 'bots in the wild', 'distributed_systems': 'distributed systems'}
NEW_TYPE_DESC = {
    'conversational attractor': 'Agent-to-agent dialogue converges on a self-reinforcing theme without outside input.',
    'inter-agent conflict': 'Agents built to help persistently undo or contest each other’s work.',
    'collective identity': 'Agents running the same model identify with each other as one collective agent.',
}


def build_informal(known):
    path = os.path.join(TAX, 'phenomena_informal.csv')
    if not os.path.exists(path):
        return
    rows = list(csv.DictReader(open(path)))
    by_type, new_types = {}, {}
    for r in rows:
        key = r['phenomenon_type']
        if key.startswith('new:'):
            name = key[4:]
            key = 'new-' + name.replace(' ', '-')
            new_types.setdefault(key, dict(key=key, label=name[0].upper() + name[1:], valence=r['valence'],
                                           description=NEW_TYPE_DESC.get(name, '')))
        elif key not in known:
            continue
        by_type.setdefault(key, []).append(dict(
            id=r['instance_id'], title=r['title'], authors=r['authors_or_org'], date=r['date'], url=r['url'],
            substrate=r['substrate'], substrate_label=SUBSTRATE_LABEL.get(r['substrate'], r['substrate']),
            tier=r['evidence_tier'], valence=r['valence'], pattern=r['pattern']))
    data = dict(types=by_type, new_types=list(new_types.values()), total=len(rows),
                tiers={t: sum(r['evidence_tier'] == t for r in rows) for t in ('informal', 'peer_reviewed')})
    json.dump(data, open(OUT_INFORMAL, 'w'), ensure_ascii=False, separators=(',', ':'))
    print(f"wrote {os.path.relpath(OUT_INFORMAL, ROOT)}: {len(rows)} informal-slice instances, "
          f"{len(new_types)} proposed types")


if __name__ == '__main__':
    main()
