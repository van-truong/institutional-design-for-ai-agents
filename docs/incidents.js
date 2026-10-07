/* Incident timeline (problem section), from assets/incidents.json (built by taxonomy/scripts/build_incidents_data.py
   from taxonomy/incidents.csv). Newest first. A short summary line counts the record, two filters narrow it, and the
   list shows the latest few until "Show all" is pressed, so the section stays short on a phone. */
(function () {
  const list = document.getElementById("inc-list");
  if (!list) return;
  const SHOW = window.matchMedia && matchMedia("(max-width: 600px)").matches ? 3 : 5;
  const stats = document.getElementById("inc-stats");
  const more = document.getElementById("inc-more");
  const filters = document.querySelectorAll("[data-inc-filter]");
  const MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
  const html = (tag, cls, txt) => { const n = document.createElement(tag); if (cls) n.className = cls; if (txt !== undefined) n.textContent = txt; return n; };
  let items = [], filter = "all", open = false;

  fetch(list.dataset.src || "assets/incidents.json").then((r) => r.json()).then((d) => {
    items = d.incidents || [];
    const real = items.filter((it) => it.setting === "Real systems").length;
    const multi = items.filter((it) => it.multi_agent).length;
    const first = items[items.length - 1].date.slice(0, 7).split("-");
    stats.replaceChildren(
      stat(items.length, "documented incidents since " + MONTHS[+first[1] - 1] + " " + first[0]),
      stat(real, "reached real systems"),
      stat(multi, "involved several agents"));
    filters.forEach((b) => b.addEventListener("click", () => {
      filter = b.dataset.incFilter;
      filters.forEach((x) => x.setAttribute("aria-pressed", x === b));
      render();
    }));
    more.addEventListener("click", () => { open = !open; render(); if (!open) list.scrollIntoView({ block: "nearest" }); });
    render();
  }).catch(() => { list.replaceChildren(html("li", "inc-empty", "The incident list could not be loaded.")); });

  function stat(n, label) {
    const d = html("div", "inc-stat");
    d.append(html("strong", "", String(n)), html("span", "", label));
    return d;
  }

  function shown() {
    return items.filter((it) => filter === "all" || (filter === "real" ? it.setting === "Real systems" : it.multi_agent));
  }

  function render() {
    const all = shown(), vis = open ? all : all.slice(0, SHOW);
    list.replaceChildren(...vis.map(row));
    more.hidden = all.length <= SHOW;
    more.textContent = open ? "Show fewer" : `Show all ${all.length}`;
    more.setAttribute("aria-expanded", open);
  }

  function row(it) {
    const li = html("li", "inc-item" + (it.setting === "Real systems" ? " is-real" : ""));
    const [y, m, d] = it.date.split("-");
    const when = html("time", "inc-when", `${MONTHS[+m - 1]} ${+d}, ${y}`);
    when.dateTime = it.date;
    const body = html("div", "inc-body");
    const a = html("a", "inc-title", it.title);
    a.href = it.url; a.target = "_blank"; a.rel = "noopener";
    const meta = html("p", "inc-meta");
    meta.append(html("span", "inc-tag" + (it.setting === "Real systems" ? " tag-real" : ""), it.setting));
    if (it.multi_agent) meta.append(html("span", "inc-tag tag-multi", "Several agents"));
    meta.append(html("span", "inc-src", it.outlet));
    body.append(a, html("p", "inc-sum", it.summary), meta);
    li.append(when, body);
    return li;
  }
})();
