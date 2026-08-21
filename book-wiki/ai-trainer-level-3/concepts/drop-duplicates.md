# drop-duplicates（重复值处理）

- **来源章节**: 2.1.2
- **定义**: 删除 DataFrame 中所有列完全相同的重复行，只保留首次出现的记录
- **用法**:
  ```python
  before = len(data)
  data = data.drop_duplicates()
  print(f'删除重复行: {before - len(data)}')
  ```
- **参数**:
  - 默认：所有列相同才算重复
  - `subset=['列1', '列2']`：仅根据指定列判断重复
  - `keep='first'`（默认）：保留第一次出现；`'last'` 保留最后一次；`False` 全部删除
- **⚠️ 易错点**: 同样返回新 DataFrame，必须重新赋值 `data = data.drop_duplicates()`
- **业务意义**: 数据采集过程中可能产生重复提交、重复记录，影响统计准确性
- **关联**: [[dropna-missing-values]] · [[data-cleaning-workflow]]
