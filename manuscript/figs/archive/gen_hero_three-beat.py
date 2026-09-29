#!/usr/bin/env python3
"""Generate figure1 as a 3-beat conceptual hero:
  aligned agent  ->  agents sharing a commons fail  ->  institution sustains cooperation
plus a position banner. Single SVG, master palette, all text >=6pt at ~textwidth."""
FONT="'Helvetica Neue', Arial, sans-serif"
INK="#3F4D5A"; MUT="#6B7787"; HAIR="#B3BEC9"
BLUE="#3A6EA5"; BLUE_BG="#DCE8F5"
GREEN="#4F9070"; GREEN_D="#2F6B4A"; GREEN_BG="#E5F0E1"
TERRA="#C2662A"; TERRA_D="#8F3F1E"; TERRA_BG="#FBEDE6"
AMBER="#C79A3A"; AMBER_D="#8A5A0B"; AMBER_BG="#FBEEDA"
VIOLET="#6C5CD0"; VIOLET_BG="#ECE9FB"; NEUT_BG="#F2F5F8"

W=850; PY=58; PH=250; PW=248; PX=[12,300,588]
CY=PY+120  # vertical center of scene area

def agent(cx,cy,color,bg="#FFFFFF"):
    return (f'<g><rect x="{cx-13:.1f}" y="{cy-9:.1f}" width="26" height="26" rx="6" '
            f'fill="{bg}" stroke="{color}" stroke-width="1.6"/>'
            f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="4.3" fill="{color}"/>'
            f'<line x1="{cx-6:.1f}" y1="{cy+9:.1f}" x2="{cx+6:.1f}" y2="{cy+9:.1f}" '
            f'stroke="{color}" stroke-width="1.6" stroke-linecap="round"/></g>')

def check(cx,cy):
    return (f'<g><circle cx="{cx:.1f}" cy="{cy:.1f}" r="11" fill="{GREEN}"/>'
            f'<path d="M {cx-5:.1f} {cy:.1f} L {cx-1.5:.1f} {cy+4:.1f} L {cx+5.5:.1f} {cy-4:.1f}" '
            f'fill="none" stroke="#FFF" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/></g>')

def cross(cx,cy):
    return (f'<g><circle cx="{cx:.1f}" cy="{cy:.1f}" r="11" fill="{TERRA}"/>'
            f'<path d="M {cx-4.5:.1f} {cy-4.5:.1f} L {cx+4.5:.1f} {cy+4.5:.1f} '
            f'M {cx+4.5:.1f} {cy-4.5:.1f} L {cx-4.5:.1f} {cy+4.5:.1f}" '
            f'stroke="#FFF" stroke-width="2.2" stroke-linecap="round"/></g>')

def pill(cx,cy,text,color,bg):
    w=len(text)*8.6+20
    return (f'<g><rect x="{cx-w/2:.1f}" y="{cy-9:.1f}" width="{w:.1f}" height="18" rx="9" '
            f'fill="{bg}" stroke="{color}" stroke-width="0.8"/>'
            f'<text x="{cx:.1f}" y="{cy:.1f}" text-anchor="middle" dominant-baseline="central" '
            f'font-size="15" fill="{color}">{text}</text></g>')

def panel(x,bg,stroke):
    return (f'<rect x="{x}" y="{PY}" width="{PW}" height="{PH}" rx="14" '
            f'fill="{bg}" stroke="{stroke}" stroke-width="1"/>')

def header(x,txt,color):
    # panel headings styled to match the other figures' headings (near-black, sentence case)
    return (f'<text x="{x+PW/2:.1f}" y="{PY+26}" text-anchor="middle" font-size="20" '
            f'font-weight="700" fill="#2C2C2A">{txt}</text>')

def caption(x,lines,color):
    o=[]
    for i,l in enumerate(lines):
        o.append(f'<text x="{x+PW/2:.1f}" y="{PY+PH-30+i*16:.1f}" text-anchor="middle" '
                 f'font-size="16" fill="{color}">{l}</text>')
    return "".join(o)

def arrow(x):
    y=PY+PH/2
    return (f'<path d="M {x:.1f} {y:.1f} L {x+22:.1f} {y:.1f}" stroke="{INK}" '
            f'stroke-width="2.4" marker-end="url(#heroarrow)"/>')

def build():
    o=[f'<svg width="100%" viewBox="0 0 {W} 440" role="img" xmlns="http://www.w3.org/2000/svg" font-family="{FONT}">']
    o.append('<title>From aligned models to governed agent societies</title>')
    o.append(f'<defs><marker id="heroarrow" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M2 1L8 5L2 9" fill="none" stroke="{INK}" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/></marker></defs>')
    o.append(f'<text x="{W/2:.1f}" y="30" text-anchor="middle" font-size="16" font-weight="700" fill="{MUT}" letter-spacing="1.4">FROM ALIGNED MODELS TO GOVERNED AGENT SOCIETIES</text>')

    # --- Beat 1: aligned in isolation ---
    x=PX[0]; cx=x+PW/2
    o.append(panel(x,NEUT_BG,HAIR)); o.append(header(x,"Aligned in isolation",INK))
    o.append(agent(cx,CY,BLUE,"#FFFFFF"))
    o.append(check(cx+22,CY-14))
    o.append(caption(x,["An individually aligned","agent avoids harm — alone."],MUT))

    # --- Beat 2: sharing a commons fails ---
    x=PX[1]; cx=x+PW/2
    o.append(panel(x,TERRA_BG,TERRA)); o.append(header(x,"Sharing a commons",TERRA_D))
    # shared resource (depleting pool) in center
    o.append(f'<ellipse cx="{cx:.1f}" cy="{CY+8:.1f}" rx="34" ry="7" fill="#FFF" stroke="{TERRA_D}" stroke-width="0.8"/>')
    o.append(f'<rect x="{cx-34:.1f}" y="{CY+8:.1f}" width="68" height="20" fill="#FFF" stroke="none"/>')
    o.append(f'<rect x="{cx-34:.1f}" y="{CY+22:.1f}" width="68" height="6" fill="{TERRA}" opacity="0.7"/>')
    o.append(f'<line x1="{cx-34:.1f}" y1="{CY+8:.1f}" x2="{cx-34:.1f}" y2="{CY+28:.1f}" stroke="{TERRA_D}" stroke-width="0.8"/>')
    o.append(f'<line x1="{cx+34:.1f}" y1="{CY+8:.1f}" x2="{cx+34:.1f}" y2="{CY+28:.1f}" stroke="{TERRA_D}" stroke-width="0.8"/>')
    o.append(f'<ellipse cx="{cx:.1f}" cy="{CY+28:.1f}" rx="34" ry="7" fill="{TERRA}" stroke="{TERRA_D}" stroke-width="0.8" opacity="0.7"/>')
    # three agents around, pulling (depletion arrows down into pool)
    for ax in (cx-52,cx,cx+52):
        o.append(agent(ax,CY-42,BLUE,"#FFFFFF"))
        o.append(f'<line x1="{ax:.1f}" y1="{CY-24:.1f}" x2="{ax:.1f}" y2="{CY:.1f}" stroke="{TERRA_D}" stroke-width="1.4" marker-end="url(#heroarrow)"/>')
    o.append(cross(cx+70,CY-46))
    o.append(caption(x,["...but collectively unsafe:","depletion, gaming, cascades."],TERRA_D))

    # --- Beat 3: institution sustains cooperation ---
    x=PX[2]; cx=x+PW/2
    o.append(panel(x,GREEN_BG,GREEN)); o.append(header(x,"Wrapped in an institution",GREEN_D))
    # institution frame (amber dashed) enclosing agents
    o.append(f'<rect x="{cx-70:.1f}" y="{CY-46:.1f}" width="140" height="58" rx="10" fill="{AMBER_BG}" stroke="{AMBER_D}" stroke-width="1.2" stroke-dasharray="5 3"/>')
    for ax in (cx-44,cx,cx+44):
        o.append(agent(ax,CY-24,BLUE,"#FFFFFF"))
    # mechanism pills below
    o.append(pill(cx-56,CY+34,"norms",VIOLET,VIOLET_BG))
    o.append(pill(cx+34,CY+34,"monitoring",VIOLET,VIOLET_BG))
    o.append(pill(cx-46,CY+58,"sanctions",VIOLET,VIOLET_BG))
    o.append(pill(cx+44,CY+58,"repair",VIOLET,VIOLET_BG))
    o.append(check(cx+78,CY-50))
    o.append(caption(x,["Institutions sustain","cooperation."],GREEN_D))

    # arrows between panels
    o.append(arrow(PX[0]+PW+2)); o.append(arrow(PX[1]+PW+2))

    # --- position banner ---
    by=PY+PH+18
    o.append(f'<rect x="12" y="{by}" width="{W-24}" height="86" rx="14" fill="{GREEN_BG}" stroke="{GREEN}" stroke-width="1.2"/>')
    o.append(f'<text x="34" y="{by+26}" font-size="13" font-weight="700" fill="{GREEN_D}" letter-spacing="1.5">POSITION</text>')
    lines=["Multi-agent AI safety needs institutional design. Even individually aligned agents can",
           "produce collectively unsafe outcomes when sharing finite resources, so we should evaluate",
           "the model-in-institution, not the model alone."]
    for i,l in enumerate(lines):
        o.append(f'<text x="140" y="{by+24+i*20:.0f}" font-size="16" fill="{INK}">{l}</text>')
    o.append('</svg>')
    return "\n".join(o)

if __name__=="__main__":
    open("figs/figure1_position-summary.html","w").write(build())
    print("wrote figs/figure1_position-summary.html")
