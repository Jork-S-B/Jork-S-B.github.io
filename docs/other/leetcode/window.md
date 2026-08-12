## 📌 [3. 无重复字符的最长子串](https://leetcode.cn/problems/longest-substring-without-repeating-characters/description/?envType=study-plan-v2&envId=top-100-liked)

给定一个字符串s，请你找出其中不含有重复字符的最长子串的长度。

```python
class Solution:
    @staticmethod
    def lengthOfLongestSubstring(s: str) -> int:
        # 执行超过时间限制
        s_len = len(s)
        max_len = 0
        for i in range(s_len):
            for j in range(i + 1, s_len + 1):  # 切片，左开右闭
                # print(s[i:j])  # 打印所有子串，会有空字符串
                substr = s[i:j]
                substr_len = len(substr)
                if len(set(substr)) == substr_len & substr_len > max_len:
                    max_len = substr_len
        return max_len

    @staticmethod
    def lengthOfLongestSubstring2(s: str) -> int:
        # 通过滑动窗口的方式优化
        # 滑动窗口：使用两个指针 left 和 right 来表示当前窗口的左右边界。
        max_len, left, right = 0, 0, 0
        tmp = []
        while (right < len(s)):
            # right从0开始，出现重复时停止，此时left开始右移并删除字符，直至重复的字符位置
            if s[right] not in tmp:
                tmp.append(s[right])
                right += 1
            else: # 逐次删字符，应该能再优化
                tmp.remove(s[left])
                left += 1
            max_len = max(len(tmp), max_len)
        return max_len

    @staticmethod
    def lengthOfLongestSubstring3(s: str) -> int:
        max_len, left = 0, 0
        tmp = {}  # { char1: 0, char2: 2, ... }，存字符出现的索引
        for right, char in enumerate(s):
            # 当出现重复时，left=字符索引位置右移1个字符
            # tmp[char] >= left，确保left不会超过right
            if char in tmp and tmp[char] >= left:
                left = tmp[char] + 1
            tmp[char] = right  # 每次遍历都更新字符对应的索引
            max_len = max(max_len, right - left + 1)
        return max_len


if __name__ == "__main__":
    s = "abba"
    print(Solution.lengthOfLongestSubstring3(s))
```