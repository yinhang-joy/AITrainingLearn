# groupby-aggregation（分组统计）

- **来源章节**: 1.1.1
- **定义**: 按某列分组后，对其他列做汇总统计（数量/求和/平均）
- **用法**:
  ```python
  df.groupby('BMI_类别')['高风险'].agg(['count', 'sum'])   # 每组人数 + 高风险人数
  df.groupby('BMI_类别')['高风险'].mean()                  # 每组高风险比例
  ```
- **三步**: `groupby('分组列')` → `['统计列']` → `.agg([...])` 或 `.mean()`
- **易错点**: 统计布尔列时 sum=True 的个数（高风险人数），mean=比例；count=行数（患者数）
- **关联**: [[pd-cut-binning]] · [[boolean-mean-ratio]]
