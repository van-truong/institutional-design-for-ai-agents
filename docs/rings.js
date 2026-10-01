/* Interactive nested-systems figure (paper Fig. 1), after Bronfenbrenner: one model at the center, inside the
   settings it acts in (microsystem), the links between them (mesosystem), and the platform, market, and legal
   institutions that govern it (exo- and macrosystem). A cutaway wedge reads outward from one model to a society
   of institutions. Hover, tap, or tab to a ring or legend item to read about it. Palette: figs/PALETTE.md. */
(function () {
  const stage = document.getElementById("rings-stage");
  const legend = document.getElementById("rings-legend");
  const panel = document.getElementById("rings-panel");
  if (!stage) return;

  const NS = "http://www.w3.org/2000/svg";
  // paper mode (stage data-mode="paper"): larger text for print, an in-figure title and legend, no animation
  const PAPER = stage.dataset.mode === "paper";
  const FS = PAPER ? { chip: 20, name: 20, story: 19, chrono: 20, model: 20 }
                   : { chip: 15, name: 17, story: 15, chrono: 15, model: 15 };
  const FONT = "'Helvetica Neue', Helvetica, Arial, sans-serif";
  const CX = 500, CY = 500;
  const INK = "#3F4D5A", MUT = "#6B7787";

  // key, name, radius (outer), [mid, dark, tint], summary, examples, longer note
  const LEVELS = [
    { key: "macro", name: "Macrosystem", r: 442, c: ["#C79A3A", "#8A5A0B", "#FBEEDA"], group: "gov",
      summary: "law, markets, norms, culture",
      items: [["law & regulation", 216], ["markets", 150], ["cultural values", 180]],
      note: "The broadest rules a society lives by. For agents, these are the legal, economic, and cultural institutions that will decide what agent groups may do and who answers for it." },
    { key: "exo", name: "Exosystem", r: 352, c: ["#4F9070", "#2F6B4A", "#E5F0E1"], group: "gov",
      summary: "settings that shape it from outside",
      items: [["platform policy", 222], ["API limits", 140], ["other agents", 180]],
      note: "Settings the model never enters directly but that still shape it: a platform's usage policy, rate and budget limits, and agents in other systems competing for the same resources." },
    { key: "meso", name: "Mesosystem", r: 262, c: ["#0F766E", "#04342C", "#E3F1EC"], group: "inter",
      summary: "links between those settings",
      items: [["handoffs", 232], ["orchestrator", 122], ["shared memory", 180]],
      note: "The web of links among the settings an agent acts in: work handed from one agent to another, an orchestrator routing tasks, and memory that many agents read and write." },
    { key: "micro", name: "Microsystem", r: 170, c: ["#3A6EA5", "#2F3D6B", "#DCE8F5"], group: "inter",
      summary: "settings it acts in directly",
      items: [["user", 270], ["tools", 90], ["task", 180]],
      note: "The settings the model acts in directly: the user it serves, the tools it calls, and the task it is given." },
    { key: "model", name: "Individual model", r: 78, c: ["#6C5CD0", "#463BA0", "#ECE9FB"], group: "model",
      summary: "the agent at the center", items: [],
      note: "One model with its prompt and policy. Model-level alignment and evaluation examine only this center." },
  ];
  const BY = Object.fromEntries(LEVELS.map((l) => [l.key, l]));
  const inner = (l) => { const i = LEVELS.indexOf(l); return i < LEVELS.length - 1 ? LEVELS[i + 1].r : 0; };
  const EXTRA = {
    wedge: { name: "Cutaway", c: [INK, INK, "#F7F9FB"], summary: "from one model to many societies",
      note: "Reading outward: one model becomes a group of interacting agents, then a society, and finally many institutions and societies interacting with one another." },
    chrono: { name: "Chronosystem", c: [MUT, INK, "#EEF2F6"], summary: "change over time",
      note: "Every layer changes over time. Models are updated, groups re-form, and rules are rewritten, so an institution that works today may not work tomorrow." },
    recip: { name: "Reciprocal influence", c: [MUT, INK, "#EEF2F6"], summary: "each layer shapes the others",
      note: "Influence runs both ways: each layer shapes, and is shaped by, the others. Agent societies will also draw on human resources, infrastructure, and services, and their behavior will feed back into them." },
  };

  // ---------- helpers ----------
  const el = (tag, attrs = {}, parent) => {
    const n = document.createElementNS(NS, tag);
    for (const [k, v] of Object.entries(attrs)) n.setAttribute(k, v);
    if (parent) parent.appendChild(n);
    return n;
  };
  const pt = (deg, r) => { const a = (deg * Math.PI) / 180; return [CX + r * Math.sin(a), CY - r * Math.cos(a)]; };
  const f = (n) => n.toFixed(1);
  const mix = (a, b, t) => {
    const p = (h) => [1, 3, 5].map((i) => parseInt(h.slice(i, i + 2), 16));
    const [x, y] = [p(a), p(b)];
    return "#" + x.map((v, i) => Math.round(v + (y[i] - v) * t).toString(16).padStart(2, "0")).join("");
  };
  // arc along the bottom, left to right, so text on it reads upright
  const bottomArc = (r, span = 176) => {
    const [x0, y0] = pt(180 + span / 2, r), [x1, y1] = pt(180 - span / 2, r);
    return `M ${f(x0)} ${f(y0)} A ${r} ${r} 0 0 0 ${f(x1)} ${f(y1)}`;
  };

  // ---------- svg ----------
  const svg = el("svg", { viewBox: PAPER ? "0 -40 1560 1064" : "0 34 1000 990", role: "img", class: "rg-svg", xmlns: NS, "font-family": FONT,
    "aria-labelledby": "rg-title rg-desc" }, stage);
  el("title", { id: "rg-title" }, svg).textContent = "From one model to a society of institutions";
  el("desc", { id: "rg-desc" }, svg).textContent =
    "Five nested rings: an individual model at the center, then the microsystem, mesosystem, exosystem, and macrosystem. " +
    "A cutaway wedge shows one model becoming a group, a society, and many interacting institutions. An arc along the bottom marks change over time.";
  const defs = el("defs", {}, svg);
  const shadow = el("filter", { id: "rg-shadow", x: "-10%", y: "-10%", width: "120%", height: "120%" }, defs);
  el("feDropShadow", { dx: "0", dy: "10", stdDeviation: "14", "flood-color": "#3F4D5A", "flood-opacity": "0.16" }, shadow);
  const soft = el("filter", { id: "rg-soft", x: "-20%", y: "-20%", width: "140%", height: "140%" }, defs);
  el("feDropShadow", { dx: "0", dy: "1.5", stdDeviation: "1.6", "flood-color": "#3F4D5A", "flood-opacity": "0.18" }, soft);
  const mk = (id, col) => {
    const m = el("marker", { id, viewBox: "0 0 10 10", refX: "8", refY: "5", markerWidth: "7", markerHeight: "7",
      orient: "auto-start-reverse" }, defs);
    el("path", { d: "M 0 0 L 10 5 L 0 10 z", fill: col }, m);
  };
  mk("rg-arrow", MUT); mk("rg-arrow-micro", "#3A6EA5"); mk("rg-arrow-ink", INK);

  // rings, largest first; each band brightens toward its inner edge
  const bands = el("g", { class: "rg-bands" }, svg);
  bands.setAttribute("filter", "url(#rg-shadow)");
  LEVELS.forEach((l, i) => {
    const g = el("radialGradient", { id: `rg-g-${l.key}`, cx: CX, cy: CY, r: l.r, gradientUnits: "userSpaceOnUse" }, defs);
    const r0 = inner(l) / l.r;
    el("stop", { offset: "0", "stop-color": mix(l.c[2], "#ffffff", 0.55) }, g);
    el("stop", { offset: String(r0), "stop-color": mix(l.c[2], "#ffffff", 0.45) }, g);
    el("stop", { offset: "1", "stop-color": mix(l.c[2], l.c[0], 0.22) }, g);
    const disk = el("circle", { cx: CX, cy: CY, r: l.r, fill: `url(#rg-g-${l.key})`, stroke: l.c[0],
      "stroke-width": "1.6", class: "rg-disk rg-hit", "data-key": l.key, tabindex: "0",
      style: `--d:${(LEVELS.length - 1 - i) * 110}ms`, "aria-label": `${l.name}: ${l.summary}` }, bands);
    disk.dataset.key = l.key;
    // a thin white rule just inside each edge gives the rings a little relief
    el("circle", { cx: CX, cy: CY, r: l.r - 2.2, fill: "none", stroke: "#fff", "stroke-opacity": "0.75",
      "stroke-width": "1.2", class: "rg-disk", "data-key": l.key, "pointer-events": "none",
      style: `--d:${(LEVELS.length - 1 - i) * 110}ms` }, bands);
  });

  // reciprocal influence: dashed two-way arrows through the rings
  const recip = el("g", { class: "rg-recip rg-hit", "data-key": "recip", tabindex: "0",
    "aria-label": "Reciprocal influence: each layer shapes the others" }, svg);
  [300, 60].forEach((deg) => {  // upper sides, clear of the example chips
    const [x0, y0] = pt(deg, 92), [x1, y1] = pt(deg, 432);
    el("line", { x1: f(x0), y1: f(y0), x2: f(x1), y2: f(y1), stroke: MUT, "stroke-width": "1.8",
      "stroke-dasharray": "6 6", "marker-start": "url(#rg-arrow)", "marker-end": "url(#rg-arrow)", opacity: "0.75" }, recip);
    el("line", { x1: f(x0), y1: f(y0), x2: f(x1), y2: f(y1), stroke: "transparent", "stroke-width": "18" }, recip);
  });

  // cutaway wedge
  const WA = 30;
  const [wl, wly] = pt(-WA, BY.macro.r), [wr, wry] = pt(WA, BY.macro.r);
  const wedgeD = `M ${CX} ${CY} L ${f(wl)} ${f(wly)} A ${BY.macro.r} ${BY.macro.r} 0 0 1 ${f(wr)} ${f(wry)} Z`;
  const clip = el("clipPath", { id: "rg-wedge-clip" }, defs);
  el("path", { d: wedgeD }, clip);
  const wg = el("linearGradient", { id: "rg-wedge-fill", x1: "0", y1: "1", x2: "0", y2: "0" }, defs);
  el("stop", { offset: "0", "stop-color": "#ffffff", "stop-opacity": "0.92" }, wg);
  el("stop", { offset: "1", "stop-color": "#ffffff", "stop-opacity": "0.72" }, wg);
  const wedge = el("g", { class: "rg-wedge rg-hit", "data-key": "wedge", tabindex: "0",
    "aria-label": "Cutaway: from one model to a society of institutions" }, svg);
  el("path", { d: wedgeD, fill: "url(#rg-wedge-fill)" }, wedge);
  const ghost = el("g", { "clip-path": "url(#rg-wedge-clip)", "pointer-events": "none" }, wedge);
  LEVELS.forEach((l) => el("circle", { cx: CX, cy: CY, r: l.r, fill: "none", stroke: l.c[0], "stroke-opacity": "0.35",
    "stroke-width": "1.2" }, ghost));
  el("path", { d: wedgeD, fill: "none", stroke: INK, "stroke-width": "1.5", "stroke-dasharray": "5 5",
    "stroke-opacity": "0.75", "pointer-events": "none" }, wedge);

  // glyphs
  const agent = (x, y, s, col, parent) => {
    const g = el("g", { transform: `translate(${f(x)} ${f(y)}) scale(${s})` }, parent);
    el("line", { x1: 0, y1: -15, x2: 0, y2: -20, stroke: col[1], "stroke-width": 1.6, "stroke-linecap": "round" }, g);
    el("circle", { cx: 0, cy: -21.5, r: 2.2, fill: col[0] }, g);
    el("rect", { x: -11, y: -15, width: 22, height: 15, rx: 5, fill: "#fff", stroke: col[1], "stroke-width": 1.6 }, g);
    el("circle", { cx: -4.5, cy: -7.5, r: 2, fill: col[1] }, g);
    el("circle", { cx: 4.5, cy: -7.5, r: 2, fill: col[1] }, g);
    el("rect", { x: -8.5, y: 2, width: 17, height: 11, rx: 4, fill: col[0], stroke: col[1], "stroke-width": 1.2 }, g);
    return g;
  };
  const temple = (x, y, s, col, parent) => {
    const g = el("g", { transform: `translate(${f(x)} ${f(y)}) scale(${s})` }, parent);
    el("path", { d: "M -16 -8 L 0 -18 L 16 -8 Z", fill: col[0], stroke: col[1], "stroke-width": 1.2, "stroke-linejoin": "round" }, g);
    [-10, -3.5, 3.5, 10].forEach((cx) => el("rect", { x: cx - 1.6, y: -7, width: 3.2, height: 12, fill: col[1] }, g));
    el("rect", { x: -17, y: 5, width: 34, height: 4, rx: 1, fill: col[1] }, g);
    return g;
  };
  const up = (r0, r1, parent) => {
    const [, y0] = pt(0, r0), [, y1] = pt(0, r1);
    el("line", { x1: CX, y1: y0, x2: CX, y2: y1, stroke: INK, "stroke-width": 1.8, "stroke-opacity": 0.7,
      "marker-end": "url(#rg-arrow-ink)" }, parent);
  };
  // cutaway captions curve with the rings: across the top for the story, along the bottom for "one model"
  const arcText = (id, d, s, col, parent, size = FS.story) => {
    el("path", { id, d, fill: "none" }, defs);
    const t = el("text", { class: "rg-wtext", fill: col, "font-size": size, "font-style": "italic", "font-weight": 600 }, parent);
    el("textPath", { href: `#${id}`, startOffset: "50%", "text-anchor": "middle" }, t).textContent = s;
    return t;
  };
  const topArc = (r, span = 54) => {
    const [x0, y0] = pt(-span / 2, r), [x1, y1] = pt(span / 2, r);
    return `M ${f(x0)} ${f(y0)} A ${r} ${r} 0 0 1 ${f(x1)} ${f(y1)}`;
  };
  const wtext = (r, s, col, parent) => arcText(`rg-story-${r}`, topArc(r), s, col, parent);
  const story = el("g", { class: "rg-story", "pointer-events": "none" }, wedge);
  const cM = BY.model.c, cI = BY.micro.c, cS = BY.exo.c, cG = BY.macro.c;
  agent(CX, CY - 30, 1.15, cM, story);
  up(84, 112, story);
  [[-30, 148], [30, 148], [0, 186]].forEach(([dx, r], i, a) => {
    const [nx, ny] = a[(i + 1) % 3];
    el("line", { x1: CX + dx, y1: CY - r + 4, x2: CX + nx, y2: CY - ny + 4, stroke: cI[0], "stroke-width": 1.4,
      "stroke-dasharray": "3 3" }, story);
  });
  [[-30, 148], [30, 148], [0, 186]].forEach(([dx, r]) => agent(CX + dx, CY - r + 12, 0.8, cI, story));
  wtext(200, "a group interacts", cI[1], story);
  up(226, 252, story);
  for (let i = -4; i <= 4; i++) agent(CX + i * 27, CY - 272, 0.52, cS, story);
  wtext(288, "a society forms", cS[1], story);
  up(312, 332, story);
  const inst = [[-92, 350], [0, 384], [92, 350]];
  inst.forEach(([dx, r], i) => {
    const [nx, nr] = inst[(i + 1) % 3];
    el("line", { x1: CX + dx, y1: CY - r, x2: CX + nx, y2: CY - nr, stroke: cG[0], "stroke-width": 1.4, "stroke-dasharray": "3 3" }, story);
  });
  inst.forEach(([dx, r]) => {
    temple(CX + dx, CY - r, 0.95, cG, story);
    for (let k = -1; k <= 1; k++) agent(CX + dx + k * 12, CY - r + 28, 0.36, cG, story);
  });
  // curved along the outer ring, like the ring itself
  wtext(416, "institutions & societies interact", cG[1], story);
  // a gentle upward curve: a wide, shallow arc whose lowest point sits just below the center
  const [om0, om1, omY, omR] = [CX - 66, CX + 66, CY + 30, 150];
  const omSag = omR - Math.sqrt(omR * omR - 66 * 66);
  const mt = arcText("rg-one-model", `M ${om0} ${f(omY - omSag)} A ${omR} ${omR} 0 0 0 ${om1} ${f(omY - omSag)}`,
    "one model", cM[1], svg, FS.model);
  mt.setAttribute("pointer-events", "none");

  // ring names (curved along the bottom) and example chips
  const labels = el("g", { class: "rg-labels" }, svg);
  LEVELS.filter((l) => l.key !== "model").forEach((l) => {
    const ri = inner(l);
    const pid = `rg-name-${l.key}`;
    el("path", { id: pid, d: bottomArc(l.r - 7), fill: "none" }, defs);  // name near the outer edge
    const t = el("text", { class: "rg-name", fill: l.c[1], "data-key": l.key, "font-size": FS.name, "font-weight": 800,
      "letter-spacing": PAPER ? "0.06em" : "0.14em" }, labels);
    const tp = el("textPath", { href: `#${pid}`, startOffset: "50%", "text-anchor": "middle" }, t);
    tp.textContent = l.name.toUpperCase();
    l.items.forEach(([label, deg0]) => {
      let deg = deg0;
      const k = FS.chip / 15, w = label.length * 8.6 * k + 26 * k, h = 26 * k;
      const r = deg === 180 ? ri + h / 2 + 7 : (ri + l.r) / 2;  // bottom chip near the inner edge, above the name
      const [x, y] = pt(deg, r);
      const chip = el("g", { class: "rg-chip", "data-key": l.key, transform: `translate(${f(x)} ${f(y)})` }, labels);
      el("rect", { x: f(-w / 2), y: f(-h / 2), width: f(w), height: f(h), rx: f(h / 2), fill: "#fff", stroke: l.c[0], "stroke-width": 1.4,
        filter: "url(#rg-soft)" }, chip);
      const ct = el("text", { y: f(5.5 * k), "text-anchor": "middle", fill: l.c[1], class: "rg-chip-text", "font-size": FS.chip,
        "font-weight": 700 }, chip);
      ct.textContent = label;
    });
  });

  // chronosystem: time runs along the bottom
  const chrono = el("g", { class: "rg-chrono rg-hit", "data-key": "chrono", tabindex: "0",
    "aria-label": "Chronosystem: change over time" }, svg);
  el("path", { d: bottomArc(474, 118), fill: "none", stroke: MUT, "stroke-width": 2.6, "stroke-linecap": "round",
    "marker-end": "url(#rg-arrow)", class: "rg-chrono-line" }, chrono);
  el("path", { d: bottomArc(474, 118), fill: "none", stroke: "transparent", "stroke-width": 26 }, chrono);
  el("path", { id: "rg-chrono-text", d: bottomArc(500, 118), fill: "none" }, defs);
  const ctt = el("text", { class: "rg-chrono-text", fill: MUT, "font-size": FS.chrono, "font-weight": 800, "letter-spacing": "0.18em" }, chrono);
  const ctp = el("textPath", { href: "#rg-chrono-text", startOffset: "50%", "text-anchor": "middle" }, ctt);
  ctp.textContent = "CHRONOSYSTEM · TIME";

  // ---------- paper mode: title and legend inside the SVG ----------
  if (PAPER) {
    const t = el("text", { x: 780, y: -2, "text-anchor": "middle", "font-size": 40, "font-weight": 800, fill: INK }, svg);
    t.textContent = "From an individual model to a society of institutions";
    const L = el("g", { class: "rg-paper-legend" }, svg);
    let y = 270;
    [["gov", "GOVERNING INSTITUTIONS"], ["inter", "AGENT–GROUP INTERACTIONS"], ["model", "INDIVIDUAL MODEL"]].forEach(([g, label]) => {
      const h = el("text", { x: 1060, y, "font-size": 20, "font-weight": 800, "letter-spacing": "0.1em", fill: MUT }, L);
      h.textContent = label;
      y += 46;
      LEVELS.filter((l) => l.group === g).forEach((l) => {
        el("circle", { cx: 1080, cy: y - 2, r: 17, fill: l.c[2], stroke: l.c[0], "stroke-width": 3 }, L);
        const n = el("text", { x: 1112, y: y + 6, "font-size": 31, "font-weight": 800, fill: l.c[1] }, L);
        n.textContent = l.name;
        const d = el("text", { x: 1112, y: y + 40, "font-size": 23, fill: INK }, L);
        d.textContent = l.summary;
        y += 92;
      });
      y += 18;
    });
    return;
  }

  // ---------- legend and detail panel ----------
  const GROUPS = [["gov", "Governing institutions"], ["inter", "Agent–group interactions"], ["model", "Individual model"]];
  if (legend) {
    GROUPS.forEach(([g, label]) => {
      const box = document.createElement("div");
      box.className = "rg-lgroup";
      const h = document.createElement("p");
      h.className = "rg-lgroup-label";
      h.textContent = label;
      box.appendChild(h);
      LEVELS.filter((l) => l.group === g).forEach((l) => {
        const b = document.createElement("button");
        b.type = "button";
        b.className = "rg-litem";
        b.dataset.key = l.key;
        b.style.setProperty("--c", l.c[0]);
        b.style.setProperty("--d", l.c[1]);
        b.style.setProperty("--t", l.c[2]);
        b.innerHTML = `<span class="rg-swatch"></span><span><strong>${l.name}</strong><small>${l.summary}</small></span>`;
        box.appendChild(b);
      });
      legend.appendChild(box);
    });
  }

  let locked = null;
  const describe = (key) => {
    if (!panel) return;
    const l = BY[key] || EXTRA[key];
    if (!l) {
      panel.innerHTML = `<p class="rg-panel-label">Explore</p><h3>Nested systems around interacting agents</h3>` +
        `<p>Hover, tap, or tab to any ring, the cutaway, or the time arc.</p>`;
      panel.style.removeProperty("--c");
      return;
    }
    panel.style.setProperty("--c", l.c[0]);
    const ex = l.items && l.items.length
      ? `<p class="rg-ex">${l.items.map(([s]) => `<span>${s}</span>`).join("")}</p>` : "";
    panel.innerHTML = `<p class="rg-panel-label">${l.summary}</p><h3>${l.name}</h3><p>${l.note}</p>${ex}`;
  };
  const activate = (key) => {
    svg.classList.toggle("has-active", !!key);
    svg.querySelectorAll("[data-key]").forEach((n) => n.classList.toggle("is-on", n.dataset.key === key));
    if (legend) legend.querySelectorAll(".rg-litem").forEach((b) => {
      b.classList.toggle("is-on", b.dataset.key === key);
      b.setAttribute("aria-pressed", String(b.dataset.key === locked));
    });
    describe(key);
  };
  const hover = (key) => activate(key || locked);
  svg.querySelectorAll(".rg-hit, .rg-chip").forEach((n) => {
    const key = n.dataset.key || n.getAttribute("data-key");
    n.addEventListener("pointerenter", () => hover(key));
    n.addEventListener("pointerleave", () => hover(null));
    n.addEventListener("focus", () => hover(key));
    n.addEventListener("blur", () => hover(null));
    n.addEventListener("click", (e) => { e.stopPropagation(); locked = locked === key ? null : key; activate(locked); });
    n.addEventListener("keydown", (e) => {
      if (e.key === "Enter" || e.key === " ") { e.preventDefault(); locked = locked === key ? null : key; activate(locked); }
    });
  });
  if (legend) legend.querySelectorAll(".rg-litem").forEach((b) => {
    b.addEventListener("pointerenter", () => hover(b.dataset.key));
    b.addEventListener("pointerleave", () => hover(null));
    b.addEventListener("focus", () => hover(b.dataset.key));
    b.addEventListener("blur", () => hover(null));
    b.addEventListener("click", () => { locked = locked === b.dataset.key ? null : b.dataset.key; activate(locked); });
  });
  svg.addEventListener("click", () => { locked = null; activate(null); });
  describe(null);

  // grow the rings outward from the model when the figure scrolls into view
  if ("IntersectionObserver" in window) {
    const io = new IntersectionObserver((es) => {
      if (es.some((e) => e.isIntersecting)) { stage.classList.add("rg-in"); io.disconnect(); }
    }, { threshold: 0.25 });
    io.observe(stage);
  } else stage.classList.add("rg-in");
})();
