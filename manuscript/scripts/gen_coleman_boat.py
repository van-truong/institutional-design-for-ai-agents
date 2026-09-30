#!/usr/bin/env python3
"""Draft figure: a Coleman boat for agent institutions (sketch, not yet in the paper).

Adapts Coleman's macro-micro-macro diagram, in the question-per-arrow form of Martinez-Pena & Ylikoski (2024),
to multi-agent AI: an institutional change (A) alters each agent's action situation through Ostrom's seven rule
types (B), the model responds (C), agents reshape each other's situations (feedback), and behavior adds up to group
outcomes (D). Endpoints can be human, artificial, or mixed, and the micro level rests on a technical substrate.
The three failure modes of Fig. 6 are pinned to the arrows where they break. Colors follow figs/PALETTE.md.
Run from manuscript/:  python3 scripts/gen_coleman_boat.py
"""
import os
from html import escape

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, '..', 'figs', 'drafts', 'figure_coleman-boat.html')

INK, MUTED, HAIR, PAGE = '#3F4D5A', '#6B7787', '#B3BEC9', '#FBFAF7'
AMBER = ('#C79A3A', '#8A5A0B', '#FBEEDA'); BLUE = ('#3A6EA5', '#2F3D6B', '#DCE8F5')
VIOLET = ('#6C5CD0', '#463BA0', '#ECE9FB'); GREEN = ('#4F9070', '#2F6B4A', '#E5F0E1')
TERRA = ('#C2662A', '#8F3F1E', '#FBEDE6'); SLATE = ('#6B7787', '#3F4D5A', '#EEF2F6')
W, H = 960, 664

def t(x, y, s, cls, anchor='middle', extra=''):
    return f'<text x="{x:.1f}" y="{y:.1f}" class="{cls}" text-anchor="{anchor}"{extra}>{escape(s)}</text>'

def box(x, y, w, h, col, title, lines, tag=None, tag_left=False):
    mid, dark, bg = col
    s = [f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="12" fill="{bg}" stroke="{mid}" stroke-width="1.6"/>',
         t(x + w / 2, y + 28, title, 'btitle', extra=f' fill="{dark}"')]
    for i, line in enumerate(lines):
        s.append(t(x + w / 2, y + 50 + i * 18, line, 'bsub'))
    if tag:
        tw = 16 + 7.2 * len(tag)
        tx = x + 10 if tag_left else x + w - tw - 10
        s.append(f'<rect x="{tx:.1f}" y="{y - 12}" width="{tw:.1f}" height="22" rx="11" fill="#fff" stroke="{mid}" stroke-width="1.1"/>')
        s.append(t(tx + tw / 2, y + 3.5, tag, 'tag', extra=f' fill="{dark}"'))
    return s

def failure(x, y, letter, text):
    w = 24 + 7.3 * len(text)
    return [f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="24" rx="12" fill="{TERRA[2]}" stroke="{TERRA[0]}" stroke-width="1.2"/>',
            t(x + 12, y + 16.5, letter, 'flet', extra=f' fill="{TERRA[1]}"'),
            t(x + 24, y + 16.5, text, 'ftext', 'start', f' fill="{TERRA[1]}"')]

def build():
    s = []
    # level bands
    s.append(f'<rect x="0" y="40" width="{W}" height="170" rx="14" fill="{PAGE}"/>')
    s.append(f'<rect x="0" y="330" width="{W}" height="304" rx="14" fill="{PAGE}"/>')
    s.append(t(16, 30, 'GROUP AND INSTITUTION (MACRO)', 'level', 'start'))
    s.append(t(16, 656, 'EACH AGENT (MICRO)', 'level', 'start'))
    # boxes
    AX, AY, BW, BH = 40, 74, 250, 110
    DX = W - 40 - BW
    BX, BY = 40, 360
    CX = W - 40 - BW
    s += box(AX, AY, BW, BH, AMBER, 'A. Institutional change', ['e.g. add graduated sanctions', 'or an appeal step'], 'human, agent, or mixed', tag_left=True)
    s += box(DX, AY, BW, BH, GREEN, 'D. Group outcomes', ['cooperation, enforcement cost,', 'false punishment, repair'], 'human, agent, or mixed')
    s += box(CX, BY, BW, 116, VIOLET, 'C. Agent behavior', ['what each model does', 'with its new options'])
    # B with Ostrom's seven rule types
    bh = 164
    s.append(f'<rect x="{BX}" y="{BY}" width="{BW + 40}" height="{bh}" rx="12" fill="{BLUE[2]}" stroke="{BLUE[0]}" stroke-width="1.6"/>')
    s.append(t(BX + (BW + 40) / 2, BY + 28, "B. Each agent's action situation", 'btitle', extra=f' fill="{BLUE[1]}"'))
    rules = ['boundary', 'position', 'choice', 'information', 'aggregation', 'payoff', 'scope']
    x, y = BX + 14, BY + 46
    for r in rules:
        w = 16 + 7.4 * len(r)
        if x + w > BX + BW + 30:
            x, y = BX + 14, y + 30
        s.append(f'<rect x="{x:.1f}" y="{y}" width="{w:.1f}" height="24" rx="12" fill="#fff" stroke="{BLUE[0]}" stroke-width="1.1"/>')
        s.append(t(x + w / 2, y + 16.5, r, 'rule', extra=f' fill="{BLUE[1]}"'))
        x += w + 6
    s.append(t(BX + (BW + 40) / 2, BY + bh - 12, "Ostrom's seven rule types", 'note'))
    # technical substrate under the micro level
    s.append(f'<rect x="40" y="{BY + bh + 78}" width="{W - 80}" height="26" rx="13" fill="{SLATE[2]}" stroke="{SLATE[0]}" stroke-width="1.1" stroke-dasharray="5 4"/>')
    s.append(t(W / 2, BY + bh + 95.5, 'technical substrate: shared memory, compute, tools, logs', 'sub', extra=f' fill="{SLATE[1]}"'))
    # arrows
    def arrow(d, dash=False, col=INK):
        da = ' stroke-dasharray="7 5"' if dash else ''
        mk = {INK: 'ah', MUTED: 'ahm', TERRA[0]: 'aht'}[col]
        return f'<path d="{d}" fill="none" stroke="{col}" stroke-width="2" marker-end="url(#{mk})"{da}/>'
    s.append(arrow(f'M{AX + BW + 6} {AY + 40} L{DX - 8} {AY + 40}', dash=True, col=MUTED))
    s.append(t(W / 2, AY + 30, 'what designers hope happens', 'note'))
    s.append(arrow(f'M{AX + 110} {AY + BH + 4} L{BX + 110} {BY - 8}'))                           # 1
    s.append(arrow(f'M{BX + BW + 46} {BY + 58} L{CX - 8} {BY + 58}'))                            # 2
    s.append(arrow(f'M{CX + 30} {BY + 120} C{CX - 20} {BY + 176} {BX + BW + 90} {BY + 176} {BX + BW + 46} {BY + 124}'))  # 3
    s.append(arrow(f'M{CX + 140} {BY - 4} L{DX + 140} {AY + BH + 8}'))                          # 4
    q = [(AX + 124, 262, '1. How does the rule change', "each agent's situation?", 'start'),
         ((BX + BW + CX) / 2 + 20, BY + 34, '2. How does', 'the model respond?', 'middle'),
         ((BX + BW + CX) / 2 + 20, BY + 190, '3. How do agents reshape each', "other's situations?", 'middle'),
         (DX + 128, 262, '4. How does behavior add up', 'to group outcomes?', 'end')]
    for x, y, l1, l2, anc in q:
        s.append(t(x, y, l1, 'q', anc)); s.append(t(x, y + 18, l2, 'q', anc))
    # failure modes pinned to where they break (Fig. 6)
    s += failure((BX + BW + CX) / 2 - 70, BY + 70, 'A', 'fine read as a price')
    s += failure(DX + 20, 300, 'B', 'score stops tracking conduct')
    s.append(arrow(f'M{DX + 30} {AY + 8} C{DX - 60} {AY - 40} {AX + BW + 60} {AY - 40} {AX + BW - 30} {AY + 4}', col=TERRA[0]))
    s += failure(W / 2 - 110, 2, 'C', 'the enforcer reshapes the rules')
    return s

def main():
    body = '\n'.join(build())
    css = f'''
  text{{font-family:"Helvetica Neue",Arial,sans-serif;}}
  .level{{font-size:13.5px;font-weight:800;letter-spacing:1.4px;fill:{MUTED};}}
  .btitle{{font-size:17px;font-weight:800;}}
  .bsub,.sub{{font-size:14.5px;fill:{INK};}}
  .tag{{font-size:12.5px;font-weight:700;font-style:italic;}}
  .rule{{font-size:13px;font-weight:700;}}
  .note{{font-size:13.5px;font-style:italic;fill:{MUTED};}}
  .q{{font-size:14.5px;font-weight:700;fill:{INK};}}
  .flet{{font-size:13px;font-weight:900;text-anchor:middle;}}
  .ftext{{font-size:13px;font-weight:700;font-style:italic;}}'''
    html = f'''<!DOCTYPE html>
<html lang="en"><head><meta charset="UTF-8"><title>Draft: a Coleman boat for agent institutions</title>
<!-- Draft generated by scripts/gen_coleman_boat.py; not yet in the paper. -->
<style>{css}
  html,body{{margin:0;background:#fff;}} .fig{{width:{W}px;margin:0 auto;padding:12px;}}
</style></head><body><div class="fig">
<svg viewBox="0 -4 {W} {H + 8}" width="{W}" height="{H + 8}" xmlns="http://www.w3.org/2000/svg">
<defs>{''.join(f'<marker id="{k}" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="{c}"/></marker>' for k, c in (('ah', INK), ('ahm', MUTED), ('aht', TERRA[0])))}</defs>
{body}
</svg></div></body></html>'''
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    open(OUT, 'w', encoding='utf-8').write(html)
    print('wrote', os.path.relpath(OUT))

if __name__ == '__main__':
    main()
