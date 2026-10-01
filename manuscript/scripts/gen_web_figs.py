#!/usr/bin/env python3
"""Paper figures drawn by the website's own scripts in paper mode, so the paper and the site share one drawing.

  figure_nested-rings   docs/rings.js    via figs/rings-paper.html     -> Fig. 1
  figure_coleman-boat   docs/coleman.js  via figs/coleman-paper.html   -> the Coleman boat
  figure_failure-modes  docs/failures.js via figs/failures-paper.html  -> where mechanisms fail

Serves the repo on a local port, loads each page in headless Chrome, saves the <svg> the script draws to
figures/<name>.svg, and prints the page to a vector PDF with Chrome (librsvg cannot draw curved textPath labels).
Run from manuscript/:  python3 scripts/gen_web_figs.py [name ...]
"""
import http.server, os, re, shutil, socketserver, subprocess, sys, threading, time

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..'))
FIGURES = os.path.join(HERE, '..', 'figures')
# name -> (page, a word the printed PDF must contain, proving the figure drew before printing)
FIGS = {
    'figure_nested-rings': ('manuscript/figs/rings-paper.html', 'Macrosystem'),
    'figure_coleman-boat': ('manuscript/figs/coleman-paper.html', 'Institutional change'),
    'figure_failure-modes': ('manuscript/figs/failures-paper.html', 'Paid, not obeyed'),
    'figure_agent-in-context-web': ('manuscript/figs/context-paper.html', 'Individual model'),
    'figure_design-space-web': ('manuscript/figs/designspace-paper.html', 'Agent institution'),
    'figure_taxonomy-circle': ('manuscript/figs/taxcircle-paper.html', 'mechanisms'),
    'figure_design-space-game': ('manuscript/figs/designspace-game-paper.html', 'Badges'),  # draft: Fig. 4 with game badges
    'figure_dilemmas': ('manuscript/figs/dilemmas-paper.html', 'Extractive'),
    'figure_phenomena-map': ('manuscript/figs/phenomena-paper.html', 'Collusion'),
}
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


def chrome(b, page, *args):
    """Run headless Chrome against the paper page, served from the repo root."""
    with socketserver.TCPServer(('0.0.0.0', 0), Quiet) as httpd:
        threading.Thread(target=httpd.serve_forever, daemon=True).start()
        time.sleep(1.5)  # Windows Chrome can miss a WSL port that was opened a moment ago
        url = f'http://localhost:{httpd.server_address[1]}/{page}'
        out = subprocess.run([b, '--headless=new', '--disable-gpu', '--virtual-time-budget=4000', *args, url],
                             capture_output=True, text=True, timeout=120).stdout
        httpd.shutdown()
    return out


def export(b, name):
    page, check = FIGS[name]
    out_svg, out_pdf = os.path.join(FIGURES, name + '.svg'), os.path.join(FIGURES, name + '.pdf')
    for _ in range(3):
        m = re.search(r'<svg[\s\S]*</svg>', chrome(b, page, '--dump-dom'))
        if m:
            break
    if not m:
        sys.exit(f'{page} did not draw an SVG; check the browser console.')
    svg = re.sub(r'\s(class|tabindex|role|aria-[a-z]+|data-key|style)="[^"]*"', '', m.group(0))  # web-only attributes
    open(out_svg, 'w', encoding='utf-8').write(svg)
    pdf = os.path.abspath(out_pdf)
    if b.startswith('/mnt/'):  # Windows Chrome from WSL needs a Windows path
        pdf = subprocess.run(['wslpath', '-w', pdf], capture_output=True, text=True).stdout.strip()
    for _ in range(3):
        chrome(b, page, '--no-pdf-header-footer', f'--print-to-pdf={pdf}')
        text = subprocess.run(['pdftotext', out_pdf, '-'], capture_output=True, text=True).stdout
        if check in text:
            break
    else:
        sys.exit(f'Chrome printed {page} before the figure loaded; run the script again.')
    subprocess.run(['pdfcrop', '--margins', '4', out_pdf, out_pdf], check=True, capture_output=True)
    print(f'wrote {os.path.relpath(out_pdf)}')


def main():
    b = browser()
    for name in sys.argv[1:] or FIGS:
        export(b, name)


if __name__ == '__main__':
    main()
