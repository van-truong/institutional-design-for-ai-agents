# GPT coding runs

Date: 2026-09-29

| Model | Exact model ID | How called | Temperature / seed | Failed batches retried |
|---|---|---|---|---|
| MODEL_A | `gpt-6-luna` | Fresh Codex agent session for each batch and pass; each session received only its staged guide, batch, and (for pass 2) `CODEBOOK_FINAL.md`. | Not settable in agent sessions. | Pass 1: batches 1–4 initially stopped with partial outputs and were rerun. Pass 2: batches 1–2 initially stopped with partial outputs and were rerun; batch 4 failed at 134/140, then was retried. |
| MODEL_B | `gpt-5.6-terra` | Fresh Codex agent session for each batch and pass; each session received only its staged guide, batch, and (for pass 2) `CODEBOOK_FINAL.md`. | Not settable in agent sessions. | None so far. |

No web sources were consulted because the coding instructions fix the evidence to the staged batch, guide, and codebook inputs.

Pass-1 code maps (`pass1_code_map.csv`) were written by the orchestrator (Claude), one subagent per model, from `CODEBOOK_FINAL.md`, the GPT files and the batches only, using that model's own pass-2 codes as a prior. Neither map has a `NEW` code. Raw responses were not saved for gpt-5.6-terra pass 1 batch 4 or gpt-6-luna pass 2 batches 1 and 4.
