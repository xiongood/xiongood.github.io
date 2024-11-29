---
title: plsql的使用技巧
author: 张一雄
summary: oracle官方客户端工具，功能是不少，但是我感觉这软件里面的操作挺反人类的！
img: https://pub-b24cf0a8c1f14e9386435977aa464959.r2.dev/img/sql.jpg
categories:
 - 工具
tags:
 - windows
 - oracle
 - plsql
---

## 常用配置

### 设置中文

![image-20230621093029430](https://pub-b24cf0a8c1f14e9386435977aa464959.r2.dev/img/20230621093030.png)

### 记住密码

![image-20230621093432463](https://pub-b24cf0a8c1f14e9386435977aa464959.r2.dev/img/20230621093433.png)

### 配置快捷键

![image-20230927111432926](https://pub-b24cf0a8c1f14e9386435977aa464959.r2.dev/img/20230927111434.png)

### 设置关键字大写

![image-20231212125352095](https://pub-b24cf0a8c1f14e9386435977aa464959.r2.dev/img/20231212125354.png)

### 修改字体大小

![image-20230621094707294](https://pub-b24cf0a8c1f14e9386435977aa464959.r2.dev/img/20230621094708.png)

### 打开和关闭左侧列表

![image-20230731151931342](https://pub-b24cf0a8c1f14e9386435977aa464959.r2.dev/img/20230731151934.png)

### 设置与使用书签

设置书签-重命名书签-跳转到书签

![image-20230725105416017](https://pub-b24cf0a8c1f14e9386435977aa464959.r2.dev/img/20230725105419.png)

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

![image-20230829150426626](https://pub-b24cf0a8c1f14e9386435977aa464959.r2.dev/img/20230829150427.png)

#### 登录

![image-20230829150504783](https://pub-b24cf0a8c1f14e9386435977aa464959.r2.dev/img/20230829150505.png)





