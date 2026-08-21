# standard-scaler（标准化/Z-score 归一化）

- **来源章节**: 2.1.2
- **定义**: 将数值特征转换为均值=0、标准差=1 的标准正态分布，消除不同量纲的影响
- **公式**: `x_标准化 = (x - 均值) / 标准差`
- **用法**:
  ```python
  from sklearn.preprocessing import StandardScaler
  
  scaler = StandardScaler()
  data[['月生活费']] = scaler.fit_transform(data[['月生活费']])
  ```
- **为什么需要标准化？**
  - 不同特征量纲差异大（如月生活费 1000~3000、问卷分值 1~5），导致模型偏向大数值特征
  - 标准化后所有特征权重相当，模型收敛更快更稳定
- **⚠️ 易错点**: 
  - `fit_transform` 返回 NumPy 数组，需重新赋值回 DataFrame
  - 训练集和测试集应用同一个 scaler（先在训练集 fit，再对测试集 transform）
- **对比**: `MinMaxScaler` 归一化到 [0, 1] 区间；`StandardScaler` 保留异常值信息
- **关联**: [[feature-engineering]] · [[train-test-split]] · [[data-cleaning-workflow]]
