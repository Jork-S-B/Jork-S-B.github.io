## 📌 概述

* 基于JVM，和Java完全兼容，可以调用Java代码。
* 兼具函数式编程和面向对象两大特性。
* 适合大数据处理，支持集合类型数据处理，Spark的底层也是用Scala编写。

### 🚁 Sample
=== "HelloWorld.scala"

    ```scala
    /*
      object：关键字，声明一个单例对象（伴生对象），全局只有一份
      伴生对象：为了解决删除static关键字后，但又要实现静态功能而诞生。
    */
    object HelloWorld {
      /*
        def：定义方法，与python定义方法有点类似
        格式为`方法名(参数名: 参数类型): 返回值类型 = { 方法体 }`
        Unit：代表没有返回值
      */
      def main(args: Array[String]): Unit = {
        println("Hello world!")
        System.out.println("Hello world by java")
      }
    }
    ```

## 📌 回归基本功

=== "Student.java"

    ```java
    public class Student {
        private String name;
        private Integer age;
        // 静态属性、静态方法与面向对象思想相悖，面向对象应当是对象属性的访问、对象方法的调用等行为
        private static String school = "tmp_school";
    
        public Student(String name, Integer age) {
            this.name = name;
            this.age = age;
        }
    
        public void printInfo(){
            System.out.println(this.name + " " + this.age + " " + Student.school);
        }
    
        public static void main(String[] args) {
            Student whm = new Student("whm", 26);
            whm.printInfo();
        }
    }
    ```

=== "StudentScala.scala"

    ```scala
    class StudentScala(name: String, var age: Int) {
      // 构造方法的变量如果未声明为类的可变字段（var），则被默认为不可变字段（val）
      def printInfo(): Unit = {
        println(name + " " + age + " " + StudentScala.school)
      }
    }
    
    // 引入伴生对象，私有成员可以互相访问
    // 名称必须一样，且必须在同一文件内
    object StudentScala {
      val school: String = "tmp_school"
    
      def main(args: Array[String]): Unit = {
        val whm = new StudentScala("whm", 26)
        whm.printInfo()
      }
    }
    ```