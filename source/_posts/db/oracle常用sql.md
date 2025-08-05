---
title: oracle常用sql
summary: oracle常用sql，持续更新
categories:
 - 数据库
tags:
 - orcle
 - sql
---

## 字符串

### 字符串判断转译

[百度](www.baidu.com)

```sql
decode(status,1,'Y','N')
-- 若果status是1  就返回Y  否则为N

-- 例子
SELECT 
    decode(DCI.DECUCT_FLAG,'Y','是','否') as DECUCT_FLAG,
    DCI.INVOICE_CODE,
    DCI.INVOICE_NUM,
    EFV.Value as INVOICE_TYPE_CODE,
    DCI.INVOICE_AMOUNT,
    DCI.INVOICE_ATT_ID
    FROM DZ_CLAIM_INVOICE DCI
    left join ets_flex_value_set EFVS on EFVS.CODE = 'INVOICE_TYPE'
    left join ets_flex_values EFV on EFVS.Flex_Value_Set_Id = EFV.Flex_Value_Set_Id and EFV.Code = DCI.INVOICE_TYPE_COD
```

### 小数显示点前零

```sql
select to_char(0.123456,'fm990.000000000') from dual
select to_char(0.123456) from dual
```

### 字符串与日期转换

```sql
-- 日期转字符串
-- 显示：08-11-07 13:22:42
select to_char(sysdate,'yy-mm-dd hh24:mi:ss') from dual   

-- 字符串转日期
--  显示：2005-12-25 13:25:59
select to_date('2005-12-25,13:25:59','yyyy-mm-dd,hh24:mi:ss') from dual 
```

日期格式

```sql
select sysdate from dual;
-- 去掉十分秒
select trunc(sysdate) from dual;
```

### CLOB转字符串

```sql
-- 使用dbms_lob.substr函数
select dbms_lob.substr(message_info) from MQ_SUBSYSTEM_LOG
```

### 替换字符串

```sql
-- 将 . 替换成 -
SELECT REPLACE('HB.SJ.LS.13.02.06', '.','-') FROM dual ;
```

### 判断字符串中包含几个某字符

```sql
SELECT LENGTH('HB.SJ.LS.13.02.06') - LENGTH(REPLACE('HB.SJ.LS.13.02.06', '.')) AS COUNT FROM dual;
```

## 计算

### 对空值进行计算

```sql
-- 空值计算返回结果为空
select null + 10 + 10 from dual;
-- 将空值转换为0再计算为正常结果
select nvl(null,0) + 10 + 10 from dual;
-- 字符串拼接没问题
select null || 10 || 10 from dual;
```

## 列转行

```sql
SELECT
replace(WM_CONCAT(DZC.CONFIG_ID),',','、')  ORG_CODES
FROM DZ_ZY_PURCHASE_CONFIG DZC
```

## 取前100行

```sql
SELECT
    *   
FROM
   SUM_PM_LTE_FLOW_CELL_D T0 
   and  rownum < 101
```

## 主键自增

```sql
--创建表
create table blog(
id integer primary key,
title varchar2(200),
content varchar2(20000),
user_id varchar2(45),
pub_date date);

--创建sequence：
create sequence blog_id_sequence
increment by 1
start with 1
nomaxvalue
nocache;

--创建触发器：
create trigger blog_id_autoincrement before
insert on ALARM_RULECODE_TEST2 for each row
when (new.id is null)
begin
select blog_id_sequence.nextval into：new.id from dual;
end;
```

## 根据某字段去重

- 方式一

  ```sql
  DELETE 
  FROM
  	tablename a 　　 
  WHERE
  	a.ROWID !=
  	　　 (
  		　　 SELECT
  		max( b.ROWID ) 
  	FROM
  		tablename b 　　 
  WHERE
  	a.NE_ID = b.NE_ID 　　)
  ```

- 方式二

  ```sql
  -- 根据字段一去重
  select  distinct 字段一,字段二 from 表名;
  ```

## 关于表

### 修改表名称

```sql
ALTER TABLE OLD_NAME RENAME TO NEW_NAME;
```

### 删除表

```sql
DROP TABLE table_name;
```

## 操作表空间

- 创建删除表空间

  ```sql
  -- 创建
  create tablespace NX_IES_DATA 	datafile 'C:\myData\oracle\\NX_IES_DATA.dbf' size 10G;
  -- 删除
  drop tablespace NX_IES_DATA 	 	including contents and datafiles;
  
  -- 表空间不够厚新增
  -- xxxxx_number.dbf 名称不能重复
  alter tablespace tablespace_name add datafile '/xxxx/xxxxx_number.dbf' size 30g autoextend off;
  ```

- 创建用户指定表空间

  ```sql
  -- 创建用户
  create user NX_IES identified by 123456 default tablespace NX_IES_DATA;
  -- 用户新增表空间
  ALTER USER NX_IES QUOTA UNLIMITED ON NX_IES_X;
  -- 角色新增权限
  grant create session to NX_IES;
  grant connect,resource,dba to NX_IES;
  ```

- 查询空间占用率

  ```sql
  
  SELECT UPPER(F.TABLESPACE_NAME) 表空间名,
         D.TOT_GROOTTE_MB 表空间大小_G,
         D.TOT_GROOTTE_MB - F.TOTAL_BYTES 已使用空间_G,
         TO_CHAR(ROUND((D.TOT_GROOTTE_MB - F.TOTAL_BYTES) / D.TOT_GROOTTE_MB * 100,
                       2),
                 '990.99') 使用比,
         F.TOTAL_BYTES 空闲空间_G,
         F.MAX_BYTES 最大块_G
    FROM (SELECT TABLESPACE_NAME,
                 ROUND(SUM(BYTES) / (1024 * 1024 * 1024), 4) TOTAL_BYTES,
                 ROUND(MAX(BYTES) / (1024 * 1024 * 1024), 4) MAX_BYTES
            FROM DBA_FREE_SPACE
           GROUP BY TABLESPACE_NAME) F,
         (SELECT DD.TABLESPACE_NAME,
                 ROUND(SUM(DD.BYTES) / (1024 * 1024 * 1024), 4) TOT_GROOTTE_MB
            FROM DBA_DATA_FILES DD
           GROUP BY DD.TABLESPACE_NAME) D
   WHERE D.TABLESPACE_NAME = F.TABLESPACE_NAME
     AND F.TABLESPACE_NAME IN ('HB_IES_DATA', 'HB_IES_X','HB_BOSS_DATA','HB_BOSS_X','NX_IES_DATA','NX_IES_DATA','NX_BOSS_DATA','NX_BOSS_X')
   ORDER BY 1 DESC;
  ```

## 角色管理

- 创建用户指定表空间

  ```sql
  -- 创建用户
  create user NX_IES identified by 123456 default tablespace NX_IES_DATA;
  
  -- 用户新增表空间
  ALTER USER NX_IES QUOTA UNLIMITED ON NX_IES_X;
  
  -- 角色新增权限
  grant create session to NX_IES;
  grant connect,resource,dba to NX_IES;
  
  -- 删除角色
  drop user NX_IES cascade;
  
  -- 如果无法删除角色
  select sid,serial# from v$session where username='USER_NAME';
  alter system kill session '862,63054';
  drop user NX_IES cascade;
  ```

## 查看sql执行记录

- 查看sql执行记录

  ```sql
  SELECT SQL_TEXT, LAST_ACTIVE_TIME, SQL_FULLTEXT
    FROM v$sql
   where LAST_ACTIVE_TIME >
         to_date('2022-06-01,09:30:59', 'yyyy-mm-dd,hh24:mi:ss')
     and LAST_ACTIVE_TIME <
         to_date('2022-06-01,12:00:00', 'yyyy-mm-dd,hh24:mi:ss')
   ORDER BY LAST_ACTIVE_TIME asc;
  
  SELECT count(*)
    FROM v$sql
   where LAST_ACTIVE_TIME >
         to_date('2022-06-01,09:30:59', 'yyyy-mm-dd,hh24:mi:ss')
     and LAST_ACTIVE_TIME <
         to_date('2022-06-01,12:00:00', 'yyyy-mm-dd,hh24:mi:ss')
   ORDER BY LAST_ACTIVE_TIME asc;
  ```

## 关于序列

```sql
-- 创建序列
create sequence DZ_CLAIM_HEADER_SEQ   
minvalue 1
maxvalue 99999999999999999999
start with 1
increment by 1
cache 20; 

-- 查询序列
select * from user_sequences  where  sequence_name='DZ_CLAIM_HEADER_SEQ';

-- 插入序列
insert into emp values(DZ_CLAIM_HEADER_SEQ.nextval);

-- 获取序列
select DZ_CLAIM_HEADER_SEQ.nextval from dual;
```

## 数据的导入导出

prompt

```bat
# 执行
sqlplus
# 输入账号密码

# 执行一下命令 自动导入
start C:\Users\java0\Desktop\xxxx.sql
```

### 导入DMP

教程出处

```http
https://blog.csdn.net/qq_45040372/article/details/128469659
```

查询文件夹

```sql
select * from dba_directories;
```

![image-20230717093917586](https://img.myfox.fun/img/20230717093918.png)

打开cmd终端

```sh
# expdp system/sys123 dumpfile=文件名.dmp logfile=文件名.log full=y directory=虚拟文件夹名
# @HBB2BDEV 为数据库名称
expdp system/12345678@HBB2BDEV dumpfile=DATA_PUMP_DIR.dmp logfile=DATA_PUMP_DIR.log full=y directory=DATA_PUMP_DIR

# expdp system/sys123@orcl directory=虚拟文件夹名 schemas=(用户1,用户2,用户3,用户4,用户5) dumpfile=文件名.dmp logfile=文件名.log

expdp system/12345678@HBB2BDEV directory=DATA_PUMP_DIR schemas=(hb_ies,hb_boss,nx_ies,nx_boss) dumpfile=DATA_PUMP_DIR.dmp logfile=DATA_PUMP_DIR.log
```



## 存储过程

- 新增

  ```sql
  -- 创建头表存储过程
  create or replace procedure save_DZ_CLAIM_HEADER(P_DOC_NUMBER                IN VARCHAR2,
                                                   P_HEADER_STATUS             IN VARCHAR2,
                                                   P_CLAIM_STATUS              IN VARCHAR2,
                                                   P_OPR_EMPLOYEE_CODE         IN VARCHAR2,
                                                   P_VENDOR_ID                 IN NUMBER,
                                                   P_VENDOR_ACCOUNT_ID         IN NUMBER,
                                                   P_BUSINESS_MAJOR_CLASS_CODE IN VARCHAR2,
                                                   P_CONTRACT_NUM              IN VARCHAR2,
                                                   P_ARRIVE_ATT_ID             IN NUMBER,
                                                   P_PAY_ATT_ID                IN NUMBER,
                                                   P_OTHER_ATT_ID              IN NUMBER,
                                                   P_SUMMARY                   IN VARCHAR2,
                                                   P_CREATED_BY                IN NUMBER,
                                                   P_LAST_UPDATED_BY           IN NUMBER,
                                                   P_MSG_CODE                  OUT NUMBER,
                                                   P_MSG_INFO                  OUT VARCHAR2,
                                                   P_HEADER_ID                 OUT NUMBER,
                                                   P_HEADER_ID_IN              IN NUMBER) as
  begin
    P_MSG_CODE := 0;
    P_MSG_INFO := '';
    P_HEADER_ID := null;
    
    -- if 判断
    if P_HEADER_ID_IN is null 
      then P_HEADER_ID := DZ_CLAIM_HEADER_SEQ.nextval;
    else P_HEADER_ID := P_HEADER_ID_IN;
    end if ;
    
    -- 业务逻辑
    insert into DZ_CLAIM_HEADER
      (HEADER_ID,
       DOC_NUMBER,
       HEADER_STATUS,
       CLAIM_STATUS,
       OPR_EMPLOYEE_CODE,
       VENDOR_ID,
       VENDOR_ACCOUNT_ID,
       BUSINESS_MAJOR_CLASS_CODE,
       CONTRACT_NUM,
       ARRIVE_ATT_ID,
       PAY_ATT_ID,
       OTHER_ATT_ID,
       SUMMARY,
       CREATED_BY,
       CREATION_DATE,
       LAST_UPDATED_BY,
       LAST_UPDATE_DATE)
    values
      (P_HEADER_ID,
       P_DOC_NUMBER,
       P_HEADER_STATUS,
       P_CLAIM_STATUS,
       P_OPR_EMPLOYEE_CODE,
       P_VENDOR_ID,
       P_VENDOR_ACCOUNT_ID,
       P_BUSINESS_MAJOR_CLASS_CODE,
       P_CONTRACT_NUM,
       P_ARRIVE_ATT_ID,
       P_PAY_ATT_ID,
       P_OTHER_ATT_ID,
       P_SUMMARY,
       P_CREATED_BY,
       sysdate,
       P_LAST_UPDATED_BY,
       sysdate);
    commit; -- 提交
  -- 抛出异常
  EXCEPTION
    WHEN OTHERS THEN
      P_MSG_CODE := -99;
      P_MSG_INFO := '保存单据头信息异常！' || SUBSTR(SQLERRM, 1, 300);
  end;
  ```

- 删除存储过程

  ```sql
  drop package paclage_name
  ```

- 调用存储过程

  ```sql
  declare--开始
  v1 number;--出参
  v2 varchar2(20);--出参
  v3 varchar2(20);--出参
  begin
    pro_9('SCOTT',v1,v2,v3);--调用
  end;
  ```

## 索引

```sql
-- 索引的创建语句（简洁）
create index 索引名 on 表名（列名）;
```

## 其他

### 查询某约束在哪个表中使用

```sql
select * from user_indexes where index_name like '%DZ_STOCK_GOODS_HEADER_PK%'
```

### 查询某表在哪些存储过程中使用

```sql
select * from user_dependencies where referenced_name = 'PO_DISTRIBUTION_LINES'
SELECT * FROM USER_SOURCE U WHERE U.TEXT LIKE '%MTL_MATERIAL_TRANS_PO%';
```

### 查询表所占空间大小

```sql
SELECT * FROM (
       SELECT segment_name, round(sum(bytes) / 1024 / 1024, 2) AS size_mb
        FROM dba_segments
        WHERE segment_name IN(
              SELECT table_name FROM User_Tables
        ) 
        GROUP BY segment_name
)
ORDER BY size_mb DESC
```













