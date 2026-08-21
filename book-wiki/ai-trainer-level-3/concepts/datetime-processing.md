# 日期时间处理

**所属章节**: 2.1.4 医疗研究数据清洗和标注设计  
**难度**: ⭐⭐⭐☆☆  
**重要性**: ⭐⭐⭐⭐☆

---

## 概念说明

日期时间处理是指将字符串格式的日期转换为 pandas 的 datetime 类型，并进行日期计算、格式化、提取等操作。医疗、金融等领域常需要计算日期差值（如住院天数、贷款期限）。

---

## 核心操作

### 1. 日期格式转换 `pd.to_datetime()`

```python
import pandas as pd

# 转换单个日期
date_str = '2023-04-25'
date_obj = pd.to_datetime(date_str)
print(type(date_obj))  # <class 'pandas._libs.tslibs.timestamps.Timestamp'>

# 转换 DataFrame 的日期列
data['就诊日期'] = pd.to_datetime(data['就诊日期'])
data['诊断日期'] = pd.to_datetime(data['诊断日期'])

# 查看转换后的类型
print(data['就诊日期'].dtype)  # datetime64[ns]
```

**支持的输入格式**（自动识别）：
- `2023-04-25` / `2023/04/25` / `2023.04.25`
- `Apr 25, 2023` / `25-Apr-2023`
- `20230425`（需要指定 `format='%Y%m%d'`）

### 2. 日期差值计算

```python
# 计算两个日期列的差值
data['诊断延迟'] = data['诊断日期'] - data['就诊日期']
# 结果类型：Timedelta（时间差对象，如 "21 days"）

# 提取天数（整数）
data['诊断延迟'] = (data['诊断日期'] - data['就诊日期']).dt.days
# 结果：21, 45, -3, ... （整数）

# 计算到当前日期的差值
from datetime import datetime
current_date = datetime(2024, 9, 1)
data['病程'] = (current_date - data['诊断日期']).dt.days
```

**重要**：
- **两个 datetime 相减 = Timedelta 对象**
- **`.dt.days` 提取整数天数**，否则无法进行数值比较

### 3. `.dt` 访问器（提取日期组件）

```python
data['年份'] = data['就诊日期'].dt.year       # 2023
data['月份'] = data['就诊日期'].dt.month      # 4
data['日'] = data['就诊日期'].dt.day          # 25
data['星期'] = data['就诊日期'].dt.dayofweek  # 0=周一, 6=周日
data['季度'] = data['就诊日期'].dt.quarter    # 1-4

# 格式化输出
data['日期字符串'] = data['就诊日期'].dt.strftime('%Y年%m月%d日')
# 输出：'2023年04月25日'
```

---

## 日期差值处理流程

### 场景：计算诊断延迟和病程

```python
from datetime import datetime
import pandas as pd

# 1. 转换日期列
data['就诊日期'] = pd.to_datetime(data['就诊日期'])
data['诊断日期'] = pd.to_datetime(data['诊断日期'])

# 2. 计算诊断延迟（诊断日期 - 就诊日期）
data['诊断延迟'] = (data['诊断日期'] - data['就诊日期']).dt.days

# 3. 计算病程（当前日期 - 诊断日期）
current_date = datetime(2024, 9, 1)
data['病程'] = (current_date - data['诊断日期']).dt.days

# 4. 检查异常值
print(data[data['诊断延迟'] < 0])  # 诊断早于就诊，不合理
print(data[data['病程'] < 0])       # 诊断日期在未来，不合理
```

---

## 常见问题与解决方案

### 问题 1：日期列类型是 object，无法计算

```python
# 错误示例
data['就诊日期'] - data['诊断日期']
# TypeError: unsupported operand type(s) for -: 'str' and 'str'

# 解决方案：先转换为 datetime
data['就诊日期'] = pd.to_datetime(data['就诊日期'])
data['诊断日期'] = pd.to_datetime(data['诊断日期'])
data['诊断延迟'] = (data['诊断日期'] - data['就诊日期']).dt.days
```

### 问题 2：忘记 `.dt.days`，结果是 Timedelta 对象

```python
# 错误示例
data['诊断延迟'] = data['诊断日期'] - data['就诊日期']
print(data['诊断延迟'])
# 输出：0    21 days
#       1    45 days
#       2   -3 days

# 无法进行数值比较
data[data['诊断延迟'] >= 0]  # 报错！

# 正确做法：加 .dt.days
data['诊断延迟'] = (data['诊断日期'] - data['就诊日期']).dt.days
print(data['诊断延迟'])
# 输出：0    21
#       1    45
#       2    -3

data[data['诊断延迟'] >= 0]  # 正常筛选
```

### 问题 3：日期格式不统一

```python
# 数据中有多种日期格式
# 2023-4-4, 2023/04/25, Apr 25 2023

# pd.to_datetime 自动识别大部分格式
data['就诊日期'] = pd.to_datetime(data['就诊日期'])

# 如果报错，尝试指定格式或启用推断
data['就诊日期'] = pd.to_datetime(data['就诊日期'], format='%Y-%m-%d', errors='coerce')
# errors='coerce'：无法解析的日期转为 NaT（缺失值）
```

---

## 考试要点

1. **必须先转换为 datetime**：`pd.to_datetime()` 是前提
2. **日期差值必须用 `.dt.days`**：否则无法进行数值比较和筛选
3. **异常值检查**：诊断日期早于就诊日期、病程为负数等不合理情况
4. **括号不能少**：`(date2 - date1).dt.days`，括号确保先计算差值再提取天数

---

## 实战示例

```python
import pandas as pd
from datetime import datetime

# 加载数据
data = pd.read_csv('medical_data.csv', encoding='gbk')

# 转换日期格式
data['就诊日期'] = pd.to_datetime(data['就诊日期'])
data['诊断日期'] = pd.to_datetime(data['诊断日期'])

# 计算诊断延迟
data['诊断延迟'] = (data['诊断日期'] - data['就诊日期']).dt.days

# 计算病程
data['病程'] = (datetime(2024, 9, 1) - data['诊断日期']).dt.days

# 删除不合理数据
print(f"清洗前: {len(data)} 行")
data = data[(data['诊断延迟'] >= 0) & (data['病程'] > 0)]
print(f"清洗后: {len(data)} 行")

# 查看结果
print(data[['就诊日期', '诊断日期', '诊断延迟', '病程']].head())
```

---

## 关联知识

- [[pandas-data-loading-inspection]]：数据加载与检查
- [[data-cleaning-operations]]：数据清洗操作
- [[boolean-indexing]]：布尔索引过滤
