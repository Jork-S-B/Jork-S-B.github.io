## 📌 NumPy

`Pandas`是基于`NumPy`构建的，因此它内部确实使用了`ndarray`来实现其核心数据结构。

`ndarray`，多维数组对象， 而`Series`可以看作是一个带索引的`ndarray`。

```python
import numpy as np
import pandas as pd

# 创建一个ndarray
arr = np.array([1, 2, 3, 4, 5])
print(arr)  # 输出: [1 2 3 4 5]

# 创建多维数组，并指定数据类型
multi_dim_arr = np.array([[1, 2, 3], [4, 5, 6]], dtype=np.int32)

# ndarray转换数据类型
arr_float = arr.astype(np.float64)
print(arr_float)  # 输出: [1. 2. 3. 4. 5.]

# 特殊值
# np.nan: 表示缺失值或未定义的数值。
# np.inf 和 -np.inf: 表示正无穷和负无穷。
special_values = np.array([np.nan, np.inf, -np.inf])
print(special_values)  # 输出: [ nan  inf -inf ]
print(special_values.dtype)  # 输出: float64

# 创建一个Series
s = pd.Series([1, 2, 3, 4, 5])
print(s.values)  # 输出: [1 2 3 4 5]，类型为 ndarray

```

!!! note "补充"

    * `ndarray`是连续存储在内存中的，并且支持高效的向量化操作。

    * `ndarray`可直接转换为`Pandas`的数据结构（如`DataFrame`），反之亦然。

## 📌 学习一些功能

### 🚁 生成一个随机数组

np.random.randn(10)

### 🚁 生成服从正态分布的数据

np.random.normal(0.0005, 0.02, 1000)  
生成1000个服从正态分布的日收益率（均值为0.0005，标准差为0.02）

### 🚁 向量化运算

用数组操作替代循环，提升计算效率。

=== "计算累计收益率"

    ```python
    import numpy as np
    
    # 生成1000个服从正态分布的日收益率（均值为0.0005，标准差为0.02）
    returns = np.random.normal(0.0005, 0.02, 1000)
    
    # 设置打印选项，抑制科学计数法，设置为小数点后6位
    np.set_printoptions(suppress=True, precision=6)
    
    # 向量化计算累计收益率
    # 1 + returns, 每个元素+1; np.cumprod, 每个元素累积乘积运算，即nums[i] = nums[i] * nums[i-1]
    cumulative_returns = np.cumprod(1 + returns) - 1
    
    print(f'1000个交易日的累计收益率为{cumulative_returns[-1] * 100:.2f}%')
    ```

=== "正态分布可视化"

    ```python
    import numpy as np
    import matplotlib.pyplot as plt
    import seaborn as sns
    
    # 生成1000个服从正态分布的日收益率（均值为0.0005，标准差为0.02）
    returns = np.random.normal(0.0005, 0.02, 1000)
    
    # 设置打印选项，抑制科学计数法，设置为小数点后6位。
    np.set_printoptions(suppress=True, precision=6)
    
    # 向量化计算累计收益率
    # 1 + returns, 每个元素+1; np.cumprod, 每个元素累积乘积运算，即nums[i] = nums[i] * nums[i-1]
    cumulative_returns = np.cumprod(1 + returns) - 1
    
    print(f'1000个交易日的累计收益率为{cumulative_returns[-1] * 100:.2f}%')
    
    # 设置中文字体
    plt.rcParams['font.sans-serif'] = ['SimHei']  # 使用黑体
    plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题
    
    # 绘制直方图
    plt.figure(figsize=(12, 6))
    
    # 绘制直方图
    # bins=30: 指定直方图的柱数。
    # alpha=0.6: 设置透明度。
    # color='g': 设置颜色为绿色。
    plt.hist(returns, bins=30, density=True, alpha=0.6, color='g', label='Histogram-直方图')
    
    # 绘制核密度估计图
    sns.kdeplot(returns, color='r', label='Kernel Density Estimate-核密度估计图')
    
    # 添加标题和标签
    plt.title('Distribution of Daily Returns-日收益率的正态分布图')
    plt.xlabel('Daily Returns-日收益率')
    plt.ylabel('Density-密度')
    plt.legend()
    
    plt.show()
    
    ```

### 🚁 求平均值

nums.mean(axis=1), 沿着行求平均值。

nums.mean(axis=0), 沿着列求平均值。

### 🚁 修改数组形状/维度

nums.reshape(-1, 1), -1表示自动计算该维度的大小, 1 表示第二维度的大小为1。

### 🚁 广播机制

允许不同形状的数组进行算术运算，而无需显式地复制数据。

广播规则使得数组可以自动扩展以匹配彼此的形状，从而进行元素级操作。

#### 🔧 广播的基本规则

* 对齐维度: 从后向前对齐两个数组的维度。如果两个维度的大小相同或其中一个维度的大小为1，则认为它们是兼容的。
* 扩展维度: 如果两个维度的大小不同，且其中一个维度的大小为1，则该维度会被扩展以匹配另一个维度的大小。
* 不兼容的情况: 如果两个维度的大小不同且都不为1，则无法进行广播，会引发`ValueError`。(如2行2列和2行3列)

=== "对齐维度和扩展维度"

    ```python
    import numpy as np
    
    a = np.array([[1, 2, 3], [4, 5, 6]])  # 形状为 (2, 3)-2行3列
    b = np.array([1, 2])  # 形状为 (2,)-1行2列
    
    # 直接广播运算时会报ValueError
    b = b.reshape(-1, 1)  # 改变形状为 (2, 1)-2行1列
    
    # 使用广播进行减法运算
    c = a - b
    
    print("a-b:\n", c)
    # [[0 1 2]
    # [2 3 4]]
    ```
