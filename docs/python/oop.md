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


## 📌 编程规范

### 🚁 类定义时方法的顺序建议

1. 类变量
2. `__new__`
3. `__init__`
4. `__post_init__`，实例化后立即调用，可以用于执行任何必要的后处理或验证
5. 其他魔术方法，如`__len__`,`__bool__`等，具有固定返回类型的，重写时必须返回该类型
6. `@property`，类属性的封装，允许使用点语法访问，并可通过`@<attribute>.setter`、`@<attribute>.deleter`设置或删除属性
7. `@staticmethod`，静态方法，不需要访问实例也不需要访问类属性或方法时；可通过类名直接调方法，不推荐
8. `@classmethod`，类方法，不需要访问实例，但需要访问类属性或方法时；可通过类名直接调方法，不推荐
9. 普通方法
10. 保护或私有方法

### 🚁 具名函数

当函数参数数量较多（一般指多于5个），且参数间有一定相关性时，建议通过类/`namedtuple`(具名元组类)/`@dataclass`等具名形式进行封装。

=== 使用namedtuple

    ```python
    from collections import namedtuple
    
    # 定义一个具名元组类
    Person = namedtuple('Person', ['name', 'age', 'email'])
    
    person1 = Person(name="Alice", age=30, email="alice@example.com")
    # person1.age = 14  # 报错：AttributeError: can't set attribute
    person2 = Person(name="Bob", age=25, email="bob@example.com")
    
    # 访问具名元组的属性
    print(person1.name)  # 输出: Alice
    print(person2.age)   # 输出: 25
    
    # 输出整个具名元组
    print(person1)  # 输出: Person(name='Alice', age=30, email='alice@example.com')
    print(person2)  # 输出: Person(name='Bob', age=25, email='bob@example.com')
    ```

=== 使用dataclass类

    ```python
    from dataclasses import dataclass
    
    @dataclass
    # 默认生成的类是可变的（除非装饰器传参frozen=True）
    class Person:
        name: str
        age: int
        email: str = "example@example.com"  # 可选参数，默认值为 example@example.com
    
    
    # dataclass自动为类生成了 __init__ 方法
    person1 = Person("Alice", 30)
    person1.age = 19
    person2 = Person("Bob", 25, "bob@example.com")
    
    # dataclass自动为类生成了 __repr__ 方法
    print(person1)  # 输出: Person(name='Alice', age=19, email='example@example.com')
    print(person2)  # 输出: Person(name='Bob', age=25, email='bob@example.com')

    """
    什么时候不宜使用：
    1. 需要继承时
    2. 复杂的业务逻辑
    3. 性能敏感
    4. 高度定制化
    """
    ```

--- 