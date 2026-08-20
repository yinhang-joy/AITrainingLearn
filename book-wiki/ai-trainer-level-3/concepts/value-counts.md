# value_counts —— 频次统计

## 基本用法

```python
data['TrafficEvent'].value_counts()
```

**作用**：统计分类字段每个值的出现次数，返回降序排列的 Series

## 输出示例

```python
data['TrafficEvent'].value_counts()

# 输出：
# Normal         450
# Traffic Jam    230
# Accident       180
# Breakdown      140
# Name: TrafficEvent, dtype: int64
```

## 参数说明

```python
data['column'].value_counts(normalize=False, sort=True, ascending=False, dropna=True)
```

| 参数 | 默认值 | 说明 |
|---|---|---|
| `normalize` | `False` | `True`=返回占比（0-1），`False`=返回次数 |
| `sort` | `True` | 是否按频次排序 |
| `ascending` | `False` | `False`=降序（大到小），`True`=升序 |
| `dropna` | `True` | 是否排除 NaN |

## 常见用法

### 1. 统计频次（默认）

```python
data['Gender'].value_counts()
# Male      523
# Female    477
```

### 2. 统计占比

```python
data['Gender'].value_counts(normalize=True)
# Male      0.523
# Female    0.477
```

### 3. 升序排列

```python
data['TrafficEvent'].value_counts(ascending=True)
# Breakdown      140  ← 最少
# Accident       180
# Traffic Jam    230
# Normal         450  ← 最多
```

### 4. 包含缺失值

```python
data['column'].value_counts(dropna=False)
# 会显示 NaN 的数量
```

## 对比其他方法

| 方法 | 代码 | 适用场景 |
|---|---|---|
| `value_counts()` | `data['col'].value_counts()` | 单列频次统计，自动排序 |
| `groupby().count()` | `data.groupby('col').size()` | 多列分组统计 |
| `len()` | `len(data[data['col'] == 'A'])` | 统计单个值的数量 |

## 典型应用

### 1. 数据探索

```python
# 快速了解分类字段的分布
print(data['TrafficEvent'].value_counts())
print(data['Gender'].value_counts())
```

### 2. 数据质量检查

```python
# 检查是否有异常分类值
print(data['Gender'].value_counts())
# Male      500
# Female    450
# Unknown    50  ← 发现异常值
```

### 3. 考试截图题

```python
# 统计每种交通事件的发生次数
traffic_event_counts = data['TrafficEvent'].value_counts()
print(traffic_event_counts)  # 截图保存
```

## 注意事项

- ⚠️ **默认降序排列**：最多的在最上面
- ⚠️ **返回的是 Series**：可以继续用索引访问 `counts['Normal']`
- ⚠️ **自动排除 NaN**：需要统计缺失值时加 `dropna=False`
