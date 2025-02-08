## 📌 切片

numpy的切片语法，与Python的切片语法基本相同，但可应用于多维数组。

* `array[start:stop:step]`: 用于一维数组的切片。
* `array[row_start:row_stop:row_step, col_start:col_stop:col_step]`: 用于二维数组的切片。
* `array[dim1_start:dim1_stop:dim1_step, dim2_start:dim2_stop:dim2_step, ...]`: 用于多维数组的切片。
* `:`: 表示选择该维度的所有元素。
* `...`: 表示省略中间的维度，自动填充。

=== "多维数组的切片"
    
    ```python
    import numpy as np
    
    arr = np.array([
        [[0, 1, 2],
         [3, 4, 5]],
        [[6, 7, 8],
         [9, 10, 11]],
        [[12, 13, 14],
         [15, 16, 17]]
    ])
    
    # 选择所有三维的前两行和前两列
    print(arr[:, :2, :2])
    # 输出:
    # [[[ 0  1]
    #   [ 3  4]]
    #
    #  [[ 6  7]
    #   [ 9 10]]
    #
    #  [[12 13]
    #   [15 16]]]
    
    # 选择第一个三维的所有行和前两列
    print(arr[0, :, :2])
    # 输出:
    # [[0 1]
    #  [3 4]]
    
    # 选择第一个三维的第2行的所有列
    print(arr[0, 1, :])
    # 输出: [3 4 5]
    
    ```

## 📌 练习

生成10000次蒙特卡洛模拟的股票价格路径（使用向量化计算）

补充：蒙特卡洛模拟（Monte Carlo Simulation）是一种基于随机抽样的计算方法，用于解决复杂问题。

它通过生成大量随机样本，模拟系统的随机行为，从而估计系统的行为和结果的概率分布。

蒙特卡洛模拟广泛应用于金融工程、物理、工程、统计学等领域，特别是在涉及不确定性或复杂系统的建模中。

=== "demo"

    ```python
    import numpy as np
    import matplotlib.pyplot as plt
    
    # 定义参数
    S_0 = 100  # 初始股票价格
    mu = 0.05  # 年化预期收益率
    sigma = 0.2  # 年化波动率
    T = 1  # 模拟1年
    dt = 0.01  # 每天的时间步长
    num_simulations = 10000  # 模拟10000次
    
    # 计算时间步长的数量
    num_steps = int(T / dt)
    
    # 生成随机数
    # 生成形状为 (num_simulations, num_steps) 的标准正态分布随机数
    Z = np.random.normal(0, 1, (num_simulations, num_steps))
    
    # 初始化股票价格路径数组，形状为 (num_simulations, num_steps + 1)
    S = np.zeros((num_simulations, num_steps + 1))
    S[:, 0] = S_0  # 设置初始股票价格
    
    # 计算股票价格路径
    for t in range(1, num_steps + 1):
        # 套入几何布朗运动公式
        # np.exp(n)，无理数e的n次方
        # np.sqrt(n)，求n的平方根
        S[:, t] = S[:, t-1] * np.exp((mu - 0.5 * sigma**2) * dt + sigma * np.sqrt(dt) * Z[:, t-1])
    
    # 设置中文字体
    plt.rcParams['font.sans-serif'] = ['SimHei']  # 使用黑体
    plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题
    
    # 绘制部分模拟路径
    plt.figure(figsize=(12, 6))
    plt.plot(S[:10].T)  # 绘制前10条路径
    plt.title('蒙特卡洛模拟的股票价格路径')
    plt.xlabel('时间步长')
    plt.ylabel('股票价格')
    plt.grid(True)
    plt.show()
    
    # 绘制最后一天的股票价格分布
    plt.figure(figsize=(12, 6))
    plt.hist(S[:, -1], bins=50, density=True, alpha=0.7, color='blue')
    plt.title('最后一天的股票价格分布')
    plt.xlabel('股票价格')
    plt.ylabel('概率密度')
    plt.grid(True)
    plt.show()
    
    ```

=== "使用向量化计算优化"
    
    ```python
    import numpy as np
    import matplotlib.pyplot as plt
    
    # 定义参数
    S_0 = 100  # 初始股票价格
    mu = 0.05  # 年化预期收益率
    sigma = 0.2  # 年化波动率
    T = 1  # 模拟1年
    dt = 0.01  # 每天的时间步长
    num_simulations = 10000  # 模拟10000次
    
    # 计算时间步长的数量
    num_steps = int(T / dt)
    
    # 生成随机数
    # 生成形状为 (num_simulations, num_steps) 的标准正态分布随机数
    Z = np.random.normal(0, 1, (num_simulations, num_steps))
    
    # 计算每个时间步长的对数收益率
    log_returns = (mu - 0.5 * sigma**2) * dt + sigma * np.sqrt(dt) * Z
    returns = np.exp(log_returns)
    
    # 计算累积乘积
    # 这里不指定axis参数，会将数组水平展开进行计算导致错误
    cumulative_returns = np.cumprod(returns, axis=1)
    
    # 计算股票价格路径
    S_cumprod = S_0 * cumulative_returns
    
    # 绘制部分模拟路径
    plt.figure(figsize=(12, 6))
    plt.plot(S_cumprod[:10].T)  # 绘制前10条路径
    plt.title('使用 np.cumprod 计算的股票价格路径')
    plt.xlabel('时间步长')
    plt.ylabel('股票价格')
    plt.grid(True)
    plt.show()
    
    # 绘制最后一天的股票价格分布
    plt.figure(figsize=(12, 6))
    plt.hist(S_cumprod[:, -1], bins=50, density=True, alpha=0.7, color='green')
    plt.title('使用 np.cumprod 计算的最后一天的股票价格分布')
    plt.xlabel('股票价格')
    plt.ylabel('概率密度')
    plt.grid(True)
    plt.show()
    
    ```