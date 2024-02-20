# 

### 分区表统计收集

```sql
execute dbms_stats.gather_table_stats(ownname => '{ownname}', tabname => '{tabname}', 
partname => '{partname}', estimate_percent => null, method_opt => 'for all indexed columns', 
cascade => true, degree => 45);

--estimate_percent => null: 表示Oracle将自动决定采样率。
--method_opt => 'for all indexed columns': 意味着对所有已索引的列进行直方图收集。
--cascade => true: 自动收集依赖于该表的所有相关对象（如索引、约束等）的统计信息。
--degree => 45: 收集统计信息时使用的进程数。
```

!!! note "补充"

    无分区的表则去掉`partname => '{partname}'`参数

---
最后更新: 2024/02/07 21:30