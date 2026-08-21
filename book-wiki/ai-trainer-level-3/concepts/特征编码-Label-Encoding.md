# 特征编码（Label Encoding）

- **来源章节**: 2.1.5
- **定义**: 将分类变量（字符串）转换为数值编码，便于机器学习模型使用
- **核心方法**:
  ```python
  from sklearn.preprocessing import LabelEncoder
  
  le = LabelEncoder()
  df['Fitness_Level'] = le.fit_transform(df['Fitness_Level'])
  # 输入: ['Good', 'Average', 'Good'] → 输出: [1, 0, 1]
  
  # 查看编码映射
  dict(zip(le.classes_, le.transform(le.classes_)))
  # {'Average': 0, 'Good': 1}
  ```
- **编码规则**: 按**字母序**排序后编号（Average < Good，所以 Average→0, Good→1）
- **使用场景**: 
  - ✅ 有序分类变量（如 Good > Average > Poor）
  - ✅ 目标变量（y）编码
  - ❌ 无序分类（如地区名）应用独热编码 `pd.get_dummies()`
- **⚠️ 易错点**: 
  - 编码顺序由字母序决定，不是出现顺序
  - 不同类别数量不影响编码值（只看字母序）
  - 新数据中出现未见过的类别会报错
- **关联**: [[数据类型转换与异常处理]] · [[数据集划分]]
