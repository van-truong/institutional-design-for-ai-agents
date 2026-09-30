# Pass-2 coding guide: deductive recoding against the codebook

You are recoding instances against a fixed codebook of **cooperation-shaping mechanisms**. Read `CODEBOOK_PASS2.md` first.

**Meta-characteristic:** the lever through which an intervention changes agents' options, information, payoffs, relationships, norms, or what happens after a deviation, in order to sustain cooperation.

Code each instance independently from its `description`, `evidence`, `title` and `field_of_use`. Ignore `seed_match`: it is an old prior and is often wrong. You are not shown earlier codes on purpose.

## Fields per instance

- `instance_id`
- `kind`: one of
  - `mechanism`: one lever dominates
  - `configuration`: two or more distinct levers are used or evaluated together, and none clearly dominates
  - `phenomenon`: an emergent pattern or outcome is reported with no identifiable lever
  - `out_of_scope`: not about shaping cooperation among agents at all
- `mechanism_id`: the single best-fitting M-id (`Mnn`). Required for `mechanism`. For `configuration`, give the most central lever. Blank for `phenomenon` and `out_of_scope`.
- `secondary_ids`: other M-ids present, semicolon-separated. Required for `configuration`.
- `configuration_id`: a C-id from the codebook's configuration list if the instance clearly belongs to one, else blank.
- `fit`:
  - `good`: the definition clearly covers it
  - `partial`: the closest mechanism, but the definition strains
  - `misfit`: no mechanism fits
- `proposed_mechanism`: required when `fit` is `misfit`, or when `partial` and you think a new mechanism is needed. Give a name and a one-sentence definition. Also note it if two codebook mechanisms look like the same lever (a merge candidate), or if one mechanism seems to cover two different levers (a split candidate).
- `evidence_type`: one of
  - `tested`: an empirical study, experiment, simulation or field data in which the lever is manipulated or measured
  - `descriptive`: a deployed system, rule, or case described without a test of its effect
  - `proposed`: a design put forward but not evaluated
  - `theory`: a formal model or argument
  - `review`: a synthesis of other studies
- `effect`: for `tested` only; one of `supports_cooperation`, `mixed`, `no_effect`, `harms_cooperation`. Otherwise blank.
- `confidence`: `high`, `medium`, or `low`
- `note`: short, optional

## Output

Write a JSON list, one object per instance, in input order, to your output path. Validate it with python: every id is present, every M-id and C-id exists in the codebook, and every value is from the allowed set. Code every instance by reading it yourself. A script may only write and validate the JSON. Don't modify any other file.
