---
title: plsql的使用技巧
author: 张一雄
summary: oracle官方客户端工具，功能是不少，但是我感觉这软件里面的操作挺反人类的！
categories:
 - 工具
tags:
 - windows
 - oracle
 - plsql
---

## 常用配置

### 设置中文

![image-20230621093029430](https://img.myfox.fun/img/20230621093030.png)

### 记住密码

![image-20230621093432463](https://img.myfox.fun/img/20230621093433.png)

### 配置快捷键

![image-20230927111432926](https://img.myfox.fun/img/20230927111434.png)

### 设置关键字大写

![image-20231212125352095](https://img.myfox.fun/img/20231212125354.png)

### 修改字体大小

![image-20230621094707294](https://img.myfox.fun/img/20230621094708.png)

### 打开和关闭左侧列表

![image-20230731151931342](https://img.myfox.fun/img/20230731151934.png)

### 设置与使用书签

设置书签-重命名书签-跳转到书签

![image-20230725105416017](https://img.myfox.fun/img/20230725105419.png)

### 连接远程服务器

#### 修改tnsnames.ora文件

```txt
xe =
  (DESCRIPTION =
    (ADDRESS = (PROTOCOL = TCP)(HOST = 192.168.43.96)(PORT = 1521))
    (CONNECT_DATA =
      (SERVER = DEDICATED)
      (SERVICE_NAME = xe)
    )
  )
```

![image-20230829150426626](https://img.myfox.fun/img/20230829150427.png)

#### 登录

![image-20230829150504783](https://img.myfox.fun/img/20230829150505.png)

## 使用

### 存储过程

#### 查看存错过程包体

选中包名称之后右击，之后可以查看包头包体

![image-20250509154408432](http://img.myfox.fun/img/image-20250509154408432.png)

![image-20250509154427683](http://img.myfox.fun/img/image-20250509154427683.png)

#### 批量编译存储过程

批量编译之后选择编译

![image-20250509154607821](http://img.myfox.fun/img/image-20250509154607821.png)

#### 批量编译存储过程2

![image-20250527113747312](http://img.myfox.fun/img/image-20250527113747312.png)

### 测试存储过程

![image-20250519110720024](http://img.myfox.fun/img/image-20250519110720024.png)

```sql
-- Created on 2025/5/19 by XIONG 
declare 
  -- Local variables here
  i integer;
begin
	-- 此处输入要测试的存储过程
  DECLARE -- 此处定义出参
    v_msg_code   NUMBER;
    v_msg_info   VARCHAR2(4000);
  BEGIN
  	-- 定义要执行的存储过程
    dz_fqlm_business_pkg.DEAL_ZHZT_RET_DATA(
      P_START_DATE => TO_DATE('2025-05-01', 'YYYY-MM-DD'), -- 替换为你需要的日期
      P_MSG_CODE   => v_msg_code,
      P_MSG_INFO   => v_msg_info
    );
	-- 打印出来出参
    DBMS_OUTPUT.PUT_LINE('返回码: ' || v_msg_code);
    DBMS_OUTPUT.PUT_LINE('提示信息: ' || v_msg_info);
  END;
end;
```

### dblinks

#### 设置dblink

![image-20250509154824810](http://img.myfox.fun/img/image-20250509154824810.png)

### 两个库，数据比较迁移

#### 选择库，点击右下角比较按钮

![image-20250514104246681](http://img.myfox.fun/img/image-20250514104246681.png)

#### 比较与迁移

![image-20250514105413172](http://img.myfox.fun/img/image-20250514105413172.png)

#### 查看差异

![image-20250514110131575](http://img.myfox.fun/img/image-20250514110131575.png)

#### 应用于目标库

![image-20250514110144664](http://img.myfox.fun/img/image-20250514110144664.png)
