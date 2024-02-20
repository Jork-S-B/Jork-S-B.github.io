# 其他笔记

### 🚁 NUMBER类型

Oracle的number类型，为节省空间会省略掉前面的0，如0.9会以.9展示。

所以需要注意number类型和varchar类型转换后的数值是否正确。

### 🚁 字段截取

|                命令                 | 说明                     |
|:---------------------------------:|:-----------------------|
|  `SUBSTR(CREATEDATE_STR, 1, 6)`   | 截取CREATEDATE_STR的前6个字符 |
| `SUBSTRING(CREATEDATE_STR, 1, 6)` | 同上，但是HiveSQL           |
|         `TRUNC(sysdate)`          | 默认截取系统日期到日，即yyyy-mm-dd |

### 🚁 类似判定语句

=== "CASE WHEN"

    ```sql
    --WHEN可以有多个
    CASE WHEN C.CREATEDATE IS NOT NULL THEN C.CREATEDATE 
         ELSE SYSDATE END CREATEDATE
    ```

=== "DECODE"

    ```sql
    --与CASE WHEN单个判定类似，若EXPRESSION = VALUE，则取RESULT1，否则取RESULT2
    DECODE(EXPRESSION, VALUE, RESULT1, RESULT2)
    ```

### 🚁 加字段时非空及默认值
```sql
ALTER TABLE TABLE_NAME ADD COLUMN VARCHAR2(32) DEFAULT '10001' NOT NULL; 
```

### 🚁 HAVING子查询
```sql
--HAVING子查询，搭配分组函数使用
SELECT AGENTID, CYCLE, REGION, COUNT(1) FROM COMMON.AGENT WHERE CYCLE BETWEEN 201801 AND 202301 
    AND REGION IN (759, 999) GROUP BY AGENTID, CYCLE, REGION HAVING COUNT(1) > 1;
```

### 🚁 某个月份减1
```sql
SELECT TO_CHAR(ADD_MONTHS(SYSDATE, -1), 'YYYYMM') FROM DUAL;

SELECT TO_CHAR(ADD_MONTH(TO_DATE('202401','YYYYMM'),-1),'YYYYMM') FROM DUAL;
```

### 🚁 时间倒序排序
```sql
--时间倒序排序，最新的靠前，空的靠后
ORDER BY CREATEDATE DESC NULLS LAST
```

### 🚁 PRINT()

`DBMS_OUTPUT.PUT_LINE('');`


### 🚁 生成数字或字符串

```sql
--生成一个0至1.5内的随机小数，最多4位小数
ROUND(DBMS_RANDOMS.VALUE(0, 1.5), 4)

--生成一个包含10个大写字母的随机字符串
DBMS_RANDOM.STRING('U', 10)
```


### 🚁 闪回机制
```sql
--以DELETE FROM删除的数据可通过TIMESTAMP方式找回
SELECT * FROM TABLE_NAME AS OF TIMESTAMP TO_TIMESTAMP('2023-03-30 10:26:11', 'YYYY-MM-DD HH24:MI:SS') 
    WHERE condition;
```
!!! note "补充"
    
    * `DELETE`操作属于DML，会触发锁；,`TRUNCATE`操作属于DDL，不会触发锁。
    * `DELETE`操作可以使用WHERE关键字，`TRUNCATE`操作不可以。
    * `DELETE`操作会触发触发器，`TRUNCATE`操作不会触发触发器。
    * `DELETE`操作会触发索引，`TRUNCATE`操作不会触发索引。
    * 清空数据量较大的表时可以使用`TRUNCATE`操作，效率较高，但不论哪种删除操作都需***先做好备份***。


### 🚁 全外连接和笛卡尔积

=== "表结构和预置数据"

    ```sql
    -- 假设表结构如下：
    CREATE TABLE students (
        id INT PRIMARY KEY,
        name VARCHAR(100)
    );
    
    CREATE TABLE scores (
        student_id INT,
        subject VARCHAR(50),
        score NUMBER(5,2)
    );
    
    -- 示例数据：
    INSERT INTO students VALUES (1, 'whm1');
    INSERT INTO students VALUES (2, 'whm2');
    INSERT INTO students VALUES (3, 'whm3');
    INSERT INTO scores VALUES (1, 'math', 90.5);
    INSERT INTO scores VALUES (1, 'en', 85.0);
    INSERT INTO scores VALUES (2, 'math', 92.0);
    INSERT INTO scores VALUES (2, 'en', 88.0);
    COMMIT;
    
    -- 查询每个学生的平均成绩：
    SELECT s.id, s.name, AVG(sc.score) AS average_score
    FROM students s
    LEFT JOIN scores sc ON s.id = sc.student_id
    GROUP BY s.id, s.name;
    ```

=== "全外连接"

    ```sql
    --若某个记录在另一个表中没有匹配的记录，则在结果中使用 NULL 值。
    WITH A AS (SELECT ROWNUM AS RN1, T.* FROM scores T where t.subject = 'math') ,
    B AS (SELECT ROWNUM AS RN2, T.* FROM students T )
    SELECT * FROM A FULL OUTER JOIN B ON A.RN1 = B.RN2;
    ```

=== "笛卡尔积"

    ```sql
    --关键字是CROSS JOIN，可以忽略不写
    --首先执行了两个表的笛卡尔积，然后通过WHERE子句进行筛选。
    WITH A AS (SELECT ROWNUM AS RN1, T.* FROM scores T where t.subject = 'math') ,
    B AS (SELECT ROWNUM AS RN2, T.* FROM students T )
    SELECT * FROM A, B WHERE A.RN1 = B.RN2;
    ```

??? note "查询结果"

    === "全外连接"
    
        ```
        {'RN1': 1, 'STUDENT_ID': 1, 'SUBJECT': 'math', 'SCORE': 90.5, 'RN2': 1, 'ID': 1, 'NAME': 'whm1'}
        {'RN1': 2, 'STUDENT_ID': 2, 'SUBJECT': 'math', 'SCORE': 92.0, 'RN2': 2, 'ID': 2, 'NAME': 'whm2'} 
        {'RN1': None, 'STUDENT_ID': None, 'SUBJECT': None, 'SCORE': None, 'RN2': 3, 'ID': 3, 'NAME': 'whm3'}
        ```
    
    === "笛卡尔积"
    
        ```
        --笛卡尔积返回AB两个表中所有可能的组合，会浪费系统资源，并且可能导致性能问题。
        {'RN1': 1, 'STUDENT_ID': 1, 'SUBJECT': 'math', 'SCORE': 90.5, 'RN2': 1, 'ID': 1, 'NAME': 'whm1'}
        {'RN1': 2, 'STUDENT_ID': 2, 'SUBJECT': 'math', 'SCORE': 92.0, 'RN2': 2, 'ID': 2, 'NAME': 'whm2'}
        ```

---
最后更新: 2024/02/06 21:23