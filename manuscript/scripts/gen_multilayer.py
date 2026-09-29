#!/usr/bin/env python3
"""figure4 (multi-layer institutions), compact + spread so all text >=6pt at ~textwidth.
Panel A: three spread isometric layers (agent-in-context). Panel B: institution -> mechanism
tree with wrapped labels. Master palette; small A/B letters + subheadings."""
FONT="'Helvetica Neue', Arial, sans-serif"
INK="#3F4D5A"; MUT="#6B7787"; HAIR="#B3BEC9"; BLK="#2C2C2A"
AM_D="#8A5A0B"; AM_M="#C79A3A"; AM_TOP="#F3E4C4"; AM_SIDE="#E3C88C"; AM_BG="#FBEEDA"
BL_D="#2F3D6B"; BL_TOP="#DCE8F5"; BL_SIDE="#A9C4E0"
VI_D="#463BA0"; VI_M="#6C5CD0"; VI_TOP="#ECE9FB"; VI_SIDE="#C4BCEC"; VI_BG="#ECE9FB"

W=720

def esc(s): return s.replace("&","&amp;")
def wrap(t,n):
    words=t.split(); lines=[]; cur=""
    for w in words:
        if len(cur)+len(w)+1<=n: cur=(cur+" "+w).strip()
        else: lines.append(cur); cur=w
    if cur: lines.append(cur)
    return lines

def diamond(cx,cy,w,h,th,top,side,label,lcolor,nodes):
    o=[]
    o.append(f'<polygon points="{cx-w:.0f},{cy:.0f} {cx:.0f},{cy+h:.0f} {cx:.0f},{cy+h+th:.0f} {cx-w:.0f},{cy+th:.0f}" fill="{side}" stroke="{side}" stroke-width="0.5"/>')
    o.append(f'<polygon points="{cx:.0f},{cy+h:.0f} {cx+w:.0f},{cy:.0f} {cx+w:.0f},{cy+th:.0f} {cx:.0f},{cy+h+th:.0f}" fill="{side}" stroke="{side}" stroke-width="0.5" opacity="0.85"/>')
    o.append(f'<polygon points="{cx:.0f},{cy-h:.0f} {cx+w:.0f},{cy:.0f} {cx:.0f},{cy+h:.0f} {cx-w:.0f},{cy:.0f}" fill="{top}" stroke="{HAIR}" stroke-width="1"/>')
    o.append(nodes(cx,cy))
    for i,l in enumerate(label):
        style='font-weight="400" font-style="italic"' if l.strip().startswith("(") else 'font-weight="700"'
        o.append(f'<text x="{cx:.0f}" y="{cy-h-34+i*15:.0f}" text-anchor="middle" font-size="15.5" {style} fill="{lcolor}">{esc(l)}</text>')
    return "".join(o)

def nodes_net(cx,cy):
    pts=[(cx+16,cy-6),(cx+9,cy+2),(cx-8,cy+4),(cx-16,cy-3),(cx-4,cy-8),(cx+6,cy-9)]
    o="".join(f'<line x1="{pts[i][0]}" y1="{pts[i][1]}" x2="{pts[(i+1)%len(pts)][0]}" y2="{pts[(i+1)%len(pts)][1]}" stroke="{AM_M}" stroke-width="1" opacity="0.5"/>' for i in range(len(pts)))
    o+="".join(f'<circle cx="{x}" cy="{y}" r="2.6" fill="{AM_M}"/>' for x,y in pts)
    return o
def nodes_tri(cx,cy):
    pts=[(cx-14,cy+3),(cx+14,cy+2),(cx,cy-8)]
    o="".join(f'<line x1="{pts[i][0]}" y1="{pts[i][1]}" x2="{pts[(i+1)%3][0]}" y2="{pts[(i+1)%3][1]}" stroke="{MUT}" stroke-width="1.1" opacity="0.55"/>' for i in range(3))
    o+="".join(f'<circle cx="{x}" cy="{y}" r="3.6" fill="{MUT}"/>' for x,y in pts)
    return o
def nodes_one(cx,cy):
    return (f'<circle cx="{cx}" cy="{cy}" r="5" fill="{VI_M}"/>'
            f'<circle cx="{cx}" cy="{cy}" r="9.5" fill="none" stroke="{VI_M}" stroke-width="1.1" opacity="0.5"/>')

def varrow(ax,ytail,yhead,color):
    """Clean single-polygon vertical arrow from tail to head (up or down)."""
    sw=5.0; hw=16.0; hh=18.0
    se = yhead-hh if yhead>ytail else yhead+hh
    pts=[(ax-sw/2,ytail),(ax+sw/2,ytail),(ax+sw/2,se),(ax+hw/2,se),(ax,yhead),(ax-hw/2,se),(ax-sw/2,se)]
    p=" ".join(f"{x:.1f},{y:.1f}" for x,y in pts)
    return f'<polygon points="{p}" fill="{color}" opacity="0.9"/>'

# Panel B tree: (group, dark, bg, mid, [(name, sublabel|None)])
MECH=[("Information layer",AM_D,AM_BG,AM_M,[("Norms & protocols",None),("Monitoring",None),("Reputation",None)]),
      ("Consequence layer",AM_D,AM_BG,AM_M,[("Sanctions",None),("Constraints",None),("Adjudication & appeal",None),("Repair & reintegration",None)])]
CHAN=[("Soft channels",VI_D,VI_BG,VI_M,[("Normative","beliefs"),("Social","relationships"),("Epistemic","information")]),
      ("Hard channels",VI_D,VI_BG,VI_M,[("Incentive","payoffs"),("Constraint","access"),("Restorative","repair")])]

# Panel B geometry
RX=286; GX=428; GW=100; LX=556; LW=112; RIGHTX=696
LEAF_H=31; PITCH=40; GROUP_GAP=6; SEC_GAP=24; Y0=76
LEAF_WRAP=13; GROUP_WRAP=14

def leaf_box(o,ly,name,sub,dcol,bg,mcol):
    cx=LX+LW/2
    o.append(f'<rect x="{LX}" y="{ly-LEAF_H/2:.0f}" width="{LW}" height="{LEAF_H}" rx="8" fill="{bg}" stroke="{mcol}" stroke-width="0.9"/>')
    if sub:
        o.append(f'<text x="{cx:.0f}" y="{ly-3:.0f}" text-anchor="middle" font-size="13" font-weight="700" fill="{dcol}">{esc(name)}</text>')
        o.append(f'<text x="{cx:.0f}" y="{ly+10:.0f}" text-anchor="middle" font-size="12.5" font-style="italic" fill="{MUT}">{esc(sub)}</text>')
    else:
        ln=wrap(name,LEAF_WRAP)
        if len(ln)==1:
            o.append(f'<text x="{cx:.0f}" y="{ly:.0f}" text-anchor="middle" dominant-baseline="central" font-size="13" font-weight="700" fill="{dcol}">{esc(name)}</text>')
        else:
            o.append(f'<text x="{cx:.0f}" y="{ly-3:.0f}" text-anchor="middle" font-size="13" font-weight="700" fill="{dcol}">{esc(ln[0])}</text>')
            o.append(f'<text x="{cx:.0f}" y="{ly+12:.0f}" text-anchor="middle" font-size="13" font-weight="700" fill="{dcol}">{esc(ln[1])}</text>')

def build():
    o=[]
    # first lay out Panel B to know total height
    body=[]
    y=Y0; groups=[]; seclabels=[]
    for sname,scol,grp in [("INSTITUTIONAL FUNCTIONS",AM_M,MECH),("MECHANISM FAMILIES",VI_M,CHAN)]:
        first_ly=y; last_ly=y
        for (gname,dcol,bg,mcol,leaves) in grp:
            lys=[y+i*PITCH for i in range(len(leaves))]
            groups.append((gname,dcol,bg,mcol,leaves,lys))
            last_ly=lys[-1]
            y=lys[-1]+PITCH+GROUP_GAP
        seclabels.append((sname,scol,(first_ly+last_ly)/2))  # vertical center of the block
        y+=SEC_GAP
    Bbottom=y
    H=max(Bbottom+18, 300)

    out=[f'<svg width="100%" viewBox="0 0 {W} {H:.0f}" role="img" xmlns="http://www.w3.org/2000/svg" font-family="{FONT}">']
    out.append('<title>Agent-in-context and the design space of agent institutions</title>')
    out.append(f'<defs><marker id="triA" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M1,1 L9,5 L1,9 z" fill="{AM_M}"/></marker>'
               f'<marker id="triV" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M1,1 L9,5 L1,9 z" fill="{VI_M}"/></marker></defs>')
    # divider + labels
    out.append(f'<line x1="248" y1="18" x2="248" y2="{H-14:.0f}" stroke="#EEF2F6" stroke-width="1.4"/>')
    out.append(f'<text x="12" y="28" font-size="17" font-weight="700" fill="{BLK}">A</text>')
    out.append(f'<text x="28" y="28" font-size="17" font-weight="700" fill="{BLK}">Agent-in-context</text>')
    out.append(f'<text x="272" y="28" font-size="17" font-weight="700" fill="{BLK}">B</text>')
    out.append(f'<text x="288" y="28" font-size="17" font-weight="700" fill="{BLK}">Design space of agent institutions</text>')

    # ---- Panel A (spread to span Panel B height) ----
    cxA=116; w=60; h=28; th=10
    top_pad=64; bot_pad=40
    span=H-top_pad-bot_pad
    cys=[top_pad+span*f for f in (0.14,0.5,0.86)]
    for (a,b) in [(0,1),(1,2)]:
        out.append(f'<line x1="{cxA-w}" y1="{cys[a]+th:.0f}" x2="{cxA-w}" y2="{cys[b]:.0f}" stroke="{HAIR}" stroke-width="1" stroke-dasharray="2 4" opacity="0.7"/>')
        out.append(f'<line x1="{cxA+w}" y1="{cys[a]+th:.0f}" x2="{cxA+w}" y2="{cys[b]:.0f}" stroke="{HAIR}" stroke-width="1" stroke-dasharray="2 4" opacity="0.7"/>')
    out.append(diamond(cxA,cys[0],w,h,th,AM_TOP,AM_SIDE,["Governing","institutions"],AM_D,nodes_net))
    out.append(diamond(cxA,cys[1],w,h,th,BL_TOP,BL_SIDE,["Agent–group","interactions"],BL_D,nodes_tri))
    out.append(diamond(cxA,cys[2],w,h,th,VI_TOP,VI_SIDE,["Individual model","(even if aligned)"],VI_D,nodes_one))
    ytop=cys[0]-10; ybot=cys[2]+h+th+8; ymid=(ytop+ybot)/2
    out.append(varrow(34,ytop,ybot,AM_M))   # top-down: tail at top, head at bottom
    LABEL_SHIFT=70  # Top-down label sits above the midpoint, Bottom-up below it
    ytd=ymid-LABEL_SHIFT; ybu=ymid+LABEL_SHIFT
    out.append(f'<text x="18" y="{ytd:.0f}" text-anchor="middle" font-size="16" font-weight="700" fill="{AM_M}" transform="rotate(-90 18 {ytd:.0f})">Top-down</text>')
    out.append(varrow(198,ybot,ytop,VI_M))  # bottom-up: tail at bottom, head at top
    out.append(f'<text x="214" y="{ybu:.0f}" text-anchor="middle" font-size="16" font-weight="700" fill="{VI_M}" transform="rotate(-90 214 {ybu:.0f})">Bottom-up</text>')

    # ---- Panel B ----
    all_gy=[sum(g[5])/len(g[5]) for g in groups]
    rooty=(min(all_gy)+max(all_gy))/2
    out.append(f'<rect x="{RX-28}" y="{rooty-20:.0f}" width="86" height="40" rx="20" fill="#F7F9FB" stroke="{INK}" stroke-width="1.1"/>')
    out.append(f'<text x="{RX+15}" y="{rooty-4:.0f}" text-anchor="middle" font-size="14.5" font-weight="700" fill="{INK}">Agent</text>')
    out.append(f'<text x="{RX+15}" y="{rooty+12:.0f}" text-anchor="middle" font-size="14.5" font-weight="700" fill="{INK}">institution</text>')
    for sname,scol,cy in seclabels:
        out.append(f'<text x="{RIGHTX}" y="{cy:.0f}" text-anchor="middle" font-size="13" font-weight="700" fill="{scol}" letter-spacing="0.6" transform="rotate(-90 {RIGHTX} {cy:.0f})">{sname}</text>')
    for (gname,dcol,bg,mcol,leaves,lys) in groups:
        gy=sum(lys)/len(lys); gw=GW; gx0=GX-16; gxr=gx0+gw; gcx=gx0+gw/2
        out.append(f'<path d="M {RX+58} {rooty:.0f} C {GX-36} {rooty:.0f}, {GX-36} {gy:.0f}, {gx0:.0f} {gy:.0f}" fill="none" stroke="{mcol}" stroke-width="1.2" opacity="0.7"/>')
        out.append(f'<rect x="{gx0:.0f}" y="{gy-16:.0f}" width="{gw}" height="32" rx="8" fill="{bg}" stroke="{mcol}" stroke-width="1.1"/>')
        gl=wrap(gname,GROUP_WRAP)
        if len(gl)==1:
            out.append(f'<text x="{gcx:.0f}" y="{gy:.0f}" text-anchor="middle" dominant-baseline="central" font-size="14" font-weight="700" fill="{dcol}">{esc(gname)}</text>')
        else:
            out.append(f'<text x="{gcx:.0f}" y="{gy-4:.0f}" text-anchor="middle" font-size="14" font-weight="700" fill="{dcol}">{esc(gl[0])}</text>')
            out.append(f'<text x="{gcx:.0f}" y="{gy+11:.0f}" text-anchor="middle" font-size="14" font-weight="700" fill="{dcol}">{esc(gl[1])}</text>')
        for (name,sub),ly in zip(leaves,lys):
            out.append(f'<path d="M {gxr:.0f} {gy:.0f} C {LX-24} {gy:.0f}, {LX-24} {ly:.0f}, {LX:.0f} {ly:.0f}" fill="none" stroke="{mcol}" stroke-width="1" opacity="0.6"/>')
            leaf_box(out,ly,name,sub,dcol,bg,mcol)
    out.append('</svg>')
    return "\n".join(out)

if __name__=="__main__":
    open("figs/figure4_multi-layer-institutions.html","w").write(build())
    print("wrote figs/figure4_multi-layer-institutions.html")
