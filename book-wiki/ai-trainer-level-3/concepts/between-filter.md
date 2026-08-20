# between-filter（异常值检测与过滤）

- **来源章节**: 1.1.4
- **定义**: 使用 `.between()` 方法检查值是否在合理区间内，过滤异常数据
- **用法**:
  ```python
  valid = df['Age'].between(18, 80)   # 返回布尔 Series
  df_clean = df[valid]                # 保留 True 的行
  # 多条件组合：
  df[(df['Age'].between(18, 80)) & (df['Amount'].between(0, 10000))]
  ```
- **参数**: 
  - `left`, `right`：左右边界
  - `inclusive='both'`（默认）：包含两端 `[left, right]`
  - `inclusive='neither'`：不含两端 `(left, right)`
  - `inclusive='left'` / `'right'`：只含一端
- **对比 pd.cut()**: 
  - `between()` 用于**过滤**：保留范围内的行
  - `pd.cut()` 用于**分类**：给每行打上区间标签
- **⚠️ 易错点**: 多条件组合必须每个条件都加括号：`(cond1) & (cond2)`
- **关联**: [[boolean-indexing]] · [[pandas-cut-binning]]
