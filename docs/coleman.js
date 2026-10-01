/* Interactive Coleman boat for agent institutions (paper Fig. 9), after Coleman (1990) and the question-per-arrow
   form of Martinez-Pena and Ylikoski (2024). An institutional change (A) reaches each agent's action situation (B)
   through Ostrom's seven rule types; the model responds (C) and reshapes other agents' situations; behavior adds up
   to group outcomes (D). Hover or tab to any part, press Play to walk the arrows, or show where institutions fail. */
(function () {
  const stage = document.getElementById("boat-stage");
  const panel = document.getElementById("boat-panel");
  const playBtn = document.getElementById("boat-play");
  const failBtn = document.getElementById("boat-fail");
  if (!stage) return;

  const NS = "http://www.w3.org/2000/svg";
  const FONT = "'Helvetica Neue', Helvetica, Arial, sans-serif";
  const INK = "#3F4D5A", MUT = "#6B7787", HAIR = "#B3BEC9";
  const C = {
    amber: ["#C79A3A", "#8A5A0B", "#FBEEDA"], green: ["#4F9070", "#2F6B4A", "#E5F0E1"],
    blue: ["#3A6EA5", "#2F3D6B", "#DCE8F5"], violet: ["#6C5CD0", "#463BA0", "#ECE9FB"],
    terra: ["#C2662A", "#8F3F1E", "#FBEDE6"], slate: ["#6B7787", "#3F4D5A", "#EEF2F6"],
  };

  const INFO = {
    A: { c: C.amber, label: "Macro · designed", title: "A. Institutional change",
      text: "Designers change the rules: for example, they add graduated sanctions or an appeal step. Designers, and the agents subject to the rules, can be human, artificial, or mixed." },
    B: { c: C.blue, label: "Micro · each agent", title: "B. Each agent's action situation",
      text: "The change reaches each agent through its action situation: what it may do, what it knows, and what each choice costs. Ostrom's seven rule types are a checklist of what an institutional change can alter." },
    C: { c: C.violet, label: "Micro · each agent", title: "C. Agent behavior",
      text: "What each model actually does with its new options. This is where model-level evaluation usually looks, and it is only one step of four." },
    D: { c: C.green, label: "Macro · emergent", title: "D. Group outcomes",
      text: "Behavior adds up to outcomes for the group: cooperation, but also enforcement cost, false punishment, and whether harm gets repaired." },
    hope: { c: C.slate, label: "The shortcut", title: "What designers hope happens",
      text: "The dashed arrow is the assumption that a rule change produces the intended group outcome directly. The boat makes us trace the micro steps that the assumption skips." },
    a1: { c: C.slate, label: "Arrow 1 · macro to micro", title: "How does the rule change each agent's situation?",
      text: "A rule only matters through what it changes for each agent: who may act, which actions are allowed, what is observed, and what each action costs." },
    a2: { c: C.slate, label: "Arrow 2 · micro", title: "How does the model respond?",
      text: "Given its new situation, what does the model do? Human responses to the same rule may be a poor guide, because agents optimize differently." },
    a3: { c: C.slate, label: "Arrow 3 · micro to micro", title: "How do agents reshape each other's situations?",
      text: "Each agent's behavior becomes part of every other agent's situation: a defection, a sanction, or a shared-memory write changes what the others face next." },
    a4: { c: C.slate, label: "Arrow 4 · micro to macro", title: "How does behavior add up to group outcomes?",
      text: "Many individual choices aggregate into group outcomes, often nonlinearly. This is the step that model-level evaluation cannot see." },
    fA: { c: C.terra, label: "Failure mode A · arrow 2", title: "A fine read as a price",
      text: "A sanction can reframe the interaction. In the Haifa daycare study, a small late-pickup fine increased lateness: an obligation became a priced service. An agent optimizing against a budgeted penalty may treat it the same way." },
    fB: { c: C.terra, label: "Failure mode B · arrow 4", title: "The score stops tracking conduct",
      text: "Any mechanism that produces a measurable signal creates a target. Reputation scores can be farmed, inflated, or gamed until they no longer track the behavior they were meant to reward." },
    fC: { c: C.terra, label: "Failure mode C · feedback", title: "The enforcer reshapes the rules",
      text: "Monitors, mediators, and sanctioning roles are authority positions with incentives of their own. When agents occupy them, the institution can be captured and the rules rewritten from inside." },
    sub: { c: C.slate, label: "Substrate", title: "The technical substrate",
      text: "Unlike human societies, the micro level runs on infrastructure designers control: shared memory, compute, tools, and logs. That is both a lever and a new place for failure." },
  };
  const RULES = {
    boundary: "who can enter or leave a position", position: "which positions exist",
    choice: "which actions each position may take", information: "what each position can know",
    aggregation: "how individual choices become a decision", payoff: "how benefits and costs are assigned",
    scope: "which outcomes may be affected",
  };

  const el = (tag, attrs = {}, parent) => {
    const n = document.createElementNS(NS, tag);
    for (const [k, v] of Object.entries(attrs)) n.setAttribute(k, v);
    if (parent) parent.appendChild(n);
    return n;
  };
  const text = (x, y, s, attrs, parent) => { const t = el("text", { x, y, ...attrs }, parent); t.textContent = s; return t; };

  const svg = el("svg", { viewBox: "0 -10 1000 690", role: "img", class: "bt-svg", "font-family": FONT,
    "aria-labelledby": "bt-title bt-desc" }, stage);
  el("title", { id: "bt-title" }, svg).textContent = "A Coleman boat for agent institutions";
  el("desc", { id: "bt-desc" }, svg).textContent =
    "An institutional change at the group level reaches each agent's action situation, shapes agent behavior, and adds up to group outcomes. Four numbered questions label the arrows, and three failure modes mark where an institution can break.";
  const defs = el("defs", {}, svg);
  const shadow = el("filter", { id: "bt-shadow", x: "-10%", y: "-20%", width: "120%", height: "150%" }, defs);
  el("feDropShadow", { dx: 0, dy: 4, stdDeviation: 6, "flood-color": INK, "flood-opacity": 0.14 }, shadow);
  [["bt-ar", INK], ["bt-ar-mut", MUT], ["bt-ar-terra", C.terra[0]]].forEach(([id, col]) => {
    const m = el("marker", { id, viewBox: "0 0 10 10", refX: 8, refY: 5, markerWidth: 7, markerHeight: 7, orient: "auto-start-reverse" }, defs);
    el("path", { d: "M 0 0 L 10 5 L 0 10 z", fill: col }, m);
  });

  // levels
  el("rect", { x: 10, y: 40, width: 980, height: 180, rx: 22, fill: "#FAF6EE" }, svg);
  el("rect", { x: 10, y: 286, width: 980, height: 360, rx: 22, fill: "#F3F6F9" }, svg);
  text(30, 210, "GROUP AND INSTITUTION · MACRO", { "font-size": 14, "font-weight": 800, "letter-spacing": "0.12em", fill: MUT }, svg);
  text(30, 670, "EACH AGENT · MICRO", { "font-size": 14, "font-weight": 800, "letter-spacing": "0.12em", fill: MUT }, svg);

  const hits = [];
  const hit = (g, key) => { g.setAttribute("tabindex", "0"); g.dataset.key = key; g.classList.add("bt-hit"); hits.push(g); return g; };

  // arrows (drawn first, under the boxes)
  const arrows = {};
  const arrow = (key, d, col = INK, dash) => {
    const g = hit(el("g", { class: "bt-arrow" }, svg), key);
    const p = el("path", { d, fill: "none", stroke: col, "stroke-width": 2.6, "stroke-linecap": "round",
      "marker-end": `url(#${col === INK ? "bt-ar" : col === MUT ? "bt-ar-mut" : "bt-ar-terra"})`,
      ...(dash ? { "stroke-dasharray": "8 7" } : {}) }, g);
    el("path", { d, fill: "none", stroke: "transparent", "stroke-width": 22 }, g);
    arrows[key] = p;
    return g;
  };
  arrow("hope", "M 336 112 L 662 112", MUT, true);
  text(500, 100, "what designers hope happens", { "text-anchor": "middle", "font-size": 15, "font-style": "italic", fill: MUT }, svg);
  arrow("a1", "M 190 178 L 190 324");
  arrow("a2", "M 384 420 L 662 420");
  arrow("a3", "M 760 482 C 700 560, 470 560, 400 498");
  arrow("a4", "M 805 344 L 805 182");
  const fbArc = arrow("fC", "M 840 62 C 760 -6, 330 -6, 252 60", C.terra[0]);
  fbArc.classList.add("bt-fail");

  // numbered questions
  const badge = (x, y, n, lines, anchor, key) => {
    const g = hit(el("g", { class: "bt-q" }, svg), key);
    el("circle", { cx: x, cy: y, r: 15, fill: INK }, g);
    text(x, y + 5.5, String(n), { "text-anchor": "middle", "font-size": 15, "font-weight": 800, fill: "#fff" }, g);
    const tx = anchor === "end" ? x - 24 : anchor === "middle" ? x : x + 24;
    lines.forEach((ln, i) => text(tx, y - 2 + i * 19 + (anchor === "middle" ? 30 : 0), ln,
      { "text-anchor": anchor, "font-size": 16, "font-weight": 700, fill: INK }, g));
  };
  badge(190, 251, 1, ["How does the rule change", "each agent's situation?"], "start", "a1");
  badge(517, 382, 2, ["How does the model respond?"], "middle", "a2");
  badge(585, 566, 3, ["How do agents reshape", "each other's situations?"], "start", "a3");
  badge(805, 251, 4, ["How does behavior add up", "to group outcomes?"], "end", "a4");

  // boxes
  const box = (key, x, y, w, h, col, title, lines, tag, tsize = 20) => {
    const g = hit(el("g", { class: "bt-box" }, svg), key);
    el("rect", { x, y, width: w, height: h, rx: 16, fill: col[2], stroke: col[0], "stroke-width": 2, filter: "url(#bt-shadow)" }, g);
    text(x + w / 2, y + 36, title, { "text-anchor": "middle", "font-size": tsize, "font-weight": 800, fill: col[1] }, g);
    lines.forEach((ln, i) => text(x + w / 2, y + 62 + i * 21, ln, { "text-anchor": "middle", "font-size": 15.5, fill: INK }, g));
    if (tag) {
      const tw = 176;
      el("rect", { x: x + w / 2 - tw / 2, y: y - 14, width: tw, height: 26, rx: 13, fill: "#fff", stroke: col[0], "stroke-width": 1.4 }, g);
      text(x + w / 2, y + 4, tag, { "text-anchor": "middle", "font-size": 13, "font-style": "italic", "font-weight": 700, fill: col[1] }, g);
    }
    return g;
  };
  box("A", 60, 70, 276, 108, C.amber, "A. Institutional change", ["e.g. add graduated sanctions", "or an appeal step"], "human, agent, or mixed");
  box("D", 664, 70, 276, 108, C.green, "D. Group outcomes", ["cooperation, enforcement cost,", "false punishment, repair"], "human, agent, or mixed");
  box("C", 664, 346, 276, 132, C.violet, "C. Agent behavior", ["what each model does", "with its new options"]);
  const bBox = box("B", 36, 326, 346, 172, C.blue, "B. Each agent's action situation", [], null, 18);
  // Ostrom's seven rule types as chips
  const rows = [["boundary", "position", "choice"], ["information", "aggregation"], ["payoff", "scope"]];
  rows.forEach((row, ri) => {
    const widths = row.map((r) => r.length * 8.4 + 24);
    let x = 209 - (widths.reduce((a, b) => a + b, 0) + 8 * (row.length - 1)) / 2;
    row.forEach((r, i) => {
      const g = el("g", { class: "bt-rule", tabindex: "0" }, bBox);
      g.dataset.rule = r;
      el("rect", { x, y: 380 + ri * 32, width: widths[i], height: 25, rx: 12.5, fill: "#fff", stroke: C.blue[0], "stroke-width": 1.3 }, g);
      text(x + widths[i] / 2, 397 + ri * 32, r, { "text-anchor": "middle", "font-size": 14, "font-weight": 700, fill: C.blue[1] }, g);
      x += widths[i] + 8;
    });
  });
  text(209, 488, "Ostrom's seven rule types", { "text-anchor": "middle", "font-size": 13, "font-style": "italic", fill: MUT }, bBox);

  // failure tags
  const fail = (key, x, y, letter, label) => {
    const g = hit(el("g", { class: "bt-fail bt-ftag" }, svg), key);
    const w = label.length * 8 + 52;
    el("rect", { x, y, width: w, height: 28, rx: 14, fill: C.terra[2], stroke: C.terra[0], "stroke-width": 1.5 }, g);
    el("circle", { cx: x + 16, cy: y + 14, r: 10, fill: C.terra[0] }, g);
    text(x + 16, y + 18.5, letter, { "text-anchor": "middle", "font-size": 13, "font-weight": 800, fill: "#fff" }, g);
    text(x + 34, y + 19, label, { "font-size": 14, "font-style": "italic", "font-weight": 700, fill: C.terra[1] }, g);
  };
  fail("fA", 432, 432, "A", "fine read as a price");
  fail("fB", 518, 296, "B", "score stops tracking conduct");
  fail("fC", 404, -4, "C", "the enforcer reshapes the rules");

  // substrate
  const sg = hit(el("g", { class: "bt-sub" }, svg), "sub");
  el("rect", { x: 40, y: 606, width: 920, height: 30, rx: 15, fill: "#fff", stroke: HAIR, "stroke-width": 1.4, "stroke-dasharray": "5 4" }, sg);
  text(500, 626, "technical substrate: shared memory, compute, tools, logs", { "text-anchor": "middle", "font-size": 14.5, fill: MUT }, sg);

  // moving token for Play
  const token = el("circle", { r: 9, fill: "#de553f", stroke: "#fff", "stroke-width": 3, class: "bt-token", opacity: 0 }, svg);

  // ---------- interaction ----------
  let locked = null, failOn = false, playing = false;
  const show = (key, rule) => {
    if (!panel) return;
    if (rule) {
      panel.style.setProperty("--c", C.blue[0]);
      panel.innerHTML = `<p class="bt-plabel">Ostrom rule type</p><h3>${rule[0].toUpperCase() + rule.slice(1)} rules</h3><p>Set ${RULES[rule]}.</p>`;
      return;
    }
    const i = INFO[key];
    if (!i) {
      panel.style.removeProperty("--c");
      panel.innerHTML = `<p class="bt-plabel">Explore</p><h3>From a rule change to group outcomes</h3><p>Hover, tap, or tab to any box, arrow, or tag. Press <strong>Play</strong> to walk the four questions, or show where institutions can fail.</p>`;
      return;
    }
    panel.style.setProperty("--c", i.c[0]);
    panel.innerHTML = `<p class="bt-plabel">${i.label}</p><h3>${i.title}</h3><p>${i.text}</p>`;
  };
  const activate = (key) => {
    svg.classList.toggle("has-active", !!key);
    hits.forEach((n) => n.classList.toggle("is-on", n.dataset.key === key));
    show(key);
  };
  hits.forEach((n) => {
    const key = n.dataset.key;
    n.addEventListener("pointerenter", () => !playing && activate(key));
    n.addEventListener("pointerleave", () => !playing && activate(locked));
    n.addEventListener("focus", () => !playing && activate(key));
    n.addEventListener("blur", () => !playing && activate(locked));
    n.addEventListener("click", (e) => { e.stopPropagation(); locked = locked === key ? null : key; activate(locked); });
    n.addEventListener("keydown", (e) => {
      if (e.key === "Enter" || e.key === " ") { e.preventDefault(); locked = locked === key ? null : key; activate(locked); }
    });
  });
  svg.querySelectorAll(".bt-rule").forEach((r) => {
    const on = (e) => { e.stopPropagation(); if (!playing) { activate("B"); show(null, r.dataset.rule); } };
    r.addEventListener("pointerenter", on);
    r.addEventListener("focus", on);
  });
  svg.addEventListener("click", () => { if (!playing) { locked = null; activate(null); } });

  if (failBtn) failBtn.addEventListener("click", () => {
    failOn = !failOn;
    svg.classList.toggle("show-fail", failOn);
    failBtn.setAttribute("aria-pressed", String(failOn));
    failBtn.textContent = failOn ? "Hide failure modes" : "Where it can fail";
    if (failOn) show("fA");
  });

  const reduce = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  const travel = (key) => new Promise((done) => {
    const p = arrows[key], len = p.getTotalLength(), dur = reduce ? 0 : 1400;
    activate(key);
    token.setAttribute("opacity", 1);
    const t0 = performance.now();
    const step = (now) => {
      const k = dur ? Math.min(1, (now - t0) / dur) : 1;
      const e = k < 0.5 ? 2 * k * k : 1 - Math.pow(-2 * k + 2, 2) / 2;
      const q = p.getPointAtLength(e * len);
      token.setAttribute("cx", q.x); token.setAttribute("cy", q.y);
      if (k < 1) requestAnimationFrame(step); else setTimeout(done, reduce ? 900 : 1300);
    };
    requestAnimationFrame(step);
  });
  if (playBtn) playBtn.addEventListener("click", async () => {
    if (playing) return;
    playing = true; playBtn.disabled = true;
    for (const k of ["a1", "a2", "a3", "a4"]) await travel(k);
    activate("D");
    await new Promise((r) => setTimeout(r, 1200));
    token.setAttribute("opacity", 0);
    playing = false; playBtn.disabled = false;
    activate(locked);
  });
  show(null);
})();
