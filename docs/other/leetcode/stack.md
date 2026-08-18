## 📌 [20. 有效的括号](https://leetcode.cn/problems/valid-parentheses/description/?envType=study-plan-v2&envId=top-100-liked)

栈，先进后出

1. 使用`Stack`类，继承自`Vector`类，提供了栈的基本操作方法
2. 使用`Deque接口`（双端队列），提供了栈的操作方法，推荐使用`ArrayDeque`
3. 使用`LinkedList`类，提供了`push`和`pop`方法

python的话使用list即可

```Java
class Solution {
    public static boolean isValid(String s) {
        if (s.length() < 2) return false;
        LinkedList<Character> stack = new LinkedList<>();
        for (char c : s.toCharArray()) {
            switch (c) {
                case '(':
                    stack.push(')');
                    break;
                case '{':
                    stack.push('}');
                    break;
                case '[':
                    stack.push(']');
                    break;
                default:
                    // stack.peek();  // 查看栈顶元素而不修改
                    if (stack.isEmpty() || stack.pop() != c) {
                        return false;
                    }
            }
        }
        return stack.isEmpty();
    }

    public static void main(String[] args) {
//        String s = "(";
//        String s = "(()";
        String s = "){";
        System.out.println(isValid(s));
    }
}
```