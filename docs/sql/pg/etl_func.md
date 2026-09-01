## NVL

NVL(traget, default)

如果 traget 为 NULL，则返回默认值。

## COALESCE

COALESCE(a, b, c, ...)

返回第一个非 NULL 的参数值

## TRIM

TRIM(str)

返回 str 去掉字符串首尾空格后的字符串

## INSTR

INSTR(str, substr)

返回 substr 在 str 中第一次出现的索引位置；如果 substr 不在 str 中，则返回 0。

INSTR('01,02,03,04', '02'), 返回 2

## SUBSTR

SUBSTR(str, start, length)

返回 str 中从 start 开始的 length 个字符。

SUBSTR('YYYYMMDD', 5, 2), 返回 'MM' 

## ROW_NUMBER

ROW_NUMBER() OVER (PARTITION BY column_name1 ORDER BY column_name2)

为查询结果集按`column_name1`分区、按`column_name2`排序，并分配唯一连续编号，从 1 开始，适合用于去重。

## RANK

RANK() OVER (PARTITION BY column_name1 ORDER BY column_name2)

为查询结果集按`column_name1`分区、按`column_name2`排序，并分配排名，从 1 开始。

允许并列排名，如: 1, 1, 3, 4, ...
