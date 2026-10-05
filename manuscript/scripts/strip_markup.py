"""Make a clean submission source: unwrap highlight macros, drop deletions, hidden blocks, and comments."""
import re, sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src).read()
s = s.replace(r"\showreviewflagstrue", r"\showreviewflagsfalse")

def arg_end(s, i):
    # s[i] == '{'; return index just past the matching brace
    d = 0
    while i < len(s):
        c = s[i]
        if c == '\\': i += 2; continue
        if c == '{': d += 1
        elif c == '}':
            d -= 1
            if d == 0: return i + 1
        i += 1
    raise ValueError("unbalanced")

UNWRAP = ["chg", "rework", "voice", "aiflag", "fixed", "dup", "vqt", "REVIEWFLAG", "REVISED"]
DROP = ["del", "delbanner", "ANG", "VAN", "TODO", "ERI", "RYAN", "JOEL", "ERIVAN"]
body_start = s.index(r"\begin{abstract}")      # leave the preamble's macro definitions alone
head, body = s[:body_start], s[body_start:]

# 1. full-line comments
body = "\n".join(l for l in body.split("\n") if not re.match(r"\s*%", l))
# 2. \iffalse ... \fi blocks (nesting-aware)
out, i = [], 0
for m in re.finditer(r"\\iffalse\b", body): pass
while True:
    m = re.search(r"\\iffalse\b", body[i:])
    if not m: out.append(body[i:]); break
    a = i + m.start(); out.append(body[i:a]); depth, j = 0, a
    for t in re.finditer(r"\\if[a-zA-Z]*|\\fi(?![a-zA-Z])", body[a:]):
        depth += 1 if t.group().startswith(r"\if") else -1
        if depth == 0: j = a + t.end(); break
    i = j
body = "".join(out)
# 3. macros
pat = re.compile(r"\\(" + "|".join(UNWRAP + DROP) + r")(?![a-zA-Z])\s*\{")
while True:
    m = pat.search(body)
    if not m: break
    b = m.end() - 1; e = arg_end(body, b)
    body = body[:m.start()] + ("" if m.group(1) in DROP else body[b + 1:e - 1]) + body[e:]
body = re.sub(r"\n{3,}", "\n\n", body)
open(dst, "w").write(head + body)
