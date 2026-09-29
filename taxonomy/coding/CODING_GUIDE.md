# Open-coding guide (pass 1)

You are open-coding instances for a taxonomy of **cooperation-shaping mechanisms**.

**Meta-characteristic:** the *lever* through which an intervention changes agents' options, information, payoffs, relationships, norms, or what happens after a deviation, in order to sustain cooperation among agents (human, animal, organization, software, LLM, or RL agents).

For each instance, read `description`, `evidence`, `field_of_use` and `title`, and assign the fields below.

## Fields

- `is_mechanism`: `true` if the instance describes an intervention or rule that shapes cooperation (designed, or emergent but acting as a rule). `false` if it only reports an emergent pattern or outcome with no identifiable lever. Examples of `false`: "agents polarize", "herding stronger than humans". Leave the rest blank if false, but still fill `phenomenon`.
- `code`: 2–6 words naming the **lever in field-neutral language**.
  - Good: "fixed cost on detected deviation", "public record of past conduct", "remove deviator from group", "deposit forfeited on breach", "third party rules on dispute", "cap on per-agent resource use", "escalating response to repeat deviation", "bonded challenge of claimed outcome", "restrict permitted actions ex ante", "reward conditional on others' contributions".
  - Bad (field-specific names): "slashing", "Pigouvian tax", "ArbCom", "strike system". Put those in `native_term` instead.
  - Reuse your own earlier codes whenever the lever is the same. Consistency matters more than nuance. Create a new code only when the lever differs.
- `native_term`: what the source calls it (e.g., "slashing", "catch shares", "Community Notes").
- `lever`: one or more of `options`, `information`, `payoffs`, `relationships`, `norms`, `post_deviation`.
- `who_acts`: `central`, `peer`, `third_party`, `self`, or `collective`.
- `timing`: `ex_ante`, `ex_post`, or `continuous`.
- `valence`: `punishment`, `reward`, `hybrid`, or `structural`.
- `requires`: other levers this one depends on (e.g., a sanction requires "detection"). Use codes, semicolon-separated, or blank.
- `phenomenon` (optional): the emergent pattern reported, in a few words, e.g. "emergent convention", "tacit collusion".
- `pathology` (optional): a documented failure or side effect.
- `confidence`: `high`, `medium`, or `low`. Use low if the description is too thin to tell the lever.
- `note` (optional): anything a reviewer should know, e.g. "two distinct levers, coded the dominant one", or "description may be wrong".

If an instance clearly bundles two distinct levers, code the dominant one and name the other in `note`.

## Sensitizing frame

These 17 primitives are a starting frame, not ground truth. Use them only as inspiration.
1. Monitoring
2. Exclusion
3. Cost imposition
4. Benefit provision
5. Graduated response
6. Commitment & constraint
7. Collective liability
8. Conditional strategy
9. Legitimacy & democratic authority
10. Disclosure incentive
11. Restoration & reintegration
12. Meta-enforcement
13. Dispute resolution & appeals
14. Norm internalization
15. Imitation / strategy evolution
16. Mechanism design
17. Mutual aid

The `seed_match` field in the input is a prior guess. Ignore it if it's wrong.

## Output

Write a JSON list of objects to your output path, one per instance, with these keys:
`instance_id, is_mechanism, code, native_term, lever, who_acts, timing, valence, requires, phenomenon, pathology, confidence, note`

Then write a second JSON file, `<output>_codes.json`: a list of `{code, definition (one sentence), n_instances}` for every code you used.

Validate both files with python. Don't modify any other file.
