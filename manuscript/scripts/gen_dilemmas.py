#!/usr/bin/env python3
"""Generate figure2 (four cooperation dilemmas) on a shared grid: equal cards,
one type scale, aligned section labels, viewBox tuned so all text >=6pt at
~1.1x textwidth. Reuses the four hand-drawn icons verbatim."""
FONT = "'Helvetica Neue', Arial, sans-serif"

# icon inner drawings, centered at (0,0); reused verbatim from the original figure
ICONS = {
"extractive": """
<ellipse cx="0" cy="-1" rx="28" ry="4" fill="#FFF" stroke="#8F3F1E" stroke-width="0.7"/>
<rect x="-28" y="-1" width="56" height="22" fill="#FFF" stroke="none"/>
<rect x="-28" y="14" width="56" height="7" fill="#C2662A" stroke="none" opacity="0.7"/>
<line x1="-28" y1="-1" x2="-28" y2="21" stroke="#8F3F1E" stroke-width="0.7"/>
<line x1="28" y1="-1" x2="28" y2="21" stroke="#8F3F1E" stroke-width="0.7"/>
<ellipse cx="0" cy="21" rx="28" ry="4" fill="#C2662A" stroke="#8F3F1E" stroke-width="0.7" opacity="0.7"/>
<line x1="-22" y1="-24" x2="-22" y2="-6" stroke="#8F3F1E" stroke-width="1.2" stroke-linecap="round" marker-end="url(#ah-coral)"/>
<line x1="0" y1="-24" x2="0" y2="-6" stroke="#8F3F1E" stroke-width="1.2" stroke-linecap="round" marker-end="url(#ah-coral)"/>
<line x1="22" y1="-24" x2="22" y2="-6" stroke="#8F3F1E" stroke-width="1.2" stroke-linecap="round" marker-end="url(#ah-coral)"/>
<text x="0" y="-38" text-anchor="middle" font-size="17" fill="#8F3F1E" font-style="italic">depletion</text>""",
"contributive": """
<ellipse cx="0" cy="-1" rx="28" ry="4" fill="#FBEEDA" stroke="#8A5A0B" stroke-width="0.7"/>
<rect x="-28" y="-1" width="56" height="22" fill="#FBEEDA" stroke="none"/>
<rect x="-28" y="17" width="56" height="4" fill="#C79A3A" stroke="none" opacity="0.5"/>
<line x1="-18" y1="17" x2="-18" y2="5" stroke="#8A5A0B" stroke-width="1.2" stroke-linecap="round" marker-end="url(#ah-amber)"/>
<line x1="0" y1="17" x2="0" y2="5" stroke="#8A5A0B" stroke-width="1.2" stroke-linecap="round" marker-end="url(#ah-amber)"/>
<line x1="18" y1="17" x2="18" y2="5" stroke="#8A5A0B" stroke-width="1.2" stroke-linecap="round" marker-end="url(#ah-amber)"/>
<line x1="-28" y1="-1" x2="-28" y2="21" stroke="#8A5A0B" stroke-width="0.7"/>
<line x1="28" y1="-1" x2="28" y2="21" stroke="#8A5A0B" stroke-width="0.7"/>
<ellipse cx="0" cy="21" rx="28" ry="4" fill="#C79A3A" stroke="#8A5A0B" stroke-width="0.7" opacity="0.6"/>
<g stroke="#8A5A0B" stroke-width="0.9" fill="none" stroke-linecap="round">
<line x1="-30" y1="-19" x2="-22" y2="-11"/><line x1="-22" y1="-19" x2="-30" y2="-11"/></g>
<g stroke="#8A5A0B" stroke-width="0.9" fill="none" stroke-linecap="round">
<line x1="-4" y1="-19" x2="4" y2="-11"/><line x1="4" y1="-19" x2="-4" y2="-11"/></g>
<g stroke="#8A5A0B" stroke-width="0.9" fill="none" stroke-linecap="round">
<line x1="22" y1="-19" x2="30" y2="-11"/><line x1="30" y1="-19" x2="22" y2="-11"/></g>
<text x="0" y="-38" text-anchor="middle" font-size="17" fill="#8A5A0B" font-style="italic">no upkeep</text>""",
"second-order": """
<path d="M -28 0 Q 0 -18 28 0 Q 0 18 -28 0 Z" fill="#FFF" stroke="#6C5CD0" stroke-width="0.9"/>
<circle cx="0" cy="0" r="7" fill="#6C5CD0"/>
<circle cx="2" cy="-2" r="2" fill="#FFF"/>
<text x="-40" y="-8" font-size="20" font-weight="500" fill="#6C5CD0">?</text>
<text x="28" y="-8" font-size="20" font-weight="500" fill="#6C5CD0">?</text>
<text x="-40" y="30" font-size="20" font-weight="500" fill="#6C5CD0">?</text>
<text x="28" y="30" font-size="20" font-weight="500" fill="#6C5CD0">?</text>
<text x="0" y="-40" text-anchor="middle" font-size="17" fill="#6C5CD0" font-style="italic">who watches whom?</text>""",
"repair": """
<path d="M -28 -10 Q -28 -18 -20 -18 L -2 -18 L -8 -2 L -22 -2 Q -28 -2 -28 -10 Z" fill="#FFF" stroke="#04342C" stroke-width="0.9"/>
<path d="M 28 14 Q 28 22 20 22 L 4 22 L 10 6 L 24 6 Q 28 6 28 14 Z" fill="#FFF" stroke="#04342C" stroke-width="0.9"/>
<line x1="-2" y1="-18" x2="10" y2="6" stroke="#04342C" stroke-width="0.7" stroke-dasharray="2 2"/>
<line x1="-8" y1="-2" x2="4" y2="22" stroke="#04342C" stroke-width="0.7" stroke-dasharray="2 2"/>
<rect x="-12" y="-2" width="24" height="10" rx="2" fill="#9FD9C7" stroke="#04342C" stroke-width="0.8" transform="rotate(28 0 3)"/>
<line x1="-7" y1="6" x2="7" y2="-1" stroke="#04342C" stroke-width="0.5" stroke-dasharray="1.5 1.5"/>
<text x="0" y="-38" text-anchor="middle" font-size="17" fill="#04342C" font-style="italic">restoration</text>""",
}

# per card: title, dark(text+border+header), bg, statement lines, human ex, llm ex
CARDS = [
 ("extractive","Extractive dilemma","#8F3F1E","#FBEDE6",
   ["Overuse of a shared","resource depletes it."],
   ["overfishing, overgrazing"],
   ["API budgets, shared compute,","tool calls, context windows"]),
 ("contributive","Contributive dilemma","#8A5A0B","#FBEEDA",
   ["Beneficiaries fail to","maintain community goods."],
   ["open-source upkeep,","unpaid moderation"],
   ["helping at a personal cost,","cleanup, verifying, volunteering"]),
 ("second-order","Second-order dilemma","#463BA0","#ECE9FB",
   ["Monitoring is itself","costly to provide."],
   ["peer monitoring, costly","security, punishment"],
   ["auditing, sanctioning agents,","setting new norms"]),
 ("repair","Repair dilemma","#04342C","#E3F1EC",
   ["Who bears the cost","of fixing harm?"],
   ["restitution, policy reform,","disaster recovery"],
   ["cleaning corrupted memory,","retractions, undoing changes,","restoring what was lost"]),
]
HEADERFILL = {"extractive":"#8F3F1E","contributive":"#8A5A0B","second-order":"#6C5CD0","repair":"#04342C"}

# geometry (viewBox units) tuned so example text (20) -> ~6.1pt at 1.12*textwidth
MARGIN=18; GAP=18; NCARD=4
CARD_W=297; W=MARGIN*2+NCARD*CARD_W+(NCARD-1)*GAP
TOP=20; HEADER_H=52; CARD_H=442; H=TOP+CARD_H+18
PAD=20
# shared y grid (absolute)
Y_HEADER=TOP+34
Y_ICON=TOP+120
Y_STmt=TOP+192
Y_DIV=TOP+238
Y_HUM=TOP+266; Y_HUM_EX=TOP+290
Y_LLM=TOP+352; Y_LLM_EX=TOP+376
LINE=23

def esc(s): return s.replace("&","&amp;")

def build():
    o=[f'<svg width="100%" viewBox="0 0 {W} {H}" role="img" xmlns="http://www.w3.org/2000/svg" font-family="{FONT}">']
    o.append('<title>Four cooperation dilemmas in human and LLM-agent systems</title>')
    o.append('<defs>')
    for cid,st in [("coral","#8F3F1E"),("amber","#8A5A0B"),("purple","#6C5CD0"),("teal","#04342C")]:
        o.append(f'<marker id="ah-{cid}" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="5" markerHeight="5" orient="auto-start-reverse"><path d="M2 1L8 5L2 9" fill="none" stroke="{st}" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></marker>')
    o.append('</defs>')
    for i,(key,title,dark,bg,stmt,hum,llm) in enumerate(CARDS):
        x=MARGIN+i*(CARD_W+GAP); cx=x+CARD_W/2; hf=HEADERFILL[key]
        # card + header
        o.append(f'<rect x="{x}" y="{TOP}" width="{CARD_W}" height="{CARD_H}" rx="16" fill="{bg}" stroke="{hf}" stroke-width="1"/>')
        o.append(f'<rect x="{x}" y="{TOP}" width="{CARD_W}" height="{HEADER_H}" rx="16" fill="{hf}"/>')
        o.append(f'<rect x="{x}" y="{TOP+28}" width="{CARD_W}" height="24" fill="{hf}"/>')
        o.append(f'<text x="{cx:.1f}" y="{Y_HEADER}" text-anchor="middle" font-size="22" font-weight="600" fill="{bg}">{title}</text>')
        # icon
        o.append(f'<g transform="translate({cx:.1f},{Y_ICON})">{ICONS[key]}</g>')
        # statement
        for j,ln in enumerate(stmt):
            o.append(f'<text x="{cx:.1f}" y="{Y_STmt+j*26}" text-anchor="middle" font-size="22" fill="{dark}">{esc(ln)}</text>')
        # divider
        o.append(f'<line x1="{x+PAD}" y1="{Y_DIV}" x2="{x+CARD_W-PAD}" y2="{Y_DIV}" stroke="{hf}" stroke-width="0.8" opacity="0.5"/>')
        # in humans
        o.append(f'<text x="{x+PAD}" y="{Y_HUM}" font-size="20" font-weight="600" fill="{dark}">In humans</text>')
        for j,ln in enumerate(hum):
            o.append(f'<text x="{x+PAD}" y="{Y_HUM_EX+j*LINE}" font-size="20" fill="#6B7787">{esc(ln)}</text>')
        # in llm agents
        o.append(f'<text x="{x+PAD}" y="{Y_LLM}" font-size="20" font-weight="600" fill="{dark}">In LLM agents</text>')
        for j,ln in enumerate(llm):
            o.append(f'<text x="{x+PAD}" y="{Y_LLM_EX+j*LINE}" font-size="20" fill="#6B7787">{esc(ln)}</text>')
    o.append('</svg>')
    return "\n".join(o)

if __name__=="__main__":
    open("figs/figure2_four-cooperation-dilemmas.html","w").write(build())
    print("wrote figs/figure2_four-cooperation-dilemmas.html")
