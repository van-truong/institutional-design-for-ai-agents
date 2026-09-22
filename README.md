# Institutional Design for AI Agents

Springer LNCS proceedings source for *Multi-Agent AI Systems Need Institutional Design, Not Just Model-Level Alignment*, presented at the ICML 2026 Trustworthy AI4GOOD Workshop.

**Website:** [Interactive paper companion](https://www.vanquynh.com/institutional-design-for-ai-agents/)

The active paper, bibliography, figures, and LNCS style files are in `manuscript/`. The original ICML camera-ready materials are preserved in `archive/icml2026/`.

We are preparing a lightly revised archival version for the Springer LNCS proceedings. The revision should preserve the workshop paper's argument, structure, and human voice.

Build the paper with:

```bash
make pdf
```

The build regenerates vector figures from the editable HTML files in `manuscript/figs/` and writes `springer-lncs-proceedings.pdf`. Inkscape is not required.

The review PDF shows flagged claims in red. The switches near the top of `manuscript.tex` can hide those flags for the final PDF or show named `\VAN{}`, `\ANG{}`, `\ERI{}`/`\ERIVAN{}`, and other inline author comments during editing.

### Review PDF color key

- `\VAN{}` / `\vqt{}` = blue
- `\ANG{}` = orange
- `\ERI{}` / `\ERIVAN{}` = violet
- `\RYAN{}` = teal
- `\JOEL{}` = magenta
- `\REVISED{}` = purple
- `\TODO{}` / `\REVIEWFLAG{}` = red

The switches near the top of `manuscript.tex` control whether review colors appear.

## Co-author review

- [ ] **Author metadata:** confirm order, co-first authorship, affiliations, emails, ORCIDs, disclosures, and Van QT Truong as sole corresponding author (`scientistvan@gmail.com`). Add the corresponding-author marker to the manuscript.
- [ ] **Final title:** choose the current title or a modest archival update:
  - `Multi-Agent AI Systems Need Institutional Design, Not Just Model-Level Alignment` (current)
  - `Institutional Design for Cooperative Multi-Agent AI Systems`
  - `Beyond Model-Level Alignment: Institutional Design for Multi-Agent AI`
  - `Designing Institutions for Safe Cooperation Among AI Agents`
- [ ] **Claim audit:** resolve the opening anecdotes, Flash Crash chronology, and flagged daycare/AWS/Amazon/1929/Ostrom/deployment claims with exact sources or narrower wording.
- [x] ~~Add the conceptual bridge and repair incompatible author-bearing citations.~~
- [x] ~~Refine the editable HTML figures and poster-derived website artwork.~~
- [ ] **Final content/figure pass:** approve blue additions, consider one sharper evaluation example, verify Figure 5 counts and captions, and inspect every figure at LNCS print size.
- [ ] **Clean PDF:** disable review colors, clear bibliography/reference warnings, and verify that source and PDF match exactly.

Keep revisions light, source-backed, and in the paper's human voice.

## LNCS final submission (Van will submit after co-authors verify their info)

- [x] ~~Convert the paper to the official Springer LNCS template.~~
- [ ] Finalize title/authors/affiliations and complete the [metadata sheet](https://docs.google.com/spreadsheets/d/1Y90xfC0UPxPT60WwL3coFsegIEaLlC78iyCaVnYzb9I/edit?usp=sharing): OpenReview `308`, one corresponding author, all emails and ORCIDs.
- [ ] Add Disclosure of Interests; confirm permissions and supplementary material; complete the [Springer LTP](https://docs.google.com/document/d/1JD0O4ZdV08ZwD7Os7CmzxDF3gm_FQFae/edit?usp=sharing).
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
