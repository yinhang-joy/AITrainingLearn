# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 目录性质

「人工智能训练师（三级）」职业技能等级考试的备考工作区，**已是 git 仓库**，远端为 GitHub private 仓库 `git@github.com:yinhang-joy/AITrainingLearn.git`（无 gh CLI，推送用 git 命令即可）。

官方素材压缩包已解压入库，源压缩包、Anaconda 安装包、VMware 安装包已删除本地不保留（均 gitignore，如重新下载回来也不会被追踪）。

## 目录结构

- `练习导航.html` — **总入口**：40 个单元卡片，每卡链接到该单元的任务要求/答题卷/练习/数据，含「在 Jupyter 打开」按钮（需 Jupyter 运行中）
- `人工智能训练师三级上网素材/` — 官方训练素材，按「章.节.任务」编号**一个单元一个文件夹**（如 `2.1.3/`），每单元内含：
  - `X.html` 任务要求（原考试平台模拟界面，已并入对应单元）· `X.docx` 答题卷 · `X.ipynb` 练习 · 数据集 · ONNX 模型（3.2.x）
  - **1.x**：pandas/numpy 数据分析填空练习（ipynb + CSV 数据集）；1.2.x 仅 docx 答题卷
  - **2.x**：docx 任务书 + ipynb + 数据集（含 Label Studio 标注、随机森林等模型训练）
  - **3.1.x**：docx + xlsx 领域数据集；**3.2.x**：ONNX 模型部署推理练习（resnet/mnist/emotion-ferplus/flower-detection/version-RFB-320）
  - **4.x**：仅 docx 答题卷
- `.venv/` — uv 虚拟环境（CPython 3.11，gitignore），依赖见 `requirements.txt`
- `README.md` — 新设备快速开始说明

## 常用操作

- 启动 Jupyter：`E:\AITraining\.venv\Scripts\jupyter-lab.exe`（根目录为仓库根）
- 重建环境：`uv venv .venv && uv pip install -r requirements.txt`
- 日常提交：`git add -A; git commit -m "说明"; git push`（首次 clone 后 main 已跟踪 origin/main）
- 快速读 docx 文本（不装 Office 时）：`unzip -p <file>.docx word/document.xml | sed 's/<[^>]*>/ /g'`

## 任务文件的约定（帮用户做题时遵守）

- 做题流程：`练习导航.html` 找到单元 → 看同文件夹内 `X.html` 任务要求 → 做 `X.ipynb` → 答 `X.docx`（如需）。
- **ipynb 是填空题**：答案处留 `_____________`，旁边标分值（如 `# 3分`）。填空而非重写单元格；多数任务为单格整段代码（仅 1.1.x 真分格），可在 Jupyter 里用 Split Cell 拆分。
- **docx 是答题卷**：卷面标注「请勿修改答题卷，在指定单元格内填写答案」。

## 注意事项

- 仓库含约 130 MB（.git 压缩后）大文件 —— 5 个 onnx 模型共 231 MB 用普通 git 硬推（非 LFS），GitHub 会给 98 MB 的两个文件挂警告属正常。
- gitignore 排除：`.venv/`、`*.rar`、`Anaconda3-*.exe`、`vm15pro_99970*`、`__pycache__/`、`*.pyc`、`.ipynb_checkpoints/`。
- **本机网络**：GitHub 22 端口被墙，`~/.ssh/config` 已把 `github.com` 路由到 `ssh.github.com:443`；新设备推送前需同样配置（或改 HTTPS remote）。
- 素材内中文文件名在 git/控制台输出中显示为 C 风格转义（如 `"\344\272\272..."`），是正常现象，不是乱码文件。
