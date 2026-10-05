# From Aligned Models to Governed Societies

**A Cross-Disciplinary Map of Cooperation Mechanisms and Emergent Patterns**

Van QT Truong, X. Angelo Huang, Erivan Inan, Ryan Faulkner, Joel N. Christoph, Terry JC Zhang, David Guzman Piedrahita, Zhijing Jin

ICML 2026 Workshop on Trustworthy AI for Good (AI4GOOD), Seoul · Springer LNCS proceedings (forthcoming)

**[Interactive companion website](https://van-truong.github.io/institutional-design-for-ai-agents/)** · **[Paper (PDF)](manuscript.pdf)**

---

AI agents increasingly share tools, compute, memory, and decision authority, and their interactions can produce
collective failures that evaluations of individual models do not catch. This position paper argues that AI safety
research should evaluate agent societies as governed systems: the unit of design and evaluation should be the
**model-in-institution**, not the model alone, with humans choosing which values those institutions enforce.

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
| [`manuscript/`](manuscript/) | LaTeX source (`manuscript.tex`), bibliography, LNCS style files, figure PDFs, and the scripts that generate them |
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
| `incidents.csv` | Real-world agent incidents linked to phenomenon types (being verified against primary sources) |
| `phenomena_informal.csv` | A separate, clearly labeled slice of informal reports (blog posts, public logs), shown only as an opt-in overlay on the website |
| `candidates_next_pass.csv` | Recent papers queued for the next coding pass |
| `search_log.csv`, `coding/` | Search queries and coding passes, for auditing |

The website's **mind map of related efforts** (`docs/assets/related.json`) is a separate, informal reading list of
new multi-agent studies, testbeds, programs, and policy work. It is not part of the coded corpus and does not feed
any counts. Entries are collected from a daily preprint digest and each is checked against its paper's own abstract.

## Building the paper

Requires a TeX distribution with `latexmk` (TeX Live or MacTeX).

```bash
make pdf        # builds manuscript.pdf at the repository root
```

The build uses the vector figure PDFs already in `manuscript/figures/`. Run `make figures` only to regenerate them
from their editable sources: website-drawn figures come from `docs/*.js` through `manuscript/figs/*-paper.html` and
`manuscript/scripts/gen_web_figs.py` (needs Chrome or Chromium and `pdfcrop`); the others come from the Python
generators in `manuscript/scripts/`.

Switches near the top of `manuscript.tex` control review markup. With `\showreviewflagstrue`, recent additions and
open questions are highlighted; set `\showreviewflagsfalse` for a clean PDF.

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

- [ ] Verify the incidents in `taxonomy/incidents.csv` against primary sources and record the result in the `verified` column.
- [ ] Code the papers in `taxonomy/candidates_next_pass.csv` and the remaining new instances, then rerun the build scripts.
- [ ] Consolidate the recently added citations (highlighted in the review PDF) before the camera-ready version.
- [ ] Add DOI and volume details to the citation once the proceedings are published.
- [ ] Choose and add a license for the code and data.
- [ ] Add issue templates for suggesting papers and proposing alternative classifications.

## Contact

Van QT Truong · scientistvan@gmail.com
