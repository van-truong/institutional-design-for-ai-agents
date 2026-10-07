/* Familiar commons vs. artificial commons (problem section). Three human commons from the poster artwork, each
   paired with the artificial commons that LLM agents share, plus a "shared pool" sketch adapted from the
   sanctions poster: five agents of different model families around one resource, with no institution yet.
   Pairs sit side by side and stack on a phone; hover, tap, or tab to a pair to emphasize it. */
(function () {
  const stage = document.getElementById("commons-stage");
  if (!stage) return;

  const NS = "http://www.w3.org/2000/svg";
  const FONT = "'Helvetica Neue', Helvetica, Arial, sans-serif";
  const INK = "#2C2C2A", MUT = "#6B7787";
  const HUM = { mid: "#C79A3A", dark: "#8A5A0B", tint: "#FBEEDA" };
  const AGT = { mid: "#6C5CD0", dark: "#463BA0", tint: "#ECE9FB" };
  const BOT = ["#C4BCEC", "#463BA0"];
  const reduce = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  const PAIRS = [
    { human: { who: "Shepherds", share: "share a pasture", cost: "overgrazing depletes the field", scene: "pasture" },
      agent: { who: "Agents", share: "share a power grid", cost: "coordinated load shifts destabilize the grid", scene: "grid" } },
    { human: { who: "Factories", share: "share a river", cost: "pollution shifts cost downstream", scene: "river" },
      agent: { who: "Agents", share: "share a database", cost: "unverified writes corrupt the state", scene: "memory" } },
    { human: { who: "Fishers", share: "share a pond", cost: "overfishing causes population collapse", scene: "pond" },
      agent: { who: "Agents", share: "share a critical codebase", cost: "unverified merges break reliant applications", scene: "code" } },
  ];

  const el = (tag, a = {}, p) => { const n = document.createElementNS(NS, tag); for (const [k, v] of Object.entries(a)) n.setAttribute(k, v); if (p) p.appendChild(n); return n; };
  const text = (x, y, s, a, p) => { const t = el("text", { x, y, ...a }, p); t.textContent = s; return t; };
  const html = (tag, cls, txt) => { const n = document.createElement(tag); if (cls) n.className = cls; if (txt !== undefined) n.textContent = txt; return n; };

  // ---------- hand-drawn glyphs, in the style of the poster and dilemmas.js ----------
  const LINE = { fill: "none", stroke: INK, "stroke-width": 1.7, "stroke-linecap": "round", "stroke-linejoin": "round" };
  const person = (g, x, y, s = 1, arms = "down") => {
    const k = (v) => v * s;
    el("circle", { cx: x, cy: y - k(38), r: k(5.5), fill: "#fff", ...LINE }, g);
    el("path", { d: `M ${x} ${y - k(32)} L ${x} ${y - k(14)} M ${x} ${y - k(14)} L ${x - k(6)} ${y} M ${x} ${y - k(14)} L ${x + k(6)} ${y}`, ...LINE }, g);
    const a = arms === "up" ? `M ${x - k(8)} ${y - k(34)} L ${x} ${y - k(27)} L ${x + k(10)} ${y - k(33)}`
      : arms === "rod" ? `M ${x - k(7)} ${y - k(19)} L ${x} ${y - k(27)} L ${x + k(10)} ${y - k(30)}`
      : `M ${x - k(7)} ${y - k(19)} L ${x} ${y - k(27)} L ${x + k(7)} ${y - k(19)}`;
    el("path", { d: a, ...LINE }, g);
  };
  const robot = (g, x, y, s, col = BOT) => {
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
    return r;
  };
  const sheep = (g, x, y) => {
    el("ellipse", { cx: x, cy: y, rx: 11, ry: 7, fill: "#fff", stroke: INK, "stroke-width": 1.4 }, g);
    el("ellipse", { cx: x - 12, cy: y - 2, rx: 4, ry: 3.4, fill: "#fff", stroke: INK, "stroke-width": 1.3 }, g);
    [-6, -1, 4, 8].forEach((dx) => el("line", { x1: x + dx, y1: y + 6, x2: x + dx, y2: y + 12, stroke: INK, "stroke-width": 1.3, "stroke-linecap": "round" }, g));
  };
  const SCENES = {
    pasture: (g) => {
      el("rect", { x: 6, y: 42, width: 118, height: 44, rx: 10, fill: "#E5F0DA" }, g);
      [[22, 66], [48, 70], [74, 66]].forEach(([x, y]) => sheep(g, x, y));
      [[96, 78], [105, 74], [112, 80]].forEach(([x, y]) => el("path", { d: `M ${x} ${y} l 2 -6 m 2 6 l 1 -7 m 2 7 l 2 -5`, stroke: "#A8C98F", "stroke-width": 1.3, "stroke-linecap": "round", fill: "none" }, g));
      person(g, 128, 82, 1.05, "up");
      el("line", { x1: 139, y1: 47, x2: 146, y2: 20, ...LINE }, g);
    },
    river: (g) => {
      el("rect", { x: 20, y: 34, width: 40, height: 34, rx: 3, fill: "#D9D9D9", stroke: INK, "stroke-width": 1.4 }, g);
      el("rect", { x: 34, y: 18, width: 10, height: 18, rx: 2, fill: "#D9D9D9", stroke: INK, "stroke-width": 1.4 }, g);
      el("rect", { x: 72, y: 46, width: 34, height: 22, rx: 3, fill: "#D9D9D9", stroke: INK, "stroke-width": 1.4 }, g);
      el("rect", { x: 82, y: 32, width: 9, height: 15, rx: 2, fill: "#D9D9D9", stroke: INK, "stroke-width": 1.4 }, g);
      [[46, 12, 3.4], [52, 6, 2.6], [93, 26, 2.8], [98, 20, 2.2]].forEach(([cx, cy, r]) => el("circle", { cx, cy, r, fill: "#fff", stroke: MUT, "stroke-width": 1.2 }, g));
      [76, 84].forEach((y, i) => el("path", { d: `M 6 ${y} q 12 -6 24 0 t 24 0 t 24 0 t 24 0 t 24 0 t 24 0`, fill: "none", stroke: i ? "#9FC8E6" : "#5B8DB8", "stroke-width": 2, "stroke-linecap": "round" }, g));
      el("path", { d: "M 112 60 q 8 6 18 2", fill: "none", stroke: "#8F3F1E", "stroke-width": 1.4, "stroke-dasharray": "2 3" }, g);
      el("path", { d: "M 128 58 l 4 4 l -5 2", fill: "none", stroke: "#8F3F1E", "stroke-width": 1.4, "stroke-linecap": "round" }, g);
    },
    pond: (g) => {
      el("ellipse", { cx: 76, cy: 74, rx: 66, ry: 15, fill: "#BFDCEB", stroke: "#5B8DB8", "stroke-width": 1.4 }, g);
      [[60, 76], [92, 72]].forEach(([x, y]) => el("path", { d: `M ${x - 5} ${y} q 5 -4 10 0`, fill: "none", stroke: INK, "stroke-width": 1.2, "stroke-linecap": "round" }, g));
      [[26, 52], [64, 48], [104, 52]].forEach(([x, y], i) => {
        person(g, x, y, 0.92, "rod");
        el("path", { d: `M ${x + 9} ${y - 27} Q ${x + 30} ${y - 34} ${x + 22 + (i === 1 ? 4 : 0)} ${y + 18}`, fill: "none", stroke: "#8F2A45", "stroke-width": 1.6, "stroke-linecap": "round" }, g);
      });
    },
    grid: (g) => {
      [30, 66, 102].forEach((x) => robot(g, x, 46, 1));
      el("path", { d: "M 128 14 l -7 13 h 7 l -6 13", fill: "none", stroke: "#C79A3A", "stroke-width": 2, "stroke-linecap": "round", "stroke-linejoin": "round" }, g);
      el("rect", { x: 14, y: 60, width: 104, height: 13, rx: 6.5, fill: "#fff", stroke: AGT.dark, "stroke-width": 1.4 }, g);
      el("rect", { x: 16, y: 62, width: 66, height: 9, rx: 4.5, fill: "#8C7FE0", class: "cm-load" }, g);
      text(14, 87, "power load", { "font-size": 11, fill: MUT, "font-style": "italic" }, g);
    },
    memory: (g) => {
      [30, 66, 102].forEach((x) => robot(g, x, 46, 1));
      el("path", { d: "M 16 62 Q 66 46 116 62", fill: "none", stroke: AGT.mid, "stroke-width": 1.4, "stroke-dasharray": "3 4" }, g);
      el("rect", { x: 18, y: 64, width: 96, height: 22, rx: 11, fill: "#fff", stroke: AGT.dark, "stroke-width": 1.4 }, g);
      text(66, 79, "memory store", { "text-anchor": "middle", "font-size": 11, "font-weight": 700, fill: AGT.dark }, g);
      el("path", { d: "M 122 66 l 8 8 m 0 -8 l -8 8", stroke: "#C2662A", "stroke-width": 2, "stroke-linecap": "round" }, g);
    },
    code: (g) => {
      [30, 66, 102].forEach((x) => robot(g, x, 40, 0.92));
      el("rect", { x: 14, y: 50, width: 118, height: 38, rx: 5, fill: "#fff", stroke: AGT.dark, "stroke-width": 1.4 }, g);
      el("circle", { cx: 21, cy: 56, r: 1.8, fill: AGT.mid }, g); el("circle", { cx: 27, cy: 56, r: 1.8, fill: AGT.mid }, g);
      [[22, 65, 60], [22, 72, 84], [22, 79, 44]].forEach(([x, y, w]) => el("line", { x1: x, y1: y, x2: x + w, y2: y, stroke: "#B7AEEF", "stroke-width": 2.4, "stroke-linecap": "round" }, g));
      el("path", { d: "M 110 64 l 6 6 l -4 4 l 6 6", fill: "none", stroke: "#C2662A", "stroke-width": 2, "stroke-linecap": "round", "stroke-linejoin": "round" }, g);
    },
  };

  const card = (d, side) => {
    const c = side === "human" ? HUM : AGT;
    const a = html("article", `cm-card cm-${side}`);
    a.style.setProperty("--c", c.mid); a.style.setProperty("--d", c.dark); a.style.setProperty("--t", c.tint);
    const svg = el("svg", { viewBox: "0 0 150 92", class: "cm-art", "font-family": FONT, "aria-hidden": "true" });
    SCENES[d.scene](el("g", {}, svg));
    a.appendChild(svg);
    const t = html("div", "cm-text");
    const h = html("p", "cm-who");
    h.appendChild(html("strong", "", d.who));
    h.appendChild(html("span", "", " " + d.share));
    t.appendChild(h);
    t.appendChild(html("p", "cm-cost", d.cost));
    a.appendChild(t);
    return a;
  };

  // ---------- layout ----------
  const wrapEl = html("div", "cm-wrap");
  const head = html("div", "cm-head");
  [["Familiar commons", "in human social dilemmas", "human"], ["Artificial commons", "in LLM-agent systems", "agent"]].forEach(([t, s, k], i) => {
    if (i === 1) head.appendChild(html("span", "cm-head-gap"));
    const h = html("p", `cm-head-${k}`);
    h.appendChild(html("strong", "", t));
    h.appendChild(html("small", "", s));
    head.appendChild(h);
  });
  wrapEl.appendChild(head);

  PAIRS.forEach((p) => {
    const row = html("div", "cm-pair");
    row.tabIndex = 0;
    row.setAttribute("aria-label", `${p.human.who} ${p.human.share}: ${p.human.cost}. Likewise, agents ${p.agent.share}: ${p.agent.cost}.`);
    row.appendChild(card(p.human, "human"));
    const link = html("div", "cm-link");
    const ls = el("svg", { viewBox: "0 0 40 40", "aria-hidden": "true" });
    el("path", { d: "M 6 20 H 30", stroke: MUT, "stroke-width": 2, "stroke-linecap": "round", "stroke-dasharray": "3 4", fill: "none", class: "cm-link-line" }, ls);
    el("path", { d: "M 26 14 L 33 20 L 26 26", stroke: MUT, "stroke-width": 2, "stroke-linecap": "round", "stroke-linejoin": "round", fill: "none" }, ls);
    link.appendChild(ls);
    link.appendChild(html("span", "", "same dilemma"));
    row.appendChild(link);
    row.appendChild(card(p.agent, "agent"));
    row.addEventListener("click", () => {
      const on = !row.classList.contains("is-on");
      wrapEl.querySelectorAll(".cm-pair").forEach((r) => r.classList.remove("is-on"));
      row.classList.toggle("is-on", on);
    });
    wrapEl.appendChild(row);
  });

  // shared pool, after the "How does this look in LLM groups?" panel of the sanctions poster
  const pool = html("figure", "cm-pool");
  const ps = el("svg", { viewBox: "0 0 420 200", class: "cm-pool-art", "font-family": FONT, role: "img",
    "aria-label": "Five LLM agents of different model families linked to one shared pool, with a question mark: which rules will they follow?" });
  const CX = 210, CY = 104;
  const MODELS = [["#E7A49B", "#8F3F1E"], ["#A9C4E0", "#2F3D6B"], ["#E3C88C", "#8A5A0B"], ["#BBD9C4", "#2F6B4A"], ["#EEF2F6", "#3F4D5A"]];
  const pts = [[70, 52], [350, 52], [62, 168], [358, 168], [210, 196]];
  pts.forEach(([x, y], i) => {
    const path = `M ${x} ${y - 16} L ${CX} ${CY}`;
    el("path", { d: path, stroke: "#9AA6B2", "stroke-width": 1.6, "stroke-dasharray": "5 5", fill: "none" }, ps);
    if (!reduce) {
      const coin = el("circle", { r: 4, fill: "#E3A43A", stroke: "#8A5A0B", "stroke-width": 1 }, ps);
      const am = el("animateMotion", { dur: `${2.6 + i * 0.35}s`, repeatCount: "indefinite", path, begin: `${i * 0.5}s` }, coin);
      am.setAttribute("keyPoints", "0;1"); am.setAttribute("keyTimes", "0;1");
    }
  });
  const hex = [...Array(6)].map((_, k) => { const a = Math.PI / 3 * k + Math.PI / 6; return `${CX + 46 * Math.cos(a)},${CY + 40 * Math.sin(a)}`; }).join(" ");
  el("polygon", { points: hex, fill: "#BFE0A8", stroke: "#4F9070", "stroke-width": 2 }, ps);
  text(CX, CY + 4, "shared pool", { "text-anchor": "middle", "font-size": 13, "font-style": "italic", "font-weight": 700, fill: "#2F6B4A" }, ps);
  text(CX, 34, "?", { "text-anchor": "middle", "font-size": 26, "font-weight": 800, fill: MUT }, ps);
  pts.forEach(([x, y], i) => {
    robot(ps, x, y + 10, 1.3, MODELS[i]);
    const lx = i % 2 === 0 && i < 4 ? x - 40 : i === 4 ? x + 36 : x + 40;
    el("rect", { x: lx - 18, y: y - 30, width: 36, height: 18, rx: 4, fill: MODELS[i][0], stroke: MODELS[i][1], "stroke-width": 1.3 }, ps);
    text(lx, y - 17, "LLM", { "text-anchor": "middle", "font-size": 11, "font-weight": 800, fill: MODELS[i][1] }, ps);
  });
  pool.appendChild(ps);
  const cap = html("figcaption", "cm-pool-cap");
  cap.innerHTML = "<strong>Now let five agents share a resource pool.</strong> There is no shared history and no baked-in group norms (yet). The institution must be specified in the prompt or other settings, and even then, different model families might answer differently.";
  pool.appendChild(cap);
  wrapEl.appendChild(pool);

  stage.appendChild(wrapEl);
})();
