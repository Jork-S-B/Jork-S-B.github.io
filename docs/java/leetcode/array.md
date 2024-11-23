## 📌 [56. 合并区间](https://leetcode.cn/problems/merge-intervals/description/?envType=study-plan-v2&envId=top-100-liked
)

以数组 intervals 表示若干个区间的集合，其中单个区间为 intervals[i] = [starti, endi] 。
请你合并所有重叠的区间，并返回 一个不重叠的区间数组，该数组需恰好覆盖输入中的所有区间 。

```Java
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

class Solution {
    public static int[][] merge(int[][] intervals) {
        // 先排序，第二个参数是匿名函数，比较两个数组的第一个元素，升序
        // 用python语法写则是: intervals.sort(key=lambda x: (x[0], x[1]))
        Arrays.sort(intervals, (a, b) -> a[0] - b[0]);

        List<int[]> res = new ArrayList<>();
        int[] current = intervals[0];
        res.add(current);

        for (int[] interval : intervals) {
            int currentEnd = current[1];
            int nextBegin = interval[0];
            int nextEnd = interval[1];

            if (currentEnd >= nextBegin) {
                // 当前区间结束值大于下一区间开始值，则重叠需要合并区间
                current[1] = Math.max(currentEnd, nextEnd);
            } else {
                // 反之不重叠，追加至arraylist即可
                res.add(interval);
                current = interval;  // 用于下次循环进行比较
            }
        }

        return res.toArray(new int[res.size()][]);
    }

    public static void main(String[] args) {
        int[][] intervals = {{1, 3}, {2, 6}, {8, 10}, {15, 18}};
        int[][] tmp = merge(intervals);
        for (int[] interval : tmp) {
            System.out.println(Arrays.toString(interval));
        }
    }
}
```