# dropna-missing-values（缺失值处理）

- **来源章节**: 2.1.2
- **定义**: 删除 DataFrame 中包含缺失值（NaN）的行或列，保证数据完整性
- **用法**:
  ```python
  initial_count = len(data)
  data = data.dropna()              # 删除任何列有缺失的行
  final_count = len(data)
  print(f'删除行数: {initial_count - final_count}')
  ```
- **参数**:
  - 默认：删除任何列有 NaN 的行
  - `axis=1`：删除包含 NaN 的列
  - `how='all'`：仅当整行/列全是 NaN 才删除
  - `subset=['列1', '列2']`：仅检查指定列
- **⚠️ 易错点**: `dropna()` 返回新 DataFrame，必须重新赋值 `data = data.dropna()`；直接调用不会改变原数据
- **替代方案**: `fillna(值)` 填充、`interpolate()` 插值（时间序列）
- **关联**: [[drop-duplicates]] · [[data-cleaning-workflow]] · [[pandas-read-excel]]
