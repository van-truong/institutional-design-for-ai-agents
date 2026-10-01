# Informal-reports and automated-systems slice (draft, 2026-10-01)

A supplementary slice of group-level phenomena from sources the main search did not cover: informal reports
(blogs, project pages, interviews, reconstructions) about multi-agent LLM systems, and automated or simulated
agents outside AI research (pricing and trading bots, encyclopedia bots, distributed services, agent-based models,
artificial life, swarm robots). Data: `taxonomy/phenomena_informal.csv` (39 instances, IDs `IX001`–`IX039`).
Nothing here is merged into `instances.csv`, `phenomena_tags.csv`, or the paper's counts.

## Why a separate tier

The main corpus codes peer-reviewed papers and preprints. Most informal reports are first-person write-ups of
uncontrolled runs, so they carry a lower evidence weight. Each row has an `evidence_tier`:

- `informal`: blog posts, project pages, interviews, and reconstructions (24 rows)
- `peer_reviewed`: the papers in the non-LLM part of the slice (15 rows)

Keep the tiers apart in any count or figure.

## Inclusion and exclusion

Included only when all four hold:

1. The pattern is group-level: it arises from interaction among two or more agents.
2. It is emergent rather than designed: nobody wrote it into the agents or the rules.
3. It is documented in a source fetched on 2026-10-01, or in an authoritative abstract page.
4. It is not already coded in the main corpus.

Two partial exceptions:

- **Already in the corpus as mechanisms:** Anthropic's multi-agent research system (`I0203`) and Project Vend
  phase two (`I0204`) are coded there as mechanisms. The phenomena they report are recorded here, cross-referenced.
- **Designed task, emergent outcome:** where an experiment assigned the roles (the AI Village saboteur game), only
  the outcome that went beyond the design is recorded, here the false-accusation cascade.

Excluded:

- Moltbook, Project Sid, Generative Agents, Schelling, and the Chirper.ai studies (Hashemi and Macy; Coppolillo
  et al.; Zhu et al.), which are already in the corpus.
- Ferrara et al., "The Rise of Social Bots" (CACM 2016). The bots are designed to manipulate, so the pattern is
  not emergent.
- Shaffer Shane et al., "Scheming in the wild" (arXiv 2604.09104). It reports single-agent incidents only.
- AI Village, "Gemini 2.5 Pro … Compounding Misalignment" (2026-08-20). It describes one agent's drift, and the
  multi-agent mechanism appears only in a reader comment.

## Searches (2026-10-01)

Web search, then fetched each primary page where possible:

- **LLM agents, informal:**
  - "AI Village AI Digest agents blog emergent behavior", then the AI Village blog archive and six of its posts
  - "Anthropic How we built our multi-agent research system …"
  - "Cognition Don't Build Multi-Agents …"
  - "Project Vend phase two …"
  - "Claude Opus 4 system card spiritual bliss attractor …"
  - "Infinite Backrooms Andy Ayrey …"
  - "Andy Ayrey When AIs Play God(se) LLMtheism"
  - "Janus repligate act i Discord …"
  - "Chirper.ai AI-only social network study …" (all results already in the corpus)
- **Automated systems in the wild:**
  - "Tsvetkova Even good bots fight …"
  - "Geiger Halfaker 2017 Operationalizing conflict …"
  - "Calvano … Algorithmic Pricing, and Collusion"
  - "Assad Clark Ershov Xu … German Retail Gasoline Market"
  - "Michael Eisen … book about flies"
  - "Kirilenko … The Flash Crash"
  - "Metastable Failures in Distributed Systems HotOS 2021"
  - "Metastable Failures in the Wild OSDI 2022"
  - "Ferrara … The rise of social bots"
- **Agent-based modeling, artificial life and robots:**
  - "Epstein Axtell Growing Artificial Societies Sugarscape …"
  - "Axelrod 1997 The Dissemination of Culture …"
  - "W. Brian Arthur 1994 … El Farol"
  - "Challet Zhang 1997 … minority game"
  - "Arthur Holland LeBaron Palmer Tayler … artificial stock market"
  - "Thomas Ray Tierra …"
  - "Ferrante … Evolution of Self-Organized Task Specialization in Robot Swarms"

## Counts

| Facet | Counts |
|---|---|
| Substrate | llm 23 · bots in the wild 5 · agent-based models 5 · distributed systems 2 · artificial life 2 · rl (pricing) 1 · robots 1 |
| Valence | harmful 20 · neutral 13 · beneficial 6 |
| Existing types | culture 6 · conformity & bias 5 · collective intelligence 4 · collusion & deception 4 · social structure 3 · cooperation 3 · economy 3 · emergent harm 3 · conventions 1 |
| Proposed types | inter-agent conflict 3 · conversational attractor 3 · collective identity 1 |

## Proposed new phenomenon types

- **Conversational attractor.** Agent-to-agent dialogue converging on a self-reinforcing theme with no outside
  input. Examples are the "spiritual bliss" state between two Claude instances, the Project Vend agents'
  all-night "eternal transcendence" exchanges, and the Infinite Backrooms. Nothing in the current ten types
  covers it. It is also the closest informal analogue to "conformity & collective bias" for open-ended talk.
- **Inter-agent conflict.** Persistent mutual undoing or antagonism between agents built to help, such as the
  Wikipedia bot "fights" and the AI Village journalists' rival headlines. It could fold into "emergent harm",
  but the Geiger and Halfaker replication shows the same traces can be routine collaboration. A separate type
  keeps that dispute visible.
- **Collective identity.** Same-model agents identifying as one agent (Act I, self-reported). This is relevant
  to collusion among copies of one model. With one source it may be better folded into "culture" until more
  evidence appears.

## What this suggests for the paper (no edits made)

- **Conformity is the most common informal failure.** Sycophantic agreement, weak-link doubt, and cascading
  consensus around a false theory show up repeatedly in the AI Village. This supports the paper's "Conformity &
  collective bias" row, which currently has only four instances.
- **Collusion now has field evidence outside LLMs.** Q-learning tacit collusion (Calvano et al.) and the German
  gasoline-market evidence (Assad et al.) are field- and simulation-grade examples. They could bridge to the
  Amazon and Flash Crash anecdotes in the paper's introduction, both of which are cited but not coded.
- **Human-behavior baselines exist.** The agent-based models (Sugarscape, Axelrod, El Farol, the minority game,
  the Santa Fe market) partly fill the empty human column of the phenomena figure.
- **Mind the evidence tier.** Many informal rows rest on one post. Several come from the AI Village team
  writing about their own runs, and Act I is self-reported on a funding page.

## Caveats to check before citing

- **Spiritual bliss:** the row cites the Asterisk interview; read the figures in the Claude Opus 4 system card
  (May 2025), which was not fetched.
- **Tierra:** the date is not printed on the fetched PDF (a Santa Fe Institute working paper); confirm it.
- **Amazon book prices:** the pricing ratios come from The Register's report of Michael Eisen's post; the
  original post could not be fetched.
- **Metastable failures in the wild:** "retries are the main sustaining effect" comes from the search abstract,
  not the fetched page.
