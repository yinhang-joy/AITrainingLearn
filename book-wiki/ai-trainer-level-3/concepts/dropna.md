# dropna —— 删除缺失值

## 基本用法

```python
data = data.dropna()
```

**作用**：删除 DataFrame 中包含缺失值（NaN）的所有行

## 参数说明

```python
data.dropna(axis=0, how='any', subset=None)
```

| 参数 | 默认值 | 说明 |
|---|---|---|
| `axis` | `0` | `0`=删除行，`1`=删除列 |
| `how` | `'any'` | `'any'`=只要有 NaN 就删，`'all'`=全是 NaN 才删 |
| `subset` | `None` | 指定检查哪些列（列表） |

## 示例

```python
# 删除任何包含 NaN 的行
data = data.dropna()

# 仅删除指定列有 NaN 的行
data = data.dropna(subset=['Age', 'Speed'])

# 删除全是 NaN 的行
data = data.dropna(how='all')
```

## 对比 fillna

| 方法 | 处理方式 | 适用场景 |
|---|---|---|
| `dropna()` | 删除包含 NaN 的行 | 缺失值少，删除不影响数据量 |
| `fillna()` | 用其他值填充 NaN | 缺失值多，保留数据完整性 |

## 注意事项

- ⚠️ **必须在类型转换之前调用**：`NaN` 无法转换为 `int` 类型
- 正确顺序：`data.dropna()` → `data['Age'].astype(int)`
- ⚠️ **会修改数据量**：使用前检查 `data.shape` 确认删除的行数是否合理
