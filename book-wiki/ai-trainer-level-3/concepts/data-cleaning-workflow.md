# data-cleaning-workflow（数据清洗工作流）

- **来源章节**: 2.1.2
- **定义**: 将原始数据转换为可用于机器学习的高质量数据集的系统化流程
- **标准流程**:
  ```
  ① 数据加载 → ② 缺失值处理 → ③ 重复值处理 → 
  ④ 数据标准化 → ⑤ 特征工程 → ⑥ 数据集划分 → ⑦ 保存输出
  ```
- **各环节要点**:
  1. **数据加载**: `pd.read_excel` / `pd.read_csv`，先用 `head()` / `info()` 探索
  2. **缺失值处理**: `dropna()` 删除 / `fillna()` 填充，记录行数变化
  3. **重复值处理**: `drop_duplicates()`，记录删除数量
  4. **数据标准化**: `StandardScaler` 消除量纲差异，仅对数值型特征
  5. **特征工程**: 选择有效特征 X、设定目标变量 y
  6. **数据集划分**: `train_test_split` 分训练测试集
  7. **保存输出**: `to_csv(index=False)` 保存清洗后数据
- **质量检查清单**:
  - ✓ 无缺失值（`data.isnull().sum()`）
  - ✓ 无重复行（`data.duplicated().sum()`）
  - ✓ 数值特征已标准化
  - ✓ 特征列命名清晰
  - ✓ 训练测试集比例合理
- **⚠️ 关键原则**: 
  - 清洗前先探索，了解数据分布和问题
  - 每步记录变化（行数、列数），便于追溯
  - 清洗后验证数据质量再进入建模
- **关联**: [[pandas-read-excel]] · [[dropna-missing-values]] · [[drop-duplicates]] · [[standard-scaler]] · [[feature-engineering]] · [[train-test-split]]
