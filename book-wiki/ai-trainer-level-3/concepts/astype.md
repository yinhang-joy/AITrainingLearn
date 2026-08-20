# astype —— 数据类型转换

## 基本用法

```python
data['Age'] = data['Age'].astype(int)
data['Speed'] = data['Speed'].astype(float)
```

**作用**：将 pandas Series（列）的数据类型转换为指定类型

## 常用类型

| 类型 | 说明 | 示例 |
|---|---|---|
| `int` | 整数（无小数点） | 年龄、数量、ID |
| `float` | 浮点数（有小数） | 速度、距离、温度 |
| `str` | 字符串 | 名称、类别、文本 |
| `bool` | 布尔值 | True/False 标志 |

## 为什么需要转换

CSV 文件读取时，pandas 可能误判数据类型：
- 数字列被识别为字符串 → 无法进行数值计算
- 整数列被识别为浮点数 → 显示多余的 `.0`

```python
# 读取后检查类型
print(data.dtypes)
# Age      float64  ← 应该是 int
# Speed    object   ← 应该是 float（object 表示字符串）

# 转换类型
data['Age'] = data['Age'].astype(int)
data['Speed'] = data['Speed'].astype(float)
```

## 注意事项

### ⚠️ 必须先清洗缺失值

```python
# ❌ 错误（NaN 无法转换为 int，会报错）
data['Age'] = data['Age'].astype(int)

# ✅ 正确（先删除 NaN，再转换）
data = data.dropna()
data['Age'] = data['Age'].astype(int)
```

### ⚠️ 转换失败会报错

```python
# 如果列中有非数字字符串，转换会失败
data['Speed'] = data['Speed'].astype(float)
# ValueError: could not convert string to float: 'abc'

# 解决方法：先清洗异常值，再转换
```

## 批量转换

```python
# 一次转换多列
data[['Age', 'Speed', 'Distance']] = data[['Age', 'Speed', 'Distance']].astype(float)
```
