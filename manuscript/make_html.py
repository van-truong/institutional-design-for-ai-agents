#!/usr/bin/env python3
"""Build a clickable, highlighted HTML reading copy of the manuscript into html-preview/.

Citations link to their source (opens in a new tab); review flags render as colored highlights.
Run `make pdf` first so .build/manuscript.bbl is current, then:  python3 make_html.py
"""
import glob, os, re, shutil, subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
os.chdir(HERE)


def sh(*a):
    subprocess.run(a, check=False, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


# 1. figures PDF -> PNG (tex4ht embeds these directly)
for f in glob.glob('figures/*.pdf'):
    b = os.path.splitext(os.path.basename(f))[0]
    sh('pdftoppm', '-png', '-r', '150', '-singlefile', f, 'figures/' + b)

# 2. HTML copy: figures -> png; flags -> plain-text sentinels so \citep still resolves
s = open('manuscript.tex', encoding='utf-8').read()
s = re.sub(r'(\\includegraphics(\[[^]]*\])?\{figures/[^}]+)\.pdf\}', r'\1.png}', s)
hook = ('\n\\renewcommand{\\voice}[1]{ZZVB#1ZZVE}\n\\renewcommand{\\aiflag}[1]{ZZAB#1ZZAE}\n'
        '\\renewcommand{\\rework}[1]{ZZRB#1ZZRE}\n\\renewcommand{\\REVIEWFLAG}[1]{ZZXB#1ZZXE}\n'
        '\\renewcommand{\\del}[1]{ZZDB#1ZZDE}\n\\begin{document}')
s = s.replace('\\begin{document}', hook, 1)
open('manuscript_html.tex', 'w', encoding='utf-8').write(s)
shutil.copy('.build/manuscript.bbl', 'manuscript_html.bbl')

# 3. build
shutil.rmtree('html-preview', ignore_errors=True); os.makedirs('html-preview/figures', exist_ok=True)
subprocess.run(['make4ht', '-d', 'html-preview', 'manuscript_html.tex'], check=False,
               stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
for f in glob.glob('figures/*.png'):
    shutil.copy(f, 'html-preview/figures/')

# 4. key -> source URL
bib = open('references.bib', encoding='utf-8').read()
key2url = {}
for e in re.split(r'(?=@\w+\{)', bib):
    m = re.match(r'@\w+\{([^,]+),', e)
    if not m:
        continue
    def fld(n, e=e):
        mm = re.search(r'\b' + n + r'\s*=\s*[{"]([^}"]+)[}"]', e, re.I)
        return mm.group(1).strip() if mm else ''
    u = fld('url') or ('https://doi.org/' + fld('doi') if fld('doi') else
                       ('https://arxiv.org/abs/' + fld('eprint') if fld('eprint') else ''))
    if u:
        key2url[m.group(1).strip()] = u

SENT = {'ZZVB': "<span class='fl-voice'>", 'ZZVE': "</span>", 'ZZAB': "<span class='fl-ai'>", 'ZZAE': "</span>",
        'ZZRB': "<span class='fl-rework'>", 'ZZRE': "</span>", 'ZZXB': "<span class='fl-review'>", 'ZZXE': "</span>",
        'ZZDB': "<del class='fl-del'>", 'ZZDE': "</del>"}
for hf in glob.glob('html-preview/manuscript_html*.html'):
    h = open(hf, encoding='utf-8').read()
    for a, b in SENT.items():
        h = h.replace(a, b)
    h = re.sub(r"<a href='#X([A-Za-z0-9]+)'",
               lambda m: ("<a class='src' target='_blank' rel='noopener' href='%s'" % key2url[m.group(1)])
               if m.group(1) in key2url else m.group(0), h)
    open(hf, 'w', encoding='utf-8').write(h)

open('html-preview/manuscript_html.css', 'a', encoding='utf-8').write('''
.fl-voice{background:#fff59d;padding:0 .05em;}.fl-ai{background:#ffc98a;padding:0 .05em;}
.fl-rework{background:#ffbccd;padding:0 .05em;}.fl-review{color:#c0392b;font-weight:bold;}.fl-del{color:#a33;}
a.src{color:#1669c1;text-decoration:none;}a.src:hover{text-decoration:underline;}
img{max-width:100%;height:auto;display:block;margin:0 auto;}
.rf-banner{position:sticky;top:0;z-index:99;background:#20303f;color:#fff;padding:8px 14px;font:13px/1.4 Arial,sans-serif;text-align:center;}
.rf-banner b{color:#ffe067;}.rf-banner .o{color:#ffc98a;}.rf-banner .p{color:#ffbccd;}.rf-banner .r{color:#ff9a8a;}.rf-banner .c{color:#9ecbff;}
''')
banner = ("<div class='rf-banner'>Review copy — <b>yellow</b> rewrite in your voice · "
          "<span class='o'>orange</span> sounds AI-written · <span class='p'>pink</span> figure to redesign · "
          "<span class='r'>red</span> verify claim · <span class='c'>blue citation numbers</span> open the source.</div>")
hf = 'html-preview/manuscript_html.html'
h = open(hf, encoding='utf-8').read()
open(hf, 'w', encoding='utf-8').write(re.sub(r'(<body[^>]*>)', r'\1' + banner, h, count=1))

for junk in glob.glob('manuscript_html*'):
    os.remove(junk)
for f in glob.glob('figures/*.png'):
    os.remove(f)
print('wrote html-preview/manuscript_html.html')
