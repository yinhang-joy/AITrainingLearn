# fillna-method（缺失值填充）

- **来源章节**: 1.1.2
- **定义**: 用前面或后面的值填充 NaN（缺失值），而非固定值
- **用法**:
  ```python
  df['Value'].fillna(method='ffill')   # 前向填充（用前面的值）
  df['Value'].fillna(method='bfill')   # 后向填充（用后面的值）
  # 链式调用（考试常用）：
  df['Value'].fillna(method='ffill').fillna(method='bfill')
  ```
- **参数**: `method='ffill'`（前向，别名 `'pad'`）/ `method='bfill'`（后向，别名 `'backfill'`）
- **⚠️ 易错点**: 
  - `ffill` 无法填充第一行的 NaN（前面没有值）
  - `bfill` 无法填充最后一行的 NaN（后面没有值）
  - 链式调用可以覆盖首尾：先 ffill 填中间，再 bfill 补首尾
- **关联**: [[isin-filter]] · [[to-csv]]
