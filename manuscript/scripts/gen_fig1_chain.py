#!/usr/bin/env python3
"""Draft Fig. 1: the position as a causal chain, with the taxonomy circle as panel B.

(A) aligned agents -> shared resource -> emergent failure -> human-designed institution -> outcomes + costs,
    with bars marking what model-level evaluation covers versus the model-in-institution.
(B) the institution's toolbox: the 66 coded mechanisms as a radial tree (families, themes, evidence markers),
    built from docs/assets/taxonomy.json so it matches the website and Fig. 4.
Colors follow figs/PALETTE.md. Run from manuscript/:  python3 scripts/gen_fig1_chain.py
"""
import json, math, os
from html import escape

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, '..', '..', 'docs', 'assets', 'taxonomy.json')
OUT = os.path.join(HERE, '..', 'figs', 'drafts', 'figure1_causal-chain.html')

INK, MUTED, HAIR, PAGE = '#3F4D5A', '#6B7787', '#B3BEC9', '#FBFAF7'
ROLE = {'slate': ('#6B7787', '#3F4D5A', '#EEF2F6'), 'blue': ('#3A6EA5', '#2F3D6B', '#DCE8F5'),
        'terra': ('#C2662A', '#8F3F1E', '#FBEDE6'), 'amber': ('#C79A3A', '#8A5A0B', '#FBEEDA'),
        'green': ('#4F9070', '#2F6B4A', '#E5F0E1')}
W = 900
TEXTWIDTH_PT = 347.0

def t(x, y, s, cls, anchor='middle', extra=''):
    return f'<text x="{x:.1f}" y="{y:.1f}" class="{cls}" text-anchor="{anchor}"{extra}>{escape(s)}</text>'

# ---------------- panel A: causal chain ----------------
CHAIN = [('slate', 'Aligned agents', ['each passes', 'model-level tests']),
         ('blue', 'Shared resource', ['memory, compute,', 'code, budgets']),
         ('terra', 'Emergent failure', ['depletion, collusion,', 'duplicated work']),
         ('amber', 'Institution', ['human-designed', 'rules and roles']),
         ('green', 'Outcomes + costs', ['cooperation, burden,', 'false punishment'])]
BW, BG, BY, BH = 160, 25, 92, 96

def chain():
    s = [t(0, 26, 'A', 'plabel', 'start'), t(22, 26, 'Why model-level alignment is not enough', 'ptitle', 'start')]
    x_last = 4 * (BW + BG) + BW
    # coverage bars
    s.append(f'<line x1="0" y1="50" x2="{x_last}" y2="50" stroke="{ROLE["amber"][0]}" stroke-width="4" stroke-linecap="round"/>')
    s.append(t(x_last / 2 + 60, 44, 'model-in-institution evaluation', 'barlabel', extra=f' fill="{ROLE["amber"][1]}"'))
    s.append(f'<line x1="0" y1="72" x2="{BW}" y2="72" stroke="{HAIR}" stroke-width="4" stroke-linecap="round"/>')
    s.append(t(BW + 10, 77, 'model-level evaluation stops here', 'barlabel', 'start', f' fill="{MUTED}"'))
    for i, (role, title, sub) in enumerate(CHAIN):
        mid, dark, bg = ROLE[role]
        x = i * (BW + BG)
        s.append(f'<rect x="{x}" y="{BY}" width="{BW}" height="{BH}" rx="10" fill="{bg}" stroke="{mid}" stroke-width="1.6"/>')
        s.append(t(x + BW / 2, BY + 33, title, 'btitle', extra=f' fill="{dark}"'))
        for j, line in enumerate(sub):
            s.append(t(x + BW / 2, BY + 56 + j * 18, line, 'bsub'))
        if i < 4:
            s.append(f'<line x1="{x+BW+2}" y1="{BY+BH/2}" x2="{x+BW+BG-4}" y2="{BY+BH/2}" class="edge" marker-end="url(#ah)"/>')
    return s

# ---------------- panel B: taxonomy circle (print version) ----------------
R_HUB, R_FAM, R_THEME, R_LEAF, R_LABEL = 28, 50, 80, 110, 122
# Hand-placed nudges that keep family labels apart near the hub.
FAM_OFFSET = {'restorative': (-30, -8), 'normative': (38, 4), 'constraint': (-6, 0), 'social': (6, 0)}
# Shorter theme names for print (full names are in Fig. 4 and on the website).
THEME_PRINT = {'Norms & compliance support': 'Norms & compliance', 'Collective choice & legitimacy': 'Collective choice',
               'Checks on enforcement': 'Checks on enforcers', 'Exclusion & conditional access': 'Exclusion & access',
               'Conditional strategies': 'Conditional strategies', 'Visibility & attribution': 'Visibility',
               'Disclosure incentives': 'Disclosure', 'Rewards & payoff alignment': 'Rewards & payoffs',
               'Mechanism design & allocation': 'Mechanism design', 'Structural constraints': 'Structural limits',
               'Commitment & contracting': 'Commitment & contracts', 'Repair & restoration': 'Repair'}

def circle(cx, cy):
    data = json.load(open(DATA))
    fams = data['families']
    n = sum(len(th['mechanisms']) for f in fams for th in f['themes'])
    gap = 1.6
    step = 360 / (n + gap * len(fams))
    ang, slot = {}, 0.8
    for f in fams:
        for th in f['themes']:
            for m in th['mechanisms']:
                ang[m['id']] = -90 + slot * step; slot += 1
        slot += gap
    P = lambda a, r: (cx + r * math.cos(math.radians(a)), cy + r * math.sin(math.radians(a)))
    links, dots, labels, flabels = [], [], [], []
    theme_angles = []
    for f in fams:
        mid, dark = f['mid'], f['dark']
        t_ang = []
        for th in f['themes']:
            a = sum(ang[m['id']] for m in th['mechanisms']) / len(th['mechanisms'])
            t_ang.append(a); theme_angles.append([a, THEME_PRINT.get(th['name'], th['name']), dark])
        fa = sum(t_ang) / len(t_ang)
        fx, fy = P(fa, R_FAM)
        links.append(f'<path d="M{cx} {cy} L{fx:.1f} {fy:.1f}" stroke="{mid}" class="lk"/>')
        for th, a in zip(f['themes'], t_ang):
            tx, ty = P(a, R_THEME)
            c1, c2 = P(fa, (R_FAM + R_THEME) / 2), P(a, (R_FAM + R_THEME) / 2)
            links.append(f'<path d="M{fx:.1f} {fy:.1f} C{c1[0]:.1f} {c1[1]:.1f} {c2[0]:.1f} {c2[1]:.1f} {tx:.1f} {ty:.1f}" stroke="{mid}" class="lk"/>')
            dots.append(f'<circle cx="{tx:.1f}" cy="{ty:.1f}" r="2.6" fill="#fff" stroke="{mid}" stroke-width="1.4"/>')
            for m in th['mechanisms']:
                ma = ang[m['id']]
                lx, ly = P(ma, R_LEAF)
                d1, d2 = P(a, (R_THEME + R_LEAF) / 2), P(ma, (R_THEME + R_LEAF) / 2)
                links.append(f'<path d="M{tx:.1f} {ty:.1f} C{d1[0]:.1f} {d1[1]:.1f} {d2[0]:.1f} {d2[1]:.1f} {lx:.1f} {ly:.1f}" stroke="{mid}" class="lk"/>')
                fill = dark if m['llm'] == 'tested' else '#fff'
                dots.append(f'<circle cx="{lx:.1f}" cy="{ly:.1f}" r="3.4" fill="{fill}" stroke="{dark}" stroke-width="1.3"/>')
                if m['llm'] == 'proposed':
                    dots.append(f'<circle cx="{lx:.1f}" cy="{ly:.1f}" r="1.2" fill="{dark}"/>')
        # family label near its hub node, pushed outward and kept horizontal
        lx, ly = P(fa, R_FAM + 16)
        ox, oy = FAM_OFFSET.get(f['id'], (0, 0))
        flabels.append(t(lx + ox, ly + 4.5 + oy, f['label'].upper(), 'famlabel', 'middle', f' fill="{dark}"'))
    # spread theme labels so neighbours never overlap (min angular gap)
    theme_angles.sort(key=lambda r: r[0])
    MIN = 9.0
    for _ in range(200):
        moved = False
        for i in range(len(theme_angles)):
            a, b = theme_angles[i], theme_angles[(i + 1) % len(theme_angles)]
            d = (b[0] - a[0]) % 360
            if d < MIN:
                push = (MIN - d) / 2 + 0.01
                a[0] -= push; b[0] += push; moved = True
        if not moved: break
    for a, name, dark in theme_angles:
        a = ((a + 180) % 360) - 180
        x, y = P(a, R_LABEL)
        flip = a > 90 or a < -90
        rot = a + 180 if flip else a
        labels.append(t(x, y + 4.5, name, 'thlabel', 'end' if flip else 'start',
                        f' fill="{dark}" transform="rotate({rot:.1f} {x:.1f} {y:.1f})"'))
    hub = (f'<circle cx="{cx}" cy="{cy}" r="{R_HUB}" fill="{PAGE}" stroke="{INK}" stroke-width="1.5"/>'
           + t(cx, cy + 2, str(n), 'hubn') + t(cx, cy + 16, 'mechanisms', 'hubs'))
    return links + dots + [hub] + flabels + labels

FUNCTIONS = [('Norms & protocols', 'info'), ('Monitoring', 'info'), ('Reputation', 'info'),
             ('Sanctions', 'cons'), ('Constraints', 'cons'), ('Adjudication & appeal', 'cons'),
             ('Repair & reintegration', 'cons')]
# Institutional-function colors (figs/PALETTE.md): grey information layer, plum consequence layer.
FN = {'info': ('#5B6B7D', '#34465A', '#E9EDF2'), 'cons': ('#9C4A78', '#6B2350', '#F6E7EF')}

def functions_row(y, inst_cx):
    """The seven institutional functions as chips, bracketed under the institution box."""
    s = []
    widths = [18 + 7.3 * len(n) for n, _ in FUNCTIONS]
    gap = 8
    total = sum(widths) + gap * (len(widths) - 1)
    x = (W - total) / 2
    s.append(f'<path d="M{inst_cx} {BY+BH} L{inst_cx} {y-12} M{x} {y-12} L{x+total} {y-12}" stroke="{INK}" stroke-width="1.2" fill="none"/>')
    s.append(t(inst_cx + 8, y - 17, 'performs seven functions', 'pnote', 'start'))
    for (name, layer), w in zip(FUNCTIONS, widths):
        mid, dark, bg = FN[layer]
        s.append(f'<rect x="{x:.1f}" y="{y}" width="{w:.1f}" height="26" rx="13" fill="{bg}" stroke="{mid}" stroke-width="1.3"/>')
        s.append(t(x + w / 2, y + 17.5, name, 'fnchip', extra=f' fill="{dark}"'))
        x += w + gap
    return s, (W - total) / 2, (W - total) / 2 + total

def build():
    s = chain()
    inst_x = 3 * (BW + BG)
    fy = BY + BH + 44
    frow, fx0, fx1 = functions_row(fy, inst_x + BW / 2)
    s += frow
    # panel B frame, fed from the functions row
    top = fy + 26 + 38
    bx0, bx1, by1 = 300, W, top + 640
    cx, cy = (bx0 + bx1) / 2, top + 345
    s.append(f'<rect x="{bx0}" y="{top}" width="{bx1-bx0}" height="{by1-top}" rx="14" fill="{ROLE["amber"][2]}" fill-opacity=".45" stroke="{ROLE["amber"][0]}" stroke-width="1.4" stroke-dasharray="6 4"/>')
    s.append(f'<path d="M{max(fx0, bx0 - 10):.1f} {fy+26} L{bx0+40} {top}" stroke="{ROLE["amber"][0]}" stroke-width="1.3" stroke-dasharray="6 4" fill="none"/>')
    s.append(f'<path d="M{fx1:.1f} {fy+26} L{bx1-40} {top}" stroke="{ROLE["amber"][0]}" stroke-width="1.3" stroke-dasharray="6 4" fill="none"/>')
    s.append(t(bx0 + 18, top + 30, 'B', 'plabel', 'start'))
    s.append(t(bx0 + 40, top + 30, 'What an institution can use', 'ptitle', 'start'))
    s.append(t(bx0 + 40, top + 52, '66 coded mechanisms in 18 themes and six families (Fig. 4)', 'pnote', 'start'))
    s += circle(cx, cy)
    # evidence key inside panel B
    ky = by1 - 22
    kx = bx0 + 18
    s.append(t(kx, ky + 4, 'LLM-agent evidence:', 'key', 'start'))
    kx += 150
    for kind, label in (('tested', 'tested'), ('proposed', 'proposed only'), ('none', 'none yet')):
        fill = INK if kind == 'tested' else '#fff'
        s.append(f'<circle cx="{kx}" cy="{ky}" r="4" fill="{fill}" stroke="{INK}" stroke-width="1.3"/>')
        if kind == 'proposed': s.append(f'<circle cx="{kx}" cy="{ky}" r="1.4" fill="{INK}"/>')
        s.append(t(kx + 10, ky + 4.5, label, 'key', 'start')); kx += 24 + 8.2 * len(label)
    # the claim, left of panel B
    claim = ['Evaluate the', 'model-in-', 'institution,', 'not the model', 'alone.']
    for i, line in enumerate(claim):
        s.append(t(0, top + 70 + i * 32, line, 'claim', 'start'))
    notes = ['Individually aligned agents can', 'still fail as a group. Institutions', 'can prevent that, but they add', 'costs and failures of their own,', 'so the outcomes are hypotheses', 'to test, not results.']
    for i, line in enumerate(notes):
        s.append(t(0, top + 260 + i * 21, line, 'note', 'start'))
    H = by1 + 6
    return s, H

def main():
    s, H = build()
    css = f'''
  text{{font-family:"Helvetica Neue",Arial,sans-serif;}}
  .plabel{{font-size:20px;font-weight:900;fill:{INK};}}
  .ptitle{{font-size:18px;font-weight:800;fill:{INK};}}
  .pnote{{font-size:14.5px;font-style:italic;fill:{MUTED};}}
  .barlabel{{font-size:14.5px;font-weight:700;}}
  .btitle{{font-size:16.5px;font-weight:800;}}
  .bsub{{font-size:14px;fill:{INK};}}
  .edge{{stroke:{INK};stroke-width:1.8;fill:none;}}
  .lk{{fill:none;stroke-width:1.1;opacity:.6;}}
  .famlabel{{font-size:13.5px;font-weight:900;letter-spacing:.04em;paint-order:stroke;stroke:#fff;stroke-width:3.5px;}}
  .thlabel{{font-size:13.5px;font-weight:700;}}
  .hubn{{font-size:19px;font-weight:900;fill:#111;}}
  .hubs{{font-size:9.5px;font-weight:700;fill:{MUTED};letter-spacing:.06em;}}
  .claim{{font-size:26px;font-weight:900;fill:#111;letter-spacing:-.3px;}}
  .note{{font-size:15px;fill:{INK};}}
  .key{{font-size:14px;fill:{MUTED};}}
  .fnchip{{font-size:13.5px;font-weight:800;}}'''
    body = '\n'.join(s)
    html = f'''<!DOCTYPE html>
<html lang="en"><head><meta charset="UTF-8"><title>Fig. 1 draft: causal chain with taxonomy circle</title>
<!-- Draft Fig. 1 generated by scripts/gen_fig1_chain.py; data from docs/assets/taxonomy.json. -->
<style>{css}
  html,body{{margin:0;background:#fff;}} .fig{{width:{W}px;margin:0 auto;padding:12px;}}
</style></head><body><div class="fig">
<svg viewBox="-6 -4 {W+12} {H+8}" width="{W+12}" height="{H+8}" xmlns="http://www.w3.org/2000/svg">
<defs><marker id="ah" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="{INK}"/></marker></defs>
{body}
</svg></div></body></html>'''
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    open(OUT, 'w', encoding='utf-8').write(html)
    minpx = 9.5
    print(f'wrote {os.path.relpath(OUT)} ({W}x{H:.0f}); smallest body text 13.5px = {13.5 * TEXTWIDTH_PT / (W + 12):.1f}pt at text width')

if __name__ == '__main__':
    main()
