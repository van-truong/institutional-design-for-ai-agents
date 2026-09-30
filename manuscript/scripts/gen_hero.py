#!/usr/bin/env python3
"""Generate Fig. 1: same agents, different institutions, different outcomes.

Three conditions with identical agents sharing one resource:
  A  no institution          -> the commons is depleted
  B  a naive fine            -> measured cooperation rises, but hidden costs appear (gaming, false punishment, lost norms)
  C  a designed institution  -> cooperation is sustained at low cost, with humans setting the rules above it
Each panel ends in the same two schematic bars (cooperation, hidden costs), without numbers.
The previous three-beat version is archived in figs/archive/. Single SVG, master palette, text >= 6 pt at \\textwidth.
Run from manuscript/:  python3 scripts/gen_hero.py
"""
FONT = "'Helvetica Neue', Arial, sans-serif"
INK = "#3F4D5A"; MUT = "#6B7787"; HAIR = "#B3BEC9"; HEAD = "#2C2C2A"
BLUE = "#3A6EA5"; BLUE_L = "#A9C4E0"; BLUE_BG = "#DCE8F5"
GREEN = "#4F9070"; GREEN_D = "#2F6B4A"; GREEN_BG = "#E5F0E1"
TERRA = "#C2662A"; TERRA_D = "#8F3F1E"; TERRA_BG = "#FBEDE6"
AMBER = "#C79A3A"; AMBER_D = "#8A5A0B"; AMBER_BG = "#FBEEDA"
VIOLET = "#6C5CD0"; VIOLET_D = "#463BA0"; VIOLET_BG = "#ECE9FB"
NEUT_BG = "#F4F6F8"

TEXTWIDTH_PT = 347.0
W = 850
PX = [12, 291, 570]; PW = 268
PY = 70; PH = 356
SCENE_Y = PY + 128          # agents row
POOL_Y = PY + 196           # top of the resource cylinder
DASH_Y = PY + 262           # outcome bars
MIN_FONT = 15.0

def esc(s): return s.replace('&', '&amp;')

def agent(cx, cy, color=BLUE):
    return (f'<g><rect x="{cx - 15:.1f}" y="{cy - 11:.1f}" width="30" height="30" rx="7" fill="#FFFFFF" stroke="{color}" stroke-width="1.7"/>'
            f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="5" fill="{color}"/>'
            f'<line x1="{cx - 7:.1f}" y1="{cy + 10:.1f}" x2="{cx + 7:.1f}" y2="{cy + 10:.1f}" stroke="{color}" stroke-width="1.7" stroke-linecap="round"/></g>')

def person(cx, cy, color):
    return (f'<g><circle cx="{cx:.1f}" cy="{cy - 7:.1f}" r="6" fill="{color}"/>'
            f'<path d="M {cx - 10:.1f} {cy + 11:.1f} Q {cx:.1f} {cy - 3:.1f} {cx + 10:.1f} {cy + 11:.1f} Z" fill="{color}"/></g>')

def badge(cx, cy, kind):
    col = {'ok': GREEN, 'bad': TERRA, 'warn': AMBER}[kind]
    o = f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="12" fill="{col}"/>'
    if kind == 'ok':
        o += f'<path d="M {cx - 5.5:.1f} {cy:.1f} L {cx - 1.5:.1f} {cy + 4.5:.1f} L {cx + 6:.1f} {cy - 4.5:.1f}" fill="none" stroke="#FFF" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/>'
    elif kind == 'bad':
        o += (f'<path d="M {cx - 5:.1f} {cy - 5:.1f} L {cx + 5:.1f} {cy + 5:.1f} M {cx + 5:.1f} {cy - 5:.1f} L {cx - 5:.1f} {cy + 5:.1f}" '
              f'stroke="#FFF" stroke-width="2.4" stroke-linecap="round"/>')
    else:
        o += (f'<line x1="{cx:.1f}" y1="{cy - 6:.1f}" x2="{cx:.1f}" y2="{cy + 2:.1f}" stroke="#FFF" stroke-width="2.6" stroke-linecap="round"/>'
              f'<circle cx="{cx:.1f}" cy="{cy + 6.5:.1f}" r="1.6" fill="#FFF"/>')
    return o

def pool(cx, top, level, stroke):
    """Cylinder of shared resource; level in [0,1]."""
    rx, ry, h = 52, 9, 34
    o = [f'<rect x="{cx - rx:.1f}" y="{top:.1f}" width="{2 * rx}" height="{h}" fill="#FFFFFF"/>']
    fh = h * level
    if level > 0:
        o.append(f'<rect x="{cx - rx:.1f}" y="{top + h - fh:.1f}" width="{2 * rx}" height="{fh:.1f}" fill="{BLUE_L}"/>')
        o.append(f'<ellipse cx="{cx:.1f}" cy="{top + h - fh:.1f}" rx="{rx}" ry="{ry}" fill="{BLUE_BG}" stroke="{BLUE}" stroke-width="0.8"/>')
    o.append(f'<ellipse cx="{cx:.1f}" cy="{top + h:.1f}" rx="{rx}" ry="{ry}" fill="{BLUE_L if level > 0 else "#FFFFFF"}" stroke="{stroke}" stroke-width="1"/>')
    o.append(f'<line x1="{cx - rx:.1f}" y1="{top:.1f}" x2="{cx - rx:.1f}" y2="{top + h:.1f}" stroke="{stroke}" stroke-width="1"/>')
    o.append(f'<line x1="{cx + rx:.1f}" y1="{top:.1f}" x2="{cx + rx:.1f}" y2="{top + h:.1f}" stroke="{stroke}" stroke-width="1"/>')
    o.append(f'<ellipse cx="{cx:.1f}" cy="{top:.1f}" rx="{rx}" ry="{ry}" fill="none" stroke="{stroke}" stroke-width="1"/>')
    return ''.join(o)

def pill(cx, cy, text, color, bg):
    w = len(text) * 7.9 + 18
    return (f'<g><rect x="{cx - w / 2:.1f}" y="{cy - 10:.1f}" width="{w:.1f}" height="20" rx="10" fill="{bg}" stroke="{color}" stroke-width="0.8"/>'
            f'<text x="{cx:.1f}" y="{cy:.1f}" text-anchor="middle" dominant-baseline="central" font-size="{MIN_FONT}" fill="{color}">{esc(text)}</text></g>')

def bars(x, y, coop, cost):
    """Two schematic outcome bars, no values."""
    o = []; bw = PW - 128
    for i, (lab, v, col) in enumerate((('Cooperation', coop, GREEN), ('Hidden costs', cost, TERRA))):
        by = y + i * 24
        o.append(f'<text x="{x + 16:.1f}" y="{by:.1f}" dominant-baseline="central" font-size="{MIN_FONT}" fill="{INK}">{lab}</text>')
        bx = x + 112
        o.append(f'<rect x="{bx:.1f}" y="{by - 5:.1f}" width="{bw}" height="10" rx="5" fill="#E7EAEE"/>')
        if v > 0:
            o.append(f'<rect x="{bx:.1f}" y="{by - 5:.1f}" width="{bw * v:.1f}" height="10" rx="5" fill="{col}"/>')
    return ''.join(o)

def panel(x, letter, title, bg, stroke, color):
    return (f'<rect x="{x}" y="{PY}" width="{PW}" height="{PH}" rx="14" fill="{bg}" stroke="{stroke}" stroke-width="1"/>'
            f'<text x="{x + 16}" y="{PY + 30}" font-size="18" font-weight="700" fill="{HEAD}">{letter}</text>'
            f'<text x="{x + 36}" y="{PY + 30}" font-size="18" font-weight="700" fill="{HEAD}">{esc(title)}</text>')

def outcome(x, lines, color):
    return ''.join(f'<text x="{x + PW / 2:.1f}" y="{PY + PH - 36 + i * 19:.1f}" text-anchor="middle" font-size="{MIN_FONT}" fill="{color}">{esc(l)}</text>'
                   for i, l in enumerate(lines))

def agents_extracting(cx, heavy, color):
    o = []
    for ax in (cx - 58, cx, cx + 58):
        o.append(agent(ax, SCENE_Y, BLUE))
        o.append(f'<line x1="{ax:.1f}" y1="{SCENE_Y + 22:.1f}" x2="{ax * 0.6 + cx * 0.4:.1f}" y2="{POOL_Y - 6:.1f}" stroke="{color}" '
                 f'stroke-width="{2.4 if heavy else 1.3}" marker-end="url(#ha)"/>')
    return ''.join(o)

def build():
    o = [f'<svg width="100%" viewBox="0 0 {W} {PY + PH + 60}" role="img" xmlns="http://www.w3.org/2000/svg" font-family="{FONT}">',
         '<title>Same agents, different institutions, different outcomes</title>',
         f'<defs><marker id="ha" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="5" markerHeight="5" orient="auto-start-reverse">'
         f'<path d="M2 1L8 5L2 9" fill="none" stroke="context-stroke" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></marker></defs>',
         f'<text x="{W / 2:.1f}" y="28" text-anchor="middle" font-size="17" font-weight="700" fill="{MUT}" letter-spacing="1.4">SAME AGENTS, DIFFERENT INSTITUTIONS</text>',
         f'<text x="{W / 2:.1f}" y="52" text-anchor="middle" font-size="{MIN_FONT}" fill="{MUT}">Three identical, individually aligned agents share one finite resource.</text>']

    # A: no institution
    x = PX[0]; cx = x + PW / 2
    o.append(panel(x, 'A', 'No institution', TERRA_BG, TERRA, TERRA_D))
    o.append(agents_extracting(cx, True, TERRA_D))
    o.append(pool(cx, POOL_Y, 0.12, TERRA_D))
    o.append(badge(x + PW - 28, PY + 24, 'bad'))
    o.append(bars(x, DASH_Y, 0.18, 0.0))
    o.append(outcome(x, ['Each agent is safe alone;', 'together they deplete the commons.'], TERRA_D))

    # B: naive fine
    x = PX[1]; cx = x + PW / 2
    o.append(panel(x, 'B', 'A naïve fine', AMBER_BG, AMBER, AMBER_D))
    o.append(agents_extracting(cx, False, AMBER_D))
    o.append(pool(cx, POOL_Y, 0.55, AMBER_D))
    o.append(pill(cx, PY + 70, 'fixed fine per violation', AMBER_D, '#FFFFFF'))
    o.append(badge(x + PW - 28, PY + 24, 'warn'))
    o.append(bars(x, DASH_Y, 0.7, 0.62))
    o.append(outcome(x, ['Measured cooperation rises, but agents', 'game it; false fines erode trust.'], AMBER_D))

    # C: designed institution with human layer
    x = PX[2]; cx = x + PW / 2
    o.append(panel(x, 'C', 'A designed institution', GREEN_BG, GREEN, GREEN_D))
    fy = SCENE_Y - 34
    o.append(f'<rect x="{cx - 104:.1f}" y="{fy:.1f}" width="208" height="72" rx="10" fill="{VIOLET_BG}" stroke="{VIOLET_D}" stroke-width="1.2" stroke-dasharray="5 3"/>')
    o.append(f'<text x="{cx + 100:.1f}" y="{fy + 14:.1f}" text-anchor="end" font-size="{MIN_FONT}" font-style="italic" fill="{VIOLET_D}">institution</text>')
    o.append(agents_extracting(cx, False, GREEN_D))
    o.append(pool(cx, POOL_Y, 0.85, GREEN_D))
    # human layer above the institution
    hx = x + 38; hy = PY + 66
    o.append(person(hx, hy, INK))
    o.append(f'<text x="{hx + 18:.1f}" y="{hy - 4:.1f}" font-size="{MIN_FONT}" fill="{INK}">humans set rules,</text>')
    o.append(f'<text x="{hx + 18:.1f}" y="{hy + 14:.1f}" font-size="{MIN_FONT}" fill="{INK}">can intervene</text>')
    o.append(f'<line x1="{hx:.1f}" y1="{hy + 14:.1f}" x2="{hx:.1f}" y2="{fy:.1f}" stroke="{INK}" stroke-width="1.3" stroke-dasharray="3 3" marker-end="url(#ha)"/>')
    o.append(badge(x + PW - 28, PY + 24, 'ok'))
    o.append(bars(x, DASH_Y, 0.8, 0.14))
    o.append(outcome(x, ['Graduated sanctions, repair, appeal:', 'cooperation sustained at low cost.'], GREEN_D))

    # one-line position
    by = PY + PH + 34
    o.append(f'<text x="{W / 2:.1f}" y="{by:.1f}" text-anchor="middle" font-size="16.5" fill="{INK}">'
             f'<tspan font-weight="700" fill="{GREEN_D}">Position:</tspan>&#160;evaluate the model-in-institution, not the model alone, and let humans author the rules.</text>')
    o.append('</svg>')
    minpt = MIN_FONT * TEXTWIDTH_PT / W
    assert minpt >= 6.0, minpt
    return '\n'.join(o), minpt

if __name__ == '__main__':
    svg, minpt = build()
    open('figs/figure1_position-summary.html', 'w').write(svg)
    print(f'wrote figs/figure1_position-summary.html (min font {minpt:.2f}pt)')
