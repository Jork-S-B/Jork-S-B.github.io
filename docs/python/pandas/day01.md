## 📌 基本数据结构

`Series`，一维带标签的数组，每个元素都有一个对应的索引（默认从0开始）。

`DataFrame`，二维带标签的表格，每一列可以包含不同类型的值。由行和列组成，每一列可以有自己的列名，每一行也有自己的行索引。

`DataFrame`的内部结构可以理解为多个`Series`的集合，每个`Series`对应一列数据。

=== "示例"

    ```python
    import pandas as pd
    
    # 自定义列名
    data = {
        'A': [1, 2, 3],
        'B': ['a', 'b', 'c'],
        'C': [True, False, True]
    }
    # 自定义行索引
    index = ['row1', 'row2', 'row3']
    df = pd.DataFrame(data, index=index)
    
    print("DataFrame:")
    print(df)
    
    # 访问特定列
    print("\nColumn 'A':")
    print(df['A'])
    
    # 访问特定行
    print("\nRow 'row1':")
    print(df.loc['row1'])
    
    # 访问特定单元格
    print("\nValue at row 'row2', column 'B':")
    print(df.at['row2', 'B'])
    
    ```

=== "输出"

    ```
    DataFrame:
          A  B      C
    row1  1  a   True
    row2  2  b  False
    row3  3  c   True
    
    Column 'A':
    row1    1
    row2    2
    row3    3
    Name: A, dtype: int64
    
    Row 'row1':
    A        1
    B        a
    C     True
    Name: row1, dtype: object
    
    Value at row 'row2', column 'B':
    b
    ```

## 📌 学习一些方法

### 🚁 读取CSV文件

pd.read_csv(file_path, index_col='date', parse_dates=True)

* index_col='date': 指定哪列被用作行索引。
* parse_dates=True: 尝试解析索引列为日期格式，转换为`datetime`对象。


### 🚁 指定某列进行日期格式转换

date = pd.to_datetime(data['date'], format='%Y%m%d')

### 🚁 手动设置行索引

data.set_index('date', inplace=True)

* inplace=True: 直接在原对象进行操作，而不会返回一个新的对象。

### 🚁 移动指定轴

shift()，默认移动行，搭配上`axis=1`则是移动列。

=== "示例"

    ```python
    import pandas as pd
    
    data = {
        'date': ['2023-01-01', '2023-01-02', '2023-01-03', '2023-01-04'],
        'Close': [100, 105, 110, 115]
    }
    data = pd.DataFrame(data)
    
    print("原始DataFrame:")
    print(data)
    
    # 使用shift(1)并计算limit
    data['limit'] = data['Close'].shift(1) * 1.1
    # # 或者使用assign方法追加新列
    # data = data.assign(limit=data['Close'].shift(1) * 1.1)
    # # 或者直接在原DataFrame修改
    # data.loc[:, 'limit'] = data['Close'].shift(1) * 1.1

    
    print("\n修改后的 DataFrame:")
    print(data)
    
    ```

=== "输出"

    ```
    原始 DataFrame:
             date  Close
    0  2023-01-01    100
    1  2023-01-02    105
    2  2023-01-03    110
    3  2023-01-04    115
    
    修改后的 DataFrame:
             date  Close  up_limit
    0  2023-01-01    100       NaN
    1  2023-01-02    105     110.0
    2  2023-01-03    110     115.5
    3  2023-01-04    115     121.0
    
    ```

### 🚁 转置（Transpose）

df_transposed = df.T

将`dataframe`的行列进行转换，称为转置。

### 🚁 前n行

df.head(10)

返回前10行；参数为空时，默认返回前5行。