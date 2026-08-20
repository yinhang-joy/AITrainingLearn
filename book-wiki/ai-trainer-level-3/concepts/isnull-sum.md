# 缺失值检测：isnull().sum()

## 概念

检测 DataFrame 中每列的缺失值数量，返回每列的 NaN 计数。

## 语法

```python
df.isnull().sum()       # 每列的缺失值数量
df.isnull().sum().sum() # 整个表的缺失值总数
```

## 原理

1. `df.isnull()` 返回与原表同形状的布尔 DataFrame（每个单元格是 True/False）
2. `.sum()` 对每列求和（True=1, False=0），得到每列的 NaN 数量

## 示例

```python
import pandas as pd

data = pd.DataFrame({
    'Name': ['Alice', 'Bob', None, 'David'],
    'Age': [25, None, 30, 35],
    'City': ['北京', '上海', '深圳', None]
})

# 检测缺失值
print(data.isnull().sum())
# Name    1
# Age     1
# City    1
# dtype: int64

# 整表缺失值总数
print(data.isnull().sum().sum())  # 3
```

## 常见用法

```python
# 找出有缺失值的列
missing_cols = data.isnull().sum()
missing_cols[missing_cols > 0]

# 缺失值占比
data.isnull().sum() / len(data)

# 检查是否有缺失值
data.isnull().sum().any()  # True 表示存在缺失值
```

## 易错点

- `isnull()` 和 `isna()` 完全等价，都是检测 NaN
- 注意与 `notnull()` 区分（返回相反结果）

## 关联操作

- [[fillna-method]] 填充缺失值
- [[dropna]] 删除缺失值
- [[notnull]] 检测非缺失值
