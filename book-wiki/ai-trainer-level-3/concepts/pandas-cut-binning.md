# pandas-cut-binning（分组统计与数据分箱）

- **来源章节**: 1.1.1（首次）、1.1.4（深化）
- **定义**: 使用 `pd.cut()` 将连续变量切分为离散区间，配合 `groupby()` 进行分组统计
- **用法**:
  ```python
  # 连续变量 → 离散区间
  age_groups = pd.cut(df['Age'], 
                      bins=[0, 25, 35, 45, 100],
                      labels=['青年', '中年', '中年', '老年'],
                      right=False)
  df['AgeGroup'] = age_groups
  
  # 分组统计
  df.groupby('AgeGroup')['Amount'].agg(['count', 'mean', 'sum'])
  ```
- **参数详解**:
  - `bins`：边界列表（n 个边界 → n-1 个区间）
  - `labels`：区间名称（长度 = len(bins) - 1）
  - `right=True`（默认）：左开右闭 `(a, b]`
  - `right=False`：左闭右开 `[a, b)`
- **⚠️ 考点**: 
  - 题目「18-25 岁」是否包含 18？需要 `right=False`
  - 不加 `right=False` 则边界值会落到上一个区间
  - bins 列表长度 = labels 长度 + 1
- **对比 between()**: 
  - `pd.cut()` 用于**分类**：给每个值打上区间标签
  - `.between()` 用于**过滤**：返回布尔 Series 筛选行
- **关联**: [[groupby-aggregation]] · [[between-filter]] · [[boolean-indexing]]
