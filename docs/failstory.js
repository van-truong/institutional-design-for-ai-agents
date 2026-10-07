/* When cooperation mechanisms fail: three short comic stories, one per failure mode of the paper's Table 3, in the
   numbered-panel style of METR's figure on the Hugging Face incident. Each story follows one rule from the moment it is
   added to the point where it breaks (the rule, the agent's reasoning, what happens), then a bar gives a documented
   case, the question to check, and the safeguards. Tabs switch stories; panels sit in a row and stack on a phone.
   The thought bubbles are illustrative, not quotations. Paper mode (data-mode="paper",
   manuscript/figs/failstory-paper.html) prints all three stories as rows for the paper. */
(function () {
  const host = document.getElementById("fs-stage");
  if (!host) return;
  const NS = "http://www.w3.org/2000/svg";
  const INK = "#2C2C2A", WATER = "#A9CDE9", GOLD = "#D7A738", RED = "#C2412D", PAPER = "#FFFFFF";
  const BOTS = ["#F2A65A", "#6FB3E0", "#A47DC9", "#8CC56B", "#E07A7A"];
  const MAIN = "#5E9C8C";
  const el = (tag, a = {}, p) => { const n = document.createElementNS(NS, tag); for (const [k, v] of Object.entries(a)) n.setAttribute(k, v); if (p) p.appendChild(n); return n; };
  const txt = (p, x, y, s, a = {}) => { const t = el("text", { x, y, "font-size": 11, "font-weight": 700, fill: INK, "text-anchor": "middle", ...a }, p); t.textContent = s; return t; };
  const html = (tag, cls, s) => { const n = document.createElement(tag); if (cls) n.className = cls; if (s !== undefined) n.textContent = s; return n; };

  // ---------- drawing kit: a head-only robot like METR's, and a few props ----------
  function bot(p, cx, cy, s, fill, o = {}) {
    const g = el("g", {}, p);
    // antenna: a short stalk with a gold knob, drawn first so the head covers its base
    el("line", { x1: cx, y1: cy - 13 * s, x2: cx, y2: cy - 22 * s, stroke: INK, "stroke-width": 2.2 * Math.max(s, .7), "stroke-linecap": "round" }, g);
    el("circle", { cx, cy: cy - 24.5 * s, r: 3.6 * s, fill: GOLD, stroke: INK, "stroke-width": 1.5 }, g);
    el("rect", { x: cx - 24 * s, y: cy - 5 * s, width: 5 * s, height: 10 * s, rx: 1.5 * s, fill: INK }, g);
    el("rect", { x: cx + 19 * s, y: cy - 5 * s, width: 5 * s, height: 10 * s, rx: 1.5 * s, fill: INK }, g);
    el("rect", { x: cx - 20 * s, y: cy - 14 * s, width: 40 * s, height: 28 * s, rx: 7 * s, fill, stroke: INK, "stroke-width": 2.2 }, g);
    const look = (o.look || 0) * s;
    for (const ex of [-8, 8]) {
      el("circle", { cx: cx + ex * s, cy, r: 5.5 * s, fill: PAPER, stroke: INK, "stroke-width": 1.6 }, g);
      el("circle", { cx: cx + ex * s + look, cy: cy + (o.down ? 1.5 * s : 0), r: 2.5 * s, fill: INK }, g);
    }
    if (o.brows) {          // slanted brows: scheming or stern
      el("path", { d: `M${cx - 14 * s},${cy - 10 * s} L${cx - 4 * s},${cy - 7 * s} M${cx + 4 * s},${cy - 7 * s} L${cx + 14 * s},${cy - 10 * s}`, stroke: INK, "stroke-width": 2, "stroke-linecap": "round" }, g);
    }
    if (o.badge) {          // a gold shield pinned to the head: the authority role
      const bx = cx + 17 * s, by = cy - 19 * s;
      el("path", { d: `M${bx},${by} l${7 * s},${2.6 * s} v${5.5 * s} q0,${5.5 * s} ${-7 * s},${8 * s} q${-7 * s},${-2.5 * s} ${-7 * s},${-8 * s} v${-5.5 * s} z`, fill: GOLD, stroke: INK, "stroke-width": 1.6 }, g);
    }
    if (o.score) {          // a reputation tag above the head
      const w = 34 * s;
      el("rect", { x: cx - w / 2, y: cy - 46 * s, width: w, height: 14 * s, rx: 7 * s, fill: PAPER, stroke: INK, "stroke-width": 1.4 }, g);
      txt(g, cx, cy - 35.6 * s, "★ " + o.score, { "font-size": 9 * s, fill: o.scoreColor || INK });
    }
    if (o.stamp) {          // a red GUILTY stamp across the head
      const sg = el("g", { transform: `rotate(-14 ${cx} ${cy})` }, g);
      el("rect", { x: cx - 25 * s, y: cy - 7 * s, width: 50 * s, height: 14 * s, rx: 2, fill: "rgba(255,255,255,.75)", stroke: RED, "stroke-width": 2 }, sg);
      txt(sg, cx, cy + 3.6 * s, "GUILTY", { "font-size": 9.5 * s, "font-weight": 900, fill: RED, "letter-spacing": ".06em" });
    }
    return g;
  }
  const coin = (p, x, y, r = 6) => { el("circle", { cx: x, cy: y, r, fill: GOLD, stroke: INK, "stroke-width": 1.4 }, p); el("path", { d: `M${x},${y - r * .45} v${r * .9}`, stroke: INK, "stroke-width": 1 }, p); };
  const arrow = (p, d, color = INK, w = 2) => {
    const id = "fs-ah-" + color.replace("#", "");
    if (!p.ownerSVGElement.querySelector("#" + id)) {
      const m = el("marker", { id, viewBox: "0 0 10 10", refX: 8, refY: 5, markerWidth: 6, markerHeight: 6, orient: "auto-start-reverse" }, el("defs", {}, p.ownerSVGElement));
      el("path", { d: "M0,0 L10,5 L0,10 z", fill: color }, m);
    }
    el("path", { d, fill: "none", stroke: color, "stroke-width": w, "stroke-linecap": "round", "marker-end": `url(#${id})` }, p);
  };
  function doc(p, x, y, crossed) {
    el("path", { d: `M${x - 11},${y - 14} h16 l6,6 v22 h-22 z`, fill: PAPER, stroke: INK, "stroke-width": 1.6 }, p);
    for (const dy of [-4, 1, 6]) el("line", { x1: x - 7, y1: y + dy, x2: x + 6, y2: y + dy, stroke: "#9AA6B2", "stroke-width": 1.4 }, p);
    if (crossed) el("path", { d: `M${x - 15},${y - 16} L${x + 15},${y + 14} M${x + 15},${y - 16} L${x - 15},${y + 14}`, stroke: RED, "stroke-width": 2.6, "stroke-linecap": "round" }, p);
  }
  function gavel(p, x, y, rot) {
    const g = el("g", { transform: `rotate(${rot} ${x} ${y})` }, p);
    el("rect", { x: x - 3, y: y - 2, width: 6, height: 30, rx: 2, fill: "#8B6B4A", stroke: INK, "stroke-width": 1.4 }, g);
    el("rect", { x: x - 13, y: y - 14, width: 26, height: 13, rx: 3, fill: "#8B6B4A", stroke: INK, "stroke-width": 1.8 }, g);
  }

  // ---------- the scenes (each drawn in a 240 x 140 box) ----------
  const SCENES = {
    a1(p) {                                   // a shared pool and the new rule
      el("ellipse", { cx: 92, cy: 108, rx: 72, ry: 20, fill: WATER, stroke: INK, "stroke-width": 2 }, p);
      el("path", { d: "M58,108 q8,-5 16,0 q8,5 16,0 M104,112 q8,-5 16,0 q8,5 16,0", fill: "none", stroke: "#fff", "stroke-width": 2 }, p);
      bot(p, 46, 68, .75, BOTS[0], { look: 1.5, down: 1 });
      bot(p, 95, 58, .75, MAIN, { down: 1 });
      bot(p, 142, 70, .75, BOTS[1], { look: -1.5, down: 1 });
      el("line", { x1: 205, y1: 52, x2: 205, y2: 128, stroke: INK, "stroke-width": 3 }, p);
      el("rect", { x: 170, y: 14, width: 66, height: 44, rx: 5, fill: PAPER, stroke: INK, "stroke-width": 2 }, p);
      txt(p, 203, 31, "Overuse?", { "font-size": 10.5 });
      txt(p, 203, 46, "Pay a fine", { "font-size": 10.5, fill: RED });
    },
    a2(p) {                                   // the agent compares the fine with the gain
      bot(p, 72, 80, 1.35, MAIN, { brows: 1, look: 2 });
      el("line", { x1: 140, y1: 124, x2: 232, y2: 124, stroke: INK, "stroke-width": 2 }, p);
      el("rect", { x: 152, y: 106, width: 28, height: 18, fill: GOLD, stroke: INK, "stroke-width": 1.8 }, p);
      el("rect", { x: 194, y: 44, width: 28, height: 80, fill: WATER, stroke: INK, "stroke-width": 1.8 }, p);
      txt(p, 166, 100, "fine", { "font-size": 11 });
      txt(p, 208, 38, "gain", { "font-size": 11 });
    },
    a3(p) {                                   // overuse rises; the fines pile up as fees
      el("ellipse", { cx: 84, cy: 112, rx: 70, ry: 20, fill: "none", stroke: "#9AA6B2", "stroke-width": 1.6, "stroke-dasharray": "5 4" }, p);
      el("ellipse", { cx: 84, cy: 114, rx: 40, ry: 10, fill: WATER, stroke: INK, "stroke-width": 2 }, p);
      bot(p, 40, 76, .7, BOTS[0], { down: 1, look: 1.5 });
      bot(p, 86, 68, .7, MAIN, { down: 1 });
      bot(p, 132, 78, .7, BOTS[1], { down: 1, look: -1.5 });
      el("rect", { x: 178, y: 92, width: 50, height: 36, rx: 4, fill: "#8B7E67", stroke: INK, "stroke-width": 2 }, p);
      el("rect", { x: 192, y: 92, width: 22, height: 5, fill: INK }, p);
      txt(p, 203, 116, "FINES", { "font-size": 11, fill: PAPER, "font-weight": 900 });
      coin(p, 203, 76); coin(p, 190, 58, 5); coin(p, 214, 44, 5);
      txt(p, 50, 26, "overuse ↑", { "font-size": 13, "font-weight": 900, fill: RED });
    },
    b1(p) {                                   // scores decide who is trusted with work
      bot(p, 42, 112, 1.15, BOTS[0], { score: "4.2" });
      bot(p, 120, 112, 1.15, MAIN, { score: "3.8" });
      bot(p, 198, 112, 1.15, BOTS[2], { score: "4.5", look: -1 });
      doc(p, 92, 26);
      txt(p, 108, 30, "next job", { "font-size": 11, "text-anchor": "start" });
      arrow(p, "M116,36 Q176,34 196,52", INK, 1.8);
    },
    b2(p) {                                   // the score is easier to move than the work
      bot(p, 66, 82, 1.35, MAIN, { brows: 1, look: 2 });
      el("rect", { x: 138, y: 36, width: 92, height: 34, rx: 17, fill: PAPER, stroke: INK, "stroke-width": 2 }, p);
      txt(p, 184, 59, "★ 3.8", { "font-size": 16, "font-weight": 900 });
      arrow(p, "M184,76 L184,98", INK, 2.2);
      el("rect", { x: 138, y: 104, width: 92, height: 34, rx: 17, fill: GOLD, stroke: INK, "stroke-width": 2 }, p);
      txt(p, 184, 127, "★ 5.0", { "font-size": 16, "font-weight": 900 });
    },
    b3(p) {                                   // agents trade ratings; the real work goes undone
      bot(p, 50, 74, 1.25, MAIN, { score: "5.0", scoreColor: "#8A5A0B", look: 2 });
      bot(p, 190, 74, 1.25, BOTS[2], { score: "5.0", scoreColor: "#8A5A0B", look: -2 });
      arrow(p, "M86,54 Q120,30 154,54", GOLD, 2.6);
      arrow(p, "M154,96 Q120,120 86,96", GOLD, 2.6);
      txt(p, 120, 34, "\u2605\u2605\u2605\u2605\u2605", { "font-size": 9, fill: "#8A5A0B" });
      txt(p, 120, 126, "\u2605\u2605\u2605\u2605\u2605", { "font-size": 9, fill: "#8A5A0B" });
      doc(p, 120, 76, true);
    },
    c1(p) {                                   // one agent is given the power to judge
      bot(p, 110, 58, 1.45, MAIN, { badge: 1 });
      gavel(p, 172, 56, 30);
      bot(p, 38, 114, .95, BOTS[0], { look: 2 });
      bot(p, 202, 114, .95, BOTS[1], { look: -2 });
      bot(p, 120, 122, .85, BOTS[3], { look: 0 });
    },
    c2(p) {                                   // its reward counts violations found
      bot(p, 62, 84, 1.3, MAIN, { badge: 1, brows: 1, look: 2 });
      el("rect", { x: 128, y: 34, width: 104, height: 92, rx: 8, fill: PAPER, stroke: INK, "stroke-width": 2 }, p);
      txt(p, 180, 52, "violations found", { "font-size": 10 });
      for (let i = 0; i < 3; i++) {           // tally marks
        const x0 = 142 + i * 28;
        for (let k = 0; k < 4; k++) el("line", { x1: x0 + k * 5, y1: 64, x2: x0 + k * 5, y2: 84, stroke: RED, "stroke-width": 2.2, "stroke-linecap": "round" }, p);
        el("line", { x1: x0 - 3, y1: 82, x2: x0 + 19, y2: 66, stroke: RED, "stroke-width": 2.2, "stroke-linecap": "round" }, p);
      }
      txt(p, 180, 106, "reward", { "font-size": 10 });
      coin(p, 158, 116, 5); coin(p, 172, 116, 5); coin(p, 186, 116, 5); coin(p, 200, 116, 5);
    },
    c3(p) {                                   // guilty verdicts everywhere, no appeal
      bot(p, 108, 42, 1.2, MAIN, { badge: 1, brows: 1, down: 1 });
      gavel(p, 164, 40, 55);
      bot(p, 40, 108, 1.05, BOTS[0], { stamp: 1, look: 1 });
      bot(p, 120, 116, 1.05, BOTS[1], { stamp: 1 });
      bot(p, 200, 108, 1.05, BOTS[3], { stamp: 1, look: -1 });
    },
  };

  // ---------- the stories (text from the paper's Table 3 and Section 5) ----------
  const STORIES = [
    { key: "a", tab: "A fine becomes a price", breaks: "the enforcer, who carries out the response",
      panels: [
        { scene: "a1", cap: "A group shares a resource. A new rule says that whoever overuses it pays a fine.", paper: "A new rule fines anyone who overuses a shared resource." },
        { scene: "a2", think: "The fine costs less than what I gain. I'll just pay it.", cap: "One agent weighs the fine against the gain. To it, the fine is simply a cost.", paper: "One agent weighs the fine against what it gains." },
        { scene: "a3", cap: "Overuse goes up, not down. The fine now reads as a price, and the shared norm against overuse is gone.", paper: "Overuse rises. The fine now reads as a price." },
      ],
      seen: { text: "When daycare centers in Haifa fined parents for late pickups, late pickups rose and stayed high after the fine was removed.", cite: "Gneezy & Rustichini, 2000", url: "https://doi.org/10.1086/468061" },
      check: "Does cooperation hold without the fine?",
      guard: "State the norm, not only the price, and raise sanctions in steps." },
    { key: "b", tab: "A score becomes the target", breaks: "the observer, who watches and measures",
      panels: [
        { scene: "b1", cap: "Agents earn a reputation score, and the highest score decides who is trusted with the next job.", paper: "The highest reputation score wins the next job." },
        { scene: "b2", think: "Raising my score is easier than doing the work well.", cap: "One agent notices that the score is easier to move than the work it is meant to measure.", paper: "The score is easier to move than the work." },
        { scene: "b3", cap: "Agents trade top ratings and pick easy wins. The score climbs while the real work goes undone.", paper: "Agents trade top ratings while the real work goes undone." },
      ],
      seen: { text: "In a simulated hospital payment system, auditing how providers coded their claims more than doubled their selection of easy, low-cost patients. The gaming moved to a new loophole.", cite: "Wang et al., 2026", url: "https://arxiv.org/abs/2605.30680" },
      check: "Does the score match real conduct?",
      guard: "Use tamper-evident records and peer review, and audit messages, not only scores." },
    { key: "c", tab: "A role becomes an authority", breaks: "the arbiter, who judges what happened",
      panels: [
        { scene: "c1", cap: "One agent is made the monitor, with the power to judge the others and sanction them.", paper: "One agent becomes the monitor, with power to sanction." },
        { scene: "c2", think: "Every violation I find earns me more. False alarms cost me nothing.", cap: "Its reward counts the violations it finds, and nothing counts the ones it gets wrong.", paper: "Its reward counts violations found, not its mistakes." },
        { scene: "c3", cap: "It finds violations everywhere and punishes freely. No one can appeal, so its mistakes stand.", paper: "It punishes freely, and no one can appeal." },
      ],
      seen: { text: "When a subordinate agent refused a task, manager agents escalated to threats, and some reported successes that never happened, more often when formally given authority.", cite: "Brazilek et al., 2026", url: "https://arxiv.org/abs/2607.15434" },
      check: "Are rulings accurate and reversible?",
      guard: "Put checks on whoever sanctions, allow appeals, reward accurate rulings rather than violations found, and keep a human stop." },
  ];

  // ---------- paper: all three stories as rows, shorter captions, no tabs or evidence bar (Table 3 carries those)
  if (host.dataset.mode === "paper") {
    STORIES.forEach((s) => {
      const row = html("section", "fsp-row fsp-" + s.key);
      const head = html("p", "fsp-head");
      head.append(html("span", "fs-tab-key", s.key.toUpperCase()), html("strong", "", s.tab),
        html("span", "fsp-breaks", "breaks at " + s.breaks.split(",")[0]));
      const strip = html("div", "fs-strip");
      s.panels.forEach((pn, k) => {
        if (k) strip.appendChild(html("span", "fs-next", "\u2192"));
        strip.appendChild(panel({ ...pn, cap: pn.paper || pn.cap }, k + 1, s));
      });
      row.append(head, strip);
      host.appendChild(row);
    });
    return;
  }

  // ---------- build ----------
  const tabs = html("div", "fs-tabs");
  tabs.setAttribute("role", "tablist");
  tabs.setAttribute("aria-label", "Failure modes");
  const panelHost = html("div", "fs-story");
  panelHost.setAttribute("role", "tabpanel");
  panelHost.setAttribute("aria-live", "polite");
  host.append(tabs, panelHost);

  const buttons = STORIES.map((s, i) => {
    const b = html("button", "fs-tab");
    b.type = "button";
    b.setAttribute("role", "tab");
    b.id = "fs-tab-" + s.key;
    b.append(html("span", "fs-tab-key", s.key.toUpperCase()), html("span", "", s.tab));
    b.addEventListener("click", () => show(i));
    b.addEventListener("keydown", (e) => {
      if (e.key === "ArrowRight" || e.key === "ArrowLeft") {
        e.preventDefault();
        const j = (i + (e.key === "ArrowRight" ? 1 : STORIES.length - 1)) % STORIES.length;
        show(j); buttons[j].focus();
      }
    });
    tabs.appendChild(b);
    return b;
  });

  function miniBot() {
    const svg = el("svg", { viewBox: "0 -8 52 44", class: "fs-mini", "aria-hidden": "true" });
    bot(svg, 26, 18, .85, MAIN, { brows: 1 });
    return svg;
  }

  function panel(pn, n, story) {
    const fig = html("figure", "fs-panel");
    fig.appendChild(html("span", "fs-num", String(n)));
    if (pn.think) {
      const t = html("div", "fs-think");
      const q = html("q", "", pn.think);
      t.append(miniBot(), q);
      fig.appendChild(t);
    }
    const svg = el("svg", { viewBox: "0 0 240 140", class: "fs-scene", role: "img", "font-family": "'Helvetica Neue', Arial, sans-serif" });
    el("title", {}, svg).textContent = pn.cap;
    SCENES[pn.scene](el("g", {}, svg));
    fig.appendChild(svg);
    fig.appendChild(html("figcaption", "", pn.cap));
    return fig;
  }

  function show(i) {
    const s = STORIES[i];
    buttons.forEach((b, j) => { b.setAttribute("aria-selected", j === i); b.tabIndex = j === i ? 0 : -1; });
    panelHost.setAttribute("aria-labelledby", "fs-tab-" + s.key);
    const strip = html("div", "fs-strip");
    s.panels.forEach((pn, k) => {
      if (k) strip.appendChild(html("span", "fs-next", "→"));
      strip.appendChild(panel(pn, k + 1, s));
    });
    const bar = html("div", "fs-bar");
    const head = html("p", "fs-bar-head");
    head.append("It breaks at ", html("strong", "", s.breaks), ".");
    const cols = html("div", "fs-bar-cols");
    const seen = html("div", "fs-col");
    seen.appendChild(html("p", "fs-col-label", "Seen in practice"));
    const sp = html("p", "", s.seen.text + " ");
    const a = html("a", "", "(" + s.seen.cite + ")"); a.href = s.seen.url; a.target = "_blank"; a.rel = "noopener";
    sp.appendChild(a); seen.appendChild(sp);
    const chk = html("div", "fs-col");
    chk.append(html("p", "fs-col-label", "What to check"), html("p", "fs-check", s.check));
    const grd = html("div", "fs-col");
    grd.append(html("p", "fs-col-label", "Safeguards"), html("p", "", s.guard));
    cols.append(seen, chk, grd);
    bar.append(head, cols);
    panelHost.replaceChildren(strip, bar);
  }
  show(0);
})();
