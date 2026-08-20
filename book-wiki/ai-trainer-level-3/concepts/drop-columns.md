# drop-columns（删除指定列）

- **来源章节**: 1.1.2
- **定义**: 删除 DataFrame 中的指定列（无论有无缺失值）
- **用法**:
  ```python
  df.drop(columns=['col1', 'col2'])     # 删除指定列
  df.drop(['col1', 'col2'], axis=1)     # 旧写法（axis=1 表示列）
  df.drop(index=[0, 1, 2])              # 删除指定行
  ```
- **与 `.dropna()` 的区别**:
  - `.drop(columns=[...])` 删除 **你指定的** 列（主动删除）
  - `.dropna()` 删除 **含缺失值（NaN）** 的行/列（自动找 NaN）
  - `.dropna()` **没有** `columns` 参数！
- **⚠️ 易错点**: 
  - ❌ `df.dropna(columns=['col'])` 语法错误（dropna 没有 columns 参数）
  - ✅ `df.drop(columns=['col'])` 删除指定列
  - ✅ `df.dropna(subset=['col'])` 删除该列为 NaN 的行
- **关联**: [[fillna-method]] · [[to-csv]]
