#!/usr/bin/env python3
"""Draft Fig. 7: the model-in-institution evaluation design as a contrast-first matrix.

Institution (rows) is crossed with agent population (columns) on one fixed task and shared resource.
Cells are unscored: each holds the four outcomes to measure, with no values. The planned contrasts are drawn
instead of results: vary the population at a fixed institution (what most benchmarks do), vary the institution
at a fixed population, and test whether the two interact. Colors follow figs/PALETTE.md.
Run from manuscript/:  python3 scripts/gen_fig7_matrix.py
"""
import os
from html import escape

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, '..', 'figs', 'drafts', 'figure7_contrast-matrix.html')

INK, MUTED, HAIR, PAGE = '#3F4D5A', '#6B7787', '#B3BEC9', '#FBFAF7'
AMBER = ('#C79A3A', '#8A5A0B', '#FBEEDA'); BLUE = ('#3A6EA5', '#2F3D6B', '#DCE8F5')
VIOLET = ('#6C5CD0', '#463BA0', '#ECE9FB'); SLATE = ('#6B7787', '#3F4D5A', '#EEF2F6')
W = 900
ROWS = [('No rules', 'shared resource only'), ('Fixed fine', 'one flat penalty'),
        ('Graduated + appeal', 'escalation, appeal, repair')]
COLS = [('Homogeneous', 'one model family'), ('Mixed', 'several model families'),
        ('Adversarial', 'plus a defecting entrant')]
OUTCOMES = [('C', 'cooperation'), ('E', 'enforcement cost'), ('F', 'false punishment'), ('R', 'repair')]
X0, Y0, CW, CH, PADC = 196, 118, 226, 100, 12
FIXED_ROW, FIXED_COL = 1, 1

def t(x, y, s, cls, anchor='middle', extra=''):
    return f'<text x="{x:.1f}" y="{y:.1f}" class="{cls}" text-anchor="{anchor}"{extra}>{escape(s)}</text>'

def build():
    s = []
    gw = 3 * CW
    # fixed task banner
    s.append(f'<rect x="{X0}" y="6" width="{gw-PADC}" height="30" rx="15" fill="{SLATE[2]}" stroke="{SLATE[0]}" stroke-width="1.3"/>')
    s.append(t(X0 + (gw - PADC) / 2, 26.5, 'Held fixed: one task and one shared resource', 'banner'))
    # axis titles
    s.append(t(X0 + (gw - PADC) / 2, 60, 'AGENT POPULATION', 'axis', extra=f' fill="{BLUE[1]}"'))
    s.append(t(10, Y0 - 16, 'INSTITUTION', 'axis', 'start', f' fill="{AMBER[1]}"'))
    for c, (name, sub) in enumerate(COLS):
        cx = X0 + c * CW + (CW - PADC) / 2
        s.append(t(cx, 84, name, 'colh', extra=f' fill="{BLUE[1]}"'))
        s.append(t(cx, 102, sub, 'sub'))
    for r, (name, sub) in enumerate(ROWS):
        cy = Y0 + r * CH + (CH - PADC) / 2
        s.append(t(10, cy - 2, name, 'rowh', 'start', f' fill="{AMBER[1]}"'))
        s.append(t(10, cy + 17, sub, 'sub', 'start'))
        for c in range(3):
            x, y = X0 + c * CW, Y0 + r * CH
            s.append(f'<rect x="{x}" y="{y}" width="{CW-PADC}" height="{CH-PADC}" rx="10" fill="#fff" stroke="{HAIR}" stroke-width="1.3"/>')
            # four unscored outcome slots
            sw, gap = 40, 10
            total = 4 * sw + 3 * gap
            sx = x + (CW - PADC - total) / 2
            for k, (letter, _) in enumerate(OUTCOMES):
                bx = sx + k * (sw + gap)
                s.append(f'<rect x="{bx:.1f}" y="{y+18}" width="{sw}" height="34" rx="6" fill="{PAGE}" stroke="{HAIR}" stroke-width="1.1" stroke-dasharray="3 3"/>')
                s.append(t(bx + sw / 2, y + 40.5, letter, 'slot'))
            s.append(t(x + (CW - PADC) / 2, y + 74, 'repeated rounds × seeds', 'cellnote'))
    # contrast 1: a row (vary population, fixed institution)
    ry = Y0 + FIXED_ROW * CH
    s.append(f'<rect x="{X0-7}" y="{ry-7}" width="{gw+2}" height="{CH+2}" rx="14" fill="none" stroke="{BLUE[0]}" stroke-width="3"/>')
    # contrast 2: a column (vary institution, fixed population)
    cx0 = X0 + FIXED_COL * CW
    s.append(f'<rect x="{cx0-7}" y="{Y0-7}" width="{CW+2}" height="{3*CH+2}" rx="14" fill="none" stroke="{AMBER[0]}" stroke-width="3" stroke-dasharray="9 5"/>')
    # notes below the grid
    ny = Y0 + 3 * CH + 26
    notes = [
        ('row', BLUE, ['Vary the population at a', 'fixed institution', '(what most benchmarks do)']),
        ('col', AMBER, ['Vary the institution at a', 'fixed population', '(a growing body of work)']),
        ('int', VIOLET, ['Interaction: does the', "institution's effect depend", 'on the population?']),
    ]
    nw = 280
    for i, (kind, col, lines) in enumerate(notes):
        x = 10 + i * (nw + 20)
        if kind == 'row':
            s.append(f'<line x1="{x}" y1="{ny+8}" x2="{x+40}" y2="{ny+8}" stroke="{col[0]}" stroke-width="3.2"/>')
        elif kind == 'col':
            s.append(f'<line x1="{x}" y1="{ny+8}" x2="{x+40}" y2="{ny+8}" stroke="{col[0]}" stroke-width="3.2" stroke-dasharray="9 5"/>')
        else:
            s.append(f'<rect x="{x}" y="{ny-4}" width="40" height="24" rx="12" fill="{col[2]}" stroke="{col[0]}" stroke-width="1.4"/>'
                     + t(x + 20, ny + 12.5, '×', 'intx', extra=f' fill="{col[1]}"'))
        for j, line in enumerate(lines):
            cls = 'note' if (j < 2 or kind == 'int') else 'notesub'
            s.append(t(x + 52, ny + 13 + j * 20, line, cls, 'start'))
    # outcome key
    ky = ny + 92
    s.append(t(10, ky, 'In every cell:', 'key', 'start'))
    kx = 118
    for letter, name in OUTCOMES:
        s.append(f'<rect x="{kx}" y="{ky-15}" width="22" height="20" rx="4" fill="{PAGE}" stroke="{HAIR}" stroke-width="1.1" stroke-dasharray="3 3"/>')
        s.append(t(kx + 11, ky, letter, 'slotk'))
        s.append(t(kx + 30, ky, name, 'key', 'start'))
        kx += 44 + 8.4 * len(name)
    s.append(t(10, ky + 24, 'Each outcome is reported with its uncertainty across runs. Cells stay empty until the study is run.', 'notesub', 'start'))
    return s, ky + 36

def main():
    s, H = build()
    css = f'''
  text{{font-family:"Helvetica Neue",Arial,sans-serif;}}
  .banner{{font-size:15px;font-weight:700;fill:{SLATE[1]};}}
  .axis{{font-size:16px;font-weight:900;letter-spacing:.05em;}}
  .colh,.rowh{{font-size:17px;font-weight:800;}}
  .sub{{font-size:14px;fill:{MUTED};font-style:italic;}}
  .slot{{font-size:15px;font-weight:800;fill:{MUTED};}}
  .slotk{{font-size:13px;font-weight:800;fill:{MUTED};}}
  .cellnote{{font-size:13.5px;fill:{MUTED};font-style:italic;}}
  .note{{font-size:15.5px;font-weight:700;fill:{INK};}}
  .notesub{{font-size:14px;fill:{MUTED};font-style:italic;}}
  .intx{{font-size:17px;font-weight:900;}}
  .key{{font-size:14px;fill:{INK};}}'''
    html = f'''<!DOCTYPE html>
<html lang="en"><head><meta charset="UTF-8"><title>Fig. 7 draft: contrast-first evaluation matrix</title>
<!-- Draft Fig. 7 generated by scripts/gen_fig7_matrix.py. -->
<style>{css}
  html,body{{margin:0;background:#fff;}} .fig{{width:{W}px;margin:0 auto;padding:12px;}}
</style></head><body><div class="fig">
<svg viewBox="0 0 {W} {H:.0f}" width="{W}" height="{H:.0f}" xmlns="http://www.w3.org/2000/svg">
{chr(10).join(s)}
</svg></div></body></html>'''
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    open(OUT, 'w', encoding='utf-8').write(html)
    print(f'wrote {os.path.relpath(OUT)} ({W}x{H:.0f}); smallest text 13px = {13 * 347 / W:.1f}pt at text width')

if __name__ == '__main__':
    main()
