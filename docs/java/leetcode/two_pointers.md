## 📌 283. 移动零

https://leetcode.cn/problems/move-zeroes/submissions/572071015/?envType=study-plan-v2&envId=top-100-liked

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