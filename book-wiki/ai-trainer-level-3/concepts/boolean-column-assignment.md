# boolean-column-assignment（布尔列赋值 / 异常值标记）

- **来源章节**: 1.1.2
- **定义**: 用布尔表达式创建新列，每行是 True/False，用于标记异常值、分类等
- **用法**:
  ```python
  # 单条件标记
  df['Anomaly'] = df['Value'] > 50
  
  # 多条件标记（温度 > 50 或湿度 > 100）
  df['Anomaly'] = ((df['SensorType'] == 'Temperature') & (df['Value'] > 50)) | \
                  ((df['SensorType'] == 'Humidity') & (df['Value'] > 100))
  
  # 统计异常数量
  df['Anomaly'].sum()   # True=1、False=0，求和 = 异常行数
  ```
- **⚠️ 易错点（考点）**: 
  - 复杂条件**必须加括号**，因为 `&` / `|` 优先级高于 `==` / `>`
  - ❌ `df['A'] > 10 & df['B'] < 5` 逻辑错误
  - ✅ `(df['A'] > 10) & (df['B'] < 5)` 正确
- **关联**: [[boolean-indexing]] · [[boolean-mean-ratio]]
