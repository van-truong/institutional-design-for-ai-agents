// Interactive taxonomy: a radial tree that unravels into the paper's list layout (Fig. 4).
// Data: assets/taxonomy.json, built by taxonomy/scripts/build_site_data.py from the coded dataset.

const SVG_NS = "http://www.w3.org/2000/svg";
const R = { hub: 52, fam: 135, theme: 215, leaf: 290 };
const LIST = { colW: 470, colGap: 44, famRow: 42, themeRow: 31, leafRow: 26, themeGap: 9, famGap: 24 };
// Text grows as the circle unravels, so the list reads at a comfortable size.
const FONT = { leaf: [12.5, 15], theme: [13, 15.5], fam: [15, 17.5] };
// Hand-placed nudges for family labels in the circle, to keep them off the branches.
const FAM_NUDGE = { normative: [-20, -12], incentive: [18, 12] };
const EVIDENCE_LABEL = { tested: "Tested with LLM agents", proposed: "Proposed for LLM agents only", none: "No LLM-agent study yet" };
const GROUPS = [["llm", "LLM-agent studies"], ["marl", "Multi-agent reinforcement learning"], ["other", "Other fields and systems"]];
const SHOW_FIRST = 8;

const stage = document.querySelector("#tx-stage");
const panel = document.querySelector("#tx-panel");
const toggle = document.querySelector("#tx-toggle");
const search = document.querySelector("#tx-search");
const filterButtons = [...document.querySelectorAll("[data-tx-filter]")];
const counter = document.querySelector("#tx-count");
const textList = document.querySelector("#tx-text-list");
const reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

let data, nodes = [], links = [], selected = null, t = 0, filter = "all", narrow = false;

const el = (name, attrs = {}, parent) => {
  const node = document.createElementNS(SVG_NS, name);
  for (const [k, v] of Object.entries(attrs)) node.setAttribute(k, v);
  if (parent) parent.appendChild(node);
  return node;
};
const html = (tag, attrs = {}, text) => {
  const node = document.createElement(tag);
  for (const [k, v] of Object.entries(attrs)) node.setAttribute(k, v);
  if (text !== undefined) node.textContent = text;
  return node;
};
const lerp = (a, b, k) => a + (b - a) * k;
const ease = (k) => (k < 0.5 ? 4 * k * k * k : 1 - Math.pow(-2 * k + 2, 3) / 2);
const polar = (deg, r) => ({ x: r * Math.cos((deg * Math.PI) / 180), y: r * Math.sin((deg * Math.PI) / 180) });
const pretty = (d) => (d === "ai ml" ? "AI/ML" : d.replace(/\b\w/g, (c) => c.toUpperCase()));

function layout() {
  const families = data.families;
  const leaves = families.flatMap((f) => f.themes.flatMap((th) => th.mechanisms.map((m) => ({ f, th, m }))));
  const slots = leaves.length + families.length * 1.6;
  const step = 360 / slots;
  let slot = 0.8;
  const radial = new Map();
  families.forEach((f) => {
    f.themes.forEach((th) => {
      th.mechanisms.forEach((m) => { radial.set(m.id, -90 + slot * step); slot += 1; });
    });
    slot += 1.6;
  });

  const list = new Map();
  const colY = [0, 0];
  const columns = narrow ? [data.columns.flat()] : data.columns;
  columns.forEach((col, c) => {
    const x0 = c * (LIST.colW + LIST.colGap);
    let y = 0;
    col.forEach((fid) => {
      const f = families.find((x) => x.id === fid);
      list.set(f.id, { x: x0 + 4, y: y + 10 });
      y += LIST.famRow;
      f.themes.forEach((th) => {
        list.set(th.id, { x: x0 + 16, y: y + 8 });
        y += LIST.themeRow;
        th.mechanisms.forEach((m) => { list.set(m.id, { x: x0 + 34, y: y + 6 }); y += LIST.leafRow; });
        y += LIST.themeGap;
      });
      y += LIST.famGap;
    });
    colY[c] = y;
  });
  const listH = Math.max(...colY);

  const theme = new Map(), fam = new Map();
  families.forEach((f) => {
    const tAngles = f.themes.map((th) => {
      const a = th.mechanisms.map((m) => radial.get(m.id));
      const mean = a.reduce((s, v) => s + v, 0) / a.length;
      theme.set(th.id, mean);
      return mean;
    });
    fam.set(f.id, tAngles.reduce((s, v) => s + v, 0) / tAngles.length);
  });
  return { radial, list, theme, fam, listH, leaves };
}

function build() {
  const L = layout();
  const svg = el("svg", { role: "group", "aria-label": "Taxonomy of cooperation-shaping mechanisms" });
  const gLinks = el("g", { class: "tx-links" }, svg);
  const gNodes = el("g", { class: "tx-nodes" }, svg);
  const hub = el("g", { class: "tx-hub" }, gNodes);
  el("circle", { r: R.hub, class: "tx-hub-circle" }, hub);
  const hubText = el("text", { class: "tx-hub-text", "text-anchor": "middle", y: -4 }, hub);
  hubText.textContent = `${data.counts.mechanisms}`;
  const hubSub = el("text", { class: "tx-hub-sub", "text-anchor": "middle", y: 14 }, hub);
  hubSub.textContent = "mechanisms";

  const center = { x: 0, y: 0 };
  data.families.forEach((f) => {
    const fa = L.fam.get(f.id);
    const fr = polar(fa, R.fam), fl = L.list.get(f.id);
    const fg = el("g", { class: "tx-fam" }, gNodes);
    el("circle", { r: 6, fill: f.mid }, fg);
    const label = el("text", { class: "tx-fam-label", fill: f.dark }, fg);
    label.textContent = f.label.toUpperCase();
    const rule = el("line", { class: "tx-fam-rule", stroke: f.mid, x1: 0, x2: LIST.colW - 8, y1: 12, y2: 12 }, fg);
    const famNode = { kind: "fam", g: fg, label, rule, r: fr, l: fl, a: fa, f };
    nodes.push(famNode);
    links.push({ path: el("path", { class: "tx-link tx-link-root", stroke: f.mid }, gLinks), from: { r: center, l: fl, a: fa, rr: 0 }, to: famNode, rr: R.fam, root: true });

    f.themes.forEach((th) => {
      const ta = L.theme.get(th.id);
      const tg = el("g", { class: "tx-theme" }, gNodes);
      el("circle", { r: 4, fill: "#fff", stroke: f.mid, "stroke-width": 2 }, tg);
      const tl = el("text", { class: "tx-theme-label", fill: f.dark, x: 10, y: 4.5 }, tg);
      tl.textContent = th.name;
      const themeNode = { kind: "theme", g: tg, label: tl, r: polar(ta, R.theme), l: L.list.get(th.id), a: ta, f, th };
      nodes.push(themeNode);
      links.push({ path: el("path", { class: "tx-link", stroke: f.mid }, gLinks), from: famNode, to: themeNode, rr: R.theme, fr: R.fam });

      th.mechanisms.forEach((m) => {
        const ma = L.radial.get(m.id);
        const flip = ma > 90 && ma < 270;
        const g = el("g", { class: "tx-leaf", tabindex: 0, role: "button", "data-id": m.id,
          "aria-label": `${m.name}. ${EVIDENCE_LABEL[m.llm]}. ${m.sources.length} sources.` }, gNodes);
        const dot = el("circle", { r: 4.6, class: `tx-dot tx-${m.llm}`, stroke: f.dark, fill: m.llm === "tested" ? f.dark : "#fff" }, g);
        if (m.llm === "proposed") el("circle", { r: 1.7, fill: f.dark }, g);
        const text = el("text", { class: "tx-leaf-label" }, g);
        text.textContent = m.short;
        const squares = el("g", { class: "tx-squares" }, g);
        for (let i = 0; i < 6; i += 1) {
          el("rect", { x: LIST.colW - 86 + i * 10, y: -4, width: 8, height: 8, rx: 1.3,
            fill: i < m.breadth ? f.mid : "#fff", stroke: f.mid, "stroke-width": 0.9 }, squares);
        }
        const leafNode = { kind: "leaf", g, dot, label: text, squares, r: polar(ma, R.leaf), l: L.list.get(m.id), a: ma, flip, f, th, m };
        nodes.push(leafNode);
        links.push({ path: el("path", { class: "tx-link", stroke: f.mid }, gLinks), from: themeNode, to: leafNode, rr: R.leaf, fr: R.theme });
        g.addEventListener("click", () => select(leafNode, true));
        g.addEventListener("mouseenter", () => { if (!selected || window.matchMedia("(hover: hover)").matches) preview(leafNode); });
        g.addEventListener("mouseleave", () => { if (selected) highlight(selected); });
        g.addEventListener("keydown", (e) => { if (e.key === "Enter" || e.key === " ") { e.preventDefault(); select(leafNode, true); } });
        g.addEventListener("focus", () => preview(leafNode));
      });
    });
  });

  const hubNode = { kind: "hub", g: hub };
  nodes.push(hubNode);
  stage.replaceChildren(svg);
  const pad = 250;
  const box = {
    r: [-(R.leaf + pad), -(R.leaf + pad), 2 * (R.leaf + pad), 2 * (R.leaf + pad)],
    l: narrow ? [-24, -28, LIST.colW + 48, L.listH + 40] : [-24, -28, 2 * LIST.colW + LIST.colGap + 48, L.listH + 40],
  };
  return { svg, box };
}

function render(k) {
  const e = ease(k);
  const { svg, box } = scene;
  svg.setAttribute("viewBox", box.r.map((v, i) => lerp(v, box.l[i], e)).join(" "));
  const labelFade = k < 0.5 ? 1 - 2 * k : 2 * k - 1;
  for (const n of nodes) {
    if (n.kind === "hub") { n.g.style.opacity = 1 - e; continue; }
    n.x = lerp(n.r.x, n.l.x, e); n.y = lerp(n.r.y, n.l.y, e);
    n.g.setAttribute("transform", `translate(${n.x.toFixed(1)} ${n.y.toFixed(1)})`);
    if (n.kind === "leaf") {
      const radialRot = n.flip ? n.a - 180 : n.a;
      const inRadial = k < 0.5;
      const rot = inRadial ? radialRot * (1 - e) : 0;
      n.label.setAttribute("transform", `rotate(${rot.toFixed(1)})`);
      n.label.setAttribute("x", inRadial && n.flip ? -10 : 10);
      n.label.setAttribute("y", 4);
      n.label.setAttribute("text-anchor", inRadial && n.flip ? "end" : "start");
      n.label.style.opacity = labelFade;
      n.label.style.fontSize = `${lerp(FONT.leaf[0], FONT.leaf[1], e).toFixed(2)}px`;
      n.squares.style.opacity = Math.max(0, 2 * k - 1);
    } else if (n.kind === "theme") {
      n.label.style.opacity = Math.max(0, 2 * k - 1);
      n.label.style.fontSize = `${lerp(FONT.theme[0], FONT.theme[1], e).toFixed(2)}px`;
    } else if (n.kind === "fam") {
      const p = polar(n.a, 22);
      const [nx, ny] = FAM_NUDGE[n.f.id] || [0, 0];
      p.x += nx; p.y += ny;
      n.label.style.fontSize = `${lerp(FONT.fam[0], FONT.fam[1], e).toFixed(2)}px`;
      const inRadial = k < 0.5;
      n.label.setAttribute("x", inRadial ? p.x : 0);
      n.label.setAttribute("y", inRadial ? p.y + 4 : 4);
      n.label.setAttribute("text-anchor", inRadial ? (Math.cos((n.a * Math.PI) / 180) < -0.2 ? "end" : Math.cos((n.a * Math.PI) / 180) > 0.2 ? "start" : "middle") : "start");
      n.label.style.opacity = labelFade;
      n.rule.style.opacity = Math.max(0, 2 * k - 1);
      n.g.querySelector("circle").style.opacity = 1 - e;
    }
  }
  for (const link of links) {
    const a = link.root ? { x: 0, y: 0 } : { x: link.from.x, y: link.from.y };
    const b = { x: link.to.x, y: link.to.y };
    if (link.root) { link.path.style.opacity = 1 - e; }
    const fromA = link.root ? link.to.a : link.from.a;
    const mid = link.root ? R.fam / 2 : (link.fr + link.rr) / 2;
    const rc1 = polar(fromA, mid), rc2 = polar(link.to.a, mid);
    const lc = { x: a.x, y: b.y };
    const c1 = { x: lerp(rc1.x, lc.x, e), y: lerp(rc1.y, lc.y, e) };
    const c2 = { x: lerp(rc2.x, lc.x, e), y: lerp(rc2.y, lc.y, e) };
    const end = link.to.kind === "leaf" ? { x: b.x - 5 * e, y: b.y } : b;
    link.path.setAttribute("d", `M${a.x.toFixed(1)} ${a.y.toFixed(1)} C${c1.x.toFixed(1)} ${c1.y.toFixed(1)} ${c2.x.toFixed(1)} ${c2.y.toFixed(1)} ${end.x.toFixed(1)} ${end.y.toFixed(1)}`);
  }
}

function animateTo(target) {
  const start = t, t0 = performance.now(), dur = reduceMotion ? 0 : 1100;
  toggle.setAttribute("aria-pressed", String(target === 1));
  toggle.textContent = target === 1 ? "Fold into a circle" : "Unravel into a list";
  stage.classList.toggle("is-list", target === 1);
  function frame(now) {
    const p = dur ? Math.min((now - t0) / dur, 1) : 1;
    t = lerp(start, target, p);
    render(t);
    if (p < 1) requestAnimationFrame(frame);
  }
  requestAnimationFrame(frame);
}

function matches(m) {
  if (filter !== "all" && m.llm !== filter) return false;
  const q = search.value.trim().toLowerCase();
  if (!q) return true;
  return [m.name, m.short, m.definition, ...m.sources.map((s) => s.title)].some((s) => s.toLowerCase().includes(q));
}

function applyFilters() {
  let n = 0;
  for (const node of nodes) {
    if (node.kind !== "leaf") continue;
    const on = matches(node.m);
    node.g.classList.toggle("is-dim", !on);
    if (on) n += 1;
  }
  counter.textContent = `${n} of ${data.counts.mechanisms} mechanisms`;
}

function highlight(node) {
  for (const n of nodes) if (n.kind === "leaf") n.g.classList.toggle("is-active", n === node);
  for (const link of links) {
    const on = node && (link.to === node || link.to === nodes.find((x) => x.kind === "theme" && x.th === node.th) || (link.root && link.to.f === node.f));
    link.path.classList.toggle("is-active", Boolean(on));
  }
}

function preview(node) { highlight(node); showPanel(node); }

function select(node, updateHash) {
  selected = node;
  preview(node);
  if (updateHash) history.replaceState(null, "", `#${node.m.id}`);
}

function showPanel(node) {
  const { m, f, th } = node;
  panel.replaceChildren();
  panel.style.setProperty("--fam", f.mid);
  panel.appendChild(html("p", { class: "leaf-card-label" }, `${f.label} · ${th.name}`));
  panel.appendChild(html("h3", {}, m.name));
  panel.appendChild(html("p", { class: "tx-def" }, m.definition));
  const status = html("p", { class: `tx-status tx-status-${m.llm}` });
  status.appendChild(html("span", { class: "tx-status-dot", "aria-hidden": "true" }));
  status.appendChild(document.createTextNode(m.llm === "tested"
    ? `${EVIDENCE_LABEL.tested} (${m.n_llm_tested} ${m.n_llm_tested === 1 ? "study" : "studies"})`
    : EVIDENCE_LABEL[m.llm]));
  panel.appendChild(status);
  const other = m.disciplines.filter((d) => d !== "ai ml");
  if (other.length) panel.appendChild(html("p", { class: "tx-disc" }, `Also used in: ${other.map(pretty).join(", ")}`));

  GROUPS.forEach(([key, title]) => {
    const rows = m.sources.filter((s) => s.agent === key);
    if (!rows.length) return;
    const wrap = html("div", { class: "tx-group" });
    wrap.appendChild(html("h4", {}, `${title} (${rows.length})`));
    const ul = html("ul", { class: "tx-sources" });
    rows.forEach((s, i) => {
      const li = html("li");
      if (i >= SHOW_FIRST) li.hidden = true;
      const title = s.url ? html("a", { href: s.url, target: "_blank", rel: "noopener" }, s.title) : html("span", {}, s.title);
      li.appendChild(title);
      const meta = [s.authors, s.year, s.venue].filter(Boolean).join(" · ");
      li.appendChild(html("span", { class: "tx-meta" }, s.seed ? `${meta} (example from the seed list)` : meta));
      if (s.secondary) li.appendChild(html("span", { class: "tx-tag tx-tag-secondary" }, "also uses this lever"));
      if (s.evidence) li.appendChild(html("span", { class: "tx-tag" }, s.evidence));
      ul.appendChild(li);
    });
    wrap.appendChild(ul);
    if (rows.length > SHOW_FIRST) {
      const more = html("button", { class: "tx-more", type: "button" }, `Show all ${rows.length}`);
      more.addEventListener("click", () => { ul.querySelectorAll("li[hidden]").forEach((li) => { li.hidden = false; }); more.remove(); });
      wrap.appendChild(more);
    }
    panel.appendChild(wrap);
  });
  const permalink = html("a", { class: "tx-permalink", href: `#${m.id}` }, `Link to this mechanism (${m.id})`);
  panel.appendChild(permalink);
}

function buildTextList() {
  const ul = html("ul");
  data.families.forEach((f) => {
    const li = html("li"); li.appendChild(html("strong", {}, f.label));
    const tu = html("ul");
    f.themes.forEach((th) => {
      const tli = html("li", {}, th.name);
      const mu = html("ul");
      th.mechanisms.forEach((m) => {
        const mli = html("li");
        const b = html("button", { type: "button", class: "tx-text-btn" }, `${m.name} (${EVIDENCE_LABEL[m.llm].toLowerCase()}, ${m.sources.length} sources)`);
        b.addEventListener("click", () => { select(nodes.find((n) => n.m === m), true); panel.scrollIntoView({ behavior: "smooth", block: "nearest" }); });
        mli.appendChild(b); mu.appendChild(mli);
      });
      tli.appendChild(mu); tu.appendChild(tli);
    });
    li.appendChild(tu); ul.appendChild(li);
  });
  textList.appendChild(ul);
}

let scene;
async function init() {
  try {
    data = await (await fetch("assets/taxonomy.json")).json();
  } catch (err) {
    stage.textContent = "The taxonomy data could not be loaded.";
    return;
  }
  document.querySelectorAll("[data-tx-count]").forEach((node) => { node.textContent = data.counts[node.dataset.txCount]; });
  narrow = stage.clientWidth < 640;
  scene = build();
  const view = new URLSearchParams(location.search).get("view");
  const startList = view ? view === "list" : window.matchMedia("(max-width: 760px)").matches;
  t = startList ? 1 : 0;
  stage.classList.toggle("is-list", startList);
  toggle.textContent = startList ? "Fold into a circle" : "Unravel into a list";
  toggle.setAttribute("aria-pressed", String(startList));
  render(t);
  toggle.addEventListener("click", () => animateTo(t > 0.5 ? 0 : 1));
  search.addEventListener("input", applyFilters);
  filterButtons.forEach((b) => b.addEventListener("click", () => {
    filter = b.dataset.txFilter;
    filterButtons.forEach((x) => x.setAttribute("aria-pressed", String(x === b)));
    applyFilters();
  }));
  applyFilters();
  buildTextList();
  let resizeTimer;
  window.addEventListener("resize", () => {
    clearTimeout(resizeTimer);
    resizeTimer = setTimeout(() => {
      const now = stage.clientWidth < 640;
      if (now === narrow) return;
      narrow = now;
      const keep = selected && selected.m.id;
      nodes = []; links = [];
      scene = build();
      render(t);
      applyFilters();
      const again = nodes.find((n) => n.kind === "leaf" && n.m.id === keep);
      if (again) select(again, false);
    }, 200);
  });
  const fromHash = nodes.find((n) => n.kind === "leaf" && `#${n.m.id}` === location.hash);
  select(fromHash || nodes.find((n) => n.kind === "leaf" && n.m.llm === "tested"), false);
}

init();
