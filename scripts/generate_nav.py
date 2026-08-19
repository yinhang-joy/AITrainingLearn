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
BOOK_WIKI = os.path.join("book-wiki", "ai-trainer-level-3")
RENDERED_DIR = os.path.join(BOOK_WIKI, "rendered")
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


def md_inline(text: str) -> str:
    """行内 md：`code` **bold** [[wiki链接]]"""
    text = html.escape(text, quote=False)
    text = re.sub(r"`([^`]+)`", r"<code>\1</code>", text)
    text = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(
        r"\[\[([^\]]+)\]\]", r'<span class="wikilink">\1</span>', text
    )
    return text


def md_to_html(src: str) -> str:
    """轻量 md→HTML（支持标题/代码块/表格/列表/引用/原始HTML/details），
    只覆盖 book-wiki 文档用到的格式子集。"""
    parts, i = [], 0
    lines = src.split("\n")
    in_code = in_list = in_table = False
    buf, head_done = [], False

    def close_block():
        nonlocal in_code, in_list, in_table, buf, head_done
        if in_code:
            parts.append("<pre><code>" + html.escape("\n".join(buf)) + "</code></pre>")
            buf, in_code = [], False
        if in_list:
            parts.append("</ul>")
            in_list = False
        if in_table:
            parts.append("</tbody></table>")
            in_table, head_done = False, False

    while i < len(lines):
        line = lines[i]
        s = line.strip()
        if s.startswith("```"):
            if in_code:
                parts.append("<pre><code>" + html.escape("\n".join(buf)) + "</code></pre>")
                buf, in_code = [], False
            else:
                in_code = True
            i += 1
            continue
        if in_code:
            buf.append(line)
            i += 1
            continue
        if s == "":
            close_block()
            i += 1
            continue
        if s.startswith(("<details", "</details", "<summary", "</summary")):
            close_block()
            parts.append(s)
            i += 1
            continue
        m = re.match(r"^(#{1,4})\s+(.*)", s)
        if m:
            close_block()
            lv = len(m.group(1)) + 2  # #→h3（卡片内层级）
            parts.append(f"<h{lv}>{md_inline(m.group(2))}</h{lv}>")
            i += 1
            continue
        if s == "---":
            close_block()
            parts.append("<hr>")
            i += 1
            continue
        if s.startswith("|") and s.endswith("|"):
            cells = [c.strip() for c in s.strip("|").split("|")]
            if not in_table:
                parts.append("<table class='md'><thead><tr>")
                parts.append("".join(f"<th>{md_inline(c)}</th>" for c in cells))
                parts.append("</tr></thead><tbody>")
                in_table, head_done = True, False
            else:
                if all(re.fullmatch(r":?-{2,}:?", c) for c in cells):
                    i += 1
                    continue
                parts.append("<tr>" + "".join(f"<td>{md_inline(c)}</td>" for c in cells) + "</tr>")
            i += 1
            continue
        if s.startswith(("- ", "* ")):
            if not in_list:
                close_block()
                parts.append("<ul>")
                in_list = True
            parts.append(f"<li>{md_inline(s[2:])}</li>")
            i += 1
            continue
        if s.startswith(("> ", ">")):
            if not in_list and not in_table:
                pass
            parts.append(f"<blockquote>{md_inline(s.lstrip('> '))}</blockquote>")
            i += 1
            continue
        close_block()
        parts.append(f"<p>{md_inline(s)}</p>")
        i += 1
    close_block()
    return "\n".join(parts)


def render_standalone_lecture(unit: str, lecture_title: str, lecture_body: str, concepts: list) -> str:
    """生成独立讲义HTML页面（含知识点卡片）"""
    concept_section = ""
    if concepts:
        cards = "".join(
            f'<section class="concept-card"><h3>{html.escape(name)}</h3><div class="content">{body}</div></section>'
            for name, _, _, body in concepts
        )
        concept_section = f'<section class="concepts"><h2>知识点卡片</h2>{cards}</section>'

    return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(unit)} {html.escape(lecture_title)}</title>
<style>
:root {{ --bg:#fff; --fg:#1a1a1a; --line:#e5e5e5; --muted:#737373; --accent:#2563eb; --chip:#f5f5f5; }}
@media (prefers-color-scheme:dark) {{ :root:not([data-theme="light"]) {{ --bg:#0a0a0a; --fg:#ededed; --line:#262626; --muted:#a3a3a3; --accent:#60a5fa; --chip:#1a1a1a; }} }}
:root[data-theme="dark"] {{ --bg:#0a0a0a; --fg:#ededed; --line:#262626; --muted:#a3a3a3; --accent:#60a5fa; --chip:#1a1a1a; }}
* {{ margin:0; padding:0; box-sizing:border-box; }}
body {{ background:var(--bg); color:var(--fg); font-family:system-ui,-apple-system,sans-serif; line-height:1.6; padding:20px; max-width:900px; margin:0 auto; }}
h1 {{ font-size:24px; margin:0 0 20px; padding-bottom:10px; border-bottom:2px solid var(--line); }}
h2 {{ font-size:20px; margin:24px 0 12px; color:var(--accent); }}
h3 {{ font-size:17px; margin:16px 0 8px; }}
h4 {{ font-size:15px; margin:12px 0 6px; }}
h5 {{ font-size:14px; margin:10px 0 4px; }}
p {{ margin:8px 0; }}
ul {{ margin:8px 0 8px 24px; }}
li {{ margin:3px 0; }}
pre {{ background:var(--chip); border:1px solid var(--line); border-radius:8px; padding:12px; overflow-x:auto; margin:12px 0; }}
code {{ font-family:Consolas,Monaco,monospace; font-size:13px; }}
p code {{ background:var(--chip); padding:2px 6px; border-radius:4px; }}
table {{ border-collapse:collapse; margin:12px 0; font-size:14px; width:100%; }}
th, td {{ border:1px solid var(--line); padding:6px 12px; text-align:left; }}
th {{ background:var(--chip); font-weight:600; }}
blockquote {{ border-left:4px solid var(--accent); margin:12px 0; padding:4px 14px; color:var(--muted); background:var(--chip); }}
hr {{ border:none; border-top:1px solid var(--line); margin:20px 0; }}
details summary {{ cursor:pointer; color:var(--accent); font-weight:500; user-select:none; }}
.wikilink {{ color:var(--accent); }}
.concepts {{ margin-top:40px; padding-top:20px; border-top:2px solid var(--line); }}
.concept-card {{ border:1px solid var(--line); border-radius:8px; padding:16px; margin:16px 0; background:var(--chip); }}
.concept-card h3 {{ margin-top:0; color:#9333ea; }}
.content > *:first-child {{ margin-top:0; }}
.content > *:last-child {{ margin-bottom:0; }}
</style>
</head>
<body>
<h1>{html.escape(unit)} {html.escape(lecture_title)}</h1>
<div class="lecture-body">{lecture_body}</div>
{concept_section}
</body>
</html>"""


def load_learning_materials() -> dict:
    """扫描 book-wiki 学习材料，返回 {unit: {lecture, concepts, rendered_path}}"""
    os.makedirs(os.path.join(ROOT, RENDERED_DIR), exist_ok=True)
    out = {}
    lect_dir = os.path.join(ROOT, BOOK_WIKI, "lectures")
    if os.path.isdir(lect_dir):
        for f in sorted(os.listdir(lect_dir)):
            if not f.endswith(".md"):
                continue
            m = re.match(r"(\d+\.\d+\.\d+)-", f)
            if not m:
                continue
            unit = m.group(1)
            ltitle = os.path.splitext(f)[0].split("-", 1)[1] if "-" in f else f
            rel = os.path.join(BOOK_WIKI, "lectures", f).replace("\\", "/")
            body = md_to_html(open(os.path.join(ROOT, rel), encoding="utf-8").read())
            out.setdefault(unit, {})["lecture"] = (rel, ltitle, body)
    conc_dir = os.path.join(ROOT, BOOK_WIKI, "concepts")
    if os.path.isdir(conc_dir):
        for f in sorted(os.listdir(conc_dir)):
            if not f.endswith(".md"):
                continue
            text = open(os.path.join(conc_dir, f), encoding="utf-8").read()
            m = re.search(r"\*\*来源章节\*\*:\s*(\d+\.\d+\.\d+)", text)
            if not m:
                continue
            dm = re.search(r"\*\*定义\*\*:\s*(.+)", text)
            summary = html.unescape(dm.group(1).strip()) if dm else ""
            name = os.path.splitext(f)[0]
            rel = os.path.join(BOOK_WIKI, "concepts", f).replace("\\", "/")
            body = md_to_html(text)
            out.setdefault(m.group(1), {}).setdefault("concepts", []).append(
                (name, rel, summary, body)
            )
    # 生成独立HTML页面
    for unit, data in out.items():
        if "lecture" in data:
            _, ltitle, lbody = data["lecture"]
            concepts = data.get("concepts", [])
            html_content = render_standalone_lecture(unit, ltitle, lbody, concepts)
            rendered_path = os.path.join(RENDERED_DIR, f"{unit}.html")
            open(os.path.join(ROOT, rendered_path), "w", encoding="utf-8").write(html_content)
            data["rendered_path"] = rendered_path.replace("\\", "/")
    return out


def build_card(unit: str, title: str, files, learning=None) -> str:
    links, previews, jbtns = [], [], []
    if learning and "rendered_path" in learning:
        _, ltitle, _ = learning["lecture"]
        rpath = learning["rendered_path"]
        links.append(
            f'<a href="{html.escape(rpath)}" target="_blank" class="file lect" '
            f'title="讲义+知识点完整页面">📖 讲义<span class="fn">{html.escape(ltitle)}</span></a>'
        )
    has_ipynb = False
    for f, role in files:
        rel = os.path.join(MAT, unit, f).replace("\\", "/")
        if f.endswith(".ipynb"):
            has_ipynb = True
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
    if has_ipynb:
        jbtns.append(
            f'<button class="jbtn reset" onclick="resetNotebook(\'{unit}\')">🔄 重置</button>'
        )
    jrow = f'<div class="jrow">{"".join(jbtns)}</div>' if jbtns else ""
    return f"""<section class="card">
      <div class="card-head"><span class="no">{unit}</span><h3>{html.escape(title)}</h3></div>
      <div class="links">{"".join(links)}</div>
      {jrow}
      {"".join(previews)}
    </section>"""


def main() -> None:
    learning = load_learning_materials()
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
        cards = "".join(
            build_card(u, t, fs, learning.get(u)) for u, t, fs in groups[g]
        )
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
.jbtn {{ display:inline-block; text-decoration:none; color:var(--accent); border:1px solid var(--accent); border-radius:6px; padding:3px 12px; font-size:12px; margin-right:6px; background:transparent; cursor:pointer; font-family:inherit; }}
.jbtn:hover {{ background:var(--chip); }}
.jbtn.reset {{ border-color:#ef4444; color:#ef4444; }}
.jbtn.reset:hover {{ background:#fef2f2; }}
.lect {{ border-color:#9333ea; color:#9333ea; }}
.lect:hover {{ background:#faf5ff; }}
details.preview {{ margin-top:10px; }}
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
<script>
function resetNotebook(unit) {{
  if (!confirm(`确定要重置 ${{unit}} 的练习笔记本吗?\\n已填写的内容将被清空，恢复为原始填空状态。`)) return;
  fetch('http://localhost:8765/reset', {{
    method: 'POST',
    headers: {{'Content-Type': 'application/json'}},
    body: JSON.stringify({{unit: unit}})
  }})
  .then(r => r.json())
  .then(d => {{
    if (d.success) alert(`✅ ${{unit}} 重置成功\\n${{d.message}}`);
    else alert(`❌ 重置失败\\n${{d.error}}`);
  }})
  .catch(e => alert(`❌ 请求失败\\n${{e.message}}\\n\\n请确保 Python 重置服务已启动:\\npython scripts/reset_service.py`));
}}
</script>
</body>
</html>"""

    out = os.path.join(ROOT, OUT)
    with open(out, "w", encoding="utf-8") as f:
        f.write(page)
    print(f"已生成 {OUT}，覆盖 {len(units)} 个单元")


if __name__ == "__main__":
    main()
