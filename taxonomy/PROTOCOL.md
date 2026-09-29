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
| 1. Seed | `primitives.csv`, `mechanisms.csv`, `pathologies.csv` from the original spreadsheet (de-duplicated union of the Overview and First-Principles sheets) | in progress |
| 2. LLM + MARL search | `papers.csv`; updates `llm_status`, `llm_evidence`, `marl_status` | not started |
| 3. Human-literature verification | verified `key_references` per mechanism | not started |
| 4. News incidents (separate track) | `incidents.csv`: verified reports of AI agents acting outside authorization, gaining unauthorized access, or leaking data | not started |
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

## 6. Verification

Every record is checked by the verifier against its cited source before it is marked
`verified`. A citation that cannot be located is removed rather than repaired from
memory. LLM-extracted fields carry their source URL until verified.

## 7. Known limitations

- Single verifier; no inter-rater agreement statistic.
- The seed inherits the original spreadsheet's selection; the Phase 2 search widens
  coverage for artificial agents, but human-literature coverage remains curated.
- `llm_status` reflects what the search found by its run date; absence of evidence is
  recorded as `untested`, not as evidence that a mechanism fails.
