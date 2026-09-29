#!/usr/bin/env python3
"""Recolor figure HTML/SVGs to the shared master palette (figs/PALETTE.md).
Each observed color is classified by hue family + lightness bucket and mapped to the
canonical hex for that (family, bucket), preserving light/dark contrast structure.
Usage: python3 scripts/harmonize_palette.py [--apply] file1.html file2.html ...
"""
import re, sys, colorsys

# canonical palette: family -> {bucket: hex}
FAM = {
 'terra':  {'bg':'#FBEDE6','light':'#E7B79A','mid':'#C2662A','dark':'#8F3F1E'},
 'amber':  {'bg':'#FBEEDA','light':'#E3C88C','mid':'#C79A3A','dark':'#8A5A0B'},
 'green':  {'bg':'#E5F0E1','light':'#BBD9C4','mid':'#4F9070','dark':'#2F6B4A'},
 'blue':   {'bg':'#DCE8F5','light':'#A9C4E0','mid':'#3A6EA5','dark':'#2F3D6B'},
 'violet': {'bg':'#ECE9FB','light':'#C4BCEC','mid':'#6C5CD0','dark':'#463BA0'},
 'teal':   {'bg':'#E3F1EC','light':'#9FD9C7','mid':'#0F766E','dark':'#04342C'},
}
HUE = {'terra':19,'amber':42,'green':145,'blue':212,'violet':255,'teal':172}
NEUTRAL = [(0.92,'#FBFAF7'),(0.80,'#EEF2F6'),(0.55,'#B3BEC9'),(0.34,'#6B7787'),(0.0,'#3F4D5A')]

def hex2hls(h):
    h=h.lstrip('#'); r,g,b=(int(h[i:i+2],16)/255 for i in (0,2,4))
    hue,l,s=colorsys.rgb_to_hls(r,g,b); return hue*360,l,s

def bucket(l):
    if l>0.90: return 'bg'
    if l>0.72: return 'light'
    if l>0.45: return 'mid'
    return 'dark'

def map_hex(h):
    hue,l,s=hex2hls(h)
    if s<0.16:  # neutral / gray
        for thr,val in NEUTRAL:
            if l>=thr: return val
        return '#3F4D5A'
    fam=min(HUE, key=lambda f: min(abs(hue-HUE[f]),360-abs(hue-HUE[f])))
    return FAM[fam][bucket(l)]

def process(path, apply):
    src=open(path).read()
    hexes=sorted(set(re.findall(r'#[0-9A-Fa-f]{6}', src)))
    changes={}
    for h in hexes:
        nh=map_hex(h)
        if nh.lower()!=h.lower(): changes[h]=nh
    print(f"\n=== {path} : {len(hexes)} colors, {len(changes)} remapped ===")
    for h in hexes:
        hue,l,s=hex2hls(h)
        tag='neutral' if s<0.16 else min(HUE, key=lambda f: min(abs(hue-HUE[f]),360-abs(hue-HUE[f])))
        arrow=f" -> {changes[h]}" if h in changes else "  (kept)"
        print(f"  {h}  L={l:.2f} S={s:.2f} [{tag}]{arrow}")
    if apply:
        out=src
        for h,nh in changes.items():
            out=re.sub(re.escape(h), nh, out, flags=re.I)
        open(path,'w').write(out)
        print("  APPLIED")

if __name__=='__main__':
    apply='--apply' in sys.argv
    files=[a for a in sys.argv[1:] if not a.startswith('--')]
    for f in files: process(f, apply)
