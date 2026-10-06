# From Aligned Models to Governed Societies

**A Cross-Disciplinary Map of Cooperation Mechanisms and Emergent Patterns**

Van QT Truong, X. Angelo Huang, Erivan Inan, Ryan Faulkner, Joel N. Christoph, Terry JC Zhang, David Guzman Piedrahita, Zhijing Jin

ICML 2026 Workshop on Trustworthy AI for Good (AI4GOOD), Seoul · Springer LNCS proceedings (forthcoming)

**[Interactive companion website](https://van-truong.github.io/institutional-design-for-ai-agents/)** · **[Paper (PDF)](manuscript/manuscript.pdf)**

---

AI agents increasingly share tools, compute, memory, and decision authority, and their interactions can produce
collective failures that evaluations of individual models do not catch. This position paper argues that AI safety
research should evaluate agent societies as governed systems. Models should be designed and evaluated together with
the institutions that govern their interactions, the **model-in-institution**, with humans choosing which values
those institutions enforce.

To ground the argument, we map how human and artificial groups have sustained cooperation:

- **A taxonomy of over 60 cooperation-shaping mechanisms**, thematically coded from hundreds of documented instances
  across AI research and nearly twenty other fields, from economics and law to evolutionary biology, platform
  governance, security, and blockchain design.
- **A map of group-level patterns already emerging among agents**, from shared conventions to collusion, linked to
  recent real-world incidents.
- **An evaluation agenda** that borrows from social-ecological systems research and experimental economics to treat
  the institution itself as a variable.

The paper is fixed once published; the website and the data in this repository keep growing.

## What's here

| Folder | Contents |
|---|---|
| [`manuscript/`](manuscript/) | The paper: LaTeX source (`manuscript.tex`, the version submitted to the proceedings), the built PDF (`manuscript.pdf`), bibliography, LNCS style files, figure PDFs, and the scripts and pages that generate the figures |
| [`docs/`](docs/) | The companion website (plain HTML, CSS, and JavaScript, served by GitHub Pages) |
| [`taxonomy/`](taxonomy/) | The coded dataset behind both maps, the coding protocol, and the scripts that build the website data |
| [`archive/icml2026/`](archive/icml2026/) | The original ICML workshop camera-ready paper and poster materials |

### The data

The taxonomy is the single source of truth for the paper's taxonomy figures and the website. See
[`taxonomy/PROTOCOL.md`](taxonomy/PROTOCOL.md) for how sources were searched and coded.

| File | What it holds |
|---|---|
| `instances.csv` | One row per documented use of a mechanism, or report of a group-level pattern, in one source |
| `mechanisms.csv`, `codebook.csv` | Mechanisms, themes, and families, with definitions |
| `papers.csv` | The coded sources |
| `configurations.csv` | Named combinations of mechanisms, such as Ostrom's design principles |
| `coding/PHENOMENA_CODEBOOK.md`, `coding/phenomena_tags.csv` | The ten phenomenon types (definitions, assignment rules, boundary cases) and each phenomenon instance's type and effect |
| `incidents.csv` | Real-world agent incidents linked to phenomenon types (each checked against its primary sources) |
| `phenomena_informal.csv` | A separate, clearly labeled slice of informal reports (blog posts, public logs), shown only as an opt-in overlay on the website |
| `candidates_next_pass.csv` | Recent papers queued for the next coding pass |
| `search_log.csv`, `coding/` | Search queries and coding passes, for auditing |

The website's **mind map of related efforts** (`docs/assets/related.json`) is a separate, informal reading list of
new multi-agent studies, testbeds, programs, and policy work. It is not part of the coded corpus and does not feed
any counts. Entries are collected from a daily preprint digest and each is checked against its paper's own abstract.

## Building the paper

Requires a TeX distribution with `latexmk` (TeX Live or MacTeX).

```bash
make pdf        # builds manuscript/manuscript.pdf
```

The build uses the vector figure PDFs already in `manuscript/figures/`, so you only need to regenerate figures after
changing their sources. Most figures are drawn by the website's own scripts, so the paper and the site share one
drawing:

```bash
cd manuscript
python3 scripts/gen_web_figs.py                 # Figs. 1-6, 8, 10 from docs/*.js (needs Chrome or Chromium, pdfcrop)
python3 scripts/gen_taxonomy.py && python3 scripts/gen_dimensions.py
./render_figures.sh                             # Figs. 7 and 9 from manuscript/figs/*.html (needs rsvg-convert, pdfcrop)
```

The taxonomy and phenomena figures read the coded data, so rerun the build scripts in `taxonomy/scripts/` first
when the data change.

## Viewing the website locally

```bash
cd docs && python3 -m http.server 8000   # then open http://localhost:8000
```

## Contributing

Corrections, missing mechanisms, alternative classifications, and suggested papers are welcome: please
[open an issue](https://github.com/van-truong/institutional-design-for-ai-agents/issues). Because thematic coding is
interpretive, we especially welcome readers who would draw the taxonomy's boundaries differently.

## Citation

```bibtex
@inproceedings{truong2026governed,
  title     = {From Aligned Models to Governed Societies: A Cross-Disciplinary Map of Cooperation Mechanisms and Emergent Patterns},
  author    = {Truong, Van QT and Huang, X. Angelo and Inan, Erivan and Faulkner, Ryan and Christoph, Joel N. and Zhang, Terry JC and Guzman Piedrahita, David and Jin, Zhijing},
  booktitle = {ICML 2026 Workshop on Trustworthy AI for Good (AI4GOOD)},
  series    = {Lecture Notes in Computer Science},
  publisher = {Springer},
  year      = {2026},
  note      = {Originally titled ``Multi-Agent AI Systems Need Institutional Design, Not Just Model-Level Alignment''},
}
```

## Acknowledgments

The website was inspired by Angelo Huang's [Prosocial Agents paper website](https://flecart.github.io/prosocial-agents/).
Full acknowledgments are in the paper.

## Open items

- [ ] Settle the remaining disagreements from the second coding pass of the newest instances, then rerun the build scripts.
- [ ] Code the papers in `taxonomy/candidates_next_pass.csv`.
- [ ] Add DOI and volume details to the citation once the proceedings are published.
- [ ] Add issue templates for suggesting papers and proposing alternative classifications.

## License

- **Code** (the website in `docs/`, and the scripts in `manuscript/scripts/` and `taxonomy/scripts/`): [MIT](LICENSE).
- **Data and figures** (everything in `taxonomy/`, `docs/assets/*.json`, and the figure files in `manuscript/figs/` and `manuscript/figures/`): [CC BY 4.0](LICENSE-CC-BY-4.0). Please cite the paper when you reuse them.
- **Not covered by either license:** the paper's text and PDF (`manuscript/manuscript.tex`, `manuscript/manuscript.pdf`, and `archive/icml2026/`), whose reuse is governed by the publisher's terms; the Springer LNCS style files (`llncs.cls`, `splncs04.bst`), which keep their own license; and the author photographs in `docs/assets/`.

## Contact

Van QT Truong · scientistvan@gmail.com
