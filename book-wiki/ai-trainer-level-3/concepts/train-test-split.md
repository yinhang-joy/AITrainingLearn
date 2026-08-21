# 数据集划分：train_test_split

## 概念

将数据集随机划分为训练集和测试集，用于模型训练和评估。

## 语法

```python
from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)
```

## 参数

| 参数 | 默认值 | 说明 |
|---|---|---|
| `X` | 必填 | 特征矩阵（自变量） |
| `y` | 必填 | 目标变量（因变量） |
| `test_size` | `0.25` | 测试集比例（0.2 表示 20%） |
| `train_size` | `None` | 训练集比例（不填时自动计算） |
| `random_state` | `None` | 随机种子（固定后每次划分结果一致） |
| `shuffle` | `True` | 是否随机打乱数据 |
| `stratify` | `None` | 分层采样（保持类别比例） |

## 为什么需要划分数据集？

### 训练集 vs 测试集

| 数据集 | 用途 | 占比 | 特点 |
|---|---|---|---|
| **训练集** | 训练模型（学习规律） | 70-80% | 模型"见过"的数据 |
| **测试集** | 评估模型（验证泛化能力） | 20-30% | 模型"没见过"的数据 |

### 避免过拟合

```python
# ❌ 错误：用全部数据训练和测试（过拟合）
model.fit(X, y)
score = model.score(X, y)  # 100% 准确率（但实际应用效果差）

# ✅ 正确：训练集训练，测试集评估
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
model.fit(X_train, y_train)
score = model.score(X_test, y_test)  # 真实的泛化能力
```

## 示例

### 示例 1：基本用法（考试常见）

```python
import pandas as pd
from sklearn.model_selection import train_test_split

# 准备数据
X = data[['cylinders', 'displacement', 'horsepower', 'weight', 
          'acceleration', 'model year', 'origin']]
y = data['mpg']

# 划分数据集（训练集 80%，测试集 20%）
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

print(f"训练集大小：{len(X_train)} 行")
print(f"测试集大小：{len(X_test)} 行")
# 输出示例：
# 训练集大小：318 行（80%）
# 测试集大小：80 行（20%）
```

### 示例 2：查看划分结果

```python
print("X_train 形状:", X_train.shape)  # (318, 7)
print("X_test 形状:", X_test.shape)    # (80, 7)
print("y_train 形状:", y_train.shape)  # (318,)
print("y_test 形状:", y_test.shape)    # (80,)

# 验证：训练集 + 测试集 = 原数据集
assert len(X_train) + len(X_test) == len(X)
```

### 示例 3：random_state 的作用

```python
# 不设置 random_state（每次运行结果不同）
X_train1, X_test1, y_train1, y_test1 = train_test_split(X, y, test_size=0.2)
X_train2, X_test2, y_train2, y_test2 = train_test_split(X, y, test_size=0.2)
print(X_train1.equals(X_train2))  # False（划分结果不同）

# 设置 random_state（每次运行结果相同）
X_train1, X_test1, y_train1, y_test1 = train_test_split(X, y, test_size=0.2, random_state=42)
X_train2, X_test2, y_train2, y_test2 = train_test_split(X, y, test_size=0.2, random_state=42)
print(X_train1.equals(X_train2))  # True（划分结果相同）
```

## 常见划分比例

| 数据集规模 | 训练集 | 测试集 | 说明 |
|---|---|---|---|
| 小（< 1000 行） | 70% | 30% | 测试集需要足够样本 |
| 中（1000-10000 行） | 80% | 20% | **考试常用** |
| 大（> 10000 行） | 90% | 10% | 训练集更多，模型更准确 |

## 参数详解

### test_size vs train_size

```python
# 方式 1：指定测试集比例（推荐）
train_test_split(X, y, test_size=0.2)  # 测试集 20%，训练集自动 80%

# 方式 2：指定训练集比例
train_test_split(X, y, train_size=0.8)  # 训练集 80%，测试集自动 20%

# 方式 3：同时指定（必须和为 1）
train_test_split(X, y, train_size=0.8, test_size=0.2)
```

### random_state（随机种子）

```python
# 不设置：每次运行结果不同（不可复现）
train_test_split(X, y, test_size=0.2)

# 设置固定值：结果可复现（考试推荐）
train_test_split(X, y, test_size=0.2, random_state=42)

# random_state 的值可以是任意整数（42、0、100、2024 等）
# 约定俗成用 42（来自《银河系漫游指南》）
```

### stratify（分层采样）

```python
# 不分层：随机划分（可能导致类别比例不均）
train_test_split(X, y, test_size=0.2)

# 分层采样：保持训练集和测试集的类别比例与原数据一致
train_test_split(X, y, test_size=0.2, stratify=y)
# 适用场景：分类问题，且类别不平衡（如正样本 90%，负样本 10%）
```

## 易错点

### ⚠️ 错误 1：参数顺序错误

```python
# ❌ 错误（参数顺序错误）
train_test_split(0.2, X, y)  # TypeError

# ❌ 错误（test_size 放在前面）
train_test_split(test_size=0.2, X, y)  # 语法错误

# ✅ 正确（X, y 在前，参数在后）
train_test_split(X, y, test_size=0.2, random_state=42)
```

### ⚠️ 错误 2：test_size 理解错误

```python
# ❌ 错误（test_size=0.8 表示测试集 80%，训练集只有 20%）
train_test_split(X, y, test_size=0.8)

# ✅ 正确（test_size=0.2 表示测试集 20%，训练集 80%）
train_test_split(X, y, test_size=0.2)
```

### ⚠️ 错误 3：返回值顺序错误

```python
# ❌ 错误（返回值顺序错误）
X_test, X_train, y_test, y_train = train_test_split(X, y, test_size=0.2)

# ✅ 正确（返回顺序：X_train, X_test, y_train, y_test）
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
```

### ⚠️ 错误 4：只划分 X，不划分 y

```python
# ❌ 错误（y 没有划分）
X_train, X_test = train_test_split(X, test_size=0.2)
# 结果：无法训练模型（缺少 y_train）

# ✅ 正确（同时划分 X 和 y）
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
```

## 完整示例：考试场景

```python
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split

# 加载和清洗数据
data = pd.read_csv('auto-mpg.csv')
data = data.dropna()
data['horsepower'] = pd.to_numeric(data['horsepower'], errors='coerce')
data = data.dropna()

# 标准化
numerical_features = ['displacement', 'horsepower', 'weight', 'acceleration']
scaler = StandardScaler()
data[numerical_features] = scaler.fit_transform(data[numerical_features])

# 分离特征和目标变量
selected_features = ['cylinders', 'displacement', 'horsepower', 'weight', 
                     'acceleration', 'model year', 'origin']
X = data[selected_features]
y = data['mpg']

# 划分数据集（训练集 80%，测试集 20%）
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

print(f"训练集：{len(X_train)} 行")
print(f"测试集：{len(X_test)} 行")

# 后续：使用 X_train 和 y_train 训练模型
# model.fit(X_train, y_train)
# score = model.score(X_test, y_test)
```

## 三元划分（进阶，考试不涉及）

```python
# 划分为训练集、验证集、测试集
X_train, X_temp, y_train, y_temp = train_test_split(X, y, test_size=0.3, random_state=42)
X_val, X_test, y_val, y_test = train_test_split(X_temp, y_temp, test_size=0.5, random_state=42)

# 结果：训练集 70%，验证集 15%，测试集 15%
```

## 关联操作

- [[concepts/StandardScaler]] 特征标准化（划分前进行）
- [[concepts/dropna]] 缺失值处理（划分前进行）
- [[concepts/to-csv]] 保存划分后的数据
