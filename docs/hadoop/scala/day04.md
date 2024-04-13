Scala融合了面向对象编程及函数式编程。

* 面向对象：对数据和行为的封装。
* 函数式编程：函数可当做一个值进行传递，具备确定性，适用于高并发、分布式计算。

## 📌 函数和方法

* 函数：1.完成某一功能的程序语句的集合，称为函数。2.没有重载和重写的概念。
* 方法：1.类中的函数称之方法。2.可以进行重载和重写。

## 📌 至简原则

* __如果函数体只有一行代码，可省略花括号__
* __如果返回值类型能推断出来，那么:和返回值类型可省略__
* __如果参数按顺序只使用一次，可直接使用下划线代替__
* __如果参数列表中只有一个参数，小括号可省略__
* 如果没有参数列表，函数声明可以省略小括号，而调用时必须省略小括号
* 如果期望是无返回值类型，可以省略等号
* `return`可省略，以最后一行作为返回值
* 如果有`return`，则必须指定返回值类型
* 如果不关心名称，只关心逻辑处理，那么函数名`def`可以省略，即匿名函数lambda表达式

=== "Learn01_FuncSimpify.scala"

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