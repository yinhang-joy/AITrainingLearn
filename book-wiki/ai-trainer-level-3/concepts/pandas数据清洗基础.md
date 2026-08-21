# pandas数据清洗基础

- **来源章节**: 2.1.5
- **定义**: 数据预处理的第一步，包括加载数据、结构检查、缺失值检测与删除、重复值处理
- **核心方法**:
  ```python
  df = pd.read_csv('data.csv')  # 加载数据
  df.info()                      # 查看结构（列名/类型/缺失值）
  df.isnull().sum()              # 统计每列缺失数量
  df = df.dropna()               # 删除含缺失值的行
  df = df.drop_duplicates()      # 删除重复行
  df.duplicated().sum()          # 统计重复行数量
  ```
- **使用场景**: 机器学习建模前的数据清洗，确保数据质量
- **⚠️ 易错点**: 
  - `dropna()` 和 `drop_duplicates()` 默认返回新 DataFrame，必须赋值 `df = df.dropna()` 才生效
  - `dropna()` 默认删除任何列有缺失的行；用 `dropna(subset=['列名'])` 指定列
- **关联**: [[数据类型转换与异常处理]] · [[数据导出]]
