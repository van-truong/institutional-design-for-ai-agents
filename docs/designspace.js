/* Interactive design space of agent institutions (paper Fig. 6). Seven institutional functions, grouped into those
   that make behavior expected and visible and those that respond to it, say what an institution must do; six mechanism
   families, grouped into those that change the game and those that shape interaction over time, say how it acts on agents. Function details follow Table 1; family definitions follow
   Section 4. Hover, tap, or tab to any node to trace its branch. Palette: figs/PALETTE.md. */
(function () {
  const stage = document.getElementById("ds-stage");
  const panel = document.getElementById("ds-panel");
  if (!stage) return;

  const NS = "http://www.w3.org/2000/svg";
  const FONT = "'Helvetica Neue', Helvetica, Arial, sans-serif";
  const INK = "#3F4D5A", MUT = "#6B7787";
  const INFO = ["#5B6B7D", "#34465A", "#E9EDF2"], CONS = ["#9C4A78", "#6B2350", "#F6E7EF"];
  const VIO = ["#6C5CD0", "#463BA0", "#ECE9FB"], PLUM = CONS;
  const FAM = {
    Normative: ["#C79A3A", "#8A5A0B", "#FBEEDA"], Social: ["#C2662A", "#8F3F1E", "#FBEDE6"],
    Epistemic: ["#3A6EA5", "#2F3D6B", "#DCE8F5"], Incentive: ["#4F9070", "#2F6B4A", "#E5F0E1"],
    Constraint: ["#6C5CD0", "#463BA0", "#ECE9FB"], Restorative: ["#0F766E", "#04342C", "#E3F1EC"],
  };

  // Table 1: question it answers, human analog, LLM-agent analog
  const FUNCS = {
    "Norms & protocols": ["What behavior is expected?", "Social norms, professional rules, community guidelines", "System prompts, constitutions, shared task protocols"],
    "Monitoring": ["What behavior is observable?", "Audits, inspections, peer review", "Logs, provenance traces, tool-use records, monitor agents"],
    "Reputation": ["How does past behavior affect future trust?", "Gossip, prestige, trust networks", "Trust scores, agent reliability histories, routing preferences"],
    "Sanctions": ["What consequences follow behavior?", "Warnings, fines, rewards, exclusion, restitution", "Budget changes, tool restrictions, repair tasks, temporary removal"],
    "Constraints": ["What actions are possible?", "Quotas, access control, licensing", "Rate limits, permissions, sandboxing, context limits"],
    "Adjudication & appeal": ["Who decides what happened?", "Courts, arbitration, mediation, appeals", "Mediator agents, voting protocols, rule-based checkers, human review"],
    "Repair & reintegration": ["How is harm corrected?", "Restorative justice, apology, restitution, re-entry", "Memory cleanup, output correction, re-verification, restored privileges"],
  };
  // Section 4: what each family modifies
  const FAMS = {
    Normative: ["norms", "Says which actions are allowed, separately from which are possible or profitable."],
    Social: ["relationships", "Shapes the interaction structure: who is in the group, who interacts with whom, and whether agents can select or exclude partners."],
    Epistemic: ["information", "Changes what agents know about one another: what they can observe or verify."],
    Incentive: ["payoffs", "Modifies each agent's payoff function, reshaping the payoff consequences of action profiles."],
    Constraint: ["access", "Modifies each agent's action set, restricting or expanding the actions that are feasible."],
    Restorative: ["repair", "Shapes what happens after a deviation: whether and how agents re-enter cooperative arrangements, make restitution, or receive corrective feedback."],
  };
  const TREE = [
    { id: "fun", label: "INSTITUTIONAL FUNCTIONS", c: PLUM,
      text: "What an institution must do. Three functions make behavior expected and visible; four act on behavior once it is seen.",
      groups: [
        { id: "info", label: "Expect & observe", c: INFO, leaves: ["Norms & protocols", "Monitoring", "Reputation"],
          text: "Functions that set what behavior is expected, what is observable, and how past behavior bears on future trust." },
        { id: "cons", label: "Respond & correct", c: CONS, leaves: ["Sanctions", "Constraints", "Adjudication & appeal", "Repair & reintegration"],
          text: "Functions that set what follows behavior, what actions are possible, who decides what happened, and how harm is corrected." },
      ] },
    { id: "fam", label: "MECHANISM FAMILIES", c: VIO,
      text: "How an institution acts on agents. Three families change the game agents play (what they can do, what their choices pay, what they know); three shape how interaction unfolds over time (norms, relationships, repair).",
      groups: [
        { id: "game", label: "Change the game", c: VIO, leaves: ["Constraint", "Incentive", "Epistemic"],
          text: "The constraint, incentive, and epistemic families: what agents can do, what their choices pay, and what they know about one another." },
        { id: "time", label: "Shape interaction", c: VIO, leaves: ["Normative", "Social", "Restorative"],
          text: "The normative, social, and restorative families: which actions are allowed, who interacts with whom, and what happens after a deviation." },
      ] },
  ];

  const el = (tag, attrs = {}, parent) => {
    const n = document.createElementNS(NS, tag);
    for (const [k, v] of Object.entries(attrs)) n.setAttribute(k, v);
    if (parent) parent.appendChild(n);
    return n;
  };
  const text = (x, y, s, attrs, parent) => { const t = el("text", { x, y, ...attrs }, parent); t.textContent = s; return t; };

  const W = 1050, COLW = 234, COLGAP = 18, SECGAP = 46;
  const x0 = (W - (4 * COLW + 2 * COLGAP + SECGAP)) / 2;
  const LEFTS = [x0, x0 + COLW + COLGAP, x0 + 2 * COLW + COLGAP + SECGAP, x0 + 3 * COLW + 2 * COLGAP + SECGAP];
  const ROOT_Y = 44, BAR1 = 84, SEC_Y = 110, BAR2 = 134, GRP_Y = 150, GRP_H = 42, LEAF0 = 238, PITCH = 52, LEAF_H = 42;
  // draft variant (stage data-variant="game"): badges naming the part of the Bayesian game each family changes
  const GAME = stage.dataset.variant === "game";
  const BADGE = { Constraint: ["A\u1d62", true], Epistemic: ["info. about \u0398", true, 11], Incentive: ["u\u1d62", true],
    Normative: ["deontic", false], Social: ["N, links", false], Restorative: ["ex post", false] };
  const H = LEAF0 + 3 * PITCH + LEAF_H / 2 + 16;  // the badge key lives in the paper's caption

  const svg = el("svg", { viewBox: `0 0 ${W} ${H}`, xmlns: "http://www.w3.org/2000/svg", role: "img", class: "ds-svg", "font-family": FONT,
    "aria-labelledby": "ds-title ds-desc" }, stage);
  el("title", { id: "ds-title" }, svg).textContent = "Design space of agent institutions";
  el("desc", { id: "ds-desc" }, svg).textContent =
    "A tree with the agent institution at the top. It branches into seven institutional functions, three that make behavior expected and visible and four that respond to it, " +
    "and six mechanism families, three that change the game agents play and three that shape interaction over time.";
  const defs = el("defs", {}, svg);
  const sh = el("filter", { id: "ds-shadow", x: "-10%", y: "-30%", width: "120%", height: "170%" }, defs);
  el("feDropShadow", { dx: 0, dy: 3, stdDeviation: 4, "flood-color": INK, "flood-opacity": 0.14 }, sh);
  const grad = (id, c) => {
    const g = el("linearGradient", { id, x1: 0, y1: 0, x2: 0, y2: 1 }, defs);
    el("stop", { offset: 0, "stop-color": "#ffffff" }, g);
    el("stop", { offset: 1, "stop-color": c }, g);
    return `url(#${id})`;
  };

  // node registry: id -> {parent, kind, info}
  const NODES = { root: { parent: null, kind: "root" } };
  const parts = []; // [element, nodeId]
  const lines = el("g", { class: "ds-lines" }, svg);
  const line = (x1, y1, x2, y2, col, node) => {
    const l = el("path", { d: `M ${x1} ${y1} L ${x2} ${y2}`, fill: "none", stroke: col, "stroke-width": 1.8, "stroke-linecap": "round", opacity: 0.75 }, lines);
    parts.push([l, node]);
  };
  const hitG = (id) => {
    const g = el("g", { class: "ds-node", tabindex: "0" }, svg);
    g.dataset.node = id;
    parts.push([g, id]);
    return g;
  };

  // root
  const rcx = W / 2;
  const rg = hitG("root");
  el("rect", { x: rcx - 110, y: ROOT_Y - 24, width: 220, height: 48, rx: 24, fill: grad("ds-g-root", "#EEF2F6"), stroke: INK, "stroke-width": 1.6, filter: "url(#ds-shadow)" }, rg);
  text(rcx, ROOT_Y + 7, "Agent institution", { "text-anchor": "middle", "font-size": 20, "font-weight": 700, fill: INK }, rg);
  NODES.root.info = { c: [INK, INK], label: "Root", title: "Agent institution",
    text: "The rules, roles, and procedures for enforcement and repair that structure interaction among agents. Its functions say what it must do; its mechanism families say how it acts on agents." };

  const secCx = [(LEFTS[0] + LEFTS[1] + COLW) / 2, (LEFTS[2] + LEFTS[3] + COLW) / 2];
  line(rcx, ROOT_Y + 24, rcx, BAR1, INK, "root");
  line(secCx[0], BAR1, secCx[1], BAR1, INK, "root");
  TREE.forEach((sec, si) => {
    const scx = secCx[si];
    NODES[sec.id] = { parent: "root", kind: "section", info: { c: sec.c, label: "Branch", title: sec.label[0] + sec.label.slice(1).toLowerCase(), text: sec.text } };
    line(scx, BAR1, scx, SEC_Y - 16, sec.c[0], sec.id);
    const sg = hitG(sec.id);
    const sw = sec.label.length * 11.5 + 30;
    el("rect", { x: scx - sw / 2, y: SEC_Y - 17, width: sw, height: 30, rx: 15, fill: "#fff", stroke: sec.c[0], "stroke-width": 1.4 }, sg);
    text(scx, SEC_Y + 4, sec.label, { "text-anchor": "middle", "font-size": 15, "font-weight": 700, "letter-spacing": "0.08em", fill: sec.c[1] }, sg);
    const lefts = LEFTS.slice(si * 2, si * 2 + 2);
    const gcx = lefts.map((l) => l + COLW / 2);
    line(scx, SEC_Y + 13, scx, BAR2, sec.c[0], sec.id);
    sec.groups.forEach((grp, gi) => {
      const left = lefts[gi], cx = gcx[gi], c = grp.c;
      NODES[grp.id] = { parent: sec.id, kind: "group", info: { c, label: sec.label.toLowerCase().replace(/^./, (m) => m.toUpperCase()), title: grp.label, text: grp.text } };
      line(scx, BAR2, cx, BAR2, sec.c[0], grp.id);
      line(cx, BAR2, cx, GRP_Y, c[0], grp.id);
      const gg = hitG(grp.id);
      el("rect", { x: left, y: GRP_Y, width: COLW, height: GRP_H, rx: 12, fill: grad(`ds-g-${grp.id}`, c[2]), stroke: c[0], "stroke-width": 1.6, filter: "url(#ds-shadow)" }, gg);
      text(cx, GRP_Y + GRP_H / 2 + 6, grp.label, { "text-anchor": "middle", "font-size": 18, "font-weight": 700, fill: c[1] }, gg);
      const sx = left + 16;
      const lys = grp.leaves.map((_, i) => LEAF0 + i * PITCH);
      line(sx, GRP_Y + GRP_H, sx, lys[lys.length - 1], c[0], grp.id);
      grp.leaves.forEach((name, li) => {
        const id = `${grp.id}-${li}`, ly = lys[li];
        const fam = FAMS[name], fun = FUNCS[name];
        const lc = fam ? FAM[name] : c;
        NODES[id] = { parent: grp.id, kind: "leaf", info: fam
          ? { c: lc, label: `Mechanism family · ${fam[0]}`, title: name, text: fam[1] }
          : { c: lc, label: grp.label, title: name, q: fun[0], human: fun[1], llm: fun[2] } };
        line(sx, ly, left + 32, ly, lc[0], id);
        const lg = hitG(id);
        const lx = left + 32, lw = COLW - 32;
        el("rect", { x: lx, y: ly - LEAF_H / 2, width: lw, height: LEAF_H, rx: 12, fill: lc[2], stroke: lc[0], "stroke-width": 1.3 }, lg);
        if (fam && GAME) {
          const [sym, inGame, bfs] = BADGE[name], bw = bfs ? Math.round(sym.length * bfs * 0.6 + 20) : Math.max(40, sym.length * (inGame ? 8 : 7) + 18), bx = lx + lw - bw - 6;
          const tx = lx + (lw - bw - 6) / 2;
          text(tx, ly - 2, name, { "text-anchor": "middle", "font-size": 15.5, "font-weight": 700, fill: lc[1] }, lg);
          text(tx, ly + 14, fam[0], { "text-anchor": "middle", "font-size": 13, "font-style": "italic", fill: MUT }, lg);
          el("rect", { x: bx, y: ly - 12, width: bw, height: 24, rx: 12, fill: "#fff", stroke: lc[0], "stroke-width": 1.3,
            ...(inGame ? {} : { "stroke-dasharray": "4 3" }) }, lg);
          text(bx + bw / 2, ly + 5, sym, { "text-anchor": "middle", "font-size": bfs || (inGame ? 15 : 12), "font-style": "italic",
            "font-family": inGame ? "'Times New Roman', Times, serif" : FONT, "font-weight": inGame ? 400 : 600, fill: lc[1] }, lg);
        } else if (fam) {
          text(lx + lw / 2, ly - 2, name, { "text-anchor": "middle", "font-size": 16, "font-weight": 700, fill: lc[1] }, lg);
          text(lx + lw / 2, ly + 14, fam[0], { "text-anchor": "middle", "font-size": 13.5, "font-style": "italic", fill: MUT }, lg);
        } else {
          text(lx + lw / 2, ly + 5.5, name, { "text-anchor": "middle", "font-size": 15, "font-weight": 700, fill: lc[1] }, lg);
        }
      });
    });
  });
  // ---------- interaction ----------
  const lineage = (id) => {
    const set = new Set([id]);
    for (let p = NODES[id].parent; p; p = NODES[p].parent) set.add(p);
    const down = (n) => Object.keys(NODES).forEach((k) => { if (NODES[k].parent === n) { set.add(k); down(k); } });
    if (NODES[id].kind !== "root") down(id);
    else Object.keys(NODES).forEach((k) => set.add(k));
    return set;
  };
  let locked = null;
  const describe = (id) => {
    if (!panel) return;
    const n = id && NODES[id];
    if (!n) {
      panel.style.removeProperty("--c");
      panel.innerHTML = `<p class="fx-plabel">Explore</p><h3>Design space of agent institutions</h3>` +
        `<p>Hover, tap, or tab to any box to trace its branch. Functions show Table 1's question and analogs; families show what they change.</p>`;
      return;
    }
    const i = n.info;
    panel.style.setProperty("--c", i.c[0]);
    let body = i.q
      ? `<p class="fx-q">${i.q}</p><dl class="fx-dl"><dt>Human analog</dt><dd>${i.human}</dd><dt>LLM-agent analog</dt><dd>${i.llm}</dd></dl>`
      : `<p>${i.text}</p>`;
    panel.innerHTML = `<p class="fx-plabel">${i.label}</p><h3>${i.title}</h3>${body}`;
  };
  const activate = (id) => {
    const on = id ? lineage(id) : null;
    svg.classList.toggle("has-active", !!id);
    parts.forEach(([e, n]) => e.classList.toggle("is-on", !!on && on.has(n)));
    parts.forEach(([e, n]) => e.classList.toggle("is-focus", n === id));
    describe(id);
  };
  svg.querySelectorAll(".ds-node").forEach((g) => {
    const id = g.dataset.node;
    g.addEventListener("pointerenter", () => activate(id));
    g.addEventListener("pointerleave", () => activate(locked));
    g.addEventListener("focus", () => activate(id));
    g.addEventListener("blur", () => activate(locked));
    g.addEventListener("click", (e) => { e.stopPropagation(); locked = locked === id ? null : id; activate(locked); });
    g.addEventListener("keydown", (e) => {
      if (e.key === "Enter" || e.key === " ") { e.preventDefault(); locked = locked === id ? null : id; activate(locked); }
    });
  });
  svg.addEventListener("click", () => { locked = null; activate(null); });
  describe(null);

  if ("IntersectionObserver" in window) {
    const io = new IntersectionObserver((es) => {
      if (es.some((e) => e.isIntersecting)) { stage.classList.add("fx-in"); io.disconnect(); }
    }, { threshold: 0.25 });
    io.observe(stage);
  } else stage.classList.add("fx-in");
})();
