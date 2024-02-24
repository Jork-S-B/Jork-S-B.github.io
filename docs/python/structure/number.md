- 整型（int）：表示整数。 
- 浮点型（float）：表示带有小数部分的实数。 
- 复数（complex）：表示复数，由实部和虚部组成。

```python
# 创建一个实部为3，虚部为4的复数
def complex_number():
    # complex(3, 4)等价于3 + 4j
    complex1 = 3 + 4j
    complex2 = complex(3, 4)
    assert complex1 == complex2
```

## 📌 需要精确计算时

```python
# 需要精确计算的场景，使用decimal模块而不是浮点数
def decimal_calculate():
    from decimal import Decimal
    print(12.3 * 0.1)
    print(Decimal(12.3) * Decimal('0.1'))
    print(Decimal('12.3') * Decimal('0.1'))
    
    # 输出：
    # 1.2300000000000002
    # 1.230000000000000071054273576
    # 1.23
```