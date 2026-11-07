#!/usr/bin/env python3
"""Tiny static server with a download page for the profile kit.

  /                -> landing page with per-file download links
  /dl/<name>       -> file served as an attachment (real download)
  /view/<name>     -> file served inline (so SVG/HTML can be previewed)
  /<name>          -> raw file, for the README's relative image refs
"""
import mimetypes
import os
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import unquote, urlparse

ROOT = os.path.dirname(os.path.abspath(__file__))
PORT = int(os.environ.get("PORT", "8000"))

FILES = [
    ("README.md", "The profile README", "Paste this into your repo's README.md", "required"),
    ("banner.svg", "Animated banner", "1200x340 — spinning Sharingan, crest, embers", "required"),
    ("sharingan.svg", "Sharingan eye", "Spins forever; used 12x in the README", "required"),
    ("divider.svg", "Section divider", "Rule with a live miniature Sharingan", "required"),
    ("typing.svg", "Typing tagline", "Self-types “Wake up to reality.”", "required"),
    ("github-profile-madara.zip", "Everything, zipped", "All 7 files in one download", "optional"),
    ("SETUP.md", "Setup guide", "Step-by-step instructions", "reference"),
    ("repo-metadata.md", "Repo metadata", "Descriptions + topics for each repo", "reference"),
]

LANDING = """<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Profile kit — download</title>
<style>
  :root{{--bg:#0b0709;--panel:#120a0e;--bor:#3a1119;--fg:#f2eae6;--mut:#a08f96;--cri:#c1121f;--emb:#ff7a18}}
  *{{box-sizing:border-box}}
  body{{margin:0;background:radial-gradient(circle at 78% 0%,#2a0509 0%,#0b0709 55%);color:var(--fg);
    font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Helvetica,Arial,sans-serif;line-height:1.55;
    min-height:100vh;padding:48px 24px 96px}}
  .wrap{{max-width:880px;margin:0 auto}}
  .kicker{{font:600 11px/1 ui-monospace,Menlo,monospace;letter-spacing:.28em;color:var(--cri);
    text-transform:uppercase;margin-bottom:14px}}
  h1{{font-size:2.1rem;margin:0 0 10px;letter-spacing:-.01em}}
  h1 span{{color:var(--cri)}}
  .sub{{color:var(--mut);margin:0 0 8px;font-size:15px}}
  .warn{{border-left:3px solid var(--emb);background:rgba(255,122,24,.09);padding:12px 16px;
    border-radius:0 6px 6px 0;font-size:13.5px;color:#e8d9cf;margin:24px 0 32px}}
  .warn b{{color:#ffb87a}}
  h2{{font-size:12px;letter-spacing:.2em;text-transform:uppercase;color:var(--mut);
    margin:34px 0 12px;font-weight:600}}
  .row{{display:flex;align-items:center;gap:16px;background:var(--panel);border:1px solid var(--bor);
    border-radius:10px;padding:14px 18px;margin-bottom:10px;text-decoration:none;color:inherit;
    transition:border-color .15s,transform .15s}}
  .row:hover{{border-color:var(--cri);transform:translateX(3px)}}
  .ico{{width:38px;height:38px;flex:none;border-radius:8px;display:grid;place-items:center;
    background:#1d080c;border:1px solid #4a1119;font:600 11px ui-monospace,monospace;color:#ff8a8a}}
  .meta{{flex:1;min-width:0}}
  .name{{font-weight:650;font-size:15px}}
  .desc{{color:var(--mut);font-size:13px;margin-top:2px}}
  .file{{font:11px ui-monospace,monospace;color:#6e5c63;margin-top:3px}}
  .tag{{font:600 10px ui-monospace,monospace;text-transform:uppercase;letter-spacing:.1em;
    border-radius:20px;padding:3px 9px;flex:none}}
  .req{{color:#ff9d9d;border:1px solid #7a1520;background:#2a0509}}
  .opt{{color:#ffc49a;border:1px solid #7a3f15;background:#2a1505}}
  .ref{{color:var(--mut);border:1px solid #3a3136;background:#161014}}
  .arrow{{color:var(--cri);flex:none;font-size:18px}}
  .foot{{color:#6e5c63;font-size:12.5px;margin-top:36px;border-top:1px solid #2a1116;padding-top:18px}}
  code{{background:#1a0e12;padding:.15em .4em;border-radius:4px;font-size:88%;color:#ffb4b4}}
  a.inline{{color:var(--emb)}}
</style></head><body><div class="wrap">

<div class="kicker">Uchiha Clan · Profile Kit</div>
<h1>Download <span>every file.</span></h1>
<p class="sub">Tap a row to download it. Five are needed; two are just reading.</p>

<div class="warn">
  <b>All 5 required files must sit loose in the repo root</b> — flat, next to each other.
  The README refers to them as <code>./banner.svg</code>. In a subfolder, it's a broken image.
</div>

<h2>Upload these</h2>
{rows_required}

<h2>Handy + reference</h2>
{rows_other}

<div class="foot">
  <a class="inline" href="/preview.html">▸ See the live preview</a> &nbsp;·&nbsp;
  <a class="inline" href="/dl/github-profile-madara.zip">▸ Grab everything at once</a>
</div>

</div></body></html>"""


def row(name, title, desc, prio, size):
    klass = {"required": "req", "optional": "opt", "reference": "ref"}[prio]
    label = {"required": "required", "optional": "bundle", "reference": "reference"}[prio]
    ext = os.path.splitext(name)[1].lower().lstrip(".") or "file"
    return f'''  <a class="row" href="/dl/{name}">
    <div class="ico">{ext.upper()[:4]}</div>
    <div class="meta">
      <div class="name">{title}</div>
      <div class="desc">{desc}</div>
      <div class="file">{name} · {size}</div>
    </div>
    <span class="tag {klass}">{label}</span>
    <span class="arrow">↓</span>
  </a>'''


class Handler(BaseHTTPRequestHandler):
    def log_message(self, fmt, *a):
        print("%s - %s" % (self.address_string(), fmt % a), flush=True)

    def _size(self, path):
        try:
            b = os.path.getsize(path)
        except OSError:
            return "?"
        return f"{b / 1024:.1f} KB" if b < 1024 * 1024 else f"{b / 1048576:.1f} MB"

    def _index(self):
        rows_req, rows_other = [], []
        for name, title, desc, prio in FILES:
            p = os.path.join(ROOT, name)
            if not os.path.exists(p):
                continue
            r = row(name, title, desc, prio, self._size(p))
            (rows_req if prio == "required" else rows_other).append(r)
        html = LANDING.format(rows_required="\n".join(rows_req),
                              rows_other="\n".join(rows_other))
        body = html.encode()
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _file(self, name, attach):
        p = os.path.join(ROOT, name)
        if not os.path.isfile(p) or os.path.commonpath([ROOT, os.path.abspath(p)]) != ROOT:
            self.send_error(404)
            return
        ctype = mimetypes.guess_type(p)[0] or "application/octet-stream"
        if p.endswith(".svg"):
            ctype = "image/svg+xml"
        if p.endswith(".md"):
            ctype = "text/markdown; charset=utf-8"
        data = open(p, "rb").read()
        self.send_response(200)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(data)))
        if attach:
            self.send_header("Content-Disposition", f'attachment; filename="{name}"')
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self):
        path = unquote(urlparse(self.path).path)
        if path in ("/", "/index.html"):
            return self._index()
        if path.startswith("/dl/"):
            return self._file(path[4:], attach=True)
        if path.startswith("/view/"):
            return self._file(path[6:], attach=False)
        return self._file(path.lstrip("/"), attach=False)


if __name__ == "__main__":
    print(f"serving {ROOT} on 0.0.0.0:{PORT}", flush=True)
    ThreadingHTTPServer(("0.0.0.0", PORT), Handler).serve_forever()
