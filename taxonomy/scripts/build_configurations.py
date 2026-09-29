#!/usr/bin/env python3
"""Build configurations.csv: named combinations of mechanisms (protocol v0.2, configuration layer).

Usage:  python3 taxonomy/scripts/build_configurations.py   (run after collapse_codes.py)

A configuration is a set of mechanisms used or evaluated together. Mechanisms stay single
levers; configurations record how levers combine.
  evaluation   combination_tested  the combination was compared with its parts
               comparison          several single levers were compared side by side
               system              a deployed or specified system (descriptive)
               proposal            proposed, not tested
               review / theory     synthesis of other studies, or a formal model
  interaction  complementary       together better than either alone, or one needs the other
               substitute          either does the same job
               interference        one lever undermines another
               not_assessed        the source does not say
Interaction codes are taken only from the source's reported evidence (see instances.csv);
`interaction_evidence` quotes that evidence.
Also writes the `configuration` column of instances.csv.
"""
import csv, os

HERE = os.path.dirname(os.path.abspath(__file__)); TAX = os.path.dirname(HERE)

# id, name, instance_ids, mechanisms, agent_type, discipline, evaluation, interaction, interaction_evidence
CONFIGS = [
 ('C01', 'Ostrom design principles', 'I0084;I0032', 'M13;M46;M42;M01;M44;M27;M51;M52', 'human', 'ecology_resource_management', 'review', 'complementary',
  'Long-enduring commons share the eight principles (Ostrom 1990); the principles are well supported across 91 studies (Cox et al. 2010).'),
 ('C02', 'Covenants with a sword', 'I0085', 'M33;M14;M42', 'human', 'economics', 'combination_tested', 'complementary',
  'Communication alone improves yields; communication plus self-chosen sanctioning is near-optimal; imposed sanctioning alone is overused.'),
 ('C03', 'Carrot and stick', 'I0003;I0096;I0008;I0512;I0529', 'M14;M21', 'human', 'economics', 'combination_tested', 'complementary',
  'Andreoni et al.: combination most effective, rewards and punishment are complements. Sefton et al.: combination gives the highest contributions.'),
 ('C04', 'Communication before punishment', 'I0058', 'M33;M14', 'human', 'ecology_resource_management', 'combination_tested', 'complementary',
  'Communication improves outcomes; punishment without communication does not.'),
 ('C05', 'Gossip and ostracism', 'I0045', 'M07;M08', 'human', 'psychology', 'combination_tested', 'complementary',
  'Gossip plus ostracism produces the highest cooperation.'),
 ('C06', 'Fine replacing a social norm', 'I0049', 'M16;M58', 'human', 'economics', 'combination_tested', 'interference',
  'Late arrivals increased after a fine was introduced and stayed high after it was removed.'),
 ('C07', 'Punishment with counter-punishment', 'I0079', 'M14;M50', 'human', 'economics', 'combination_tested', 'interference',
  'Fear of retaliation reduces punishment, and cooperation falls relative to punishment-only treatments.'),
 ('C08', 'Monitoring with conditional cooperators', 'I0094', 'M01;M41', 'human', 'ecology_resource_management', 'combination_tested', 'complementary',
  'Groups with more conditional cooperators invest more in patrols and have more productive forests.'),
 ('C09', 'Antitrust enforcement package', 'I0017', 'M16;M47;M48', 'human', 'law', 'comparison', 'not_assessed',
  'Leniency strengthens deterrence; rewards drive prices to competitive levels.'),
 ('C10', 'Deposit-refund (tax plus subsidy)', 'I0087', 'M17;M22', 'human', 'economics', 'combination_tested', 'complementary',
  'Deposit-refund reaches the waste target at about half the cost of disposal fees or recycling subsidies alone (simulation).'),
 ('C11', 'Extralegal merchant order', 'I0014', 'M51;M05;M08;M11', 'human', 'law', 'system', 'complementary',
  'Unpaid arbitration awards are posted publicly and lead to expulsion and boycott; the system handles nearly all disputes more cheaply than courts.'),
 ('C12', 'Managerial compliance model', 'I0025', 'M01;M58;M51', 'state', 'international_relations', 'theory', 'not_assessed', ''),
 ('C13', 'Peer pressure in partnerships', 'I0061', 'M18;M01', 'human', 'organizational_management', 'theory', 'complementary',
  'Theoretical: guilt and shame work through mutual monitoring.'),
 ('C14', 'Axelrod-Keohane cooperation under anarchy', 'I0004', 'M39;M38;M01', 'state', 'international_relations', 'theory', 'not_assessed', ''),
 ('C15', 'Commons governance functions', 'I0034', 'M01;M51;M46', 'human', 'ecology_resource_management', 'review', 'not_assessed', ''),
 ('C16', 'Robust peer-to-peer incentives', 'I0133', 'M39;M04', 'software', 'distributed_systems', 'system', 'not_assessed', ''),
 ('C17', 'Slashdot moderation and meta-moderation', 'I0157', 'M06;M50;M37', 'human', 'platform_governance', 'system', 'not_assessed', ''),
 ('C18', 'Twitch moderation toolkit', 'I0186', 'M34;M62;M09;M08', 'human', 'platform_governance', 'comparison', 'not_assessed',
  'Users imitated observed behavior, more from high-status users; proactive chat modes discouraged spam.'),
 ('C19', 'Wikipedia arbitration', 'I0194', 'M51;M44;M34', 'human', 'platform_governance', 'system', 'not_assessed', ''),
 ('C20', 'Oversight Board', 'I0156', 'M54;M58', 'organization', 'platform_governance', 'system', 'not_assessed', ''),
 ('C21', 'Open-source code of conduct', 'I0160', 'M58;M48;M52', 'human', 'computer_science', 'system', 'not_assessed', ''),
 ('C22', 'Proof-of-stake validation', 'I0131;I0507;I0449;I0450', 'M28;M27;M08;M22;M43', 'software', 'blockchain', 'system', 'not_assessed', ''),
 ('C23', 'Practical Byzantine fault tolerance', 'I0118', 'M43;M54;M56', 'software', 'distributed_systems', 'system', 'not_assessed', ''),
 ('C24', 'Token governance with timelock and guardian', 'I0122', 'M42;M34;M35', 'human', 'blockchain', 'system', 'not_assessed', ''),
 ('C25', 'CONFIDANT reputation and isolation', 'I0115', 'M05;M07;M12;M08', 'software', 'computer_science', 'system', 'not_assessed', ''),
 ('C26', 'Integrated trust model (FIRE)', 'I0147', 'M05;M07', 'software', 'ai_ml', 'system', 'not_assessed', ''),
 ('C27', 'Email sender authentication (DMARC)', 'I0179', 'M04;M01', 'organization', 'security', 'system', 'not_assessed', ''),
 ('C28', 'Agent visibility and infrastructure', 'I0213;I0214', 'M04;M01;M03;M30;M57;M56', 'llm', 'ai_ml', 'proposal', 'not_assessed', ''),
 ('C29', 'Decentralized agent governance (ETHOS)', 'I0210;I0211', 'M04;M34;M42;M51;M19', 'llm', 'ai_ml', 'proposal', 'not_assessed', ''),
 ('C30', 'Institutional AI governance', 'I0254', 'M01;M22;M16;M58;M44', 'llm', 'ai_ml', 'proposal', 'not_assessed', ''),
 ('C31', 'Agent identity and verification (PRIMUS)', 'I0202', 'M08;M04;M43', 'llm', 'ai_ml', 'proposal', 'not_assessed', ''),
 ('C32', 'Verify-then-pay commerce stack', 'I0226;I0220', 'M31;M34;M03;M05', 'llm', 'ai_ml', 'proposal', 'not_assessed', ''),
 ('C33', 'Sentinel oversight agents', 'I0230;I0227', 'M01;M35;M57;M08;M03', 'llm', 'ai_ml', 'system', 'not_assessed', ''),
 ('C34', 'Collusion auditing and channel limits', 'I0262;I0240', 'M02;M01', 'llm', 'ai_ml', 'system', 'not_assessed', ''),
 ('C35', 'Sandboxed agent economy', 'I0264;I0265', 'M34;M65;M01;M05;M35', 'llm', 'ai_ml', 'proposal', 'not_assessed', ''),
 ('C36', 'Blockchain agent-to-agent security (BlockA2A)', 'I0280', 'M34;M04;M03;M43', 'llm', 'ai_ml', 'proposal', 'not_assessed', ''),
 ('C37', 'Reputation incentive ledger (DART)', 'I0243', 'M05;M22;M08', 'llm', 'ai_ml', 'proposal', 'not_assessed', ''),
 ('C38', 'Agent-run firm (Project Vend)', 'I0204', 'M34;M44;M33', 'llm', 'ai_ml', 'system', 'not_assessed', ''),
 ('C39', 'Agent self-governance in a commons (GovSim-SelfGovern)', 'I0362', 'M42;M08;M36;M63', 'llm', 'ai_ml', 'comparison', 'not_assessed',
  'Catch caps dominate but fail under scarcity; survival in fatal scenarios requires fiscal reserves or exile.'),
 ('C40', 'Reputation network (RepuNet)', 'I0370', 'M07;M05;M10', 'llm', 'ai_ml', 'system', 'not_assessed',
  'Reputation avoids cooperation collapse; exploitative agents become socially isolated.'),
 ('C41', 'Cooperation mechanism benchmark (CoopEval)', 'I0396;I0397;I0398', 'M38;M05;M29;M52', 'llm', 'ai_ml', 'comparison', 'not_assessed',
  'Contracting and mediation were most effective; repetition deteriorates with varying co-players.'),
 ('C42', 'Collusion mitigations for pricing agents', 'I0301', 'M19;M59;M38', 'llm', 'ai_ml', 'comparison', 'substitute',
  'Prompt-only warnings reduce but do not eliminate above-Nash pricing; an expected-damages regulator brings prices close to competitive.'),
 ('C43', 'Punishment with strategy imitation', 'I0409;I0410', 'M14;M62', 'llm', 'ai_ml', 'system', 'not_assessed',
  'Explicit punishment drives norm emergence; reluctant cooperators switch after being punished.'),
 ('C44', 'Punishment, partner selection and reputation (MARL)', 'I0442', 'M14;M15;M10;M05', 'marl', 'ai_ml', 'combination_tested', 'not_assessed',
  'The effect of direct punishment depends on how it combines with third-party punishment, partner selection and reputation.'),
 ('C45', 'Mutual aid bail fund', 'I0527', 'M63;M20', 'human', 'sociology', 'system', 'not_assessed', ''),
]

def main():
    mech = {r['mechanism_id'] for r in csv.DictReader(open(os.path.join(TAX, 'codebook.csv')))}
    inst = {r['instance_id']: r for r in csv.DictReader(open(os.path.join(TAX, 'instances.csv')))}
    cols = ['config_id', 'name', 'mechanisms', 'n_mechanisms', 'instance_ids', 'sources', 'agent_type', 'discipline',
            'evaluation', 'interaction', 'interaction_evidence', 'verified']
    rows, bad = [], []
    link = {}
    for cid, name, iids, mids, at, disc, ev, ix, txt in CONFIGS:
        bad += [f'{cid}:{x}' for x in mids.split(';') if x not in mech] + [f'{cid}:{x}' for x in iids.split(';') if x not in inst]
        for i in iids.split(';'): link.setdefault(i, []).append(cid)
        rows.append(dict(config_id=cid, name=name, mechanisms=mids, n_mechanisms=len(mids.split(';')), instance_ids=iids,
                         sources=';'.join(sorted({inst[i]['source_key'] for i in iids.split(';') if i in inst})),
                         agent_type=at, discipline=disc, evaluation=ev, interaction=ix, interaction_evidence=txt, verified=''))
    if bad: raise SystemExit('unknown ids: ' + ', '.join(bad))
    with open(os.path.join(TAX, 'configurations.csv'), 'w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=cols); w.writeheader(); w.writerows(rows)

    icols = list(next(iter(inst.values())).keys())
    if 'configuration' not in icols: icols.insert(icols.index('mechanism') + 1, 'configuration')
    for i, r in inst.items(): r['configuration'] = ';'.join(link.get(i, []))
    with open(os.path.join(TAX, 'instances.csv'), 'w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=icols); w.writeheader(); w.writerows(inst.values())

    from collections import Counter
    print(len(rows), 'configurations;', dict(Counter(r['evaluation'] for r in rows)), dict(Counter(r['interaction'] for r in rows)))
    art = [r for r in rows if r['agent_type'] in ('llm', 'marl')]
    print(f"artificial-agent configurations: {len(art)}; combination tested: {sum(r['evaluation'] == 'combination_tested' for r in art)}")

if __name__ == '__main__':
    main()
