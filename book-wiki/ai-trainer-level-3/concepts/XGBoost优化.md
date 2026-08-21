# XGBoost 优化

**适用场景**：提升模型性能，处理复杂非线性关系，机器学习竞赛常胜算法

---

## 核心概念

**XGBoost**（eXtreme Gradient Boosting）：基于梯度提升的集成学习算法，通过训练多棵决策树并组合预测结果，实现高精度预测。

---

## 为什么 XGBoost 通常更好？

### 线性回归 vs XGBoost

| 特性 | 线性回归 | XGBoost |
|------|----------|---------|
| 关系假设 | 只能拟合线性关系 | 可拟合复杂非线性关系 |
| 特征交互 | 需手动构造 | 自动捕捉 |
| 异常值 | 敏感 | 鲁棒 |
| 训练速度 | 快 | 较慢 |
| 可解释性 | 高（看权重） | 中等（看特征重要性） |
| 过拟合风险 | 低 | 高（需调参） |

### 直观对比
```python
# 数据关系：y = x² + noise（非线性）

# 线性回归：强行拟合直线
LinearRegression → R² = 0.3（差）

# XGBoost：多棵树拟合曲线
XGBRegressor → R² = 0.85（好）
```

---

## sklearn 风格实现

### 基本用法
```python
from xgboost import XGBRegressor

# 初始化模型
xgb_model = XGBRegressor()

# 训练
xgb_model.fit(X_train, y_train)

# 预测
y_pred = xgb_model.predict(X_test)
```

### 2.2.4 考试版本（带超参数）
```python
xgb_model = XGBRegressor(
    n_estimators=1000,      # 树的数量
    learning_rate=0.05,     # 学习率
    max_depth=5,            # 树的最大深度
    subsample=0.8,          # 样本采样比例
    colsample_bytree=0.8    # 特征采样比例
)
xgb_model.fit(X_train, y_train)
```

---

## 关键超参数详解

### 1. `n_estimators`（树的数量）
```python
xgb_model = XGBRegressor(n_estimators=1000)
```
- **含义**：训练多少棵决策树
- **取值**：通常 100~2000
- **效果**：
  - 太少：欠拟合（R² 低）
  - 太多：过拟合 + 训练慢
- **经验值**：1000（考试默认）

---

### 2. `learning_rate`（学习率）
```python
xgb_model = XGBRegressor(learning_rate=0.05)
```
- **含义**：每棵树的贡献权重
- **取值**：通常 0.01~0.3
- **效果**：
  - 太大：训练快但不稳定，容易过拟合
  - 太小：训练慢但更稳定，泛化性好
- **搭配**：`learning_rate` 越小，`n_estimators` 要越大
  - `learning_rate=0.1, n_estimators=100`
  - `learning_rate=0.05, n_estimators=1000`（考试版本）

---

### 3. `max_depth`（树的最大深度）
```python
xgb_model = XGBRegressor(max_depth=5)
```
- **含义**：每棵树的层数
- **取值**：通常 3~10
- **效果**：
  - 太浅（如 2）：欠拟合
  - 太深（如 15）：过拟合
- **经验值**：5~7

---

### 4. `subsample`（样本采样比例）
```python
xgb_model = XGBRegressor(subsample=0.8)
```
- **含义**：每棵树随机选择 80% 的训练样本
- **取值**：通常 0.5~1.0
- **效果**：防止过拟合（类似随机森林的 Bagging）
- **经验值**：0.8

---

### 5. `colsample_bytree`（特征采样比例）
```python
xgb_model = XGBRegressor(colsample_bytree=0.8)
```
- **含义**：每棵树随机选择 80% 的特征
- **取值**：通常 0.3~1.0
- **效果**：防止过拟合，减少特征间的高相关性影响
- **经验值**：0.8

---

## 完整训练与评估流程（2.2.4 原题）

```python
from xgboost import XGBRegressor
from sklearn.metrics import mean_squared_error, r2_score
import pandas as pd

# 初始化 XGBoost 模型
xgb_model = XGBRegressor(
    n_estimators=1000,
    learning_rate=0.05,
    max_depth=5,
    subsample=0.8,
    colsample_bytree=0.8,
    random_state=42  # 考试必加
)

# 训练模型
xgb_model.fit(X_train, y_train)

# 预测
y_pred_xg = xgb_model.predict(X_test)

# 评估
mse_xg = mean_squared_error(y_test, y_pred_xg)
r2_xg = r2_score(y_test, y_pred_xg)

# 保存结果
results_xg = pd.DataFrame({'实际值': y_test, '预测值': y_pred_xg})
results_xg.to_csv('2.2.4_results_xg.txt', index=False, sep='\t')

# 保存报告
with open('2.2.4_report_xgb.txt', 'w') as f:
    f.write(f'均方误差: {mse_xg}\n')
    f.write(f'决定系数: {r2_xg}\n')
```

---

## 性能对比分析

### 预期结果
```python
# 线性回归
MSE: 0.1523, R²: 0.4217

# XGBoost
MSE: 0.1012, R²: 0.6543

# 提升：MSE 降低 33%，R² 提升 55%
```

### 为什么会提升？
1. **捕捉非线性关系**：低碳行为与特征的关系可能是非线性的
2. **特征交互**：如"生源地 × 月生活费"的组合影响
3. **异常值鲁棒**：决策树基于分裂规则，对极端值不敏感

---

## 高级技巧

### 1. 特征重要性分析
```python
import matplotlib.pyplot as plt

# 获取特征重要性
importance = xgb_model.feature_importances_
feature_names = X_train.columns

# 排序并可视化
sorted_idx = importance.argsort()
plt.barh(feature_names[sorted_idx], importance[sorted_idx])
plt.xlabel('特征重要性')
plt.show()
```

### 2. 早停（Early Stopping）
```python
xgb_model = XGBRegressor(
    n_estimators=10000,
    early_stopping_rounds=50,  # 50 轮无改善则停止
    eval_metric='rmse'
)
xgb_model.fit(
    X_train, y_train,
    eval_set=[(X_test, y_test)],
    verbose=False
)
```
- 自动找到最佳树数量，避免过拟合

### 3. 超参数调优
```python
from sklearn.model_selection import GridSearchCV

param_grid = {
    'max_depth': [3, 5, 7],
    'learning_rate': [0.01, 0.05, 0.1],
    'n_estimators': [500, 1000, 2000]
}

grid_search = GridSearchCV(
    XGBRegressor(),
    param_grid,
    cv=5,
    scoring='r2'
)
grid_search.fit(X_train, y_train)

print(f"最佳参数: {grid_search.best_params_}")
print(f"最佳 R²: {grid_search.best_score_}")
```

---

## 常见错误

### 错误 1：超参数拼写错误
```python
# 错误
xgb_model = XGBRegressor(n_estimator=1000)  # 少了s

# 正确
xgb_model = XGBRegressor(n_estimators=1000)
```

### 错误 2：忘记设置 random_state
```python
# 错误：每次运行结果不同
xgb_model = XGBRegressor(n_estimators=1000)

# 正确：考试必加
xgb_model = XGBRegressor(n_estimators=1000, random_state=42)
```

### 错误 3：过度拟合
```python
# 危险配置：极易过拟合
xgb_model = XGBRegressor(
    n_estimators=5000,
    learning_rate=0.3,
    max_depth=15,
    subsample=1.0,        # 不采样
    colsample_bytree=1.0  # 不采样
)
# 训练集 R² = 0.99，测试集 R² = 0.3（严重过拟合）
```

---

## XGBoost vs 其他集成算法

| 算法 | 速度 | 精度 | 过拟合风险 | 适用场景 |
|------|------|------|------------|----------|
| Random Forest | 快 | 中 | 低 | 中等规模数据 |
| XGBoost | 中 | 高 | 中 | 结构化数据竞赛 |
| LightGBM | 很快 | 高 | 中 | 大规模数据 |
| CatBoost | 慢 | 高 | 低 | 分类特征多的数据 |

---

## 考试注意事项

1. **参数顺序无所谓**，但建议按题目给的顺序填写
2. **必须设置的参数**（2.2.4 原题）：
   ```python
   n_estimators=1000
   learning_rate=0.05
   max_depth=5
   subsample=0.8
   colsample_bytree=0.8
   ```
3. **文件命名**：`2.2.4_results_xg.txt`（注意 `_xg` 后缀）
4. **评估指标**：MSE 和 R²（与线性回归对比）

---

## 相关概念

- [[concepts/线性回归模型]]
- [[concepts/集成学习]]
- [[concepts/决策树]]
- [[concepts/随机森林]]
- [[concepts/梯度提升]]
