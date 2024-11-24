## 📌 [1. 两数之和](https://leetcode.cn/problems/two-sum/description/?envType=study-plan-v2&envId=top-100-liked)

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
        System.out.println(Arrays.toString(twoSum2(nums, target)));  // 输出[0, 1]
    }
}
```

## 📌 [49. 字母异位词分组](https://leetcode.cn/problems/group-anagrams/description/?envType=study-plan-v2&envId=top-100-liked)

`Map`是接口，定义了键值对映射的基本操作。

`HashMap`是`Map`接口的一个具体实现，提供了基于哈希表的映射关系，适用于大多数非线程安全的场景。

=== "Java版"

    ```Java
    package org.example;
    
    import java.util.ArrayList;
    import java.util.Arrays;
    import java.util.HashMap;
    import java.util.List;
    import java.util.stream.Collectors;
    
    
    class Solution {
        public static List<List<String>> groupAnagrams(String[] strs) {
            HashMap<String, List<String>> map = new HashMap<>();
            for (String str : strs) {
                char[] array = str.toCharArray();
                Arrays.sort(array);
                String key = new String(array);
                List<String> list = map.getOrDefault(key, new ArrayList<String>());
                list.add(str);
                map.put(key, list);
            }
            return new ArrayList<List<String>>(map.values());
        }
    
        public static List<List<String>> groupAnagrams2(String[] strs) {
            HashMap<String, List<String>> map = new HashMap<>();
            // str内按单个字符排序
            for (String str : strs) {
                char[] chars = str.toCharArray();
                Arrays.sort(chars);
                String sortedStr = new String(chars);
    
                // 排序后的字符串作为map的键，匹配的str作为值最近进列表，即[str1、str2]
                // computeIfAbsent，缺少该键时，设置值为列表并追加字符串
                map.computeIfAbsent(sortedStr, key -> new ArrayList<>()).add(str);
            }
    //            return map.values().stream().collect(Collectors.toList());
            return new ArrayList<>(map.values());
        }
    
        public static void main(String[] args) {
            String[] strs = {"eat", "tea", "tan", "ate", "nat", "bat"};
            System.out.println(groupAnagrams(strs));
        }
    }
    ```

=== "Python版"

    ```python
    from collections import defaultdict
    from typing import List
    
    class Solution:
        def groupAnagrams(self, strs: List[str]) -> List[List[str]]:
            hasht = {}
            for st in strs:
                key = "".join(sorted(st))
                if key in hasht.keys():
                    hasht[key].append(st)
                else:
                    hasht[key] = [st]  # 预期返回类型为List[List[str]]，所以需要先指定字典值类型为list
            return list(hasht.values())
    
        # 小优化一下
        def groupAnagrams2(self, strs: List[str]) -> List[List[str]]:
            # defaultdic，特殊的字典，当访问一个不存在的键时，会自动创建一个默认值。
            # 初始化defaultdict，默认值类型为list
            res_dict = defaultdict(list)
    
            # str内按单个字符排序
            for str in strs:
                tmp = sorted(str)  # ['a','e','t']
                key_str = ''.join(tmp)
                # 排序后的字符串作为map的键，匹配的str作为值最近进列表，即[str1、str2]
                res_dict[key_str].append(str)
    
            # 预期返回类型为List[List[str]]
            return list(res_dict.values())
    
    
    if __name__ == "__main__":
        solution = Solution()
        strs = ["eat", "tea", "tan", "ate", "nat", "bat"]
        print(solution.groupAnagrams2(strs))
    ```