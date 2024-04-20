Scala融合了面向对象编程及函数式编程。

* 面向对象：对数据和行为的封装。
* 函数式编程：函数可当做一个值进行传递，具备确定性，适用于高并发、分布式计算。

## 📌 函数和方法

* 函数：1.完成某一功能的程序语句的集合，称为函数。2.没有重载和重写的概念。
* 方法：1.类中的函数称之方法。2.可以进行重载和重写。

## 📌 至简原则

* __如果函数体只有一行代码，可省略花括号__
* __如果返回值类型能推断出来，那么返回值类型可省略为`=>`__
* __如果参数按顺序只使用一次，可直接使用下划线代替__
* __如果参数列表中只有一个参数，小括号可省略__
* 如果没有参数列表，函数声明可以省略小括号，而调用时必须省略小括号
* 如果期望是无返回值类型，可以省略等号
* `return`可省略，以最后一行作为返回值
* 如果有`return`，则必须指定返回值类型
* 如果不关心名称，只关心逻辑处理，那么函数名`def`可以省略，即匿名函数lambda表达式

```scala
object Learn01_FuncSimpify {
  def main(args: Array[String]): Unit = {
    // 参数默认值，一般放在参数列表后面
    // 可变参数，一般放在参数列表最后面
    // 两者不能混用
    def func1(str1: String = "", str2: String) {
      println("str1:" + str1)
      println("str2:" + str2)
    }

    def func2(str_collection: String*): Seq[String] = str_collection

    func1(str2 = "whm")
    val seq = func2("1", "2") // WrappedArray(1, 2)

    // 使用匿名函数：reduceByKey((x + y) => { x + y }) // reduceByKey()，Spark的方法，实现分组+聚合
    // 根据至简原则可简化为：reduceByKey(_ + _)
  }
}

```

## 📌 高阶函数的使用

* 函数作为值进行传递
* 函数作为参数进行传递
* 函数作为返回值进行传递

=== "HighOrderFunc"

    ```scala
    object Learn02_HighOrderFunc {
      def main(args: Array[String]): Unit = {
        def func(n: Int) = n + 1
    
        // 1. 函数作为值进行传递
        val f1 = func _
        // 等价于
        val f2: Int => Int = func
    
        println(f1) // 此时打印func函数的引用
        println(f1(1))
    
    
        // 2. 函数作为参数进行传递
        def calc(function: (Int, Int) => Int, i: Int, i1: Int) = {
          function(i, i1)
        }
    
        //println(calc((a, b) => a + b, 1, 2))
        println(calc(_ + _, 1, 2)) // 上一行的匿名函数进行简化
    
        // 3. 函数作为返回值进行传递
        def func1(): Int => (String => Boolean) = {
          def func2(n1: Int): String => Boolean = { // 好处是可以使用外部函数的变量，这种情况称之为闭包
            def func3(n2: String): Boolean = {
              if (n1.toString == n2 && n2 != "") true else false
            }
            func3
          }
          func2
        }
    
        println(func1()(1)("1"))
        println(func1()(1)("2"))
    
        // 使用匿名函数简化func1函数体
        def simpify_func1(): Int => (String => Boolean) = {
          // 1.使用匿名函数，先省略掉方法名
          // 2.单行代码可省略返回值、花括号
          // 3.函数返回类型可推导，省略为`=>`
          // 4.参数列表已定义了嵌套函数的返回类型，所以匿名函数的参数类型可省略
          n1 => n2 => if (n1.toString == n2 && n2 != "") true else false
        }
    
        println(simpify_func1()(1)("1"))
        println(simpify_func1()(1)("2"))
    
        // 使用柯里化简化func1函数体
        def currying_func1()(n1: Int)(n2: String): Boolean = {
          if (n1.toString == n2 && n2 != "") true else false
        }
    
        println(currying_func1()(1)("1"))
        println(currying_func1()(1)("2"))
     
      }
    }
    ```


=== "函数作为传参的练习"

    ```scala
    // 对数组进行处理，处理过程以函数作为传参，并处理后的结果作为返回值（有点像策略模式？）
    def arrOperation(arr: Array[Int], function: Int => Int): Array[AnyVal] = {
      for (i <- arr) yield function(i)
    }

    val arr: Array[Int] = Array(1, 2, 3, 4, 5)
    // Array是引用类型，不能直接打印
    println(arrOperation(arr, _ * 2).mkString(","))
    println(arrOperation(arr, (i: Int) => if (i % 2 == 0) i else 0).mkString(",")) // todo，如果要把0的从数组中删除，应该怎么处理？
    ```

!!! note "补充"

    * 在函数式编程中，尽量少用多参数函数。
    * 通过函数柯里化，将接受多个参数的函数，转换成一系列接收一个参数的函数。
    * 函数调用时使用了外部函数的变量，这种情况称之为闭包；柯里化的底层一定是闭包。

## 📌 递归

* 要有跳出条件
* 递归层级越多，可能会损耗更多栈空间资源
* 支持`@tailrec`尾递归：在最后一行调用自身而不进行额外计算，及时释放栈空间


```scala
object Learn03_Tailrec {
  def main(args: Array[String]): Unit = {
    /* 递归
    * 要有跳出条件
    * 递归层级越多，可能会损耗更多栈空间资源
    * 支持@tailrec尾递归：在最后一行调用自身而不进行额外计算，及时释放栈空间
    */
    // 尾递归实现阶乘
    def factorial(n: Int): Int = {
      @tailrec
      def fact(n: Int, acc: Int): Int = {
        if (n <= 1) return acc
        fact(n - 1, n * acc)
      }
      fact(n, 1)
    }
    println(factorial(5))
    println(factorial(1))
  }
}
```