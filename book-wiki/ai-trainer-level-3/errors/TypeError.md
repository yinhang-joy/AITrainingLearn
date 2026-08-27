# TypeError 错误排查

## 常见错误 1：缺少必需参数

### 错误信息
```
TypeError: fit_transform() missing 1 required positional argument: 'X'
```

### 原因
调用方法时没有传入必需的参数。

### 解决方案

```python
# ❌ 错误
scaler = StandardScaler()
data[cols] = scaler.fit_transform()

# ✅ 正确
data[cols] = scaler.fit_transform(data[cols])
```

---

## 常见错误 2：参数类型错误

### 错误信息
```
TypeError: ufunc 'isnan' not supported for the input types
```

### 原因
数值运算遇到了字符串类型数据。

### 解决方案

```python
# 检查数据类型
print(data['horsepower'].dtype)  # object（字符串）

# 转换为数值类型
data['horsepower'] = pd.to_numeric(data['horsepower'], errors='coerce')
```

---

## 常见错误 3：对象不可调用

### 错误信息
```
TypeError: 'Series' object is not callable
```

### 原因
把方法当成属性用了，忘记加括号。

### 解决方案

```python
# ❌ 错误
avg = data['score'].mean  # 返回方法对象

# ✅ 正确
avg = data['score'].mean()  # 调用方法
```

---

## 常见错误 4：无法拼接不同类型

### 错误信息
```
TypeError: can only concatenate str (not "int") to str
```

### 原因
字符串和数字直接拼接。

### 解决方案

```python
# ❌ 错误
msg = "年龄: " + 25

# ✅ 方案1：转换为字符串
msg = "年龄: " + str(25)

# ✅ 方案2：使用 f-string
msg = f"年龄: {25}"
```

---

## 常见错误 5：索引类型错误

### 错误信息
```
TypeError: list indices must be integers or slices, not str
```

### 原因
对 list 使用了字符串索引（list 只能用整数索引）。

### 解决方案

```python
# ❌ 错误
data = [1, 2, 3]
print(data['age'])

# ✅ 方案1：用 DataFrame
data = pd.DataFrame({'age': [1, 2, 3]})
print(data['age'])

# ✅ 方案2：用字典
data = {'age': [1, 2, 3]}
print(data['age'])
```

---

## 常见错误 6：布尔运算符误用

### 错误信息
```
TypeError: cannot compare a dtyped [float64] array with a scalar of type [bool]
```

### 原因
pandas 条件筛选用了 `and` / `or` 而不是 `&` / `|`。

### 解决方案

```python
# ❌ 错误
result = data[(data['age'] > 18) and (data['score'] > 60)]

# ✅ 正确
result = data[(data['age'] > 18) & (data['score'] > 60)]
```

---

## 快速排查步骤

1. **查看完整错误信息**：最后一行是关键
2. **定位出错行**：Traceback 指向的行号
3. **检查变量类型**：`print(type(变量))` 或 `print(data.dtypes)`
4. **验证参数数量**：方法签名要求几个参数
5. **测试简化版本**：用最小数据复现问题

## 相关错误

- [[ValueError]] - 值错误
- [[AttributeError]] - 属性错误
- [[KeyError]] - 键错误
