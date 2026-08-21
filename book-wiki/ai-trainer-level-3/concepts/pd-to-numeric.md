# 数据类型转换：pd.to_numeric()

## 概念

将 Series 转换为数值类型（int 或 float），处理字符串列中的数值数据。

## 语法

```python
pd.to_numeric(series)                    # 严格转换（失败则报错）
pd.to_numeric(series, errors='raise')    # 失败时抛出异常（默认）
pd.to_numeric(series, errors='coerce')   # 失败时设为 NaN
pd.to_numeric(series, errors='ignore')   # 失败时保持原值
```

## 参数详解

| 参数 | 默认值 | 说明 |
|---|---|---|
| `series` | 必填 | 待转换的 Series（通常是 DataFrame 的一列） |
| `errors` | `'raise'` | 转换失败时的处理方式 |
| `downcast` | `None` | 向下转型（如 `'integer'` / `'float'`） |

### errors 参数对比

| errors 参数 | 遇到无法转换的值 | 适用场景 |
|---|---|---|
| `'raise'`（默认） | 抛出 `ValueError` 异常 | 数据必须完全干净 |
| `'coerce'` | 转为 `NaN` | 数据可能有异常值，需要统一清理（**考试常用**） |
| `'ignore'` | 保持原值（仍是字符串） | 仅尝试转换，失败不处理 |

## 示例

### 示例 1：正常转换

```python
import pandas as pd

data = pd.Series(['1', '2', '3', '4'])
print(data.dtype)  # object（字符串）

# 转换为数值
data_numeric = pd.to_numeric(data)
print(data_numeric.dtype)  # int64
print(data_numeric)
# 0    1
# 1    2
# 2    3
# 3    4
```

### 示例 2：errors='raise'（默认，严格模式）

```python
data = pd.Series(['1', '2', '3a', '4'])

# ❌ 转换失败，抛出异常
try:
    pd.to_numeric(data)
except ValueError as e:
    print(f"错误：{e}")
# 输出：ValueError: Unable to parse string "3a" at position 2
```

### 示例 3：errors='coerce'（推荐，考试常用）

```python
data = pd.Series(['1', '2', '3a', '4', 'invalid'])

# ✅ 无法转换的值设为 NaN
data_numeric = pd.to_numeric(data, errors='coerce')
print(data_numeric)
# 0    1.0
# 1    2.0
# 2    NaN  ← '3a' 转为 NaN
# 3    4.0
# 4    NaN  ← 'invalid' 转为 NaN
```

### 示例 4：errors='ignore'（保持原值）

```python
data = pd.Series(['1', '2', '3a', '4'])

# 失败时保持原值（仍是字符串）
data_numeric = pd.to_numeric(data, errors='ignore')
print(data_numeric)
# 0      1   ← 仍是字符串 '1'
# 1      2
# 2     3a   ← 保持原值
# 3      4
print(data_numeric.dtype)  # object（未转换）
```

## 考试常见场景：清洗 horsepower 列

### 问题背景

```python
# 原始数据（CSV 读取后）
data = pd.read_csv('auto-mpg.csv')
print(data['horsepower'].head(10))
# 0      130
# 1      165
# 2      150
# 3      150
# 4      140
# 5      198
# 6      220
# 7      215
# 8      225
# 9      190

print(data['horsepower'].dtype)  # object（字符串类型）

# 发现异常值
print(data['horsepower'].unique())
# ['130', '165', '150', ..., '170a', '95b', '', '?']
#                             ↑ 异常值：包含字母或空值
```

### 解决方案

```python
# 步骤 1：使用 errors='coerce' 转换
data['horsepower'] = pd.to_numeric(data['horsepower'], errors='coerce')

# 步骤 2：删除转换后产生的 NaN
data = data.dropna()

# 步骤 3：验证转换结果
print(data['horsepower'].dtype)  # float64（已转为数值）
print(data['horsepower'].isnull().sum())  # 0（无缺失值）
```

## 为什么需要 pd.to_numeric？

### 问题：CSV 读取时的类型推断

```python
# CSV 文件内容：
# horsepower
# 130
# 165
# 170a  ← 包含非数值字符
# 150

# pandas 读取时的行为
data = pd.read_csv('auto-mpg.csv')
print(data['horsepower'].dtype)  # object
# 原因：pandas 发现 '170a' 无法转为数值，整列识别为字符串
```

### 后果：无法进行数值运算

```python
# ❌ 字符串无法参与数值运算
data['horsepower'].mean()  # TypeError

# ❌ 标准化失败
from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()
scaler.fit_transform(data[['horsepower']])  # ValueError
```

### 解决：先转换类型，再清理 NaN

```python
# 转换 + 清理
data['horsepower'] = pd.to_numeric(data['horsepower'], errors='coerce')
data = data.dropna()

# ✅ 现在可以进行数值运算
print(data['horsepower'].mean())  # 104.47
```

## 易错点

### ⚠️ 错误 1：忘记赋值

```python
# ❌ 错误（只转换不保存）
pd.to_numeric(data['horsepower'], errors='coerce')

# ✅ 正确
data['horsepower'] = pd.to_numeric(data['horsepower'], errors='coerce')
```

### ⚠️ 错误 2：使用默认 errors='raise'

```python
# ❌ 错误（遇到异常值会报错）
data['horsepower'] = pd.to_numeric(data['horsepower'])
# ValueError: Unable to parse string "170a"

# ✅ 正确（使用 errors='coerce'）
data['horsepower'] = pd.to_numeric(data['horsepower'], errors='coerce')
```

### ⚠️ 错误 3：转换后忘记清理 NaN

```python
# ❌ 不完整（转换后有 NaN，但未删除）
data['horsepower'] = pd.to_numeric(data['horsepower'], errors='coerce')
# 后续标准化仍会报错

# ✅ 完整流程
data['horsepower'] = pd.to_numeric(data['horsepower'], errors='coerce')
data = data.dropna()  # 删除 NaN
```

## 相关转换方法对比

| 方法 | 作用 | 适用场景 |
|---|---|---|
| `pd.to_numeric()` | 转为数值（int/float） | 字符串列包含数值数据 |
| `pd.to_datetime()` | 转为日期时间 | 字符串列包含日期数据 |
| `.astype(int)` | 强制转换类型 | 数据已是数值，只需改变精度 |
| `.astype(str)` | 转为字符串 | 数值列转为文本 |

```python
# pd.to_numeric（推荐，有错误处理）
pd.to_numeric(data['horsepower'], errors='coerce')

# astype（无错误处理，遇到异常直接报错）
data['horsepower'].astype(float)  # 遇到 '170a' 会报错
```

## 完整示例：数据清洗流程

```python
import pandas as pd

# 加载数据
data = pd.read_csv('auto-mpg.csv')

# 步骤 1：检查数据类型
print("原始数据类型:")
print(data.dtypes)
# horsepower    object  ← 应该是数值，但被识别为字符串

# 步骤 2：转换为数值类型
data['horsepower'] = pd.to_numeric(data['horsepower'], errors='coerce')

# 步骤 3：检查转换后的缺失值
print("\n转换后缺失值:")
print(data['horsepower'].isnull().sum())  # 6（有 6 个异常值被转为 NaN）

# 步骤 4：删除缺失值
data = data.dropna()

# 步骤 5：验证最终结果
print("\n最终数据类型:")
print(data['horsepower'].dtype)  # float64
print("\n最终缺失值:")
print(data['horsepower'].isnull().sum())  # 0
```

## 关联操作

- [[concepts/dropna]] 删除转换后产生的 NaN
- [[concepts/isnull-sum]] 检测转换后的缺失值
- [[concepts/pandas-read-csv]] 数据加载
- [[concepts/StandardScaler]] 标准化（需要数值类型）
