#!/usr/bin/env python3
"""Generate the failure-mode flow figure (Table 2 as a flowchart).

Layout follows the Pennsieve agent-loops figures; colors follow manuscript/figs/PALETTE.md:
amber = mechanism, terracotta = failure, blue = measurement and check (information),
green = safeguards and outcomes, violet = mechanism family.
"""
import os
from html import escape

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "figs", "figure7_failure-modes-flow.html")

W, HEAD, RH, GAP = 960, 34, 204, 12
X = dict(mech=(18, 162), fail=(202, 180), meas=(404, 150), dcx=642, dhw=76, dhh=54, safe=(746, 198))

ROWS = [
    dict(tag="A", title="A fine becomes a price", family="incentive family", breaks="the rule meets behavior",
         mech=("Fine", "a charge for a violation"),
         fail=("Paid, not obeyed", ["agents treat the fine", "as a fee for the act"]),
         meas=["contribution", "stability"],
         q=["Cooperation", "holds without", "the fine?"],
         safe=["state the norm, not", "only the price", "graduated sanctions"], bullets={0, 2}),
    dict(tag="B", title="A score becomes the target", family="social & epistemic", breaks="behavior becomes a signal",
         mech=("Reputation score", "past conduct sets trust"),
         fail=("Score is gamed", ["reputation farming;", "shallow cooperation"]),
         meas=["gameability;", "false negatives"],
         q=["Score", "matches real", "conduct?"],
         safe=["tamper-evident records", "peer review", "audit messages, not", "only scores"], bullets={0, 1, 2}),
    dict(tag="C", title="A role becomes an authority", family="epistemic & constraint", breaks="the institution feeds back on itself",
         mech=("Monitor or judge", "a role that can sanction"),
         fail=("Over-detects or", ["is captured", "rewarded for violations"]),
         meas=["false punishment;", "capture; override"],
         q=["Rulings", "accurate and", "reversible?"],
         safe=["checks on sanctioners", "appeals", "elected or rotating roles", "a human stop"], bullets={0, 1, 2, 3}),
]

def t(x, y, s, cls, extra=""):
    return f'<text x="{x:.1f}" y="{y:.1f}" class="{cls}"{extra}>{escape(s)}</text>'

def header():
    y = 20
    cols = [("MECHANISM", X["mech"][0] + X["mech"][1] / 2), ("FAILURE", X["fail"][0] + X["fail"][1] / 2),
            ("MEASURE", X["meas"][0] + X["meas"][1] / 2), ("CHECK", X["dcx"]),
            ("SAFEGUARDS", X["safe"][0] + X["safe"][1] / 2)]
    return "\n".join(t(x, y, s, "colhead") for s, x in cols)

def row(i, r):
    y0 = HEAD + i * (RH + GAP)
    bt, bh = y0 + 72, 92
    yc = bt + bh / 2
    mx, mw = X["mech"]; fx, fw = X["fail"]; kx, kw = X["meas"]; sx, sw = X["safe"]
    dcx, dhw, dhh = X["dcx"], X["dhw"], X["dhh"]
    s = [f'<rect x="1" y="{y0}" width="{W-2}" height="{RH}" rx="12" class="panel"/>',
         t(18, y0 + 30, f'{r["tag"]}. {r["title"]}', "ptitle"),
         t(18, y0 + 53, 'Breaks where ' + r["breaks"], "breaks")]
    fam_w = 11 + 7.6 * len(r["family"])
    s.append(f'<rect x="{W-18-fam_w:.1f}" y="{y0+12}" width="{fam_w:.1f}" height="26" rx="13" class="famchip"/>')
    s.append(t(W - 18 - fam_w / 2, y0 + 30, r["family"], "famtext"))
    # mechanism
    s.append(f'<rect x="{mx}" y="{bt}" width="{mw}" height="{bh}" rx="10" class="mech"/>')
    s.append(t(mx + mw / 2, yc - 4, r["mech"][0], "mtitle"))
    s.append(t(mx + mw / 2, yc + 18, r["mech"][1], "sub"))
    s.append(f'<line x1="{mx+mw}" y1="{yc}" x2="{fx-3}" y2="{yc}" class="edge" marker-end="url(#ah)"/>')
    # failure
    s.append(f'<rect x="{fx}" y="{bt}" width="{fw}" height="{bh}" rx="10" class="fail"/>')
    lines = [r["fail"][0]] + r["fail"][1]
    n_title = 1 if len(lines) == 3 and r["tag"] != "C" else 2
    top = yc - (len(lines) - 1) * 9.5 + 5
    for j, line in enumerate(lines):
        s.append(t(fx + fw / 2, top + j * 19, line, "ftitle" if j < n_title else "sub"))
    s.append(f'<line x1="{fx+fw}" y1="{yc}" x2="{kx-3}" y2="{yc}" class="edge" marker-end="url(#ah)"/>')
    # measure
    s.append(f'<rect x="{kx}" y="{yc-30}" width="{kw}" height="60" rx="10" class="meas"/>')
    for j, line in enumerate(r["meas"]):
        s.append(t(kx + kw / 2, yc - 5 + j * 19, line, "mtext"))
    s.append(f'<line x1="{kx+kw}" y1="{yc}" x2="{dcx-dhw-3}" y2="{yc}" class="edge" marker-end="url(#ah)"/>')
    # check
    s.append(f'<polygon points="{dcx},{yc-dhh} {dcx+dhw},{yc} {dcx},{yc+dhh} {dcx-dhw},{yc}" class="check"/>')
    for j, line in enumerate(r["q"]):
        s.append(t(dcx, yc - 13 + j * 17, line, "qtext"))
    # yes: keep
    s.append(f'<line x1="{dcx}" y1="{yc-dhh}" x2="{dcx}" y2="{y0+40}" class="edge" marker-end="url(#ah)"/>')
    s.append(t(dcx - 9, y0 + 55, "yes", "elabel", ' style="text-anchor:end"'))
    s.append(f'<rect x="{dcx-62}" y="{y0+12}" width="124" height="26" rx="13" class="keep"/>')
    s.append(t(dcx, y0 + 30, "keep; retest", "keeptext"))
    # no: safeguards
    s.append(f'<line x1="{dcx+dhw}" y1="{yc}" x2="{sx-3}" y2="{yc}" class="edge" marker-end="url(#ah)"/>')
    s.append(t((dcx + dhw + sx) / 2, yc - 8, "no", "elabel"))
    s.append(f'<rect x="{sx}" y="{bt}" width="{sw}" height="{bh}" rx="10" class="safe"/>')
    items = r["safe"]
    top = yc - (len(items) - 1) * 9.5 + 5
    for j, line in enumerate(items):
        ty = top + j * 19
        if j in r["bullets"]:
            s.append(f'<circle cx="{sx+16}" cy="{ty-5:.1f}" r="2.7" class="dot"/>')
        s.append(t(sx + 26, ty, line, "item"))
    # loop back: revise the institution
    ly = bt + bh + 20
    sxm, mxm = sx + sw / 2, mx + mw / 2
    s.append(f'<path d="M {sxm} {bt+bh} L {sxm} {ly-8} Q {sxm} {ly} {sxm-8} {ly} L {mxm+8} {ly} '
             f'Q {mxm} {ly} {mxm} {ly-8} L {mxm} {bt+bh+3}" class="edge" marker-end="url(#ah)"/>')
    s.append(f'<rect x="{W/2-100}" y="{ly-11}" width="200" height="22" class="knock"/>')
    s.append(t(W / 2, ly + 5, "revise the institution", "elabel"))
    return "\n".join(s)

H = HEAD + 3 * RH + 2 * GAP + 2
body = header() + "\n" + "\n".join(row(i, r) for i, r in enumerate(ROWS))

html = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Failure modes, checks, and safeguards (flow)</title>
<!-- Flowchart version of Table 2 (tab:family-dilemma-guide). Generated by scripts/gen_failure_flow.py.
     Palette: manuscript/figs/PALETTE.md. amber = mechanism, terracotta = failure,
     blue = measure and check, green = safeguards and keep, violet = mechanism family. -->
<style>
  :root{{
    --ink:#3F4D5A; --muted:#6B7787; --hair:#B3BEC9; --page:#FBFAF7;
    --amber:#C79A3A; --amber-d:#8A5A0B; --amber-bg:#FBEEDA;
    --terra:#C2662A; --terra-d:#8F3F1E; --terra-bg:#FBEDE6;
    --blue:#3A6EA5; --blue-d:#2F3D6B; --blue-bg:#DCE8F5;
    --green:#4F9070; --green-d:#2F6B4A; --green-bg:#E5F0E1;
    --violet-d:#463BA0; --violet-l:#C4BCEC; --violet-bg:#ECE9FB;
  }}
  html,body{{background:#fff;margin:0;}}
  body{{font-family:"Helvetica Neue",Arial,sans-serif;color:var(--ink);}}
  .fig{{width:{W}px;margin:0 auto;padding:10px;}}
  .panel{{fill:var(--page);stroke:var(--hair);stroke-width:1.2;}}
  .knock{{fill:var(--page);stroke:none;}}
  .mech{{fill:var(--amber-bg);stroke:var(--amber);stroke-width:1.5;}}
  .fail{{fill:var(--terra-bg);stroke:var(--terra);stroke-width:1.5;}}
  .meas{{fill:#fff;stroke:var(--blue);stroke-width:1.4;stroke-dasharray:5 4;}}
  .check{{fill:var(--blue-bg);stroke:var(--blue);stroke-width:1.5;}}
  .safe{{fill:var(--green-bg);stroke:var(--green);stroke-width:1.5;}}
  .keep{{fill:var(--green-bg);stroke:var(--green);stroke-width:1.3;}}
  .famchip{{fill:var(--violet-bg);stroke:var(--violet-l);stroke-width:1.2;}}
  .dot{{fill:var(--green-d);}}
  .edge{{fill:none;stroke:var(--ink);stroke-width:1.7;}}
  text{{font-family:"Helvetica Neue",Arial,sans-serif;}}
  .colhead{{font-size:13.5px;font-weight:700;letter-spacing:1.4px;fill:var(--muted);text-anchor:middle;}}
  .ptitle{{font-size:20px;font-weight:700;fill:var(--ink);letter-spacing:-.2px;}}
  .famtext{{font-size:14px;font-style:italic;fill:var(--violet-d);text-anchor:middle;}}
  .mtitle{{font-size:17px;font-weight:700;fill:var(--amber-d);text-anchor:middle;}}
  .ftitle{{font-size:17px;font-weight:700;fill:var(--terra-d);text-anchor:middle;}}
  .sub{{font-size:15px;fill:var(--ink);text-anchor:middle;}}
  .mtext{{font-size:15px;fill:var(--blue-d);text-anchor:middle;}}
  .qtext{{font-size:15px;font-weight:700;fill:var(--blue-d);text-anchor:middle;}}
  .keeptext{{font-size:14.5px;font-weight:700;fill:var(--green-d);text-anchor:middle;}}
  .item{{font-size:15px;fill:var(--ink);}}
  .elabel{{font-size:15px;font-style:italic;fill:var(--muted);text-anchor:middle;}}
  .breaks{{font-size:14.5px;font-style:italic;font-weight:700;fill:var(--terra-d);}}
</style>
</head>
<body>
<div class="fig">
<svg viewBox="0 0 {W} {H}" width="{W}" height="{H}" xmlns="http://www.w3.org/2000/svg">
<defs><marker id="ah" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#3F4D5A"/></marker></defs>
{body}
</svg>
</div>
</body>
</html>
'''
open(OUT, "w", encoding="utf-8").write(html)
print("wrote", os.path.relpath(OUT), W, H)
