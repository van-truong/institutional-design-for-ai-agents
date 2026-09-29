# Institutional Design for AI Agents

Springer LNCS proceedings source for *Multi-Agent AI Systems Need Institutional Design, Not Just Model-Level Alignment*, presented at the ICML 2026 Trustworthy AI4GOOD Workshop.

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
- [ ] **Author metadata:** each co-author confirms order, co-first authorship, affiliations, emails, ORCIDs, and disclosures.
- [ ] **Final title:** choose the current title or a modest archival update:
  - `Multi-Agent AI Systems Need Institutional Design, Not Just Model-Level Alignment` (current)
  - `Institutional Design for Cooperative Multi-Agent AI Systems`
  - `Beyond Model-Level Alignment: Institutional Design for Multi-Agent AI`
  - `Designing Institutions for Safe Cooperation Among AI Agents`
- [x] ~~**Claim audit:** resolve the opening anecdotes, Flash Crash chronology, and flagged daycare/AWS/Amazon/1929/Ostrom/deployment claims with exact sources or narrower wording.~~
- [x] ~~Verify every cited reference (no fabricated sources); update preprints to their published versions.~~
- [x] ~~Rebuild the taxonomy from a documented search and thematic coding (Appendix A), with a cross-model coding check.~~
- [x] ~~Add the conceptual bridge and repair incompatible author-bearing citations.~~
- [x] ~~Refine the editable HTML figures and poster-derived website artwork.~~
- [x] ~~Approve blue, green, and yellow additions.~~
- [ ] **Final content/figure pass:** redesign Figs 1 and 6 (pink "Draft figure" captions), verify the taxonomy figure counts and captions, and inspect every figure at LNCS print size.
- [ ] **Remaining strikeouts:** review the red `\del{}` text (Sections 3, 6, Discussion, Appendices A and B).
- [ ] **Table 2:** replace with an untested-mechanisms table or delete.
- [ ] **Alternative Views + Discussion:** decide whether to merge them into one section.
- [ ] **Taxonomy:** code the 84 new instances (I0562–I0645) and re-run the downstream scripts; the verifier reviews `coding/gpt/cross_model_disagreements.csv` and the I_A source flags, then clears the red "verification in progress" flag.
- [x] ~~Clear bibliography and reference warnings.~~
- [ ] **Clean PDF:** disable review colors (`\showreviewflagsfalse`) and verify that source and PDF match exactly.

Keep revisions light, source-backed, and in the paper's human voice.

## LNCS final submission (Van will submit after co-authors verify their info)

- [x] ~~Convert the paper to the official Springer LNCS template.~~
- [ ] Finalize title/authors/affiliations and complete the [metadata sheet](https://docs.google.com/spreadsheets/d/1Y90xfC0UPxPT60WwL3coFsegIEaLlC78iyCaVnYzb9I/edit?usp=sharing): OpenReview `308`, one corresponding author, all emails and ORCIDs.
- [x] ~~Add Disclosure of Interests.~~
- [ ] Confirm permissions and supplementary material; complete the [Springer LTP](https://docs.google.com/document/d/1JD0O4ZdV08ZwD7Os7CmzxDF3gm_FQFae/edit?usp=sharing).
- [ ] Package the matching PDF and clean source as `OpenReview_308_Truong.zip`, then upload it to the [submission folder](https://drive.google.com/drive/folders/1Pt1cvqcWZGlNgVKuyEwlLPJ_Hm3sA_oI?usp=sharing).
- [ ] Be available for the Springer proof turnaround (approximately 72 hours).

## Website follow-up

[Visit the interactive paper companion](https://www.vanquynh.com/institutional-design-for-ai-agents/). Hat tip to Angelo Huang and the [Prosocial Agents paper website](https://flecart.github.io/prosocial-agents/) for the inspiration. The archival paper stays fixed; this evidence map can evolve.

- [x] ~~Launch the poster-inspired landing page with author photos and artwork.~~
- [x] ~~Make Figure 5 interactive by hover, click, touch, and keyboard; rotate and highlight the selected branch.~~
- [x] ~~Expose uncurated leaves and evidence gaps instead of implying complete coverage.~~
- [ ] Add a small, verified set of evidence records with exact links, supported claims, source locations, and limitations.
- [ ] Add evidence-status filters, search, stable leaf links, and an accessible list view.
- [ ] Add reviewed issue/PR contribution templates, attribution, change history, and dated snapshots.
