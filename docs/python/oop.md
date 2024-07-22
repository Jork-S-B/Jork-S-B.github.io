面向对象：把公共数据封装到对象，类（文件、redis信息等）函数封装到一个类，将函数归类和划分。

实例化：通过类创建一个对象的过程。

## 📌 多态

多态指同一种接口可以有多种不同的实现方式。

鸭子模型是一种动态类型检查的概念，是多态的一种常见实现方式。不限制传参类型，只要求这个对象有函数所期望的方法或属性。

```python
class Duck:
    def quack(self):
        print("Quack!")

class Turkey:
    def quack(self):
        print("Gobble gobble!")

def make_quack(animal):
    animal.quack()

# 创建对象
duck = Duck()
turkey = Turkey()

# 调用函数
make_quack(duck)  # 输出 "Quack!"
make_quack(turkey)  # 输出 "Gobble gobble!"

class Dog:
    def bark(self):
        print("Woof woof!")

dog = Dog()
make_quack(dog)  # 将会抛出 AttributeError: 'Dog' object has no attribute 'quack'

```

## 📌 继承

子类继承父类的属性和方法，子类可以重写父类的方法。

```python
class Base:
    def __init__(self):
        pass

    def func(self):
        # 通过在父类抛NotImplementedError异常约束子类。
        # 面向对象的约束：通过继承，在父类中的方法抛异常，实现对子类的控制。
        raise NotImplementedError("Subclass must implement this abstract method")


class Foo(Base):
    # self优先从子类中查找，子类优先于父类
    def __init__(self):
        super().__init__()  # 如果不显式调用，父类的构造方法不会被执行。
```

### 🚁 抽象类

无法被实例化，用于设计者表达自己的设计意图，并且要求后续的开发者按照设计来泛化实现。

继承抽象类的子类可实例化，必须实现抽象类中的抽象方法。

python中通过`@abstreactmethod`装饰器实现抽象方法

## 📌 特殊成员方法/魔术方法

子类应尽量避免在继承内置类型的同时重写其魔术方法。

### 🚁 __call__

当一个对象被当作函数调用时，即在对象后面加上括号()，便会寻找并调用该对象的`__call__`方法。

在`unittest`中，测试类`TestCase`即通过该方式调用run方法。

### 🚁 __new__

`__new__`方法在创建对象时调用，返回一个对象。

```python
# 限制某个类只能创建一个实例（单例模式）
class Singleton:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

```

### 🚁 __str__

`print(myclass())`  
调用`__str__`方法，返回对象的字符串表示形式。

### 🚁 __dict__

`myclass().__dict__`  
对象的变量转为字典

### 🚁 __doc__

描述信息，当定义类、方法，第一个语句是字符串时，就会被自动赋值给`__doc__`属性。


## 📌 变量

Python中，以单下划线开头的变量作为保护变量，表明不希望用户直接访属性的约定。  
但实际通过`instance._variable`的方式可以访问，但不会被`from module import *`导入。

而双下划线开头的变量表示私有变量，目的是为了防止子类中同名变量或方法的冲突。  
但实际通过`instance._ClassName__variable`的方式可以访问。


