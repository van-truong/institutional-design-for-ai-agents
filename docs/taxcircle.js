/* The taxonomy as a compact circle for the paper: six family hubs, 18 theme nodes, and 66 mechanisms as dots
   around the edge, colored by family. A filled leaf has been tested with LLM agents, a dashed leaf only
   proposed, an open leaf has no LLM study. Same data and angular layout as the website's circle (taxonomy.js),
   without the leaf labels. Renders into #tc-stage; reads data-src (default assets/taxonomy.json). */
(function () {
  const stage = document.getElementById("tc-stage");
  if (!stage) return;
  const NS = "http://www.w3.org/2000/svg";
  const FONT = "'Helvetica Neue', Helvetica, Arial, sans-serif";
  const INK = "#3F4D5A", MUT = "#6B7787";
  const W = 760, H = 760, CX = 380, CY = 368;
  const R = { hub: 108, theme: 192, leaf: 268, label: 318 };
  const el = (tag, a = {}, p) => { const n = document.createElementNS(NS, tag); for (const [k, v] of Object.entries(a)) n.setAttribute(k, v); if (p) p.appendChild(n); return n; };
  const f1 = (n) => n.toFixed(1);
  // angle 0 = right, clockwise (screen coordinates), as in taxonomy.js
  const pt = (deg, r) => [CX + r * Math.cos((deg * Math.PI) / 180), CY + r * Math.sin((deg * Math.PI) / 180)];
  const mix = (a, b, t) => {
    const p = (h) => [1, 3, 5].map((i) => parseInt(h.slice(i, i + 2), 16));
    const [x, y] = [p(a), p(b)];
    return "#" + x.map((v, i) => Math.round(v + (y[i] - v) * t).toString(16).padStart(2, "0")).join("");
  };

  fetch(stage.dataset.src || "assets/taxonomy.json").then((r) => r.json()).then(draw);

  function draw(data) {
    const fams = data.families;
    const nLeaves = fams.reduce((s, f) => s + f.themes.reduce((t, th) => t + th.mechanisms.length, 0), 0);
    const step = 360 / (nLeaves + fams.length * 1.6);
    let slot = 0.8;
    fams.forEach((f) => {
      f.a0 = -90 + slot * step;
      f.themes.forEach((th) => {
        th.a0 = -90 + slot * step;
        th.mechanisms.forEach((m) => { m.a = -90 + slot * step; slot += 1; });
        th.a = (th.a0 + -90 + (slot - 1) * step) / 2;
      });
      f.a1 = -90 + (slot - 1) * step;
      f.a = (f.a0 + f.a1) / 2;
      slot += 1.6;
    });

    const TOP = 44;  // headroom for the figure title
    const svg = el("svg", { viewBox: `0 ${-TOP} ${W} ${H + TOP}`, width: W, height: H + TOP, xmlns: NS, "font-family": FONT, role: "img" }, stage);
    el("title", {}, svg).textContent = "The taxonomy at a glance";
    const ttl = el("text", { x: CX, y: -14, "text-anchor": "middle", "font-size": 20.5, "font-weight": 700, fill: "#2C2C2A" }, svg);
    ttl.textContent = "Cooperation-shaping mechanisms at a glance";
    const defs = el("defs", {}, svg);
    const glow = el("radialGradient", { id: "tc-bg", cx: CX, cy: CY, r: R.label + 30, gradientUnits: "userSpaceOnUse" }, defs);
    el("stop", { offset: "0", "stop-color": "#FFFFFF" }, glow);
    el("stop", { offset: "1", "stop-color": "#F6F3ED" }, glow);
    [R.theme, R.leaf].forEach((r) => el("circle", { cx: CX, cy: CY, r, fill: "none", stroke: "#E4E0D6", "stroke-width": 1, "stroke-dasharray": "3 5" }, svg));

    const curve = (a1, r1, a2, r2, col, w, op) => {
      const [x1, y1] = pt(a1, r1), [x2, y2] = pt(a2, r2), rm = (r1 + r2) / 2;
      const [c1x, c1y] = pt(a1, rm), [c2x, c2y] = pt(a2, rm);
      el("path", { d: `M ${f1(x1)} ${f1(y1)} C ${f1(c1x)} ${f1(c1y)}, ${f1(c2x)} ${f1(c2y)}, ${f1(x2)} ${f1(y2)}`, fill: "none", stroke: col, "stroke-width": w, "stroke-opacity": op }, svg);
    };
    // branches: center -> hub -> theme -> leaf
    fams.forEach((f) => {
      const [hx, hy] = pt(f.a, R.hub);
      el("line", { x1: CX, y1: CY, x2: f1(hx), y2: f1(hy), stroke: f.mid, "stroke-width": 2.4, "stroke-opacity": 0.55 }, svg);
      f.themes.forEach((th) => {
        curve(f.a, R.hub, th.a, R.theme, f.mid, 2, 0.6);
        th.mechanisms.forEach((m) => curve(th.a, R.theme, m.a, R.leaf - 7.5, f.mid, 1.1, 0.45));
      });
    });
    // leaves: a small pointed leaf along each radius
    fams.forEach((f) => f.themes.forEach((th) => th.mechanisms.forEach((m) => {
      const [x, y] = pt(m.a, R.leaf);
      const tested = m.llm === "tested", proposed = m.llm === "proposed";
      el("circle", { cx: f1(x), cy: f1(y), r: 7.5, fill: tested ? f.mid : proposed ? mix(f.mid, "#ffffff", 0.75) : "#ffffff",
        stroke: tested ? f.dark : f.mid, "stroke-width": 1.6, ...(proposed ? { "stroke-dasharray": "2.5 2" } : {}) }, svg);
    })));
    // theme nodes and family hubs
    fams.forEach((f) => {
      f.themes.forEach((th) => {
        const [x, y] = pt(th.a, R.theme);
        el("circle", { cx: f1(x), cy: f1(y), r: 6.5, fill: "#fff", stroke: f.mid, "stroke-width": 2.2 }, svg);
      });
      const [hx, hy] = pt(f.a, R.hub);
      el("circle", { cx: f1(hx), cy: f1(hy), r: 13, fill: mix(f.mid, "#ffffff", 0.82), stroke: f.mid, "stroke-width": 2.6 }, svg);
      el("circle", { cx: f1(hx), cy: f1(hy), r: 5, fill: f.mid }, svg);
    });
    // center
    el("circle", { cx: CX, cy: CY, r: 66, fill: "#fff", stroke: INK, "stroke-width": 1.8 }, svg);
    const ct = (y, s, a) => { const t = el("text", { x: CX, y, "text-anchor": "middle", fill: INK, ...a }, svg); t.textContent = s; };
    ct(CY + 6, `${Math.floor(nLeaves / 10) * 10}+`, { "font-size": 46, "font-weight": 800 });  // rounded down, like the paper's prose
    ct(CY + 32, "mechanisms", { "font-size": 18, fill: MUT });
    // family names curve around the outside, readable on both halves
    fams.forEach((f) => {
      const span = Math.max(f.a1 - f.a0 + 18, 40), bottom = Math.sin((f.a * Math.PI) / 180) > 0.15;
      const r = R.label + (bottom ? 12 : 0);
      const [x0, y0] = pt(bottom ? f.a + span / 2 : f.a - span / 2, r), [x1, y1] = pt(bottom ? f.a - span / 2 : f.a + span / 2, r);
      el("path", { id: `tc-${f.id}`, d: `M ${f1(x0)} ${f1(y0)} A ${r} ${r} 0 0 ${bottom ? 0 : 1} ${f1(x1)} ${f1(y1)}`, fill: "none" }, defs);
      const t = el("text", { "font-size": 22, "font-weight": 800, "letter-spacing": "0.12em", fill: f.dark }, svg);
      el("textPath", { href: `#tc-${f.id}`, startOffset: "50%", "text-anchor": "middle" }, t).textContent = f.label.toUpperCase();
    });
    // legend
    const ly = H - 16;
    const key = [["tested", "tested with LLM agents"], ["proposed", "proposed only"], ["none", "no LLM study"]];
    let lx = 128;
    key.forEach(([k, txt]) => {
      el("circle", { cx: lx, cy: ly - 5, r: 7.5, fill: k === "tested" ? MUT : k === "proposed" ? "#E7EAEE" : "#fff",
        stroke: k === "tested" ? INK : MUT, "stroke-width": 1.6, ...(k === "proposed" ? { "stroke-dasharray": "2.5 2" } : {}) }, svg);
      const t = el("text", { x: lx + 22, y: ly, "font-size": 17, fill: MUT }, svg);
      t.textContent = txt;
      lx += 22 + txt.length * 8.6 + 34;
    });
  }
})();
