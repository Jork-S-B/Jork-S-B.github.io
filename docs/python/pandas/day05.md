回到pandas的功能

## 📌 滚动窗口计算

### 🚁 rolling

series.rolling(window=5): 创建窗口大小为5的滚动窗口对象，并搭配统计方法进行计算。

统计计算方法一览: 

- mean(): 计算滚动窗口的均值。
- std(): 计算滚动窗口的标准差。
- sum(): 计算滚动窗口的总和。
- min(): 计算滚动窗口的最小值。
- max(): 计算滚动窗口的最大值。
- median(): 计算滚动窗口的中位数。
- quantile(q): 计算滚动窗口的分位数。
- apply(func, raw=False, args=(), kwargs={}): 应用自定义函数。
- agg(func, *args, **kwargs): 应用多个聚合函数

```python
import pandas as pd
import numpy as np

# 创建dataframe，从2023-01-01开始，生成100个日期，频率为每天
dates = pd.date_range('2023-01-01', periods=100, freq='D')
# 使用累积和，生成一个具有趋势性的时间序列，类似于股票价格的长期趋势。
data = np.random.randn(100).cumsum()
# 创建DataFrame，日期作为索引，股价作为列
df = pd.DataFrame(data, index=dates, columns=['Value'])

# 计算5日移动平均 (MA5)
# rolling(window=5): 创建窗口大小为5的滚动窗口对象
# mean(): 计算每个时间点前5个数据点的均值。
ma5 = df['Value'].rolling(window=5).mean()

# 同理得ma20
ma20 = df['Value'].rolling(window=20).mean()

# 基于ma20计算布林带
# 计算20日标准差
std_20 = df['Value'].rolling(window=20).std()

# 设定布林带的倍数因子，默认为2
k = 2

# 根据公式，计算布林带上轨 (UB) 和下轨 (LB)
upper_band = ma20 + k * std_20
lower_band = ma20 - k * std_20

# 将布林带添加到DataFrame中
df['MA20'] = ma20
df['Upper_Band'] = upper_band
df['Lower_Band'] = lower_band

# 打印或绘制结果
print(df.tail())

```

### 🚁 expanding

用于计算滚动窗口的累积统计量。

与`rolling`不同，`expanding`窗口大小会随着数据点的增加而逐渐扩大，即从起始点到当前点的所有数据。

常用方法: 

- mean(): 计算累积均值。
- sum(): 计算累积总和。
- std(): 计算累积标准差。
- var(): 计算累积方差。
- median(): 计算累积中位数。
- min(): 计算累积最小值。
- max(): 计算累积最大值。
- apply(func): 应用自定义函数。

```python
import pandas as pd
import numpy as np

# 创建dataframe，从2023-01-01开始，生成100个日期，频率为每天
dates = pd.date_range('2023-01-01', periods=100, freq='D')
# 使用累积和，生成一个具有趋势性的时间序列，类似于股票价格（收盘价）的长期趋势。
data = np.random.randn(100).cumsum()
df = pd.DataFrame(data, index=dates, columns=['Value'])

# 计算每日回报率
df['Return'] = df['Value'].pct_change()

# 使用 expanding 和 apply 计算累积回报率
df['Cumulative_Return'] = df['Return'].add(1).expanding().apply(np.prod) - 1

print(df.tail())
```

## 📌 时间序列处理

### 🚁 pct_change

用于计算数组相较于前一个元素的百分比变化。

DataFrame.pct_change(self, periods=1, fill_method='pad', limit=None, freq=None, **kwargs)

- periods: 默认为1，表示相对于前一个元素计算百分比变化。
- fill_method: 默认为'pad'-使用前向填充缺失值；可选bfill-使用后向填充缺失值。

### 🚁 resample

用于对时间序列数据进行重采样，改变时间序列的频率，例如从日数据转换为月数据。

DataFrame.resample(rule, axis=0, closed=None, label=None, convention='start', kind=None, loffset=None, base=0, on=None, level=None, origin='start_day', offset=None)

- rule: 重采样的频率，包括'D'-天，'W'-周，'M'-月，'Y'-年。
- axis: 指定沿着哪个轴进行重采样。默认为0，即沿着行方向。

返回`DatetimeIndexResampler`或`PeriodIndexResampler`对象，可以进一步进行聚合操作。

```python
# 日线转周线（取每周最后一个交易日的收盘价）
weekly_data = data['Close'].resample('W-FRI').last()
```

## 📌 数据清洗与对齐

### 🚁 dropna

用于删除包含缺失值（NaN）的行或列

### 🚁 ffill

用前一个非缺失值填充缺失值（NaN）

DataFrame.ffill(axis=0, inplace=False, limit=None, downcast=None)

- axis: 0-行，1-列
- inplace: 默认为False，True表示直接在原记录修改。
- limit: 指定最大连续填充的`NaN`值数量。

### 🚁 merge

将`DataFrame`按指定列进行链接，类似SQL中的join操作。
