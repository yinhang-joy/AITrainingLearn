# 跨列比较：列间关系验证

## 概念

通过比较运算符对 DataFrame 的多个列进行逐行比较，验证列间的业务逻辑关系。

## 语法

```python
df['列A'] > df['列B']                    # 简单比较
df['列A'] < (df['列B'] * 系数)          # 带计算的比较
df['列A'] == df['列B'] + df['列C']      # 多列计算
```

## 原理

pandas 列运算是**逐行计算**的：
1. 先对列进行运算（加减乘除），得到新的 Series
2. 再进行比较，返回布尔 Series（每行是 True/False）

## 示例

### 场景1：收入与贷款关系

```python
import pandas as pd

data = pd.DataFrame({
    'CustomerID': [1, 2, 3, 4],
    'Income': [10000, 8000, 15000, 5000],
    'LoanAmount': [30000, 35000, 50000, 20000]
})

# 贷款金额应小于收入的 5 倍
data['is_loan_valid'] = data['LoanAmount'] < (data['Income'] * 5)
print(data)
#    CustomerID  Income  LoanAmount  is_loan_valid
# 0           1   10000       30000           True  ← 30000 < 50000
# 1           2    8000       35000           True  ← 35000 < 40000
# 2           3   15000       50000           True  ← 50000 < 75000
# 3           4    5000       20000           True  ← 20000 < 25000
```

### 场景2：价格一致性检查

```python
orders = pd.DataFrame({
    'Price': [100, 200, 150],
    'Quantity': [2, 3, 4],
    'Total': [200, 600, 500]  # 第3行有错误
})

# 总价应等于单价×数量
orders['is_total_correct'] = orders['Total'] == (orders['Price'] * orders['Quantity'])
print(orders)
#    Price  Quantity  Total  is_total_correct
# 0    100         2    200              True
# 1    200         3    600              True
# 2    150         4    500             False  ← 应该是 600
```

### 场景3：日期逻辑检查

```python
events = pd.DataFrame({
    'StartDate': ['2024-01-01', '2024-02-01', '2024-03-01'],
    'EndDate': ['2024-01-10', '2024-01-25', '2024-03-15']
})

events['StartDate'] = pd.to_datetime(events['StartDate'])
events['EndDate'] = pd.to_datetime(events['EndDate'])

# 结束日期应晚于开始日期
events['is_date_valid'] = events['EndDate'] > events['StartDate']
print(events)
#    StartDate    EndDate  is_date_valid
# 0 2024-01-01 2024-01-10           True
# 1 2024-02-01 2024-01-25          False  ← 结束早于开始
# 2 2024-03-01 2024-03-15           True
```

## 常见业务场景

| 业务规则 | pandas 写法 |
|---|---|
| 贷款金额 < 收入的5倍 | `df['LoanAmount'] < (df['Income'] * 5)` |
| 收入 > 支出 | `df['Income'] > df['Expense']` |
| 总价 = 单价 × 数量 | `df['Total'] == (df['Price'] * df['Quantity'])` |
| 年龄 > 工龄 | `df['Age'] > df['WorkYears']` |
| 结束时间 > 开始时间 | `df['EndTime'] > df['StartTime']` |
| 折扣价 < 原价 | `df['DiscountPrice'] < df['OriginalPrice']` |

## 易错点

### ⚠️ 陷阱1：括号丢失

```python
# ❌ 错误（运算符优先级导致逻辑错误）
df['LoanAmount'] < df['Income'] * 5
# 相当于 (df['LoanAmount'] < df['Income']) * 5

# ✅ 正确
df['LoanAmount'] < (df['Income'] * 5)
```

### ⚠️ 陷阱2：缺失值导致 NaN 结果

```python
data = pd.DataFrame({
    'A': [10, None, 30],
    'B': [5, 20, 15]
})

print(data['A'] > data['B'])
# 0     True
# 1      NaN  ← 缺失值参与比较返回 NaN
# 2     True

# 处理方法1：视 NaN 为不合理
(data['A'] > data['B']).fillna(False)

# 处理方法2：排除缺失值后再比较
data['A'].notnull() & (data['A'] > data['B'])
```

### ⚠️ 陷阱3：浮点数相等比较

```python
# ❌ 不可靠（浮点数精度问题）
df['Total'] == (df['Price'] * df['Quantity'])

# ✅ 推荐（容忍微小误差）
import numpy as np
np.isclose(df['Total'], df['Price'] * df['Quantity'])
```

## 组合多条件

```python
# 同时满足多个关系
valid = (df['LoanAmount'] < df['Income'] * 5) & \
        (df['LoanAmount'] > 1000) & \
        (df['Income'] > 2000)

# 至少满足一个
valid = (df['Income'] > 10000) | (df['CreditScore'] > 700)
```

## 关联操作

- [[between-range-check]] 单列区间验证
- [[boolean-indexing]] 布尔索引筛选
- [[boolean-column-assignment]] 结果赋值到新列
