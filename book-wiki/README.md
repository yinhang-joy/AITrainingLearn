# book-wiki 使用指南

这是你的**做题工具库**，不是课本，不是笔记本。

## 📚 目录结构

```
book-wiki/ai-trainer-level-3/
├── quick-ref/          ⭐ 速查手册（做题时翻这里）
│   ├── 数据筛选.md      - 布尔索引、between、isin
│   ├── 数据清洗.md      - dropna、fillna、duplicated
│   ├── 数据转换.md      - astype、cut、StandardScaler
│   ├── 数据聚合.md      - groupby、value_counts
│   ├── 数据保存.md      - to_csv、to_excel
│   └── 特征工程.md      - train_test_split、StandardScaler
│
├── concepts/           ⭐ 概念卡片（某个方法不会用时查）
│   ├── train_test_split.md
│   ├── StandardScaler.md
│   └── pd-cut.md
│
├── errors/             ⭐ 错误字典（遇到报错时查）
│   ├── TypeError.md
│   ├── ValueError.md
│   ├── KeyError.md
│   └── AttributeError.md
│
├── mastery-map.md      - 进度追踪（完成单元后更新）
└── lectures/           - 讲义备份（备用，不常看）
```

## 🎯 使用场景

### 1️⃣ 做题时忘记语法 → 查 **quick-ref/**

**例**：忘记 `groupby` 怎么写
```bash
# 打开 book-wiki/ai-trainer-level-3/quick-ref/数据聚合.md
# 快速找到示例代码，复制粘贴
```

### 2️⃣ 遇到新概念不理解 → 查 **concepts/**

**例**：不知道 `train_test_split` 四个返回值是什么
```bash
# 打开 book-wiki/ai-trainer-level-3/concepts/train_test_split.md
# 查看参数说明、返回值表格、示例代码
```

### 3️⃣ 代码报错不知道怎么改 → 查 **errors/**

**例**：遇到 `TypeError: fit_transform() missing 1 required positional argument`
```bash
# 打开 book-wiki/ai-trainer-level-3/errors/TypeError.md
# 找到"缺少必需参数"章节，对照错误代码和正确代码
```

### 4️⃣ 完成单元后记录进度 → 更新 **mastery-map.md**

```bash
# 我会帮你更新，你不用手动操作
```

---

## ✅ 与旧版本对比

| 旧版 book-wiki | 新版 book-wiki |
|----------------|----------------|
| ❌ 讲义太长，不想看 | ✅ 速查手册，一页搞定 |
| ❌ 做完题写日记 | ✅ 做题时实时查询 |
| ❌ 概念列表没用法 | ✅ 概念卡片有示例 |
| ❌ 没有错误排查 | ✅ 错误字典快速定位 |

---

## 🚀 下次做题流程

1. 打开 `练习导航.html`，找到单元
2. 打开 Jupyter，加载 `X.ipynb`
3. **遇到不会的 → 打开 `book-wiki/quick-ref/`**
4. **报错了 → 打开 `book-wiki/errors/`**
5. 做完后发消息："X.X.X 已完成，检查答案"

---

现在你觉得 book-wiki 有用了吗？还有什么需要补充的？
