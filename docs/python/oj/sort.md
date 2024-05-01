## 📌 选择排序 - Selection Sort

时间复杂度：O(n^2)；空间复杂度：O(1)。

🎗 基本思路

1. 在未排序序列中找到最小（或最大）元素，存放到排序序列的起始位置。
2. 再从剩余未排序元素中继续寻找最小（或最大）元素，然后放到已排序序列的末尾。
3. 重复第二步，直到所有元素均排序完毕。

!!! note "补充"

    时间复杂度，表示算法在最坏情况下的时间增长趋势。

    空间复杂度，评估算法在执行过程中所使用的额外空间（不包括输入数据所占用的空间）。

## 📌 快速排序 - Quick Sort

时间复杂度：最好O(nlogn)，最坏O(n^2)；空间复杂度：O(1)。

🎗 基本思路

1. 选定基准值：从待排序的数组中，通常选择第一个或最后一个元素，或者采用随机选择。
2. 分割数组：与基准值作比较，将待排序的数据分割成独立的两部分，其中一部分的所有数据都比另外一部分的所有数据都要小（或大）。
3. 递归排序：对分割后的两部分数据分别进行快速排序。
4. 合并：若在原数组上进行操作，则无需额外空间以及合并。

## 📌 归并排序 - Merge Sort

时间复杂度：O(nlogn)；空间复杂度：O(n)。

🎗 基本思路

1. 分解：将待排序的数组不断分成两个子数组，直到每个子数组只有一个元素为止。
2. 递归排序：对这两个子数组分别进行归并排序。
3. 合并：将两个已排序的子数组合并成一个有序数组，直到最后只剩下一个有序数组为止。合并过程中，需要用到一个辅助数组来暂存合并后的有序数组。

```python
def merge_sort(arr: list):
    if len(arr) <= 1:
        return arr

    # 分解：将数组分成两部分
    mid = len(arr) // 2
    left = arr[:mid]
    right = arr[mid:]

    # 递归排序：分别对左右两部分进行归并排序
    left = merge_sort(left)
    right = merge_sort(right)

    # 合并：将两个已排序的子数组合并成一个有序数组
    return merge(left, right)

def merge(left: list, right: list):
    merged = []
    left_index = 0
    right_index = 0

    # 合并两个子数组，直到其中一个被完全遍历
    while left_index < len(left) and right_index < len(right):
        if left[left_index] <= right[right_index]:
            merged.append(left[left_index])
            left_index += 1
        else:
            merged.append(right[right_index])
            right_index += 1

    # 将未完全遍历的子数组剩余部分添加到merged中
    merged.extend(left[left_index:])
    merged.extend(right[right_index:])

    return merged

arr = [38, 27, 43, 3, 9, 82, 10]
sorted_arr = merge_sort(arr)
print(sorted_arr)  # 输出: [3, 9, 10, 27, 38, 43, 82]

```