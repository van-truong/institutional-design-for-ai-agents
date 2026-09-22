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

## Co-author review

- [ ] **Author metadata:** confirm co-first authorship for Van Truong and Xuanqiang Angelo Huang; corresponding author and email; affiliations; ORCIDs; disclosures; and contribution statement.
- [ ] **Opening examples:** review narrower wording for the cryptocurrency transfer and Citibank anecdotes. The current Citibank citation predates the appellate outcome it is used to support.
- [ ] **Flash Crash:** correct the claim that trade-cancellation rules were created only after 2010; the SEC approved cross-exchange rules in 2009.
- [ ] **Evidence claims:** verify the daycare-study interpretation, AWS smart-bed anecdote, Amazon textbook price, 1929 comparison, Ostrom community-size figures, claims that surveys or benchmarks demonstrate deployed AI systems, and categorical claims about current agents' institutional capacities.
- [ ] **Scope and voice:** approve only small, source-backed corrections. Avoid restructuring the paper, adding new empirical claims, or flattening the authors' voice.
- [ ] **Conceptual bridge:** consider a short explanation connecting cooperation dilemmas, institutional functions, mechanism families, and evaluation dimensions.
- [ ] **Evaluation example:** consider sharpening one existing example with a baseline, intervention, repeated trials, and success and failure measures.
- [ ] **Figures and format:** verify Figure 5's stated counts, figure order and captions, readability, corresponding-author placement, and all LNCS submission requirements.
- [x] **Citation rendering:** replace incompatible author-bearing citations; the review PDF no longer contains `(author?)`.
- [ ] **Final PDF check:** turn off review colors, resolve remaining bibliography metadata warnings, and check for unresolved references, visible comments, clipping, and source/PDF mismatch.

## LNCS final submission (Van will submit after co-authors verify their info)

- [x] Use the official Springer LNCS proceedings template.
- [ ] Finalize the title, author names and order, affiliations, running head, and name-rendering instructions. Mark **exactly one** corresponding author and include that person's email; authorship cannot change after delivery to Springer.
- [ ] Include the required Disclosure of Interests statement. Resolve any third-party permissions and approved supplementary-material files; add figure alt text if available.
- [ ] Complete the [AI4GOOD author metadata sheet](https://docs.google.com/spreadsheets/d/1Y90xfC0UPxPT60WwL3coFsegIEaLlC78iyCaVnYzb9I/edit?usp=sharing) with the OpenReview submission number, final title, separated given/family names, affiliations, exactly one corresponding author, corresponding-author email, every author email, and every ORCID. Preserve the publication order and separate multiple entries with semicolons.

Draft spreadsheet values to verify:

- **Title:** `Multi-Agent AI Systems Need Institutional Design, Not Just Model-Level Alignment`
- **Given names:** `Van QT; Xuanqiang Angelo; Erivan; Ryan; Joël Naoki; Terry Jingchen; David; Zhijing`
- **Family names:** `Truong; Huang; Inan; Faulkner; Christoph; Zhang; Guzman Piedrahita; Jin` — confirm that `Guzman Piedrahita` is indexed as one compound family name.
- **Affiliation mapping:** Truong (1, 2, 3); Huang (2, 3, 4, 5); Inan (2, 3); Faulkner (2, 3); Christoph (6); Zhang (2, 3); Guzman Piedrahita (2, 3, 4); Jin (2, 3, 7). Confirm the seven numbered affiliations against the paper before transcribing them.
- **Affiliations:** 1—University of Pennsylvania, Philadelphia, PA, USA; 2—Jinesis Lab, University of Toronto and Vector Institute, Toronto, Canada; 3—EuroSafeAI; 4—ETH Zürich, Zürich, Switzerland; 5—Institute for Decentralized AI, Oxford, UK; 6—Harvard Kennedy School, Cambridge, MA, USA; 7—Max Planck Institute for Intelligent Systems, Tübingen, Germany.
- **Still needed from authors:** OpenReview number; explicit choice of one corresponding author; all author emails; all ORCIDs; optional indexing notes; and confirmation of supplementary material and third-party permissions. The paper currently contains only `scientistvan@gmail.com` and does not explicitly mark correspondence.
- **Current status fields:** source format is `LaTeX`; Disclosure of Interests and signed LTP are not yet complete; final authorship/order and final PDF/source match remain pending.
- Leave `Organizer: Part / Topical Section`, `Organizer: Starting Page / Sequence No.`, and `Organizer: Paper Number in Submission Folder` blank for the organizers unless instructed otherwise.

- [ ] Complete the [pre-filled Springer Licence-to-Publish form](https://docs.google.com/document/d/1JD0O4ZdV08ZwD7Os7CmzxDF3gm_FQFae/edit?usp=sharing). The corresponding author must match the paper and metadata sheet, have authority to sign for all authors, and provide a handwritten signature. The proceedings field must read `Trustworthy AI for Good Workshop (AI4GOOD@ICML 2026)`. Contact the organizers first for Open Choice or special copyright forms.
- [ ] Prepare one clean final source set using short filenames: all TeX, figures, required style/font files, bibliography files including `.bib` and `.bbl`, and the exactly matching final PDF. Include actual files—not links—and exclude older versions.
- [ ] Create exactly one `OpenReview_<SubmissionNumber>_<FirstAuthorLastName>.zip` containing the final PDF, complete source, signed LTP, and any applicable permissions or supplementary material. Upload it to the [AI4GOOD author-submissions folder](https://drive.google.com/drive/folders/1Pt1cvqcWZGlNgVKuyEwlLPJ_Hm3sA_oI?usp=sharing).
- [ ] Ensure the corresponding author can respond to Springer proofs within approximately 72 hours. At proof stage, only typesetting or conversion errors may be corrected—not title, content, values, or authorship.

## Website follow-up

The `website-interactive-taxonomy` branch will prototype a small GitHub Pages site inspired by [prosocial-agents](https://flecart.github.io/prosocial-agents/). It will present the paper and an interactive Figure 5 with searchable, clearly labeled human, LLM-agent, computational-agent, tutorial, and proposal evidence. The first version should curate a small representative set of mechanisms rather than claiming complete evidence coverage. The archival paper remains fixed; the website can evolve separately.
