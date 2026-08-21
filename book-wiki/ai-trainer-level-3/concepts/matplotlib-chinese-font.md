# Matplotlib 中文字体配置

**所属章节**: 2.1.4 医疗研究数据清洗和标注设计  
**难度**: ⭐⭐☆☆☆  
**重要性**: ⭐⭐⭐☆☆

---

## 概念说明

matplotlib 默认不支持中文显示，中文会显示为方块（□□□）。需要通过 `FontProperties` 加载中文字体文件，并对每个中文元素（标题、标签、图例）单独指定字体。

---

## 问题演示

### 不配置中文字体的结果

```python
import matplotlib.pyplot as plt

plt.bar(['感冒', '糖尿病', '高血压'], [120, 85, 95])
plt.title('疾病统计')
plt.xlabel('疾病类型')
plt.ylabel('患者数')
plt.show()

# 输出：标题和标签全是方块 □□□□
```

**原因**：matplotlib 默认使用不包含中文字符的字体（如 DejaVu Sans）。

---

## 解决方案

### 方法 1：使用 FontProperties（推荐，考试常用）

```python
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

# 1. 加载中文字体文件
font_path = 'C:/Windows/Fonts/simhei.ttf'  # Windows 黑体
my_font = fm.FontProperties(fname=font_path)

# 2. 绘图时对每个中文元素指定字体
plt.bar(['感冒', '糖尿病', '高血压'], [120, 85, 95])
plt.title('疾病统计', fontproperties=my_font)       # 标题
plt.xlabel('疾病类型', fontproperties=my_font)       # X 轴标签
plt.ylabel('患者数', fontproperties=my_font)         # Y 轴标签
plt.xticks(fontproperties=my_font)                  # X 轴刻度标签
plt.yticks(fontproperties=my_font)                  # Y 轴刻度标签
plt.legend(prop=my_font)                            # 图例
plt.show()
```

**关键点**：
- `fontproperties=my_font`：用于标题、标签
- `prop=my_font`：用于图例（参数名不同）
- **每个中文元素都要单独指定**

### 方法 2：全局配置（适合多张图）

```python
import matplotlib.pyplot as plt

# 全局设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei']      # 黑体
plt.rcParams['axes.unicode_minus'] = False        # 解决负号显示问题

# 后续绘图自动使用中文字体
plt.bar(['感冒', '糖尿病', '高血压'], [120, 85, 95])
plt.title('疾病统计')
plt.xlabel('疾病类型')
plt.show()
```

**优点**：一次配置，后续图表都生效  
**缺点**：考试环境可能不支持全局配置，方法 1 更稳妥

---

## 常用中文字体

### Windows 系统

| 字体名称 | 文件路径 | 字体风格 |
|---|---|---|
| **黑体** | `C:/Windows/Fonts/simhei.ttf` | 粗体，适合标题 |
| 宋体 | `C:/Windows/Fonts/simsun.ttc` | 衬线字体 |
| 微软雅黑 | `C:/Windows/Fonts/msyh.ttc` | 现代感 |
| 楷体 | `C:/Windows/Fonts/simkai.ttf` | 手写风格 |

**考试推荐**：`simhei.ttf`（黑体），兼容性最好。

### Linux 系统

```python
# 常见中文字体路径
font_path = '/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc'  # 文泉驿正黑
```

### macOS 系统

```python
font_path = '/System/Library/Fonts/PingFang.ttc'  # 苹方
```

---

## 完整示例

### 场景：医疗数据可视化

```python
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

# 加载数据
data = pd.read_csv('medical_data.csv', encoding='gbk')

# 统计疾病类型分布
disease_counts = data['疾病类型'].value_counts()

# 设置中文字体
font_path = 'C:/Windows/Fonts/simhei.ttf'
my_font = fm.FontProperties(fname=font_path)

# 绘制柱状图
plt.figure(figsize=(10, 6))
plt.bar(disease_counts.index, disease_counts.values)
plt.title('不同疾病类型的患者分布', fontproperties=my_font, fontsize=16)
plt.xlabel('疾病类型', fontproperties=my_font, fontsize=12)
plt.ylabel('患者数量', fontproperties=my_font, fontsize=12)
plt.xticks(rotation=45, fontproperties=my_font)  # X 轴标签旋转 45 度
plt.yticks(fontproperties=my_font)
plt.tight_layout()  # 自动调整布局，避免标签被截断
plt.show()

# 绘制散点图
plt.figure(figsize=(8, 6))
plt.scatter(data['年龄'], data['疾病严重程度'])
plt.title('年龄和疾病严重程度的关系', fontproperties=my_font)
plt.xlabel('年龄', fontproperties=my_font)
plt.ylabel('疾病严重程度', fontproperties=my_font)
plt.xticks(fontproperties=my_font)
plt.yticks(fontproperties=my_font)
plt.show()
```

---

## 常见错误与解决方案

### 错误 1：字体路径错误

```python
# 错误示例
font_path = 'simhei.ttf'  # 只写文件名，找不到文件
my_font = fm.FontProperties(fname=font_path)
# OSError: cannot open resource

# 解决方案：使用完整路径
font_path = 'C:/Windows/Fonts/simhei.ttf'
```

### 错误 2：图例忘记用 `prop`

```python
# 错误示例
plt.legend(fontproperties=my_font)  # 图例不生效

# 正确做法：图例用 prop 参数
plt.legend(prop=my_font)
```

### 错误 3：忘记配置 X/Y 轴刻度标签

```python
# 问题：标题和标签正常，但轴上的刻度标签（如"感冒"）还是方块

# 解决方案：加上 xticks 和 yticks
plt.xticks(fontproperties=my_font)
plt.yticks(fontproperties=my_font)
```

### 错误 4：负号显示为方块

```python
# 问题：使用中文字体后，负号（-）显示为方块

# 解决方案：全局配置解决负号问题
plt.rcParams['axes.unicode_minus'] = False
```

---

## 考试模板（复制即用）

```python
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

# 设置中文字体（考试固定模板）
font_path = 'C:/Windows/Fonts/simhei.ttf'
my_font = fm.FontProperties(fname=font_path)

# 绘图（根据题目调整）
plt.bar(x_data, y_data)
plt.title('标题', fontproperties=my_font)
plt.xlabel('X轴', fontproperties=my_font)
plt.ylabel('Y轴', fontproperties=my_font)
plt.xticks(fontproperties=my_font)
plt.yticks(fontproperties=my_font)
plt.legend(prop=my_font)  # 如果有图例
plt.show()
```

---

## 考试要点

1. **字体路径必须完整**：`C:/Windows/Fonts/simhei.ttf`
2. **每个中文元素都要指定**：title / xlabel / ylabel / xticks / yticks / legend
3. **图例用 `prop`，其他用 `fontproperties`**
4. **考试环境通常是 Windows**，黑体路径固定

---

## 关联知识

- [[groupby-value-counts-unstack]]：分组统计与可视化
- [[data-visualization]]：数据可视化基础
