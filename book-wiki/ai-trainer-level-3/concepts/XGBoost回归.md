# XGBoost回归

- **来源章节**: 2.2.3
- **定义**: 梯度提升树算法，串行构建决策树，后面的树专门修正前面的错误，通常比随机森林更准确
- **用法**:
  ```python
  import xgboost as xgb
  
  # 初始化 XGBoost 回归模型
  xgb_model = xgb.XGBRegressor(n_estimators=100, random_state=42)
  
  # 训练模型
  xgb_model.fit(X_train, y_train)
  
  # 预测
  y_pred_xgb = xgb_model.predict(X_test)
  
  # 评估
  xgb_train_score = xgb_model.score(X_train, y_train)
  xgb_test_score = xgb_model.score(X_test, y_test)
  ```
- **核心参数**:
  - `n_estimators=100`: 决策树数量
  - `random_state=42`: 随机种子
  - `learning_rate`: 学习率（默认 0.3），控制每棵树的贡献度
  - `max_depth`: 树的最大深度（默认 6）
- **工作原理**:
  1. 构建第一棵树，预测结果
  2. 计算**残差**（真实值 - 预测值）
  3. 构建第二棵树，专门预测第一棵树的残差
  4. 重复步骤 2-3，每棵树修正前面的错误
  5. 最终预测 = 所有树的预测值累加
- **与随机森林对比**:
  | 维度 | 随机森林 | XGBoost |
  |---|---|---|
  | 构建方式 | 并行（独立树） | 串行（后树修正前树） |
  | 速度 | 快 | 慢 |
  | 准确性 | 高 | 通常更高 |
  | 过拟合风险 | 低 | 中等（需调参） |
  | 使用场景 | 快速原型、稳定性优先 | 竞赛、高精度需求 |
- **什么时候用 XGBoost**:
  - 随机森林结果不够好时
  - 需要更高精度时（如 Kaggle 竞赛）
  - 有充足训练时间时
  - 需要分析特征重要性时
- **考试中的作用**: 作为对比模型分析随机森林的错误案例并改进预测结果
- **易错点**: 
  - XGBoost 需要单独安装 `pip install xgboost`
  - 参数调优复杂，默认参数通常够用
- **关联**: [[随机森林回归]] · [[模型评估指标]] · [[模型持久化]]
