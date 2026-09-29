# GPT coding runs

Date: 2026-09-29

| Model | Exact model ID | How called | Temperature / seed | Failed batches retried |
|---|---|---|---|---|
| MODEL_A | `gpt-6-luna` | Fresh Codex agent session for each batch and pass; each session received only its staged guide, batch, and (for pass 2) `CODEBOOK_FINAL.md`. | Not settable in agent sessions. | Pass 1: batches 1–4 initially stopped with partial outputs and were rerun. Pass 2: batches 1–2 initially stopped with partial outputs and were rerun; batch 1 had another incomplete attempt (136/141); batch 4 had two incomplete attempts (no saved output, then 134/140) before validation passed. |
| MODEL_B | `gpt-5.6-terra` | Fresh Codex agent session for each batch and pass; each session received only its staged guide, batch, and (for pass 2) `CODEBOOK_FINAL.md`. | Not settable in agent sessions. | None. |

No web sources were consulted because the coding instructions fix the evidence to the staged batch, guide, and codebook inputs.

The orchestrator mapped each pass-1 open code separately to `CODEBOOK_FINAL.md` using only that model's pass-1 code summaries; pass-2 outputs were not used in the mapping. The map contains 0 `NEW` codes for GPT-6-Luna and 3 for GPT-5.6-Terra: `adjust agent memory depth`, `adjust decision randomness`, and `induce confirmation bias`.

Each `raw/passN_batchN.txt` is the completed JSON response for that batch. Pass-1 coding JSON files were schema-normalized after preserving the raw JSON: fields other than `phenomenon` were blanked on `is_mechanism: false` rows, and whitespace around lever enum values was trimmed. The raw copies retain the pre-normalization responses.
