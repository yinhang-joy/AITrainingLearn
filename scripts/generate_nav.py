"""生成 练习导航.html：扫描素材单元目录，生成卡片式导航页。

用法：python scripts/generate_nav.py（在仓库根目录运行）
依赖：pandas（预览数据用），openpyxl（xlsx 预览用）
"""
import os
import re
import html
import glob
import json
from urllib.parse import quote

import pandas as pd

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MAT = "人工智能训练师三级上网素材"
OUT = "练习导航.html"
PREVIEW_ROWS = 8
PREVIEW_COLS = 8


def read_title(unit_dir: str, unit: str) -> str:
    """从单元内 HTML 的 <title> 提取任务名"""
    hpath = os.path.join(unit_dir, f"{unit}.html")
    raw = ""
    if os.path.exists(hpath):
        for enc in ("utf-8", "gbk"):
            try:
                with open(hpath, encoding=enc) as f:
                    raw = f.read()
                break
            except (UnicodeDecodeError, OSError):
                continue
    m = re.search(r"<title>(.*?)</title>", raw, re.S)
    return html.unescape(m.group(1).strip()) if m else unit


def make_preview(path: str) -> str:
    """读取 csv/xlsx 前几行，生成 <details> 预览表格 HTML"""
    try:
        if path.endswith(".xlsx"):
            df = pd.read_excel(path, nrows=PREVIEW_ROWS)
        else:
            for enc in ("utf-8", "gbk"):
                try:
                    df = pd.read_csv(path, nrows=PREVIEW_ROWS, encoding=enc)
                    break
                except UnicodeDecodeError:
                    continue
            else:
                return ""
    except Exception:
        return ""
    if df is None or df.empty:
        return ""
    df = df.iloc[:, :PREVIEW_COLS]
    head = "".join(f"<th>{html.escape(str(c))}</th>" for c in df.columns)
    rows = ""
    for _, r in df.iterrows():
        cells = "".join(
            f"<td title=\"{html.escape(str(v))}\">{html.escape(str(v))[:40]}</td>"
            for v in r.values
        )
        rows += f"<tr>{cells}</tr>"
    return (
        f'<details class="preview"><summary>数据预览（前 {len(df)} 行）</summary>'
        f'<div class="tblwrap"><table><thead><tr>{head}</tr></thead>'
        f"<tbody>{rows}</tbody></table></div></details>"
    )


def jlab_url(rel: str) -> str:
    return "http://localhost:8888/lab/tree/" + quote(rel, safe="/")


def build_card(unit: str, title: str, files) -> str:
    links, previews, jbtns = [], [], []
    for f, role in files:
        rel = os.path.join(MAT, unit, f).replace("\\", "/")
        if f.endswith(".ipynb"):
            jbtns.append(
                f'<a href="{jlab_url(rel)}" target="_blank" class="jbtn">在 Jupyter 打开</a>'
            )
        if f.endswith((".csv", ".xlsx")):
            previews.append(make_preview(os.path.join(MAT, unit, f)))
            if f.endswith(".csv"):
                jbtns.append(
                    f'<a href="{jlab_url(rel)}" target="_blank" class="jbtn">Jupyter 表格</a>'
                )
        links.append(
            f'<a href="{html.escape(rel)}" target="_blank" class="file" '
            f'title="{html.escape(rel)}">{role}<span class="fn">{html.escape(f)}</span></a>'
        )
    jrow = f'<div class="jrow">{"".join(jbtns)}</div>' if jbtns else ""
    return f"""<section class="card">
      <div class="card-head"><span class="no">{unit}</span><h3>{html.escape(title)}</h3></div>
      <div class="links">{"".join(links)}</div>
      {jrow}
      {"".join(previews)}
    </section>"""


def main() -> None:
    units = []
    for d in sorted(
        glob.glob(os.path.join(MAT, "*")),
        key=lambda x: [int(p) for p in os.path.basename(x).split(".")],
    ):
        unit = os.path.basename(d)
        files = []
        for f in sorted(os.listdir(d)):
            if os.path.isdir(os.path.join(d, f)):
                continue
            ext = os.path.splitext(f)[1].lower().lstrip(".")
            role = {
                "html": "任务要求",
                "docx": "答题卷",
                "ipynb": "练习",
                "csv": "数据",
                "xlsx": "数据",
                "onnx": "模型",
                "jpg": "图片",
                "png": "图片",
                "txt": "标签",
            }.get(ext, "文件")
            if ext == "ipynb":
                # 含填空标记的是练习，否则是 enrich 生成的资料型笔记本
                try:
                    nb = json.load(open(os.path.join(d, f), encoding="utf-8"))
                    text = "".join(
                        "".join(c.get("source", [])) for c in nb["cells"]
                    )
                    role = "练习" if "__________" in text else "资料"
                except Exception:
                    role = "练习"
            files.append((f, role))
        units.append((unit, read_title(d, unit), files))

    groups = {}
    for unit, title, files in units:
        groups.setdefault(unit.split(".")[0], []).append((unit, title, files))

    sections = []
    for g in sorted(groups):
        cards = "".join(build_card(u, t, fs) for u, t, fs in groups[g])
        sections.append(
            f'<h2 class="chapter">第 {g} 章（{g}.x）</h2><div class="grid">{cards}</div>'
        )

    page = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>人工智能训练师（三级）练习导航</title>
<style>
:root {{ --bg:#f6f7f9; --card:#fff; --fg:#1c1e21; --muted:#6b7280; --line:#e5e7eb; --accent:#2563eb; --chip:#eff6ff; }}
@media (prefers-color-scheme: dark) {{
  :root {{ --bg:#0f1115; --card:#171a21; --fg:#e5e7eb; --muted:#9ca3af; --line:#2a2f3a; --accent:#60a5fa; --chip:#17223b; }}
}}
* {{ box-sizing:border-box; margin:0; padding:0; }}
body {{ background:var(--bg); color:var(--fg); font:14px/1.6 "Microsoft YaHei",system-ui,sans-serif; padding:24px 20px 60px; }}
header {{ max-width:1200px; margin:0 auto 8px; }}
h1 {{ font-size:22px; }}
.tip {{ color:var(--muted); margin:6px 0 20px; font-size:13px; }}
.chapter {{ max-width:1200px; margin:28px auto 12px; font-size:16px; color:var(--muted); border-left:3px solid var(--accent); padding-left:10px; }}
.grid {{ max-width:1200px; margin:0 auto; display:grid; grid-template-columns:repeat(auto-fill,minmax(360px,1fr)); gap:14px; }}
.card {{ background:var(--card); border:1px solid var(--line); border-radius:10px; padding:14px 16px; }}
.card-head {{ display:flex; align-items:baseline; gap:10px; margin-bottom:10px; }}
.no {{ background:var(--chip); color:var(--accent); border-radius:6px; padding:2px 8px; font-weight:700; white-space:nowrap; }}
h3 {{ font-size:14px; font-weight:600; }}
.links {{ display:flex; flex-wrap:wrap; gap:6px; }}
.file {{ text-decoration:none; color:var(--fg); border:1px solid var(--line); border-radius:6px; padding:3px 8px; font-size:12px; display:inline-flex; align-items:baseline; gap:6px; }}
.file:hover {{ border-color:var(--accent); }}
.fn {{ color:var(--muted); max-width:150px; overflow:hidden; text-overflow:ellipsis; white-space:nowrap; }}
.jrow {{ margin-top:10px; }}
.jbtn {{ display:inline-block; text-decoration:none; color:var(--accent); border:1px solid var(--accent); border-radius:6px; padding:3px 12px; font-size:12px; margin-right:6px; }}
.jbtn:hover {{ background:var(--chip); }}
.preview {{ margin-top:10px; }}
.preview summary {{ cursor:pointer; color:var(--muted); font-size:12px; user-select:none; }}
.tblwrap {{ overflow-x:auto; max-height:260px; overflow-y:auto; border:1px solid var(--line); border-radius:6px; margin-top:6px; }}
table {{ border-collapse:collapse; font-size:11px; width:100%; }}
th,td {{ border:1px solid var(--line); padding:3px 8px; text-align:left; white-space:nowrap; }}
th {{ background:var(--chip); position:sticky; top:0; }}
</style>
</head>
<body>
<header>
  <h1>📚 人工智能训练师（三级）练习导航</h1>
  <p class="tip">每个单元一个卡片，所有链接在新标签页打开。任务要求（HTML）浏览器打开 · 答题卷（docx）Word 打开 · 练习/数据可经「在 Jupyter 打开 / Jupyter 表格」查看（需 Jupyter 运行于本机 8888 端口）· 数据卡片内附前几行预览。导航页由 scripts/generate_nav.py 生成，素材变动后重新运行即可。</p>
</header>
{"".join(sections)}
</body>
</html>"""

    out = os.path.join(ROOT, OUT)
    with open(out, "w", encoding="utf-8") as f:
        f.write(page)
    print(f"已生成 {OUT}，覆盖 {len(units)} 个单元")


if __name__ == "__main__":
    main()
