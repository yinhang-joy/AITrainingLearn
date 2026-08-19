"""为每个单元生成「合并笔记本」：任务要求 + 数据预览 + 答题卷 全部作为 Markdown 单元格。

用法：python scripts/enrich_notebooks.py（仓库根目录运行）
- 已有 ipynb 的单元：在顶部插入 Markdown 单元格（原练习单元格保持不动）
- 无 ipynb 的单元（1.2.x / 3.1.x / 4.x）：新建笔记本，内容为资料型 Markdown
- 幂等：重跑时先移除上次插入的单元格（标记 <!-- auto:enriched -->）
依赖：pandas（数据预览），openpyxl（xlsx 预览）
"""
import html
import json
import os
import re
import zipfile
from xml.sax.saxutils import unescape as xml_unescape

import pandas as pd

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MAT = os.path.join(ROOT, "人工智能训练师三级上网素材")
MARKER = "<!-- auto:enriched -->"
PREVIEW_ROWS = 8
PREVIEW_COLS = 8
MAX_HTML_CHARS = 5000
MAX_DOCX_CHARS = 4000


def extract_html(path: str):
    """返回 (标题, 正文文本)"""
    raw = ""
    for enc in ("utf-8", "gbk"):
        try:
            with open(path, encoding=enc) as f:
                raw = f.read()
            break
        except (UnicodeDecodeError, OSError):
            continue
    title_m = re.search(r"<title>(.*?)</title>", raw, re.S)
    title = html.unescape(title_m.group(1).strip()) if title_m else ""
    body = re.sub(r"<script.*?</script>", "", raw, flags=re.S)
    body = re.sub(r"<style.*?</style>", "", body, flags=re.S)
    body = re.sub(r"<br\s*/?>|</p>|</li>|</div>|<h[1-6][^>]*>|</h[1-6]>", "\n", body)
    body = re.sub(r"<[^>]+>", "", body)
    body = html.unescape(body).replace("\xa0", " ")
    body = re.sub(r"[ \t\u3000]+", " ", body)
    body = re.sub(r"\n\s*\n+", "\n\n", body).strip()
    return title, body[:MAX_HTML_CHARS]


def extract_docx(path: str) -> str:
    try:
        with zipfile.ZipFile(path) as z:
            xml = z.read("word/document.xml").decode("utf-8", errors="ignore")
    except (KeyError, OSError):
        return ""
    xml = re.sub(r"<w:tab\s*/>", "\t", xml)
    xml = re.sub(r"<w:br\s*/>", "\n", xml)
    xml = re.sub(r"</w:p>", "\n", xml)
    text = re.sub(r"<[^>]+>", "", xml)
    text = xml_unescape(text)
    text = re.sub(r"[ \t\u3000]+", " ", text)
    text = re.sub(r"\n\s*\n+", "\n\n", text).strip()
    return text[:MAX_DOCX_CHARS]


def preview_markdown(path: str) -> str:
    try:
        if path.endswith(".xlsx"):
            df = pd.read_excel(path, nrows=PREVIEW_ROWS)
        else:
            df = None
            for enc in ("utf-8", "gbk"):
                try:
                    df = pd.read_csv(path, nrows=PREVIEW_ROWS, encoding=enc)
                    break
                except UnicodeDecodeError:
                    continue
    except Exception:
        return ""
    if df is None or df.empty:
        return ""
    extra_cols = max(0, df.shape[1] - PREVIEW_COLS)
    df = df.iloc[:, :PREVIEW_COLS]

    def esc(v):
        s = str(v).replace("|", "\\|").replace("\n", " ")
        return s[:40] if len(s) > 40 else s

    head = " | ".join(esc(c) for c in df.columns)
    sep = " | ".join("---" for _ in df.columns)
    rows = [" | ".join(esc(v) for v in r.values) for _, r in df.iterrows()]
    note = f"\n\n*共 {df.shape[1] + extra_cols} 列，预览前 {len(df)} 行*" if extra_cols else ""
    return f"| {head} |\n| {sep} |\n| " + " |\n| ".join(rows) + " |" + note


def md_cell(source: str) -> dict:
    return {
        "cell_type": "markdown",
        "id": __import__("uuid").uuid4().hex[:8],
        "metadata": {},
        "source": [line + "\n" for line in (source + "\n" + MARKER).splitlines()]
        + [""],
    }


def is_enriched_cell(cell: dict) -> bool:
    return MARKER in "".join(cell.get("source", []))


def enrich_unit(unit_dir: str, unit: str) -> None:
    parts = []
    title, body = extract_html(os.path.join(unit_dir, f"{unit}.html"))
    heading = f"# {unit} {title}" if title and not title.startswith(unit) else f"# {unit}"
    parts.append((heading + "\n\n## 📋 任务要求\n\n" + body).strip())
    data_files = sorted(
        f for f in os.listdir(unit_dir) if f.lower().endswith((".csv", ".xlsx"))
    )
    if data_files:
        previews = [preview_markdown(os.path.join(unit_dir, f)) for f in data_files]
        previews = [p for p in previews if p]
        if previews:
            label = " / ".join(f for f, p in zip(data_files, previews) if p)
            parts.append(f"## 🗂 数据预览（{label}）\n\n" + "\n\n---\n\n".join(previews))
    docx = os.path.join(unit_dir, f"{unit}.docx")
    if os.path.exists(docx):
        doc_text = extract_docx(docx)
        if doc_text:
            parts.append(f"## 📝 答题卷内容（{unit}.docx）\n\n" + doc_text)
    if not parts:
        return

    nb_path = os.path.join(unit_dir, f"{unit}.ipynb")
    if os.path.exists(nb_path):
        with open(nb_path, encoding="utf-8") as f:
            nb = json.load(f)
        nb["cells"] = [c for c in nb["cells"] if not is_enriched_cell(c)]
        new_cells = [md_cell(p) for p in parts]
        nb["cells"] = new_cells + nb["cells"]
    else:
        nb = {
            "cells": [md_cell(p) for p in parts],
            "metadata": {
                "kernelspec": {
                    "display_name": "Python 3",
                    "language": "python",
                    "name": "python3",
                },
                "language_info": {"name": "python", "version": "3.11"},
            },
            "nbformat": 4,
            "nbformat_minor": 5,
        }
    with open(nb_path, "w", encoding="utf-8") as f:
        json.dump(nb, f, ensure_ascii=False, indent=1)


def main() -> None:
    units = [
        d
        for d in sorted(os.listdir(MAT))
        if os.path.isdir(os.path.join(MAT, d)) and re.fullmatch(r"\d+\.\d+\.\d+", d)
    ]
    for unit in units:
        enrich_unit(os.path.join(MAT, unit), unit)
    print(f"已处理 {len(units)} 个单元")


if __name__ == "__main__":
    main()
