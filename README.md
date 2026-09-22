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

## LNCS final submission

- [x] Use the official Springer LNCS proceedings template.
- [ ] Finalize the title, author names and order, affiliations, running head, and name-rendering instructions. Mark **exactly one** corresponding author and include that person's email; authorship cannot change after delivery to Springer.
- [ ] Include the required Disclosure of Interests statement. Resolve any third-party permissions and approved supplementary-material files; add figure alt text if available.
- [ ] Complete the [AI4GOOD author metadata sheet](https://docs.google.com/spreadsheets/d/1Y90xfC0UPxPT60WwL3coFsegIEaLlC78iyCaVnYzb9I/edit?usp=sharing) with the OpenReview submission number, final title, separated given/family names, affiliations, exactly one corresponding author, corresponding-author email, every author email, and every ORCID. Preserve the publication order and separate multiple entries with semicolons.
- [ ] Complete the [pre-filled Springer Licence-to-Publish form](https://docs.google.com/document/d/1JD0O4ZdV08ZwD7Os7CmzxDF3gm_FQFae/edit?usp=sharing). The corresponding author must match the paper and metadata sheet, have authority to sign for all authors, and provide a handwritten signature. The proceedings field must read `Trustworthy AI for Good Workshop (AI4GOOD@ICML 2026)`. Contact the organizers first for Open Choice or special copyright forms.
- [ ] Prepare one clean final source set using short filenames: all TeX, figures, required style/font files, bibliography files including `.bib` and `.bbl`, and the exactly matching final PDF. Include actual files—not links—and exclude older versions.
- [ ] Create exactly one `OpenReview_<SubmissionNumber>_<FirstAuthorLastName>.zip` containing the final PDF, complete source, signed LTP, and any applicable permissions or supplementary material. Upload it to the [AI4GOOD author-submissions folder](https://drive.google.com/drive/folders/1Pt1cvqcWZGlNgVKuyEwlLPJ_Hm3sA_oI?usp=sharing).
- [ ] Ensure the corresponding author can respond to Springer proofs within approximately 72 hours. At proof stage, only typesetting or conversion errors may be corrected—not title, content, values, or authorship.

## Website follow-up

The `website-interactive-taxonomy` branch will prototype a small GitHub Pages site inspired by [prosocial-agents](https://flecart.github.io/prosocial-agents/). It will present the paper and an interactive Figure 5 with searchable, clearly labeled human, LLM-agent, computational-agent, tutorial, and proposal evidence. The first version should curate a small representative set of mechanisms rather than claiming complete evidence coverage. The archival paper remains fixed; the website can evolve separately.
