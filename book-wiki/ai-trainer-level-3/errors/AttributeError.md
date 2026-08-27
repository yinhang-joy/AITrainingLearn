# AttributeError 错误排查

## 常见错误 1：对象没有该属性/方法

### 错误信息
```
AttributeError: 'DataFrame' object has no attribute 'methodName'
```

### 原因
调用了不存在的属性或方法名拼写错误。

### 解决方案

```python
# 查看对象的所有方法
print(dir(data))

# ❌ 常见拼写错误
data.drop_na()      # 正确是 dropna()
data.fillNa()       # 正确是 fillna()
data.value_count()  # 正确是 value_counts()

# ✅ 正确写法
data.dropna()
data.fillna(0)
data['col'].value_counts()
```

---

## 常见错误 2：Series 和 DataFrame 方法混淆

### 错误信息
```
AttributeError: 'Series' object has no attribute 'drop'
```

### 原因
Series 和 DataFrame 方法不完全相同。

### 解决方案

```python
# Series 删除元素用 .drop()
series = pd.Series([1, 2, 3], index=['a', 'b', 'c'])
series.drop('a')  # ✅ 可以

# DataFrame 删除列
data.drop('col_name', axis=1)  # ✅ 可以

# ❌ 错误
series['a'].drop()  # Series 单个元素没有 drop
```

---

## 常见错误 3：str accessor 错误

### 错误信息
```
AttributeError: Can only use .str accessor with string values
```

### 原因
对非字符串列使用 `.str` 方法。

### 解决方案

```python
# 检查数据类型
print(data['col'].dtype)  # int64

# ❌ 错误（数值列不能用 .str）
data['col'].str.contains('abc')

# ✅ 先转换为字符串
data['col'] = data['col'].astype(str)
data['col'].str.contains('abc')
```

---

## 常见错误 4：链式操作丢失返回值

### 错误信息
```
AttributeError: 'NoneType' object has no attribute 'head'
```

### 原因
某个操作返回 None，后续链式调用失败。

### 解决方案

```python
# ❌ 错误（inplace=True 返回 None）
result = data.dropna(inplace=True).head()
# AttributeError: 'NoneType' object has no attribute 'head'

# ✅ 方案1：不用 inplace
result = data.dropna().head()

# ✅ 方案2：分步操作
data.dropna(inplace=True)
result = data.head()
```

---

## 常见错误 5：模型未拟合

### 错误信息
```
AttributeError: 'LogisticRegression' object has no attribute 'coef_'
```

### 原因
在 `.fit()` 之前访问模型属性。

### 解决方案

```python
from sklearn.linear_model import LogisticRegression

model = LogisticRegression()

# ❌ 错误（未训练）
print(model.coef_)  # AttributeError

# ✅ 正确（先训练）
model.fit(X_train, y_train)
print(model.coef_)
```

---

## 常见错误 6：访问私有属性

### 错误信息
```
AttributeError: 'StandardScaler' object has no attribute 'mean'
```

### 原因
属性名错误，应该是 `mean_` 而不是 `mean`。

### 解决方案

```python
scaler = StandardScaler()
scaler.fit(X_train)

# ❌ 错误
print(scaler.mean)  # AttributeError

# ✅ 正确（注意末尾的下划线）
print(scaler.mean_)
print(scaler.scale_)
```

**规则**：sklearn 中 fit 后生成的属性都有**下划线后缀**。

---

## 快速排查步骤

1. **检查拼写**：方法名大小写、下划线
2. **查看类型**：`print(type(obj))`
3. **查看可用方法**：`print(dir(obj))`
4. **确认对象状态**：是否已初始化、是否已 fit
5. **检查链式调用**：是否有操作返回 None

## 常见拼写错误

| ❌ 错误 | ✅ 正确 |
|---------|---------|
| `drop_na()` | `dropna()` |
| `fillNa()` | `fillna()` |
| `value_count()` | `value_counts()` |
| `isnull()` 后忘记 `sum()` | `isnull().sum()` |
| `scaler.mean` | `scaler.mean_` |
| `model.coef` | `model.coef_` |

## 相关错误

- [[TypeError]] - 类型错误
- [[KeyError]] - 键错误
- [[NameError]] - 名称错误
