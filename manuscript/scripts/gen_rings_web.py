#!/usr/bin/env python3
"""Fig. 1 for the paper, drawn by the website's docs/rings.js in paper mode (same code as the interactive figure).

Serves the repo on a local port, loads figs/rings-paper.html in headless Chrome, saves the <svg> that rings.js
draws to figures/figure_nested-rings.svg, and prints the page to a vector PDF with Chrome (librsvg cannot draw
the curved textPath labels). Run from manuscript/:  python3 scripts/gen_rings_web.py
"""
import http.server, os, re, shutil, socketserver, subprocess, sys, threading, time

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..'))
OUT_SVG = os.path.join(HERE, '..', 'figures', 'figure_nested-rings.svg')
OUT_PDF = os.path.join(HERE, '..', 'figures', 'figure_nested-rings.pdf')
PAGE = 'manuscript/figs/rings-paper.html'
WIN_CHROME = '/mnt/c/Program Files/Google/Chrome/Application/chrome.exe'


def browser():
    for b in ('chromium', 'google-chrome', 'chromium-browser'):
        if shutil.which(b):
            return b
    if os.path.exists(WIN_CHROME):
        return WIN_CHROME
    sys.exit('Chrome or Chromium is required to export Fig. 1.')


class Quiet(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *a, **k):
        super().__init__(*a, directory=ROOT, **k)

    def log_message(self, *a):
        pass


def chrome(b, *args):
    """Run headless Chrome against the paper page, served from the repo root."""
    with socketserver.TCPServer(('0.0.0.0', 0), Quiet) as httpd:
        threading.Thread(target=httpd.serve_forever, daemon=True).start()
        time.sleep(1.5)  # Windows Chrome can miss a WSL port that was opened a moment ago
        url = f'http://localhost:{httpd.server_address[1]}/{PAGE}'
        out = subprocess.run([b, '--headless=new', '--disable-gpu', '--virtual-time-budget=4000', *args, url],
                             capture_output=True, text=True, timeout=120).stdout
        httpd.shutdown()
    return out


def main():
    b = browser()
    for _ in range(3):
        m = re.search(r'<svg[\s\S]*</svg>', chrome(b, '--dump-dom'))
        if m:
            break
    if not m:
        sys.exit('rings.js did not draw an SVG; check the browser console.')
    svg = re.sub(r'\s(class|tabindex|role|aria-[a-z]+|data-key|style)="[^"]*"', '', m.group(0))  # web-only attributes
    open(OUT_SVG, 'w', encoding='utf-8').write(svg)
    pdf = os.path.abspath(OUT_PDF)
    if b.startswith('/mnt/'):  # Windows Chrome from WSL needs a Windows path
        pdf = subprocess.run(['wslpath', '-w', pdf], capture_output=True, text=True).stdout.strip()
    for _ in range(3):
        chrome(b, '--no-pdf-header-footer', f'--print-to-pdf={pdf}')
        text = subprocess.run(['pdftotext', OUT_PDF, '-'], capture_output=True, text=True).stdout
        if 'Macrosystem' in text:
            break
    else:
        sys.exit('Chrome printed the page before the figure loaded; run the script again.')
    subprocess.run(['pdfcrop', '--margins', '4', OUT_PDF, OUT_PDF], check=True, capture_output=True)
    print(f'wrote {os.path.relpath(OUT_PDF)}')


if __name__ == '__main__':
    main()
