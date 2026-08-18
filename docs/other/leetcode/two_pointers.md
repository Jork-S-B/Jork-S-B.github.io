## 双指针分类

### 对撞

适用场景: **数组已排序**，需要检查首尾元素是否符合要求时。

以`while left < right`为循环

[167. 两数之和 II - 输入有序数组](https://leetcode.cn/problems/two-sum-ii-input-array-is-sorted/description/)

[15. 三数之和](https://leetcode.cn/problems/3sum/description/)

```python
from typing import List


class Solution:
    def threeSum(self, nums: list[int]) -> list[list[int]]:
        """
        给你一个整数数组 nums ，判断是否存在三元组 [nums[i], nums[j], nums[k]] 满足 i != j、i != k 且 j != k ，同时还满足 nums[i] + nums[j] + nums[k] == 0 。请你返回所有和为 0 且不重复的三元组。
        注意：答案中不可以包含重复的三元组。
        """
        length = len(nums)
        if length < 3: return []

        nums.sort()

        res = []
        for i in range(length - 2):
            if nums[i] > 0: break
            # 外层去重：跳过重复的第一个数
            if i > 0 and nums[i] == nums[i - 1]:
                continue

            l = i + 1
            r = length - 1
            while l < r:
                sums = nums[i] + nums[l] + nums[r]
                if sums == 0:
                    res.append([nums[i], nums[l], nums[r]])
                    # 内层去重：跳过左指针重复元素
                    while l < r and nums[l] == nums[l + 1]:
                        l += 1
                    # 内层去重：跳过右指针重复元素
                    while l < r and nums[r] == nums[r - 1]:
                        r -= 1

                    # 同时移动指针，进入下一组可能的组合
                    l += 1
                    r -= 1

                elif sums > 0:
                    r -= 1
                else:
                    l += 1
        return res


if __name__ == '__main__':
    tmp = Solution()
    print(tmp.threeSum([-1, 0, 1, 2, -1, -4]))  # 输出：[[-1, -1, 2],[-1, 0, 1]]
    print(tmp.threeSum([0, 1, 1]))  # 输出：[]
    print(tmp.threeSum([0, 0, 0]))  # 输出：[[0, 0, 0]]
    # 去重检查
    print(tmp.threeSum([0, 0, 0, 0]))  # 输出：[[0, 0, 0]]
    print(tmp.threeSum([1, 2, 0, 1, 0, 0, 0, 0]))  # 输出：[[0, 0, 0]]

    print(tmp.threeSum([-4, 2, 2, 1, 3, 0, 4]))  # 输出：[[-4, 0, 4], [-4, 1, 3], [-4, 2, 2]]
    print(tmp.threeSum([-100, -70, -60, 110, 120, 130, 160]))  # 输出：[[-100, -60, 160],[-70, -60, 130]]

```

### 快慢

适用场景: 需原地修改数组，或过滤/移除元素，或寻找特定长度的子数组。

慢指针负责记录索引，快指针负责遍历查找。

[26. 删除有序数组中的重复项](https://leetcode.cn/problems/remove-duplicates-from-sorted-array/description/)

### 滑动窗口

适用场景：需要寻找满足特定条件（如`和 ≥ target`、`不含重复字符`、`包含特定字符数`）的连续子数组或子串，且数据具有**单调性**（如全为正数）或问题性质允许窗口边界单向移动时。

- `for right in range(n)` 驱动右指针扩展，内层嵌套 `while` 收缩左边界。
- 双指针都从0开始，确保所有元素都被考虑。

[209. 长度最小的子数组](https://leetcode.cn/problems/minimum-size-subarray-sum/description/)

=== "错误解法"

    ```python
    from typing import List


    class Solution:
        def minSubArrayLen(self, target: int, nums: List[int]) -> int:
            """
            给定一个含有 n 个正整数的数组和一个正整数 target 。
            找出该数组中满足其总和大于等于 target 的长度最小的 子数组 [numsl, numsl+1, ..., numsr-1, numsr] ，并返回其长度。如果不存在符合条件的子数组，返回 0 。
            """
            res = len(nums)
            current_sum = nums[0]
            l = 0
            for r in range(1, len(nums), 1):  # 错误点1: 右指针应从0开始，否则当nums[0] >= target时，返回结果错误
                current_sum += nums[r]
                while current_sum >= target:
                    res = min(res, r - l + 1)
                    current_sum -= nums[l]
                    l += 1

            if current_sum < target and l == 0: return 0
            return res


    if __name__ == '__main__':
        tmp = Solution()
        # print(tmp.minSubArrayLen(7, [2, 3, 1, 2, 4, 3]))  # 输出：2
        # print(tmp.minSubArrayLen(4, [1, 4, 4]))  # 输出：1
        # print(tmp.minSubArrayLen(11, [1, 1, 1, 1, 1, 1, 1, 1]))  # 输出：0
        print(tmp.minSubArrayLen(6, [10, 2, 3]))  # 输出：1，实际输出2
    ```

=== "正确解法"

    ```python
    from typing import List


    class Solution:
        def minSubArrayLen(self, target: int, nums: List[int]) -> int:
            """
            给定一个含有 n 个正整数的数组和一个正整数 target 。
            找出该数组中满足其总和大于等于 target 的长度最小的 子数组 [numsl, numsl+1, ..., numsr-1, numsr] ，并返回其长度。如果不存在符合条件的子数组，返回 0 。
            """
            # 或者设置res=无限大: res = float('inf')
            res = len(nums)
            current_sum = 0
            l = 0
            for r in range(len(nums)):
                current_sum += nums[r]
                while current_sum >= target:
                    res = min(res, r - l + 1)
                    current_sum -= nums[l]
                    l += 1

            if current_sum < target and l == 0: return 0  # 左指针未收缩，累计之和都小于target，说明没有符合条件的子数组
            return res


    if __name__ == '__main__':
        tmp = Solution()
        print(tmp.minSubArrayLen(7, [2, 3, 1, 2, 4, 3]))  # 输出：2
        print(tmp.minSubArrayLen(4, [1, 4, 4]))  # 输出：1
        print(tmp.minSubArrayLen(11, [1, 1, 1, 1, 1, 1, 1, 1]))  # 输出：0
        print(tmp.minSubArrayLen(6, [10, 2, 3]))  # 输出：1
    ```

--- 

## 📌 [283. 移动零](https://leetcode.cn/problems/move-zeroes/submissions/572071015/?envType=study-plan-v2&envId=top-100-liked)

给定一个数组`nums`，编写一个函数将所有0移动到数组的末尾，同时保持非零元素的相对顺序。

请注意，必须在不复制数组的情况下原地对数组进行操作。

```java
import java.util.Arrays;

class Solution {

    // 遍历数组，将非0的元素放到前面，将0元素放到后面。
    public static void moveZeroes(int[] nums) {
        int j = 0;
        for (int i = 0; i < nums.length; i++) {
            if (nums[i] != 0) {
                nums[j++] = nums[i];
            }
        }
        for (int i = j; i < nums.length; i++) {
            nums[i] = 0;
        }
    }

    public static void main(String[] args) {
        int[] nums = {0, 1, 0, 3, 12};
        moveZeroes(nums);
        System.out.println(Arrays.toString(nums));
    }
}
```