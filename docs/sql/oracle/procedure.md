```sql
DECLARE
	V_MONTH VARCHAR2(20);
	V_SQL VARHCAR2(2000);
	V_COUNT NUMBER(8) := 0;
	CURSOR i is SELECT T.* FROM TABLE_NAME2 WHERE CONDITION;
BEGIN
	SELECT TO_CHAR(SYSDATE, 'YYMMDD') INTO V_MONTH FROM DUAL;
	--以表名拼接当前日期的方式建备份表
	V_SQL := 'CREATE TABLE TABLE_NAME1'||V_MONTH||'AS SELECT FORM TABLE_NAME1'; EXECUTE IMMEDIATE V_SQL;
	
	FOR TEMP1 IN i LOOP
		FOR T2 IN (  --查询结果是202101到202207
		SELECT TO_CHAR(ADD_MONTHS(TO_DATE('202101', 'YYYYMM'), ROWNUM - 1), 'YYYYMM') MONTH 
		    FORM DUAL CONNECT BY ROWNUM <= MONTHS_BETWEEN(TO_DATE('202207', 'YYYYMM'), 
		    TO_DATE('202101', 'YYYYMM')) +1 ) LOOP
			INSERT INTO TABLE_NAME1 SELECT COLUMN1, COLUMN2, T2.MONTH,
			    DECODE(COLUMN3, 'VALUE', 'Y', 'N') FROM TABLE_NAME1' ||V_MONTH;
			V_COUNT := V_COUNT + 1;
			IF MOD(V_COUNT, 1000) = 0 THEN  --入库1000条时提交一次
				COMMIT;
			END IF;
		END LOOP;
	END LOOP;
	DBMS_OUTPUT.PUT_LINE('入库数目为：' || V_COUNT);
END;
```

---