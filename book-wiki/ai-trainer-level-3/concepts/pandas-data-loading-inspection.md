# Pandas 数据加载与检查

**所属章节**: 2.1.4 医疗研究数据清洗和标注设计  
**难度**: ⭐⭐☆☆☆  
**重要性**: ⭐⭐⭐⭐⭐

---

## 概念说明

数据加载与检查是数据分析的第一步，用于将外部数据文件（如 CSV）读入 pandas DataFrame，并快速了解数据的结构、类型、完整性。

---

## 核心操作

### 1. 数据加载

```python
import pandas as pd

# 基本加载
data = pd.read_csv('data.csv')

# 指定编码（处理中文数据）
data = pd.read_csv('data.csv', encoding='gbk')  # 或 'utf-8'

# 其他常用参数
data = pd.read_csv('data.csv',
                   sep=',',           # 分隔符（默认逗号）
                   header=0,          # 第几行作为列名（默认第一行）
                   index_col=0,       # 第几列作为行索引
                   na_values=['NA', '?'])  # 自定义缺失值标记
```

### 2. 数据检查三件套

```python
# ① 查看数据类型
print(data.dtypes)
# 输出：PatientID    int64
#       Age          int64
#       Name         object  ← 字符串类型
#       Date         object  ← 需要转换为 datetime

# ② 查看表结构和内存信息
print(data.info())
# 输出：
# <class 'pandas.core.frame.DataFrame'>
# RangeIndex: 5441 entries, 0 to 5440
# Data columns (total 22 columns):
# #   Column  Non-Null Count  Dtype 
# 0   病人ID   5441 non-null   int64 
# 1   年龄     5441 non-null   int64 
# ...

# ③ 查看每列缺失值数量
print(data.isnull().sum())
# 输出：PatientID       0
#       Age            12
#       Name            5
```

### 3. 其他常用检查方法

```python
data.head()           # 查看前 5 行
data.head(10)         # 查看前 10 行
data.tail()           # 查看后 5 行

data.shape            # 数据形状：(行数, 列数)
data.columns          # 列名列表
data.describe()       # 数值列的统计摘要（均值、标准差、分位数）

data['Age'].value_counts()  # 某列的值分布统计
```

---

## 为什么需要检查

| 检查项 | 目的 | 发现的问题示例 |
|---|---|---|
| `dtypes` | 确认数据类型是否正确 | 日期被读成 object，需要 `pd.to_datetime()` |
| `info()` | 了解数据规模和完整性 | 5000 行数据，但某列只有 4800 非空值 |
| `isnull().sum()` | 定位缺失值 | Age 列有 12 个缺失值，需要填充或删除 |
| `describe()` | 发现数值异常 | 年龄最大值 999，明显异常 |

---

## 常见编码问题

### 为什么需要指定 `encoding='gbk'`？

```python
# 错误：不指定编码读取含中文的 CSV
data = pd.read_csv('medical_data.csv')
# UnicodeDecodeError: 'utf-8' codec can't decode byte 0xb2 in position 0

# 正确：指定 gbk 编码
data = pd.read_csv('medical_data.csv', encoding='gbk')
```

**原因**：
- pandas 默认使用 UTF-8 编码读取文件
- 很多中文 CSV 文件（尤其是 Excel 导出的）使用 **GBK 或 GB2312 编码**
- 编码不匹配会导致 `UnicodeDecodeError`

**常见编码**：
- `utf-8`：国际标准，支持所有语言
- `gbk` / `gb2312`：中文常用编码
- `latin1`：西欧语言

---

## 考试要点

1. **必须指定编码**：医疗、金融等含中文的数据文件通常是 gbk 编码
2. **三项检查顺序**：`dtypes` → `info()` → `isnull().sum()`
3. **日期识别**：CSV 中的日期默认读为 object（字符串），需要手动转换为 datetime

---

## 实战示例

```python
import pandas as pd

# 加载医疗数据
data = pd.read_csv('medical_data.csv', encoding='gbk')

# 快速检查
print("数据形状:", data.shape)                    # (5441, 22)
print("\n列名:", data.columns.tolist())
print("\n数据类型:\n", data.dtypes)
print("\n缺失值统计:\n", data.isnull().sum())
print("\n数值列统计:\n", data.describe())

# 发现问题：就诊日期是 object 类型，需要转换
print("\n就诊日期类型:", data['就诊日期'].dtype)   # object
data['就诊日期'] = pd.to_datetime(data['就诊日期'])
print("转换后类型:", data['就诊日期'].dtype)       # datetime64[ns]
```

---

## 关联知识

- [[pandas-read-csv]]：数据加载详解
- [[datetime-processing]]：日期类型转换
- [[data-cleaning-operations]]：数据清洗流程
