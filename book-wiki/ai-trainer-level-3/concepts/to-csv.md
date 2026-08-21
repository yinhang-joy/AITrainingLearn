# 数据保存：to_csv()

## 概念

将 DataFrame 保存为 CSV 文件。

## 语法

```python
df.to_csv(filepath)
df.to_csv(filepath, index=False)
df.to_csv(filepath, index=False, encoding='utf-8')
```

## 参数

| 参数 | 默认值 | 说明 |
|---|---|---|
| `filepath` | 必填 | 保存路径（相对路径或绝对路径） |
| `index` | `True` | 是否保存行索引（**考试常设为 False**） |
| `encoding` | `'utf-8'` | 文件编码（中文可能需要 `'utf-8-sig'` 或 `'gbk'`） |
| `sep` | `','` | 分隔符（逗号） |
| `header` | `True` | 是否保存列名 |
| `columns` | `None` | 只保存指定列 |

## 示例

### 示例 1：基本用法（考试常见）

```python
import pandas as pd

# 数据清洗后保存
cleaned_data.to_csv('2.1.1_cleaned_data.csv', index=False)

print("清洗后的数据已保存到 2.1.1_cleaned_data.csv")
```

### 示例 2：index=True vs index=False

```python
data = pd.DataFrame({
    'cylinders': [8, 8, 8],
    'mpg': [18.0, 15.0, 18.0]
})

# index=True（默认，会保存行索引）
data.to_csv('with_index.csv')
# 生成的 CSV 内容：
# ,cylinders,mpg
# 0,8,18.0
# 1,8,15.0
# 2,8,18.0
# ↑ 第一列是无用的索引

# index=False（推荐，不保存索引）
data.to_csv('without_index.csv', index=False)
# 生成的 CSV 内容：
# cylinders,mpg
# 8,18.0
# 8,15.0
# 8,18.0
# ↑ 无索引列，干净整洁
```

### 示例 3：编码问题（中文文件名/数据）

```python
# UTF-8（推荐，跨平台兼容）
data.to_csv('数据.csv', index=False, encoding='utf-8')

# UTF-8 with BOM（Windows Excel 打开中文不乱码）
data.to_csv('数据.csv', index=False, encoding='utf-8-sig')

# GBK（Windows 旧系统）
data.to_csv('数据.csv', index=False, encoding='gbk')
```

### 示例 4：只保存部分列

```python
# 只保存指定列
data.to_csv('output.csv', index=False, columns=['cylinders', 'mpg'])
```

## 常见用法

### 用法 1：保存清洗后的数据（考试场景）

```python
# 数据清洗流程
data = pd.read_csv('auto-mpg.csv')
data = data.dropna()
data['horsepower'] = pd.to_numeric(data['horsepower'], errors='coerce')
data = data.dropna()

# 保存清洗后的数据
data.to_csv('cleaned_data.csv', index=False)
```

### 用法 2：保存训练集和测试集

```python
from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

# 合并特征和目标变量
train_data = X_train.copy()
train_data['mpg'] = y_train

test_data = X_test.copy()
test_data['mpg'] = y_test

# 保存
train_data.to_csv('train.csv', index=False)
test_data.to_csv('test.csv', index=False)
```

### 用法 3：保存时追加时间戳

```python
from datetime import datetime

# 文件名包含时间戳
timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
filename = f'cleaned_data_{timestamp}.csv'
data.to_csv(filename, index=False)
# 生成：cleaned_data_20260820_143052.csv
```

## 易错点

### ⚠️ 错误 1：忘记 index=False

```python
# ❌ 错误（保存时多一列索引）
data.to_csv('output.csv')
# 生成的 CSV：
# ,cylinders,mpg  ← 第一列是无用的索引
# 0,8,18.0
# 1,8,15.0

# ✅ 正确
data.to_csv('output.csv', index=False)
# 生成的 CSV：
# cylinders,mpg
# 8,18.0
# 8,15.0
```

### ⚠️ 错误 2：路径错误

```python
# ❌ 错误（相对路径可能保存到意外位置）
data.to_csv('output.csv', index=False)
# 保存到当前工作目录（可能不是你预期的位置）

# ✅ 推荐（使用绝对路径或明确相对路径）
import os
save_path = os.path.join('考生文件夹', '2.1.1_cleaned_data.csv')
data.to_csv(save_path, index=False)
```

### ⚠️ 错误 3：文件被占用

```python
# ❌ 错误（文件已在 Excel 中打开）
data.to_csv('output.csv', index=False)
# PermissionError: [Errno 13] Permission denied

# ✅ 解决方案
# 1. 关闭 Excel 中打开的文件
# 2. 保存为不同文件名
data.to_csv('output_v2.csv', index=False)
```

## 保存后验证

```python
# 保存数据
data.to_csv('cleaned_data.csv', index=False)

# 验证：重新读取并检查
verify_data = pd.read_csv('cleaned_data.csv')
print(f"原数据：{data.shape}")
print(f"保存后：{verify_data.shape}")
print(f"列名一致：{list(data.columns) == list(verify_data.columns)}")
```

## 对比：to_csv vs to_excel

| 方法 | 文件格式 | 适用场景 |
|---|---|---|
| `.to_csv()` | CSV（文本） | 数据交换、机器学习（**考试常用**） |
| `.to_excel()` | Excel（二进制） | 数据报告、人工审核 |

```python
# CSV（推荐，文件小，兼容性好）
data.to_csv('output.csv', index=False)

# Excel（需要安装 openpyxl）
data.to_excel('output.xlsx', index=False)
```

## 完整示例：考试场景

```python
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split

# 数据清洗
data = pd.read_csv('auto-mpg.csv')
data = data.dropna()
data['horsepower'] = pd.to_numeric(data['horsepower'], errors='coerce')
data = data.dropna()

# 标准化
numerical_features = ['displacement', 'horsepower', 'weight', 'acceleration']
scaler = StandardScaler()
data[numerical_features] = scaler.fit_transform(data[numerical_features])

# 特征工程
selected_features = ['cylinders', 'displacement', 'horsepower', 'weight', 
                     'acceleration', 'model year', 'origin']
X = data[selected_features]
y = data['mpg']

# 划分数据集
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 合并特征和目标变量
cleaned_data = X.copy()
cleaned_data['mpg'] = y

# 保存清洗后的数据（不保存索引）
cleaned_data.to_csv('2.1.1_cleaned_data.csv', index=False)

print("\n清洗后的数据已保存到 2.1.1_cleaned_data.csv")
```

## 关联操作

- [[concepts/pandas-read-csv]] 数据加载（读取 CSV）
- [[concepts/dropna]] 缺失值处理（保存前清洗）
- [[concepts/StandardScaler]] 特征标准化（保存前处理）
- [[concepts/train-test-split]] 数据集划分（保存前划分）
