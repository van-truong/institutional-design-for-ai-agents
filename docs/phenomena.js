/* Interactive group-level phenomena section. Reads assets/phenomena.json (built by
   taxonomy/scripts/build_phenomena_data.py) and renders a substrate matrix whose rows expand
   to the papers behind each phenomenon type, plus documented real-world incidents. */
(function () {
  const $ = (sel, p = document) => p.querySelector(sel);
  const html = (tag, attrs = {}, text) => {
    const n = document.createElement(tag);
    for (const [k, v] of Object.entries(attrs)) n.setAttribute(k, v);
    if (text !== undefined) n.textContent = text;
    return n;
  };
  const VAL = { beneficial: "benef", neutral: "neut", harmful: "harm" };
  const GROUPLAB = { llm: "LLM-agent studies", marl: "MARL studies", human: "Human studies" };
  const SHOW_FIRST = 6;

  fetch("assets/phenomena.json").then((r) => r.json()).then(render).catch(() => {
    const m = $("#ph-matrix"); if (m) m.textContent = "The phenomena data could not be loaded.";
  });

  function dotCell(count, val) {
    const cell = html("div", { class: "ph-cell", role: "cell" });
    if (count) {
      const sz = Math.round(20 + 6 * Math.sqrt(count));
      const d = html("span", { class: `ph-dot ph-${VAL[val]}`, style: `--sz:${sz}px` }, String(count));
      cell.appendChild(d);
    } else {
      cell.appendChild(html("span", { class: "ph-dot ph-empty", "aria-label": "none" }));
    }
    return cell;
  }

  function render(data) {
    document.querySelectorAll("[data-ph-count]").forEach((n) => { n.textContent = data.counts[n.dataset.phCount]; });
    const leg = $("#ph-legend");
    if (leg) data.valences.forEach(([k, label]) => {
      const item = html("span", { class: "ph-legend-item" });
      item.appendChild(html("span", { class: `ph-dot ph-${VAL[k]} ph-legdot` }));
      item.appendChild(html("span", {}, label));
      leg.appendChild(item);
    });

    const incByKey = Object.fromEntries(data.incidents.map((x) => [x.key, x]));
    const matrix = $("#ph-matrix");
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
    // open a row from the URL hash (#ph-<key>), a shareable permalink
    const key = (location.hash.match(/^#ph-(.+)$/) || [])[1];
    if (key) {
      const target = matrix.querySelector(`#ph-${CSS.escape(key)} .ph-rowhead`);
      if (target) { target.click(); target.scrollIntoView({ block: "center" }); }
    }
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
})();
