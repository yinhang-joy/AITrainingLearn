# 布尔取反：~ 运算符

## 概念

对布尔 Series 或布尔 DataFrame 的每个值取反（True ↔ False），常用于筛选「不满足条件」的数据。

## 语法

```python
~series              # 对布尔 Series 取反
~df['布尔列']        # 对列取反
~(条件表达式)        # 对条件结果取反
```

## 原理

按位取反（bitwise NOT）：
- True → False
- False → True
- NaN → NaN（⚠️ 注意：NaN 取反仍是 NaN）

## 示例

### 场景1：筛选不合理数据

```python
import pandas as pd

data = pd.DataFrame({
    'Name': ['Alice', 'Bob', 'Charlie', 'David'],
    'Age': [25, 150, 30, -5]
})

# 合理年龄：18-70
data['is_valid'] = data['Age'].between(18, 70)
print(data)
#       Name  Age  is_valid
# 0    Alice   25      True
# 1      Bob  150     False  ← 超出范围
# 2  Charlie   30      True
# 3    David   -5     False  ← 超出范围

# 筛选不合理数据（取反）
invalid_data = data[~data['is_valid']]
print(invalid_data)
#     Name  Age  is_valid
# 1    Bob  150     False
# 3  David   -5     False
```

### 场景2：排除特定值

```python
cities = pd.Series(['北京', '上海', '深圳', '广州', '北京'])

# 不在列表中的城市
not_first_tier = cities[~cities.isin(['北京', '上海', '广州', '深圳'])]
print(not_first_tier)
# Series([], dtype: object)  ← 所有城市都在列表里

# 不是北京的城市
not_beijing = cities[~(cities == '北京')]
print(not_beijing)
# 1    上海
# 2    深圳
# 3    广州
```

### 场景3：保留非重复行

```python
data = pd.DataFrame({
    'ID': [1, 2, 2, 3, 3],
    'Value': [10, 20, 20, 30, 30]
})

# 删除重复行（保留首次出现）
unique_data = data[~data.duplicated()]
print(unique_data)
#    ID  Value
# 0   1     10
# 1   2     20
# 3   3     30
```

## 常见用法

```python
# 非缺失值
df[~df['Age'].isnull()]
# 等价于
df[df['Age'].notnull()]

# 不在列表中
df[~df['City'].isin(['北京', '上海'])]

# 不满足条件
df[~(df['Score'] > 60)]
# 等价于
df[df['Score'] <= 60]

# 不重复
df[~df.duplicated()]

# 不合理数据
df[~df['is_valid']]
```

## 对比：~ vs == False

```python
data = pd.DataFrame({
    'is_valid': [True, False, None]
})

# 方法1：取反 ~
print(~data['is_valid'])
# 0    False
# 1     True
# 2      NaN  ← NaN 取反仍是 NaN

# 方法2：== False
print(data['is_valid'] == False)
# 0    False
# 1     True
# 2    False  ← NaN == False 返回 False
```

**区别**：
- `~` 对 NaN 返回 NaN
- `== False` 对 NaN 返回 False

**实际影响**：
```python
# 筛选时的区别
data[~data['is_valid']]          # NaN 行不会被选中（NaN 视为非 True）
data[data['is_valid'] == False]  # NaN 行也不会被选中（NaN == False 为 False）
```

## 易错点

### ⚠️ 陷阱1：忘记加括号

```python
# ❌ 错误（优先级导致语法错误）
df[~df['Age'] > 18]
# 相当于 df[(~df['Age']) > 18]，对数值取反后再比较（逻辑错误）

# ✅ 正确
df[~(df['Age'] > 18)]
```

### ⚠️ 陷阱2：对数值列取反

```python
ages = pd.Series([10, 20, 30])

# ❌ 错误（对数值取反是按位取反，不是逻辑取反）
print(~ages)
# 0   -11
# 1   -21
# 2   -31
# 按位取反：~10 = -11（二进制取反）

# ✅ 正确（先转布尔再取反）
valid = ages > 18
print(~valid)
# 0     True  ← 10 <= 18
# 1    False  ← 20 > 18
# 2    False  ← 30 > 18
```

### ⚠️ 陷阱3：NaN 的特殊性

```python
series = pd.Series([True, False, None])

# ~ 对 NaN 返回 NaN
print(~series)
# 0    False
# 1     True
# 2      NaN

# 如需将 NaN 视为 False
(~series).fillna(False)
# 0    False
# 1     True
# 2    False
```

## 性能优化

对于大数据集，`~` 比 `== False` 略快（直接位运算 vs 元素比较）。

```python
# 推荐写法（更快）
df[~df['is_valid']]

# 可行但稍慢
df[df['is_valid'] == False]
```

## 关联操作

- [[boolean-indexing]] 布尔索引筛选
- [[isin-filter]] 多值筛选
- [[duplicated-sum]] 重复值检测
- [[isnull-sum]] 缺失值检测
