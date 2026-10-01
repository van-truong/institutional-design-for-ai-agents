/* Group-level phenomena (paper Fig. 6). Reads assets/phenomena.json (built by
   taxonomy/scripts/build_phenomena_data.py).
   Website: two views, like the taxonomy. A radial "map" (default) places the ten phenomenon types around a circle,
   with one ring per substrate (humans, MARL agents, LLM agents) and dots sized by coded instances; the "list" view
   is the substrate matrix whose rows expand to the papers behind each type and the real-world incidents.
   Paper (a container with data-mode="paper"): a static two-panel figure, (A) the same spoke map with larger print
   text above (B) the unravelled list drawn in the style of the taxonomy figure (Fig. 5): band pills, tree
   connectors, sized evidence dots, and incident chips. */
(function () {
  const $ = (sel, p = document) => p.querySelector(sel);
  const html = (tag, attrs = {}, text) => {
    const n = document.createElement(tag);
    for (const [k, v] of Object.entries(attrs)) n.setAttribute(k, v);
    if (text !== undefined) n.textContent = text;
    return n;
  };
  const NS = "http://www.w3.org/2000/svg";
  const svgEl = (tag, attrs = {}, parent) => {
    const n = document.createElementNS(NS, tag);
    for (const [k, v] of Object.entries(attrs)) n.setAttribute(k, v);
    if (parent) parent.appendChild(n);
    return n;
  };
  const stext = (x, y, s, attrs, parent) => { const t = svgEl("text", { x, y, ...attrs }, parent); t.textContent = s; return t; };
  const wrap = (s, n) => {
    const out = []; let cur = "";
    s.split(" ").forEach((w) => { if ((cur + " " + w).trim().length <= n) cur = (cur + " " + w).trim(); else { if (cur) out.push(cur); cur = w; } });
    if (cur) out.push(cur);
    return out;
  };

  const VAL = { beneficial: "benef", neutral: "neut", harmful: "harm" };
  // valence colors (figs/PALETTE.md; as in gen_phenomena.py): mid, dark, tint
  const VC = { beneficial: ["#4F9070", "#2F6B4A", "#E5F0E1"], neutral: ["#3A6EA5", "#2F3D6B", "#DCE8F5"],
    harmful: ["#C2662A", "#8F3F1E", "#FBEDE6"] };
  const FONT = "'Helvetica Neue', Helvetica, Arial, sans-serif";
  const INK = "#3F4D5A", MUT = "#6B7787", HAIR = "#B3BEC9";
  const SUBS = [["human", "Humans"], ["marl", "MARL agents"], ["llm", "LLM agents"]];
  const GROUPLAB = { llm: "LLM-agent studies", marl: "MARL studies", human: "Human studies" };
  const SHOW_FIRST = 6;
  // short incident labels for the printed figure
  const SHORT = {
    "emergence-collusion-sim": "Agents collude to bypass guardrails",
    "metr-redwood-agent-message-board": "Hidden message board to cheat an eval",
    "servicenow-agent-to-agent-injection": "Agents turned against each other",
    "openai-hf-intrusion-2026": "Agents breach production infrastructure",
    "openai-dsewiki-breakout": "Agents hijack a live website",
    "anthropic-gtg1002-espionage": "AI-orchestrated espionage campaign",
    "anthropic-multiagent-turf-wars": "Multi-agent “turf wars”",
  };

  const paperHost = document.querySelector('[data-ph-paper]');
  const PAPER = !!paperHost && paperHost.dataset.mode === "paper";
  const src = (paperHost && paperHost.dataset.src) || "assets/phenomena.json";

  fetch(src).then((r) => r.json()).then((data) => (PAPER ? drawPaper(data, paperHost) : render(data))).catch(() => {
    const m = $("#ph-matrix"); if (m) m.textContent = "The phenomena data could not be loaded.";
  });

  // ---------------------------------------------------------------- glyphs (shared with the rings figure's style)
  function glyph(kind, x, y, s, col, parent) {
    const g = svgEl("g", { transform: `translate(${x} ${y}) scale(${s})` }, parent);
    if (kind === "human") {
      svgEl("circle", { cx: 0, cy: -9, r: 6.5, fill: "#fff", stroke: col, "stroke-width": 1.8 }, g);
      svgEl("path", { d: "M -11 12 Q -11 0 0 0 Q 11 0 11 12 Z", fill: col, opacity: 0.85 }, g);
    } else {
      svgEl("line", { x1: 0, y1: -15, x2: 0, y2: -20, stroke: col, "stroke-width": 1.6, "stroke-linecap": "round" }, g);
      svgEl("circle", { cx: 0, cy: -21.5, r: 2.2, fill: col }, g);
      svgEl("rect", { x: -11, y: -15, width: 22, height: 15, rx: kind === "marl" ? 2 : 5, fill: "#fff", stroke: col, "stroke-width": 1.6 }, g);
      if (kind === "marl") {
        svgEl("rect", { x: -6.5, y: -10, width: 4, height: 4, fill: col }, g);
        svgEl("rect", { x: 2.5, y: -10, width: 4, height: 4, fill: col }, g);
      } else {
        svgEl("circle", { cx: -4.5, cy: -7.5, r: 2, fill: col }, g);
        svgEl("circle", { cx: 4.5, cy: -7.5, r: 2, fill: col }, g);
        svgEl("path", { d: "M 13 -22 h 12 a 3 3 0 0 1 3 3 v 5 a 3 3 0 0 1 -3 3 h -7 l -4 3 v -3 h -1 a 3 3 0 0 1 -3 -3 v -5 a 3 3 0 0 1 3 -3 z",
          fill: "#fff", stroke: col, "stroke-width": 1.3 }, g);
      }
      svgEl("rect", { x: -8.5, y: 2, width: 17, height: 11, rx: 4, fill: col, opacity: 0.85 }, g);
    }
    return g;
  }
  const flag = (x, y, s, parent) => {
    const g = svgEl("g", { transform: `translate(${x} ${y}) scale(${s})` }, parent);
    svgEl("line", { x1: 0, y1: 7, x2: 0, y2: -7, stroke: VC.harmful[1], "stroke-width": 1.6, "stroke-linecap": "round" }, g);
    svgEl("path", { d: "M 0 -7 L 9 -4 L 0 -1 Z", fill: VC.harmful[0] }, g);
    return g;
  };
  const dotR = (n, k = 1) => (n ? (6 + 3.4 * Math.sqrt(n)) * k : 3 * k);

  // ---------------------------------------------------------------- paper: (A) the spoke map above (B) the
  // unravelled list, styled like the taxonomy figure (Fig. 5)
  function drawPaper(data, host) {
    const W = 1000, SA = 0.75, FS = 1.4, RAD_TOP = 4, RAD_BOT = 880;  // spoke-map crop (its own 1200-wide frame)
    const svg = svgEl("svg", { xmlns: NS, "font-family": FONT, role: "img" }, host);
    // panel headings in the taxonomy figure's title style (bold ink, centered), sized to print like Fig. 5's title
    const panel = (y, letter, title) => {
      stext(20, y, letter, { "font-size": 25, "font-weight": 800, fill: "#3F4D5A" }, svg);
      stext(W / 2, y, title, { "font-size": 25, "font-weight": 700, fill: "#3F4D5A", "text-anchor": "middle" }, svg);
    };
    panel(28, "A", "Phenomena by type and kind of agent");
    const ga = svgEl("g", { transform: `translate(${((W - 1200 * SA) / 2).toFixed(1)} ${(50 - RAD_TOP * SA).toFixed(1)}) scale(${SA})` }, svg);
    radialMap(ga, data, { fs: FS, idp: "pp-", ringKey: false, interactive: false });
    const yb = 50 + (RAD_BOT - RAD_TOP) * SA + 18;
    svgEl("line", { x1: 20, y1: yb - 10, x2: W - 20, y2: yb - 10, stroke: HAIR, "stroke-width": 1 }, svg);
    panel(yb + 24, "B", "Phenomena with documented real-world incidents");
    const H = drawList(svg, data, yb + 40);
    svg.setAttribute("viewBox", `0 0 ${W} ${H.toFixed(0)}`);
    svg.setAttribute("width", W); svg.setAttribute("height", H.toFixed(0));
    host.style.width = W + "px"; host.style.height = H.toFixed(0) + "px";
  }

  // the list, drawn from y0 down; returns the bottom edge (including the legend)
  function drawList(svg, data, y0) {
    const incBy = Object.fromEntries(data.incidents.map((x) => [x.key, x]));
    const W = 1000, LX = 64, COL = [452, 524, 596], IX = 642, IP = 21, WR = 40;
    const rowH = (t) => Math.max(wrap(t.label, WR).length > 1 ? 44 : 32, (t.incidents || []).length * IP + 8);
    const bands = [
      { title: "WHAT AGENT GROUPS BUILD", c: VC.neutral, types: data.types.filter((t) => t.valence !== "harmful") },
      { title: "WHERE IT GOES WRONG", c: VC.harmful, types: data.types.filter((t) => t.valence === "harmful") },
    ];
    // column heads with substrate glyphs
    SUBS.forEach(([k, lab], i) => {
      glyph(k, COL[i], y0 + 24, 1.05, INK, svg);
      stext(COL[i], y0 + 58, lab.split(" ")[0], { "text-anchor": "middle", "font-size": 15, "font-weight": 700, fill: INK }, svg);
    });
    flag(IX + 8, y0 + 52, 1.5, svg);
    stext(IX + 24, y0 + 58, "Documented in the wild", { "font-size": 15.5, "font-weight": 700, fill: VC.harmful[1] }, svg);
    let y = y0 + 66;
    bands.forEach((b) => {
      // band pill and rule, as for the taxonomy's families
      const pw = b.title.length * 12.2 + 34;
      svgEl("rect", { x: 20, y: y + 6, width: pw, height: 30, rx: 15, fill: b.c[1] }, svg);
      stext(20 + pw / 2, y + 27, b.title, { "text-anchor": "middle", "font-size": 16, "font-weight": 800, "letter-spacing": "0.08em", fill: "#fff" }, svg);
      svgEl("line", { x1: 26 + pw, y1: y + 21, x2: W - 16, y2: y + 21, stroke: b.c[0], "stroke-width": 1.6 }, svg);
      y += 44;
      const top = y, mids = [];
      b.types.forEach((t, i) => {
        const h = rowH(t), mid = y + h / 2, c = VC[t.valence];
        mids.push(mid);
        if (i % 2 === 1) svgEl("rect", { x: LX - 18, y, width: W - LX + 2, height: h, rx: 8, fill: "#F7F6F2" }, svg);
        svgEl("circle", { cx: 40, cy: mid, r: 5.5, fill: "#fff", stroke: c[0], "stroke-width": 2.2 }, svg);
        const lines = wrap(t.label, WR);
        lines.forEach((ln, k) => stext(LX, mid + 5.5 - (lines.length - 1) * 9.5 + k * 19, ln, { "font-size": 16.5, "font-weight": 700, fill: c[1] }, svg));
        SUBS.forEach(([k], j) => {
          const n = t.counts[k], r = Math.min(dotR(n), h / 2 - 1);
          if (n) {
            svgEl("circle", { cx: COL[j], cy: mid, r, fill: c[2], stroke: c[0], "stroke-width": 1.8 }, svg);
            stext(COL[j], mid + 5.5, String(n), { "text-anchor": "middle", "font-size": 15, "font-weight": 800, fill: c[1] }, svg);
          } else svgEl("circle", { cx: COL[j], cy: mid, r: 3.4, fill: "#fff", stroke: HAIR, "stroke-width": 1.3 }, svg);
        });
        const incs = (t.incidents || []).map((key) => incBy[key]).filter(Boolean);
        incs.forEach((inc, k) => {
          const iy = mid - (incs.length - 1) * IP / 2 + k * IP;
          const label = (SHORT[inc.key] || inc.short) + (inc.year ? ` (${inc.year})` : "");
          const w = label.length * 6.9 + 34;
          svgEl("rect", { x: IX, y: iy - 9.5, width: w, height: 19, rx: 9.5, fill: VC.harmful[2], stroke: VC.harmful[0], "stroke-width": 1.1 }, svg);
          flag(IX + 14, iy, 0.9, svg);
          stext(IX + 26, iy + 5, label, { "font-size": 14, "font-weight": 600, fill: VC.harmful[1] }, svg);
        });
        y += h;
      });
      // tree connector from the pill down to each row
      svgEl("line", { x1: 40, y1: top - 8, x2: 40, y2: mids[mids.length - 1] - 6, stroke: b.c[0], "stroke-width": 1.6, opacity: 0.6 }, svg);
      y += 10;
    });
    // legend, in the taxonomy figure's footer style
    const ly = y + 30;
    svgEl("line", { x1: 20, y1: ly - 22, x2: W - 20, y2: ly - 22, stroke: HAIR, "stroke-width": 1 }, svg);
    stext(20, ly, "Effect on cooperation:", { "font-size": 15, "font-weight": 700, fill: INK }, svg);
    let lx = 200;
    [["beneficial", "beneficial"], ["neutral", "neutral / surprising"], ["harmful", "harmful"]].forEach(([k, lab]) => {
      svgEl("circle", { cx: lx, cy: ly - 5, r: 8, fill: VC[k][2], stroke: VC[k][0], "stroke-width": 1.8 }, svg);
      stext(lx + 14, ly, lab, { "font-size": 15, fill: INK }, svg);
      lx += lab.length * 8 + 46;
    });
    stext(W - 20, ly, `Dot area ∝ instances (${data.counts.total} in all)`, { "text-anchor": "end", "font-size": 15, "font-style": "italic", fill: MUT }, svg);
    return ly + 12;
  }

  // ---------------------------------------------------------------- the radial "spoke" map, shared by the website
  // and the paper. Draws in a 1200 x 925 frame into `svg` (an <svg> or <g>); o.fs scales the text for print.
  function radialMap(svg, data, o) {
    const W = 1200, CX = 600, CY = 430, RING = { human: 150, marl: 228, llm: 306 }, k = o.fs, P = o.idp;
    const builds = data.types.filter((t) => t.valence !== "harmful"), wrongs = data.types.filter((t) => t.valence === "harmful");
    const ang = {};
    builds.forEach((t, i) => { ang[t.key] = -96 + (192 * i) / (builds.length - 1); });
    wrongs.forEach((t, i) => { ang[t.key] = 154 + (52 * i) / Math.max(1, wrongs.length - 1); });
    const pt = (deg, r) => { const a = (deg * Math.PI) / 180; return [CX + r * Math.sin(a), CY - r * Math.cos(a)]; };
    const f = (n) => n.toFixed(1);
    const defs = svgEl("defs", {}, svg);
    const sh = svgEl("filter", { id: P + "shadow", x: "-10%", y: "-10%", width: "120%", height: "120%" }, defs);
    svgEl("feDropShadow", { dx: 0, dy: 6, stdDeviation: 10, "flood-color": INK, "flood-opacity": 0.12 }, sh);
    const donut = (a0, a1, r0, r1) => {
      const [x0, y0] = pt(a0, r1), [x1, y1] = pt(a1, r1), [x2, y2] = pt(a1, r0), [x3, y3] = pt(a0, r0);
      const lg = a1 - a0 > 180 ? 1 : 0;
      return `M ${f(x0)} ${f(y0)} A ${r1} ${r1} 0 ${lg} 1 ${f(x1)} ${f(y1)} L ${f(x2)} ${f(y2)} A ${r0} ${r0} 0 ${lg} 0 ${f(x3)} ${f(y3)} Z`;
    };
    const sectors = svgEl("g", { filter: `url(#${P}shadow)` }, svg);
    svgEl("path", { d: donut(-112, 112, 84, 336), fill: "#EEF4FA", stroke: "#C9DAEC", "stroke-width": 1.2 }, sectors);
    svgEl("path", { d: donut(144, 216, 84, 336), fill: "#FCF1EA", stroke: "#EBC9B4", "stroke-width": 1.2 }, sectors);
    // substrate rings with glyph labels in the right-hand gap
    SUBS.forEach(([k, lab]) => {
      svgEl("circle", { cx: CX, cy: CY, r: RING[k], fill: "none", stroke: HAIR, "stroke-width": 1.2, "stroke-dasharray": "4 5" }, svg);
    });
    if (o.ringKey) {
      // ring key under the map: substrates from the center out
      stext(CX - 400, 908, "RINGS, FROM THE CENTER OUT", { "font-size": 13, "font-weight": 800, "letter-spacing": "0.1em", fill: MUT }, svg);
      SUBS.forEach(([sk, lab], i) => {
        const x = CX - 90 + i * 160;
        glyph(sk, x, 908, 0.8, INK, svg);
        stext(x + 20, 913, lab, { "font-size": 15, "font-weight": 700, fill: INK }, svg);
      });
    } else {
      // print: name each ring in the empty lower-right gap between the two sectors
      SUBS.forEach(([sk, lab]) => {
        const [x, y] = pt(134, RING[sk]);
        stext(f(x), f(y + 5 * k), lab, { "text-anchor": "middle", "font-size": 13.5 * k, "font-weight": 700, fill: MUT,
          stroke: "#fff", "stroke-width": 4, "paint-order": "stroke" }, svg);
      });
    }
    // sector titles curved inside the donut
    const arcPath = (id, r, a0, a1, sweep) => {
      const [x0, y0] = pt(a0, r), [x1, y1] = pt(a1, r);
      svgEl("path", { id, d: `M ${f(x0)} ${f(y0)} A ${r} ${r} 0 0 ${sweep} ${f(x1)} ${f(y1)}`, fill: "none" }, defs);
    };
    arcPath(P + "arc-build", k > 1 ? 113 : 110, k > 1 ? -92 : -78, k > 1 ? 92 : 78, 1);
    arcPath(P + "arc-wrong", 120, 236, 124, 0);
    [[P + "arc-build", "WHAT AGENT GROUPS BUILD", VC.neutral[1]], [P + "arc-wrong", "WHERE IT GOES WRONG", VC.harmful[1]]].forEach(([id, s, c]) => {
      const t = svgEl("text", { "font-size": 13.5 * Math.min(k, 1.2), "font-weight": 800, "letter-spacing": k > 1 ? "0.05em" : "0.12em", fill: c }, svg);
      const tp = svgEl("textPath", { href: `#${id}`, startOffset: "50%", "text-anchor": "middle" }, t);
      tp.textContent = s;
    });
    svgEl("circle", { cx: CX, cy: CY, r: 70, fill: "#fff", stroke: HAIR, "stroke-width": 1.2 }, svg);
    stext(CX, CY + 6 * k, String(data.counts.total), { "text-anchor": "middle", "font-size": 40 * k, "font-weight": 800, fill: INK }, svg);
    stext(CX, CY + 30 * k, "instances", { "text-anchor": "middle", "font-size": 13.5 * k, fill: MUT }, svg);

    const nodes = [];
    data.types.forEach((t) => {
      const a = ang[t.key], c = VC[t.valence];
      const g = svgEl("g", o.interactive ? { class: "ph-rnode", tabindex: "0", role: "button", "aria-label": `${t.label}: ${t.total} instances` } : {}, svg);
      g.dataset.key = t.key;
      const [sx, sy] = pt(a, 78), [ex, ey] = pt(a, 334);
      svgEl("line", { x1: f(sx), y1: f(sy), x2: f(ex), y2: f(ey), stroke: c[0], "stroke-width": 1.4, opacity: 0.35, class: "ph-spoke" }, g);
      SUBS.forEach(([sk]) => {
        const n = t.counts[sk], [x, y] = pt(a, RING[sk]);
        if (n) {
          svgEl("circle", { cx: f(x), cy: f(y), r: f(dotR(n, 1.1 * Math.sqrt(k))), fill: c[2], stroke: c[0], "stroke-width": 2 }, g);
          stext(f(x), f(y + 5.5 * k), String(n), { "text-anchor": "middle", "font-size": 15 * k, "font-weight": 800, fill: c[1] }, g);
        } else svgEl("circle", { cx: f(x), cy: f(y), r: 3.5, fill: "#fff", stroke: HAIR, "stroke-width": 1.3 }, g);
      });
      // horizontal label outside the circle
      const s = Math.sin((a * Math.PI) / 180), co = Math.cos((a * Math.PI) / 180);
      const [lx, ly] = pt(a, 356 + (k - 1) * 20), LH = 19 * k;
      const anchor = s > 0.25 ? "start" : s < -0.25 ? "end" : "middle";
      const lines = wrap(t.label, 22);
      const y0 = co > 0.5 ? ly - (lines.length - 1) * LH : co < -0.5 ? ly + 14 * k : ly - ((lines.length - 1) * LH) / 2 + 5 * k;
      lines.forEach((ln, j) => stext(f(lx), f(y0 + j * LH), ln, { "text-anchor": anchor, "font-size": 16.5 * k, "font-weight": 700, fill: c[1] }, g));
      const incs = (t.incidents || []).length;
      if (incs) {
        const iy = y0 + lines.length * LH + 2 * k, label = `${incs} documented incident${incs > 1 ? "s" : ""}`;
        const iw = (label.length * 7 + 26) * k, ix = anchor === "start" ? lx : anchor === "end" ? lx - iw : lx - iw / 2;
        svgEl("rect", { x: f(ix), y: f(iy - 14 * k), width: f(iw), height: f(21 * k), rx: f(10.5 * k), fill: VC.harmful[2], stroke: VC.harmful[0], "stroke-width": 1 }, g);
        flag(f(ix + 12 * k), f(iy - 3.5 * k), 0.85 * k, g);
        stext(f(ix + 22 * k), f(iy + 1 * k), label, { "font-size": 12.5 * k, "font-weight": 700, fill: VC.harmful[1] }, g);
      }
      nodes.push(g);
    });
    return nodes;
  }

  // ---------------------------------------------------------------- website
  function render(data) {
    document.querySelectorAll("[data-ph-count]").forEach((n) => { n.textContent = data.counts[n.dataset.phCount]; });
    if (!document.querySelector('link[href="phenomena.css"]')) {
      document.head.appendChild(html("link", { rel: "stylesheet", href: "phenomena.css" }));
    }
    const leg = $("#ph-legend");
    if (leg) data.valences.forEach(([k, label]) => {
      const item = html("span", { class: "ph-legend-item" });
      item.appendChild(html("span", { class: `ph-dot ph-${VAL[k]} ph-legdot` }));
      item.appendChild(html("span", {}, label));
      leg.appendChild(item);
    });

    const incByKey = Object.fromEntries(data.incidents.map((x) => [x.key, x]));
    const matrix = $("#ph-matrix");
    if (!matrix) return;
    matrix.textContent = "";
    matrix.setAttribute("role", "table");

    const head = html("div", { class: "ph-head", role: "row" });
    head.appendChild(html("div", { class: "ph-label ph-headlabel", role: "columnheader" }, "Group-level phenomenon"));
    data.substrates.forEach(([, label]) => head.appendChild(html("div", { class: "ph-cell ph-headcell", role: "columnheader" }, label)));
    head.appendChild(html("div", { class: "ph-caret", "aria-hidden": "true" }));
    matrix.appendChild(head);

    let split = false;
    data.types.forEach((t) => {
      if (t.valence === "harmful" && !split) {
        split = true;
        matrix.appendChild(html("div", { class: "ph-band" }, "Where it goes wrong"));
      }
      matrix.appendChild(rowFor(t, incByKey));
    });

    const radial = buildRadial(data, incByKey, matrix);
    // open a row from the URL hash (#ph-<key>), a shareable permalink, in the list view
    const key = (location.hash.match(/^#ph-(.+)$/) || [])[1];
    if (key) radial.openInList(key);
  }

  function rowFor(t, incByKey) {
    const row = html("div", { class: "ph-row", id: `ph-${t.key}` });
    const btn = html("button", { class: "ph-rowhead", type: "button", "aria-expanded": "false" });
    const lab = html("div", { class: "ph-label" });
    lab.appendChild(html("span", { class: `ph-chip ph-${VAL[t.valence]}`, "aria-hidden": "true" }));
    lab.appendChild(html("span", { class: "ph-name" }, t.label));
    btn.appendChild(lab);
    ["human", "marl", "llm"].forEach((s) => btn.appendChild(dotCell(t.counts[s], t.valence)));
    btn.appendChild(html("span", { class: "ph-caret", "aria-hidden": "true" }, "›"));

    const detail = html("div", { class: "ph-detail" });
    detail.hidden = true;
    buildDetail(detail, t, incByKey);
    btn.addEventListener("click", () => {
      const opening = detail.hidden;
      detail.hidden = !opening;
      btn.setAttribute("aria-expanded", String(opening));
      row.classList.toggle("ph-open", opening);
    });
    row.appendChild(btn);
    row.appendChild(detail);
    return row;
  }

  function dotCell(count, val) {
    const cell = html("div", { class: "ph-cell", role: "cell" });
    if (count) {
      const sz = Math.round(20 + 6 * Math.sqrt(count));
      cell.appendChild(html("span", { class: `ph-dot ph-${VAL[val]}`, style: `--sz:${sz}px` }, String(count)));
    } else {
      cell.appendChild(html("span", { class: "ph-dot ph-empty", "aria-label": "none" }));
    }
    return cell;
  }

  function buildDetail(detail, t, incByKey) {
    detail.appendChild(html("p", { class: "ph-desc" }, t.description));
    ["llm", "marl", "human"].forEach((s) => {
      const rows = (t.sources[s] || []);
      if (!rows.length) return;
      const g = html("div", { class: "ph-group" });
      g.appendChild(html("h4", {}, `${GROUPLAB[s]} (${rows.length})`));
      const ul = html("ul", { class: "ph-sources" });
      rows.forEach((src, i) => {
        const li = html("li");
        if (i >= SHOW_FIRST) li.hidden = true;
        li.appendChild(src.url ? html("a", { href: src.url, target: "_blank", rel: "noopener" }, src.title) : html("span", {}, src.title));
        const meta = [src.authors, src.year, src.venue].filter(Boolean).join(" · ");
        if (meta) li.appendChild(html("span", { class: "ph-meta" }, meta));
        ul.appendChild(li);
      });
      g.appendChild(ul);
      if (rows.length > SHOW_FIRST) {
        const more = html("button", { class: "ph-more", type: "button" }, `Show all ${rows.length}`);
        more.addEventListener("click", () => { ul.querySelectorAll("li[hidden]").forEach((li) => { li.hidden = false; }); more.remove(); });
        g.appendChild(more);
      }
      detail.appendChild(g);
    });
    const incs = (t.incidents || []).map((k) => incByKey[k]).filter(Boolean);
    if (incs.length) {
      const g = html("div", { class: "ph-group ph-wild" });
      g.appendChild(html("h4", {}, "Documented in the wild"));
      const ul = html("ul", { class: "ph-incidents" });
      incs.forEach((inc) => {
        const li = html("li");
        li.appendChild(inc.url ? html("a", { href: inc.url, target: "_blank", rel: "noopener" }, inc.short) : html("span", {}, inc.short));
        if (inc.year) li.appendChild(html("span", { class: "ph-meta" }, inc.year));
        ul.appendChild(li);
      });
      g.appendChild(ul);
      detail.appendChild(g);
    }
    detail.appendChild(html("a", { class: "ph-permalink", href: `#ph-${t.key}` }, "Link to this phenomenon"));
  }

  // ---------------------------------------------------------------- website: the radial map and the view toggle
  function buildRadial(data, incByKey, matrix) {
    const legend = $("#ph-legend"), hint = $(".ph-hint");
    const bar = html("div", { class: "ph-toolbar", role: "toolbar", "aria-label": "Phenomena view" });
    const toggle = html("button", { class: "tx-btn tx-btn-primary", type: "button", "aria-pressed": "false" }, "Unravel into a list");
    bar.appendChild(toggle);
    const wrapEl = html("div", { class: "ph-radial-wrap" });
    const stage = html("div", { class: "ph-radial", id: "ph-radial" });
    const panel = html("aside", { class: "ph-rpanel", "aria-live": "polite" });
    wrapEl.appendChild(stage); wrapEl.appendChild(panel);
    matrix.parentNode.insertBefore(bar, legend || matrix);
    matrix.parentNode.insertBefore(wrapEl, matrix);

    const svg = svgEl("svg", { viewBox: "0 0 1200 925", "font-family": FONT, role: "img", class: "ph-rsvg",
      "aria-label": "Radial map of group-level phenomena by type and kind of agent" }, stage);
    const nodes = radialMap(svg, data, { fs: 1, idp: "ph-", ringKey: true, interactive: true });

    const intro = () => {
      panel.style.removeProperty("--c");
      panel.innerHTML = `<p class="ph-plabel">Explore</p><h3>Ten patterns that emerge</h3><p>Each spoke is one phenomenon type; the rings hold the instances studied with humans, MARL agents, and LLM agents. Hover, tap, or tab to a spoke.</p>`;
    };
    let locked = null;
    const show = (key) => {
      svg.classList.toggle("has-active", !!key);
      nodes.forEach((n) => n.classList.toggle("is-on", n.dataset.key === key));
      const t = data.types.find((d) => d.key === key);
      if (!t) return intro();
      const c = VC[t.valence];
      panel.style.setProperty("--c", c[0]);
      const incs = (t.incidents || []).map((k) => incByKey[k]).filter(Boolean);
      const sub = SUBS.map(([k, lab]) => `<span><strong>${t.counts[k]}</strong> ${lab}</span>`).join("");
      panel.innerHTML = `<p class="ph-plabel">${t.valence === "harmful" ? "Where it goes wrong" : "What agent groups build"}</p><h3>${t.label}</h3>` +
        `<p>${t.description}</p><p class="ph-rcounts">${sub}</p>` +
        (incs.length ? `<p class="ph-rinc"><strong>In the wild:</strong> ${incs.map((i) => i.short).join("; ")}.</p>` : "");
      const open = html("button", { class: "tx-btn", type: "button" }, "Open the papers ›");
      open.addEventListener("click", () => openInList(t.key));
      panel.appendChild(open);
    };
    nodes.forEach((n) => {
      const key = n.dataset.key;
      n.addEventListener("pointerenter", () => show(key));
      n.addEventListener("pointerleave", () => show(locked));
      n.addEventListener("focus", () => show(key));
      n.addEventListener("blur", () => show(locked));
      n.addEventListener("click", (e) => { e.stopPropagation(); locked = locked === key ? null : key; show(locked || key); });
      n.addEventListener("keydown", (e) => { if (e.key === "Enter" || e.key === " ") { e.preventDefault(); locked = key; show(key); } });
    });
    svg.addEventListener("click", () => { locked = null; show(null); });
    intro();

    const HINT_MAP = "Hover or tap a spoke to read about it; open the papers from the panel, or unravel the map into a list.";
    const HINT_LIST = hint ? hint.textContent : "";
    const setView = (list) => {
      wrapEl.hidden = list;
      matrix.hidden = !list;
      if (legend) legend.hidden = !list;
      toggle.setAttribute("aria-pressed", String(list));
      toggle.textContent = list ? "Show as a map" : "Unravel into a list";
      if (hint) hint.textContent = list ? HINT_LIST : HINT_MAP;
    };
    toggle.addEventListener("click", () => setView(!matrix.hidden ? false : true));
    // on phones the list reads better than a small map
    setView(!!(window.matchMedia && window.matchMedia("(max-width: 640px)").matches));

    function openInList(key) {
      setView(true);
      const target = matrix.querySelector(`#ph-${CSS.escape(key)} .ph-rowhead`);
      if (target) {
        if (target.getAttribute("aria-expanded") !== "true") target.click();
        target.scrollIntoView({ block: "center", behavior: "smooth" });
      }
    }
    return { openInList };
  }
})();
