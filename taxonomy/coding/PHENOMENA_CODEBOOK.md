# Phenomenon codebook

This codebook defines the phenomenon types behind the paper's phenomena figure (Fig. 8) and the website's
phenomena tab. With it, a reader can audit how instances were grouped, or recode them independently and compare.

## Unit and inclusion

- **Unit:** one coded instance (`taxonomy/instances.csv`).
- **Inclusion:** the instance has `kind = phenomenon`. That is, it reports an emergent pattern or outcome among
  agents with no identifiable lever behind it, for example "agents polarize" or "a convention forms" (see
  `CODING_GUIDE.md`, `is_mechanism = false`, and `CODING_GUIDE_PASS2.md`, `kind = phenomenon`). An instance that
  names a rule, incentive, or intervention that shapes the pattern is coded as a mechanism instead, even if the
  pattern is emergent.
- **Open label:** during coding, each phenomenon instance got a short free-text label naming the pattern
  (`phenomenon` in `pass1_batch*.json`; `coder_note` in `pass_new84_draft.csv` for I0562 onward).

## Procedure

1. Collect the open labels.
2. Group them thematically by the *kind of pattern* reported, regardless of agent type or field.
3. Give each instance exactly one type: the one that names the primary pattern the source reports.
4. Code agent type from the instance (`agent_type`: human, MARL, LLM).
5. Code each instance's effect on cooperation separately from its type (see Valence below).

The result is `coding/phenomena_tags.csv` (`instance_id, phenomenon_type, valence`).
`scripts/build_phenomena_data.py` builds the website data and the figure counts from it.

## Types

The figure order is the order of the table below. The first seven types describe what groups do. The last three
describe where things go wrong. A type's default effect is the effect most of its instances have. Each instance
still carries its own valence.

| Key | Type | Definition | Assign here when the source mainly reports… | Not here: use instead | Default effect |
|---|---|---|---|---|---|
| `comm_language` | Emergent communication & language | Agents invent signals, protocols, or a shared language without being given one. | a new signal, code, vocabulary, or protocol; its structure (compositionality); or how to measure it | agreement on *which* action to take → `convention_coord` | neutral |
| `convention_coord` | Conventions & coordination | Groups settle on shared conventions, norms, or equilibria through repeated interaction. | convergence on one of several equivalent options, tipping by a committed minority, or stable strategy mixes | conventions that set up lasting roles or ranks → `social_structure`; group-wide drift toward a wrong answer → `conformity_bias` | neutral |
| `social_structure` | Social structure: networks, hierarchy, roles | Networks, hierarchies, elites, and roles emerge from who interacts with whom. | network topology, leaders, elites, stratification, specialization, or community structure | transmission of behavior across a population → `culture` | neutral |
| `culture` | Culture, norms & individuality | Cultures, individual identities, and transmitted behavior develop across a population. | behavior passed between agents or generations, group-specific norms, or the absence of socialization | one-off convergence in a single game → `convention_coord` | neutral |
| `collective_intel` | Collective intelligence & performance | Group problem-solving that can exceed, or fall short of, the individual agents. | group performance compared with individuals, emergent curricula, or emergent tool use | performance lost to biased consensus → `conformity_bias` | neutral |
| `economy` | Emergent economy & resource use | Markets, trade, bartering, and resource dynamics arise among agents (and people). | exchange, prices, market behavior, free-riding on a shared resource, or adverse selection | coordinated pricing against third parties → `collusion_deception` | neutral |
| `cooperation` | Spontaneous cooperation | Agents cooperate or act prosocially even when they could defect. | prosocial behavior that no rule or incentive in the setup explains | cooperation that a named mechanism produces → code as a mechanism, not a phenomenon | beneficial |
| `conformity_bias` | Conformity & collective bias | Groups converge on biased or mistaken consensus, or amplify one another's errors. | conformity, herding, group-size-dependent bias, or opinion dynamics that distort accuracy | deliberate deception by some agents → `collusion_deception` | harmful |
| `collusion_deception` | Collusion, deception & manipulation | Agents coordinate against oversight, collude, or deceive one another or people. | tacit or explicit collusion, hidden or steganographic channels, or deceptive or adversarial communication | harm without coordination against a third party or overseer → `harm` | harmful |
| `harm` | Emergent harm: toxicity, fragility, breakout | Toxic dynamics, fragile networks, or agents acting outside their intended scope. | toxicity spread, cascading failure, inter-agent attack surfaces, unfair outcomes, or acting outside scope | harm that depends on agents coordinating against oversight → `collusion_deception` | harmful |

## Valence (effect on cooperation)

Valence is coded per instance, not per type.

- **beneficial:** the pattern supports cooperation or collective welfare (e.g. a shared vocabulary that improves
  coordination).
- **harmful:** the pattern undermines collective welfare, safety, fairness, or oversight (e.g. collusion against
  buyers, toxicity spread).
- **neutral or surprising:** the source reports the pattern without a clear effect either way, or the effect
  depends on context.

## Real-world incidents

Incidents (`taxonomy/incidents.csv`) are not instances. They are linked to a type only where the report describes
that type's pattern. The links are in `INCIDENT_TYPES` in `scripts/build_phenomena_data.py`.

## Current counts

`phenomena_tags.csv` is the source of truth. The website shows live counts.

## Boundary cases

These assignments sat on a boundary under the rules above. They were reviewed against the rules on 2026-10-06.

- I0348 "cooperative norms; division of labor; cumulative culture" moved from `comm_language` to `culture`: the
  source reports transmitted norms and artifact lineages, not signals or protocols.
- I0425 "emergent role specialization" moved from `convention_coord` to `social_structure`, consistent with other
  specialization instances.
- I0334 "converged coordination formats enabling unsanctioned information sharing" moved from `collective_intel`
  to `collusion_deception` (harmful): the shared channel evaded the evaluation's rules.
- I0563 "harmful task decomposition bypasses per-trajectory monitors" moved from `harm` to `collusion_deception`:
  the harm depends on evading oversight.
- I0283 "emergent roles, collective rule change, transmitted memes" stays under review between `culture` and
  `social_structure`.
