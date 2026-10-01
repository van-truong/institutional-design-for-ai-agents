/* Motivational design space: the hand-drawn sticky-note collage, shown as nine tiles (one per note) so each note
   can wiggle gently on hover. Every tile is the same SVG seen through an svgView window cropped to one note, so the
   artwork stays a single file. Note boxes are in the SVG's viewBox units (800 x 900), with room for tape and shadow. */
(function () {
  const fig = document.querySelector(".paper-collage");
  const img = fig && fig.querySelector("img");
  if (!img) return;
  const SRC = img.getAttribute("src"), VW = 800, VH = 900;
  const NOTES = [  // measured from a native 800 x 900 render (ink extents, 2-px margin)
    [19, 29, 246, 280], [276, 38, 242, 276], [532, 37, 252, 265],
    [28, 334, 245, 262], [274, 335, 248, 248], [526, 332, 248, 263],
    [22, 616, 248, 258], [276, 609, 243, 255], [526, 613, 250, 266],
  ];
  const grid = document.createElement("div");
  grid.className = "notes-grid";
  grid.setAttribute("role", "img");
  grid.setAttribute("aria-label", img.getAttribute("alt") || "");
  NOTES.forEach(([x, y, w, h], i) => {
    const t = document.createElement("img");
    t.className = "note-tile";
    t.src = `${SRC}#svgView(viewBox(${x},${y},${w},${h}))`;
    t.alt = "";
    t.setAttribute("aria-hidden", "true");
    t.decoding = "async";
    Object.assign(t.style, { left: `${(100 * x) / VW}%`, top: `${(100 * y) / VH}%`, width: `${(100 * w) / VW}%`,
      height: `${(100 * h) / VH}%`, animationDelay: `${(i % 3) * 0.12}s` });
    grid.appendChild(t);
  });
  img.replaceWith(grid);
})();
