# data-read-and-view（数据读取与查看）

- **来源章节**: 1.1.4
- **定义**: 读取 CSV 文件到 DataFrame 并使用三件套查看数据概况
- **用法**:
  ```python
  data = pd.read_csv('file.csv')
  data.head()       # 查看前 5 行
  data.info()       # 列类型、缺失值
  data.describe()   # 数值列统计
  ```
- **三件套区别**:
  - `.head()`：看数据长什么样（前 5 行）
  - `.info()`：看数据类型和缺失值
  - `.describe()`：看数值分布（均值、最大最小值、四分位数）
- **易错点**: `.describe()` 只统计数值列（int/float），字符串列不会显示
- **关联**: [[dropna-missing-values]] · [[astype-conversion]]
