# MinMax 归一化

**所属章节**: 2.1.4 医疗研究数据清洗和标注设计  
**难度**: ⭐⭐⭐☆☆  
**重要性**: ⭐⭐⭐⭐☆

---

## 概念说明

MinMax 归一化（也称最小-最大缩放）是一种数据预处理方法，将数值特征缩放到固定区间（通常是 [0, 1]），消除不同特征之间量纲和数值范围的差异。

---

## 为什么需要归一化

### 场景：医疗数据的量纲差异

```python
# 原始数据（不同特征的数值范围差异巨大）
年龄: 18, 25, 45, 67        # 范围 0-120
体重: 45.5, 68.2, 82.1      # 范围 40-100 kg
身高: 160, 175, 182         # 范围 150-190 cm

# 问题：如果直接用于机器学习
# - 体重和身高的数值远大于年龄，会主导模型训练
# - 距离计算（如 KNN）会被大数值特征主导
# - 梯度下降收敛慢（不同特征的梯度尺度差异大）
```

**归一化的好处**：
1. **消除量纲影响**：年龄（岁）、体重（kg）、身高（cm）统一到 [0, 1]
2. **加速模型收敛**：梯度下降算法在归一化数据上更快
3. **提升模型性能**：某些算法（如神经网络、KNN、SVM）对数值范围敏感

---

## 核心操作

### 1. MinMaxScaler 基本用法

```python
from sklearn.preprocessing import MinMaxScaler

# 创建归一化器
scaler = MinMaxScaler()

# 归一化单列
data['年龄'] = scaler.fit_transform(data[['年龄']])

# 归一化多列
columns_to_normalize = ['年龄', '体重', '身高']
data[columns_to_normalize] = scaler.fit_transform(data[columns_to_normalize])
```

**重要**：
- `fit_transform()` 需要传入 **二维数组**：`data[['列名']]` 或 `data[['列1', '列2']]`
- 单列也要双层方括号：`data[['年龄']]`（形状是 (n, 1)），不能用 `data['年龄']`（形状是 (n,)）

### 2. 归一化公式

```python
# MinMax 归一化公式
归一化值 = (原始值 - 最小值) / (最大值 - 最小值)

# 示例：年龄 [18, 25, 45, 67, 120]
最小值 = 18, 最大值 = 120
45 归一化后 = (45 - 18) / (120 - 18) = 27 / 102 ≈ 0.265
```

**结果范围**：
- 最小值归一化为 0
- 最大值归一化为 1
- 中间值在 0 和 1 之间

### 3. 指定归一化区间

```python
# 归一化到 [0, 1]（默认）
scaler = MinMaxScaler()

# 归一化到 [-1, 1]
scaler = MinMaxScaler(feature_range=(-1, 1))

# 归一化到 [0, 100]
scaler = MinMaxScaler(feature_range=(0, 100))
```

---

## 完整示例

### 场景：医疗数据归一化

```python
import pandas as pd
from sklearn.preprocessing import MinMaxScaler

# 加载数据
data = pd.read_csv('medical_data.csv', encoding='gbk')

# 查看原始数据
print("归一化前:")
print(data[['年龄', '体重', '身高']].describe())
#         年龄        体重        身高
# mean   45.2      68.5      170.3
# min    18.0      45.0      150.0
# max   120.0     100.0      190.0

# 创建归一化器
scaler = MinMaxScaler()

# 归一化
columns_to_normalize = ['年龄', '体重', '身高']
data[columns_to_normalize] = scaler.fit_transform(data[columns_to_normalize])

# 查看归一化后数据
print("\n归一化后:")
print(data[['年龄', '体重', '身高']].describe())
#         年龄      体重      身高
# mean   0.267    0.427    0.507
# min    0.000    0.000    0.000
# max    1.000    1.000    1.000

# 查看部分数据
print("\n示例数据:")
print(data[['年龄', '体重', '身高']].head())
#      年龄      体重      身高
# 0  0.265    0.427    0.500
# 1  0.196    0.527    0.625
# 2  0.088    0.436    0.550
```

---

## 常见错误与解决方案

### 错误 1：传入一维数组

```python
# 错误示例
data['年龄'] = scaler.fit_transform(data['年龄'])
# ValueError: Expected 2D array, got 1D array instead

# 原因：data['年龄'] 是 Series（一维），MinMaxScaler 需要二维数组

# 正确做法：使用双层方括号
data['年龄'] = scaler.fit_transform(data[['年龄']])
```

### 错误 2：归一化前有缺失值

```python
# 错误示例
data[['年龄', '体重']] = scaler.fit_transform(data[['年龄', '体重']])
# 如果有 NaN，结果全是 NaN

# 解决方案 1：先删除缺失值
data = data.dropna(subset=['年龄', '体重'])

# 解决方案 2：先填充缺失值
data['年龄'].fillna(data['年龄'].mean(), inplace=True)
data['体重'].fillna(data['体重'].median(), inplace=True)

# 再归一化
data[['年龄', '体重']] = scaler.fit_transform(data[['年龄', '体重']])
```

### 错误 3：训练集和测试集分别归一化

```python
# 错误示例（数据泄露）
train[['年龄']] = MinMaxScaler().fit_transform(train[['年龄']])
test[['年龄']] = MinMaxScaler().fit_transform(test[['年龄']])
# 问题：训练集和测试集的归一化范围不同

# 正确做法：先在训练集上 fit，再对测试集 transform
scaler = MinMaxScaler()
train[['年龄']] = scaler.fit_transform(train[['年龄']])    # fit + transform
test[['年龄']] = scaler.transform(test[['年龄']])           # 只 transform
```

---

## 归一化 vs 标准化

| 方法 | 公式 | 结果范围 | 适用场景 |
|---|---|---|---|
| **MinMax 归一化** | `(x - min) / (max - min)` | [0, 1] | 数据分布均匀，无极端异常值 |
| **Z-score 标准化** | `(x - mean) / std` | 无固定范围 | 数据呈正态分布，有异常值时更稳健 |

**选择建议**：
- **MinMax**：数据范围有界（如年龄 0-120），需要固定区间时
- **StandardScaler**：数据有异常值，或需要保留分布形状时

---

## 考试要点

1. **导入正确的包**：`from sklearn.preprocessing import MinMaxScaler`
2. **双层方括号**：`data[['列名']]` 传入二维数组
3. **fit_transform 一步到位**：`scaler.fit_transform(data[cols])`
4. **归一化前处理缺失值**：否则结果全是 NaN

---

## 实战代码

```python
from sklearn.preprocessing import MinMaxScaler
import pandas as pd

# 加载数据
data = pd.read_csv('medical_data.csv', encoding='gbk')

# 创建归一化器
scaler = MinMaxScaler()

# 归一化多列
columns_to_normalize = ['年龄', '体重', '身高']
data[columns_to_normalize] = scaler.fit_transform(data[columns_to_normalize])

# 查看结果
print(data[columns_to_normalize].head())
print(data[columns_to_normalize].describe())
```

---

## 关联知识

- [[data-cleaning-operations]]：数据清洗操作
- [[pandas-data-loading-inspection]]：数据加载与检查
