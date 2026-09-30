#!/usr/bin/env python3
"""Generate an unwrapped (horizontal dendrogram) taxonomy figure as a single-SVG HTML.
Two columns of families so 73 leaves fit a page with >=6pt leaf text at \\textwidth.
Colorblind-safe Okabe-Ito palette."""
import html

# family: (line1, line2, discipline, color) ; leaves in display order
FAMILIES = {
 "social":     ("Social /","reputational","sociology · anthropology","#C2662A",
    ["Gossip & shaming","Ostracism & exile","Praise & status","Public commitment",
     "Resource taboo","Metanorm","Ridicule","Universalization"]),
 "formal":     ("Formal /","institutional","law · governance","#C79A3A",
    ["Warning","Escalating fine","Suspension","Rehabilitation","Elected monitor",
     "Collective punishment","Institutional choice","Cheap talk","Binding commitment",
     "Liquidated damages","Sentencing guidelines","Auto-fixed fine","Cross-default",
     "Whistleblower leniency","Anti-social filter","Constitutional rules","Formal appeals",
     "Mediation & arbitration","False-positive correction"]),
 "economic":   ("Economic /","incentive-based","economics · behavioural science","#4F9070",
    ["Pigouvian tax","Pigouvian subsidy","Altruistic punishment","Carrot/stick choice",
     "Moral hazard premium","Reputation bond","Fermi imitation","Algorithm generation",
     "TFT / WSLS","Threshold switch","Nudge & defaults"]),
 "technical":  ("Technical /","protocol-enforced","computer science · cryptography","#3A6EA5",
    ["Cryptographic log","Reputation score","Immutable transparency","Hard rate limit",
     "Graduated throttling","Exponential back-off","Allow/deny list","Governance graph",
     "VCG mechanism","PoS slashing","Restaking","Staking reward","Token toxicity",
     "Auto-execution","DAO voting","Curated registry","Hard-fork override"]),
 "mutualaid":  ("Mutual aid /","solidarity","sociology · solidarity economics","#6C5CD0",
    ["Timebanking","Community currency","Generalised reciprocity","Network embeddedness",
     "Mutual accountability","Indirect reciprocity","Worker cooperative","Participatory budgeting",
     "Bail / insurance pool","Mutual-aid DAO","Mesh network"]),
 "restorative":("Restorative /","reparative","restorative justice · law","#0F766E",
    ["Repair","Restitution","Reintegration","Reconciliation","Apology","Truth-telling",
     "Post-breach rehab"]),
}

COLUMNS = [["social","formal","economic"], ["technical","mutualaid","restorative"]]

# geometry (user units)
ROW      = 17.0     # per-leaf vertical step
FAM_GAP  = 16.0     # extra gap between families in a column
TOP      = 74.0     # top margin (title sits above)
LEFT_PAD = 14.0     # left margin so right-aligned labels never clip
PANEL_W  = 320.0    # width of one column panel
PANEL_GAP= 24.0
LABEL_X  = 112.0    # right edge that family labels align to
SPINE_X  = 120.0    # vertical family spine
DOT_X    = 150.0    # leaf marker
TEXT_X   = 159.0    # leaf text start

def esc(s): return html.escape(s, quote=False)

def build():
    # compute per-column heights, use max
    col_rows = [sum(len(FAMILIES[f][4]) for f in col) + FAM_GAP/ROW*(len(col)-1) for col in COLUMNS]
    body_h = max(col_rows) * ROW
    H = TOP + body_h + 40
    W = LEFT_PAD + PANEL_W*2 + PANEL_GAP + 8
    out = []
    out.append(f'<?xml version="1.0" encoding="UTF-8"?>')
    out.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W:.0f} {H:.0f}" '
               f'font-family="\'Helvetica Neue\', Arial, sans-serif">')
    out.append('<title>Taxonomy of cooperation-shaping mechanisms</title>')
    out.append('<desc>An unwrapped tree of 73 cooperation-shaping mechanisms grouped into six '
               'families, drawn from sociology, anthropology, law, governance, economics, '
               'behavioural science, computer science, cryptography, solidarity economics, and '
               'restorative justice.</desc>')
    out.append('<style>'
               '.leaf{font-size:13px;fill:#2C2C2A}'
               '.fam{font-size:14.5px;font-weight:700;text-anchor:end}'
               '.disc{font-size:9px;font-style:italic;text-anchor:end}'
               '.root{font-size:16px;font-weight:700;fill:#2C2C2A;text-anchor:middle}'
               '.rootsub{font-size:11px;font-style:italic;fill:#5F5E5A;text-anchor:middle}'
               '</style>')
    # title
    out.append(f'<text class="root" x="{W/2:.1f}" y="34">Cooperation-shaping mechanisms for agent groups</text>')

    for ci, col in enumerate(COLUMNS):
        ox = LEFT_PAD + ci*(PANEL_W+PANEL_GAP)
        y = TOP
        for fkey in col:
            l1,l2,disc,color,leaves = FAMILIES[fkey]
            n = len(leaves)
            y0 = y
            y1 = y + (n-1)*ROW
            ymid = (y0+y1)/2
            # family spine
            out.append(f'<line x1="{ox+SPINE_X:.1f}" y1="{y0:.1f}" x2="{ox+SPINE_X:.1f}" '
                       f'y2="{y1:.1f}" stroke="{color}" stroke-width="2.4"/>')
            # family label (two lines) + discipline, right-aligned to spine
            out.append(f'<text class="fam" x="{ox+LABEL_X:.1f}" y="{ymid-7:.1f}" fill="{color}">{esc(l1)}</text>')
            out.append(f'<text class="fam" x="{ox+LABEL_X:.1f}" y="{ymid+8:.1f}" fill="{color}">{esc(l2)}</text>')
            # discipline subtitles omitted from the figure (listed in the caption) to keep all
            # figure lettering >=6pt and reduce clutter.
            # connector from label to spine
            out.append(f'<line x1="{ox+SPINE_X-6:.1f}" y1="{ymid:.1f}" x2="{ox+SPINE_X:.1f}" '
                       f'y2="{ymid:.1f}" stroke="{color}" stroke-width="1.2" opacity="0.7"/>')
            for i,leaf in enumerate(leaves):
                ly = y + i*ROW
                out.append(f'<line x1="{ox+SPINE_X:.1f}" y1="{ly:.1f}" x2="{ox+DOT_X:.1f}" '
                           f'y2="{ly:.1f}" stroke="{color}" stroke-width="1.1" opacity="0.65"/>')
                out.append(f'<circle cx="{ox+DOT_X:.1f}" cy="{ly:.1f}" r="2.2" fill="{color}"/>')
                out.append(f'<text class="leaf" x="{ox+TEXT_X:.1f}" y="{ly:.1f}" '
                           f'dominant-baseline="central">{esc(leaf)}</text>')
            y = y1 + FAM_GAP + ROW
    out.append('</svg>')
    return "\n".join(out)

if __name__ == "__main__":
    total = sum(len(FAMILIES[f][4]) for f in FAMILIES)
    assert total == 73, total
    open('figs/figure5_cooperation-taxonomy.html','w').write(build())
    print("wrote figs/figure5_cooperation-taxonomy.html ; total leaves:", total)
