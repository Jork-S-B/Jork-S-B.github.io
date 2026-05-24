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


## 📌 [70. 爬楼梯](https://leetcode.cn/problems/climbing-stairs/description/?envType=study-plan-v2&envId=top-100-liked)

假设你正在爬楼梯。需要 n 阶你才能到达楼顶。

每次你可以爬 1 或 2 个台阶。你有多少种不同的方法可以爬到楼顶呢？

```python
class Solution:
    @staticmethod
    def climbStair(n: int) -> int:
        if n == 1:
            return 1
        nums = [0] * (n + 1)  # 空列表
        nums[0], nums[1] = 1, 1  # 初始化
        for i in range(2, n + 1):
            nums[i] = nums[i - 1] + + nums[i - 2]
        return nums[n]


if __name__ == "__main__":
    print(Solution.climbStair(3))
```

## 📌 [198. 打家劫舍](https://leetcode.cn/problems/house-robber/description/?envType=study-plan-v2&envId=top-100-liked)

你是一个专业的小偷，计划偷窃沿街的房屋。每间房内都藏有一定的现金，影响你偷窃的唯一制约因素就是相邻的房屋装有相互连通的防盗系统，如果两间相邻的房屋在同一晚上被小偷闯入，系统会自动报警。

给定一个代表每个房屋存放金额的非负整数数组，计算你 不触动警报装置的情况下 ，一夜之内能够偷窃到的最高金额。

```python
from typing import List


class Solution:

    @staticmethod
    def rob(nums: List[int]) -> int:
        nums_len = len(nums)
        res = [0] * (nums_len + 1)  # 空列表
        res[1] = nums[0]
        for i in range(1, nums_len):
            res[i + 1] = max(nums[i] + res[i - 1], res[i])
        return res[nums_len]


if __name__ == "__main__":
    tmp = [2, 7, 9, 3, 1]
    print(Solution.rob(tmp))
```