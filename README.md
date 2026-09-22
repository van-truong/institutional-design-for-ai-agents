# Institutional Design for AI Agents

Springer LNCS proceedings source for *Multi-Agent AI Systems Need Institutional Design, Not Just Model-Level Alignment*, presented at the ICML 2026 Trustworthy AI4GOOD Workshop.

The active paper, bibliography, figures, and LNCS style files are in `manuscript/`. The original ICML camera-ready materials are preserved in `archive/icml2026/`.

We are preparing a lightly revised archival version for the Springer LNCS proceedings. The revision should preserve the workshop paper's argument, structure, and human voice.

Build the paper with:

```bash
make pdf
```

The build regenerates vector figures from the editable HTML files in `manuscript/figs/` and writes `springer-lncs-proceedings.pdf`. Inkscape is not required.

The review PDF shows flagged claims in red. The switches near the top of `manuscript.tex` can hide those flags for the final PDF or show named `\VAN{}`, `\ANG{}`, `\ERI{}`/`\ERIVAN{}`, and other inline author comments during editing.

### Review PDF color key

- **Blue body text:** prose proposed by Van for the archival revision (`\vqt{}`).
- **Dark red body text:** claims or wording that need the human review listed below (`\REVIEWFLAG{}`).
- **Named inline comments:** hidden by default; when enabled, Van is blue, Angelo is orange, Erivan is violet, Ryan is teal, and Joel is magenta.
- Review colors are controlled by the switches near the top of `manuscript.tex` and should be disabled in the final archival PDF.

## Co-author review

- [ ] **Author metadata:** confirm co-first authorship for Van Truong and Xuanqiang Angelo Huang; Van QT Truong as the sole corresponding author (`scientistvan@gmail.com`); affiliations; ORCIDs; disclosures; and contribution statement. The corresponding-author designation still needs to be marked explicitly in the manuscript.
- [ ] **Final title:** decide whether to retain the current working title or adopt a modest archival update:
  - `Multi-Agent AI Systems Need Institutional Design, Not Just Model-Level Alignment` (current)
  - `Institutional Design for Cooperative Multi-Agent AI Systems`
  - `Beyond Model-Level Alignment: Institutional Design for Multi-Agent AI`
  - `Designing Institutions for Safe Cooperation Among AI Agents`
- [ ] **Opening examples:** review narrower wording for the cryptocurrency transfer and Citibank anecdotes. The current Citibank citation predates the appellate outcome it is used to support.
- [ ] **Flash Crash:** correct the claim that trade-cancellation rules were created only after 2010; the SEC approved cross-exchange rules in 2009.
- [ ] **Evidence claims:** verify the daycare-study interpretation, AWS smart-bed anecdote, Amazon textbook price, 1929 comparison, Ostrom community-size figures, claims that surveys or benchmarks demonstrate deployed AI systems, and categorical claims about current agents' institutional capacities.
- [ ] **Scope and voice:** approve only small, source-backed corrections. Avoid restructuring the paper, adding new empirical claims, or flattening the authors' voice.
- [x] **Conceptual bridge:** added a short explanation connecting cooperation dilemmas, institutional functions, mechanism families, and evaluation dimensions; awaiting co-author approval in blue.
- [ ] **Evaluation example:** consider sharpening one existing example with a baseline, intervention, repeated trials, and success and failure measures.
- [ ] **Figure source refinement:** fix overrunning or clipped text in the editable HTML figures, refine spacing and visual hierarchy, regenerate every vector PDF, and inspect the figures at their final LNCS print size.
- [ ] **Figures and format:** verify Figure 5's stated counts, figure order and captions, readability, corresponding-author placement, and all LNCS submission requirements.
- [x] **Citation rendering:** replace incompatible author-bearing citations; the review PDF no longer contains `(author?)`.
- [ ] **Final PDF check:** turn off review colors, resolve remaining bibliography metadata warnings, and check for unresolved references, visible comments, clipping, and source/PDF mismatch.

## LNCS final submission (Van will submit after co-authors verify their info)

- [x] Use the official Springer LNCS proceedings template.
- [ ] Finalize the title, author names and order, affiliations, running head, and name-rendering instructions. Mark Van QT Truong as the **sole corresponding author** with `scientistvan@gmail.com`; authorship cannot change after delivery to Springer.
- [ ] Include the required Disclosure of Interests statement. Resolve any third-party permissions and approved supplementary-material files; add figure alt text if available.
- [ ] Complete the [AI4GOOD author metadata sheet](https://docs.google.com/spreadsheets/d/1Y90xfC0UPxPT60WwL3coFsegIEaLlC78iyCaVnYzb9I/edit?usp=sharing) with the OpenReview submission number, final title, separated given/family names, affiliations, exactly one corresponding author, corresponding-author email, every author email, and every ORCID. Preserve the publication order and separate multiple entries with semicolons.

Draft spreadsheet values to verify:

- **OpenReview submission number:** `308`
- **Title:** `Multi-Agent AI Systems Need Institutional Design, Not Just Model-Level Alignment`
- **Given names:** `Van QT; Xuanqiang Angelo; Erivan; Ryan; Joël Naoki; Terry Jingchen; David; Zhijing`
- **Family names:** `Truong; Huang; Inan; Faulkner; Christoph; Zhang; Guzman Piedrahita; Jin` — confirm that `Guzman Piedrahita` is indexed as one compound family name.
- **Affiliation mapping:** Truong (1, 2); Huang (2, 3, 4, 5); Inan (2, 3); Faulkner (2, 3); Christoph (6); Zhang (2, 3); Guzman Piedrahita (2, 3, 4); Jin (2, 3, 7). Van QT Truong is no longer affiliated with EuroSafeAI. Confirm the seven numbered affiliations against the paper before transcribing them.
- **Affiliations:** 1—University of Pennsylvania, Philadelphia, PA, USA; 2—Jinesis Lab, University of Toronto and Vector Institute, Toronto, Canada; 3—EuroSafeAI; 4—ETH Zürich, Zürich, Switzerland; 5—Institute for Decentralized AI, Oxford, UK; 6—Harvard Kennedy School, Cambridge, MA, USA; 7—Max Planck Institute for Intelligent Systems, Tübingen, Germany.
- **Corresponding author:** `Van QT Truong`; `scientistvan@gmail.com`. The manuscript still needs an explicit corresponding-author marker.
- **Still needed from authors:** all remaining author emails; all ORCIDs; optional indexing notes; final title approval; and confirmation of supplementary material and third-party permissions.
- **Current status fields:** source format is `LaTeX`; Disclosure of Interests and signed LTP are not yet complete; final authorship/order and final PDF/source match remain pending.
- Leave `Organizer: Part / Topical Section`, `Organizer: Starting Page / Sequence No.`, and `Organizer: Paper Number in Submission Folder` blank for the organizers unless instructed otherwise.

- [ ] Complete the [pre-filled Springer Licence-to-Publish form](https://docs.google.com/document/d/1JD0O4ZdV08ZwD7Os7CmzxDF3gm_FQFae/edit?usp=sharing). The corresponding author must match the paper and metadata sheet, have authority to sign for all authors, and provide a handwritten signature. The proceedings field must read `Trustworthy AI for Good Workshop (AI4GOOD@ICML 2026)`. Contact the organizers first for Open Choice or special copyright forms.
- [ ] Prepare one clean final source set using short filenames: all TeX, figures, required style/font files, bibliography files including `.bib` and `.bbl`, and the exactly matching final PDF. Include actual files—not links—and exclude older versions.
- [ ] Create exactly one `OpenReview_<SubmissionNumber>_<FirstAuthorLastName>.zip` containing the final PDF, complete source, signed LTP, and any applicable permissions or supplementary material. Upload it to the [AI4GOOD author-submissions folder](https://drive.google.com/drive/folders/1Pt1cvqcWZGlNgVKuyEwlLPJ_Hm3sA_oI?usp=sharing).
- [ ] Ensure the corresponding author can respond to Springer proofs within approximately 72 hours. At proof stage, only typesetting or conversion errors may be corrected—not title, content, values, or authorship.

## Website follow-up

The `website-interactive-taxonomy` branch will prototype a small GitHub Pages site inspired by [prosocial-agents](https://flecart.github.io/prosocial-agents/). It will present the paper and an interactive Figure 5 with searchable, clearly labeled human, LLM-agent, computational-agent, tutorial, and proposal evidence. The archival paper remains fixed; the website can evolve separately.

Evidence gaps are a primary output of the site. The first version should curate a small representative set of mechanisms, visibly distinguish well-supported, weakly supported, conflicting, and not-yet-curated leaves, and avoid implying complete evidence coverage. Empty leaves should help researchers see where empirical work, replication, transfer studies, or implementation examples are still missing.

Potential features:

- click a taxonomy leaf to view its definition, evidence, limitations, and open questions;
- search and filter by mechanism family, study population, evidence type, outcome, and publication year;
- visually encode evidence coverage and gaps without treating citation count as evidence quality;
- provide stable links to individual leaves and an accessible text/list view;
- store evidence as small structured records with exact DOI or public URL, supported claim, source locator, limitation, and verification date;
- let researchers propose new studies, corrections, and examples through GitHub issues or pull requests, with a contribution template and human review before merge;
- preserve contributor attribution and a public change history for additions to the evidence map;
- periodically export a dated snapshot so the evolving website can be distinguished from the frozen archival paper.
