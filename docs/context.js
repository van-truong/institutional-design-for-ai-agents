/* Interactive agent-in-context figure (paper Fig. 2). Individual models are nested within agent-group interactions
   and governing institutions. Institutions can form top-down, designed and imposed on agents, or bottom-up, as
   conventions that emerge from repeated interaction; for AI agents today the paper argues the first must lead.
   The mini rings beside each layer match the nested-systems figure (Fig. 1). Palette: figs/PALETTE.md. */
(function () {
  const stage = document.getElementById("ctx-stage");
  const panel = document.getElementById("ctx-panel");
  if (!stage) return;

  const NS = "http://www.w3.org/2000/svg";
  const FONT = "'Helvetica Neue', Helvetica, Arial, sans-serif";
  const INK = "#3F4D5A", MUT = "#6B7787", HAIR = "#B3BEC9";
  const AMBER = ["#C79A3A", "#8A5A0B", "#F3E4C4", "#E3C88C"];
  const BLUE = ["#3A6EA5", "#2F3D6B", "#DCE8F5", "#A9C4E0"];
  const VIOLET = ["#6C5CD0", "#463BA0", "#ECE9FB", "#C4BCEC"];
  // Fig. 1 ring colors, outermost first: macro, exo, meso, micro, model
  const RING = [["macro", "#C79A3A", "#FBEEDA"], ["exo", "#4F9070", "#E5F0E1"], ["meso", "#0F766E", "#E3F1EC"],
    ["micro", "#3A6EA5", "#DCE8F5"], ["model", "#6C5CD0", "#ECE9FB"]];

  const LAYERS = [
    { key: "gov", y: 118, c: AMBER, title: "Governing institutions", rings: ["exo", "macro"], nodes: "net",
      bullets: ["norms, monitoring, sanctions, repair", "platform, market & legal structure", "who sets and enforces the rules"],
      note: "Fig. 1: exo- and macrosystem",
      text: "The rules, roles, and procedures for enforcement and repair that structure interaction among agents: North's rules of the game and Ostrom's rules in use, together with the machinery that applies them." },
    { key: "inter", y: 278, c: BLUE, title: "Agent–group interactions", rings: ["micro", "meso"], nodes: "tri",
      bullets: ["communication, handoffs, shared memory", "conventions, reciprocity, reputation", "emergent roles & coordination"],
      note: "Fig. 1: micro- and mesosystem",
      text: "The settings an agent acts in and the links between them. This is where conventions, reciprocity, and roles can form, and where group-level failures can arise even when each agent appears aligned." },
    { key: "model", y: 438, c: VIOLET, title: "Individual model", sub: "(even if aligned)", rings: ["model"], nodes: "one",
      bullets: ["alignment, refusals, capabilities", "truthfulness, instruction-following", "what single-model evals test"],
      note: "Fig. 1: the model at the center",
      text: "One model, however well aligned. Single-model evaluations examine only this layer, so they cannot see behavior that emerges only when agents interact." },
  ];
  const ARROWS = {
    down: { c: AMBER, title: "Top-down: designed and imposed",
      text: "Institutions as rules, mechanisms, and governance arrangements intentionally designed to align incentives, resolve conflicts, and protect collective outcomes. For AI agents today, we argue this direction must lead: humans specify the rules and structures within which agents operate." },
    up: { c: VIOLET, title: "Bottom-up: emergent conventions",
      text: "Institutions as stable patterns of behavior sustained by conventions and repeated interaction, as in Ostrom's self-governing commons. This presupposes persistent memory, expectations about others' strategies, and collective intentionality, which current LLM agents mostly lack, so stable bottom-up institutions in AI societies cannot yet be assumed." },
  };

  const el = (tag, attrs = {}, parent) => {
    const n = document.createElementNS(NS, tag);
    for (const [k, v] of Object.entries(attrs)) n.setAttribute(k, v);
    if (parent) parent.appendChild(n);
    return n;
  };
  const text = (x, y, s, attrs, parent) => { const t = el("text", { x, y, ...attrs }, parent); t.textContent = s; return t; };

  const svg = el("svg", { viewBox: "0 0 900 540", xmlns: "http://www.w3.org/2000/svg", role: "img", class: "ctx-svg", "font-family": FONT,
    "aria-labelledby": "ctx-title ctx-desc" }, stage);
  el("title", { id: "ctx-title" }, svg).textContent = "The agent in its institutional context";
  el("desc", { id: "ctx-desc" }, svg).textContent =
    "Three stacked layers: governing institutions on top, agent-group interactions in the middle, and the individual model at the bottom. " +
    "A top-down arrow marks designed institutions and a bottom-up arrow marks emergent conventions.";
  const defs = el("defs", {}, svg);
  const sh = el("filter", { id: "ctx-shadow", x: "-20%", y: "-30%", width: "140%", height: "180%" }, defs);
  el("feDropShadow", { dx: 0, dy: 8, stdDeviation: 7, "flood-color": INK, "flood-opacity": 0.16 }, sh);
  [["ctx-ar-amber", AMBER[0]], ["ctx-ar-violet", VIOLET[0]]].forEach(([id, col]) => {
    const m = el("marker", { id, viewBox: "0 0 10 10", refX: 7, refY: 5, markerWidth: 3, markerHeight: 3, orient: "auto" }, defs);
    el("path", { d: "M 0 0 L 10 5 L 0 10 z", fill: col }, m);
  });

  const hits = [];
  const hit = (g, key) => { g.setAttribute("tabindex", "0"); g.dataset.key = key; g.classList.add("ctx-hit"); hits.push(g); return g; };

  // dotted guides between the stacked tiles
  const TX = 250, TW = 112, TH = 40, DEPTH = 13;
  [TX - TW, TX + TW].forEach((x) => el("line", { x1: x, y1: LAYERS[0].y, x2: x, y2: LAYERS[2].y, stroke: HAIR,
    "stroke-width": 1.2, "stroke-dasharray": "3 5" }, svg));

  // arrows with horizontal labels
  const arrowG = (key, x, y0, y1, col, marker, label, sub, ly) => {
    const g = hit(el("g", { class: "ctx-arrow" }, svg), key);
    const gr = el("linearGradient", { id: `ctx-g-${key}`, gradientUnits: "userSpaceOnUse", x1: x, y1: y0, x2: x, y2: y1 }, defs);
    el("stop", { offset: 0, "stop-color": col, "stop-opacity": 0.35 }, gr);
    el("stop", { offset: 1, "stop-color": col, "stop-opacity": 1 }, gr);
    el("line", { x1: x, y1: y0, x2: x, y2: y1, stroke: `url(#ctx-g-${key})`, "stroke-width": 7, "stroke-linecap": "round",
      "marker-end": `url(#${marker})` }, g);
    el("line", { x1: x, y1: y0, x2: x, y2: y1, stroke: "transparent", "stroke-width": 30 }, g);
    const w = 130;
    el("rect", { x: x - w / 2, y: ly - 22, width: w, height: 44, rx: 12, fill: "#fff", stroke: col, "stroke-width": 1.6 }, g);
    text(x, ly - 3, label, { "text-anchor": "middle", "font-size": 15, "font-weight": 700, "letter-spacing": "0.06em", fill: col }, g);
    text(x, ly + 14, sub, { "text-anchor": "middle", "font-size": 12.5, "font-style": "italic", fill: MUT }, g);
  };
  arrowG("down", 62, 88, 462, AMBER[0], "ctx-ar-amber", "TOP-DOWN", "designed, imposed", 52);
  arrowG("up", 438, 462, 88, VIOLET[0], "ctx-ar-violet", "BOTTOM-UP", "emergent conventions", 500);

  // layers
  const nodes = (kind, cx, cy, col, g) => {
    const pts = kind === "net" ? [[-46, -4], [-22, -14], [4, -12], [26, -2], [-10, 6], [16, 8]]
      : kind === "tri" ? [[-26, 4], [0, -12], [26, 4]] : [[0, 0]];
    const links = kind === "net" ? [[0, 1], [1, 2], [2, 3], [1, 4], [4, 5], [2, 5], [3, 5]] : kind === "tri" ? [[0, 1], [1, 2], [0, 2]] : [];
    links.forEach(([a, b]) => el("line", { x1: cx + pts[a][0], y1: cy + pts[a][1], x2: cx + pts[b][0], y2: cy + pts[b][1],
      stroke: col[0], "stroke-width": 1.6, opacity: 0.8 }, g));
    if (kind === "one") el("circle", { cx, cy, r: 13, fill: "none", stroke: col[0], "stroke-width": 1.4, opacity: 0.6 }, g);
    pts.forEach(([dx, dy]) => el("circle", { cx: cx + dx, cy: cy + dy, r: kind === "one" ? 7 : 5, fill: col[0], stroke: "#fff", "stroke-width": 1.5 }, g));
  };
  const miniRings = (cx, cy, on, g) => {
    RING.forEach(([k, mid, tint], i) => {
      const r = 30 - i * 6;
      const lit = on.includes(k);
      el("circle", { cx, cy, r, fill: lit ? tint : "#fff", stroke: lit ? mid : HAIR, "stroke-width": lit ? 2.4 : 1.1 }, g);
    });
  };

  LAYERS.forEach((l, i) => {
    const g = hit(el("g", { class: "ctx-layer", style: `--d:${(2 - i) * 140}ms` }, svg), l.key);
    const { y } = l, c = l.c;
    el("path", { d: `M ${TX - TW} ${y} L ${TX} ${y + TH} L ${TX + TW} ${y} L ${TX + TW} ${y + DEPTH} L ${TX} ${y + TH + DEPTH} L ${TX - TW} ${y + DEPTH} Z`,
      fill: c[3] }, g);
    const tg = el("linearGradient", { id: `ctx-top-${l.key}`, x1: 0, y1: 0, x2: 1, y2: 1 }, defs);
    el("stop", { offset: 0, "stop-color": "#ffffff", "stop-opacity": 0.9 }, tg);
    el("stop", { offset: 1, "stop-color": c[2] }, tg);
    el("path", { d: `M ${TX - TW} ${y} L ${TX} ${y - TH} L ${TX + TW} ${y} L ${TX} ${y + TH} Z`, fill: `url(#ctx-top-${l.key})`,
      stroke: c[0], "stroke-width": 1.4, filter: "url(#ctx-shadow)", class: "ctx-tile" }, g);
    nodes(l.nodes, TX, y, c, g);
    // right-hand label
    miniRings(530, y - 18, l.rings, g);
    text(580, y - 26, l.title, { "font-size": 22, "font-weight": 700, fill: c[1] }, g);
    let ty = y - 4;
    if (l.sub) { text(580, ty, l.sub, { "font-size": 17, "font-style": "italic", fill: c[1] }, g); ty += 22; }
    l.bullets.forEach((b, k) => {
      el("circle", { cx: 586, cy: ty + k * 21 - 5, r: 2.6, fill: c[0] }, g);
      text(596, ty + k * 21, b, { "font-size": 15, fill: INK }, g);
    });
    text(580, ty + l.bullets.length * 21 + 2, l.note, { "font-size": 13, "font-style": "italic", fill: MUT }, g);
  });

  // ---------- interaction ----------
  let locked = null;
  const describe = (key) => {
    if (!panel) return;
    const l = LAYERS.find((x) => x.key === key), a = ARROWS[key];
    if (!l && !a) {
      panel.style.removeProperty("--c");
      panel.innerHTML = `<p class="fx-plabel">Explore</p><h3>The agent in its institutional context</h3>` +
        `<p>Hover, tap, or tab to a layer or to either arrow.</p>`;
      return;
    }
    const it = l || a;
    panel.style.setProperty("--c", it.c[0]);
    panel.innerHTML = `<p class="fx-plabel">${l ? "Layer" : "Direction"}</p><h3>${it.title}</h3><p>${it.text}</p>`;
  };
  const activate = (key) => {
    svg.classList.toggle("has-active", !!key);
    hits.forEach((n) => n.classList.toggle("is-on", n.dataset.key === key));
    describe(key);
  };
  hits.forEach((n) => {
    const key = n.dataset.key;
    n.addEventListener("pointerenter", () => activate(key));
    n.addEventListener("pointerleave", () => activate(locked));
    n.addEventListener("focus", () => activate(key));
    n.addEventListener("blur", () => activate(locked));
    n.addEventListener("click", (e) => { e.stopPropagation(); locked = locked === key ? null : key; activate(locked); });
    n.addEventListener("keydown", (e) => {
      if (e.key === "Enter" || e.key === " ") { e.preventDefault(); locked = locked === key ? null : key; activate(locked); }
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
