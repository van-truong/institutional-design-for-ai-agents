/* Mind map of related efforts: a connected-papers style map and a reading list, both from assets/related.json.
   Topics from our framework sit on a ring; each paper, testbed, program, or policy paper is a dot pulled toward
   the topics it speaks to, so neighbors share topics. Filled dots are cited in the paper; open dots are related
   work we have read but not cited. Hover or focus a dot or a topic to light up its links; click for details.
   The "adjacent" entries (agent capabilities and infrastructure) appear only in the reading list.
   Paper mode (data-variant="paper", manuscript/figs/related-paper.html): a static print with a title and legend,
   larger type, and labels only on cited work; the open dots are named on the site. */
(function () {
  const stage = document.getElementById("rel-stage");
  if (!stage) return;
  const PAPER = stage.dataset.variant === "paper";
  const FS = PAPER ? { hub: 22, item: 20, title: 29, key: 20 } : { hub: 13.5, item: 11.5 };
  const panel = document.getElementById("rel-panel");
  const listHost = document.getElementById("rel-list");
  const NS = "http://www.w3.org/2000/svg";
  const FONT = "'Helvetica Neue', Arial, sans-serif";
  const PAPER_C = "#7c1948", REL_C = "#2F5D8F", PROG_C = "#C79A3A";
  const el = (tag, a = {}, p) => { const n = document.createElementNS(NS, tag); for (const [k, v] of Object.entries(a)) n.setAttribute(k, v); if (p) p.appendChild(n); return n; };
  const html = (tag, cls, txt) => { const n = document.createElement(tag); if (cls) n.className = cls; if (txt !== undefined) n.textContent = txt; return n; };
  // text widths measured in the browser, so pills and label boxes fit the real type
  const ruler = el("svg", { width: 0, height: 0, style: "position:absolute;visibility:hidden" }, document.body);
  const measure = (str, fs, weight) => {
    const t = el("text", { "font-size": fs, "font-weight": weight, "font-family": FONT }, ruler);
    t.textContent = str; const w = t.getComputedTextLength(); t.remove(); return w;
  };
  const dotColor = (it) => (it.kind === "program" || it.kind === "policy") ? PROG_C : it.status === "paper" ? PAPER_C : REL_C;

  fetch(stage.dataset.src || "assets/related.json").then((r) => r.json()).then(draw).catch(() => {
    stage.textContent = "The map could not be loaded.";
  });

  function draw(data) {
    const C = Object.fromEntries(data.concepts.map((c) => [c.id, c]));
    const items = data.items;
    const checked = PAPER ? null : document.getElementById("rel-checked");
    if (checked) {
      const d = new Date(data.checked + "T12:00:00");
      checked.dateTime = data.checked;
      checked.textContent = d.toLocaleDateString(undefined, { year: "numeric", month: "long", day: "numeric" });
    }

    // ---- layout: topics on an ellipse, items relaxed by a small deterministic force simulation
    const W = PAPER ? 1240 : 1000, H = PAPER ? 820 : 660, cx = W / 2, cy = H / 2 + 4;
    const hwOf = (c) => (measure(c.label, FS.hub, 800) + 26) / 2;
    const maxHW = Math.max(...data.concepts.map(hwOf));
    const RX = W / 2 - maxHW - 8, RY = H / 2 - FS.hub - 12;
    const hubs = data.concepts.map((c, i) => {
      const a = -Math.PI / 2 + (i / data.concepts.length) * 2 * Math.PI;
      return { ...c, x: cx + RX * Math.cos(a), y: cy + RY * Math.sin(a), hw: hwOf(c) };
    });
    const H_ = Object.fromEntries(hubs.map((h) => [h.id, h]));
    let seed = 7;
    const rand = () => ((seed = (seed * 16807) % 2147483647) / 2147483647);
    const nodes = items.map((it) => {
      const hs = it.concepts.map((k) => H_[k]);
      const mx = hs.reduce((s, h) => s + h.x, 0) / hs.length, my = hs.reduce((s, h) => s + h.y, 0) / hs.length;
      // single-topic items start part of the way in from their topic; multi-topic ones near their centroid
      const pull = hs.length === 1 ? 0.78 : 0.92;
      return { it, x: cx + (mx - cx) * pull + (rand() - 0.5) * 30, y: cy + (my - cy) * pull + (rand() - 0.5) * 30 };
    });
    for (let step = 0; step < 420; step++) {
      const cool = 1 - step / 460;
      for (const n of nodes) {
        let fx = 0, fy = 0;
        for (const k of n.it.concepts) {            // springs to each topic
          const h = H_[k], dx = h.x - n.x, dy = h.y - n.y, d = Math.hypot(dx, dy) || 1;
          const f = (d - (PAPER ? 130 : 95)) * 0.012;
          fx += (dx / d) * f; fy += (dy / d) * f;
        }
        for (const m of nodes) {                     // dots keep apart
          if (m === n) continue;
          const dx = n.x - m.x, dy = n.y - m.y, d2 = dx * dx + dy * dy + 0.01, d = Math.sqrt(d2);
          const R0 = PAPER ? 120 : 90, K = PAPER ? 900 : 420;
          if (d < R0) { const f = K / d2; fx += (dx / d) * f; fy += (dy / d) * f; }
        }
        for (const h of hubs) {                      // and clear of the whole topic label
          const ux = (n.x - h.x) / (h.hw + 16), uy = (n.y - h.y) / 30, d = Math.hypot(ux, uy) || 0.01;
          if (d < 1) { const f = (1 - d) * 9; fx += (ux / d) * f; fy += (uy / d) * f * 0.6; }
        }
        fx += (cx - n.x) * 0.0015; fy += (cy - n.y) * 0.0015;
        n.x = Math.max(24, Math.min(W - 24, n.x + fx * 4 * cool));
        n.y = Math.max(24, Math.min(H - 24, n.y + fy * 4 * cool));
      }
    }

    // ---- label spots, cited work first
    const LH = FS.item * 0.62, hh = FS.hub * 0.8 + 6;
    const boxes = hubs.map((h) => [h.x - h.hw - 3, h.y - hh, h.x + h.hw + 3, h.y + hh]);
    nodes.forEach((n) => boxes.push([n.x - 8, n.y - 8, n.x + 8, n.y + 8]));
    const hit = (b) => boxes.some((o) => b[0] < o[2] && b[2] > o[0] && b[1] < o[3] && b[3] > o[1]);
    [...nodes].sort((a, b) => (a.it.status === "paper" ? 0 : 1) - (b.it.status === "paper" ? 0 : 1)).forEach((n) => {
      if (PAPER && n.it.status !== "paper") return;
      const w = measure(n.it.short, FS.item, 700) + 2, up = FS.item * 0.35;
      const spots = [];
      for (const far of PAPER ? [0, 36, 72] : [0, 24]) for (const dy of (PAPER ? [0, -1.4, 1.4, -2.8, 2.8, -4.2, 4.2] : [0, -1.4, 1.4, -2.8, 2.8]).map((k) => k * LH)) {
        const off = dy || far ? 6 + far : 0;   // a label moved off its dot sits further out, joined by a leader
        const lead = !!(dy || far);
        spots.push({ x: n.x + 11 + off, y: n.y + up + dy, anchor: "start", lead, b: [n.x + 10 + off, n.y + dy - LH, n.x + 11 + off + w, n.y + dy + LH] });
        spots.push({ x: n.x - 11 - off, y: n.y + up + dy, anchor: "end", lead, b: [n.x - 11 - off - w, n.y + dy - LH, n.x - 10 - off, n.y + dy + LH] });
      }
      spots.push({ x: n.x, y: n.y - 11, anchor: "middle", b: [n.x - w / 2, n.y - 11 - 2 * LH, n.x + w / 2, n.y - 9] });
      spots.push({ x: n.x, y: n.y + 11 + 2 * LH, anchor: "middle", b: [n.x - w / 2, n.y + 10, n.x + w / 2, n.y + 12 + 2 * LH] });
      for (let i = spots.length - 1; i >= 0; i--) if (!(spots[i].b[0] > 2 && spots[i].b[2] < W - 2)) spots.splice(i, 1);
      const own = boxes.findIndex((o) => o[0] === n.x - 8 && o[1] === n.y - 8);
      const mine = boxes.splice(own, 1)[0];
      const ok = spots.find((sp) => !hit(sp.b));
      boxes.push(mine);
      // if every spot collides (paper only), take the one that overlaps least
      const overlap = (b) => boxes.reduce((t, o) => t + Math.max(0, Math.min(b[2], o[2]) - Math.max(b[0], o[0])) * Math.max(0, Math.min(b[3], o[3]) - Math.max(b[1], o[1])), 0);
      const pick = ok || (PAPER ? spots.reduce((m, sp) => (overlap(sp.b) < overlap(m.b) ? sp : m), spots[0]) : null);
      if (pick) { n.lab = pick; boxes.push(pick.b); }
    });

    // ---- drawing
    const TOP = PAPER ? 62 : 0, BOT = PAPER ? 56 : 0;
    const svg = el("svg", { viewBox: `0 ${-TOP} ${W} ${H + TOP + BOT}`, class: "rel-svg", role: "img", "font-family": FONT, "aria-labelledby": "rel-title rel-desc" }, stage);
    el("title", { id: "rel-title" }, svg).textContent = "Mind map of related efforts";
    el("desc", { id: "rel-desc" }, svg).textContent =
      `${items.length} papers, testbeds, programs, and policy papers, each linked to the topics from our framework that it addresses. The same entries are listed below the map.`;
    const gEdges = el("g", { class: "rel-edges" }, svg);
    const gHubs = el("g", { class: "rel-hubs" }, svg);
    const gNodes = el("g", { class: "rel-nodes" }, svg);
    const edges = [];
    nodes.forEach((n) => n.it.concepts.forEach((k) => {
      const h = H_[k];
      const ln = el("line", { x1: n.x, y1: n.y, x2: h.x, y2: h.y, stroke: h.c, "stroke-width": 1.1, opacity: 0.22 }, gEdges);
      edges.push({ ln, n, k });
    }));
    hubs.forEach((h) => {
      const g = el("g", { class: "rel-hub", tabindex: 0, role: "button", "aria-label": `${h.full}: show linked work` }, gHubs);
      const tw = h.hw * 2;
      el("rect", { x: h.x - tw / 2, y: h.y - hh + 2, width: tw, height: 2 * hh - 4, rx: hh - 2, fill: "#fff", stroke: h.c, "stroke-width": 2 }, g);
      const t = el("text", { x: h.x, y: h.y + FS.hub * 0.34, "text-anchor": "middle", "font-size": FS.hub, "font-weight": 800, fill: h.c }, g);
      t.textContent = h.label;
      h.g = g;
      g.addEventListener("mouseenter", () => focusHub(h));
      g.addEventListener("focus", () => focusHub(h));
      g.addEventListener("mouseleave", clearFocus);
      g.addEventListener("blur", clearFocus);
      g.addEventListener("click", () => showHub(h));
      g.addEventListener("keydown", (e) => { if (e.key === "Enter" || e.key === " ") { e.preventDefault(); showHub(h); } });
    });
    nodes.forEach((n) => {
      const it = n.it, col = dotColor(it), filled = it.status === "paper" || it.kind === "program" || it.kind === "policy";
      const g = el("g", { class: "rel-node", tabindex: 0, role: "button", "aria-label": `${it.short}: details` }, gNodes);
      g.dataset.status = it.status;
      el("circle", { cx: n.x, cy: n.y, r: 13, fill: "transparent" }, g);          // larger touch target
      if (it.kind === "program" || it.kind === "policy")
        el("rect", { x: n.x - 6.5, y: n.y - 6.5, width: 13, height: 13, transform: `rotate(45 ${n.x} ${n.y})`, fill: col, stroke: "#fff", "stroke-width": 1.5 }, g);
      else
        el("circle", { cx: n.x, cy: n.y, r: 7, fill: filled ? col : "#fff", stroke: col, "stroke-width": filled ? 1.5 : 2.4 }, g);
      const lp = n.lab;
      if (PAPER && !lp) return;
      if (lp && lp.lead) {
        const lx = lp.anchor === "start" ? lp.b[0] : lp.b[2], ly = (lp.b[1] + lp.b[3]) / 2;
        el("line", { x1: n.x, y1: n.y, x2: lx, y2: ly, stroke: "#8A8A8A", "stroke-width": 1.2 }, g).parentNode.insertBefore(g.lastChild, g.firstChild);
      }
      const lab = el("text", { x: lp ? lp.x : n.x + 11, y: lp ? lp.y : n.y + 4, "text-anchor": lp ? lp.anchor : "start", "font-size": FS.item, "font-weight": 700, fill: "#2C2C2A", class: lp ? "rel-label" : "rel-label rel-label-hover" }, g);
      if (PAPER) { lab.setAttribute("paint-order", "stroke"); lab.setAttribute("stroke", "#fff"); lab.setAttribute("stroke-width", 4); lab.setAttribute("stroke-linejoin", "round"); }
      lab.textContent = it.short;
      n.g = g;
      g.addEventListener("mouseenter", () => focusNode(n));
      g.addEventListener("focus", () => focusNode(n));
      g.addEventListener("mouseleave", clearFocus);
      g.addEventListener("blur", clearFocus);
      g.addEventListener("click", () => showItem(it));
      g.addEventListener("keydown", (e) => { if (e.key === "Enter" || e.key === " ") { e.preventDefault(); showItem(it); } });
    });

    if (PAPER) { paperFrame(svg); return; }
    function paperFrame(svg) {
      const t = el("text", { x: W / 2, y: -20, "text-anchor": "middle", "font-size": FS.title, "font-weight": 700, fill: "#2C2C2A" }, svg);
      t.textContent = "Mind map of related efforts";
      const keys = [["paper", "Cited in this paper"], ["related", "Related work, named on the companion site"], ["prog", "Programs and policy"]];
      const widths = keys.map(([, l]) => measure(l, FS.key, 400) + 24);
      let x = (W - widths.reduce((a, b) => a + b, 0) - 30 * (keys.length - 1)) / 2;
      const y = H + 30;
      keys.forEach(([k, l], i) => {
        if (k === "prog") el("rect", { x: x + 2, y: y - 7, width: 12, height: 12, transform: `rotate(45 ${x + 8} ${y - 1})`, fill: PROG_C }, svg);
        else el("circle", { cx: x + 8, cy: y - 1, r: 7, fill: k === "paper" ? PAPER_C : "#fff", stroke: k === "paper" ? PAPER_C : REL_C, "stroke-width": k === "paper" ? 1.5 : 2.4 }, svg);
        const tx = el("text", { x: x + 22, y: y + FS.key * 0.33, "font-size": FS.key, fill: "#2C2C2A" }, svg);
        tx.textContent = l;
        x += widths[i] + 30;
      });
    }

    // ---- highlighting
    const active = { paper: true, related: true };
    const visible = (it) => active[it.status];
    function paint(onNodes, onHubs) {
      svg.classList.toggle("rel-dim", !!onNodes);
      nodes.forEach((n) => {
        const show = visible(n.it);
        n.g.style.display = show ? "" : "none";
        n.g.classList.toggle("on", !!onNodes && onNodes.has(n));
      });
      hubs.forEach((h) => h.g.classList.toggle("on", !!onHubs && onHubs.has(h.id)));
      edges.forEach((e) => {
        const show = visible(e.n.it), on = !!onNodes && onNodes.has(e.n) && (!onHubs || onHubs.has(e.k));
        e.ln.style.display = show ? "" : "none";
        e.ln.setAttribute("opacity", on ? 0.85 : onNodes ? 0.06 : 0.22);
        e.ln.setAttribute("stroke-width", on ? 2 : 1.1);
      });
    }
    function focusNode(n) { paint(new Set([n]), new Set(n.it.concepts)); }
    function focusHub(h) { paint(new Set(nodes.filter((n) => n.it.concepts.includes(h.id) && visible(n.it))), new Set([h.id])); }
    function clearFocus() { paint(null, null); }

    // ---- detail panel
    function chips(ids) {
      const w = html("div", "rel-chips");
      ids.forEach((k) => { const s = html("span", "rel-chip", C[k].label); s.style.setProperty("--c", C[k].c); w.appendChild(s); });
      return w;
    }
    function badge(it) {
      const label = it.kind === "program" ? "Program" : it.kind === "policy" ? "Policy" : it.status === "paper" ? "Cited in the paper" : "Related, not cited";
      const b = html("span", "rel-badge", label);
      b.style.setProperty("--c", dotColor(it));
      return b;
    }
    function showItem(it) {
      panel.replaceChildren();
      panel.appendChild(badge(it));
      const h = html("h4", "rel-p-title");
      const a = html("a", "", it.title); a.href = it.url; a.target = "_blank"; a.rel = "noopener";
      h.appendChild(a); panel.appendChild(h);
      panel.appendChild(html("p", "rel-p-meta", `${it.who} · ${it.venue}`));
      panel.appendChild(html("p", "rel-p-note", it.note));
      panel.appendChild(chips(it.concepts));
    }
    function showHub(h) {
      panel.replaceChildren();
      const t = html("h4", "rel-p-title", h.full); t.style.color = h.c; panel.appendChild(t);
      const these = items.filter((it) => it.concepts.includes(h.id) && visible(it));
      panel.appendChild(html("p", "rel-p-meta", `${these.length} linked ${these.length === 1 ? "entry" : "entries"}`));
      const ul = html("ul", "rel-p-list");
      these.forEach((it) => {
        const li = html("li"); const b = html("button", "rel-linkbtn", it.short);
        b.style.setProperty("--c", dotColor(it));
        b.addEventListener("click", () => showItem(it));
        li.appendChild(b); ul.appendChild(li);
      });
      panel.appendChild(ul);
    }
    function resetPanel() {
      panel.replaceChildren(html("p", "rel-p-hint", "Hover over or tap a dot to see what it is, or a topic to see everything linked to it."));
    }
    resetPanel();

    // ---- filters
    document.querySelectorAll("[data-rel-filter]").forEach((b) => {
      const k = b.dataset.relFilter;
      const n = items.filter((it) => it.status === k).length;
      b.querySelector(".rel-count").textContent = `(${n})`;
      b.addEventListener("click", () => {
        active[k] = !active[k];
        if (!active.paper && !active.related) { active[k === "paper" ? "related" : "paper"] = true; }
        document.querySelectorAll("[data-rel-filter]").forEach((x) => x.setAttribute("aria-pressed", active[x.dataset.relFilter]));
        clearFocus(); resetPanel();
      });
    });

    // ---- reading list
    if (listHost) {
      const groups = [
        ["Related work we have read but not cited", items.filter((it) => it.status === "related" && it.kind !== "program" && it.kind !== "policy")],
        ["Programs and policy", items.filter((it) => it.kind === "program" || it.kind === "policy")],
        ["Cited in the paper", items.filter((it) => it.status === "paper")],
      ];
      groups.forEach(([title, list]) => {
        const sec = html("div", "rel-group");
        sec.appendChild(html("h4", "rel-group-title", `${title} (${list.length})`));
        const ul = html("ul", "rel-items");
        list.forEach((it) => ul.appendChild(entry(it, true)));
        sec.appendChild(ul); listHost.appendChild(sec);
      });
      const det = html("details", "rel-adjacent");
      det.appendChild(html("summary", "", `Adjacent reading: agent capabilities and infrastructure (${data.adjacent.length})`));
      det.appendChild(html("p", "rel-adj-note", "Useful background on what single agents can do, but not about how groups of agents are governed. Not shown in the map."));
      const ul = html("ul", "rel-items");
      data.adjacent.forEach((it) => ul.appendChild(entry(it, false)));
      det.appendChild(ul); listHost.appendChild(det);
    }
    function entry(it, withChips) {
      const li = html("li", "rel-item");
      const a = html("a", "rel-item-title", it.title); a.href = it.url; a.target = "_blank"; a.rel = "noopener";
      li.appendChild(a);
      li.appendChild(html("span", "rel-item-meta", ` — ${it.who}, ${it.venue}`));
      li.appendChild(html("p", "rel-item-note", it.note));
      if (withChips) li.appendChild(chips(it.concepts));
      return li;
    }
  }
})();
