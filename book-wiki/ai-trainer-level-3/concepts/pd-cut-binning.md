# pd-cut-binning（区间切分）

- **来源章节**: 1.1.1
- **定义**: 把连续数值（如 BMI）按边界切成多个区间类别
- **用法**:
  ```python
  df['BMI_类别'] = pd.cut(df['BMI'], bins=[0, 18.5, 24.0, 28.0, 100],
                          labels=['偏瘦', '正常', '超重', '肥胖'], right=False)
  ```
- **参数**: `bins` 边界列表（n 个边界 → n-1 个区间）；`labels` 区间名；`right=False` 左闭右开 `[a, b)`
- **⚠️ 易错点（考点）**: 默认是左开右闭 `(a, b]`，边界值 18.5 会被算进前一个区间「偏瘦」；题目定义「正常 18.5～23.9」必须 `right=False` 才让 18.5 归「正常」
- **关联**: [[groupby-aggregation]] · [[boolean-mean-ratio]]
