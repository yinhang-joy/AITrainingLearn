# pd.cut

## 一句话说明

将连续数值数据分箱（分组），转换为离散的类别标签。

## 语法

```python
pd.cut(
    x,                    # 要分箱的数据
    bins,                 # 分箱边界或箱数
    labels=None,          # 自定义标签
    right=True,           # 是否右闭合
    include_lowest=False  # 是否包含最小值
)
```

## 参数说明

| 参数 | 说明 | 示例 |
|------|------|------|
| `bins` | 分箱边界列表或箱数 | `[0, 18, 35, 60, 100]` 或 `5` |
| `labels` | 自定义标签（可选） | `['青少年', '青年', '中年', '老年']` |
| `right` | 是否右闭合（默认 True） | `True`: `(0, 18]`，`False`: `[0, 18)` |
| `include_lowest` | 是否包含最小值 | `True`: 第一个区间左闭 |

## 示例

### 基本用法（指定边界）

```python
import pandas as pd

ages = [5, 12, 18, 25, 35, 45, 65, 80]

# 按年龄段分组
age_groups = pd.cut(
    ages,
    bins=[0, 18, 35, 60, 100],
    labels=['青少年', '青年', '中年', '老年']
)

print(age_groups)
# [青少年, 青少年, 青年, 青年, 中年, 中年, 老年, 老年]
```

### right 参数（区间开闭）

```python
data = pd.DataFrame({'age': [18, 19, 35, 36, 60, 61]})

# right=True（默认）：右闭合 (0, 18], (18, 35], (35, 60], (60, 100]
data['group1'] = pd.cut(
    data['age'],
    bins=[0, 18, 35, 60, 100],
    labels=['A', 'B', 'C', 'D'],
    right=True
)
# 18 → A, 19 → B, 35 → B, 36 → C

# right=False：左闭合 [0, 18), [18, 35), [35, 60), [60, 100)
data['group2'] = pd.cut(
    data['age'],
    bins=[0, 18, 35, 60, 100],
    labels=['A', 'B', 'C', 'D'],
    right=False
)
# 18 → B, 19 → B, 35 → C, 36 → C
```

### 等宽分箱（指定箱数）

```python
scores = [55, 62, 78, 85, 92, 98]

# 自动分为 4 个等宽区间
score_levels = pd.cut(scores, bins=4)
print(score_levels)
# (54.96, 65.75], (54.96, 65.75], (65.75, 76.5], (76.5, 87.25], (87.25, 98.0], (87.25, 98.0]
```

### 实际应用：成绩分级

```python
data = pd.DataFrame({'score': [45, 58, 67, 72, 88, 95]})

data['grade'] = pd.cut(
    data['score'],
    bins=[0, 60, 70, 80, 90, 100],
    labels=['不及格', '及格', '中等', '良好', '优秀'],
    right=False  # [0,60), [60,70), [70,80), [80,90), [90,100)
)

print(data)
#    score grade
# 0     45  不及格
# 1     58  不及格
# 2     67   及格
# 3     72   中等
# 4     88   良好
# 5     95   优秀
```

## pd.cut vs pd.qcut

| 方法 | 分箱方式 | 结果 | 适用场景 |
|------|----------|------|----------|
| **pd.cut** | 等宽分箱 | 区间宽度相等 | 有明确阈值（如年龄段） |
| **pd.qcut** | 等频分箱 | 每组数量相近 | 需要均匀分布（如分位数） |

```python
data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

# 等宽：每个区间宽度 2.5
pd.cut(data, bins=4)
# (0.991, 3.25], (0.991, 3.25], (0.991, 3.25], (3.25, 5.5], ...

# 等频：每组 2-3 个数
pd.qcut(data, q=4)
# (0.999, 3.0], (0.999, 3.0], (3.0, 5.5], (3.0, 5.5], ...
```

## 易错点

⚠️ **labels 数量要比 bins 少 1**：
```python
# ❌ 错误（4个边界 → 3个区间，但给了4个标签）
pd.cut(ages, bins=[0, 18, 35, 60, 100], labels=['A', 'B', 'C', 'D'])

# ✅ 正确（4个边界 → 3个区间 → 3个标签）
pd.cut(ages, bins=[0, 18, 35, 60], labels=['A', 'B', 'C'])
```

⚠️ **边界值归属问题**：
```python
# 18 岁应该算青少年还是青年？取决于 right 参数
age = 18

# right=True（默认）: 18 属于 (0, 18] → 青少年
pd.cut([18], bins=[0, 18, 35], labels=['青少年', '青年'], right=True)
# ['青少年']

# right=False: 18 属于 [18, 35) → 青年
pd.cut([18], bins=[0, 18, 35], labels=['青少年', '青年'], right=False)
# ['青年']
```

⚠️ **超出边界值会变成 NaN**：
```python
ages = [5, 150]  # 150 超出范围
result = pd.cut(ages, bins=[0, 18, 35, 60, 100], labels=['A', 'B', 'C', 'D'])
print(result)
# ['A', NaN]
```

## 相关概念

- [[pd-qcut]] - 等频分箱
- [[boolean-indexing]] - 条件筛选（分箱的替代方案）
