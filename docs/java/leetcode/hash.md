
## 📌 1. 两数之和

https://leetcode.cn/problems/two-sum/description/?envType=study-plan-v2&envId=top-100-liked

判断遍历值是否小于`target`，小于时先记录数值及下标`i`

继续往后遍历，找`target-nums[i]`的值，及其下标`j`

若能找到则返回数组`[i,j]`

```Java
import java.util.Arrays;
import java.util.HashMap;

class Solution {
    public static int[] twoSum(int[] nums, int target) {
        // 冒泡，比较两数之和==target
        for (int i = 0; i < nums.length; i++) {
            for (int j = i + 1; j < nums.length; j++) {
                if (nums[i] + nums[j] == target) {
                    return new int[]{i, j};
                }
            }
        }
        return new int[]{};
    }
    
    // 优化
    public static int[] twoSum2(int[] nums, int target) {
        // 遍历存入哈希表，同时判断两数之和==target
        HashMap<Integer, Integer> map = new HashMap<>();
        for(int i = 0 ; i< nums.length; i++){
            if (map.containsKey(target - nums[i])){
                return new int[]{map.get(target - nums[i]), i};
            }
            map.put(nums[i], i);
        }
        return new int[]{};
    }

    public static void main(String[] args) {
        int[] nums = {2, 7, 11, 15};
        int target = 9;
        System.out.println(Arrays.toString(twoSum(nums, target)));
    }
}
```