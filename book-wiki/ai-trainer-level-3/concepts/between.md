# between —— 范围验证

## 基本用法

```python
data['Age'].between(18, 70)
```

**作用**：检查每个值是否在指定范围内，返回布尔列（True/False）

## 等价写法对比

```python
# 使用 between（简洁）
data['Age'].between(18, 70)

# 传统写法（繁琐）
(data['Age'] >= 18) & (data['Age'] <= 70)
```

**结果**：两者完全相同，但 `between` 更易读

## 参数说明

```python
data['Age'].between(left, right, inclusive='both')
```

| 参数 | 默认值 | 说明 |
|---|---|---|
| `left` | 必填 | 范围下界 |
| `right` | 必填 | 范围上界 |
| `inclusive` | `'both'` | 边界是否包含：`'both'`（闭区间）/ `'neither'`（开区间）/ `'left'` / `'right'` |

### 区间类型示例

```python
# 闭区间 [18, 70]（包含边界）
data['Age'].between(18, 70, inclusive='both')  # 默认
# 18 ✓  70 ✓

# 开区间 (18, 70)（不包含边界）
data['Age'].between(18, 70, inclusive='neither')
# 18 ✗  70 ✗

# 左闭右开 [18, 70)
data['Age'].between(18, 70, inclusive='left')
# 18 ✓  70 ✗
```

## 常见应用

### 1. 数据清洗（删除异常值）

```python
# 保留合理范围内的数据
data = data[(data['Age'].between(18, 70)) & 
            (data['Speed'].between(0, 200))]
```

### 2. 数据审核（标记异常）

```python
# 找出不合理的数据（取反）
unreasonable = data[~(data['Age'].between(18, 70))]
```

### 3. 多条件筛选

```python
# 同时验证多个字段
valid_data = data[(data['Age'].between(18, 70)) & 
                  (data['Speed'].between(0, 200)) & 
                  (data['Distance'].between(1, 1000))]
```

## 注意事项

### ⚠️ 必须加括号（多条件时）

```python
# ❌ 错误（运算符优先级导致逻辑错误）
data = data[data['Age'].between(18, 70) & data['Speed'].between(0, 200)]

# ✅ 正确
data = data[(data['Age'].between(18, 70)) & (data['Speed'].between(0, 200))]
```

### ⚠️ 取反时整个条件加括号

```python
# ❌ 错误
unreasonable = data[~data['Age'].between(18, 70)]

# ✅ 正确
unreasonable = data[~(data['Age'].between(18, 70))]
```

## 对比其他方法

| 方法 | 代码 | 优势 |
|---|---|---|
| `between` | `data['Age'].between(18, 70)` | 简洁易读 |
| 传统比较 | `(data['Age'] >= 18) & (data['Age'] <= 70)` | 灵活但繁琐 |
| `isin` | `data['Age'].isin(range(18, 71))` | 仅适用于整数 |
