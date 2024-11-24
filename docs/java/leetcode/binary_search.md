## 📌 [35. 搜索插入位置](https://leetcode.cn/problems/search-insert-position/description/?envType=study-plan-v2&envId=top-100-liked)

```Java
// 二分查找的时间复杂度 O(log n)
class Solution {
    public static int searchInsert(int[] nums, int target) {
        int left = 0;
        int right = nums.length - 1;
        int mid;

        while (left <= right) {
            mid = (left + right) / 2;
            if (nums[mid] < target) {
                left = mid + 1;
            } else if (nums[mid] > target) {
                right = mid - 1;
            } else
                return mid;
        }
        return left;  // 找不到target对应的索引位置，则返回应该按顺序插入的位置

    }

    public static void main(String[] args) {
        int[] nums = {1, 3, 5, 6};
        int target = 7;
        System.out.println(searchInsert(nums, target));
    }
}
```

## 📌 [74. 搜索二维矩阵](https://leetcode.cn/problems/search-a-2d-matrix/description/?envType=study-plan-v2&envId=top-100-liked)

```Java
class Solution {
    
    public static boolean searchMatrix(int[][] matrix, int target) {
        int row = matrix.length;  // 3行
        int col = matrix[0].length;  // 4列
        int left = 0;
        int right = row * col - 1;
        int mid;
        while (left <= right) {
            mid = (left + right) / 2;
            // mid除以列数确定区间索引值，mid取余列数确定列索引值
            if (matrix[mid / col][mid % col] < target) {
                left = mid + 1;
            } else if (matrix[mid / col][mid % col] > target) {
                right = mid - 1;
            } else
                return true;
        }
        return false;
    }

    public static void main(String[] args) {
        int [][] matrix = {{1,3,5,7}, {10,11,16,20},{23,30,34,60}};
        int target = 60;
        // target存在于矩阵中，则返回true
        System.out.println(searchMatrix(matrix, target));
    }
}
```