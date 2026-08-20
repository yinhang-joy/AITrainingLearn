# 区间验证：between()

## 概念

检查 Series 中的每个值是否在指定区间内，返回布尔 Series。

## 语法

```python
series.between(left, right)                      # 闭区间 [left, right]
series.between(left, right, inclusive='both')    # 闭区间 [left, right]（默认）
series.between(left, right, inclusive='neither') # 开区间 (left, right)
series.between(left, right, inclusive='left')    # 左闭右开 [left, right)
series.between(left, right, inclusive='right')   # 左开右闭 (left, right]
```

## 原理

等价于 `(series >= left) & (series <= right)`，但更简洁易读。

## 示例

```python
import pandas as pd

ages = pd.Series([15, 18, 25, 50, 70, 75])

# 检查年龄是否在 18-70 之间（闭区间）
valid_age = ages.between(18, 70)
print(valid_age)
# 0    False  ← 15 < 18
# 1     True  ← 18 在区间内
# 2     True  ← 25 在区间内
# 3     True  ← 50 在区间内
# 4     True  ← 70 在区间内
# 5    False  ← 75 > 70

# 筛选合理年龄
print(ages[valid_age])
# 1    18
# 2    25
# 3    50
# 4    70
```

## 处理缺失值

```python
ages_with_nan = pd.Series([15, 18, None, 50, 70])

# between 遇到 NaN 返回 NaN（不是 False）
print(ages_with_nan.between(18, 70))
# 0    False
# 1     True
# 2      NaN  ← 缺失值返回 NaN
# 3     True
# 4     True

# 将 NaN 视为不合理（转为 False）
print(ages_with_nan.between(18, 70).fillna(False))
# 0    False
# 1     True
# 2    False  ← NaN 转为 False
# 3     True
# 4     True
```

## 参数详解

| inclusive 参数 | 含义 | 等价写法 |
|---|---|---|
| `'both'`（默认） | 闭区间 | `(s >= a) & (s <= b)` |
| `'neither'` | 开区间 | `(s > a) & (s < b)` |
| `'left'` | 左闭右开 | `(s >= a) & (s < b)` |
| `'right'` | 左开右闭 | `(s > a) & (s <= b)` |

## 常见用法

```python
# 信用评分合理性检查
df['is_credit_valid'] = df['CreditScore'].between(300, 850)

# 收入区间统计
df['income_range'] = pd.cut(df['Income'], bins=[0, 5000, 10000, 50000])
df[df['Income'].between(5000, 10000)]

# 时间范围筛选
df['Date'] = pd.to_datetime(df['Date'])
df[df['Date'].between('2024-01-01', '2024-12-31')]
```

## 易错点

- **默认包含边界**：题目「18 到 70」通常指 `[18, 70]`，直接用 `.between(18, 70)` 即可
- **NaN 返回 NaN**：不是 False，可能导致后续逻辑错误
- **类型匹配**：左右边界类型要与 Series 类型一致（数值 vs 字符串 vs 日期）

## 对比：between vs 双重比较

```python
# 方法1：between（推荐）
df['Age'].between(18, 70)

# 方法2：双重比较（等价但繁琐）
(df['Age'] >= 18) & (df['Age'] <= 70)
```

**推荐 between 的原因**：
- 代码更简洁
- 避免括号错误（& 优先级高于比较运算符）
- 语义更清晰

## 关联操作

- [[cross-column-comparison]] 跨列比较
- [[boolean-indexing]] 布尔索引筛选
- [[pd-cut-binning]] 区间分箱
