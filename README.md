# 人工智能训练师（三级）备考素材

「人工智能训练师（三级）」职业技能等级考试的官方训练素材与练习环境。本仓库包含全部素材（含 ONNX 模型文件），**克隆后即可离线做题**，无需再下载任何素材。

## 目录

- `人工智能训练师三级上网素材/` — 官方训练素材：ipynb 填空练习、docx 答题卷、数据集（csv/xlsx）、ONNX 模型（3.2.x 部署练习用）
- `人工智能训练师三级考试平台模拟界面/` — 考试平台模拟界面存档（HTML，与素材包任务编号一一对应）

## 新设备快速开始

1. 安装 Python 3.11+ 与 [uv](https://docs.astral.sh/uv/)（包管理器）
2. 创建虚拟环境并安装依赖：

   ```
   uv venv .venv
   uv pip install -r requirements.txt
   ```

3. 启动 Jupyter：

   - Windows：`.venv\Scripts\jupyter-lab.exe`
   - macOS/Linux：`.venv/bin/jupyter-lab`

## 说明

- 素材内 ipynb 为官方原样保留的填空练习（空格处填答案）；1.1.x 分格，多数任务为单格整段代码
- 本仓库含约 230 MB 模型文件，clone 体积较大属正常
- 环境依赖清单见 `requirements.txt`（虚拟环境本身不纳入版本管理）
