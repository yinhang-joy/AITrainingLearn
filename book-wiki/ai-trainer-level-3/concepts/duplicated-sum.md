# 重复值检测：duplicated().sum()

## 概念

检测 DataFrame 中完全重复的行数量，返回重复行的计数。

## 语法

```python
df.duplicated().sum()              # 重复行数量
df.duplicated(keep='first').sum()  # 默认：标记第2次及之后出现的重复行
df.duplicated(keep='last').sum()   # 标记第1次到倒数第2次出现的重复行
df.duplicated(keep=False).sum()    # 标记所有重复行（包括首次出现）
```

## 原理

1. `df.duplicated()` 返回布尔 Series（每行是 True/False）
2. 默认 `keep='first'`：每组重复行中，第一次出现标记为 False，后续标记为 True
3. `.sum()` 统计 True 的数量（即重复行数量）

## 示例

```python
import pandas as pd

data = pd.DataFrame({
    'Name': ['Alice', 'Bob', 'Alice', 'David', 'Bob'],
    'Age': [25, 30, 25, 35, 30]
})

# 检测重复行
print(data.duplicated())
# 0    False  ← Alice, 25 首次出现
# 1    False  ← Bob, 30 首次出现
# 2     True  ← Alice, 25 重复
# 3    False  ← David, 35 首次出现
# 4     True  ← Bob, 30 重复

print(data.duplicated().sum())  # 2

# 查看重复的行内容
print(data[data.duplicated()])
#     Name  Age
# 2  Alice   25
# 4    Bob   30
```

## 常见用法

```python
# 删除重复行（保留第一次出现）
data_cleaned = data[~data.duplicated()]
# 或者
data_cleaned = data.drop_duplicates()

# 基于特定列检测重复
data.duplicated(subset=['Name']).sum()

# 查看所有重复行（包括首次出现）
data[data.duplicated(keep=False)]
```

## 参数说明

| 参数 | 含义 | 标记结果 |
|---|---|---|
| `keep='first'` | 保留首次出现 | 第2次及之后标记为 True |
| `keep='last'` | 保留最后出现 | 第1次到倒数第2次标记为 True |
| `keep=False` | 不保留任何 | 所有重复行标记为 True |

## 易错点

- **默认是整行比较**：所有列都相同才算重复
- 如需按特定列检测：`duplicated(subset=['列名'])`
- `duplicated()` 返回的是标记，不是重复行本身

## 关联操作

- [[drop-duplicates]] 删除重复行
- [[boolean-not-operator]] 取反筛选
