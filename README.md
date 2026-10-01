# Institutional Design for AI Agents

Springer LNCS proceedings source for *From Aligned Models to Governed Societies: A Cross-Disciplinary Map of Cooperation Mechanisms and Emergent Patterns*, presented at the ICML 2026 Trustworthy AI4GOOD Workshop (originally titled *Multi-Agent AI Systems Need Institutional Design, Not Just Model-Level Alignment*).

**Website:** [Interactive paper companion](https://www.vanquynh.com/institutional-design-for-ai-agents/)

The active paper, bibliography, figures, and LNCS style files are in `manuscript/`. The original ICML camera-ready materials are preserved in `archive/icml2026/`.

We are preparing a lightly revised archival version for the Springer LNCS proceedings. The revision should preserve the workshop paper's argument, structure, and human voice.

Build the paper with:

```bash
make pdf
```

The build uses the submission-ready vector PDFs in `manuscript/figures/` and writes `springer-lncs-proceedings.pdf`. Run `make figures` only when intentionally regenerating those PDFs from the editable HTML files in `manuscript/figs/`. Inkscape is not required.

The review PDF shows flagged claims in red. The switches near the top of `manuscript.tex` can hide those flags for the final PDF or show named `\VAN{}`, `\ANG{}`, `\ERI{}`/`\ERIVAN{}`, and other inline author comments during editing.

### Review PDF color key

- `\VAN{}` / `\vqt{}` = blue
- `\ANG{}` = orange
- `\ERI{}` / `\ERIVAN{}` = violet
- `\RYAN{}` = teal
- `\JOEL{}` = magenta
- `\REVISED{}` = purple
- `\TODO{}` / `\REVIEWFLAG{}` = red
- `\del{}` = red strikeout (proposed deletion; hidden when review flags are off)
- `\rework{}` = pink highlight (figure or caption still to be redesigned)

The switches near the top of `manuscript.tex` control whether review colors appear.

## Co-author review

- [x] ~~Add ORCIDs, the co-first-author and corresponding-author markers, and the corresponding email to the manuscript.~~
- [x] ~~**Author metadata:** each co-author confirms order, co-first authorship, affiliations, emails, ORCIDs, and disclosures.~~
- [x] ~~**Final title:** `From Aligned Models to Governed Societies: A Cross-Disciplinary Map of Cooperation Mechanisms and Emergent Patterns`.~~
- [x] ~~**Claim audit:** resolve the opening anecdotes, Flash Crash chronology, and flagged daycare/AWS/Amazon/1929/Ostrom/deployment claims with exact sources or narrower wording.~~
- [x] ~~Verify every cited reference (no fabricated sources); update preprints to their published versions.~~
- [x] ~~Rebuild the taxonomy from a documented search and thematic coding (Appendix A), with a cross-model coding check.~~
- [x] ~~Add the conceptual bridge and repair incompatible author-bearing citations.~~
- [x] ~~Refine the editable HTML figures and poster-derived website artwork.~~
- [x] ~~Approve blue, green, and yellow additions.~~
- [ ] **Final content/figure pass:** Figs 1–8 are redesigned and the draft evaluation matrix (old Fig 9) is dropped; still check every figure at LNCS print size (Fig 1 ring text prints at about 4pt).
- [ ] **Remaining strikeouts:** review the red `\del{}` text (Sections 3, 6, Discussion, Appendices A and B).
- [x] ~~**Table 2:** replaced with a failure-mode flow figure (Fig. 6); merged the two metrics tables; expanded the evaluations table into an inventory.~~
- [x] ~~**Alternative Views + Discussion:** merged into one section, "Alternative Views and Open Questions".~~
- [ ] **Taxonomy:** code the 84 new instances (I0562–I0645) and re-run the downstream scripts; the verifier reviews `coding/gpt/cross_model_disagreements.csv` and the I_A source flags, then clears the red "verification in progress" flag.
- [x] ~~Clear bibliography and reference warnings.~~
- [ ] **Clean PDF:** disable review colors (`\showreviewflagsfalse`) and verify that source and PDF match exactly.

Keep revisions light, source-backed, and in the paper's human voice.

## LNCS final submission (Van will submit after co-authors verify their info)

> **⚠ Do not submit until these are done** (blockers found 2026-10-01):
>
> - [ ] **Verify the seven incidents shown in Fig. 6** against their primary sources, then set `verified` in `taxonomy/incidents.csv` (all rows are currently blank). Drop any chip you cannot confirm, then rerun `python3 scripts/gen_web_figs.py figure_phenomena-map` from `manuscript/`.
>   - Multi-agent "turf wars" (2026), `anthropic-multiagent-turf-wars`
>   - Agents collude to bypass guardrails (2026), `emergence-collusion-sim`
>   - Hidden message board to cheat an eval (2026), `metr-redwood-agent-message-board`
>   - Agents turned against each other (2025), `servicenow-agent-to-agent-injection`
>   - Agents breach production infrastructure (2026), `openai-hf-intrusion-2026`
>   - Agents hijack a live website (2026), `openai-dsewiki-breakout`
>   - AI-orchestrated espionage campaign (2025), `anthropic-gtg1002-espionage`
> - [ ] **Resolve the two red `\REVIEWFLAG` notes**, which print as text even with review colors off:
>   - Sec. 3 ("Separating phenomena from mechanisms"): say who grouped the phenomenon labels into types and assigned effects, and how.
>   - Appendix A ("Limitations"): replace "[verification in progress]" with what was actually verified.
> - [ ] **Turn review colors off** (`\showreviewflagsfalse`), rebuild, and confirm no highlight, strikeout, or placeholder text remains.

- [x] ~~Convert the paper to the official Springer LNCS template.~~
- [x] ~~Finalize title/authors/affiliations and complete the [metadata sheet](https://docs.google.com/spreadsheets/d/1Y90xfC0UPxPT60WwL3coFsegIEaLlC78iyCaVnYzb9I/edit?usp=sharing): OpenReview `308`, one corresponding author, all emails and ORCIDs.~~
- [x] ~~Add Disclosure of Interests.~~
- [x] ~~Sign the [Springer LTP](https://docs.google.com/document/d/1JD0O4ZdV08ZwD7Os7CmzxDF3gm_FQFae/edit?usp=sharing) (handwritten signature).~~ Saved in `manuscript/OpenReview_308_Truong/`, which is git-ignored and must never be committed.
- [ ] Confirm third-party permissions and any supplementary material (none planned beyond the public website and dataset).
- [ ] Turn review flags off (`\showreviewflagsfalse`), rebuild, and check the PDF has no colored flags, strikeouts, or placeholder text.
- [ ] Assemble the package in `manuscript/OpenReview_308_Truong/` (see below), test-compile it, then zip it as `OpenReview_308_Truong.zip` and upload it to the [submission folder](https://drive.google.com/drive/folders/1Pt1cvqcWZGlNgVKuyEwlLPJ_Hm3sA_oI?usp=sharing).

### Submission package

Springer wants one ZIP per paper with actual copies (no links) of: all `.tex` files, the figures, the required style files, the `.bib` and `.bbl` files, the compiled PDF, and the signed LTP. The PDF must correspond exactly to the source, file names should be short, and only one version of each file may be included. Alt text is optional; Springer may generate it in production.

| File | Source |
|---|---|
| `manuscript.tex` | `manuscript/manuscript.tex` (review flags off) |
| `references.bib` | `manuscript/references.bib` |
| `manuscript.bbl` | `manuscript/manuscript.bbl` (`make pdf` keeps it in sync with `.build/`) |
| `llncs.cls`, `splncs04.bst` | `manuscript/` |
| `figures/*.pdf` | only the figures the paper includes (9 files) |
| `manuscript.pdf` | the compiled PDF, `springer-lncs-proceedings.pdf` |
| `LTP_308_Truong.pdf` | the signed LTP, renamed to a short name |

From `manuscript/`, after the final `make pdf`:

```bash
PKG=OpenReview_308_Truong
mkdir -p $PKG/figures
cp manuscript.tex references.bib llncs.cls splncs04.bst $PKG/
cp .build/manuscript.bbl $PKG/
cp ../springer-lncs-proceedings.pdf $PKG/manuscript.pdf
grep -v '^[[:space:]]*%' manuscript.tex | grep -o 'includegraphics[^{]*{figures/[^}]*}' \
  | grep -o 'figures/[^}]*' | sort -u | xargs -I{} cp {} $PKG/figures/
ls $PKG $PKG/figures

# test-compile a throwaway copy to confirm the package is complete and matches the PDF
rm -rf /tmp/pkgtest && cp -r $PKG /tmp/pkgtest && (cd /tmp/pkgtest && latexmk -pdf -interaction=nonstopmode manuscript.tex >/dev/null)
pdfinfo /tmp/pkgtest/manuscript.pdf | grep Pages; pdfinfo $PKG/manuscript.pdf | grep Pages

zip -r OpenReview_308_Truong.zip $PKG
```
- [ ] Be available for the Springer proof turnaround (approximately 72 hours).

## Website follow-up

[Visit the interactive paper companion](https://www.vanquynh.com/institutional-design-for-ai-agents/). Hat tip to Angelo Huang and the [Prosocial Agents paper website](https://flecart.github.io/prosocial-agents/) for the inspiration. The archival paper stays fixed; this evidence map can evolve.

- [x] ~~Launch the poster-inspired landing page with author photos and artwork.~~
- [x] ~~Make Figure 5 interactive by hover, click, touch, and keyboard; rotate and highlight the selected branch.~~
- [x] ~~Expose uncurated leaves and evidence gaps instead of implying complete coverage.~~
- [ ] Add a small, verified set of evidence records with exact links, supported claims, source locations, and limitations.
- [x] ~~Add evidence-status filters, search, stable leaf links, and an accessible list view.~~ (interactive taxonomy: circle that unravels into the Fig. 4 list; every mechanism links to its coded sources)
- [ ] Add reviewed issue/PR contribution templates, attribution, change history, and dated snapshots.
