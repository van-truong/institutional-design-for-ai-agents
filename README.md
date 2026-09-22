# Institutional Design for AI Agents

Springer LNCS proceedings source for *Multi-Agent AI Systems Need Institutional Design, Not Just Model-Level Alignment*, presented at the ICML 2026 Trustworthy AI4GOOD Workshop.

The active paper, bibliography, figures, and LNCS style files are in `manuscript/`. The original ICML camera-ready materials are preserved in `archive/icml2026/`.

We are preparing a lightly revised archival version for the Springer LNCS proceedings. The revision should preserve the workshop paper's argument, structure, and human voice.

Build the paper with:

```bash
make pdf
```

The build regenerates vector figures from the editable HTML files in `manuscript/figs/` and writes `springer-lncs-proceedings.pdf`. Inkscape is not required.

## Co-author review

- [ ] **Author metadata:** confirm co-first authorship for Van Truong and Xuanqiang Angelo Huang; corresponding author and email; affiliations; ORCIDs; disclosures; and contribution statement.
- [ ] **Opening examples:** review narrower wording for the cryptocurrency transfer and Citibank anecdotes. The current Citibank citation predates the appellate outcome it is used to support.
- [ ] **Flash Crash:** correct the claim that trade-cancellation rules were created only after 2010; the SEC approved cross-exchange rules in 2009.
- [ ] **Evidence claims:** verify the daycare-study interpretation, AWS smart-bed anecdote, Amazon textbook price, 1929 comparison, Ostrom community-size figures, and claims that surveys or benchmarks demonstrate deployed AI systems.
- [ ] **Scope and voice:** approve only small, source-backed corrections. Avoid restructuring the paper, adding new empirical claims, or flattening the authors' voice.
- [ ] **Conceptual bridge:** consider a short explanation connecting cooperation dilemmas, institutional functions, mechanism families, and evaluation dimensions.
- [ ] **Evaluation example:** consider sharpening one existing example with a baseline, intervention, repeated trials, and success and failure measures.
- [ ] **Figures and format:** verify Figure 5's stated counts, figure order and captions, readability, corresponding-author placement, and all LNCS submission requirements.
- [ ] **PDF blocker:** fix the citations currently printed as `(author?)`, then check for unresolved references, visible comments, clipping, and source/PDF mismatch.

## Website follow-up

The `website-interactive-taxonomy` branch will prototype a small GitHub Pages site inspired by [prosocial-agents](https://flecart.github.io/prosocial-agents/). It will present the paper and an interactive Figure 5 with searchable, clearly labeled human, LLM-agent, computational-agent, tutorial, and proposal evidence. The first version should curate a small representative set of mechanisms rather than claiming complete evidence coverage. The archival paper remains fixed; the website can evolve separately.
