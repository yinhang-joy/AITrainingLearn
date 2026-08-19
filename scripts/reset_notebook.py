#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""重置 ipynb 到原始填空状态（从 git 恢复）"""
import subprocess, sys, os

if len(sys.argv) < 2:
    print("用法: python reset_notebook.py 1.1.1")
    print("      python reset_notebook.py 1.1.1 2.1.3  （可同时重置多个）")
    sys.exit(1)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)

for unit in sys.argv[1:]:
    path = f"人工智能训练师三级上网素材/{unit}/{unit}.ipynb"
    if not os.path.exists(path):
        print(f"❌ {unit}: 文件不存在 {path}")
        continue
    try:
        subprocess.run(["git", "restore", path], check=True, capture_output=True, text=True)
        print(f"✅ {unit}: 已重置为原始填空状态")
    except subprocess.CalledProcessError as e:
        print(f"❌ {unit}: git restore 失败 — {e.stderr.strip()}")
