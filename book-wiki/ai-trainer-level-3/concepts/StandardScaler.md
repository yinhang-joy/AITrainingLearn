# 特征标准化：StandardScaler

## 概念

将数值型特征标准化为均值=0、标准差=1 的分布，消除量纲差异。

## 语法

```python
from sklearn.preprocessing import StandardScaler

scaler = StandardScaler()
scaler.fit(X)                    # 学习参数（均值、标准差）
X_scaled = scaler.transform(X)   # 应用转换
X_scaled = scaler.fit_transform(X)  # 一步完成（推荐）
```

## 原理

$$
x_{\text{标准化}} = \frac{x - \mu}{\sigma}
$$

- $\mu$：该特征的均值
- $\sigma$：该特征的标准差
- 标准化后：均值 ≈ 0，标准差 ≈ 1

## 为什么需要标准化？

### 问题：量纲差异导致特征权重失衡

```python
# 汽车数据集示例
data = pd.DataFrame({
    'weight': [3504, 3693, 3436, 3433],      # 3000-5000 kg
    'acceleration': [12.0, 11.5, 11.0, 12.0] # 8-24 s
})

# 未标准化：模型会认为 weight 更重要（因为数值更大）
# 标准化后：两个特征在同一量纲下比较
```

### 需要标准化的算法

- 线性回归（Linear Regression）
- 逻辑回归（Logistic Regression）
- 支持向量机（SVM）
- K 近邻（KNN）
- 神经网络（Neural Networks）

### 不需要标准化的算法

- 决策树（Decision Tree）
- 随机森林（Random Forest）
- XGBoost / LightGBM

## 示例

### 示例 1：基本用法

```python
import pandas as pd
from sklearn.preprocessing import StandardScaler

# 原始数据
data = pd.DataFrame({
    'weight': [3504, 3693, 3436, 3433],
    'acceleration': [12.0, 11.5, 11.0, 12.0]
})

print("原始数据:")
print(data)
#    weight  acceleration
# 0    3504          12.0
# 1    3693          11.5
# 2    3436          11.0
# 3    3433          12.0

# 标准化
scaler = StandardScaler()
data_scaled = scaler.fit_transform(data)

print("\n标准化后:")
print(data_scaled)
#        weight  acceleration
# 0  [ 0.20,      1.13]
# 1  [ 1.79,      0.38]
# 2  [-0.65,     -1.13]
# 3  [-0.73,      1.13]
# ↑ 均值≈0，标准差≈1
```

### 示例 2：查看学习到的参数

```python
scaler = StandardScaler()
scaler.fit(data)

# 查看每列的均值
print("均值:", scaler.mean_)
# [3516.5   11.625]

# 查看每列的标准差
print("标准差:", scaler.scale_)
# [118.16    0.47]
```

### 示例 3：部分特征标准化（考试常见）

```python
# 只标准化数值型连续特征
numerical_features = ['displacement', 'horsepower', 'weight', 'acceleration']

# 创建标准化器
scaler = StandardScaler()

# 只对指定列标准化
data[numerical_features] = scaler.fit_transform(data[numerical_features])

# 其他列（如 cylinders / origin）保持不变
```

## fit vs transform vs fit_transform

| 方法 | 作用 | 适用场景 |
|---|---|---|
| `.fit(X)` | 学习参数（均值、标准差） | 训练集 |
| `.transform(X)` | 应用已学习的参数 | 测试集（使用训练集的参数） |
| `.fit_transform(X)` | 学习 + 应用（一步完成） | 训练集（推荐） |

```python
# 训练集：fit_transform（学习参数并应用）
X_train_scaled = scaler.fit_transform(X_train)

# 测试集：transform（使用训练集的参数）
X_test_scaled = scaler.transform(X_test)

# ❌ 错误（测试集不能 fit_transform）
X_test_scaled = scaler.fit_transform(X_test)  # 会导致数据泄露
```

## 标准化 vs 归一化

| 方法 | 公式 | 结果范围 | 适用场景 |
|---|---|---|---|
| StandardScaler（标准化） | $(x - \mu) / \sigma$ | 无固定范围（通常 -3 到 3） | 数据符合正态分布 |
| MinMaxScaler（归一化） | $(x - \min) / (\max - \min)$ | [0, 1] | 数据需要固定范围 |

```python
# StandardScaler（考试常用）
from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()
data_scaled = scaler.fit_transform(data)

# MinMaxScaler（特定场景）
from sklearn.preprocessing import MinMaxScaler
scaler = MinMaxScaler()
data_scaled = scaler.fit_transform(data)
```

## 注意事项

### ⚠️ 注意 1：只标准化特征 X，不标准化目标变量 y

```python
# ✅ 正确
X_scaled = scaler.fit_transform(X)
y = data['mpg']  # y 保持不变

# ❌ 错误（y 也标准化了，预测结果难以解释）
X_scaled = scaler.fit_transform(X)
y_scaled = scaler.fit_transform(y.values.reshape(-1, 1))
```

### ⚠️ 注意 2：不标准化类别特征

```python
# cylinders（气缸数）：4, 6, 8 → 离散特征，不标准化
# origin（产地）：1, 2, 3 → 类别特征，不标准化

# 只标准化连续数值特征
numerical_features = ['displacement', 'horsepower', 'weight', 'acceleration']
data[numerical_features] = scaler.fit_transform(data[numerical_features])
```

### ⚠️ 注意 3：训练集和测试集使用相同的标准化参数

```python
# ✅ 正确
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)  # 学习训练集的参数
X_test_scaled = scaler.transform(X_test)        # 使用训练集的参数

# ❌ 错误（测试集单独学习参数，导致数据泄露）
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.fit_transform(X_test)    # 错误！
```

## 易错点

### ⚠️ 错误 1：只 fit 不 transform

```python
# ❌ 错误（只学习参数，未应用）
scaler = StandardScaler()
scaler.fit(data[numerical_features])  # 数据未改变

# ✅ 正确（学习并应用）
scaler = StandardScaler()
data[numerical_features] = scaler.fit_transform(data[numerical_features])
```

### ⚠️ 错误 2：忘记赋值

```python
# ❌ 错误（计算结果未保存）
scaler = StandardScaler()
scaler.fit_transform(data[numerical_features])

# ✅ 正确
data[numerical_features] = scaler.fit_transform(data[numerical_features])
```

### ⚠️ 错误 3：对整个 DataFrame 标准化（包括非数值列）

```python
# ❌ 错误（car name 是文本列，无法标准化）
scaler = StandardScaler()
data_scaled = scaler.fit_transform(data)  # ValueError

# ✅ 正确（只标准化数值列）
numerical_features = ['displacement', 'horsepower', 'weight', 'acceleration']
data[numerical_features] = scaler.fit_transform(data[numerical_features])
```

## 完整示例：考试场景

```python
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split

# 加载数据
data = pd.read_csv('auto-mpg.csv')

# 数据清洗（略）
# ...

# 标准化数值型特征
numerical_features = ['displacement', 'horsepower', 'weight', 'acceleration']
scaler = StandardScaler()
data[numerical_features] = scaler.fit_transform(data[numerical_features])

# 分离特征和目标变量
X = data[['cylinders', 'displacement', 'horsepower', 'weight', 
          'acceleration', 'model year', 'origin']]
y = data['mpg']

# 划分数据集
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

print("标准化后的训练集:")
print(X_train.head())
```

## 关联操作

- [[concepts/train-test-split]] 数据集划分（标准化后进行）
- [[concepts/pd-to-numeric]] 数据类型转换（标准化前先转为数值）
- [[concepts/dropna]] 缺失值处理（标准化前先清理）
