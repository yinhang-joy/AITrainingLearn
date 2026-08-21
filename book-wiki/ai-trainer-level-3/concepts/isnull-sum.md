# 缺失值检测：isnull().sum()

## 概念

检测 DataFrame 中每列的缺失值数量。

## 语法

```python
df.isnull().sum()         # 每列缺失值数量
df.isnull().sum().sum()   # 总缺失值数量
```

## 原理

- `.isnull()`：返回布尔 DataFrame（每个单元格是 True/False）
  - `True`：该单元格是 NaN（缺失值）
  - `False`：该单元格有值
- `.sum()`：对布尔值求和（True=1，False=0）
  - 第一次 `.sum()`：按列求和（每列有多少个 True）
  - 第二次 `.sum()`：对所有列求和（总共多少个 True）

## 示例

```python
import pandas as pd

data = pd.DataFrame({
    'A': [1, 2, None, 4],
    'B': [5, None, None, 8],
    'C': [9, 10, 11, 12]
})

# 检查每列的缺失值数量
print(data.isnull().sum())
# 输出：
# A    1   ← 第 3 行缺失
# B    2   ← 第 2、3 行缺失
# C    0   ← 无缺失
# dtype: int64

# 检查总缺失值数量
print(data.isnull().sum().sum())
# 输出：3
```

## 可视化缺失值

```python
# 查看缺失值的布尔矩阵
print(data.isnull())
#        A      B      C
# 0  False  False  False
# 1  False   True  False
# 2   True   True  False
# 3  False  False  False

# 查看非缺失值数量
print(data.notnull().sum())
# 输出：
# A    3
# B    2
# C    4
```

## 常见用法

### 用法 1：找出有缺失值的列

```python
# 只显示有缺失值的列
missing_cols = data.isnull().sum()
print(missing_cols[missing_cols > 0])
# 输出：
# A    1
# B    2
```

### 用法 2：计算缺失率

```python
# 每列的缺失率（百分比）
missing_rate = (data.isnull().sum() / len(data)) * 100
print(missing_rate)
# 输出：
# A    25.0   ← 1/4 = 25%
# B    50.0   ← 2/4 = 50%
# C     0.0
```

### 用法 3：数据质量报告

```python
# 综合报告
report = pd.DataFrame({
    '缺失值数量': data.isnull().sum(),
    '缺失率(%)': (data.isnull().sum() / len(data)) * 100,
    '非缺失值数量': data.notnull().sum()
})
print(report)
#    缺失值数量  缺失率(%)  非缺失值数量
# A         1     25.0          3
# B         2     50.0          2
# C         0      0.0          4
```

## 易错点

### ⚠️ 错误 1：忘记 `.sum()`

```python
# ❌ 错误（只返回布尔矩阵，无法直观看数量）
print(data.isnull())
#        A      B      C
# 0  False  False  False
# 1  False   True  False
# ...

# ✅ 正确
print(data.isnull().sum())
# A    1
# B    2
# C    0
```

### ⚠️ 错误 2：混淆 isnull 和 notnull

```python
# isnull() 统计缺失值
print(data.isnull().sum())
# A    1  ← 有 1 个缺失

# notnull() 统计非缺失值
print(data.notnull().sum())
# A    3  ← 有 3 个非缺失
```

## 相关方法对比

| 方法 | 返回值 | 用途 |
|---|---|---|
| `.isnull()` | 布尔 DataFrame | 标记每个单元格是否缺失 |
| `.isnull().sum()` | Series（每列缺失数量） | 统计每列缺失值数量 |
| `.isnull().any()` | Series（每列是否有缺失） | 判断每列是否存在缺失值 |
| `.isnull().sum().sum()` | int（总缺失数量） | 统计整个 DataFrame 的缺失值总数 |

## 示例：考试常见题型

```python
import pandas as pd

# 加载数据
data = pd.read_csv('auto-mpg.csv')

# 任务：检查缺失值
print("检查缺失值:")
print(data.isnull().sum())
# 输出示例：
# mpg             0
# cylinders       0
# displacement    6   ← 有 6 个缺失值
# horsepower      0
# weight          0
# acceleration    1   ← 有 1 个缺失值
# model year      0
# origin          0
# car name        0
```

## 关联操作

- [[concepts/dropna]] 删除缺失值
- [[concepts/fillna]] 填充缺失值
- [[concepts/pandas-read-csv]] 数据加载
- [[concepts/boolean-indexing]] 筛选缺失值行
