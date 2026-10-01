#!/usr/bin/env python3
"""Normalize website headshots so every face is the same size and height inside its circle.

Each source photo gets hand-measured landmarks (face center x, eye line y, chin y, in a 300-px preview where the long
side is 300). The crop is a square whose side makes eye-to-chin = TARGET of the diameter, with the face midpoint at
(0.5, MID_Y). Where the crop runs past the photo, or past an old circular crop, pixels are extended radially from
inside the usable area and softened, so shoulders and background continue instead of showing a hard edge.
Writes docs/assets/heads/<name>.jpg (400x400). Run from the repo root.
"""
import math, os
import numpy as np
from PIL import Image, ImageFilter

SRC, OUT = 'docs/assets', 'docs/assets/heads'
TARGET, MID_Y, SIZE, MAX_ZOOM_OUT = 0.20, 0.47, 400, 1.32  # eye-to-chin / diameter, matched to Van, Erivan, and Terry
# name: (face center x, eye y, chin y) in the 300-px preview; circle=True if the source is already circle-cropped
HEADS = {
    'van-truong': (150, 112, 172, True), 'xuanqiang-angelo-huang': (152, 112, 156, False),
    'erivan-inan': (145, 105, 152, False), 'ryan-faulkner': (150, 113, 200, False),
    'joel-naoki-christoph': (95, 96, 150, False), 'terry-jingchen-zhang': (185, 142, 210, True),
    'david-guzman-piedrahita': (138, 114, 205, True), 'zhijing-jin': (150, 132, 215, True),
}


def main():
    os.makedirs(OUT, exist_ok=True)
    for name, (fx, ey, cy, circle) in HEADS.items():
        im = Image.open(os.path.join(SRC, name + '.jpg')).convert('RGB')
        w, h = im.size
        s = 300 / max(w, h)
        fx, ey, cy = fx / s, ey / s, cy / s
        side = (cy - ey) / TARGET
        usable = (min(w, h) if circle else max(w, h))
        side = min(side, MAX_ZOOM_OUT * usable)  # very tight sources stay a little closer than the rest
        mx, my = fx, (ey + cy) / 2
        x0, y0 = mx - side / 2, my - MID_Y * side
        a = np.asarray(im).astype(np.float32)
        # usable region: the old circle, or the full rectangle
        ccx, ccy, rr = w / 2, h / 2, min(w, h) / 2 - 3
        ys, xs = np.mgrid[0:SIZE, 0:SIZE]
        px = x0 + (xs + 0.5) * side / SIZE
        py = y0 + (ys + 0.5) * side / SIZE
        if circle:
            dx, dy = px - ccx, py - ccy
            r = np.hypot(dx, dy)
            outside = r > rr
            k = np.where(outside, rr / np.maximum(r, 1e-6), 1.0)
            qx, qy = ccx + dx * k, ccy + dy * k  # upper half: continue the backdrop radially
            # lower half: continue shoulders and clothing straight down from the old circle's edge
            lx = np.clip(px, ccx - rr * 0.97, ccx + rr * 0.97)
            ly = np.minimum(py, ccy + np.sqrt(np.maximum(rr * rr - (lx - ccx) ** 2, 0)) - 2)
            low = outside & (py > ccy)
            qx, qy = np.where(low, lx, qx), np.where(low, ly, qy)
        else:
            outside = (px < 1) | (py < 1) | (px > w - 2) | (py > h - 2)
            qx, qy = np.clip(px, 1, w - 2), np.clip(py, 1, h - 2)
        xi, yi = np.clip(qx.astype(int), 0, w - 1), np.clip(qy.astype(int), 0, h - 1)
        out = Image.fromarray(a[yi, xi].astype(np.uint8))
        if outside.any():  # soften the extended pixels so they read as background, not streaks
            soft = out.filter(ImageFilter.GaussianBlur(7))
            mask = Image.fromarray((outside * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(9))
            out = Image.composite(soft, out, mask)
        out.save(os.path.join(OUT, name + '.jpg'), quality=88)
        print(f'{name}: crop side {side:.0f}px, extended {outside.mean():.0%}')


if __name__ == '__main__':
    main()
