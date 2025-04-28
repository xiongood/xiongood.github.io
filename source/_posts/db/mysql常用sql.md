---
title: mysqlchangyongsql
img: https://gitee.com/xiongood/image/raw/master/mysql.jpg
categories:
 - 数据库
tags:
 - mysql
---



## **字段处理**

### 判断字段是否为空（转译）

```sql
select ifnull(null,'hello');
select ifnull('','hello');
```

- 拓展：

1.isnull(exper) 判断exper是否为空，是则返回1，否则返回0

2.ifnull(exper1,exper2)判断exper1是否为空，是则用exper2代替

3.nullif(exper1,exper2)如果expr1= expr2 成立，那么返回值为NULL，否则返回值为  expr1。

### 判断后转译

```sql
-- 用case判断
select username,if*(*sex=1,'男','女'*)* as sex from user;
-- 用if判断
SELECT username,*(*CASE sex  WHEN 1 THEN '男'  WHEN 2 THEN  '女'  ELSE '未知' END*)* as sex FROM user;
```

### 类型转换

**注意**：mysql 类型转换并不是用的int float之类的，而且用的其他关键字代替

#### 字符串转数字

```sql
SELECT CAST('123' AS SIGNED);
SELECT CONVERT('123',SIGNED);
SELECT '123'+0;
```

**语法**：

```sql
cast(字段名 as 类型)
```

**全部类型：**
```sql
CHAR[(N)] 字符型

DATE  日期型

DATETIME  日期和时间型

DECIMAL  float型

SIGNED  int

TIME  时间型
```
### 字符串拼接

**括号中的第一个字段为分隔符**

```sql
SELECT CONCAT_WS('-','a','b');
SELECT concat_ws('-', NAME,PHONE) FROM user_t;
```
**直接拼接**
```sql
SELECT concat('a','-','c','-b');
```
### 保留两位小数
```sql
SELECT 100 / 33; -- 3.0303
SELECT ROUND(100 / 33); -- 3
SELECT ROUND(100 / 33, 2); -- 3.03
```
## 分组处理

### 分组查询后拼接其他字段

**分数表的表结构**

![image-20240412193854811](https://gitee.com/xiongood/image/raw/master/20240412193856.png)



**根据姓名分组后拼装科目与分数**

```sql
SELECT name, GROUP_CONCAT(course, ':', score,'分')
FROM score_t
GROUP BY name;
```
**执行结果**

![image-20240412193908598](https://gitee.com/xiongood/image/raw/master/20240412193910.png)

 

### 分组查询后拼接其他字段+排序
```sql
SELECT name, GROUP_CONCAT(course, ':',score order by score ASC separator ',' )
FROM score_t
GROUP BY name;
```
### 分组后对其他字段进行分类汇总

**表结构：**

![image-20240412193917471](https://gitee.com/xiongood/image/raw/master/20240412193919.png)

 

**根据姓名分组，并且汇总每人的请假、旷课、迟到次数：**
```sql
SELECT name                     AS "姓名",
    COUNT(CASE WHEN status = '旷课' THEN 1 END) AS "旷课总数",
    COUNT(CASE WHEN status = '迟到' THEN 1 END) AS "迟到总数",
    COUNT(CASE WHEN status = '请假' THEN 1 END) AS "请假总数"
FROM user_status_t
GROUP BY name;
```
**结果：**

![image-20240412193926985](https://gitee.com/xiongood/image/raw/master/20240412193928.png)

 

### 分组后取某字段最大值的记录

**分数表表结构：**

![image-20240412193934874](https://gitee.com/xiongood/image/raw/master/20240412193936.png)

 

**根据姓名分组，查询出每人的最高分：**
```sql
SELECT A.*
FROM score_t A,
   (SELECT name, max(score) max_Score FROM score_t GROUP BY name) B
WHERE A.name = B.name
 AND A.score = B.max_Score
ORDER BY A.score DESC
```
**查询结果：**

![image-20240412193951983](https://gitee.com/xiongood/image/raw/master/20240412193953.png)

 

### 分组排序并取前n条数据

**表结构：**

![image-20240412193959406](https://gitee.com/xiongood/image/raw/master/20240412194001.png)

 

**根据学科分组，查找每个学科的前两名的同学姓名及分数：**
```sql
SELECT a.*
FROM (
     SELECT t1.*,
        (SELECT COUNT(*) + 1
         FROM score_t
         WHERE score_t.course = t1.course AND score_t.score > t1.score) AS group_id
     FROM score_t t1
   ) a
WHERE a.group_id <= 2
ORDER BY course, group_id;
```
**查询结果：**

![image-20240412194007560](https://gitee.com/xiongood/image/raw/master/20240412194009.png)

 

## 操作表结构

### 排序后取第一名
```sql
SELECT 【字段名】
FROM 【表名】
ORDER BY ID
Mysql
```
### 修改表名
```sql
alter table user_T rename AS user_t;
```
注意：Mysql再liunx环境下，表明区分大小写

### 新增自增主键（不是设置主键自增）
```sql
alter table 【表名】 modify id bigint auto_increment primary key;
```
### 设置主键自增
```sql
alter table person modify id int auto_increment;
```
### 添加字段
```sql
ALTER TABLE t_oneminute_5g_kpi137 ADD pmDrbEstabAtt5qi varchar(50)
```
## 关于索引

### 查看索引
```sql
show index from org_oldperson_leave;
show keys from org_oldperson_leave;
```
### 添加PRIMARY KEY（主键索引）
```sql
ALTER TABLE `table_name` ADD PRIMARY KEY ( `column` )
```
**添加UNIQUE(唯一索引)** 
```sql
ALTER TABLE `table_name` ADD UNIQUE ( `column` ) 
```
### 添加INDEX(普通索引) 
```sql
ALTER TABLE `table_name` ADD INDEX index_name ( `column` ) 
```
### 添加FULLTEXT(全文索引) 
```sql
ALTER TABLE `table_name` ADD FULLTEXT ( `column`) 
```
### 添加多列索引 

**多列索引必须 所有的列同时查询到，才会走多列索引**
```sql
ALTER TABLE `table_name` ADD INDEX index_name ( `column1`, `column2`, `column3` )
```
说明：

联合索引字段顺序为（a,b,c,d）

查询条件为 b a 时生效

查询添加为 a c、c a 时生效

查询条件为 b c 时不生效

#### 测试索引

##### 查看执行计划：
```sql
EXPLAIN select * from STATUS_T where UPDATED_BY =  '1'
```
##### 执行计划中的信息

1、id：包含一组数字，表示查询中执行select子句或操作表的顺序。id相同，可以认为是一组，从上往下顺序执行；在所有组中，id值越大，优先级越高，越先执行。

2、select_type：主要用于区别普通查询, 联合查询, 子查询等复杂查询。

  SIMPLE：查询中不包含子查询或者UNION

  查询中若包含任何复杂的子部分，最外层查询则被标记为：PRIMARY

  在SELECT或WHERE列表中包含了子查询，该子查询被标记为：SUBQUERY

  在FROM列表中包含的子查询被标记为：DERIVED（衍生）

  若第二个SELECT出现在UNION之后，则被标记为UNION；若UNION包含在FROM子句的子查询中，外层SELECT将被标记为：DERIVED

  从UNION表获取结果的SELECT被标记为：UNION RESULT

3、type：表示MySQL在表中找到所需行的方式，又称“访问类型”（ALL、index、range、ref、eq_ref、const、system、NULL），由左至右，由最差到最好

  ALL：Full Table Scan， MySQL将遍历全表以找到匹配的行

  index：Full Index Scan，index与ALL区别为index类型只遍历索引树

  range：索引范围扫描，对索引的扫描开始于某一点，返回匹配值域的行，常见于between、<、>等的查询

  ref：非唯一性索引扫描，返回匹配某个单独值的所有行。常见于使用非唯一索引即唯一索引的非唯一前缀进行的查找

  eq_ref：唯一性索引扫描，对于每个索引键，表中只有一条记录与之匹配。常见于主键或唯一索引扫描

  const、system：当MySQL对查询某部分进行优化，并转换为一个常量时，使用这些类型访问。如将主键置于where列表中，MySQL就能将该查询转换为一个常量

  system是const类型的特例，当查询的表只有一行的情况下， 使用system

  NULL：MySQL在优化过程中分解语句，执行时甚至不用访问表或索引

4、possible_keys：指出MySQL能使用哪个索引在表中找到行，查询涉及到的字段上若存在索引，则该索引将被列出，但不一定被查询使用

5、key：显示MySQL在查询中实际使用的索引，若没有使用索引，显示为NULL

  查询中若使用了覆盖索引，则该索引仅出现在key列表中

6、key_len：表示索引中使用的字节数，可通过该列计算查询中使用的索引的长度

  key_len显示的值为索引字段的最大可能长度，并非实际使用长度，即key_len是根据表定义计算而得，不是通过表内检索出的

7、ref：表示上述表的连接匹配条件，即哪些列或常量被用于查找索引列上的值

8、rows：表示MySQL根据表统计信息及索引选用情况，估算的找到所需的记录所需要读取的行数

9、Extra：包含不适合在其他列中显示但十分重要的额外信息

  Using index：该值表示相应的select操作中使用了覆盖索引（Covering Index）。

  MySQL可以利用索引返回select列表中的字段，而不必根据索引再次读取数据文件

  包含所有满足查询需要的数据的索引称为 覆盖索引（Covering Index）

  注意：如果要使用覆盖索引，一定要注意select列表中只取出需要的列，不可select *，因为如果将所有字段一起做索引会导致索引文件过大，查询性能下降

  Using where：表示MySQL服务器在存储引擎受到记录后进行“后过滤”（Post-filter）,

  如果查询未能使用索引，Using where的作用只是提醒我们MySQL将用where子句来过滤结果集

  Using temporary：表示MySQL需要使用临时表来存储结果集，常见于排序和分组查询

  Using filesort：MySQL中无法利用索引完成的排序操作称为“文件排序”

## 添加注释

### 给表加注释
```sql
alter table test1 comment '修改后的表的注释';
```
### 给字段加注释
```sql
ALTER TABLE reward_notes MODIFY COLUMN pay_type int COMMENT '付款方式，1：微信，2：支付宝';
```
## 关于日期

### 只取年月日
```sql
SELECT CURDATE*()*;
```sql
### 只取时分秒
```sql
SELECT CURTIME*()*;
```
### 取年月日时分秒
```sql
SELECT NOW*()*

SELECT sysdate*()*;
```
### 取任意格式时间
```sql
SELECT date_format(d.ts,'%Y-%m-%d') from tb_call_detail d
```
## 关于表空间

### 操作表空间
```sql
--  创建带字符集的数据库：
create database mydb2 CHARACTER SET=utf8;
--  创建带校验的数据库：
create database mydb3 CHARACTER SET=utf8 COLLATE utf8_general_ci;
--  显示数据库：
show databases;
-- 删除数据库：
DROP DATABASE shujukuba;
-- 修改数据库编码：
ALTER DATABASE shujukuba character set gb2312;
```
### 查看表所占空间
```sql
SELECT TABLE_NAME as tableName ,
concat(((DATA_LENGTH+INDEX_LENGTH)/(1024*1024*1024)),"GB") as Size,
TABLE_ROWS as rows
FROM information_schema.`TABLES`
WHERE TABLE_SCHEMA='数据库名称'
AND TABLE_NAME='表名'
```


## 分区

### 查询分区
```sql
SELECT PARTITION_NAME,PARTITION_METHOD,PARTITION_EXPRESSION,PARTITION_DESCRIPTION,
TABLE_ROWS,SUBPARTITION_NAME,SUBPARTITION_METHOD,SUBPARTITION_EXPRESSION
FROM information_schema.PARTITIONS
WHERE TABLE_SCHEMA=SCHEMA() AND TABLE_NAME='tableName';
```


### 删除分区
```sql
alter table t_scene_monitor_five_g_kpi137 drop partition p20220101;
```


### 新建分区

 

## 关于隔离机制

### 数据库事务隔离级别
```sql
select * from users;
-- 事务隔离级别详解
-- https://zhuanlan.zhihu.com/p/117476959
/*查看数据库事务隔离级别*/
show variables like 'transaction_isolation';
SELECT @@transaction_isolation;

SELECT @@tx_isolation;
show variables like 'tx_isolation';

/*查看数据库有多少事务正在运行*/
select * from information_schema.innodb_trx;

/*设置隔离级别未读未提交*/
set global transaction isolation level read uncommitted
/*设置隔离级别读提交*/;
set global transaction isolation level read committed;
/*设置隔离级别可重复读*/;
set global transaction isolation level repeatable read;
```
## 测试用表

### 学生分数表
```sql
SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for score_t
-- ----------------------------
DROP TABLE IF EXISTS `score_t`;
CREATE TABLE `score_t`  (
              `id` int(11) NOT NULL,
              `name` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '姓名',
              `course` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '科目',
              `score` int(255) NULL DEFAULT NULL COMMENT '分数',
              PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of score_t
-- ----------------------------
INSERT INTO `score_t` VALUES (1, '张三', '数学', 52);
INSERT INTO `score_t` VALUES (2, '李四', '数学', 14);
INSERT INTO `score_t` VALUES (3, '王五', '数学', 56);
INSERT INTO `score_t` VALUES (4, '张三', '语文', 37);
INSERT INTO `score_t` VALUES (5, '李四', '语文', 45);
INSERT INTO `score_t` VALUES (6, '王五', '语文', 21);
INSERT INTO `score_t` VALUES (7, '张三', '英语', 9);
INSERT INTO `score_t` VALUES (8, '李四', '英语', 42);
INSERT INTO `score_t` VALUES (9, '王五', '英语', 37);

SET FOREIGN_KEY_CHECKS = 1;
```
### 学生状态表

```sql
SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for user_status_t
-- ----------------------------
DROP TABLE IF EXISTS `user_status_t`;
CREATE TABLE `user_status_t`  (
                 `id` bigint(20) NOT NULL COMMENT 'id',
                 `name` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '姓名',
                 `status` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '状态',
                 PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of user_status_t
-- ----------------------------
INSERT INTO `user_status_t` VALUES (1, '张三', '旷课');
INSERT INTO `user_status_t` VALUES (2, '李四', '请假');
INSERT INTO `user_status_t` VALUES (3, '王五', '迟到');
INSERT INTO `user_status_t` VALUES (4, '张三', '请假');
INSERT INTO `user_status_t` VALUES (5, '李四', '迟到');
INSERT INTO `user_status_t` VALUES (6, '王五', '旷课');
INSERT INTO `user_status_t` VALUES (7, '张三', '请假');
INSERT INTO `user_status_t` VALUES (8, '李四', '迟到');
INSERT INTO `user_status_t` VALUES (9, '王五', '旷课');
INSERT INTO `user_status_t` VALUES (10, '张三', '请假');
INSERT INTO `user_status_t` VALUES (11, '张三', '请假');
INSERT INTO `user_status_t` VALUES (12, '张三', '请假');

SET FOREIGN_KEY_CHECKS = 1;
```
