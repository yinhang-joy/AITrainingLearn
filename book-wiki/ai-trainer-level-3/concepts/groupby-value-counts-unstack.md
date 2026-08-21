# GroupBy + value_counts + unstack 组合

**所属章节**: 2.1.4 医疗研究数据清洗和标注设计  
**难度**: ⭐⭐⭐⭐☆  
**重要性**: ⭐⭐⭐⭐☆

---

## 概念说明

这是一个经典的数据分组统计模式，用于生成**双维度交叉频次表**（透视表）。常用于分析两个分类变量之间的关系，如「不同疾病类型的治疗结果分布」。

---

## 核心操作

### 组合拳三步走

```python
# 完整写法
result = data.groupby('疾病类型')['治疗结果'].value_counts().unstack()

# 拆解说明：
# ① data.groupby('疾病类型')          # 按疾病类型分组
# ② ['治疗结果']                       # 选择要统计的列
# ③ .value_counts()                   # 每组内统计治疗结果的频次
# ④ .unstack()                        # 把多级索引展开为透视表
```

**返回结果**（DataFrame 透视表）：

| 疾病类型 | 治愈 | 好转 | 未愈 | 死亡 |
|---|---|---|---|---|
| 感冒 | 120 | 45 | 3 | 0 |
| 糖尿病 | 35 | 68 | 52 | 8 |
| 高血压 | 48 | 92 | 35 | 5 |
| 骨折 | 85 | 42 | 12 | 2 |

---

## 逐步拆解

### 步骤 1：`groupby('疾病类型')`

```python
grouped = data.groupby('疾病类型')
print(type(grouped))  # <class 'pandas.core.groupby.generic.DataFrameGroupBy'>

# 分组对象本身不可直接查看，需要配合聚合操作
```

### 步骤 2：`['治疗结果']`

```python
grouped_series = data.groupby('疾病类型')['治疗结果']
print(type(grouped_series))  # <class 'pandas.core.groupby.generic.SeriesGroupBy'>

# 选择要统计的列，变成 SeriesGroupBy 对象
```

### 步骤 3：`.value_counts()`

```python
counts = data.groupby('疾病类型')['治疗结果'].value_counts()
print(counts)

# 输出（多级索引 Series）：
# 疾病类型  治疗结果
# 感冒     治愈     120
#         好转      45
#         未愈       3
# 糖尿病    好转      68
#         治愈      35
#         未愈      52
#         死亡       8
# ...
```

**问题**：多级索引不直观，无法直接绘图。

### 步骤 4：`.unstack()`

```python
pivot_table = data.groupby('疾病类型')['治疗结果'].value_counts().unstack()
print(pivot_table)

# 输出（DataFrame 透视表）：
# 治疗结果   治愈   好转   未愈   死亡
# 疾病类型                    
# 感冒     120.0  45.0   3.0   NaN
# 糖尿病    35.0  68.0  52.0   8.0
# 高血压    48.0  92.0  35.0   5.0
# 骨折     85.0  42.0  12.0   2.0
```

**`unstack()` 作用**：
- 把多级索引的最内层（治疗结果）变成列名
- 把计数值填入对应单元格
- 缺失的组合填 NaN（如感冒没有死亡病例）

---

## 完整示例

### 场景：分析疾病类型与治疗结果关系

```python
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

# 加载数据
data = pd.read_csv('medical_data.csv', encoding='gbk')

# 统计疾病类型 × 治疗结果的分布
treatment_distribution = data.groupby('疾病类型')['治疗结果'].value_counts().unstack()

# 查看统计结果
print(treatment_distribution)
#         治愈   好转   未愈   死亡
# 疾病类型                    
# 感冒     120   45    3   NaN
# 糖尿病    35   68   52     8
# 高血压    48   92   35     5
# 骨折     85   42   12     2

# 填充 NaN 为 0（可选）
treatment_distribution = treatment_distribution.fillna(0)

# 绘制堆叠柱状图
font_path = 'C:/Windows/Fonts/simhei.ttf'
my_font = fm.FontProperties(fname=font_path)

treatment_distribution.plot.bar(stacked=True, figsize=(10, 6))
plt.title('不同疾病类型的治疗结果分布', fontproperties=my_font, fontsize=16)
plt.xlabel('疾病类型', fontproperties=my_font, fontsize=12)
plt.ylabel('患者数量', fontproperties=my_font, fontsize=12)
plt.xticks(rotation=45, fontproperties=my_font)
plt.legend(prop=my_font)
plt.tight_layout()
plt.show()
```

---

## 变体操作

### 1. 不使用 `unstack()`（保持多级索引）

```python
# 适合查看具体数字，不适合绘图
counts = data.groupby('疾病类型')['治疗结果'].value_counts()
print(counts)
```

### 2. 归一化（显示比例而非计数）

```python
# 每组内的比例（行和为 1）
proportions = data.groupby('疾病类型')['治疗结果'].value_counts(normalize=True).unstack()
print(proportions)
#         治愈      好转      未愈      死亡
# 疾病类型                          
# 感冒     0.714   0.268   0.018   NaN
# 糖尿病    0.214   0.417   0.319   0.049
```

### 3. 使用 `crosstab()`（等效方法）

```python
# crosstab 是专门用于交叉表的函数
pivot = pd.crosstab(data['疾病类型'], data['治疗结果'])
print(pivot)
# 结果与 groupby + value_counts + unstack 相同
```

---

## 常见错误与解决方案

### 错误 1：忘记 `unstack()`

```python
# 错误示例
result = data.groupby('疾病类型')['治疗结果'].value_counts()
result.plot.bar()
# ValueError: No numeric data to plot

# 原因：多级索引 Series 不能直接绘图

# 正确做法：加 unstack()
result = data.groupby('疾病类型')['治疗结果'].value_counts().unstack()
result.plot.bar()
```

### 错误 2：NaN 影响绘图

```python
# 问题：某些疾病没有特定治疗结果，unstack 后为 NaN
treatment_distribution = data.groupby('疾病类型')['治疗结果'].value_counts().unstack()
# 感冒没有死亡病例 → NaN

# 解决方案：填充 NaN 为 0
treatment_distribution = treatment_distribution.fillna(0)
```

### 错误 3：列名顺序混乱

```python
# 问题：unstack 后列的顺序可能不是你想要的（按字母排序）

# 解决方案：指定列顺序
treatment_distribution = treatment_distribution[['治愈', '好转', '未愈', '死亡']]
```

---

## 考试要点

1. **完整写法不能少任何一步**：`groupby(...)[...].value_counts().unstack()`
2. **`unstack()` 是关键**：多级索引 → 透视表
3. **绘图前填充 NaN**：`fillna(0)` 避免绘图异常
4. **堆叠柱状图参数**：`.plot.bar(stacked=True)`

---

## 实战代码

```python
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

# 加载数据
data = pd.read_csv('medical_data.csv', encoding='gbk')

# 统计疾病类型与治疗结果的交叉分布
treatment_outcome_distribution = data.groupby('疾病类型')['治疗结果'].value_counts().unstack()

# 填充缺失值
treatment_outcome_distribution = treatment_outcome_distribution.fillna(0)

# 设置中文字体
font_path = 'C:/Windows/Fonts/simhei.ttf'
my_font = fm.FontProperties(fname=font_path)

# 绘制堆叠柱状图
treatment_outcome_distribution.plot.bar(stacked=True)
plt.title('不同疾病类型的治疗结果分布', fontproperties=my_font)
plt.xlabel('疾病类型', fontproperties=my_font)
plt.ylabel('治疗结果数量', fontproperties=my_font)
plt.xticks(fontproperties=my_font)
plt.legend(prop=my_font)
plt.show()
```

---

## 关联知识

- [[groupby-aggregation]]：GroupBy 聚合详解
- [[pandas-crosstab]]：交叉表专用方法
- [[matplotlib-chinese-font]]：matplotlib 中文显示
