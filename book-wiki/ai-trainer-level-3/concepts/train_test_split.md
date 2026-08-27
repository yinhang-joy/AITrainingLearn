# train_test_split

## 一句话说明

将数据集划分为训练集和测试集，用于训练模型和评估模型泛化能力。

## 语法

```python
from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.2,
    random_state=42,
    stratify=None
)
```

## 返回值

| 返回值 | 含义 | 用途 |
|--------|------|------|
| `X_train` | 训练集特征数据 | 用于 `model.fit(X_train, y_train)` |
| `X_test` | 测试集特征数据 | 用于 `model.predict(X_test)` |
| `y_train` | 训练集目标变量（标签） | 用于 `model.fit(X_train, y_train)` |
| `y_test` | 测试集目标变量（标签） | 用于评估：`accuracy_score(y_test, y_pred)` |

## 参数说明

| 参数 | 说明 | 默认值 | 常用值 |
|------|------|--------|--------|
| `test_size` | 测试集比例或数量 | 0.25 | 0.2, 0.25, 0.3 |
| `random_state` | 随机种子（结果可复现） | None | 42, 0, 1234 |
| `stratify` | 分层抽样（保持类别比例） | None | `y`（类别不平衡时） |
| `shuffle` | 是否打乱数据 | True | True |

## 示例

### 基本用法

```python
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

# 准备数据
X = data[['feature1', 'feature2', 'feature3']]
y = data['target']

# 1. 划分数据（80% 训练，20% 测试）
X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.2,      # 测试集占 20%
    random_state=42     # 固定随机种子
)

# 2. 训练模型
model = LogisticRegression()
model.fit(X_train, y_train)

# 3. 预测
y_pred = model.predict(X_test)

# 4. 评估
accuracy = accuracy_score(y_test, y_pred)
print(f"准确率: {accuracy:.2%}")
```

### 分层抽样（类别不平衡时）

```python
# 假设数据类别不平衡：90% 类别A，10% 类别B
# stratify=y 保证训练集和测试集都保持 9:1 比例
X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.2,
    stratify=y,         # 分层抽样
    random_state=42
)

print(y_train.value_counts(normalize=True))  # 训练集比例
print(y_test.value_counts(normalize=True))   # 测试集比例
```

## 为什么要划分？

**训练集**：让模型学习数据的规律
**测试集**：检验模型对"未见过"数据的泛化能力

如果用同一批数据训练和测试：
- ❌ 模型可能"死记硬背"（过拟合）
- ❌ 测试准确率虚高，实际应用效果差

## 易错点

⚠️ **顺序问题**：先划分，再标准化
```python
# ❌ 错误（数据泄露）
scaler.fit_transform(X)
X_train, X_test = train_test_split(X)

# ✅ 正确
X_train, X_test, y_train, y_test = train_test_split(X, y)
scaler.fit_transform(X_train)
scaler.transform(X_test)
```

⚠️ **忘记设置 random_state**：
```python
# ❌ 每次运行结果不同
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

# ✅ 结果可复现
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
```

⚠️ **test_size 理解错误**：
- `test_size=0.2` → 测试集 20%，训练集 80%
- `test_size=100` → 测试集 100 条数据（整数表示数量）

## 相关概念

- [[StandardScaler]] - 标准化（在划分后进行）
- [[cross_val_score]] - 交叉验证（更稳健的评估方法）
- [[stratify]] - 分层抽样详解
