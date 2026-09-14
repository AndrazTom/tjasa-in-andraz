import re, base64, mimetypes, sys, os

PROJECT = "/Users/andraz/Documents/saveDateCode"
SRC = os.path.join(PROJECT, "index.html")
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(PROJECT, "_artifact_build.html")

with open(SRC, "r") as f:
    html = f.read()

# index.html is a full standalone document (DOCTYPE/html/head/body) for
# self-hosting (GitHub Pages etc). Claude Artifacts inject their own
# doctype/head/body wrapper (with charset + viewport already set), so strip
# ours back out and keep just <title>, <style>, and the body content/script.
html = re.sub(r"<!DOCTYPE[^>]*>\s*", "", html, flags=re.IGNORECASE)
html = re.sub(r"</?html[^>]*>\s*", "", html, flags=re.IGNORECASE)
html = re.sub(r"<head>\s*", "", html, flags=re.IGNORECASE)
html = re.sub(r"</head>\s*", "", html, flags=re.IGNORECASE)
html = re.sub(r'<meta charset="UTF-8">\s*', "", html, flags=re.IGNORECASE)
html = re.sub(r'<meta name="viewport"[^>]*>\s*', "", html, flags=re.IGNORECASE)
html = re.sub(r"<body>\s*", "", html, flags=re.IGNORECASE)
html = re.sub(r"</body>\s*", "", html, flags=re.IGNORECASE)

pattern = re.compile(r"""(['"(])(images/[^'")]+)(['")])""")

def inline(m):
    prefix, relpath, suffix = m.groups()
    abspath = os.path.join(PROJECT, relpath)
    mime = mimetypes.guess_type(abspath)[0] or "application/octet-stream"
    with open(abspath, "rb") as imgf:
        b64 = base64.b64encode(imgf.read()).decode("ascii")
    return f"{prefix}data:{mime};base64,{b64}{suffix}"

html2 = pattern.sub(inline, html)

with open(OUT, "w") as f:
    f.write(html2)

print("wrote", OUT, "size", len(html2))
