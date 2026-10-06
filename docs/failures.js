/* Where cooperation mechanisms fail (paper Fig. 8): three failure modes from Section 6, each placed at the
   enforcement stage where it breaks (Fig. 7: Observer, Arbiter, Enforcer) and the Coleman-boat arrow it hits.
   Each column runs mechanism -> failure -> what to measure -> the check -> safeguards, and loops back to revise
   and retest the institution. Hover, tap, or tab to any part for details. Stage data-mode="paper" for print. */
(function () {
  const stage = document.getElementById("fail-stage");
  const panel = document.getElementById("fail-panel");
  if (!stage) return;
  const PAPER = stage.dataset.mode === "paper";

  const NS = "http://www.w3.org/2000/svg";
  const FONT = "'Helvetica Neue', Helvetica, Arial, sans-serif";
  const INK = "#3F4D5A", MUT = "#6B7787", HAIR = "#B3BEC9";
  const C = {
    amber: ["#C79A3A", "#8A5A0B", "#FBEEDA"], terra: ["#C2662A", "#8F3F1E", "#FBEDE6"],
    blue: ["#3A6EA5", "#2F3D6B", "#DCE8F5"], green: ["#4F9070", "#2F6B4A", "#E5F0E1"],
    violet: ["#6C5CD0", "#463BA0", "#ECE9FB"],
  };
  // enforcement-stage colors match Fig. 7 (information layer slate, consequence layer plum)
  const STAGE = { Observer: ["#5B6B7D", "#34465A", "#E9EDF2"], Arbiter: ["#9C4A78", "#6B2350", "#F6E7EF"],
    Enforcer: ["#9C4A78", "#6B2350", "#F6E7EF"] };

  const MODES = [
    { tag: "A", title: "A fine becomes a price", stage: "Enforcer", n: 3, arrow: "arrow 2",
      breaks: "where the rule meets behavior", families: ["incentive"],
      mech: ["Fine", "a charge for a violation"], fail: ["Paid, not obeyed", "agents treat the fine as a fee for the act"],
      meas: "contribution stability", check: "Does cooperation hold without the fine?",
      safe: ["state the norm, not only the price", "graduated sanctions"],
      note: "A sanction can reframe the interaction. In the Haifa daycare study, a small fine for late pickup increased lateness: an obligation became a priced service. An agent optimizing against a budgeted penalty may treat it the same way." },
    { tag: "B", title: "A score becomes the target", stage: "Observer", n: 1, arrow: "arrow 4",
      breaks: "where behavior becomes a signal", families: ["social", "epistemic"],
      mech: ["Reputation score", "past conduct sets trust"], fail: ["Score is gamed", "reputation farming; shallow cooperation"],
      meas: "gameability; false negatives", check: "Does the score match real conduct?",
      safe: ["tamper-evident records", "peer review", "audit messages, not only scores"],
      note: "Any mechanism that produces a measurable signal creates a new optimization target. Agents can farm, inflate, or depress scores until the score stops tracking the conduct it was meant to reward." },
    { tag: "C", title: "A role becomes an authority", stage: "Arbiter", n: 2, arrow: "the feedback loop",
      breaks: "where the institution feeds back on itself", families: ["epistemic", "constraint"],
      mech: ["Monitor or judge", "a role that can sanction"], fail: ["Over-detects or abuses its authority", "rewarded for finding violations"],
      meas: "false punishment; abuse of authority; override", check: "Are rulings accurate and reversible?",
      safe: ["checks on sanctioners", "appeals", "elected or rotating roles", "a human stop"],
      note: "A monitor, mediator, or sanctioning role is an authority position with incentives of its own. A monitor rewarded for violations and never fined for false positives generates violations; agents in these roles can collude or abuse their authority." },
  ];
  const STEP = {
    mech: ["Mechanism", "The lever the institution adds."], fail: ["Failure", "How the lever breaks in practice."],
    meas: ["Measure", "What an evaluation should record to catch the failure (see the candidate metrics in Section 7)."],
    check: ["Check", "If the answer is yes, keep the mechanism and retest later; if no, add safeguards."],
    safe: ["Safeguards", "Mechanisms from the taxonomy that address the failure, after which the institution is tested again."],
  };

  const el = (tag, attrs = {}, parent) => {
    const n = document.createElementNS(NS, tag);
    for (const [k, v] of Object.entries(attrs)) n.setAttribute(k, v);
    if (parent) parent.appendChild(n);
    return n;
  };
  const text = (x, y, s, a, p) => { const t = el("text", { x, y, ...a }, p); t.textContent = s; return t; };
  const wrap = (s, n) => {
    const out = []; let cur = "";
    s.split(" ").forEach((w) => { if ((cur + " " + w).trim().length <= n) cur = (cur + " " + w).trim(); else { out.push(cur); cur = w; } });
    if (cur) out.push(cur);
    return out;
  };

  const W = 1000, H = 690, COLW = 314, GAP = 15, X0 = (W - 3 * COLW - 2 * GAP) / 2;
  const svg = el("svg", { viewBox: `0 0 ${W} ${H}`, xmlns: NS, "font-family": FONT, role: "img", class: "fl-svg",
    "aria-labelledby": "fl-title fl-desc" }, stage);
  el("title", { id: "fl-title" }, svg).textContent = "Where cooperation mechanisms fail";
  el("desc", { id: "fl-desc" }, svg).textContent =
    "Three failure modes, each at the enforcement stage where it breaks: a fine becomes a price (Enforcer), a score becomes the target (Observer), and a role becomes an authority (Arbiter). Each column runs from mechanism to failure, measure, check, and safeguards, then loops back to revise the institution.";
  const defs = el("defs", {}, svg);
  const sh = el("filter", { id: "fl-shadow", x: "-10%", y: "-10%", width: "120%", height: "130%" }, defs);
  el("feDropShadow", { dx: 0, dy: 3, stdDeviation: 5, "flood-color": INK, "flood-opacity": 0.12 }, sh);
  [["fl-ar", INK], ["fl-ar-g", C.green[0]]].forEach(([id, col]) => {
    const m = el("marker", { id, viewBox: "0 0 10 10", refX: 8, refY: 5, markerWidth: 6, markerHeight: 6, orient: "auto-start-reverse" }, defs);
    el("path", { d: "M 0 0 L 10 5 L 0 10 z", fill: col }, m);
  });

  const hits = [];
  MODES.forEach((m, i) => {
    const x = X0 + i * (COLW + GAP), st = STAGE[m.stage];
    const col = el("g", { class: "fl-col", tabindex: "0" }, svg);
    col.dataset.key = m.tag;
    hits.push(col);
    el("rect", { x, y: 8, width: COLW, height: H - 16, rx: 20, fill: "#FBFAF7", stroke: "#E4E0D6", "stroke-width": 1.2 }, col);
    // stage header, as in Fig. 7
    el("path", { d: `M ${x} 28 Q ${x} 8 ${x + 20} 8 L ${x + COLW - 20} 8 Q ${x + COLW} 8 ${x + COLW} 28 L ${x + COLW} 50 L ${x} 50 Z`, fill: st[1] }, col);
    text(x + 20, 35, m.stage.toUpperCase(), { "font-size": 15, "font-weight": 800, "letter-spacing": "0.1em", fill: "#fff" }, col);
    text(x + COLW - 16, 35, `boat: ${m.arrow}`, { "text-anchor": "end", "font-size": 12.5, "font-style": "italic", fill: st[2] }, col);
    // title and where it breaks
    el("circle", { cx: x + 26, cy: 80, r: 13, fill: C.terra[0] }, col);
    text(x + 26, 85, m.tag, { "text-anchor": "middle", "font-size": 15, "font-weight": 800, fill: "#fff" }, col);
    text(x + 48, 86, m.title, { "font-size": 16.5, "font-weight": 800, fill: INK }, col);
    wrap("Breaks " + m.breaks, 38).forEach((ln, k) => text(x + 20, 112 + k * 16, ln, { "font-size": 13.5, "font-style": "italic", "font-weight": 600, fill: C.terra[1] }, col));

    // spine with five steps
    const sx = x + 24, bx = x + 44, bw = COLW - 60;
    const node = (key, y, h, c, dash) => {
      const g = el("g", { class: "fl-step", tabindex: "0" }, col);
      g.dataset.key = m.tag; g.dataset.step = key;
      el("rect", { x: bx, y, width: bw, height: h, rx: 12, fill: dash ? "#fff" : c[2], stroke: c[0], "stroke-width": 1.5,
        ...(dash ? { "stroke-dasharray": "5 4" } : {}), filter: "url(#fl-shadow)" }, g);
      el("circle", { cx: sx, cy: y + h / 2, r: 6.5, fill: "#fff", stroke: c[0], "stroke-width": 2.4 }, col);
      return g;
    };
    const lab = (g, y, s) => text(bx + 12, y, s.toUpperCase(), { "font-size": 10.5, "font-weight": 800, "letter-spacing": "0.1em", fill: MUT }, g);
    let y = 146;
    const spine = el("line", { x1: sx, y1: y + 20, x2: sx, y2: 600, stroke: HAIR, "stroke-width": 2 }, col);
    let g = node("mech", y, 64, C.amber); lab(g, y + 18, "mechanism");
    text(bx + 12, y + 38, m.mech[0], { "font-size": 16, "font-weight": 800, fill: C.amber[1] }, g);
    text(bx + 12, y + 55, m.mech[1], { "font-size": 13, fill: INK }, g);
    y += 78;
    g = node("fail", y, 78, C.terra); lab(g, y + 18, "failure");
    text(bx + 12, y + 38, m.fail[0], { "font-size": 15, "font-weight": 800, fill: C.terra[1] }, g);
    wrap(m.fail[1], 34).forEach((ln, k) => text(bx + 12, y + 55 + k * 15, ln, { "font-size": 13, fill: INK }, g));
    y += 92;
    g = node("meas", y, 56, C.blue, true); lab(g, y + 18, "measure");
    text(bx + 12, y + 40, m.meas, { "font-size": 13.5, "font-weight": 700, fill: C.blue[1] }, g);
    y += 70;
    const cl = wrap(m.check, 32);
    g = node("check", y, 48 + cl.length * 16, C.blue); lab(g, y + 18, "check");
    cl.forEach((ln, k) => text(bx + 12, y + 38 + k * 16, ln, { "font-size": 13.5, "font-weight": 700, fill: C.blue[1] }, g));
    text(bx + 12, y + 38 + cl.length * 16, "yes: keep and retest  ·  no: add safeguards", { "font-size": 12, "font-style": "italic", fill: MUT }, g);
    y += 62 + cl.length * 16;
    const sh = 34 + m.safe.length * 17;
    g = node("safe", y, sh, C.green); lab(g, y + 18, "safeguards");
    m.safe.forEach((s, k) => {
      el("path", { d: `M ${bx + 14} ${y + 33 + k * 17} l 4 4 l 7 -8`, fill: "none", stroke: C.green[0], "stroke-width": 2.2,
        "stroke-linecap": "round", "stroke-linejoin": "round" }, g);
      text(bx + 32, y + 38 + k * 17, s, { "font-size": 13.5, fill: C.green[1], "font-weight": 600 }, g);
    });
    spine.setAttribute("y2", y + sh / 2);
    // loop: revise the institution and test again
    const ly = y + sh / 2, top = 178;
    el("path", { d: `M ${bx + bw} ${ly} L ${x + COLW - 6} ${ly} L ${x + COLW - 6} ${top} L ${bx + bw + 3} ${top}`, fill: "none",
      stroke: C.green[0], "stroke-width": 1.8, "stroke-dasharray": "6 5", "marker-end": "url(#fl-ar-g)", class: "fl-loop" }, col);
    // families
    const fy = H - 46;
    text(x + 18, fy + 4, "MOST EXPOSED", { "font-size": 10, "font-weight": 800, "letter-spacing": "0.1em", fill: MUT }, col);
    let fx = x + 120;
    m.families.forEach((f) => {
      const w = f.length * 7 + 18;
      el("rect", { x: fx, y: fy - 13, width: w, height: 24, rx: 12, fill: C.violet[2], stroke: C.violet[0], "stroke-width": 1.2 }, col);
      text(fx + w / 2, fy + 4, f, { "text-anchor": "middle", "font-size": 12, "font-weight": 700, "font-style": "italic", fill: C.violet[1] }, col);
      fx += w + 6;
    });
    text(x + COLW - 16, fy + 26, "↺ revise, then test again", { "text-anchor": "end", "font-size": 12, "font-style": "italic", fill: C.green[1] }, col);
  });

  if (PAPER) return;

  // on the web, each column becomes its own card so the three can sit in a row or stack on a phone;
  // the shared defs (shadow, arrowheads) stay in a zero-size SVG that every card can reference
  const cards = document.createElement("div");
  cards.className = "fl-cards";
  stage.appendChild(cards);
  hits.forEach((col, i) => {
    const x = X0 + i * (COLW + GAP);
    const card = el("svg", { viewBox: `${x - 4} 2 ${COLW + 8} ${H - 4}`, xmlns: NS, "font-family": FONT, class: "fl-svg fl-card",
      role: "img", "aria-label": `${MODES[i].tag}. ${MODES[i].title} (${MODES[i].stage} stage)` });
    card.appendChild(col);
    cards.appendChild(card);
  });
  svg.setAttribute("class", "fl-defs");
  svg.setAttribute("width", "0"); svg.setAttribute("height", "0");
  svg.setAttribute("aria-hidden", "true");

  // ---------- interaction ----------
  let locked = null;
  const show = (tag, step) => {
    if (!panel) return;
    const m = MODES.find((d) => d.tag === tag);
    if (!m) {
      panel.style.removeProperty("--c");
      panel.innerHTML = `<p class="fl-plabel">Explore</p><h3>Three ways a mechanism can backfire</h3><p>Each column sits at the enforcement stage where it breaks. Hover, tap, or tab to a column or a step.</p>`;
      return;
    }
    const st = STAGE[m.stage];
    panel.style.setProperty("--c", step ? (step === "safe" ? C.green[0] : step === "fail" ? C.terra[0] : step === "mech" ? C.amber[0] : C.blue[0]) : st[0]);
    const head = `<p class="fl-plabel">${m.tag} · ${m.stage} stage · Coleman boat ${m.arrow}</p><h3>${m.title}</h3>`;
    if (step) {
      const [name, gloss] = STEP[step];
      const body = step === "safe" ? `<ul>${m.safe.map((s) => `<li>${s}</li>`).join("")}</ul>`
        : step === "mech" ? `<p><strong>${m.mech[0]}</strong>: ${m.mech[1]}.</p>`
        : step === "fail" ? `<p><strong>${m.fail[0]}</strong>: ${m.fail[1]}.</p>`
        : step === "meas" ? `<p><strong>${m.meas}</strong></p>` : `<p><strong>${m.check}</strong></p>`;
      panel.innerHTML = `${head}<p class="fl-step-name">${name}</p>${body}<p class="fl-gloss">${gloss}</p>`;
    } else panel.innerHTML = `${head}<p>${m.note}</p>`;
  };
  const activate = (tag, step) => {
    stage.classList.toggle("has-active", !!tag);
    hits.forEach((c) => c.classList.toggle("is-on", c.dataset.key === tag));
    stage.querySelectorAll(".fl-step").forEach((s) => s.classList.toggle("is-step", !!step && s.dataset.key === tag && s.dataset.step === step));
    show(tag, step);
  };
  stage.querySelectorAll(".fl-col, .fl-step").forEach((n) => {
    const tag = n.dataset.key, step = n.dataset.step;
    const on = (e) => { e.stopPropagation(); activate(tag, step); };
    const off = (e) => { e.stopPropagation(); activate(locked ? locked[0] : null, locked ? locked[1] : null); };
    n.addEventListener("pointerenter", on); n.addEventListener("focus", on);
    n.addEventListener("pointerleave", off); n.addEventListener("blur", off);
    n.addEventListener("click", (e) => { e.stopPropagation(); locked = locked && locked[0] === tag && locked[1] === step ? null : [tag, step]; activate(tag, step); });
    n.addEventListener("keydown", (e) => { if (e.key === "Enter" || e.key === " ") { e.preventDefault(); n.dispatchEvent(new Event("click")); } });
  });
  stage.addEventListener("click", () => { locked = null; activate(null); });
  show(null);
})();
