#!/usr/bin/env python3
"""Fig. 2, agent-in-context: the three-layer stack, with bullets naming what happens at each level.

The three isometric layers (governing institutions, agent-group interactions, individual model) sit in a column,
each with a label and a few bullets listing what operates, emerges, or can be observed at that level, between the
top-down and bottom-up arrows. Each label also carries a miniature of Fig. 1 (the nested rings) with the rings that
correspond to that layer filled in, so the two figures read as the same picture at two resolutions. Reuses
gen_multilayer's plates, node glyphs, arrows, and colors.
Run from manuscript/:  python3 scripts/gen_agent_in_context.py
"""
import os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import gen_multilayer as ml  # noqa: E402

OUT = os.path.join(HERE, '..', 'figs', 'figure_agent-in-context.html')
W, H = 720, 504
CX, PW, PH, TH = 120, 56, 23, 9
TITLE = 'The agent in its institutional context'
LAYERS = [  # (y, top fill, side fill, label lines, label color, node glyph, Fig. 1 rings, bullets, note)
    (114, ml.AM_TOP, ml.AM_SIDE, ['Governing institutions'], ml.AM_D, ml.nodes_net, ('exo', 'macro'),
     ['norms, monitoring, sanctions, repair', 'platform, market & legal structure', 'who sets and enforces the rules'],
     'Fig. 1: exo- and macrosystem'),
    (264, ml.BL_TOP, ml.BL_SIDE, ['Agent–group interactions'], ml.BL_D, ml.nodes_tri, ('micro', 'meso'),
     ['communication, handoffs, shared memory', 'conventions, reciprocity, reputation', 'emergent roles & coordination'],
     'Fig. 1: micro- and mesosystem'),
    (414, ml.VI_TOP, ml.VI_SIDE, ['Individual model', '(even if aligned)'], ml.VI_D, ml.nodes_one, ('model',),
     ['alignment, refusals, capabilities', 'truthfulness, instruction-following', 'what single-model evals test'],
     'Fig. 1: the model at the center'),
]
# Fig. 1's rings, inner to outer: (key, radius, fill when highlighted); colors match gen_nested_rings.py
RINGS = [('model', 6, '#6C5CD0'), ('micro', 12, '#A9C4E0'), ('meso', 18, '#9FD9C7'),
         ('exo', 24, '#BBD9C4'), ('macro', 30, '#E3C88C')]
LX = 300           # left edge of the ring icon / text block


def ring_icon(cx, cy, keys):
    """A miniature of Fig. 1 with the rings that correspond to one layer filled in."""
    o = []
    for key, r, col in reversed(RINGS):
        on = key in keys
        o.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{col if on else "#fff"}" '
                 f'stroke="{"#8A96A3" if on else "#C9D1DA"}" stroke-width="{1.1 if on else 0.9}"/>')
    return ''.join(o)


def build():
    o = [f'<svg viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" xmlns="http://www.w3.org/2000/svg" font-family="{ml.FONT}">',
         '<title>Agent-in-context</title>',
         f'<text x="{W/2:.0f}" y="40" text-anchor="middle" font-size="19" font-weight="800" fill="{ml.INK}">{ml.esc(TITLE)}</text>']
    # dotted guides joining the plate edges
    for (ya, *_), (yb, *_) in zip(LAYERS, LAYERS[1:]):
        for x in (CX - PW, CX + PW):
            o.append(f'<line x1="{x}" y1="{ya + TH + 2}" x2="{x}" y2="{yb - 2}" stroke="{ml.HAIR}" stroke-width="1" stroke-dasharray="2 4" opacity="0.7"/>')
    for y, top, side, label, col, nodes, *_ in LAYERS:
        o.append(ml.diamond(CX, y, PW, PH, TH, top, side, [], col, nodes))
    # arrows: top-down on the left, bottom-up between the plates and the text
    ytop, ybot = LAYERS[0][0] - PH - 6, LAYERS[-1][0] + PH + TH + 6
    ymid = (ytop + ybot) / 2
    o.append(ml.varrow(34, ytop, ybot, ml.AM_M))
    o.append(f'<text x="15" y="{ymid:.0f}" text-anchor="middle" font-size="15.5" font-weight="700" fill="{ml.AM_M}" transform="rotate(-90 15 {ymid:.0f})">Top-down</text>')
    o.append(ml.varrow(206, ybot, ytop, ml.VI_M))
    o.append(f'<text x="225" y="{ymid:.0f}" text-anchor="middle" font-size="15.5" font-weight="700" fill="{ml.VI_M}" transform="rotate(-90 225 {ymid:.0f})">Bottom-up</text>')
    # per layer: ring icon, label, bullets, and a note naming the matching rings of Fig. 1
    tx = LX + 42
    for y, top, side, label, col, nodes, rings, bullets, note in LAYERS:
        yb = y - 46
        o.append(ring_icon(LX + 2, yb + 32, rings))
        for i, line in enumerate(label):
            style = 'font-weight="400" font-style="italic"' if line.startswith('(') else 'font-weight="800"'
            o.append(f'<text x="{tx}" y="{yb + i * 19:.0f}" font-size="16.5" {style} fill="{col}">{ml.esc(line)}</text>')
        yy = yb + len(label) * 19 + 4
        for b in bullets:
            o.append(f'<circle cx="{tx + 3:.0f}" cy="{yy - 4:.0f}" r="2.1" fill="{col}"/>')
            o.append(f'<text x="{tx + 12}" y="{yy:.0f}" font-size="13.5" fill="{ml.INK}">{ml.esc(b)}</text>')
            yy += 18
        o.append(f'<text x="{tx}" y="{yy + 2:.0f}" font-size="12.5" font-style="italic" fill="{ml.MUT}">{ml.esc(note)}</text>')
    o.append('</svg>')
    return '\n'.join(o)


def main():
    svg = build()
    html = (f'<!DOCTYPE html>\n<html lang="en"><head><meta charset="UTF-8"><title>Agent-in-context</title>\n'
            f'<!-- Generated by scripts/gen_agent_in_context.py. -->\n'
            f'<style>html,body{{margin:0;background:#fff;}} .fig{{width:{W}px;margin:0 auto;padding:12px;}}</style></head>'
            f'<body><div class="fig">\n{svg}\n</div></body></html>')
    open(OUT, 'w', encoding='utf-8').write(html)
    print('wrote', os.path.relpath(OUT), f'{W}x{H}')


if __name__ == '__main__':
    main()
