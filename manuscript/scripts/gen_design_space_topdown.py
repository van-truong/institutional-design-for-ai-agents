#!/usr/bin/env python3
"""Fig.: the design space of agent institutions as a top-down tree (alternative to figure_design-space).

Root at top, branching into institutional functions and mechanism families, then into four groups; each group's
leaves stack vertically beneath it on a spine, so every label reads horizontally and the figure fits at
\\linewidth. Labels, groups, and colors come from gen_multilayer.py so the two versions stay in sync.
Writes figures/figure_design-space-topdown.svg/.pdf. Run from manuscript/:  python3 scripts/gen_design_space_topdown.py
"""
import os, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from gen_multilayer import FONT, INK, BLK, FC_M, VI_M, MECH, CHAN, FAMILY_LEAF, esc, wrap  # noqa: E402

OUT_SVG = os.path.join(HERE, '..', 'figures', 'figure_design-space-topdown.svg')
OUT_PDF = os.path.join(HERE, '..', 'figures', 'figure_design-space-topdown.pdf')

# geometry: four columns, a wider gap between the two sections
COLW, COLGAP, SECGAP, MARGIN = 150, 18, 36, 12
LEFTS = [MARGIN, MARGIN + COLW + COLGAP]
LEFTS += [LEFTS[1] + COLW + SECGAP, LEFTS[1] + COLW + SECGAP + COLW + COLGAP]
W = LEFTS[3] + COLW + MARGIN
ROOT_Y, BAR1_Y, SEC_Y, BAR2_Y, GRP_Y = 66, 100, 122, 146, 162   # GRP_Y: top of group boxes
GRP_H, LEAF_H, PITCH, LEAF0 = 34, 32, 41, 226                  # LEAF0: first leaf center
SPINE_DX, LEAF_DX = 12, 24                                     # spine and leaf offsets from column left
LEAF_W = COLW - LEAF_DX
LEAF_WRAP = 15


def text(x, y, s, size, color, weight='700', style='', extra=''):
    st = f' font-style="{style}"' if style else ''
    return (f'<text x="{x:.1f}" y="{y:.1f}" text-anchor="middle" font-size="{size}" font-weight="{weight}"{st} '
            f'fill="{color}"{extra}>{esc(s)}</text>')


def line(x1, y1, x2, y2, color, w=1.2, op=0.75):
    return (f'<path d="M {x1:.1f} {y1:.1f} L {x2:.1f} {y2:.1f}" fill="none" stroke="{color}" stroke-width="{w}" '
            f'opacity="{op}" stroke-linecap="round"/>')


def leaf(x0, cy, name, sub, dcol, bg, mcol):
    cx = x0 + LEAF_W / 2
    o = [f'<rect x="{x0:.1f}" y="{cy - LEAF_H / 2:.1f}" width="{LEAF_W}" height="{LEAF_H}" rx="8" fill="{bg}" '
         f'stroke="{mcol}" stroke-width="0.9"/>']
    if sub:
        o += [text(cx, cy - 2.5, name, 14, dcol), text(cx, cy + 11.5, sub, 13, '#6B7787', '400', 'italic')]
    else:
        ln = wrap(name, LEAF_WRAP)
        if len(ln) == 1:
            o.append(text(cx, cy + 5, name, 14, dcol))
        else:
            o += [text(cx, cy - 2.5, ln[0], 14, dcol), text(cx, cy + 12, ln[1], 14, dcol)]
    return o


def build():
    sections = [('INSTITUTIONAL FUNCTIONS', FC_M, MECH, LEFTS[:2]), ('MECHANISM FAMILIES', VI_M, CHAN, LEFTS[2:])]
    nmax = max(len(g[4]) for _, _, grp, _ in sections for g in grp)
    H = LEAF0 + (nmax - 1) * PITCH + LEAF_H / 2 + 14
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H:.0f}" width="{W}" height="{H:.0f}" '
         f'font-family="{FONT}" role="img">', '<title>Design space of agent institutions</title>',
         '<rect width="100%" height="100%" fill="#fff"/>',
         f'<text x="{MARGIN}" y="26" font-size="17" font-weight="700" fill="{BLK}">Design space of agent institutions</text>']
    # root
    rcx = W / 2
    sec_cx = [(l[0] + l[1] + COLW) / 2 for _, _, _, l in sections]
    o.append(line(rcx, ROOT_Y + 20, rcx, BAR1_Y, INK))
    o.append(line(sec_cx[0], BAR1_Y, sec_cx[1], BAR1_Y, INK))
    o += [f'<rect x="{rcx - 88:.1f}" y="{ROOT_Y - 20}" width="176" height="40" rx="20" fill="#F7F9FB" stroke="{INK}" '
          f'stroke-width="1.1"/>', text(rcx, ROOT_Y + 5.5, 'Agent institution', 15.5, INK)]
    for (sname, scol, grp, lefts), scx in zip(sections, sec_cx):
        o.append(line(scx, BAR1_Y, scx, SEC_Y - 13, scol))
        o.append(text(scx, SEC_Y + 4, sname, 13.5, scol, extra=' letter-spacing="0.7"'))
        gcx = [l + COLW / 2 for l in lefts]
        o.append(line(scx, SEC_Y + 10, scx, BAR2_Y, scol))
        o.append(line(gcx[0], BAR2_Y, gcx[1], BAR2_Y, scol))
        for (gname, dcol, bg, mcol, leaves), left, cx in zip(grp, lefts, gcx):
            o.append(line(cx, BAR2_Y, cx, GRP_Y, mcol))
            o.append(f'<rect x="{left}" y="{GRP_Y}" width="{COLW}" height="{GRP_H}" rx="8" fill="{bg}" stroke="{mcol}" '
                     f'stroke-width="1.1"/>')
            o.append(text(cx, GRP_Y + GRP_H / 2 + 5, gname, 14.5, dcol))
            lys = [LEAF0 + i * PITCH for i in range(len(leaves))]
            sx = left + SPINE_DX
            o.append(line(sx, GRP_Y + GRP_H, sx, lys[-1], mcol, 1, 0.6))
            for (name, sub), ly in zip(leaves, lys):
                ld, lb, lm = FAMILY_LEAF.get(name, (dcol, bg, mcol))
                o.append(line(sx, ly, left + LEAF_DX, ly, lm, 1, 0.6))
                o += leaf(left + LEAF_DX, ly, name, sub, ld, lb, lm)
    o.append('</svg>')
    return '\n'.join(o)


if __name__ == '__main__':
    open(OUT_SVG, 'w', encoding='utf-8').write(build())
    subprocess.run(['rsvg-convert', '--format', 'pdf1.5', '-o', OUT_PDF, OUT_SVG], check=True)
    print(f'wrote {os.path.relpath(OUT_PDF)}')
