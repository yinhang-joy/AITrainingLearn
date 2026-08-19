# boolean-indexing（布尔索引筛选）

- **来源章节**: 1.1.1
- **定义**: 用布尔序列（True/False）筛选 DataFrame 的行 —— `df[布尔序列]` 只留下 True 的行
- **用法**:
  ```python
  df[df['DaysInHospital'] > 7]   # 留住院>7天的行
  ```
- **机制**: `df['列'] > 7` 先逐行比较生成布尔列；`df[...]` 里放字符串=取列，放布尔序列=筛行
- **易错点**: 比较运算的括号；筛选变量可复用（如 high_risk）
- **关联**: [[boolean-mean-ratio]] · [[pandas-read-csv]]
