# 数据清洗操作

**所属章节**: 2.1.4 医疗研究数据清洗和标注设计  
**难度**: ⭐⭐⭐☆☆  
**重要性**: ⭐⭐⭐⭐⭐

---

## 概念说明

数据清洗是指对原始数据进行预处理，去除或修正不合理、不一致、重复的数据，使其符合分析和建模要求。常见操作包括修改列名、删除重复值、过滤异常数据。

---

## 核心操作

### 1. 修改列名 `rename()`

```python
# 修改单个列名
data.rename(columns={'病人ID': '患者ID'}, inplace=True)

# 修改多个列名
data.rename(columns={
    '病人ID': '患者ID',
    '就诊日期': 'visit_date',
    '诊断日期': 'diagnosis_date'
}, inplace=True)

# 批量修改（如统一转为小写）
data.columns = data.columns.str.lower()

# 不使用 inplace（返回新 DataFrame）
data_new = data.rename(columns={'病人ID': '患者ID'})
```

**参数说明**：
- `columns`：字典，键为旧列名，值为新列名
- `inplace=True`：原地修改，不返回新对象（节省内存）

### 2. 删除重复值 `drop_duplicates()`

```python
# 删除完全重复的行（所有列都相同）
initial_rows = data.shape[0]
data.drop_duplicates(inplace=True)
deleted_rows = initial_rows - data.shape[0]
print(f'删除的重复行数: {deleted_rows}')

# 基于特定列判断重复（只看这几列）
data.drop_duplicates(subset=['患者ID', '就诊日期'], inplace=True)

# 保留最后一次出现的记录（默认保留第一次）
data.drop_duplicates(keep='last', inplace=True)
```

**参数说明**：
- `subset`：指定用于判断重复的列，默认全部列
- `keep`：保留策略
  - `'first'`（默认）：保留第一次出现的行
  - `'last'`：保留最后一次出现的行
  - `False`：删除所有重复行（包括第一次出现的）

### 3. 多条件过滤（布尔索引）

```python
# 单条件过滤
data = data[data['年龄'] < 120]

# 多条件过滤（与逻辑 &）
data = data[(data['诊断延迟'] >= 0) & 
            (data['病程'] > 0) & 
            (data['年龄'] < 120)]

# 多条件过滤（或逻辑 |）
data = data[(data['疾病类型'] == '糖尿病') | 
            (data['疾病类型'] == '高血压')]

# 排除条件（非逻辑 ~）
data = data[~(data['治疗结果'] == '死亡')]

# 范围过滤
data = data[(data['年龄'] >= 18) & (data['年龄'] <= 65)]
# 或使用 between
data = data[data['年龄'].between(18, 65)]
```

**重要规则**：
- **每个条件必须加括号**：`(条件1) & (条件2)`
- **与 `&`、或 `|`、非 `~`**：不能用 `and` / `or` / `not`
- **`&` 优先级高于比较运算符**，不加括号会报错

---

## 数据清洗完整流程

### 场景：医疗数据异常值处理

```python
import pandas as pd
from datetime import datetime

# 1. 加载数据
data = pd.read_csv('medical_data.csv', encoding='gbk')
print(f"原始数据: {data.shape[0]} 行")

# 2. 修改列名
data.rename(columns={'病人ID': '患者ID'}, inplace=True)

# 3. 日期转换
data['就诊日期'] = pd.to_datetime(data['就诊日期'])
data['诊断日期'] = pd.to_datetime(data['诊断日期'])

# 4. 计算新字段
data['诊断延迟'] = (data['诊断日期'] - data['就诊日期']).dt.days
data['病程'] = (datetime(2024, 9, 1) - data['诊断日期']).dt.days

# 5. 删除不合理数据（多条件过滤）
data = data[(data['诊断延迟'] >= 0) &    # 诊断不能早于就诊
            (data['病程'] > 0) &           # 病程必须为正
            (data['年龄'] > 0) &           # 年龄必须大于0
            (data['年龄'] < 120) &         # 年龄上限
            (data['体重'] > 20) &          # 体重下限
            (data['体重'] < 200) &         # 体重上限
            (data['身高'] > 50) &          # 身高下限
            (data['身高'] < 250)]          # 身高上限
print(f"过滤后: {data.shape[0]} 行")

# 6. 删除重复值
initial_rows = data.shape[0]
data.drop_duplicates(inplace=True)
deleted_rows = initial_rows - data.shape[0]
print(f"删除重复行: {deleted_rows} 行")

# 7. 删除缺失值（可选）
data.dropna(subset=['患者ID', '疾病类型'], inplace=True)

print(f"最终数据: {data.shape[0]} 行")
```

---

## 常见错误与解决方案

### 错误 1：多条件过滤不加括号

```python
# 错误示例
data = data[data['年龄'] > 0 & data['年龄'] < 120]
# ValueError: The truth value of a Series is ambiguous

# 原因：& 优先级高于 >，实际运算是 data['年龄'] > (0 & data['年龄']) < 120

# 正确做法：每个条件加括号
data = data[(data['年龄'] > 0) & (data['年龄'] < 120)]
```

### 错误 2：使用 and/or 而非 &/|

```python
# 错误示例
data = data[(data['年龄'] > 0) and (data['年龄'] < 120)]
# ValueError: The truth value of a Series is ambiguous

# 原因：and/or 用于标量布尔值，不支持 Series

# 正确做法：使用 & 和 |
data = data[(data['年龄'] > 0) & (data['年龄'] < 120)]
data = data[(data['疾病类型'] == '糖尿病') | (data['疾病类型'] == '高血压')]
```

### 错误 3：忘记 inplace，修改未生效

```python
# 错误示例
data.rename(columns={'病人ID': '患者ID'})  # 返回新对象，data 未改变
print(data.columns)  # 还是 '病人ID'

# 正确做法 1：使用 inplace=True
data.rename(columns={'病人ID': '患者ID'}, inplace=True)

# 正确做法 2：重新赋值
data = data.rename(columns={'病人ID': '患者ID'})
```

---

## 数据清洗规范示例

### 医疗数据清洗规范（考试答题卷参考）

1. **日期一致性**：就诊日期 ≤ 诊断日期 ≤ 当前日期
2. **年龄合理性**：0 < 年龄 < 120
3. **体重合理性**：20 kg < 体重 < 200 kg
4. **身高合理性**：50 cm < 身高 < 250 cm
5. **重复记录处理**：删除患者ID、就诊日期、疾病类型完全相同的记录
6. **缺失值处理**：关键字段（患者ID、疾病类型）不允许缺失

---

## 考试要点

1. **`rename()` 必须指定 columns 参数**：`rename(columns={...})`
2. **多条件过滤必须加括号**：`(条件1) & (条件2)`
3. **使用 `&` 和 `|`，不用 `and` 和 `or`**
4. **记录删除的行数**：`initial_rows - data.shape[0]`

---

## 实战示例

```python
import pandas as pd

# 加载数据
data = pd.read_csv('medical_data.csv', encoding='gbk')

# 修改列名
data.rename(columns={'病人ID': '患者ID'}, inplace=True)

# 删除重复值并记录
initial_rows = data.shape[0]
data.drop_duplicates(inplace=True)
print(f'删除重复行: {initial_rows - data.shape[0]} 行')

# 多条件过滤异常数据
data = data[(data['年龄'] > 0) & (data['年龄'] < 120) & 
            (data['体重'] > 20) & (data['体重'] < 200)]

print(f'清洗后数据: {data.shape[0]} 行')
```

---

## 关联知识

- [[boolean-indexing]]：布尔索引详解
- [[datetime-processing]]：日期时间处理
- [[dropna-missing-values]]：缺失值处理
