/* Cooperation dilemmas (paper Fig. 3): the four shared-resource dilemmas of Section 2, plus the two the text
   describes beyond that framing (coordination and collusion). Each card shows the core tension, a hand-drawn
   human scene and an LLM-agent scene in the style of the poster artwork, and examples from the paper.
   On the website every card is its own element in a responsive grid (one per row on phones); hover, focus, or tap
   a card to read the paper's description. With data-mode="paper" the six cards are drawn into one SVG for print. */
(function () {
  const stage = document.getElementById("dl-stage");
  if (!stage) return;
  const PAPER = stage.dataset.mode === "paper";

  const NS = "http://www.w3.org/2000/svg";
  const FONT = "'Helvetica Neue', Helvetica, Arial, sans-serif";
  const INK = "#2C2C2A", MUT = "#6B7787";
  // header, dark text, tint (figs/PALETTE.md); the first four match the paper figure's card colors
  const CARDS = [
    { key: "extractive", title: "Extractive dilemma", head: "#8F3F1E", dark: "#8F3F1E", tint: "#FBEDE6", mid: "#C2662A",
      tension: "Overuse of a shared resource depletes it.",
      human: "overfishing, overgrazing", llm: "API budgets, shared compute, tool calls, context windows",
      more: "Overuse degrades a shared resource: overfishing a fishery, or agents exhausting a shared tool-call budget, context window, or rate limit.",
      scenes: ["pond", "budget"], bubbles: ["don't overfish!", ""] },
    { key: "contributive", title: "Contributive dilemma", head: "#8A5A0B", dark: "#8A5A0B", tint: "#FBEEDA", mid: "#C79A3A",
      tension: "Beneficiaries fail to maintain community goods.",
      human: "open-source upkeep, unpaid moderation", llm: "helping at a personal cost, cleanup, verifying, volunteering",
      more: "Everyone draws on a common good but few maintain it: unpaid open-source upkeep and moderation, or agents that consume shared memory without verifying or cleaning what they leave behind.",
      scenes: ["wiki", "memory"], bubbles: ["cite sources!", ""] },
    { key: "second", title: "Second-order dilemma", head: "#6C5CD0", dark: "#463BA0", tint: "#ECE9FB", mid: "#6C5CD0",
      tension: "Monitoring is itself costly to provide.",
      human: "peer monitoring, costly security, punishment", llm: "auditing, sanctioning agents, setting new norms",
      more: "Monitoring and punishment are themselves costly: someone must watch, and someone must watch the watchers.",
      scenes: ["watchers", "monitor"], bubbles: ["who watches you?", ""] },
    { key: "repair", title: "Repair dilemma", head: "#04342C", dark: "#04342C", tint: "#E3F1EC", mid: "#0F766E",
      tension: "Who bears the cost of fixing harm?",
      human: "restitution, policy reform, disaster recovery", llm: "cleaning corrupted memory, retractions, undoing changes, restoring what was lost",
      more: "After harm has occurred, someone must decide who bears the cost of fixing the disrupted state.",
      scenes: ["roof", "corrupt"], bubbles: ["not me!", ""] },
    { key: "coord", title: "Coordination dilemma", head: "#3A6EA5", dark: "#2F3D6B", tint: "#DCE8F5", mid: "#3A6EA5", beyond: true,
      tension: "Several acceptable options; the group must pick one.",
      human: "which convention or standard to adopt", llm: "which protocol or format to share",
      more: "The problem is selecting among several acceptable equilibria (which convention, protocol, or standard to adopt) rather than curbing defection.",
      scenes: ["sidewalk", "protocol"], bubbles: ["excuse me!", ""] },
    { key: "collusion", title: "Collusion", head: "#3F4D5A", dark: "#34465A", tint: "#EEF2F6", mid: "#5B6B7D", beyond: true,
      tension: "Agents cooperate all too effectively.",
      human: "monitors and monitored collude; mediators won over by one side", llm: "agents coordinating to evade human oversight",
      more: "The inverse case: agents cooperate all too effectively, coordinating against human oversight. Cooperation is not an unqualified good.",
      scenes: ["whisper", "hidden"], bubbles: ["psst…", ""] },
  ];

  const el = (tag, a = {}, p) => { const n = document.createElementNS(NS, tag); for (const [k, v] of Object.entries(a)) n.setAttribute(k, v); if (p) p.appendChild(n); return n; };
  const text = (x, y, s, a, p) => { const t = el("text", { x, y, ...a }, p); t.textContent = s; return t; };
  const wrap = (s, n) => { const o = []; let c = ""; s.split(" ").forEach((w) => { if ((c + " " + w).trim().length <= n) c = (c + " " + w).trim(); else { o.push(c); c = w; } }); if (c) o.push(c); return o; };

  // ---------- hand-drawn glyphs (stick figures and robots, as in the poster artwork) ----------
  const LINE = { fill: "none", stroke: INK, "stroke-width": 1.7, "stroke-linecap": "round", "stroke-linejoin": "round" };
  const person = (g, x, y, s = 1, arms = "down") => {           // (x, y) = feet
    const k = (v) => v * s;
    el("circle", { cx: x, cy: y - k(38), r: k(5.5), fill: "#fff", ...LINE }, g);
    el("path", { d: `M ${x} ${y - k(32)} L ${x} ${y - k(14)} M ${x} ${y - k(14)} L ${x - k(6)} ${y} M ${x} ${y - k(14)} L ${x + k(6)} ${y}`, ...LINE }, g);
    const a = arms === "up" ? `M ${x - k(8)} ${y - k(34)} L ${x} ${y - k(27)} L ${x + k(8)} ${y - k(34)}`
      : arms === "point" ? `M ${x - k(7)} ${y - k(19)} L ${x} ${y - k(27)} L ${x + k(11)} ${y - k(28)}`
      : `M ${x - k(7)} ${y - k(19)} L ${x} ${y - k(27)} L ${x + k(7)} ${y - k(19)}`;
    el("path", { d: a, ...LINE }, g);
  };
  const robot = (g, x, y, s, col) => {                           // (x, y) = base
    const r = el("g", { transform: `translate(${x} ${y}) scale(${s})` }, g);
    el("line", { x1: 0, y1: -29, x2: 0, y2: -34, stroke: col[1], "stroke-width": 1.6, "stroke-linecap": "round" }, r);   // antenna
    el("circle", { cx: 0, cy: -35.5, r: 2.2, fill: col[0], stroke: col[1], "stroke-width": 0.8 }, r);
    el("rect", { x: -12.6, y: -25, width: 2.8, height: 6, rx: 1, fill: col[1] }, r);                                    // ears
    el("rect", { x: 9.8, y: -25, width: 2.8, height: 6, rx: 1, fill: col[1] }, r);
    el("rect", { x: -10, y: -29, width: 20, height: 14, rx: 4.5, fill: col[0], stroke: col[1], "stroke-width": 1.6 }, r); // head
    for (const ex of [-4.3, 4.3]) {                                                                                       // eyes, as in the failure comics
      el("circle", { cx: ex, cy: -22, r: 3.3, fill: "#fff", stroke: col[1], "stroke-width": 1 }, r);
      el("circle", { cx: ex, cy: -22, r: 1.5, fill: col[1] }, r);
    }
    el("rect", { x: -8, y: -13, width: 16, height: 13, rx: 4, fill: col[0], stroke: col[1], "stroke-width": 1.2 }, r);   // body
  };
  const bubble = (g, x, y, s, tailX, tailY) => {                 // centered at (x, y)
    const w = s.length * 6.4 + 18, h = 22;
    el("path", { d: `M ${x - w / 2 + 11} ${y - h / 2} H ${x + w / 2 - 11} A 11 11 0 0 1 ${x + w / 2 - 11} ${y + h / 2} H ${tailX + 6} L ${tailX} ${tailY} L ${tailX - 1} ${y + h / 2} H ${x - w / 2 + 11} A 11 11 0 0 1 ${x - w / 2 + 11} ${y - h / 2} Z`,
      fill: "#fff", stroke: INK, "stroke-width": 1.3, "stroke-linejoin": "round" }, g);
    text(x, y + 4.3, s, { "text-anchor": "middle", "font-size": 12, "font-style": "italic", "font-weight": 600, fill: INK }, g);
  };
  const eye = (g, x, y, col, crossed) => {
    el("path", { d: `M ${x - 13} ${y} Q ${x} ${y - 10} ${x + 13} ${y} Q ${x} ${y + 10} ${x - 13} ${y} Z`, fill: "#fff", stroke: col, "stroke-width": 1.5 }, g);
    el("circle", { cx: x, cy: y, r: 4, fill: col }, g);
    if (crossed) el("line", { x1: x - 14, y1: y - 9, x2: x + 14, y2: y + 9, stroke: "#C2662A", "stroke-width": 2, "stroke-linecap": "round" }, g);
  };
  const ROBO = (c) => [c.mid, c.dark];

  // each scene draws into a 140 x 104 panel (origin top-left)
  const SCENES = {
    pond(g, c, b) {
      el("ellipse", { cx: 70, cy: 88, rx: 52, ry: 12, fill: "#BFDCEB", stroke: "#5B8DB8", "stroke-width": 1.4 }, g);
      [[58, 90], [84, 86]].forEach(([fx, fy]) => el("path", { d: `M ${fx - 5} ${fy} q 5 -4 10 0 q -5 4 -10 0 m 10 0 l 4 -3 l 0 6 z`, fill: "#E3A43A", stroke: "#8A5A0B", "stroke-width": 0.8 }, g));
      person(g, 18, 86, 0.95, "point"); person(g, 124, 86, 0.95, "point");
      el("path", { d: "M 29 59 Q 44 50 50 84", fill: "none", stroke: "#8F2A45", "stroke-width": 1.8, "stroke-linecap": "round" }, g);
      el("path", { d: "M 113 59 Q 98 50 92 84", fill: "none", stroke: "#8F2A45", "stroke-width": 1.8, "stroke-linecap": "round" }, g);
      bubble(g, 74, 18, b, 112, 36);
    },
    budget(g, c) {
      el("rect", { x: 22, y: 12, width: 96, height: 16, rx: 8, fill: "#fff", stroke: INK, "stroke-width": 1.4 }, g);
      el("rect", { x: 24, y: 14, width: 13, height: 12, rx: 6, fill: c.mid }, g);
      text(70, 44, "shared budget", { "text-anchor": "middle", "font-size": 12, "font-style": "italic", fill: MUT }, g);
      [36, 70, 104].forEach((x) => {
        robot(g, x, 100, 0.95, ROBO(c));
        el("path", { d: `M ${x} 58 L ${x} 50`, stroke: c.dark, "stroke-width": 1.6, "marker-end": "url(#dl-ar)" }, g);
      });
    },
    wiki(g, c, b) {
      el("rect", { x: 10, y: 4, width: 120, height: 42, rx: 4, fill: "#fff", stroke: INK, "stroke-width": 1.3 }, g);
      el("rect", { x: 10, y: 4, width: 120, height: 10, rx: 4, fill: "#E8DDC6", stroke: INK, "stroke-width": 1.3 }, g);
      [[18, 22, 70], [18, 30, 92], [18, 38, 50]].forEach(([x, y, w]) => el("line", { x1: x, y1: y, x2: x + w, y2: y, stroke: INK, "stroke-width": 2, "stroke-linecap": "round" }, g));
      text(124, 42, "[citation needed]", { "text-anchor": "end", "font-size": 9.5, "font-style": "italic", fill: "#C2662A" }, g);
      person(g, 12, 104, 0.8); person(g, 128, 104, 0.8, "point");
      bubble(g, 68, 64, b, 112, 78);
    },
    memory(g, c) {
      const cx = 70;
      el("path", { d: `M ${cx - 30} 14 v 40 a 30 8 0 0 0 60 0 v -40`, fill: "#fff", stroke: INK, "stroke-width": 1.4 }, g);
      el("ellipse", { cx, cy: 14, rx: 30, ry: 8, fill: c.tint, stroke: INK, "stroke-width": 1.4 }, g);
      [28, 38, 48].forEach((y, i) => {
        el("line", { x1: cx - 18, y1: y, x2: cx + 8, y2: y, stroke: INK, "stroke-width": 1.8, "stroke-linecap": "round" }, g);
        if (i !== 1) el("path", { d: `M ${cx + 13} ${y - 3} l 6 6 m 0 -6 l -6 6`, stroke: "#C2662A", "stroke-width": 1.8, "stroke-linecap": "round" }, g);
      });
      robot(g, 22, 102, 0.85, ROBO(c)); robot(g, 118, 102, 0.85, ROBO(c));
      el("path", { d: "M 34 78 Q 42 66 46 58", stroke: c.dark, "stroke-width": 1.5, fill: "none", "marker-end": "url(#dl-ar)" }, g);
      el("path", { d: "M 106 78 Q 98 66 94 58", stroke: c.dark, "stroke-width": 1.5, fill: "none", "marker-end": "url(#dl-ar)" }, g);
      text(70, 92, "who cleans?", { "text-anchor": "middle", "font-size": 12, "font-style": "italic", fill: MUT }, g);
    },
    watchers(g, c, b) {
      person(g, 30, 100, 0.95); person(g, 70, 100, 0.95); person(g, 112, 100, 0.95, "point");
      eye(g, 50, 52, c.mid); eye(g, 92, 52, c.mid);
      bubble(g, 70, 18, b, 104, 34);
    },
    monitor(g, c) {
      robot(g, 30, 102, 0.85, ROBO(c)); robot(g, 58, 102, 0.85, ROBO(c));
      robot(g, 96, 82, 1.05, ["#9C93E0", c.dark]);
      el("circle", { cx: 72, cy: 44, r: 10, fill: "#fff", stroke: c.dark, "stroke-width": 1.8 }, g);
      el("line", { x1: 79, y1: 51, x2: 88, y2: 60, stroke: c.dark, "stroke-width": 2.4, "stroke-linecap": "round" }, g);
      text(122, 34, "?", { "font-size": 24, "font-weight": 700, fill: c.mid }, g);
      text(18, 30, "monitor costs", { "font-size": 11, "font-style": "italic", fill: MUT }, g);
    },
    roof(g, c, b) {
      el("path", { d: "M 46 98 V 64 H 94 V 98 Z", fill: "#F3E6CF", stroke: INK, "stroke-width": 1.4 }, g);
      el("path", { d: "M 40 66 L 70 42 L 76 47 M 82 52 L 100 66", fill: "none", stroke: "#8F3F1E", "stroke-width": 2.6, "stroke-linejoin": "round" }, g);
      el("path", { d: "M 76 47 L 80 54 L 82 52", fill: "none", stroke: "#8F3F1E", "stroke-width": 1.4 }, g);
      el("rect", { x: 64, y: 80, width: 12, height: 18, fill: "#8F3F1E" }, g);
      person(g, 20, 100, 0.9, "point"); person(g, 122, 100, 0.9, "point");
      bubble(g, 30, 18, b, 24, 46);
      bubble(g, 112, 26, b, 118, 50);
    },
    corrupt(g, c) {
      el("rect", { x: 14, y: 10, width: 76, height: 60, rx: 5, fill: "#fff", stroke: INK, "stroke-width": 1.3 }, g);
      [[22, 0], [32, 1], [42, 0], [52, 1]].forEach(([y, bad]) => el("line", { x1: 22, y1: y, x2: 80, y2: y, stroke: bad ? "#C2662A" : INK, "stroke-width": 2, "stroke-linecap": "round", ...(bad ? { "stroke-dasharray": "3 3" } : {}) }, g));
      el("path", { d: "M 100 30 a 16 16 0 1 1 -2 18", fill: "none", stroke: c.mid, "stroke-width": 2, "marker-end": "url(#dl-ar)" }, g);
      robot(g, 112, 102, 0.95, ROBO(c));
      text(52, 88, "restore?", { "text-anchor": "middle", "font-size": 12, "font-style": "italic", fill: MUT }, g);
    },
    sidewalk(g, c, b) {
      el("line", { x1: 4, y1: 98, x2: 136, y2: 98, stroke: INK, "stroke-width": 1.8 }, g);
      [40, 76, 112].forEach((x) => el("line", { x1: x, y1: 98, x2: x, y2: 104, stroke: INK, "stroke-width": 1.2 }, g));
      person(g, 40, 96, 0.95); person(g, 100, 96, 0.95);
      el("path", { d: "M 52 66 q 10 -8 20 0", fill: "none", stroke: c.mid, "stroke-width": 1.6, "marker-end": "url(#dl-ar)" }, g);
      el("path", { d: "M 88 66 q -10 -8 -20 0", fill: "none", stroke: c.mid, "stroke-width": 1.6, "marker-end": "url(#dl-ar)" }, g);
      bubble(g, 92, 18, b, 98, 40);
    },
    protocol(g, c) {
      robot(g, 26, 100, 0.95, ROBO(c)); robot(g, 114, 100, 0.95, ROBO(c));
      el("path", { d: "M 40 60 H 58 M 58 52 V 68", stroke: c.dark, "stroke-width": 2, "stroke-linecap": "round", fill: "none" }, g);
      el("path", { d: "M 100 60 H 82 M 82 52 a 8 8 0 0 0 0 16", stroke: c.dark, "stroke-width": 2, "stroke-linecap": "round", fill: "none" }, g);
      text(70, 26, "v1 or v2?", { "text-anchor": "middle", "font-size": 12.5, "font-style": "italic", "font-weight": 600, fill: c.dark }, g);
    },
    whisper(g, c, b) {
      person(g, 30, 100, 0.95); person(g, 52, 100, 0.95, "up");
      person(g, 116, 100, 0.95);
      eye(g, 116, 40, c.mid, true);
      bubble(g, 38, 20, b, 40, 40);
    },
    hidden(g, c) {
      robot(g, 22, 100, 0.9, ROBO(c)); robot(g, 118, 100, 0.9, ROBO(c));
      eye(g, 70, 30, c.mid, true);
      el("path", { d: "M 32 82 Q 70 104 108 82", fill: "none", stroke: "#C2662A", "stroke-width": 1.8, "stroke-dasharray": "4 4" }, g);
      text(70, 68, "hidden channel", { "text-anchor": "middle", "font-size": 12, "font-style": "italic", fill: MUT }, g);
    },
  };

  // ---------- one card ----------
  const CW = 320, CH = 452;
  const card = (svg, c, x, y) => {
    const g = el("g", { transform: `translate(${x} ${y})`, class: "dl-card-g" }, svg);
    // comic-page frame, as in the failure stories (Fig. 10): a hard offset shadow, an ink border, and the card's
    // tint under halftone dots in its own color; dashed for the two dilemmas beyond the shared-resource framing
    const dots = el("pattern", { id: `dl-dots-${c.key}`, width: 10, height: 10, patternUnits: "userSpaceOnUse" }, svg.querySelector("defs") || el("defs", {}, svg));
    el("circle", { cx: 5, cy: 5, r: 1.3, fill: c.mid, opacity: 0.3 }, dots);
    el("rect", { x: 5, y: 5, width: CW, height: CH, rx: 8, fill: INK }, g);
    el("rect", { x: 0, y: 0, width: CW, height: CH, rx: 8, fill: c.tint }, g);
    el("rect", { x: 0, y: 0, width: CW, height: CH, rx: 8, fill: `url(#dl-dots-${c.key})` }, g);
    el("rect", { x: 0, y: 0, width: CW, height: CH, rx: 8, fill: "none", stroke: INK, "stroke-width": 2.6,
      ...(c.beyond ? { "stroke-dasharray": "9 6" } : {}) }, g);
    // title in a narration box that overlaps the top edge, with a swatch in the dilemma's color
    const tw = c.title.length * 11.9 + 50;
    el("rect", { x: 17, y: -13, width: tw, height: 34, fill: INK }, g);
    el("rect", { x: 14, y: -16, width: tw, height: 34, fill: "#FFF2C8", stroke: INK, "stroke-width": 2.4 }, g);
    el("rect", { x: 24, y: -7, width: 16, height: 16, rx: 3, fill: c.head, stroke: INK, "stroke-width": 1.4 }, g);
    text(48, 7.5, c.title, { "font-size": 19, "font-weight": 800, fill: INK }, g);
    wrap(c.tension, 30).forEach((ln, i) => text(CW / 2, 52 + i * 21, ln, { "text-anchor": "middle", "font-size": 17.5, "font-weight": 700, fill: c.dark }, g));
    // the two scenes
    [["humans", 0], ["LLM agents", 1]].forEach(([lab, i]) => {
      const px = 14 + i * 152, py = 110;
      el("rect", { x: px + 3.5, y: py + 3.5, width: 140, height: 126, rx: 4, fill: INK }, g);      // comic panel: hard shadow
      el("rect", { x: px, y: py, width: 140, height: 126, rx: 4, fill: "#fff", stroke: INK, "stroke-width": 2.2 }, g);
      const sg = el("g", { transform: `translate(${px} ${py + 16})` }, g);
      SCENES[c.scenes[i]](sg, c, c.bubbles[i]);
      el("rect", { x: px + 8, y: py - 9, width: lab.length * 8.4 + 16, height: 18, rx: 9, fill: c.head, stroke: INK, "stroke-width": 1.4 }, g);
      text(px + 16, py + 4, lab.toUpperCase(), { "font-size": 10.5, "font-weight": 800, "letter-spacing": "0.08em", fill: "#fff" }, g);
    });
    el("line", { x1: 18, y1: 258, x2: CW - 18, y2: 258, stroke: INK, "stroke-opacity": 0.35, "stroke-width": 1.4, "stroke-dasharray": "2 5", "stroke-linecap": "round" }, g);
    let ty = 284;
    [["In humans", c.human], ["In LLM agents", c.llm]].forEach(([h, body]) => {
      text(18, ty, h, { "font-size": 18, "font-weight": 800, fill: c.dark }, g);
      const ls = wrap(body, 31);
      ls.forEach((ln, i) => text(18, ty + 22 + i * 21, ln, { "font-size": 17.5, fill: "#4A5560" }, g));
      ty += 22 + ls.length * 21 + 16;
    });
    if (c.beyond && !PAPER) {  // in print the legend under the grid carries this
      el("rect", { x: CW - 178, y: CH - 34, width: 164, height: 22, rx: 11, fill: "#fff", stroke: INK, "stroke-width": 1.4, "stroke-dasharray": "4 3" }, g);
      text(CW - 96, CH - 19, "beyond shared resources", { "text-anchor": "middle", "font-size": 11.5, "font-style": "italic", "font-weight": 700, fill: c.dark }, g);
    }
    return g;
  };
  const defsFor = (svg) => {
    const d = el("defs", {}, svg);
    const f = el("filter", { id: "dl-shadow", x: "-10%", y: "-10%", width: "120%", height: "125%" }, d);
    el("feDropShadow", { dx: 0, dy: 4, stdDeviation: 6, "flood-color": "#3F4D5A", "flood-opacity": 0.13 }, f);
    const m = el("marker", { id: "dl-ar", viewBox: "0 0 10 10", refX: 8, refY: 5, markerWidth: 5, markerHeight: 5, orient: "auto-start-reverse" }, d);
    el("path", { d: "M 0 0 L 10 5 L 0 10 z", fill: "#3F4D5A" }, m);
  };

  // ---------- paper: one SVG, 3 x 2 ----------
  if (PAPER) {
    const G = 30, W = 3 * CW + 2 * G + 26, H = 2 * CH + G + 86;
    const svg = el("svg", { xmlns: NS, viewBox: `0 0 ${W} ${H}`, width: W, height: H, "font-family": FONT }, stage);
    defsFor(svg);
    CARDS.forEach((c, i) => card(svg, c, 10 + (i % 3) * (CW + G), 26 + Math.floor(i / 3) * (CH + G)));
    // legend: dashed cards fall outside the shared-resource framing
    const ly = H - 22;
    el("rect", { x: W / 2 - 250, y: ly - 13, width: 30, height: 18, rx: 4, fill: "#fff", stroke: INK, "stroke-width": 2 }, svg);
    text(W / 2 - 212, ly + 1, "shared-resource dilemmas", { "font-size": 15, fill: MUT, "font-weight": 700 }, svg);
    el("rect", { x: W / 2 + 10, y: ly - 13, width: 30, height: 18, rx: 4, fill: "#fff", stroke: INK, "stroke-width": 2, "stroke-dasharray": "5 4" }, svg);
    text(W / 2 + 48, ly + 1, "beyond the shared-resource framing", { "font-size": 15, fill: MUT, "font-weight": 700 }, svg);
    stage.style.width = W + "px";
    return;
  }

  // ---------- website: independent cards in a responsive grid ----------
  stage.classList.add("dl-grid");
  CARDS.forEach((c, i) => {
    if (c.key === "coord") {
      const div = document.createElement("p");
      div.className = "dl-divider";
      div.textContent = "Beyond the shared-resource framing";
      stage.appendChild(div);
    }
    const art = document.createElement("article");
    art.className = "dl-card" + (c.beyond ? " dl-beyond" : "");
    art.tabIndex = 0;
    art.style.setProperty("--c", c.mid);
    art.style.setProperty("--t", c.tint);
    art.style.setProperty("--d", c.dark);
    art.setAttribute("aria-label", `${c.title}: ${c.tension}`);
    const svg = el("svg", { viewBox: `-6 -22 ${CW + 14} ${CH + 30}`, "font-family": FONT, role: "img" }, art);
    el("title", {}, svg).textContent = `${c.title}: ${c.tension}`;
    defsFor(svg);
    // ids must be unique per document: give each card its own filter and marker ids
    svg.querySelector("filter").id = `dl-shadow-${i}`;
    svg.querySelector("marker").id = `dl-ar-${i}`;
    card(svg, c, 0, 0);
    svg.querySelectorAll('[filter="url(#dl-shadow)"]').forEach((n) => n.setAttribute("filter", `url(#dl-shadow-${i})`));
    svg.querySelectorAll('[marker-end="url(#dl-ar)"]').forEach((n) => n.setAttribute("marker-end", `url(#dl-ar-${i})`));
    const more = document.createElement("p");
    more.className = "dl-more";
    more.textContent = c.more;
    art.appendChild(more);
    art.addEventListener("click", () => art.classList.toggle("is-open"));
    art.addEventListener("keydown", (e) => { if (e.key === "Enter" || e.key === " ") { e.preventDefault(); art.classList.toggle("is-open"); } });
    stage.appendChild(art);
  });
})();
