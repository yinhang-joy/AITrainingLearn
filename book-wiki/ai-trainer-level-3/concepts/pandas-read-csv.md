# pandas-read-csv

- **来源章节**: 1.1.1
- **定义**: 用 pandas 把 CSV 文件读成 DataFrame（表格对象），所有分析的第一步
- **用法**:
  ```python
  df = pd.read_csv('patient_data.csv')
  df.head()   # 前 5 行
  df.info()   # 列名/类型/缺失值
  ```
- **易错点**: 读入后先看数据再动手；文件路径考试已给
- **关联**: [[boolean-indexing]] · [[groupby-aggregation]]
