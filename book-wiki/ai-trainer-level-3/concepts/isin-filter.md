# isin-filter（多值筛选）

- **来源章节**: 1.1.2
- **定义**: 筛选某列的值在指定列表里的行 —— 比多个 `==` 或条件简洁
- **用法**:
  ```python
  df[df['SensorType'].isin(['Temperature', 'Humidity'])]
  # 等价于（但更简洁）：
  df[(df['SensorType'] == 'Temperature') | (df['SensorType'] == 'Humidity')]
  ```
- **参数**: `.isin([列表])` —— 必须是列表，不能直接传多个参数
- **⚠️ 易错点**: 
  - ❌ `.isin('A', 'B')` 语法错误（isin 只接受一个参数）
  - ✅ `.isin(['A', 'B'])` 必须用列表包裹
- **关联**: [[boolean-indexing]] · [[groupby-aggregation]]
