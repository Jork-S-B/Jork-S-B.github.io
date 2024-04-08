# 查询锁表&解锁

1. 查看当前系统中的锁表情况，没有数据即没锁表

    `SELECT * FROM V$LOCKED_OBJECT;`
    
2. 找SESSION_ID对应的SERIAL#

    `SELECT * FROM V$SESSION WHERE SID = '{SESSION_ID}';`

3. 删除SESSION_ID及其SERIAL#以解锁

    `ALTER SYSTEM KILL SESSION '79,51107';`

---
上述步骤组合起来
```sql
DECLARE
	V_SQL VARHCAR2(2000);
	CURSOR i is SELECT SID||','||SERIAL# tmp_SESSION FROM V$SESSION 
	WHERE SID IN (SELECT SESSION_ID FROM V$LOCKED_OBJECT);
BEGIN
	FOR TEMP IN i LOOP
		--''''：外部的单引号包含的内容表示需要拼接的内容，中间两个单引号代表单引号转义字符
		V_SQL := ALTER SYSTEM KILL SESSION ''''||TEMP.tmp_SESSION||'''' ; EXECUTE IMMEDIATE V_SQL;
	END LOOP;
	DBMS_OUTPUT.PUT_LINE(V_SQL);
END;
```

!!! note "补充"

      ```sql
      --查看数据库引起锁表的SQL语句 
      SELECT A.USERNAME, A.MACHINE, A.PROGRAM, A.SID, A.SERIAL#, A.STATUS, C.PIECE, C.SQL_TEXT 
          FROM V$SESSION A, V$SQLTEXT C
          WHERE A.SID IN (SELECT DISTINCT T2.SID FROM V$LOCKED_OBJECT T1, V$SESSION T2 WHERE T1.SESSION_ID = T2.SID)
          AND A.SQL_ADDRESS = C.ADDRESS(+) ORDER BY C.PIECE;
      ```

---