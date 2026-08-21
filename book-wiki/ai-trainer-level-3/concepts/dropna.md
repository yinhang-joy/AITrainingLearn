# 缺失值删除：dropna()

## 概念

删除 DataFrame 中包含缺失值（NaN）的行或列。

## 语法

```python
df.dropna()                    # 删除任何包含 NaN 的行（默认）
df.dropna(axis=0)              # 删除行（axis=0）
df.dropna(axis=1)              # 删除列（axis=1）
df.dropna(how='any')           # 任何 NaN 都删除（默认）
df.dropna(how='all')           # 全部是 NaN 才删除
df.dropna(subset=['A', 'B'])   # 只检查指定列
df.dropna(inplace=True)        # 就地修改（不推荐）
```

## 参数详解

| 参数 | 默认值 | 说明 |
|---|---|---|
| `axis` | `0` | `0`=删除行，`1`=删除列 |
| `how` | `'any'` | `'any'`=任何 NaN 都删，`'all'`=全是 NaN 才删 |
| `subset` | `None` | 只检查指定列的缺失值 |
| `inplace` | `False` | `True`=就地修改，`False`=返回新 DataFrame |

## 示例

```python
import pandas as pd
import numpy as np

data = pd.DataFrame({
    'A': [1, 2, np.nan, 4],
    'B': [5, np.nan, np.nan, 8],
    'C': [9, 10, 11, 12]
})

print("原始数据:")
print(data)
#      A    B   C
# 0  1.0  5.0   9
# 1  2.0  NaN  10
# 2  NaN  NaN  11
# 3  4.0  8.0  12
```

### 示例 1：删除包含任何 NaN 的行（默认）

```python
cleaned = data.dropna()
print(cleaned)
#      A    B   C
# 0  1.0  5.0   9
# 3  4.0  8.0  12
# ← 第 1、2 行被删除（包含 NaN）
```

### 示例 2：删除全部是 NaN 的行

```python
data_with_all_nan = pd.DataFrame({
    'A': [1, np.nan, np.nan, 4],
    'B': [5, np.nan, np.nan, 8],
    'C': [9, np.nan, np.nan, 12]
})

cleaned = data_with_all_nan.dropna(how='all')
print(cleaned)
#      A    B   C
# 0  1.0  5.0   9
# 3  4.0  8.0  12
# ← 第 1、2 行被删除（全是 NaN）
```

### 示例 3：删除包含 NaN 的列

```python
cleaned = data.dropna(axis=1)
print(cleaned)
#     C
# 0   9
# 1  10
# 2  11
# 3  12
# ← 列 A 和 B 被删除（包含 NaN）
```

### 示例 4：只检查指定列的缺失值

```python
# 只删除 A 列有缺失值的行（B 列的缺失值忽略）
cleaned = data.dropna(subset=['A'])
print(cleaned)
#      A    B   C
# 0  1.0  5.0   9
# 1  2.0  NaN  10
# 3  4.0  8.0  12
# ← 第 2 行被删除（A 列是 NaN）
# ← 第 1 行保留（虽然 B 列是 NaN，但只检查 A 列）
```

## 常见用法：考试场景

```python
import pandas as pd

# 加载数据
data = pd.read_csv('auto-mpg.csv')

# 检查缺失值
print(data.isnull().sum())
# displacement    6
# acceleration    1

# 删除包含缺失值的行
data = data.dropna()

# 验证清洗结果
print(data.isnull().sum())
# displacement    0
# acceleration    0
```

## inplace 参数的注意事项

```python
# ❌ 不推荐（就地修改，无法撤销）
data.dropna(inplace=True)

# ✅ 推荐（返回新 DataFrame，原数据不变）
data_cleaned = data.dropna()

# ✅ 如果需要覆盖原变量
data = data.dropna()
```

**为什么不推荐 inplace=True**：
- 原数据丢失，无法撤销
- 调试时不方便对比清洗前后的数据
- 函数没有返回值（`None`），容易写出 `data = data.dropna(inplace=True)` 导致 `data` 变成 `None`

## 易错点

### ⚠️ 错误 1：忘记赋值

```python
# ❌ 错误（只计算不保存）
data.dropna()  # 返回新 DataFrame，但没赋值给变量

# ✅ 正确
data = data.dropna()
```

### ⚠️ 错误 2：混淆 axis 参数

```python
# axis=0（默认）：删除行
data.dropna(axis=0)  # 删除包含 NaN 的行

# axis=1：删除列
data.dropna(axis=1)  # 删除包含 NaN 的列
```

### ⚠️ 错误 3：误用 inplace

```python
# ❌ 错误（data 变成 None）
data = data.dropna(inplace=True)
print(data)  # None

# ✅ 正确（两种方式二选一）
data.dropna(inplace=True)  # 方式 1：就地修改
data = data.dropna()       # 方式 2：返回新对象（推荐）
```

## 对比：dropna vs fillna

| 方法 | 作用 | 适用场景 |
|---|---|---|
| `.dropna()` | 删除缺失值所在的行/列 | 缺失值较少，删除不影响样本量 |
| `.fillna(value)` | 填充缺失值 | 缺失值较多，删除会损失大量数据 |

```python
# 删除缺失值
data = data.dropna()

# 填充缺失值
data['A'].fillna(data['A'].mean(), inplace=True)  # 用均值填充
data['B'].fillna(0, inplace=True)                  # 用 0 填充
```

## 数据清洗的最佳实践

```python
# 步骤 1：检查缺失值
print("清洗前缺失值统计:")
print(data.isnull().sum())

# 步骤 2：删除缺失值
data_cleaned = data.dropna()

# 步骤 3：验证清洗结果
print("\n清洗后缺失值统计:")
print(data_cleaned.isnull().sum())

# 步骤 4：查看数据量变化
print(f"\n清洗前：{len(data)} 行")
print(f"清洗后：{len(data_cleaned)} 行")
print(f"删除：{len(data) - len(data_cleaned)} 行")
```

## 关联操作

- [[concepts/isnull-sum]] 缺失值检测
- [[concepts/fillna]] 填充缺失值
- [[concepts/pandas-read-csv]] 数据加载
- [[concepts/pd-to-numeric]] 数据类型转换（可能产生新的 NaN）
