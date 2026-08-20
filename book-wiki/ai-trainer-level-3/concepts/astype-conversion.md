# astype-conversion（数据类型转换）

- **来源章节**: 1.1.4
- **定义**: 将 DataFrame 列转换为正确的数据类型（整型、浮点型、字符串）
- **用法**:
  ```python
  df['Age'] = df['Age'].astype(int)      # 浮点 → 整型
  df['Amount'] = df['Amount'].astype(float)  # 字符串 → 浮点
  ```
- **常用类型**:
  - `int` / `'int64'`：整型
  - `float` / `'float64'`：浮点型
  - `str` / `'object'`：字符串
- **⚠️ 易错点**: 
  - 浮点转整型**截断小数**（不是四舍五入）：`89.9 → 89`
  - 四舍五入需要先 `round()`：`df['col'].round().astype(int)`
  - 转换前检查合法性：`'abc'.astype(float)` 会报错
- **关联**: [[dropna-missing-values]] · [[between-filter]]
