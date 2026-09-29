#!/usr/bin/env python3
"""Generate figure3 (institutional design dimensions): three enforcement-stage cards
on top, seven evaluation properties in two rows (4+3) so every box holds >=6.5pt text
at \\textwidth. Amber = enforcement stages, violet = evaluation properties."""
FONT="'Helvetica Neue', Arial, sans-serif"
AM_D="#8A5A0B"; AM_BG="#FBEEDA"
VI_D="#463BA0"; VI_M="#6C5CD0"; VI_BG="#ECE9FB"; MUT="#6B7787"; INK="#3F4D5A"

STAGES=[("1","Observer","Who can see relevant behavior?",
         "peer agents, logs, monitoring systems, human auditors"),
        ("2","Arbiter","Who decides whether a violation occurred?",
         "rule-based checker, mediator agent, judge, voting system, human review"),
        ("3","Enforcer","Who applies the sanction to whom?",
         "peer agents, platform, tool orchestration layers, authority figures, smart contracts")]

PROPS=[("Timing","before or after harm?",["ex ante rate limits","vs.","ex post fines"]),
       ("Reversibility","can it be undone?",["warning","vs.","permanent exclusion"]),
       ("Adaptivity","does it escalate?",["graduated sanctions,","re-entry conditions"]),
       ("Observability","visible or hidden?",["tool logs","vs.","private reasoning"]),
       ("Gameability","can it be exploited?",["reputation farming,","surface compliance"]),
       ("Repair","does it restore?",["memory cleanup,","output correction"]),
       ("Scale","across many agents?",["local trust","vs.","platform-wide"])]

W=560; M=13;
# stage cards
SG=16; SCW=(W-2*M-2*SG)/3; SY=34; S_HEAD=24
# property boxes
PGAP=10; PBW=126; PBH=84
def wrap(t,n):
    words=t.split(); lines=[]; cur=""
    for w in words:
        if len(cur)+len(w)+1<=n: cur=(cur+" "+w).strip()
        else: lines.append(cur); cur=w
    if cur: lines.append(cur)
    return lines
def esc(s): return s.replace("&","&amp;")

def stage_card(x,badge,title,q,examples):
    o=[]; cx=x+SCW/2
    o.append(f'<rect x="{x:.1f}" y="{SY}" width="{SCW:.1f}" height="{SCH}" rx="8" fill="{AM_BG}" stroke="{AM_D}" stroke-width="0.6"/>')
    o.append(f'<rect x="{x:.1f}" y="{SY}" width="{SCW:.1f}" height="{S_HEAD}" rx="8" fill="{AM_D}"/>')
    o.append(f'<rect x="{x:.1f}" y="{SY+12}" width="{SCW:.1f}" height="12" fill="{AM_D}"/>')
    bcy=SY+12
    o.append(f'<circle cx="{x+16:.1f}" cy="{bcy}" r="8.5" fill="{AM_BG}"/>')
    o.append(f'<text x="{x+16:.1f}" y="{bcy+3.9:.1f}" text-anchor="middle" font-size="11" font-weight="700" fill="{AM_D}">{badge}</text>')
    o.append(f'<text x="{cx:.1f}" y="{SY+16}" text-anchor="middle" font-size="13.5" font-weight="700" fill="{AM_BG}">{title}</text>')
    dy=SY+40+2*14+4  # fixed (assume up to 2 question lines) so dividers/labels align across cards
    ql=wrap(q,26)
    qc=(SY+S_HEAD+dy)/2  # vertical center of the region between header and divider
    y0=qc-(len(ql)-1)*7+3.5
    for j,l in enumerate(ql):
        o.append(f'<text x="{cx:.1f}" y="{y0+j*14:.1f}" text-anchor="middle" font-size="11" font-style="italic" fill="{AM_D}">{esc(l)}</text>')
    o.append(f'<line x1="{x+10:.1f}" y1="{dy:.1f}" x2="{x+SCW-10:.1f}" y2="{dy:.1f}" stroke="{AM_D}" stroke-width="0.4" opacity="0.5"/>')
    o.append(f'<text x="{x+12:.1f}" y="{dy+16:.1f}" font-size="11" font-weight="700" fill="{AM_D}">In LLM agents</text>')
    for j,l in enumerate(wrap(examples,32)):
        o.append(f'<text x="{x+12:.1f}" y="{dy+31+j*13:.1f}" font-size="11" fill="{MUT}">{esc(l)}</text>')
    return "\n".join(o)

def prop_box(x,y,title,q,ex):
    o=[]; cx=x+PBW/2
    o.append(f'<rect x="{x:.1f}" y="{y}" width="{PBW}" height="{PBH}" rx="6" fill="#FFF" stroke="{VI_M}" stroke-width="0.6"/>')
    o.append(f'<rect x="{x:.1f}" y="{y}" width="{PBW}" height="22" rx="6" fill="{VI_BG}"/>')
    o.append(f'<rect x="{x:.1f}" y="{y+11}" width="{PBW}" height="11" fill="{VI_BG}"/>')
    o.append(f'<text x="{cx:.1f}" y="{y+15}" text-anchor="middle" font-size="12" font-weight="700" fill="{VI_D}">{title}</text>')
    o.append(f'<text x="{cx:.1f}" y="{y+35}" text-anchor="middle" font-size="10.5" font-style="italic" fill="{MUT}">{esc(q)}</text>')
    o.append(f'<line x1="{x+9:.1f}" y1="{y+43}" x2="{x+PBW-9:.1f}" y2="{y+43}" stroke="{VI_M}" stroke-width="0.3" opacity="0.5"/>')
    for j,l in enumerate(ex):
        o.append(f'<text x="{cx:.1f}" y="{y+57+j*12}" text-anchor="middle" font-size="11" fill="{MUT}">{esc(l)}</text>')
    return "\n".join(o)

# stage card height sized for Enforcer (longest): question 1 line + 3 example lines
SCH=142
H=0
def build():
    o=[f'<svg width="100%" viewBox="0 0 {W} {{H}}" role="img" xmlns="http://www.w3.org/2000/svg" font-family="{FONT}">']
    o.append('<title>Design dimensions for cooperation-shaping institutions</title>')
    # Panel A label
    o.append(f'<text x="{M}" y="22" font-size="13" font-weight="700" fill="#2C2C2A">A</text>')
    o.append(f'<text x="{M+14}" y="22" font-size="13" font-weight="700" fill="#2C2C2A">Enforcement stages</text>')
    for i,(b,t,q,ex) in enumerate(STAGES):
        x=M+i*(SCW+SG); o.append(stage_card(x,b,t,q,ex))
        # arrow between cards
        if i<2:
            ax=x+SCW+2; o.append(f'<path d="M {ax:.1f} {SY+SCH/2:.1f} L {ax+SG-4:.1f} {SY+SCH/2:.1f}" stroke="{AM_D}" stroke-width="1.4" marker-end="url(#ah3)"/>')
    # Panel B label
    blab=SY+SCH+22
    o.append(f'<text x="{M}" y="{blab}" font-size="13" font-weight="700" fill="#2C2C2A">B</text>')
    o.append(f'<text x="{M+14}" y="{blab}" font-size="13" font-weight="700" fill="#2C2C2A">Evaluation properties</text>')
    # property rows
    row1=PROPS[:4]; row2=PROPS[4:]
    ry1=SY+SCH+38
    x0=(W-(4*PBW+3*PGAP))/2
    for i,(t,q,ex) in enumerate(row1):
        o.append(prop_box(x0+i*(PBW+PGAP),ry1,t,q,ex))
    ry2=ry1+PBH+12
    x0b=(W-(3*PBW+2*PGAP))/2
    for i,(t,q,ex) in enumerate(row2):
        o.append(prop_box(x0b+i*(PBW+PGAP),ry2,t,q,ex))
    total_h=ry2+PBH+8
    o.append('</svg>')
    svg="\n".join(o).replace("{H}",str(int(total_h)))
    # inject arrow marker into defs
    defs=f'<defs><marker id="ah3" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="5" markerHeight="5" orient="auto-start-reverse"><path d="M2 1L8 5L2 9" fill="none" stroke="{AM_D}" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/></marker></defs>'
    svg=svg.replace("</title>","</title>\n"+defs)
    return svg

if __name__=="__main__":
    open("figs/figure3_institutional-design-dimensions.html","w").write(build())
    print("wrote figs/figure3_institutional-design-dimensions.html")
