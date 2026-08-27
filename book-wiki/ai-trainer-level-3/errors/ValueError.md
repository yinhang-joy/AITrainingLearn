# ValueError 错误排查

## 常见错误 1：形状不匹配

### 错误信息
```
ValueError: operands could not be broadcast together with shapes (100,) (80,)
```

### 原因
两个数组长度不同，无法进行元素对应的运算。

### 解决方案

```python
# 检查长度
print(len(X_train))  # 100
print(len(y_train))  # 80

# 确保长度一致
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
```

---

## 常见错误 2：标签数量不匹配

### 错误信息
```
ValueError: Bin labels must be one fewer than the number of bin edges
```

### 原因
`pd.cut()` 的 labels 数量不对。

### 解决方案

```python
# ❌ 错误（4个边界 → 3个区间，但给了4个标签）
pd.cut(ages, bins=[0, 18, 35, 60, 100], labels=['A', 'B', 'C', 'D'])

# ✅ 正确（4个边界 → 3个区间 → 3个标签）
pd.cut(ages, bins=[0, 18, 35, 60], labels=['A', 'B', 'C'])
```

**规则**：N 个边界 → N-1 个区间 → N-1 个标签

---

## 常见错误 3：无法转换为数值

### 错误信息
```
ValueError: could not convert string to float: 'abc'
```

### 原因
字符串无法直接转换为数字。

### 解决方案

```python
# ❌ 错误（强制转换会报错）
data['col'] = data['col'].astype(float)

# ✅ 方案1：用 to_numeric（异常值变 NaN）
data['col'] = pd.to_numeric(data['col'], errors='coerce')

# ✅ 方案2：先清洗再转换
data = data[data['col'].str.isdigit()]  # 只保留数字
data['col'] = data['col'].astype(float)
```

---

## 常见错误 4：列名不存在

### 错误信息
```
ValueError: "['col_name'] not in index"
```

### 原因
DataFrame 中不存在指定的列名。

### 解决方案

```python
# 检查列名
print(data.columns)

# ❌ 可能是拼写错误
data['Horsepower']  # 实际列名是 'horsepower'

# ✅ 正确
data['horsepower']

# 或使用 .get() 避免报错
data.get('col_name', default_value)
```

---

## 常见错误 5：空数据聚合

### 错误信息
```
ValueError: Cannot index with multidimensional key
```

### 原因
对空 DataFrame 进行操作。

### 解决方案

```python
# 检查数据是否为空
if data.empty:
    print("数据为空")
else:
    result = data.groupby('category').mean()
```

---

## 常见错误 6：数据范围错误

### 错误信息
```
ValueError: Input contains NaN, infinity or a value too large
```

### 原因
模型训练数据包含 NaN 或无穷大。

### 解决方案

```python
# 检查 NaN
print(X.isnull().sum())

# 检查无穷大
print(np.isinf(X).sum())

# 清洗数据
X = X.dropna()  # 删除 NaN
X = X.replace([np.inf, -np.inf], np.nan).dropna()  # 删除无穷大
```

---

## 快速排查步骤

1. **读完整错误信息**：ValueError 后面的描述是关键
2. **检查数据形状**：`print(data.shape)`, `print(len(X))`
3. **检查数据内容**：`print(data.head())`, `print(data.isnull().sum())`
4. **验证参数合法性**：bins/labels 数量、列名是否存在
5. **简化测试**：用小样本数据复现

## 相关错误

- [[TypeError]] - 类型错误
- [[KeyError]] - 键错误
- [[IndexError]] - 索引错误
