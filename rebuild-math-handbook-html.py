#!/usr/bin/env python3
"""从桌面公式手册 .md 重新生成可读 HTML（KaTeX）。"""
from pathlib import Path
import json
import sys

MD = Path("/home/midea/桌面/考研数学二-必背公式手册.md")
OUTS = [
    Path("/home/midea/桌面/考研数学二-必背公式手册.html"),
    Path("/home/midea/Documents/learning/考研数学二-必背公式手册.html"),
]

def main() -> None:
    if not MD.exists():
        print("找不到:", MD, file=sys.stderr)
        sys.exit(1)
    md_js = json.dumps(MD.read_text(encoding="utf-8"), ensure_ascii=False)
    html = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>考研数学二 · 必背公式手册</title>
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.css" />
<style>
  :root { --bg:#f7f4ef; --paper:#fffdf8; --ink:#1c1917; --muted:#78716c; --accent:#0f766e; --border:#e7e5e4; }
  body { margin:0; font-family:"Noto Serif SC","Songti SC",Georgia,serif; background:var(--bg); color:var(--ink); line-height:1.7; }
  .wrap { max-width:880px; margin:0 auto; padding:2rem 1.25rem 4rem; }
  .toolbar { position:sticky; top:0; display:flex; gap:.75rem; flex-wrap:wrap; align-items:center; background:#f7f4efe6; border-bottom:1px solid var(--border); padding:.65rem 0; margin-bottom:1rem; }
  .toolbar span { color:var(--muted); font-size:.9rem; }
  .toolbar button { border:1px solid var(--border); background:#fff; border-radius:8px; padding:.35rem .7rem; cursor:pointer; }
  #content { background:var(--paper); border:1px solid var(--border); border-radius:14px; padding:1.5rem 1.6rem; }
  #content h1 { border-bottom:2px solid var(--accent); padding-bottom:.4rem; }
  #content h2 { color:#134e4a; margin-top:2rem; }
  #content table { border-collapse:collapse; width:100%; margin:1rem 0; }
  #content th, #content td { border:1px solid var(--border); padding:.45rem .6rem; }
  #content th { background:#f5f5f4; }
  #content strong { color:#9a3412; }
  #content .katex-display { overflow-x:auto; }
  .err { color:#b91c1c; background:#fef2f2; padding:1rem; border-radius:8px; }
</style>
</head>
<body>
  <div class="wrap">
    <div class="toolbar">
      <strong style="color:var(--accent)">公式阅读版</strong>
      <span>由 .md 生成 · 需联网加载 KaTeX</span>
      <button type="button" onclick="window.scrollTo({top:0,behavior:'smooth'})">回顶部</button>
    </div>
    <article id="content"><p>渲染中…</p></article>
  </div>
  <script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>
  <script src="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.js"></script>
  <script src="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/contrib/auto-render.min.js"></script>
  <script>
    const MD = __MD__;
    const el = document.getElementById('content');
    try {
      marked.setOptions({ gfm: true });
      el.innerHTML = marked.parse(MD);
      renderMathInElement(el, {
        delimiters: [
          {left: '$$', right: '$$', display: true},
          {left: '$', right: '$', display: false}
        ],
        throwOnError: false
      });
    } catch (e) {
      el.innerHTML = '<div class="err">渲染失败：' + e + '</div>';
    }
  </script>
</body>
</html>
""".replace("__MD__", md_js)

    for p in OUTS:
        try:
            p.write_text(html, encoding="utf-8")
            print("已生成:", p)
            return
        except PermissionError:
            print("无权限:", p)
    sys.exit(1)

if __name__ == "__main__":
    main()
