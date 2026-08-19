# boolean-mean-ratio（布尔列求平均 = 占比）

- **来源章节**: 1.1.1
- **定义**: 对布尔列取 `.mean()`，因 True=1 / False=0，平均值即条件成立的比例
- **用法**:
  ```python
  (df['DaysInHospital'] > 7).mean()   # → 0.426，即 42.6%
  ```
- **易错点**: 比较表达式外面要加括号再 `.mean()`；与 `len(筛选)/len(df)` 等价
- **关联**: [[boolean-indexing]] · [[groupby-aggregation]]
