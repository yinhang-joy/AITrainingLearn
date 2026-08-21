# Pipeline与特征标准化

**标签**: `sklearn` `Pipeline` `StandardScaler` `数据标准化`

---

## 定义

**Pipeline（管道）**：sklearn 的工具，将多个处理步骤（如标准化、特征选择、模型训练）串联成一个流程，一次调用完成所有操作。

**StandardScaler（标准化）**：将特征转换为均值=0、标准差=1 的分布，消除量纲差异。

---

## 核心方法

### 1. Pipeline 构建
```python
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression

pipeline = Pipeline([
    ('scaler', StandardScaler()),       # 步骤1：标准化（名称, 对象）
    ('regressor', LinearRegression())   # 步骤2：线性回归
])
```

**参数格式**：列表，每个元素是 `(步骤名, 处理器/模型对象)` 元组。

### 2. 训练与预测
```python
# 训练（自动执行：标准化训练集 → 训练模型）
pipeline.fit(X_train, y_train)

# 预测（自动执行：用训练集参数标准化测试集 → 预测）
y_pred = pipeline.predict(X_test)

# 评估
score = pipeline.score(X_test, y_test)
```

---

## StandardScaler 原理

### 数学公式
```
z = (x - mean) / std
```

- `mean`：训练集该特征的均值
- `std`：训练集该特征的标准差
- 结果：转换后均值=0、标准差=1

### 为什么需要标准化

**问题**：不同特征量纲不同，导致模型偏向数值大的特征。

| 特征 | 原始值范围 | 影响权重 |
|---|---|---|
| 重量（kg） | 800～2000 | 主导模型 |
| 排量（L） | 1.0～8.0 | 被忽略 |

**标准化后**：所有特征在同一尺度（-3～3 之间），模型公平对待。

### 示例
```python
from sklearn.preprocessing import StandardScaler

scaler = StandardScaler()

# 训练集：计算均值和标准差
scaler.fit(X_train)
X_train_scaled = scaler.transform(X_train)

# 测试集：用训练集的均值/标准差转换（防止数据泄露）
X_test_scaled = scaler.transform(X_test)

print(f"训练集均值: {scaler.mean_}")
print(f"训练集标准差: {scaler.scale_}")
```

---

## Pipeline 的三大优势

### 1. 防止数据泄露
```python
# ❌ 错误：用全部数据的统计量
scaler.fit(X)  # X 包含训练集+测试集
X_scaled = scaler.transform(X)
X_train, X_test = X_scaled[:800], X_scaled[800:]

# ✅ 正确：Pipeline 自动只用训练集
pipeline.fit(X_train, y_train)      # 只用 X_train 计算均值/标准差
pipeline.predict(X_test)            # 用训练集参数转换 X_test
```

### 2. 代码简洁
```python
# 不用 Pipeline（5 行）
scaler = StandardScaler()
scaler.fit(X_train)
X_train_scaled = scaler.transform(X_train)
model = LinearRegression()
model.fit(X_train_scaled, y_train)

# 用 Pipeline（3 行）
pipeline = Pipeline([('scaler', StandardScaler()), ('model', LinearRegression())])
pipeline.fit(X_train, y_train)
pipeline.predict(X_test)
```

### 3. 便于部署
```python
import pickle

# 保存 pipeline（包含 scaler 参数 + 模型参数）
with open('model.pkl', 'wb') as f:
    pickle.dump(pipeline, f)

# 加载后直接用于新数据（自动标准化）
with open('model.pkl', 'rb') as f:
    pipeline = pickle.load(f)

predictions = pipeline.predict(new_data)  # 自动用训练时的 scaler 参数
```

---

## 实际应用示例

```python
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split

# 数据分割
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

# 构建 pipeline
pipeline = Pipeline([
    ('scaler', StandardScaler()),
    ('regressor', RandomForestRegressor(n_estimators=100, random_state=42))
])

# 训练
pipeline.fit(X_train, y_train)

# 评估
print(f"测试集 R²: {pipeline.score(X_test, y_test):.4f}")
```

---

## 常见问题

### Q1: 所有模型都需要标准化吗？
**A**: 
- **需要**：线性模型（线性回归、逻辑回归、SVM、神经网络）
- **不需要**：树模型（决策树、随机森林、XGBoost）— 树模型对特征尺度不敏感
- **建议**：统一加 StandardScaler，对树模型无害，且方便切换模型

### Q2: Pipeline 里的步骤顺序重要吗？
**A**: 非常重要！必须按实际执行顺序排列：
1. 数据预处理（标准化、填充缺失值）
2. 特征选择（PCA、特征筛选）
3. 模型训练（最后一步必须是模型）

### Q3: 如何访问 Pipeline 中的某个步骤？
```python
# 访问 scaler
scaler = pipeline.named_steps['scaler']
print(scaler.mean_)

# 访问模型
model = pipeline.named_steps['regressor']
print(model.feature_importances_)  # 随机森林的特征重要性
```

---

## 其他标准化方法

| 方法 | 公式 | 适用场景 |
|---|---|---|
| **StandardScaler** | `(x - mean) / std` | 通用，假设数据近似正态分布 |
| **MinMaxScaler** | `(x - min) / (max - min)` | 需要固定范围（如 [0, 1]），神经网络常用 |
| **RobustScaler** | `(x - median) / IQR` | 有异常值时，对异常值不敏感 |

```python
from sklearn.preprocessing import MinMaxScaler, RobustScaler

# MinMaxScaler: 缩放到 [0, 1]
pipeline = Pipeline([
    ('scaler', MinMaxScaler()),
    ('model', LinearRegression())
])

# RobustScaler: 用中位数和四分位距（对异常值稳健）
pipeline = Pipeline([
    ('scaler', RobustScaler()),
    ('model', LinearRegression())
])
```

---

## 与其他概念的关系

- **前置步骤**: [[特征工程与数据分割]]
- **后续步骤**: [[线性回归建模]] · [[随机森林模型改进]]
- **配合使用**: [[模型持久化与结果保存]]

---

## 考试要点

1. Pipeline 的参数格式：`[('名称', 对象), ...]`（列表+元组）
2. StandardScaler 用法：`scaler.fit(X_train)` → `scaler.transform(X_test)`
3. Pipeline 自动防止数据泄露（只用训练集的统计量）
4. `pipeline.fit()` / `pipeline.predict()` / `pipeline.score()` 用法

**典型填空**：
```python
pipeline = Pipeline([
    ('scaler', ___________()),          # 答案：StandardScaler
    ('regressor', LinearRegression())
])
```
