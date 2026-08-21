# 数据加载：pd.read_csv()

## 概念

读取 CSV 文件，返回 pandas DataFrame 对象。

## 语法

```python
df = pd.read_csv(filepath)
df = pd.read_csv(filepath, sep=',', header=0, encoding='utf-8')
```

## 参数

| 参数 | 默认值 | 说明 |
|---|---|---|
| `filepath` | 必填 | 文件路径（相对路径或绝对路径） |
| `sep` | `','` | 分隔符（CSV 默认逗号，TSV 用 `'\t'`） |
| `header` | `0` | 第几行作为列名（0=第一行，None=无列名） |
| `encoding` | `'utf-8'` | 文件编码（中文文件可能需要 `'gbk'` 或 `'gb18030'`） |
| `index_col` | `None` | 指定哪一列作为索引 |
| `usecols` | `None` | 只读取指定列（列表或函数） |

## 示例

```python
import pandas as pd

# 基本用法
data = pd.read_csv('auto-mpg.csv')

# 查看加载结果
print(data.head())      # 前 5 行
print(data.shape)       # (行数, 列数)
print(data.columns)     # 列名列表
print(data.dtypes)      # 每列的数据类型
```

## 常见问题与解决

### 问题 1：中文乱码

```python
# ❌ 错误（编码不匹配）
data = pd.read_csv('data.csv')  # 可能显示乱码

# ✅ 解决方案
data = pd.read_csv('data.csv', encoding='gbk')
# 或
data = pd.read_csv('data.csv', encoding='gb18030')
```

### 问题 2：文件路径找不到

```python
# ❌ 错误（路径写错）
data = pd.read_csv('data.csv')  # FileNotFoundError

# ✅ 解决方案 1：使用绝对路径
data = pd.read_csv('E:/AITraining/data/data.csv')

# ✅ 解决方案 2：确认当前工作目录
import os
print(os.getcwd())  # 打印当前目录
data = pd.read_csv('./data/data.csv')
```

### 问题 3：无列名的 CSV

```python
# 原始 CSV：
# 18,8,307,130,3504
# 15,8,350,165,3693

# ❌ 错误（第一行被当作列名）
data = pd.read_csv('no_header.csv')
# 结果：列名变成 ['18', '8', '307', ...]

# ✅ 正确（指定无列名）
data = pd.read_csv('no_header.csv', header=None)
# 结果：列名变成 [0, 1, 2, ...]

# ✅ 手动指定列名
data = pd.read_csv('no_header.csv', header=None, 
                   names=['mpg', 'cylinders', 'displacement', ...])
```

## 数据加载后的验证（最佳实践）

```python
# 加载数据
data = pd.read_csv('auto-mpg.csv')

# 验证步骤 1：查看形状
print(f"数据集大小：{data.shape[0]} 行 × {data.shape[1]} 列")

# 验证步骤 2：查看前几行
print(data.head())

# 验证步骤 3：查看数据类型
print(data.dtypes)

# 验证步骤 4：查看基本统计信息
print(data.describe())  # 数值列的均值、标准差、最小值、最大值等

# 验证步骤 5：检查缺失值
print(data.isnull().sum())
```

## 性能优化（大文件）

```python
# 只读取需要的列
data = pd.read_csv('large_file.csv', usecols=['mpg', 'weight', 'horsepower'])

# 分块读取（逐块处理）
chunk_size = 10000
for chunk in pd.read_csv('large_file.csv', chunksize=chunk_size):
    # 处理每个块
    print(chunk.shape)
```

## 关联操作

- [[concepts/isnull-sum]] 缺失值检测
- [[concepts/dropna]] 缺失值删除
- [[concepts/to-csv]] 保存为 CSV
- [[concepts/boolean-indexing]] 数据筛选
