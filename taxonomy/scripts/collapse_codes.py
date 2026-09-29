#!/usr/bin/env python3
"""Pass-1 collapse: merge open codes into mechanisms and themes (protocol v0.2, step 4-5).

Usage:  python3 taxonomy/scripts/collapse_codes.py

Inputs:  coding/pass1_batch*.json (open codes per instance), instances.csv
Outputs: codebook.csv     themes and mechanisms with definitions, discipline facets, and evidence counts
         coding_log.csv   every open code -> mechanism decision (merge / keep), with instance counts
         instances.csv    fills `code` and `mechanism` from pass 1
The mapping below is the single record of the collapse decisions; edit it, then re-run.
"""
import collections, csv, glob, json, os

HERE = os.path.dirname(os.path.abspath(__file__)); TAX = os.path.dirname(HERE)

THEMES = {
    'T01': 'Visibility & attribution', 'T02': 'Reputation', 'T03': 'Exclusion & conditional access',
    'T04': 'Cost imposition', 'T05': 'Rewards & payoff alignment', 'T06': 'Calibrated response',
    'T07': 'Commitment & contracting', 'T08': 'Structural constraints', 'T09': 'Conditional strategies',
    'T10': 'Collective choice & legitimacy', 'T11': 'Disclosure incentives', 'T12': 'Checks on enforcement',
    'T13': 'Dispute resolution', 'T14': 'Repair & restoration', 'T15': 'Norm formation & internalization',
    'T16': 'Social learning', 'T17': 'Mutual aid', 'T18': 'Mechanism design & allocation',
}

# id: (theme, name, definition)
MECH = {
 'M01': ('T01', 'Conduct monitoring & transparency', 'Agents\' actions are observed, inspected, audited, or disclosed so deviations can be detected.'),
 'M02': ('T01', 'Communication & internal-state oversight', 'A monitor inspects or constrains the messages or internal states agents exchange, to detect or prevent covert coordination.'),
 'M03': ('T01', 'Tamper-evident records', 'Actions are recorded in an attributable log that cannot be altered undetectably and can be audited.'),
 'M04': ('T01', 'Identity & attribution', 'Agents carry persistent, verifiable identities (and costly new ones) so actions and consequences attach to a responsible party.'),
 'M05': ('T02', 'Reputation records & scores', 'A persistent record or score of past conduct is kept and made available to others.'),
 'M06': ('T02', 'Peer evaluation & review', 'Peers assess an agent\'s conduct or output and publish or aggregate the assessment.'),
 'M07': ('T02', 'Gossip', 'Agents pass information about third parties\' conduct to others who may interact with them.'),
 'M08': ('T03', 'Expulsion', 'A deviator is removed from the group, resource, or platform.'),
 'M09': ('T03', 'Temporary suspension', 'A deviator is excluded or cut off for a bounded period or until a condition is met.'),
 'M10': ('T03', 'Partner choice & tie severing', 'Agents choose, keep, or drop interaction partners based on their observed or reported conduct.'),
 'M11': ('T03', 'Shared blocklists & revocation', 'A shared list of flagged agents or revoked credentials lets many parties refuse the same deviators.'),
 'M12': ('T03', 'Access & terms conditioned on record', 'Access, privileges, or prices depend on an agent\'s reputation or proof of compliance.'),
 'M13': ('T03', 'Membership boundaries', 'Insiders defend a resource against outsiders or impose costs on non-members to induce joining.'),
 'M14': ('T04', 'Peer punishment', 'A peer pays a cost to reduce a deviator\'s payoff.'),
 'M15': ('T04', 'Third-party punishment', 'An unaffected observer sanctions a deviator.'),
 'M16': ('T04', 'Centralized (pool) sanctioning & fines', 'A central authority, often funded by members, applies fines or penalties for detected deviations under explicit rules.'),
 'M17': ('T04', 'Externality pricing & central incentive adjustment', 'A charge proportional to imposed harm, or taxes and subsidies set (often learned) by a planner, realign individual payoffs.'),
 'M18': ('T04', 'Shaming & social disapproval', 'Deviations are met with non-material costs: disapproval, public exposure, or reputational pressure.'),
 'M19': ('T04', 'Liability for harm', 'The deviator bears the damages its action causes, or a guarantee is enforced when a claim proves false.'),
 'M20': ('T04', 'Collective liability', 'Group members share liability for any member\'s deviation, giving them reason to monitor one another.'),
 'M21': ('T05', 'Peer reward & gifting', 'Agents transfer part of their own payoff to peers, typically cooperators.'),
 'M22': ('T05', 'Payment for cooperation', 'A central party pays for a cooperative act, verified behavior, contribution, or outcome.'),
 'M23': ('T05', 'Status & prestige', 'Contributors receive visible status markers or prestige.'),
 'M24': ('T05', 'Combined carrot & stick', 'Both reward and punishment instruments are available, possibly switched by context.'),
 'M25': ('T05', 'Outcome sharing & aligned stakes', 'Agents share in joint output or hold stakes in the system or in others\' payoffs, so their payoff rises with collective success.'),
 'M26': ('T05', 'Relative-performance incentives', 'Rewards depend on an agent\'s rank relative to others.'),
 'M27': ('T06', 'Graduated & proportional sanctions', 'Responses escalate with repetition or duration, or scale with the severity of the deviation.'),
 'M28': ('T07', 'Deposits, bonds & stakes', 'An agent (or a third party on its behalf) posts collateral that is forfeited on breach or refunded on compliance.'),
 'M29': ('T07', 'Binding contracts', 'Agents agree to enforceable conditional transfers or penalties, often executed automatically.'),
 'M30': ('T07', 'Self-commitment devices', 'An agent binds its own future action or makes backing out costly.'),
 'M31': ('T07', 'Escrow & verify-then-pay', 'Payment is held by a neutral mechanism and released only when performance is verified.'),
 'M32': ('T07', 'Assurance contracts', 'Contributions are refunded (possibly with a bonus) if a collective threshold is not reached.'),
 'M33': ('T07', 'Pre-play communication & pledges', 'Agents exchange non-binding messages or public pledges before acting.'),
 'M34': ('T08', 'Ex ante action restriction & scoped permissions', 'Only pre-specified actions, scopes, zones, or time-bounded rights are permitted.'),
 'M35': ('T08', 'Runtime interception & interruption', 'An enforcement layer or overseer blocks, resamples, or halts an agent\'s actions as they happen.'),
 'M36': ('T08', 'Usage caps & quotas', 'Hard limits bound each agent\'s use of a shared resource or its rate of action.'),
 'M37': ('T08', 'Rotation & turn-taking', 'Access to shares of a resource is assigned in turns or by lot.'),
 'M38': ('T08', 'Interaction structure', 'Who interacts with whom, how often, and in what roles is designed: network topology, repetition, population composition.'),
 'M39': ('T09', 'Direct reciprocity', 'An agent conditions its behavior toward a partner on that partner\'s past behavior toward it.'),
 'M40': ('T09', 'Indirect reciprocity', 'Agents help others according to the recipient\'s conduct toward third parties.'),
 'M41': ('T09', 'Group-conditional cooperation', 'An agent adjusts its own contribution or use to what others do collectively or to aggregate signals.'),
 'M42': ('T10', 'Collective choice of rules', 'Members propose, vote on, or veto the rules or allocations that govern them.'),
 'M43': ('T10', 'Robust aggregation & quorum', 'Decisions require agreement among independent parties and discount faulty or outlying inputs.'),
 'M44': ('T10', 'Legitimate & elected authority', 'Authority to lead, monitor, or sanction is assigned by election or recognized as legitimate.'),
 'M45': ('T10', 'Institutional choice & exit', 'Agents choose which institutional regime to join, or may opt out.'),
 'M46': ('T10', 'Nested & adaptive rule-making', 'Rule-making is layered or delegated, and rules are revised or redesigned over time.'),
 'M47': ('T11', 'Leniency for self-reporting', 'Agents that disclose their own or joint wrongdoing receive reduced penalties.'),
 'M48': ('T11', 'Rewards for reporting others', 'Agents are paid for reporting others\' violations or flaws, and reporting is made cheap.'),
 'M49': ('T12', 'Meta-norms', 'Agents who fail to sanction deviators are themselves sanctioned.'),
 'M50': ('T12', 'Checks on sanctioners', 'Safeguards limit the abuse of sanctioning power (filters on antisocial punishment, audits of officials, collective checks on dominance).'),
 'M51': ('T13', 'Third-party adjudication', 'A designated or peer adjudicator issues a binding ruling, possibly after tiered escalation.'),
 'M52': ('T13', 'Mediation', 'A neutral third party helps parties reach agreement without imposing a ruling.'),
 'M53': ('T13', 'Bonded challenge', 'Agents stake funds to challenge a claimed outcome, winning if upheld and losing if not.'),
 'M54': ('T13', 'Appeals & error correction', 'Sanctioned agents can contest decisions, and wrongful outcomes are reversed.'),
 'M55': ('T14', 'Restitution & reintegration', 'The offender repairs harm or apologizes, and the relationship is rebuilt or membership restored.'),
 'M56': ('T14', 'Undoing deviation\'s effects', 'The output of a deviation is reverted, removed, or rolled back so deviation yields nothing.'),
 'M57': ('T14', 'Failure attribution & incident analysis', 'After a failure, evidence is used to identify responsible agents and causes.'),
 'M58': ('T15', 'Explicit norms & codes of conduct', 'Expected behavior is written down, published, and explained, including when sanctions are applied.'),
 'M59': ('T15', 'Instilled prosocial dispositions', 'Agents\' preferences or reasoning are shaped (by training or prompting) to value cooperative outcomes.'),
 'M60': ('T15', 'Defaults & choice architecture', 'The cooperative option is made the default.'),
 'M61': ('T15', 'Norm learning', 'Agents infer norms, or which institution is authoritative, from observed sanctions and behavior.'),
 'M62': ('T16', 'Imitation & strategy selection', 'Higher-payoff strategies spread through copying or selection.'),
 'M63': ('T17', 'Mutual aid, pooling & mutual credit', 'Members pool resources, give without direct exchange, or trade services in mutual credit.'),
 'M64': ('T18', 'Incentive-compatible mechanisms', 'Allocation and payment rules make truthful reporting or cooperation each agent\'s best strategy.'),
 'M65': ('T18', 'Market & matching allocation', 'Tasks or resources are allocated through auctions, markets, or central matching rather than free negotiation.'),
}

C = {}  # open code -> mechanism
def m(mid, *codes):
    for c in codes: C[c] = mid
m('M01', 'monitoring of conduct', 'central monitoring of conduct', 'monitoring of interactions', 'inspection to verify compliance',
  'local monitoring and sanctioning', 'budget-constrained audit scheduling', 'observation of others\' interactions',
  'observe others\' past interactions', 'third-party observation of conduct', 'third-party observation of interactions',
  'visibility of individual conduct to peers', 'public disclosure of actions', 'public disclosure of individual actions',
  'make deviation detectable', 'trace and notify exposed contacts')
m('M02', 'monitoring of inter-agent communication', 'internal-state monitoring for collusion', 'monitoring of internal states',
  'limit covert communication channels')
m('M03', 'public verifiable log of actions', 'tamper-evident record of actions', 'audit of tamper-evident logs')
m('M04', 'attributable identity for agents', 'attribute actions to identified agents', 'make actors identifiable',
  'verifiable identity credential', 'entry cost for new identities', 'label source of messages',
  'signed attestation of compliance', 'announced response to failed authentication')
m('M05', 'public record of past conduct', 'aggregated reputation score', 'aggregate witness reputation information',
  'peer-assigned reputation scores', 'learned reputation assignment norm', 'blind simultaneous rating reveal',
  'certified performance credentials')
m('M06', 'distributed peer rating of content', 'crowd annotation of misleading content', 'public peer evaluation of conduct',
  'peer review with public pressure')
m('M07', 'gossip about others\' conduct', 'peer gossip about others\' conduct', 'peer-shared reputation information',
  'sharing reputational information')
m('M08', 'remove deviator from group', 'reduce number of resource users')
m('M09', 'temporary exclusion by peer', 'temporary exclusion from resource', 'temporary restriction of participation',
  'cut off after failure threshold')
m('M10', 'partner choice by observed conduct', 'partner selection by reputation', 'reputation-based partner selection',
  'choose interaction partners', 'partner choice among competitors', 'sever ties with deviator', 'sever ties with deviating partner')
m('M11', 'shared blocklist of deviators', 'shared blocklist of flagged agents', 'public revocation of credentials')
m('M12', 'access gated by reputation', 'degrade access below reputation threshold', 'reduced access based on reputation',
  'permissions gated on reputation', 'access conditional on compliance proof', 'cost scaled to past conduct')
m('M13', 'exclude outsiders from resource', 'cost imposed on non-participants')
m('M14', 'costly peer penalty on deviator', 'costly peer punishment', 'costly peer punishment of deviators', 'peer sanction of deviator')
m('M15', 'third party punishes violators', 'third-party sanction of deviator')
m('M16', 'fixed cost on detected deviation', 'fine calibrated to detection probability', 'swift certain modest sanction',
  'standardized sanction schedule', 'collectively funded central sanction', 'codified rules with central enforcement',
  'explicit rules with central enforcement', 'threat of cost imposition', 'credible threat of punishment',
  'restrict resources of detected deviator')
m('M17', 'charge for imposed externality', 'charge per unit of harm', 'central agent shapes others\' rewards',
  'central learned reward reshaping', 'adaptive central incentive payments', 'per-use cost on actions',
  'transfer based on deviation from average')
m('M18', 'non-payoff disapproval signal', 'social disapproval of deviator', 'informal peer social pressure',
  'public exposure of violations', 'public disclosure on missed deadline')
m('M19', 'liability for caused harm', 'enforceable quality guarantee')
m('M20', 'collective penalty for member deviation', 'group liable for member default', 'joint liability for group members')
m('M21', 'peer reward transfer', 'voluntary transfer of reward to peers', 'voluntary transfer to others')
m('M22', 'payment for cooperative act', 'subsidy for cooperative action', 'reward per accepted contribution',
  'payment conditional on verified behavior', 'payment conditional on outcome', 'matching subsidy for contributions')
m('M23', 'status award at activity threshold', 'status reward for contribution')
m('M24', 'peer reward and penalty options', 'peer reward or punishment option', 'reward and penalty by conduct',
  'reward compliance, penalize deviation', 'state-contingent reward or punishment')
m('M25', 'contribution-proportional reward', 'reward by marginal contribution', 'reward based on group outcome',
  'stake in others\' payoffs', 'shared ownership of joint output', 'transfer payoffs to align incentives', 'stake aligned with system value')
m('M26', 'reward by relative performance rank', 'reward by relative rank')
m('M27', 'escalating response to repeat deviation', 'penalty growing with deviation duration', 'graduated throttling above usage cap',
  'penalty scaled to deviation severity', 'punishment scaled to detected deviation', 'sanction scaled to detected deviation')
m('M28', 'deposit forfeited on breach', 'deposit refunded on compliance', 'third party bonds agent for premium')
m('M29', 'binding contingent transfer contract', 'binding conditional transfer contract', 'binding contract between agents',
  'binding contract with automatic execution', 'self-executing contract rules', 'pre-agreed penalty for breach', 'pre-agreed penalty for exit')
m('M30', 'binding commitment to future action', 'voluntary binding commitment', 'binding self-commitment device', 'costly signal of commitment')
m('M31', 'escrow held until delivery', 'payment escrowed until verified', 'payment released only on verified delivery',
  'authorized payment settlement protocol', 'third party verifies obligation met')
m('M32', 'refund if threshold unmet', 'refund plus bonus if threshold unmet')
m('M33', 'non-binding communication before play', 'non-binding pre-play promise', 'non-binding public pledge',
  'pre-play communication among agents', 'pre-play communication channel', 'open communication among agents',
  'public statement of intended action')
m('M34', 'restrict permitted actions ex ante', 'authenticated identity and scoped permissions', 'central access-control policy',
  'signed verifiable authorization', 'mandatory checklist before action', 'restrict use in zones or seasons',
  'gate admission to shared state', 'central specification of roles and scope', 'contained environment for agent interaction',
  'time-limited rights expiring unless renewed')
m('M35', 'block violating actions at runtime', 'trusted monitor blocks suspicious actions', 'external interruption of agent')
m('M36', 'cap on per-agent action rate', 'cap on per-agent resource use', 'isolate agents\' resource shares',
  'tradeable individual resource quota', 'escrowed budget for irreversible actions')
m('M37', 'rotate access to shared resource', 'learned shared-channel access rule')
m('M38', 'design of communication topology', 'fixed local interaction structure', 'interaction network structure',
  'diversify agent types', 'role differentiation via personas', 'dense closed network ties', 'repeated interaction with same partners')
m('M39', 'reciprocate partner\'s past cooperation', 'reciprocate partner\'s prior action', 'reciprocate toward past cooperators',
  'withhold resources from non-contributor')
m('M40', 'help conditional on partner\'s reputation', 'help conditional on recipient reputation', 'help conditional on reputation',
  'community punishment of deviator')
m('M41', 'cooperation conditional on others\' cooperation', 'self-imposed back-off on congestion')
m('M42', 'collective vote on rules', 'group-voted adoption of rules', 'collective rule-making by participants',
  'collective vote on allocation', 'collective voting on allocation', 'consensus with binding veto')
m('M43', 'quorum of matching reports required', 'aggregate independent judgments', 'discount unreliable peer inputs',
  'robust aggregation of peer evaluations')
m('M44', 'elected leader coordinates group', 'elected bounded authority', 'monitor chosen by group vote',
  'choose who holds sanction authority', 'recognize legitimate rule source', 'learn which institution is authoritative')
m('M45', 'choice among institutional regimes', 'agents choose institution to join', 'opt into sanctioning institution',
  'voluntary choice of institution', 'option to opt out of game')
m('M46', 'nested rule-making tiers', 'delegate rule-making to local groups', 'adaptive revision of rules',
  'tailor institutional design features', 'externally optimized rule set')
m('M47', 'reduced penalty for self-report', 'reduced penalty for self-reporting', 'reward for reporting collusion')
m('M48', 'reward for reporting violations', 'bounty for reported flaws', 'low-cost channel for disclosure')
m('M49', 'penalize failure to punish', 'sanction non-punishers', 'sanction those who fail to sanction')
m('M50', 'block punishment of cooperators', 'retaliation against punishers permitted', 'institutional checks and audit',
  'collective sanction of dominance attempts')
m('M51', 'third party rules on dispute', 'peer jury rules on reports', 'adjudicated adversarial debate',
  'tiered audit escalating to panel', 'escalate uncertain decisions upward')
m('M52', 'mediator facilitates agreement', 'third party mediates between parties', 'third party mediates negotiation')
m('M53', 'bonded challenge of claimed outcome')
m('M54', 'appeal of sanction decisions', 'independent review of appeals', 'reverse wrongful sanctions', 'collective override of protocol outcome')
m('M55', 'offender repairs harm caused', 'apology to repair breach', 'restorative reintegration of offender', 'conditional path to reinstatement')
m('M56', 'roll back to prior state', 'compensating rollback on failure', 'revert deviant contribution', 'nullify gains from deviation',
  'remove violating content', 'peer policing of deviation', 'peer suppression of selfish acts')
m('M57', 'identify culpable agents ex post', 'structured incident reporting')
m('M58', 'written code of conduct', 'published standard of conduct', 'public norm-setting messages', 'explain norm when sanctioning',
  'non-coercive compliance management')
m('M59', 'instill prosocial preferences via training', 'internalized moral preference', 'prompt instilling prosocial reasoning',
  'prompt to universalize conduct')
m('M60', 'default set to desired action')
m('M61', 'learn norms from observed sanctions', 'agent-level norm formation module')
m('M62', 'imitate higher-payoff strategies', 'imitate successful strategies', 'spread of higher-payoff strategies',
  'selection of successful strategies', 'selection of surviving strategies')
m('M63', 'pooled mutual aid fund', 'pay forward to any member', 'open peer relay infrastructure', 'horizontal mutual accountability',
  'time-based mutual credit', 'credit earned by serving others', 'rotating allocation of pooled funds', 'rotating pooled payout')
m('M64', 'incentive-compatible allocation auction', 'incentive-compatible allocation rule', 'incentive-compatible protocol design',
  'mechanism implementing efficient equilibrium', 'payments inducing truthful reports', 'reward agreement with consensus report',
  'reward rule making contribution dominant')
m('M65', 'auction allocation of resources', 'market allocation of tasks', 'central allocation mechanism')
BUNDLES = {'bundle of commons design principles'}  # not a single lever: kept as instances, excluded from mechanisms

def main():
    P = []
    for f in sorted(glob.glob(os.path.join(TAX, 'coding', 'pass1_batch[0-9].json'))): P += json.load(open(f))
    inst = {r['instance_id']: r for r in csv.DictReader(open(os.path.join(TAX, 'instances.csv')))}
    code_of = {p['instance_id']: (p['code'] or '').strip().lower() for p in P if p['is_mechanism']}
    unmapped = sorted({c for c in code_of.values() if c not in C and c not in BUNDLES})
    if unmapped: raise SystemExit('unmapped codes: ' + '; '.join(unmapped))
    stale = sorted(set(C) - set(code_of.values()))
    if stale: print('mapping has codes no instance uses:', '; '.join(stale))

    for iid, r in inst.items():
        c = code_of.get(iid, '')
        r['code'] = c or ('(phenomenon)' if iid in {p['instance_id'] for p in P} else '')
        r['mechanism'] = C.get(c, 'BUNDLE' if c in BUNDLES else '')
    cols = list(next(iter(inst.values())).keys())
    with open(os.path.join(TAX, 'instances.csv'), 'w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=cols); w.writeheader(); w.writerows(inst.values())

    per_code = collections.Counter(code_of.values())
    by_mech = collections.defaultdict(list)
    for iid, c in code_of.items():
        if c in C: by_mech[C[c]].append(inst[iid])
    with open(os.path.join(TAX, 'coding_log.csv'), 'w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=['pass', 'open_code', 'n_instances', 'mechanism_id', 'mechanism', 'action'])
        w.writeheader()
        for c in sorted(per_code, key=lambda c: (C.get(c, 'Z'), c)):
            mid = C.get(c)
            siblings = sum(1 for x in C if C[x] == mid and x in per_code) if mid else 0
            w.writerow({'pass': 1, 'open_code': c, 'n_instances': per_code[c], 'mechanism_id': mid or 'BUNDLE',
                        'mechanism': MECH[mid][1] if mid else 'not a single lever',
                        'action': 'bundle' if not mid else ('merge' if siblings > 1 else 'keep')})

    rows = []
    for mid, (tid, name, defn) in MECH.items():
        rs = by_mech.get(mid, [])
        nonseed = [r for r in rs if r['origin'] != 'seed']
        disc = collections.Counter(d for r in nonseed for d in r['discipline'].split(';') if d)
        fields = sorted({r['field_of_use'] for r in nonseed if r['field_of_use'] and r['discipline'] != 'ai_ml'})
        rows.append({'theme_id': tid, 'theme': THEMES[tid], 'mechanism_id': mid, 'mechanism': name, 'definition': defn,
                     'n_instances': len(rs), 'n_llm': sum(r['agent_type'] == 'llm' for r in rs),
                     'n_marl': sum(r['agent_type'] == 'marl' for r in rs), 'n_seed': len(rs) - len(nonseed),
                     'n_disciplines': len(disc), 'disciplines': ';'.join(f'{d}:{n}' for d, n in disc.most_common()),
                     'native_terms': '', 'example_fields': '; '.join(fields[:6]),
                     'open_codes': ';'.join(sorted(x for x in C if C[x] == mid and x in per_code))})
    nat = collections.defaultdict(set)
    for p in P:
        c = code_of.get(p['instance_id'])
        if c in C and p.get('native_term'): nat[C[c]].add(p['native_term'].strip())
    for r in rows: r['native_terms'] = '; '.join(sorted(nat[r['mechanism_id']], key=str.lower)[:12])
    with open(os.path.join(TAX, 'codebook.csv'), 'w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)

    empty = [r['mechanism_id'] for r in rows if not r['n_instances']]
    print(f"{len(code_of)} coded instances, {len(per_code)} open codes -> {len(MECH)} mechanisms in {len(THEMES)} themes; "
          f"phenomena: {sum(1 for p in P if not p['is_mechanism'])}; bundles: {sum(per_code[b] for b in BUNDLES)}")
    if empty: print('mechanisms with no instance:', empty)

if __name__ == '__main__':
    main()
