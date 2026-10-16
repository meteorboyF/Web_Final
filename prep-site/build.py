#!/usr/bin/env python3
"""Builds index.html from src/*.html fragments.

Directives inside fragments (each on its own line):
  @@code <lang> [title]     ... raw code ...   @@end
  @@table [title] | hl=1,3   header|header / row|row (prefix a cell with * to mark it changed)   @@end
"""
import html, os, re, glob

HERE = os.path.dirname(os.path.abspath(__file__))
LANG = {"js": "javascript", "html": "markup", "php": "php", "sql": "sql", "txt": "none"}
LABEL = {"js": "JavaScript", "html": "HTML", "php": "PHP", "sql": "SQL", "txt": "Text"}


def code_block(lang, title, body):
    body = body.strip("\n")
    t = html.escape(title) if title else LABEL.get(lang, lang)
    return (
        f'<figure class="code" data-lang="{lang}"><figcaption><span class="lang lang-{lang}">{LABEL.get(lang, lang)}</span>'
        f'<span class="fname">{t if title else ""}</span><button class="copy" type="button">Copy</button></figcaption>'
        f'<pre><code class="language-{LANG.get(lang, lang)}">{html.escape(body)}</code></pre></figure>'
    )


def table_block(spec, body):
    title, hl = spec, set()
    if "|" in spec:
        title, opts = spec.split("|", 1)
        m = re.search(r"hl=([\d,]+)", opts)
        if m:
            hl = {int(x) for x in m.group(1).split(",")}
    lines = [l for l in body.strip("\n").split("\n") if l.strip()]
    head = [c.strip() for c in lines[0].split("|")]
    out = ['<div class="rt">']
    if title.strip():
        out.append(f'<div class="rt-title">{html.escape(title.strip())}</div>')
    out.append('<div class="rt-scroll"><table><thead><tr>')
    out += [f"<th>{html.escape(h)}</th>" for h in head]
    out.append("</tr></thead><tbody>")
    for i, l in enumerate(lines[1:], 1):
        cls = ' class="hl"' if i in hl else ""
        out.append(f"<tr{cls}>")
        for c in l.split("|"):
            c = c.strip()
            if c.startswith("*"):
                out.append(f'<td class="chg">{html.escape(c[1:])}</td>')
            else:
                out.append(f"<td>{html.escape(c)}</td>")
        out.append("</tr>")
    out.append("</tbody></table></div></div>")
    return "".join(out)


def process(text):
    out, i, lines = [], 0, text.split("\n")
    while i < len(lines):
        line = lines[i]
        m = re.match(r"\s*@@(code|table)\s*(.*)$", line)
        if not m:
            out.append(line)
            i += 1
            continue
        kind, arg = m.group(1), m.group(2).strip()
        j = i + 1
        while not re.match(r"\s*@@end\s*$", lines[j]):
            j += 1
        body = "\n".join(lines[i + 1 : j])
        if kind == "code":
            parts = arg.split(None, 1)
            out.append(code_block(parts[0], parts[1] if len(parts) > 1 else "", body))
        else:
            out.append(table_block(arg, body))
        i = j + 1
    return "\n".join(out)


parts = [process(open(f, encoding="utf-8").read()) for f in sorted(glob.glob(os.path.join(HERE, "src", "*.html")))]
body = "\n".join(parts)
# artifact.html: fragment (the Artifact host adds the doctype/head/body skeleton)
open(os.path.join(HERE, "artifact.html"), "w", encoding="utf-8").write(body)
# index.html: standalone page to open locally
open(os.path.join(HERE, "index.html"), "w", encoding="utf-8").write(
    '<!DOCTYPE html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n'
    '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
    + body.replace("</style>", "</style>\n</head>\n<body>", 1) + "\n</body>\n</html>\n")
print("built index.html", sum(len(p) for p in parts) // 1024, "KB")
