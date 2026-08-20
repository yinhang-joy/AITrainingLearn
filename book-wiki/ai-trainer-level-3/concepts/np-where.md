# np-where（条件赋值）

- **来源章节**: 1.1.1, 1.1.2
- **定义**: 根据条件返回不同的值（类似三元运算符 `条件 ? 值1 : 值2`）
- **用法**:
  ```python
  np.where(条件, 条件为True时的值, 条件为False时的值)
  
  # 1.1.1 示例：字符串分类
  df['RiskLevel'] = np.where(df['DaysInHospital'] > 7, '高风险患者', '低风险患者')
  
  # 1.1.2 示例：布尔标记
  df['is_abnormal'] = np.where(
      (df['SensorType'] == 'Temperature') & (df['Value'] > 50),
      True, False
  )
  ```
- **与直接布尔赋值的区别**:
  ```python
  # 方式1：np.where（更明确）
  df['Anomaly'] = np.where(df['Value'] > 50, True, False)
  
  # 方式2：直接布尔表达式（结果相同，更简洁）
  df['Anomaly'] = df['Value'] > 50
  ```
  - 当结果是 **字符串/数字** 时，必须用 `np.where`
  - 当结果是 **True/False** 时，两种都可以，布尔表达式更简洁
- **多条件嵌套**:
  ```python
  # 三种情况：高/中/低
  df['Level'] = np.where(df['Value'] > 80, '高',
                np.where(df['Value'] > 50, '中', '低'))
  ```
- **⚠️ 易错点**: 复杂条件必须加括号（和布尔索引一样）
- **关联**: [[boolean-column-assignment]] · [[boolean-indexing]]
