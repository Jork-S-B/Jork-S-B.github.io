## 📌 运算符

Scala运算符的本质也是对象的方法：

* 当调用对象的方法时，`.`可以省略。
* 当方法没有参数时，`()`可以省略。

=== "Learn01_Operator.scala"

    ```scala
    object Learn01_Operator {
      def main(args: Array[String]): Unit = {
        println(10 / 3) // 输出3
        // println((10.0 / 3).formatted("%2.2f")) // 输出3.33
        // Scala 3.4.1："Use `formatString.format(value)` instead of `value.formatted(formatString)`"
        println("%.2f".format(10.0 / 3)) // 输出3.33
        println(-5 % 3) // 输出2
    
        val s1: String = "abc"
        val s2 = new String("abc")
        println(s1 == s2) // 打印true，比较内容
        println(s1.eq(s2)) // 打印false，比较地址
    
        // scala运算符本质也是对象的方法
        println(1.1.+(2))
        // 1.当调用对象的方法时，.可以省略
        println(1.1 + 2)
        // 2.当方法没有参数时，()可以省略
        println((1.1 + 2) toInt)
      }
    }
    
    ```

## 📌 条件分支

* Scala没有`Switch`，而是使用模式匹配`match-case`来处理。
* Scala的分支语句可以带返回值。

=== "Learn02_Condition.scala"

    ```scala
    import scala.io.StdIn
    
    object Learn02_Condition {
        def main(args: Array[String]): Unit = {
        // Scala的分支语句可以带返回值
        val str = StdIn.readLine().toInt
        var res: Any = if (str > 0) { // 判定语句后只有一行代码时，花括号`{}`可以省略
          println("正数")
          str
        } else if (str == 0) {
          println("零")
          0
        } else {
          println("负数")
          "负数"
        }
        println(res)
    
        // 类似三元运算符的写法
        res = if (str > 0) str else "非正数"
        println(res)
    
    
      }
    }
    ```

## 📌 For循环

=== "Learn03_Cycle.scala"

    ```scala
    import scala.util.control.Breaks
    
    object Learn03_Cycle {
      def main(args: Array[String]): Unit = {
        // 1.for循环，范围遍历，包含边界[1, 3]，并设置步长为3
        for (i <- 1 to 3 by 3) {
          println(i) // 1
        }
    
        // 2.for循环，范围遍历，不包含边界[1, 3)，并设置倒序输出
        for (i <- 1 until 3 reverse ) {
          println(i) // 2, 1
        }
    
        // 3.Scala没有continue语句，以循环守卫代替，类似在循环中加条件判断
        for (i <- 1 to 10 if i % 10 == 0) {
          println(i)
        }
    
        // 4.小数的循环遍历
        import scala.math.BigDecimal.RoundingMode
    
        val start = BigDecimal("10.9")
        val end = BigDecimal("11.0")
        val step = BigDecimal("0.1")
    
        for (i <- start to end by step) {
          println(i.setScale(1, RoundingMode.HALF_UP)) // 四舍五入，保留1位小数
        }
    
        // 5.嵌套循环
        for (i <- 1 to 3; j <- 1 to i) {
          print(s"$j*$i=${i * j}\t")
          if (j == i) println()
        }
    
        // 6.循环中引入变量
        for (i <- 1 until 3; j = 4 - i) {
          // val j = 4-i
          println(j)
        }
    
        // 7.for循环遍历集合，执行操作后返回新的集合
        val list1 = List(8, 9)
        val list2 = for (i <- list1) yield i - 2
        println(list2)
    
        // 8.Scala没有break语句，通过抛出异常的方式来终止循环
        // Breaks类的break方法，实现异常的抛出和捕捉
        Breaks.breakable {
          for (i <- 1 to 10) {
            if (i == 2) Breaks.break()
            println(i)
          }
        }
    
      }
    }
    ```