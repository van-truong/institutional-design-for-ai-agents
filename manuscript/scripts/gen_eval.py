#!/usr/bin/env python3
"""Generate Fig. 6: the model-in-institution evaluation design, as a schematic (no scores).

Rows vary the institution; columns vary the agent population. Each cell is a small multiple of four
outcome bars (cooperation and three of its costs or safeguards), drawn schematically without values.
The pattern shows an interaction: the fixed fine that helps a homogeneous group backfires in a mixed
group, which is why institutions must be evaluated together with the agents they govern. A band marks
the single row that most existing benchmarks sample.
The previous score matrix is archived in figs/archive/. Run from manuscript/:  python3 scripts/gen_eval.py
"""
FONT = "'Helvetica Neue', Arial, sans-serif"
INK = "#3F4D5A"; MUT = "#6B7787"; HAIR = "#B3BEC9"; HEAD = "#2C2C2A"
GREEN = "#4F9070"; AMBER = "#C79A3A"; TERRA = "#C2662A"; TEAL = "#0F766E"
AMBER_D = "#8A5A0B"; VIOLET_D = "#463BA0"; TERRA_D = "#8F3F1E"
BLUE_BG = "#DCE8F5"; BLUE = "#3A6EA5"

TEXTWIDTH_PT = 347.0
COLS = ['Homogeneous\ngroup A', 'Homogeneous\ngroup B', 'Mixed group\nA + B']
ROWS = ['No enforcement', 'Fixed fine', 'Graduated +\nrepair + appeal']
METRICS = [('cooperation', GREEN), ('enforcement cost', AMBER), ('false punishment', TERRA), ('repair', TEAL)]
# schematic bar heights (row, col) -> (cooperation, enforcement cost, false punishment, repair)
V = [[(0.35, 0, 0, 0), (0.28, 0, 0, 0), (0.22, 0, 0, 0)],
     [(0.80, 0.35, 0.18, 0), (0.66, 0.40, 0.28, 0), (0.26, 0.72, 0.78, 0)],
     [(0.82, 0.25, 0.10, 0.70), (0.76, 0.28, 0.12, 0.66), (0.72, 0.34, 0.16, 0.62)]]
CROSS = (1, 2)          # the cell where the fine backfires
BENCH_ROW = 0           # the row most benchmarks occupy

GX = 176; GY = 120; CW = 158; RH = 118; cw = 132; ch = 96
W = GX + len(COLS) * CW + 18
H = GY + len(ROWS) * RH + 104
FS_MIN = 13.0

def esc(s): return s.replace('&', '&amp;')

def lines(x, y, text, anchor, size, weight, color, lh=17):
    ls = text.split('\n'); y0 = y - (len(ls) - 1) * lh / 2
    return ''.join(f'<text x="{x:.1f}" y="{y0 + k * lh:.1f}" text-anchor="{anchor}" dominant-baseline="central" font-size="{size}" '
                   f'font-weight="{weight}" fill="{color}">{esc(l)}</text>' for k, l in enumerate(ls))

def cell(x, y, vals, highlight):
    o = [f'<rect x="{x:.1f}" y="{y:.1f}" width="{cw}" height="{ch}" rx="8" fill="#F7F9FB" '
         f'stroke="{TERRA if highlight else HAIR}" stroke-width="{2.2 if highlight else 0.8}"/>']
    base = y + ch - 14; top = y + 14; bw = 18; gap = (cw - 4 * bw) / 5
    o.append(f'<line x1="{x + 10:.1f}" y1="{base:.1f}" x2="{x + cw - 10:.1f}" y2="{base:.1f}" stroke="{HAIR}" stroke-width="0.8"/>')
    for k, ((_, col), v) in enumerate(zip(METRICS, vals)):
        bx = x + gap + k * (bw + gap); h = (base - top) * v
        if v > 0:
            o.append(f'<rect x="{bx:.1f}" y="{base - h:.1f}" width="{bw}" height="{h:.1f}" rx="2" fill="{col}"/>')
        else:
            o.append(f'<rect x="{bx:.1f}" y="{base - 2:.1f}" width="{bw}" height="2" fill="{col}" opacity="0.45"/>')
    return ''.join(o)

def build():
    o = [f'<svg width="100%" viewBox="0 0 {W} {H}" role="img" xmlns="http://www.w3.org/2000/svg" font-family="{FONT}">',
         '<title>The model-in-institution evaluation design</title>',
         f'<defs><marker id="ev" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">'
         f'<path d="M2 1L8 5L2 9" fill="none" stroke="{INK}" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></marker></defs>',
         f'<text x="{W / 2:.0f}" y="26" text-anchor="middle" font-size="16" font-weight="700" fill="{MUT}" letter-spacing="1.2">EVALUATING THE MODEL-IN-INSTITUTION</text>']
    gw = len(COLS) * CW; gh = len(ROWS) * RH
    # sweep arrows
    o.append(f'<line x1="{GX + 6}" y1="60" x2="{GX + gw - 10}" y2="60" stroke="{INK}" stroke-width="1.6" marker-end="url(#ev)"/>')
    o.append(f'<text x="{GX + gw / 2:.0f}" y="52" text-anchor="middle" font-size="14" font-weight="700" fill="{INK}">vary the agents &#8594; does the institution transfer?</text>')
    o.append(f'<line x1="30" y1="{GY + 4}" x2="30" y2="{GY + gh - 8}" stroke="{INK}" stroke-width="1.6" marker-end="url(#ev)"/>')
    o.append(f'<text x="22" y="{GY + gh / 2:.0f}" text-anchor="middle" font-size="14" font-weight="700" fill="{INK}" '
             f'transform="rotate(-90 22 {GY + gh / 2:.0f})">vary the institution &#8594; which works, at what cost?</text>')
    # benchmark band (drawn first, under the row)
    by = GY + BENCH_ROW * RH + 2
    o.append(f'<rect x="{44}" y="{by:.1f}" width="{GX + gw - 40:.1f}" height="{RH - 4}" rx="10" fill="{BLUE_BG}" opacity="0.75"/>')
    o.append(f'<text x="{56}" y="{by + RH - 30:.1f}" font-size="{FS_MIN}" font-style="italic" fill="{BLUE}">most benchmarks:</text>')
    o.append(f'<text x="{56}" y="{by + RH - 14:.1f}" font-size="{FS_MIN}" font-style="italic" fill="{BLUE}">one fixed row</text>')
    # column headers
    for j, c in enumerate(COLS):
        o.append(lines(GX + j * CW + CW / 2, GY - 22, c, 'middle', 14.5, 700, AMBER_D))
    # rows
    for i, r in enumerate(ROWS):
        ry = GY + i * RH
        o.append(lines(GX - 14, ry + RH / 2 - (16 if i == BENCH_ROW else 0), r, 'end', 14.5, 700, VIOLET_D))
        for j in range(len(COLS)):
            x = GX + j * CW + (CW - cw) / 2; y = ry + (RH - ch) / 2
            o.append(cell(x, y, V[i][j], (i, j) == CROSS))
    # interaction callout
    cxr = GX + CROSS[1] * CW + CW / 2; cyr = GY + CROSS[0] * RH + (RH - ch) / 2
    ty = GY + gh + 22
    o.append(f'<text x="{GX + gw:.0f}" y="{ty:.0f}" text-anchor="end" font-size="{FS_MIN}" font-weight="700" fill="{TERRA_D}">'
             f'Interaction: the fine that helps group A backfires in the mixed group.</text>')
    # legend
    ly = ty + 34; lx = 44
    o.append(f'<text x="{lx}" y="{ly}" font-size="{FS_MIN}" font-weight="700" fill="{INK}">Each cell, repeated runs:</text>')
    lx += 172
    for lab, col in METRICS:
        o.append(f'<rect x="{lx}" y="{ly - 10}" width="11" height="11" rx="2" fill="{col}"/>')
        o.append(f'<text x="{lx + 16}" y="{ly}" font-size="{FS_MIN}" fill="{MUT}">{lab}</text>')
        lx += 16 + len(lab) * 6.9 + 14
    o.append(f'<text x="{44}" y="{ly + 22}" font-size="{FS_MIN}" fill="{MUT}">Bars are schematic, not results.</text>')
    o.append('</svg>')
    minpt = FS_MIN * TEXTWIDTH_PT / W
    assert minpt >= 6.0, minpt
    return '\n'.join(o), minpt

if __name__ == '__main__':
    svg, minpt = build()
    open('figs/figure6_model-in-institution-eval.html', 'w').write(svg)
    print(f'wrote figs/figure6_model-in-institution-eval.html (viewBox {W}x{H}, min font {minpt:.2f}pt)')
