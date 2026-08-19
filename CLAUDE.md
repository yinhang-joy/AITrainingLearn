# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 目录性质

这不是代码仓库，而是「人工智能训练师（三级）」职业技能等级考试的备考工作区。没有 git、构建脚本、测试或 CI。两个素材压缩包已解压到同名目录：`人工智能训练师三级上网素材/`（40 个编号任务目录）和 `人工智能训练师三级考试平台模拟界面/`（40 个 HTML）。Python 环境是 uv 管理的 `.venv/`（不用 Anaconda）。

## 文件清单与用途

- `人工智能训练师三级上网素材.rar`（221 MiB，RAR5，无密码）— 官方训练素材，解压后根目录为 `人工智能训练师三级上网素材/`，按「章.节.任务」三级编号组织（每个编号一个子目录）：
  - **1.1.x**（1.1.1–1.1.5）：Jupyter 填空练习（pandas/numpy 数据分析），每任务配一个 CSV 数据集（patient_data、sensor_data、credit_data、user_behavior_data、vehicle_traffic_data）
  - **1.2.x**：仅 docx 答题卷
  - **2.x**（2.1.x / 2.2.x）：docx 任务书 + ipynb + 数据集（auto-mpg、finance、fitness analysis、medical 等；涉及 Label Studio 数据标注、随机森林等模型训练）
  - **3.1.x**：docx + xlsx 领域数据集（智能家居/教育/金融等）
  - **3.2.x**：ONNX 模型部署推理练习（resnet、mnist、emotion-ferplus、flower-detection、version-RFB-320 人脸检测）。注意 3.2.1 的 `resnet.onnx` 约 102 MB
  - **4.x**：仅 docx 答题卷
- `人工智能训练师三级考试平台模拟界面.rar`（318 KiB）— 考试平台模拟界面的离线存档，每个考核任务一个 HTML（1.1.1 到 4.2.5，与素材包编号一一对应）。HTML 的 `<title>` 即任务名称（如「2.2.3 日常运动量随机森林预测模型开发与测试」），正文含考核任务要求（设备环境、任务描述、考试结果）。**这是了解每个编号任务实际考核内容的第一手参考。**
- `Anaconda3-2025.06-1-Windows-x86_64.exe` — Python/Jupyter 环境安装包（跑 ipynb 需要）
- `vm15pro_99970/` 与 `vm15pro_99970.zip` — VMware Workstation 15.5.7 安装包（来自非官方下载站，安装有风险自担）

## 常用操作

- 运行 ipynb：用 `.venv` 里的 Jupyter —— `E:\AITraining\.venv\Scripts\jupyter-lab.exe`（依赖已装齐：pandas、numpy、scipy、Pillow、onnxruntime、scikit-learn、openpyxl）。素材包内残留 `__pycache__/box_utils_numpy.cpython-39.pyc`，说明官方编写环境是 Python 3.9，本地 3.12 无碍。
- 重建环境：`cd E:\AITraining && uv venv .venv && uv pip install -p .venv jupyterlab pandas numpy scipy pillow onnxruntime scikit-learn openpyxl`
- 快速读 docx 文本（不装 Office 时）：`unzip -p <file>.docx word/document.xml | sed 's/<[^>]*>/ /g'`
- 解压/更新素材包（7-Zip 在 `C:\Program Files\7-Zip\7z.exe`）：
  ```
  "C:\Program Files\7-Zip\7z.exe" x "E:\AITraining\<压缩包>.rar" -o"E:\AITraining"
  ```

## 任务文件的约定（帮助用户做题时遵守）

- **ipynb 是填空题**：代码单元已给出，答案处留 `_____________` 空白，每题旁边标注分值（如 `# 3分`）。帮用户完成时应填空而非重写单元格。
- **docx 是答题卷**：卷面标注「请勿修改答题卷，在指定单元格内填写答案」。
- **编号跨包对应**：先打开模拟界面包中同编号的 HTML 看官方任务要求，再回到素材包对应目录做题。

## 注意事项

- 素材包内中文文件名是 GBK 编码，7z 命令行在某些 shell 下列目录会乱码（编号路径不受影响）；用资源管理器或 PowerShell 操作最省事。
- 解压后的素材与 `.venv/` 都在本目录内；将来若 git 管理本目录，必须 gitignore：`Anaconda3-*.exe`、`vm15pro_99970.zip`、两个 `.rar`、`.venv/`、以及素材里约 98 MB 的 `3.2.1/resnet.onnx`（接近 GitHub 100 MB 上限）。
