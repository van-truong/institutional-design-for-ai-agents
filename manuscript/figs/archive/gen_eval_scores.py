#!/usr/bin/env python3
"""Generate figure6: the model-in-institution evaluation design.
A models x institutions matrix; each cell = repeated runs scored on a metric.
Two sweeps: vary model (fix institution) and vary institution (fix model)."""
FONT="'Helvetica Neue', Arial, sans-serif"
INK="#3F4D5A"; MUT="#6B7787"; HAIR="#B3BEC9"
TERRA="#C2662A"; AMBER="#C79A3A"; GREEN="#4F9070"; GREEN_D="#2F6B4A"
AMBER_D="#8A5A0B"; VIOLET="#6C5CD0"; VIOLET_D="#463BA0"; VIOLET_BG="#ECE9FB"

MODELS=["Model A","Model B","Model C","Model D"]
INSTS=["No institution","Monitoring +\nsanctions","Graduated +\nrepair"]
# illustrative cooperation scores per (institution row, model col)
VALS=[[0.24,0.31,0.19,0.27],
      [0.54,0.63,0.46,0.58],
      [0.83,0.77,0.69,0.86]]
METRICS=["cooperation rate","enforcement cost","false-punishment","inequality of burden","repair success"]

def barcolor(v): return TERRA if v<0.4 else (AMBER if v<0.7 else GREEN)

GX=196; GY=104; CW=122; RH=70; cw=104; ch=48
W=GX+len(MODELS)*CW+16
H=GY+len(INSTS)*RH+96

def esc(s): return s.replace("&","&amp;")

def build():
    o=[f'<svg width="100%" viewBox="0 0 {W} {H}" role="img" xmlns="http://www.w3.org/2000/svg" font-family="{FONT}">']
    o.append('<title>The model-in-institution evaluation design</title>')
    o.append(f'<defs><marker id="ev" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M2 1L8 5L2 9" fill="none" stroke="{INK}" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></marker></defs>')
    o.append(f'<text x="{W/2:.0f}" y="26" text-anchor="middle" font-size="16" font-weight="700" fill="{MUT}" letter-spacing="1.2">EVALUATING THE MODEL-IN-INSTITUTION</text>')
    # top sweep arrow (vary model)
    o.append(f'<line x1="{GX+6}" y1="62" x2="{GX+len(MODELS)*CW-16}" y2="62" stroke="{INK}" stroke-width="1.6" marker-end="url(#ev)"/>')
    o.append(f'<text x="{GX+ (len(MODELS)*CW)/2:.0f}" y="54" text-anchor="middle" font-size="14.5" font-weight="700" fill="{INK}">vary model &#8594; does the institution transfer?</text>')
    # left sweep arrow (vary institution)
    o.append(f'<line x1="34" y1="{GY+6}" x2="34" y2="{GY+len(INSTS)*RH-14}" stroke="{INK}" stroke-width="1.6" marker-end="url(#ev)"/>')
    o.append(f'<text x="26" y="{GY+len(INSTS)*RH/2:.0f}" text-anchor="middle" font-size="14.5" font-weight="700" fill="{INK}" transform="rotate(-90 26 {GY+len(INSTS)*RH/2:.0f})">vary institution &#8594; which sustains cooperation?</text>')
    # model headers
    for j,m in enumerate(MODELS):
        cx=GX+j*CW+CW/2
        o.append(f'<text x="{cx:.0f}" y="{GY-14}" text-anchor="middle" font-size="15" font-weight="700" fill="{AMBER_D}">{m}</text>')
    # rows
    for i,inst in enumerate(INSTS):
        ry=GY+i*RH
        # row label (violet), possibly 2 lines
        lines=inst.split("\n")
        ly=ry+RH/2 - (len(lines)-1)*8
        for k,l in enumerate(lines):
            o.append(f'<text x="{GX-14}" y="{ly+k*16:.0f}" text-anchor="end" font-size="14" font-weight="700" fill="{VIOLET_D}">{esc(l)}</text>')
        for j,m in enumerate(MODELS):
            cx=GX+j*CW; v=VALS[i][j]; col=barcolor(v)
            x=cx+(CW-cw)/2; y=ry+(RH-ch)/2
            o.append(f'<rect x="{x:.0f}" y="{y:.0f}" width="{cw}" height="{ch}" rx="7" fill="#F7F9FB" stroke="{HAIR}" stroke-width="0.8"/>')
            # metric bar
            bx=x+12; bw=cw-46; by=y+ch/2
            o.append(f'<rect x="{bx:.0f}" y="{by-5:.0f}" width="{bw}" height="10" rx="5" fill="#E7EAEE"/>')
            o.append(f'<rect x="{bx:.0f}" y="{by-5:.0f}" width="{bw*v:.0f}" height="10" rx="5" fill="{col}"/>')
            o.append(f'<text x="{x+cw-8:.0f}" y="{by:.0f}" text-anchor="end" dominant-baseline="central" font-size="13" font-weight="700" fill="{col}">{int(v*100)}</text>')
    # legend
    ly=GY+len(INSTS)*RH+30
    o.append(f'<text x="{GX-14}" y="{ly}" text-anchor="end" font-size="13.5" font-weight="700" fill="{INK}">Each cell:</text>')
    o.append(f'<text x="{GX}" y="{ly}" font-size="13.5" fill="{MUT}">repeated multi-agent runs, scored on</text>')
    cx=GX
    o.append(f'<text x="40" y="{ly+22}" font-size="13" fill="{MUT}">'+" · ".join(METRICS)+'</text>')
    # color key
    ky=ly+2
    kx=W-14
    for lab,c in [("sustained",GREEN),("partial",AMBER),("fails",TERRA)]:
        w=len(lab)*7.4+22
        kx-=w+6
        o.append(f'<rect x="{kx:.0f}" y="{ky-11}" width="14" height="10" rx="3" fill="{c}"/>')
        o.append(f'<text x="{kx+18:.0f}" y="{ky-6}" font-size="12.5" fill="{MUT}">{lab}</text>')
    o.append('</svg>')
    return "\n".join(o)

if __name__=="__main__":
    open("figs/figure6_model-in-institution-eval.html","w").write(build())
    print("wrote figs/figure6_model-in-institution-eval.html")
