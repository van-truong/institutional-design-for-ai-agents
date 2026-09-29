# Taxonomy protocol: cooperation-shaping mechanisms for agent groups

Status: **draft v0.1 (2026-09-29)** — Phase 0/1. Decisions below were set by the authors on 2026-09-29.

This folder is the single source of truth for the mechanism taxonomy. The paper's
taxonomy figure (Fig. 4, `manuscript/scripts/gen_taxonomy.py`) and the project
website (`docs/`) are both generated from these files.

## 1. Purpose

Build an auditable catalogue of mechanisms that shape cooperation among agents,
each linked to (a) evidence that it works — or fails — in human institutions and
(b) whether it has been tested with LLM agents or multi-agent RL (MARL) agents.
The catalogue supports three uses: the paper's taxonomy and method section, a
tested-versus-untested gap map, and the website's deep-dive tabs and mind map.

## 2. Design decisions

| Decision | Choice |
|---|---|
| Backbone | **17 causal primitives** (each a distinct lever on behavior). The six discipline families of the original figure are kept as a **facet**. |
| Coding | **LLM-assisted extraction, single human verifier.** Records are pre-coded by an LLM with source URLs; one author (V.Q.T.) verifies every record. No inter-rater agreement statistic is reported; this is stated as a limitation. |
| Literature scope | **LLM multi-agent work, 2023–present**, plus **MARL precursors** (non-LLM multi-agent RL), flagged separately. |
| Data home | Public, in this repository. Only published or preprinted work is cited. The original working spreadsheet stays private and gitignored. |

## 2a. Coding method (v0.2, 2026-09-29)

The published taxonomy is built by **thematic coding of extracted instances**, not by
confirming the seed. The original spreadsheet and the Phase 1 seed are a **sensitizing
list**: they suggest codes and search terms, but no seed entry survives unless the coded
evidence supports it.

1. **Meta-characteristic.** The lever through which an intervention changes agents'
   options, information, payoffs, relationships, norms, or what happens after a deviation,
   in order to sustain cooperation among agents.
2. **Instances (`instances.csv`).** One row is one documented use of a mechanism in one
   source: an empirical study, a deployed system, or a legal or institutional rule. It
   records the source, the **discipline** and **field of use**, the agent type (human,
   LLM, MARL, software, organization), and a short description in the source's own terms.
   Instances come from the search papers (Phase 2), the cross-disciplinary search (2b), and
   the seed's human examples (tagged `origin=seed`).
3. **Open coding.** Each instance gets a descriptive code for its lever, plus structural
   attributes: who acts (central, peer, third party, self), timing (ex ante, ex post),
   valence, and the target of the change.
4. **Collapse.** Codes that use the same lever are merged into one **mechanism**, even when
   disciplines name them differently. For example, a Pigouvian tax, a regulatory fine, and
   a slashing penalty are all a fixed cost on a deviation. The disciplines and fields where
   a mechanism appears become its **facet**, and the published row lists all of them.
   Every merge and split is logged in `coding_log.csv`.
5. **Group.** Mechanisms are grouped into higher-level themes (the primitives). The 17 seed
   primitives are the starting frame, and they are revised when the coded mechanisms do not
   fit them.
6. **Ending conditions** (Nickerson, Varshney & Muntermann, 2013). Iteration stops when
   the last pass over new instances produces no new mechanism and no merge or split, and
   every mechanism has at least one instance.

The single verifier reviews every code and merge; the coding log is the audit trail.

## 3. Unit of record

One row of `mechanisms.csv` is one **mechanism**: an intervention that changes
agents' options, information, payoffs, relationships, norms, or what happens after
a deviation, in a setting with repeated or multi-party interaction, with at least one
documented instance (an empirical study, a deployed system, or a legal or
institutional rule).

### Codebook (`mechanisms.csv`)

| Field | Values / meaning |
|---|---|
| `id` | `Pnn-mm` — primitive number, then mechanism number within it |
| `name` | Short name of the mechanism |
| `primitive_id`, `primitive` | One of the 17 primitives (`primitives.csv`) |
| `discipline_family` | Facet: `social`, `formal`, `economic`, `technical`, `mutual_aid`, `restorative` |
| `domain` | Finer domain label (e.g., `Legal / contractual`) |
| `valence` | `punishment`, `reward`, `hybrid`, `structural` |
| `game_type` | Dilemma structure it applies to, e.g. `CPR` (extractive), `PGG` (contributive), `both` |
| `functions` | Paper's 7 institutional functions it serves: `norms`, `monitoring`, `reputation`, `sanctions`, `constraints`, `adjudication`, `repair` (semicolon-separated) |
| `channels` | Paper's 6 mechanism families: `normative`, `social`, `epistemic`, `incentive`, `constraint`, `restorative` |
| `dilemmas` | Which dilemmas it addresses: `extractive`, `contributive`, `second_order`, `repair`, `coordination`, `collusion` |
| `human_example` | A concrete real-world instance |
| `key_references` | Canonical human-literature references (verified in Phase 3) |
| `llm_status` | `tested`, `partial`, `discussed`, `untested` — with LLM agents |
| `llm_evidence` | Which LLM studies test it, and how |
| `marl_status` | `tested`, `partial`, `untested` — with non-LLM multi-agent RL (Phase 2) |
| `marl_evidence` | Which MARL studies test it, and how (Phase 2) |
| `ai_analogue` | What the mechanism looks like in an LLM agent system |
| `sources` | Where the record came from: `overview`, `first_principles`, `search` |
| `match` | How a seed record was merged: `exact`, `fuzzy`, `assigned` (assigned = the primitive was chosen by judgment; verify first) |
| `precoded` | Which fields were pre-filled from the primitive's defaults rather than coded individually |
| `verified` | Verifier initials + date once checked; blank until then |
| `notes` | Free text |

`functions`, `channels`, and `dilemmas` are **pre-coded from the primitive's defaults**
(`primitives.csv`) in the seed and listed in `precoded`; verification replaces them
with record-specific codes.

Pathologies (`pathologies.csv`) are linked at the **primitive** level via
`pathology_ids` in `primitives.csv`.

## 4. Phases

| Phase | Output | Status |
|---|---|---|
| 0. Protocol | this file | draft |
| 1. Seed | `primitives.csv`, `mechanisms.csv`, `pathologies.csv` from the original spreadsheet (de-duplicated union of the Overview and First-Principles sheets) | done |
| 2. LLM + MARL search | `papers.csv`, `search_log.csv`, `search_raw/`; updates `llm_status`, `llm_evidence`, `marl_status`, `marl_evidence` (`scripts/merge_search.py`) | run 2026-09-29; in verification |
| 3. Human-literature verification | verified `key_references` per mechanism | not started |
| 4. News incidents (separate track) | `incidents.csv`: verified reports of AI agents acting outside authorization, gaining unauthorized access, or leaking data | collected 2026-09-29; in verification |
| 5. Outputs | regenerated Fig. 4; website tabs, mind map, gap map; method paragraph + screening counts in the paper | not started |

## 5. Search protocol (Phase 2)

**Sources.** arXiv (cs.AI, cs.CL, cs.MA, cs.GT, cs.LG), ACL Anthology, and the
proceedings of NeurIPS, ICML, ICLR, AAMAS, and IJCAI; forward and backward
citation chasing from seed papers.

**Seed papers.** GovSim, Melting Pot, Concordia, CoopEval, SanctSim, and other
multi-agent cooperation studies already cited in the manuscript or the original
spreadsheet.

**Query template** (run per primitive, adapted to each source's syntax):

```
("large language model" OR LLM OR "language agent" OR "multi-agent reinforcement learning" OR MARL)
AND ("social dilemma" OR "public goods" OR "common-pool" OR commons OR cooperation)
AND (<primitive terms>)
```

where `<primitive terms>` are listed per primitive in `primitives.csv`
(e.g., graduated response: `"graduated sanction*" OR escalat* OR "rate limit*"`).

**Inclusion.**
- *LLM track:* two or more LLM-based agents interact, **and** the study manipulates
  or measures a cooperation-shaping mechanism. 2023–present.
- *MARL track:* two or more learning agents (non-LLM), **and** the study manipulates
  or measures a cooperation-shaping mechanism. Flagged `track=marl`.

**Exclusion.** Single-agent alignment or safety evaluations; human-subject studies
without artificial agents (these belong to the human-evidence track); position papers
that name a mechanism without testing it (recorded as `discussed`, not `tested`).

**Screening record.** For each query: date run, source, hits, screened on
title/abstract, included, and exclusion reasons — reported as a PRISMA-style flow in
the paper.

**Theme slice (G7).** A seventh slice collects papers that report emergent group-level
behavior among artificial agents (conventions, culture, collective dynamics, collusion,
agent societies), whether or not they test a mechanism. These papers may have empty
`mechanism_ids`. Every paper carries zero or more `themes` tags from a fixed vocabulary:
`emergent_culture`, `emergent_norms`, `emergent_communication`, `emergent_structure`,
`collective_dynamics`, `emergent_collusion`, `agent_societies`, `emergent_institutions`.

**Run.** Six slices (G1–G6) covering the 17 primitives, plus G7, each run by an LLM search agent
on 2026-09-29. The merge de-duplicates papers by arXiv ID, then DOI, then normalized
title. It added one mechanism the seed lacked (P04-06, peer reward / gifting) and
reconciled citation keys that differed between slices (`KEY_ALIASES` in the script).

**Instance slices (2b).** I_A covers social and life sciences, I_B technical and
sociotechnical systems, and I_C AI-agent governance gaps. `scripts/build_instances.py`
combines them with the search papers and the seed's human examples into `instances.csv`.

### Search status: resume when the web-search budget resets

The session's web-search budget (200 queries) ran out during G7, so the three instance
slices ran with reduced coverage. They are **not complete** and should be re-run or
extended with web search:

| Slice | What happened | Resume with |
|---|---|---|
| G7 (emergent behavior) | Finished on arXiv API searches after the budget ran out | Post-2018 MARL emergent communication; Y Social / S3 social-network simulators; leader emergence among LLM agents |
| I_A (social sciences) | No web search. Sources were recalled, and every DOI was checked on Crossref (28 recalled DOIs corrected). 88 of 105 instances are `located_via=search`: the paper exists, but the description was coded from recall, not the source | Open each source and check `description`/`evidence`; sociology is thin (1 instance); add Greif 1993, Mauss, Braithwaite (books), IAEA safeguards, escrow |
| I_B (technical systems) | No web search. Recalled, checked on Crossref and by fetching docs and RFCs; 28 of 95 are `search`; some numbers are marked "(from memory)" | Piatek 2007 and Kalodner 2018 (USENIX pages blocked); a Kleros primary source; multi-robot systems |
| I_C (AI-agent gaps) | arXiv API only; coded from abstracts | METR and Cooperative AI Foundation reports; the A2A / AP2 / MCP permission specs; 2025 AI Agent Index (arXiv 2602.17753); venue labels filled in from memory |

A resumed slice writes to the same file name; re-running `build_instances.py` picks it up.

## 6. Verification

Every record is checked by the verifier against its cited source before it is marked
`verified`. `scripts/build_verify_queue.py` writes `verify_queue.csv`, which orders the
checks. It lists records placed by judgment and additions from the search first, then
seed claims the search could not confirm, papers not confirmed from an opened page, and
incidents. A citation that cannot be located is removed rather than repaired from
memory. LLM-extracted fields carry their source URL until verified.

## 7. Known limitations

- Single verifier; no inter-rater agreement statistic.
- The seed inherits the original spreadsheet's selection; the Phase 2 search widens
  coverage for artificial agents, but human-literature coverage remains curated.
- `llm_status` reflects what the search found by its run date; absence of evidence is
  recorded as `untested`, not as evidence that a mechanism fails.
