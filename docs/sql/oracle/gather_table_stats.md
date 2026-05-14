`ANALYZE TABLE` 用于**更新表的统计信息**，这些信息是查询优化器选择执行计划的关键依据。

## 核心作用
- **刷新索引的基数（cardinality）**：估算索引列中不同值的数量。
- **更新表的页数和行数估算**：帮助优化器判断是走索引还是全表扫描。
- **提升复杂查询（多表 JOIN、范围查询）的计划质量**：避免因过时统计导致索引失效或选错驱动表。

## 何时需要执行
- **大批量数据变更后**（ INSERT/UPDATE/DELETE 影响超过 10% 的行）。
- **表结构变更**（如新增索引、分区）。
- **查询性能突然下降**，怀疑统计信息陈旧。

## 使用示例
```sql
-- 分析单表
ANALYZE TABLE mydb.users;

-- 分析多个表
ANALYZE TABLE orders, products;
```

## 注意事项
- InnoDB 会在某些条件下（如表打开超过阈值）**自动收集统计信息**，但手动执行能更及时更新。
- 大表上执行 `ANALYZE` 有一定 I/O 开销，建议在**业务低峰期**进行。
- 执行后优化器会使用新统计信息重新评估执行计划（可通过 `EXPLAIN` 验证）。

--- 

## 分区表统计收集

```shell
execute dbms_stats.gather_table_stats(ownname => '{ownname}', tabname => '{tabname}', 
partname => '{partname}', estimate_percent => null, method_opt => 'for all indexed columns', 
cascade => true, degree => 45);

# estimate_percent => null: 表示Oracle将自动决定采样率。
# method_opt => 'for all indexed columns': 意味着对所有已索引的列进行直方图收集。
# cascade => true: 自动收集依赖于该表的所有相关对象（如索引、约束等）的统计信息。
# degree => 45: 收集统计信息时使用的进程数。

# 无分区的表则去掉`partname => '{partname}'`参数
```

---
