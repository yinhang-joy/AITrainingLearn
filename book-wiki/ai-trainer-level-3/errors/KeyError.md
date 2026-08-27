# KeyError 错误排查

## 常见错误 1：列名不存在

### 错误信息
```
KeyError: 'column_name'
```

### 原因
DataFrame 中不存在指定的列名。

### 解决方案

```python
# 查看所有列名
print(data.columns)
print(data.columns.tolist())  # 列表形式

# ❌ 可能原因：拼写错误
data['Horsepower']  # 实际是 'horsepower'（小写）

# ✅ 方案1：修正列名
data['horsepower']

# ✅ 方案2：重命名列（如果列名不规范）
data.rename(columns={'old_name': 'new_name'}, inplace=True)

# ✅ 方案3：安全访问（不报错）
value = data.get('column_name', default_value)
```

---

## 常见错误 2：多层索引问题

### 错误信息
```
KeyError: ('level_0', 'level_1')
```

### 原因
MultiIndex（多层索引）访问方式不对。

### 解决方案

```python
# 查看索引结构
print(data.index)

# ❌ 错误
data['level_1']

# ✅ 正确
data.loc[('level_0', 'level_1')]

# 或重置索引
data = data.reset_index()
```

---

## 常见错误 3：字典键不存在

### 错误信息
```
KeyError: 'key_name'
```

### 原因
字典中不存在该键。

### 解决方案

```python
my_dict = {'a': 1, 'b': 2}

# ❌ 错误
value = my_dict['c']  # KeyError

# ✅ 方案1：用 .get()（推荐）
value = my_dict.get('c', 0)  # 不存在返回 0

# ✅ 方案2：先检查
if 'c' in my_dict:
    value = my_dict['c']
else:
    value = 0

# ✅ 方案3：用 defaultdict
from collections import defaultdict
my_dict = defaultdict(int)  # 默认值 0
value = my_dict['c']  # 自动返回 0
```

---

## 常见错误 4：groupby 后列名变化

### 错误信息
```
KeyError: 'column_name'
```

### 原因
`groupby().agg()` 后列名结构变化。

### 解决方案

```python
# groupby 后检查列名
result = data.groupby('category')['sales'].agg(['mean', 'sum'])
print(result.columns)  # ['mean', 'sum']

# ❌ 错误
result['sales']  # 已经没有 'sales' 列了

# ✅ 正确
result['mean']  # 直接用聚合函数名

# 或重置列名
result.columns = ['avg_sales', 'total_sales']
```

---

## 常见错误 5：读取 CSV 后列名问题

### 错误信息
```
KeyError: 'column_name'
```

### 原因
CSV 列名前后有空格或不可见字符。

### 解决方案

```python
# 读取 CSV 后检查列名
data = pd.read_csv('file.csv')
print(data.columns.tolist())  # [' age ', 'score']（注意空格）

# ✅ 方案1：去除空格
data.columns = data.columns.str.strip()

# ✅ 方案2：读取时处理
data = pd.read_csv('file.csv', skipinitialspace=True)

# ✅ 方案3：重命名
data.rename(columns=lambda x: x.strip(), inplace=True)
```

---

## 快速排查步骤

1. **打印所有列名**：`print(data.columns.tolist())`
2. **检查拼写**：大小写、空格、特殊字符
3. **查看数据结构**：`print(data.head())`, `print(data.info())`
4. **用 .get() 代替直接访问**：更安全
5. **重置索引**：如果是 MultiIndex 问题

## 常见陷阱

❌ **列名前后有空格**：
```python
data.columns  # [' age', 'score ']
data['age']   # KeyError
```

❌ **列名类型不对**：
```python
data.columns  # [0, 1, 2]（整数）
data['0']     # KeyError（应该用 data[0]）
```

❌ **操作后列名变化**：
```python
result = data.groupby('A')['B'].mean()
result['B']  # KeyError（mean() 后 'B' 变成了索引）
```

## 相关错误

- [[ValueError]] - 值错误
- [[AttributeError]] - 属性错误
- [[IndexError]] - 索引错误
