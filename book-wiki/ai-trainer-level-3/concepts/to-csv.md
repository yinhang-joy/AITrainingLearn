# to-csv（保存 CSV）

- **来源章节**: 1.1.2
- **定义**: 把 DataFrame 保存为 CSV 文件
- **用法**:
  ```python
  df.to_csv('cleaned_sensor_data.csv', index=False)
  ```
- **参数**: 
  - 第一个参数：文件名（字符串），相对路径保存在工作目录
  - `index=False`：**考试必加**，不保存行号列（否则 CSV 第一列是 0,1,2...）
- **⚠️ 易错点**: 
  - 忘记 `index=False` 会多一列行号，导致后续读取时列数不匹配
  - 文件名要加引号（字符串）
- **关联**: [[pandas-read-csv]] · [[fillna-method]]
