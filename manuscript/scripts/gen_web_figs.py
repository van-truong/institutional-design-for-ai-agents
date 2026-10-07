#!/usr/bin/env python3
"""Paper figures drawn by the website's own scripts in paper mode, so the paper and the site share one drawing.

  figure_nested-rings          docs/rings.js       -> Fig. 1, nested systems around an agent
  figure_agent-in-context-web  docs/context.js     -> Fig. 2, top-down and bottom-up institutions
  figure_dilemmas              docs/dilemmas.js    -> Fig. 3, cooperation dilemmas
  figure_taxonomy-circle       docs/taxcircle.js   -> Fig. 4, the taxonomy at a glance
  figure_related-map           docs/related.js     -> Fig. 5, mind map of related efforts
  figure_design-space-game     docs/designspace.js -> Fig. 6, the design space of agent institutions
  figure_phenomena-map         docs/phenomena.js   -> Fig. 8, group-level phenomena
  figure_failure-stories       docs/failstory.js   -> Fig. 10, three ways a mechanism can fail (HTML panels, PDF only)
  figure_coleman-boat          docs/coleman.js     -> Fig. 11, the Coleman boat
Each is printed from its paper-mode page, manuscript/figs/*-paper.html. Figs. 7 and 9 come from render_figures.sh.

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
    'figure_agent-in-context-web': ('manuscript/figs/context-paper.html', 'Individual model'),
    'figure_taxonomy-circle': ('manuscript/figs/taxcircle-paper.html', 'mechanisms'),
    'figure_design-space-game': ('manuscript/figs/designspace-game-paper.html', 'deontic'),
    'figure_dilemmas': ('manuscript/figs/dilemmas-paper.html', 'Extractive'),
    'figure_phenomena-map': ('manuscript/figs/phenomena-paper.html', 'Collusion'),
    'figure_related-map': ('manuscript/figs/related-paper.html', 'Mind map'),
    'figure_failure-stories': ('manuscript/figs/failstory-paper.html', 'becomes a price'),
}
# figures laid out in HTML around several small drawings: printed to PDF only, with no single SVG to save
HTML_ONLY = {'figure_failure-stories'}
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

    def end_headers(self):
        # Chrome otherwise reuses a cached copy of a script it saw moments ago, and prints a stale figure
        self.send_header('Cache-Control', 'no-store')
        super().end_headers()


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
    if name not in HTML_ONLY:
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
