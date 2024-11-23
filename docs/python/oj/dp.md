```python
from typing import List

class Solution:
    
    @staticmethod
    def generate(numRows: int) -> List[List[int]]:
        # 118. 杨辉三角_leetcode
        # 在「杨辉三角」中，每个数是它左上方和右上方的数的和。
        if numRows == 1:
            return [[1]]
        fib = [0] * (numRows + 1)
        fib[1] = [1]
        fib[2] = [1, 1]

        for n in range(3, numRows + 1):
            num = [1]
            for i in range(1, n - 2 + 1):  # 计算的次数为numRows-2，所以循环次数为numRows-2+1
                num.append(fib[n - 1][i] + fib[n - 1][i - 1])
            num.append(1)
            fib[n] = num

        fib.pop(0)
        return fib

    @staticmethod
    def climbStair(n: int) -> int:
        # 顽猴爬山，每次跳1步或3步，问爬n个台阶有多少种跳跃方式
        if n == 1:
            return 1
        nums = [0] * (n + 1)
        nums[0] = 1
        nums[1] = 1
        for i in range(2, n + 1):
            nums[i] = nums[i - 1] + + nums[i - 3]
        return nums[n]

```