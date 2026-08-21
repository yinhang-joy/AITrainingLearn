# pandas-read-excel

- **来源章节**: 2.1.2
- **定义**: 用 pandas 读取 Excel 文件（`.xlsx` / `.xls`）为 DataFrame，处理表格数据的第一步
- **用法**:
  ```python
  data = pd.read_excel('大学生低碳生活行为的影响因素数据集.xlsx')
  data.head()    # 前 5 行
  data.shape     # (行数, 列数)
  data.info()    # 列名/类型/缺失值
  ```
- **依赖**: 需要安装 `openpyxl`（读 `.xlsx`）或 `xlrd`（读旧版 `.xls`）
- **易错点**: 读取后先用 `head()` / `info()` 查看数据结构再动手清洗；Excel 列名可能包含空格需完全匹配
- **关联**: [[pandas-read-csv]] · [[dropna-missing-values]] · [[data-cleaning-workflow]]
