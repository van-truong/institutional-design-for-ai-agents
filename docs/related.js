/* Related efforts (website only): a connected-papers style map and a reading list, both from assets/related.json.
   Topics from our framework sit on a ring; each paper, testbed, program, or policy paper is a dot pulled toward
   the topics it speaks to, so neighbors share topics. Filled dots are cited in the paper; open dots are related
   work we have read but not cited. Hover or focus a dot or a topic to light up its links; click for details.
   The "adjacent" entries (agent capabilities and infrastructure) appear only in the reading list. */
(function () {
  const stage = document.getElementById("rel-stage");
  if (!stage) return;
  const panel = document.getElementById("rel-panel");
  const listHost = document.getElementById("rel-list");
  const NS = "http://www.w3.org/2000/svg";
  const FONT = "'Helvetica Neue', Arial, sans-serif";
  const PAPER_C = "#7c1948", REL_C = "#2F5D8F", PROG_C = "#C79A3A";
  const el = (tag, a = {}, p) => { const n = document.createElementNS(NS, tag); for (const [k, v] of Object.entries(a)) n.setAttribute(k, v); if (p) p.appendChild(n); return n; };
  const html = (tag, cls, txt) => { const n = document.createElement(tag); if (cls) n.className = cls; if (txt !== undefined) n.textContent = txt; return n; };
  const dotColor = (it) => (it.kind === "program" || it.kind === "policy") ? PROG_C : it.status === "paper" ? PAPER_C : REL_C;

  fetch("assets/related.json").then((r) => r.json()).then(draw).catch(() => {
    stage.textContent = "The map could not be loaded.";
  });

  function draw(data) {
    const C = Object.fromEntries(data.concepts.map((c) => [c.id, c]));
    const items = data.items;
    const checked = document.getElementById("rel-checked");
    if (checked) {
      const d = new Date(data.checked + "T12:00:00");
      checked.dateTime = data.checked;
      checked.textContent = d.toLocaleDateString(undefined, { year: "numeric", month: "long", day: "numeric" });
    }

    // ---- layout: topics on an ellipse, items relaxed by a small deterministic force simulation
    const W = 1000, H = 660, cx = W / 2, cy = H / 2 + 4, RX = 410, RY = 262;
    const hubs = data.concepts.map((c, i) => {
      const a = -Math.PI / 2 + (i / data.concepts.length) * 2 * Math.PI;
      return { ...c, x: cx + RX * Math.cos(a), y: cy + RY * Math.sin(a), hw: (c.label.length * 7.6 + 26) / 2 };
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
          const f = (d - 95) * 0.012;
          fx += (dx / d) * f; fy += (dy / d) * f;
        }
        for (const m of nodes) {                     // dots keep apart
          if (m === n) continue;
          const dx = n.x - m.x, dy = n.y - m.y, d2 = dx * dx + dy * dy + 0.01, d = Math.sqrt(d2);
          if (d < 90) { const f = 420 / d2; fx += (dx / d) * f; fy += (dy / d) * f; }
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
    const boxes = hubs.map((h) => [h.x - h.hw - 3, h.y - 17, h.x + h.hw + 3, h.y + 17]);
    nodes.forEach((n) => boxes.push([n.x - 8, n.y - 8, n.x + 8, n.y + 8]));
    const hit = (b) => boxes.some((o) => b[0] < o[2] && b[2] > o[0] && b[1] < o[3] && b[3] > o[1]);
    [...nodes].sort((a, b) => (a.it.status === "paper" ? 0 : 1) - (b.it.status === "paper" ? 0 : 1)).forEach((n) => {
      const w = n.it.short.length * 6.5 + 2;
      const spots = [
        { x: n.x + 11, y: n.y + 4, anchor: "start", b: [n.x + 10, n.y - 7, n.x + 11 + w, n.y + 7] },
        { x: n.x - 11, y: n.y + 4, anchor: "end", b: [n.x - 11 - w, n.y - 7, n.x - 10, n.y + 7] },
        { x: n.x, y: n.y - 12, anchor: "middle", b: [n.x - w / 2, n.y - 23, n.x + w / 2, n.y - 9] },
        { x: n.x, y: n.y + 21, anchor: "middle", b: [n.x - w / 2, n.y + 10, n.x + w / 2, n.y + 24] },
      ].filter((sp) => sp.b[0] > 2 && sp.b[2] < W - 2);
      const own = boxes.findIndex((o) => o[0] === n.x - 8 && o[1] === n.y - 8);
      const mine = boxes.splice(own, 1)[0];
      const ok = spots.find((sp) => !hit(sp.b));
      boxes.push(mine);
      if (ok) { n.lab = ok; boxes.push(ok.b); }
    });

    // ---- drawing
    const svg = el("svg", { viewBox: `0 0 ${W} ${H}`, class: "rel-svg", role: "img", "font-family": FONT, "aria-labelledby": "rel-title rel-desc" }, stage);
    el("title", { id: "rel-title" }, svg).textContent = "Map of related work";
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
      el("rect", { x: h.x - tw / 2, y: h.y - 15, width: tw, height: 30, rx: 15, fill: "#fff", stroke: h.c, "stroke-width": 2 }, g);
      const t = el("text", { x: h.x, y: h.y + 4.6, "text-anchor": "middle", "font-size": 13.5, "font-weight": 800, fill: h.c }, g);
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
      const lab = el("text", { x: lp ? lp.x : n.x + 11, y: lp ? lp.y : n.y + 4, "text-anchor": lp ? lp.anchor : "start", "font-size": 11.5, "font-weight": 700, fill: "#2C2C2A", class: lp ? "rel-label" : "rel-label rel-label-hover" }, g);
      lab.textContent = it.short;
      n.g = g;
      g.addEventListener("mouseenter", () => focusNode(n));
      g.addEventListener("focus", () => focusNode(n));
      g.addEventListener("mouseleave", clearFocus);
      g.addEventListener("blur", clearFocus);
      g.addEventListener("click", () => showItem(it));
      g.addEventListener("keydown", (e) => { if (e.key === "Enter" || e.key === " ") { e.preventDefault(); showItem(it); } });
    });

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
