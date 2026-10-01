/* Research agenda (website): four steps on a path that loops back on itself, since every correction feeds the
   map again. Each step has a small drawn icon, its number, the original messaging, and a link to where a reader
   can act on it. Cards rise in when the section scrolls into view; they stack on a phone. */
(function () {
  const stage = document.getElementById("agenda-stage");
  if (!stage) return;

  const NS = "http://www.w3.org/2000/svg";
  const STEPS = [
    { n: "01", title: "See the evidence", text: "Connect leaves to exact human, LLM-agent, and computational-agent studies.",
      c: ["#3A6EA5", "#2F3D6B", "#DCE8F5"], icon: "evidence", link: ["#taxonomy", "Browse the taxonomy"] },
    { n: "02", title: "See the gaps", text: "Distinguish strong, weak, conflicting, and not-yet-curated coverage.",
      c: ["#C79A3A", "#8A5A0B", "#FBEEDA"], icon: "gaps", link: ["#taxonomy", "Find the open circles"] },
    { n: "03", title: "Question the map", text: "Show limitations and open questions instead of treating citation count as quality.",
      c: ["#C2662A", "#8F3F1E", "#FBEDE6"], icon: "question", link: ["https://github.com/van-truong/institutional-design-for-ai-agents/issues", "Propose another reading"] },
    { n: "04", title: "Help it grow", text: "Welcome reviewed corrections and additions through GitHub.",
      c: ["#4F9070", "#2F6B4A", "#E5F0E1"], icon: "grow", link: ["https://github.com/van-truong/institutional-design-for-ai-agents", "Contribute on GitHub"] },
  ];

  const el = (tag, a = {}, p) => { const n = document.createElementNS(NS, tag); for (const [k, v] of Object.entries(a)) n.setAttribute(k, v); if (p) p.appendChild(n); return n; };
  const html = (tag, cls, txt) => { const n = document.createElement(tag); if (cls) n.className = cls; if (txt !== undefined) n.textContent = txt; return n; };

  const ICONS = {
    evidence: (g, c) => {     // a source document with a magnifier over it
      el("rect", { x: 16, y: 12, width: 34, height: 44, rx: 4, fill: "#fff", stroke: c[1], "stroke-width": 2 }, g);
      [22, 30, 38].forEach((y, i) => el("line", { x1: 22, y1: y, x2: 44 - i * 5, y2: y, stroke: c[0], "stroke-width": 2.4, "stroke-linecap": "round" }, g));
      el("circle", { cx: 50, cy: 46, r: 12, fill: c[2], stroke: c[1], "stroke-width": 2.6 }, g);
      el("line", { x1: 59, y1: 55, x2: 68, y2: 64, stroke: c[1], "stroke-width": 4, "stroke-linecap": "round" }, g);
    },
    gaps: (g, c) => {         // the taxonomy's evidence circles: filled, dotted, open
      el("circle", { cx: 18, cy: 38, r: 8, fill: c[0], stroke: c[1], "stroke-width": 2 }, g);
      el("circle", { cx: 38, cy: 38, r: 8, fill: "#fff", stroke: c[1], "stroke-width": 2, "stroke-dasharray": "3 2.5" }, g);
      el("circle", { cx: 58, cy: 38, r: 8, fill: "#fff", stroke: c[1], "stroke-width": 2 }, g);
    },
    question: (g, c) => {     // a folded map with a question mark
      el("path", { d: "M 10 18 L 28 12 L 46 18 L 64 12 V 58 L 46 64 L 28 58 L 10 64 Z", fill: "#fff", stroke: c[1], "stroke-width": 2, "stroke-linejoin": "round" }, g);
      el("path", { d: "M 28 12 V 58 M 46 18 V 64", stroke: c[0], "stroke-width": 1.4, "stroke-dasharray": "3 3" }, g);
      el("circle", { cx: 52, cy: 46, r: 13, fill: c[0] }, g);
      const t = el("text", { x: 52, y: 52, "text-anchor": "middle", "font-size": 18, "font-weight": 800, fill: "#fff", "font-family": "'Helvetica Neue', Arial, sans-serif" }, g);
      t.textContent = "?";
    },
    grow: (g, c) => {         // a sprout with a plus leaf
      el("path", { d: "M 38 62 V 30", stroke: c[1], "stroke-width": 2.6, "stroke-linecap": "round" }, g);
      el("path", { d: "M 38 40 C 22 40 16 28 18 20 C 30 20 38 28 38 40 Z", fill: c[2], stroke: c[1], "stroke-width": 2 }, g);
      el("path", { d: "M 38 32 C 52 32 58 22 56 14 C 44 14 38 22 38 32 Z", fill: c[0], stroke: c[1], "stroke-width": 2 }, g);
      el("path", { d: "M 22 62 H 54", stroke: c[1], "stroke-width": 2.4, "stroke-linecap": "round" }, g);
      el("circle", { cx: 60, cy: 46, r: 9, fill: "#fff", stroke: c[1], "stroke-width": 2 }, g);
      el("path", { d: "M 60 41 v 10 M 55 46 h 10", stroke: c[1], "stroke-width": 2.2, "stroke-linecap": "round" }, g);
    },
  };

  const wrap = html("div", "ag-wrap");
  const row = html("ol", "ag-steps");
  STEPS.forEach((s, i) => {
    const li = html("li", "ag-step");
    li.style.setProperty("--c", s.c[0]); li.style.setProperty("--d", s.c[1]); li.style.setProperty("--t", s.c[2]);
    li.style.setProperty("--i", i);
    const badge = html("span", "ag-num", s.n);
    li.appendChild(badge);
    const ic = el("svg", { viewBox: "0 0 76 76", class: "ag-icon", "aria-hidden": "true" });
    ICONS[s.icon](el("g", {}, ic), s.c);
    li.appendChild(ic);
    li.appendChild(html("h4", "ag-title", s.title));
    li.appendChild(html("p", "ag-text", s.text));
    const a = html("a", "ag-link", s.link[1] + " →");
    a.href = s.link[0];
    if (s.link[0].startsWith("http")) { a.target = "_blank"; a.rel = "noopener"; }
    li.appendChild(a);
    row.appendChild(li);
  });
  wrap.appendChild(row);

  // the loop: every reviewed correction or addition flows back into the map
  const loop = html("div", "ag-loop");
  const ls = el("svg", { viewBox: "0 0 1000 60", preserveAspectRatio: "none", class: "ag-loop-art", "aria-hidden": "true" });
  const defs = el("defs", {}, ls);
  const m = el("marker", { id: "ag-ar", viewBox: "0 0 10 10", refX: 8, refY: 5, markerWidth: 7, markerHeight: 7, orient: "auto-start-reverse" }, defs);
  el("path", { d: "M 0 0 L 10 5 L 0 10 z", fill: "#4F9070" }, m);
  el("path", { d: "M 880 6 C 880 48, 860 50, 780 50 L 220 50 C 140 50, 120 48, 120 10", fill: "none", stroke: "#4F9070",
    "stroke-width": 2.2, "stroke-dasharray": "7 6", "marker-end": "url(#ag-ar)", class: "ag-loop-line", "vector-effect": "non-scaling-stroke" }, ls);
  loop.appendChild(ls);
  loop.appendChild(html("p", "ag-loop-text", "↺ each reviewed correction or addition feeds back into the map"));
  wrap.appendChild(loop);
  stage.appendChild(wrap);

  if ("IntersectionObserver" in window) {
    const io = new IntersectionObserver((es) => {
      if (es.some((e) => e.isIntersecting)) { wrap.classList.add("ag-in"); io.disconnect(); }
    }, { threshold: 0.2 });
    io.observe(wrap);
  } else wrap.classList.add("ag-in");
})();
