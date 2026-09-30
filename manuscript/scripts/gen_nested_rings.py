#!/usr/bin/env python3
"""Fig. 1: nested systems around interacting agents (Bronfenbrenner), with a cutaway "viewing window".

Concentric bands -- individual model at the center, microsystem and mesosystem (agent-group interactions), and
exosystem and macrosystem (governing institutions). A pie-slice wedge at the top is a cutaway that zooms outward:
one model -> a group of agents interacting -> a higher-order society, with arrows for the transitions. The mechanism
taxonomy is no longer embedded here (it lives in the taxonomy figure and the interactive site). Colors: figs/PALETTE.md.
Run from manuscript/:  python3 scripts/gen_nested_rings.py
"""
import math, os, subprocess
from html import escape

HERE = os.path.dirname(os.path.abspath(__file__))
OUT_HTML = os.path.join(HERE, '..', 'figs', 'figure_nested-rings.html')
OUT_SVG = os.path.join(HERE, '..', 'figures', 'figure_nested-rings.svg')
OUT_PDF = os.path.join(HERE, '..', 'figures', 'figure_nested-rings.pdf')

FONT = "'Helvetica Neue', Arial, sans-serif"
INK, MUT, HAIR, PAGE = '#3F4D5A', '#6B7787', '#B3BEC9', '#FBFAF7'
SC = float(os.environ.get('RINGS_TEXT_SCALE', '1.0'))

# band colors (mid, dark, tint)
MODEL = ('#6C5CD0', '#463BA0', '#ECE9FB')
MICRO = ('#3A6EA5', '#2F3D6B', '#DCE8F5')
MESO  = ('#0F766E', '#04342C', '#E3F1EC')
EXO   = ('#4F9070', '#2F6B4A', '#E5F0E1')
MACRO = ('#C79A3A', '#8A5A0B', '#FBEEDA')

CX, CY = 590, 610
# outer radius of each band, inner -> outer
R_MODEL, R_MICRO, R_MESO, R_EXO, R_MACRO = 90, 196, 300, 420, 548
BANDS = [(R_MACRO, MACRO, 'MACROSYSTEM'), (R_EXO, EXO, 'EXOSYSTEM'),
         (R_MESO, MESO, 'MESOSYSTEM'), (R_MICRO, MICRO, 'MICROSYSTEM'), (R_MODEL, MODEL, None)]
# example settings inside each ring, placed on the lower arc (angles in deg, 90 = straight down)
MICRO_ITEMS = [('user', 150), ('tools', 30), ('task', 90)]
MESO_ITEMS = [('handoffs', 145), ('orchestrator', 35), ('shared memory', 90)]
EXO_ITEMS = [('platform policy', 150), ('API limits', 30), ('other agents', 90)]
MACRO_ITEMS = [('law & regulation', 152), ('markets', 28), ('cultural values', 90)]
# cutaway wedge: a sector at the top
WA0, WA1 = -125, -55          # wedge angular span (deg); -90 = straight up
LEG_X, LEG_W = 1180, 470
W = LEG_X + LEG_W
H = 1250


def P(a, r):
    return CX + r * math.cos(math.radians(a)), CY + r * math.sin(math.radians(a))


def t(x, y, s, size, col, anchor='middle', weight='400', italic=False, extra=''):
    st = f' font-style="italic"' if italic else ''
    return f'<text x="{x:.1f}" y="{y:.1f}" text-anchor="{anchor}" font-size="{size:.1f}" font-weight="{weight}"{st} fill="{col}"{extra}>{escape(s)}</text>'


def robot(x, y, s, col):
    mid, dark, _ = col
    return (f'<g><line x1="{x}" y1="{y-13*s:.1f}" x2="{x}" y2="{y-18*s:.1f}" stroke="{dark}" stroke-width="{1.4*s:.1f}"/>'
            f'<circle cx="{x}" cy="{y-19.5*s:.1f}" r="{2*s:.1f}" fill="{mid}"/>'
            f'<rect x="{x-9*s:.1f}" y="{y-13*s:.1f}" width="{18*s:.1f}" height="{13*s:.1f}" rx="{3.5*s:.1f}" fill="#fff" stroke="{dark}" stroke-width="{1.5*s:.1f}"/>'
            f'<circle cx="{x-4*s:.1f}" cy="{y-6.5*s:.1f}" r="{1.8*s:.1f}" fill="{dark}"/><circle cx="{x+4*s:.1f}" cy="{y-6.5*s:.1f}" r="{1.8*s:.1f}" fill="{dark}"/>'
            f'<rect x="{x-7*s:.1f}" y="{y+1.5*s:.1f}" width="{14*s:.1f}" height="{10*s:.1f}" rx="{2.5*s:.1f}" fill="{mid}" stroke="{dark}" stroke-width="{1.3*s:.1f}"/></g>')


def wedge_path(a0, a1, r):
    x0, y0 = P(a0, r); x1, y1 = P(a1, r)
    return f'M{CX},{CY} L{x0:.1f},{y0:.1f} A{r},{r} 0 0 1 {x1:.1f},{y1:.1f} Z'


def pill(a, r, label, col):
    mid, dark, _ = col
    x, y = P(a, r)
    w = (16 + 7.2 * len(label)) * SC
    return (f'<rect x="{x-w/2:.1f}" y="{y-11*SC:.1f}" width="{w:.1f}" height="{22*SC:.1f}" rx="{11*SC:.1f}" fill="#fff" stroke="{mid}" stroke-width="1.3"/>'
            + t(x, y + 4.6*SC, label, 13*SC, dark, weight='700'))


def institution(x, y, s, col):
    """A small classical-building glyph: pediment + columns (a governing institution)."""
    mid, dark, _ = col
    o = [f'<polygon points="{x-20*s:.1f},{y-8*s:.1f} {x+20*s:.1f},{y-8*s:.1f} {x:.1f},{y-20*s:.1f}" fill="{mid}" stroke="{dark}" stroke-width="{1.2*s:.1f}"/>',
         f'<rect x="{x-20*s:.1f}" y="{y-8*s:.1f}" width="{40*s:.1f}" height="{4*s:.1f}" fill="{dark}"/>']
    for k in (-15, -5, 5, 15):
        o.append(f'<rect x="{x+k*s-1.6*s:.1f}" y="{y-4*s:.1f}" width="{3.2*s:.1f}" height="{16*s:.1f}" fill="{mid}" stroke="{dark}" stroke-width="{0.8*s:.1f}"/>')
    o.append(f'<rect x="{x-22*s:.1f}" y="{y+12*s:.1f}" width="{44*s:.1f}" height="{4*s:.1f}" fill="{dark}"/>')
    return ''.join(o)


def society_node(x, y, s, col):
    """A small institution with a few agents beneath it: one society."""
    o = [institution(x, y - 4 * s, 0.6 * s, col)]
    for k in (-1, 0, 1):
        o.append(robot(x + k * 11 * s, y + 26 * s, 0.42 * s, col))
    return ''.join(o)


def build():
    o = [f'<svg viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" xmlns="http://www.w3.org/2000/svg" font-family="{FONT}">',
         '<title>Nested systems around interacting agents</title>',
         f'<rect width="{W}" height="{H}" fill="#fff"/>']
    # rings
    for r, (mid, dark, tint), _ in BANDS:
        o.append(f'<circle cx="{CX}" cy="{CY}" r="{r}" fill="{tint}" stroke="{mid}" stroke-width="1.8"/>')
    # ring name labels on the lower arc (bottom-center of each band)
    radii = [b[0] for b in BANDS]
    for i, (r, (mid, dark, tint), name) in enumerate(BANDS):
        if name:
            rr = (r + radii[i+1]) / 2
            o.append(t(CX, CY + rr + 6*SC, name, 19*SC, dark, weight='900'))
    # ---- Bronfenbrenner hallmarks: two-way influence and mesosystem links (drawn under the pills) ----
    def arcpath(a0, a1, r):
        x0, y0 = P(a0, r); x1, y1 = P(a1, r)
        laf = 1 if (a1 - a0) % 360 > 180 else 0
        return f'M{x0:.1f} {y0:.1f} A{r} {r} 0 {laf} 1 {x1:.1f} {y1:.1f}'
    rr_micro = (R_MODEL + R_MICRO) / 2 + 22
    # cross-layer double-headed arrows: influence runs inward and outward across every layer
    for ang in (45, 135):
        (x0, y0), (x1, y1) = P(ang, R_MODEL + 8), P(ang, R_MACRO - 10)
        o.append(f'<line x1="{x0:.1f}" y1="{y0:.1f}" x2="{x1:.1f}" y2="{y1:.1f}" stroke="{MUT}" stroke-width="1.7" stroke-dasharray="6 5" opacity="0.6" marker-start="url(#ar)" marker-end="url(#ar)"/>')
    # microsystem: the agent's direct two-way ties to each setting
    for a in (30, 90, 150):
        (x0, y0), (x1, y1) = P(a, R_MODEL + 4), P(a, rr_micro - 18)
        o.append(f'<line x1="{x0:.1f}" y1="{y0:.1f}" x2="{x1:.1f}" y2="{y1:.1f}" stroke="{MICRO[0]}" stroke-width="1.7" marker-start="url(#ar)" marker-end="url(#ar)"/>')
    # mesosystem = links between microsystem settings
    for a0, a1 in ((30, 90), (90, 150)):
        o.append(f'<path d="{arcpath(a0, a1, rr_micro)}" fill="none" stroke="{MESO[0]}" stroke-width="1.7" stroke-dasharray="4 3" opacity="0.85"/>')
    # example pills on the lower arc of each ring
    for items, (r_in, r_out), col in ((MICRO_ITEMS, (R_MODEL, R_MICRO), MICRO), (MESO_ITEMS, (R_MICRO, R_MESO), MESO),
                                       (EXO_ITEMS, (R_MESO, R_EXO), EXO), (MACRO_ITEMS, (R_EXO, R_MACRO), MACRO)):
        rr = (r_in + r_out) / 2 + 22
        for label, a in items:
            o.append(pill(a, rr, label, col))
    # ---- cutaway wedge: a translucent window with the zoom scenes ----
    o.append(f'<path d="{wedge_path(WA0, WA1, R_MACRO)}" fill="#ffffff" fill-opacity="0.80" stroke="{INK}" stroke-width="1.6" stroke-dasharray="5 4"/>')
    def uarrow(r0, r1):
        o.append(f'<line x1="{CX}" y1="{CY-r0:.0f}" x2="{CX}" y2="{CY-r1:.0f}" stroke="{MUT}" stroke-width="2.4" marker-end="url(#ar)"/>')
    # scene 1: one model (center)
    o.append(robot(CX, CY - 46, 1.35, MODEL))
    o.append(t(CX, CY + 20, 'one model', 12*SC, MODEL[1], italic=True))
    uarrow(78, 100)
    # scene 2: a group of agents interacting (micro/meso)
    g = [(CX-40, CY-150), (CX+40, CY-150), (CX, CY-198)]
    for a in range(3):
        for b in range(a+1, 3):
            o.append(f'<line x1="{g[a][0]}" y1="{g[a][1]-6}" x2="{g[b][0]}" y2="{g[b][1]-6}" stroke="{MICRO[0]}" stroke-width="1.6" stroke-dasharray="4 3"/>')
    for x, y in g:
        o.append(robot(x, y, 1.0, MICRO))
    o.append(t(CX, CY - 222, 'a group interacts', 12*SC, MESO[1], italic=True))
    uarrow(240, 262)
    # scene 3: a society (a larger population)
    for k in range(-4, 5):
        o.append(robot(CX + k*22, CY - 300, 0.5, EXO))
    o.append(t(CX, CY - 328, 'a society', 12*SC, EXO[1], italic=True))
    uarrow(348, 370)
    # scene 4: many institutions and societies interacting (macro)
    nodes = [(CX-94, CY-436), (CX, CY-462), (CX+94, CY-436)]
    for a in range(3):
        for b in range(a+1, 3):
            o.append(f'<line x1="{nodes[a][0]}" y1="{nodes[a][1]}" x2="{nodes[b][0]}" y2="{nodes[b][1]}" stroke="{MACRO[1]}" stroke-width="1.5" stroke-dasharray="4 3" opacity="0.85"/>')
    for x, y in nodes:
        o.append(society_node(x, y, 1.0, MACRO))
    o.append(t(CX, CY - 508, 'institutions & societies interact', 12*SC, MACRO[1], italic=True))
    # chronosystem arc at the bottom
    R = R_MACRO + 22
    (x0, y0), (x1, y1) = P(150, R), P(30, R)
    o.append(f'<path d="M{x0:.1f} {y0:.1f} A{R} {R} 0 0 0 {x1:.1f} {y1:.1f}" fill="none" stroke="{MUT}" stroke-width="2.4" marker-end="url(#ar)"/>')
    o.append(t(CX, CY + R + 30*SC, 'CHRONOSYSTEM (TIME)', 18*SC, MUT, weight='800'))
    o += legend()
    o.append('</svg>')
    return o


# outer -> inner, so Macrosystem sits on top and the legend matches the cutaway wedge order
LEGEND = [
    ('Macrosystem', MACRO, 'law, markets, norms, culture'),
    ('Exosystem', EXO, 'settings that shape it from outside'),
    ('Mesosystem', MESO, 'links between those settings'),
    ('Microsystem', MICRO, 'settings it acts in directly'),
    ('Individual model', MODEL, 'the agent at the center'),
]
GROUPS = [(0, 1, ['governing', 'institutions']), (2, 3, ['agent-group', 'interactions']), (4, 4, ['individual', 'model'])]


def legend():
    LS = SC * 1.5
    s = []
    lx = LEG_X + 70
    line, sw = 27 * LS, 22 * LS
    tx = lx + sw + 13
    rowgap = 30 * LS
    row_h = 14 * LS + line + rowgap
    y = CY - len(LEGEND) * row_h / 2 + 30
    tops, bots = [], []
    for name, (mid, dark, tint), desc in LEGEND:
        y += 14 * LS
        s.append(f'<rect x="{lx:.1f}" y="{y-sw+3:.1f}" width="{sw:.1f}" height="{sw:.1f}" rx="5" fill="{tint}" stroke="{mid}" stroke-width="2"/>')
        s.append(t(tx, y, name, 19*LS, dark, anchor='start', weight='800'))
        tops.append(y - sw + 3)
        y += line
        s.append(t(tx, y + 2, desc, 14.5*LS, INK, anchor='start'))
        bots.append(y + 10)
        y += rowgap
    # brackets grouping rings into the three layers of Fig. 2
    bx = lx - 22
    for a, b, label in GROUPS:
        ya, yb = tops[a] - 2, bots[b]
        s.append(f'<path d="M{bx+8:.1f} {ya:.1f} L{bx:.1f} {ya:.1f} L{bx:.1f} {yb:.1f} L{bx+8:.1f} {yb:.1f}" fill="none" stroke="{HAIR}" stroke-width="2"/>')
        ym = (ya + yb) / 2
        for k, ln in enumerate(label):
            x = bx - 12 - (len(label) - 1 - k) * 20 * LS
            s.append(t(x, ym, ln, 14*LS, MUT, italic=True, extra=f' transform="rotate(-90 {x:.1f} {ym:.1f})"'))
    return s


def main():
    body = '\n'.join(build())
    marker = f'<defs><marker id="ar" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="{MUT}"/></marker></defs>'
    svg = body.replace('<title>', marker + '\n<title>', 1)
    open(OUT_SVG, 'w', encoding='utf-8').write(svg)
    html = (f'<!DOCTYPE html>\n<html lang="en"><head><meta charset="UTF-8"><title>Nested systems</title>\n'
            f'<!-- Generated by scripts/gen_nested_rings.py. -->\n'
            f'<style>html,body{{margin:0;background:#fff;}} .fig{{width:{W}px;margin:0 auto;padding:12px;}}</style></head>'
            f'<body><div class="fig">\n{svg}\n</div></body></html>')
    open(OUT_HTML, 'w', encoding='utf-8').write(html)
    subprocess.run(['rsvg-convert', '--format', 'pdf1.5', '-o', OUT_PDF, OUT_SVG], check=True)
    print('wrote', os.path.relpath(OUT_HTML), 'and', os.path.relpath(OUT_PDF))


if __name__ == '__main__':
    main()
