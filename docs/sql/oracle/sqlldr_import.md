# sqlldr导入大量数据

sqlldr：SQL Loader的简写，是Oracle提供的一个工具，用于将数据从一个数据库导入另一个数据库。

### 🚁 使用方法

```bash
#!/bin/bash
# 目标数据库连接串
target_dbstr="user/pw@ip:port"
# 待导入的数据文件，格式如：xxxx|xx|xxx|x
file_name=tablename.txt
# 目标表字段，日期的字段需要说明日期格式
field="column1, column2, createdate date 'yyyy-mm-dd hh24:mi:ss', memo"

# 写入ctl文件
table=tablename
cat > ./${table}.ctl << EOF
load data
infile "${file_name}"
append into table ${table}
fields terminated by '|'
TRAILING NULLCOLS
(
${field}
)
EOF

sqlldr userid=${target_dbstr} control=./${table}.ctl log=./${table}.log bad=./${table}.bad

```
!!! note "补充：使用sqluldr2导出查询结果"

    `./sqluldr2 user="user/pw" query="select * from table" head=no field="|" file="./tablename.txt" charset=ZHS16GBK`

---

### 🚁 sqlplus生成ctl文件

上述脚本需要手动填入目标表的字段至field变量，有多个表要导入时就比较麻烦。可以用sqlplus来生成ctl文件，然后用sqlldr导入。

=== "ldr.sh"

    ```sh
    #!/bin/bash
    if [ $# = 0 ] ; then
    echo "使用方法：sh ldr.sh 表名"
    exit;
    fi
    target_dbstr="user/pw@ip:port/db"
    table=$1
    
    # make_ctl.sql参数说明
    # 参数1=目标表名
    # 参数2=truncate|append等装载方式
    # 参数3=字段分隔符
    sqlplus ${target_dbstr} @./make_ctl.sql ${table} append "|"
    
    # APPEND 追加
    # INSERT 默认值，如果原先的表有数据，sqlloader会停止
    # REPLACE 如果原先的表有数据，原先的数据会全部删除
    # TRUNCATE 和replace的相同，会用truncate语句删除现存数据
    
    sqlldr userid=${target_dbstr} control=./${table}.ctl log=./${table}.log bad=./${table}.bad
    ```

=== "make_ctl.sql"

    ```sql
    set echo off                                     
    set heading off                                  
    set verify off
    set feedback off
    set show off
    set trim off                                     
    set pages 0                                      
    set concat on                                    
    set lines 300                                    
    set trimspool on                                 
    set trimout on

    spool &1..ctl                                    
    select 'LOAD DATA'||chr (10)||             
           'INFILE '''||lower (table_name)||'.txt'''||chr (10)||
           '&2 into table '||table_name||chr (10)||
           'FIELDS TERMINATED BY "&3"'|| chr (10)||
           'TRAILING NULLCOLS'||chr (10)||'('        
    from   user_tables                                
    where  table_name = upper ('&1');                
    select decode (rownum, 1, '   ', ' , ')||
           rpad (column_name, 33, ' ')||
           decode (data_type,
                   'VARCHAR2', 'CHAR('||RTRIM(TO_CHAR(DATA_LENGTH+4)) ||')  NULLIF ('||column_name||'=BLANKS)'||' "trim(:'||column_name||')"',
                   'FLOAT',    'DECIMAL EXTERNAL NULLIF('||column_name||'=BLANKS)',
                   'NUMBER',   decode (data_precision, 0,
                               'INTEGER EXTERNAL NULLIF ('||column_name||
                               '=BLANKS)', decode (data_scale, 0,
                               'INTEGER EXTERNAL NULLIF ('||
                               column_name||'=BLANKS)',
                               'DECIMAL EXTERNAL NULLIF ('||
                               column_name||'=BLANKS)')),
                   'DATE',     'DATE "YYYY-MM-DD HH24:MI:SS"  NULLIF ('||column_name||'=BLANKS)',
                   null)
    from   
    (select * from user_tab_columns
    where  table_name = upper ('&1')
    order  by column_id ) t;                           
    select ')'                                       
    from sys.dual;
    spool off 
    quit
    ```

---