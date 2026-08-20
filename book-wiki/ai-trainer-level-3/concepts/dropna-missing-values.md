# dropna-missing-values（缺失值处理）

- **来源章节**: 1.1.4
- **定义**: 识别并删除包含缺失值（NaN）的记录，保证数据完整性
- **用法**:
  ```python
  data.isnull().sum()    # 统计每列缺失值数量
  data = data.dropna()   # 删除任意列有 NaN 的行
  ```
- **参数**: 
  - `how='any'`（默认）：任意列有 NaN 就删除该行
  - `how='all'`：所有列都是 NaN 才删除
  - `subset=['col1', 'col2']`：只检查指定列
- **对比填充方法**: 
  - `dropna()` 删除缺失值（数据量减少）
  - `fillna()` 填充缺失值（数据量不变，1.1.2 已学）
- **易错点**: 删除后原 DataFrame 不变，需要重新赋值 `data = data.dropna()`
- **关联**: [[fillna-method]] · [[data-read-and-view]]
