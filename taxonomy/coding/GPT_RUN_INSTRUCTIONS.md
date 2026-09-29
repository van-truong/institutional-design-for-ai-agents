# Cross-model coding run: instructions for the GPT agent

Goal: two GPT models independently repeat both coding passes of the taxonomy. We then measure how well they agree with the final Claude-coded dataset and with each other, and replace the red placeholder in Appendix A with the result.

Repo root: `institutional-design-for-ai-agents/`. Branch: `van-revisions`. Do not commit, push, or switch branches. The author will review and commit.

## 0. Models and run manifest

- Use two different GPT models: **MODEL_A = `<fill in>`** and **MODEL_B = `<fill in>`**. The author names them. If none are given, ask before starting.
- Write `taxonomy/coding/gpt/RUNS.md` recording, for each model:
  - the exact model ID and date
  - how it was called (API or agent session)
  - temperature and seed, if settable
  - any batch that failed and was retried
- **Independence rules:**
  - Each model codes each batch in a fresh context: a new API call or a new subagent with no memory of other batches.
  - A model never sees another model's output, or any Claude output.
  - Prefer the OpenAI API with `OPENAI_API_KEY`, one request per batch per pass, and temperature 0 where supported. Save the raw responses under `taxonomy/coding/gpt/<model>/raw/`.

## 1. Inputs (fixed; do not edit)

| File | Use |
|---|---|
| `taxonomy/coding/batch1.json` … `batch4.json` | The 561 instances, split into 4 batches (same batches the Claude coders got) |
| `taxonomy/coding/CODING_GUIDE.md` | Pass-1 instructions (open coding) |
| `taxonomy/coding/CODING_GUIDE_PASS2.md` | Pass-2 instructions (deductive recoding) |
| `taxonomy/coding/CODEBOOK_FINAL.md` | The final 66-mechanism codebook. **Use this in pass 2 wherever the guide says `CODEBOOK_PASS2.md`**, because that older file predates the final codebook. |

**Blinding.** The GPT coders must not be given any of the following:
- `pass1_*`, `pass2_*`, `pass3_*`, `disagreements.csv`, `pass2_review.csv`
- `instances.csv`, `codebook.csv`, `coding_log.csv`, `configurations.csv`
- the manuscript

Pass the batch file and the guide text only. For pass 2, also pass `CODEBOOK_FINAL.md`. You, the orchestrator, may read everything to compute agreement afterwards.

## 2. Pass 1: open coding (per model)

For each batch, give the model `CODING_GUIDE.md` and the batch. Write:

- `taxonomy/coding/gpt/<model>/pass1_batchN.json`
- `taxonomy/coding/gpt/<model>/pass1_batchN_codes.json`

Use the schema in the guide. Validate each file:
- every `instance_id` in the batch is present, once
- the enum fields hold allowed values
- the JSON parses

Re-request only the batches that fail, and log the retries in `RUNS.md`.

**Ending-condition check.** Map each GPT open code to the closest mechanism in `CODEBOOK_FINAL.md`, or mark it `NEW` if no mechanism covers its lever. Do this in a separate step, as the orchestrator, and log every decision to `taxonomy/coding/gpt/<model>/pass1_code_map.csv` with columns `open_code, n_instances, mechanism_id_or_NEW, rationale`. A `NEW` code means that model found a lever the codebook lacks. Report these; do not add them to the codebook.

## 3. Pass 2: recoding against the codebook (per model)

For each batch, give the model `CODING_GUIDE_PASS2.md` (with `CODEBOOK_FINAL.md` substituted for `CODEBOOK_PASS2.md`), `CODEBOOK_FINAL.md`, and the batch. Write `taxonomy/coding/gpt/<model>/pass2_batchN.json`, then validate it the same way:
- every `mechanism_id` and `configuration_id` exists in `CODEBOOK_FINAL.md`
- enums hold allowed values
- every id is present

## 4. Agreement

Write `taxonomy/scripts/cross_model_agreement.py`, using only the standard library, in the style of `taxonomy/scripts/pass2_compare.py` (you may reuse its `kappa` function). It reads the GPT pass-2 files and `taxonomy/instances.csv` and writes `taxonomy/coding/gpt/agreement.txt` and `taxonomy/coding/gpt/cross_model_disagreements.csv`.

**Reference coding.** Use the `mechanism` and `kind` columns of `instances.csv` (the final coding). Also report agreement with `mechanism_p2` (the independent Claude pass 2) as a secondary line.

**Report:**
1. Per GPT model vs the reference: percent agreement and Cohen's κ on the primary mechanism, over instances that both codings code as `kind = mechanism` with a valid M-id. Give the n. Repeat at the theme level; the theme is `theme_id` in `codebook.csv`, looked up by M-id.
2. MODEL_A vs MODEL_B: the same metrics.
3. Fleiss' κ across the three codings (reference, MODEL_A, MODEL_B) on instances where all three code a single mechanism. Give the n.
4. Agreement on `kind` (mechanism / configuration / phenomenon / out_of_scope) as percent agreement and κ, per GPT model vs the reference.
5. Per model:
   - counts of `fit` (good / partial / misfit)
   - the number of `NEW` levers from the pass-1 code map
   - which mechanisms the model never used
6. Agreement on `evidence_type` per GPT model vs the reference `evidence_type` column (percent and κ).

**Disagreements file.** `cross_model_disagreements.csv` lists every instance where **both** GPT models agree with each other but differ from the reference mechanism, since those are the strongest signals of a reference error. Then list instances where all three differ. Use the same columns as `taxonomy/coding/disagreements.csv`: `instance_id, title, url, discipline, description, evidence, p1, p1_definition, p2, p2_definition, decision, verifier, note`. Here `p1` is the reference, and `p2` is the GPT consensus or "A: Mxx / B: Myy". Leave `decision` blank for the author.

## 5. Update the manuscript and protocol

**Manuscript** (`manuscript/manuscript.tex`, Appendix A, *Coding* paragraph). Replace exactly this text:

```
\REVIEWFLAG{[Planned: two GPT models will repeat both coding passes independently, and this section will be updated with the agreement across the merged codings.]}
```

Replace it with one or two sentences wrapped in `\chg{...}`, for example:

```
\chg{To test sensitivity to the coding model, two GPT models (MODEL_A, MODEL_B) independently repeated both passes on the same inputs. Their agreement with the final coding on the primary mechanism was X\% ($\kappa = \ldots$) and Y\% ($\kappa = \ldots$), and Fleiss' $\kappa$ across the three codings was Z ($n = \ldots$). Their open codes produced N levers not covered by the codebook.}
```

Writing rules:
- Report the numbers as they come out.
- Do not round in a way that changes the reading.
- Do not describe the agreement as good or bad unless the numbers clearly support it.
- If `NEW` levers exist, say so plainly and name them in `agreement.txt`.
- Keep the separate red `\REVIEWFLAG{[verification in progress]}` flag unchanged; that one is the author's.
- Use `\mbox{}` around any `\ref` or `\cite` inside `\chg`.
- Use US spelling, and no em-dash asides.

**Limitations sentence.** The Limitations sentence currently says "All coders were LLMs…". Leave it, unless the GPT results change what it should say. Then edit minimally, inside `\chg`.

**Protocol** (`taxonomy/PROTOCOL.md`). Add a row to the "Coding status" table for the cross-model run: the models, date, headline agreement numbers, and a pointer to `coding/gpt/agreement.txt`.

## 6. Build check

From the repo root, run `make pdf`, then check:

```
grep -c '^!' manuscript/.build/manuscript.log                       # must be 0
grep 'Warning.*undefined' manuscript/.build/manuscript.log          # must be empty
```

If `make pdf` fails on stale figures, run `rm -rf manuscript/.build` and rebuild.

## 7. Report back

Summarize the following in chat:
- the models used
- the table of metrics from `agreement.txt`
- any `NEW` levers
- the number of rows in `cross_model_disagreements.csv`
- the exact sentence you put in the manuscript
- the list of files created or changed

Do not commit. Do not add co-author or attribution trailers anywhere.

## Constraints

- Do not edit any existing file under `taxonomy/coding/` or `taxonomy/search_raw/`, or `instances.csv`, `codebook.csv`, `configurations.csv`, or `coding_log.csv`. All new output goes under `taxonomy/coding/gpt/`, plus the new script.
- Do not modify the private spreadsheet `2026-04-07_Sanctioning_taxonomy.xlsx` or anything under `lab-notebook/`.
- Do not regenerate figures.
