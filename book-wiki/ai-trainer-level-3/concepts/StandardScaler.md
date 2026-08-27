# StandardScaler

## 一句话说明

sklearn 标准化工具，将数据转换为均值 0、标准差 1 的分布（Z-score 标准化）。

## 语法

```python
from sklearn.preprocessing import StandardScaler

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)  # 训练集
X_test_scaled = scaler.transform(X_test)  # 测试集
```

## 公式

$$z = \frac{x - \mu}{\sigma}$$

- $x$: 原始值
- $\mu$: 均值
- $\sigma$: 标准差
- $z$: 标准化后的值

## 参数说明

StandardScaler 默认参数适用于大多数场景，一般不需要调整。

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `copy` | 是否复制数据 | True |
| `with_mean` | 是否减去均值 | True |
| `with_std` | 是否除以标准差 | True |

## 示例

### 基本用法

```python
from sklearn.preprocessing import StandardScaler
import pandas as pd

# 原始数据
data = pd.DataFrame({
    'age': [25, 30, 35, 40, 45],
    'salary': [5000, 6000, 7000, 8000, 9000],
    'score': [60, 70, 80, 90, 100]
})

# 标准化数值列
numerical_features = ['age', 'salary', 'score']
scaler = StandardScaler()
data[numerical_features] = scaler.fit_transform(data[numerical_features])

print(data)
# 结果：均值接近 0，标准差接近 1
```

### 训练集 + 测试集（正确做法）

```python
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

# 1. 划分数据
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 2. 在训练集上拟合标准化器
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)  # 学习参数 + 转换

# 3. 用训练集的参数转换测试集
X_test_scaled = scaler.transform(X_test)  # 仅转换，不学习

# 4. 训练模型
model.fit(X_train_scaled, y_train)
```

⚠️ **重要原则**：
- **训练集**：`fit_transform()` - 学习均值和标准差，并转换
- **测试集**：`transform()` - 用训练集的均值和标准差转换
- **绝对不能**在测试集上用 `fit_transform()`！

## 为什么需要标准化？

1. **消除量纲影响**：年龄（20-60）和收入（5000-50000）量级差异大
2. **加快模型训练**：梯度下降算法收敛更快
3. **提高模型性能**：逻辑回归、SVM、KNN 等对特征尺度敏感

## 何时使用？

✅ **需要标准化**：
- 逻辑回归、线性回归
- SVM、KNN
- 神经网络
- PCA 降维

❌ **不需要标准化**：
- 决策树、随机森林
- XGBoost、LightGBM

## 易错点

⚠️ **忘记传入数据参数**：
```python
# ❌ 错误（缺少参数）
data[cols] = scaler.fit_transform()
# TypeError: fit_transform() missing 1 required positional argument: 'X'

# ✅ 正确
data[cols] = scaler.fit_transform(data[cols])
```

⚠️ **在测试集上用 fit_transform**：
```python
# ❌ 错误（数据泄露）
X_test_scaled = scaler.fit_transform(X_test)

# ✅ 正确
X_test_scaled = scaler.transform(X_test)
```

⚠️ **划分前标准化**：
```python
# ❌ 错误（数据泄露）
X_scaled = scaler.fit_transform(X)
X_train, X_test = train_test_split(X_scaled)

# ✅ 正确
X_train, X_test = train_test_split(X)
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)
```

## 对比：StandardScaler vs MinMaxScaler

| 方法 | 结果范围 | 公式 | 适用场景 |
|------|----------|------|----------|
| **StandardScaler** | 均值0，标准差1 | $z = \frac{x-\mu}{\sigma}$ | 正态分布数据 |
| **MinMaxScaler** | [0, 1] | $z = \frac{x-\min}{\max-\min}$ | 需要固定范围 |
| **RobustScaler** | 中位数0 | 用中位数和四分位数 | 有异常值 |

## 相关概念

- [[train_test_split]] - 数据集划分
- [[MinMaxScaler]] - 归一化
- [[fit_transform]] - 拟合并转换
