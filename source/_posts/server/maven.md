---
title: maven的使用
author: 张一雄
summary: java程序员离不开的jar包管理工具！
img: https://pub-b24cf0a8c1f14e9386435977aa464959.r2.dev/img/20230816150128.png
categories:
 - 后端
tags:
 - maven
 - java
---

## windows安装maven

### maven与jdk对应关系

```http
https://maven.apache.org/docs/history.html
```

### 选择更多版本

![image-20230904164729092](https://pub-b24cf0a8c1f14e9386435977aa464959.r2.dev/img/20230904164730.png)

### 载并解压

```http
https://maven.apache.org/download.cgi
```

![image-20230508152102570](C:/Users/java0/AppData/Roaming/Typora/typora-user-images/image-20230508152102570.png)

### 配置

![image-20230508152221543](https://pub-b24cf0a8c1f14e9386435977aa464959.r2.dev/img/20230508152222.png)![image-20230508152247843](https://pub-b24cf0a8c1f14e9386435977aa464959.r2.dev/img/20230508152248.png)

![image-20230508152343204](https://pub-b24cf0a8c1f14e9386435977aa464959.r2.dev/img/20230508152344.png)

![image-20230508152511676](https://pub-b24cf0a8c1f14e9386435977aa464959.r2.dev/img/20230508152512.png)

### 测试

```sh
mvn -v
```



## 一个简单且完整的配置

```xml
<?xml version="1.0" encoding="UTF-8"?>
<settings xmlns="http://maven.apache.org/SETTINGS/1.2.0"
          xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
          xsi:schemaLocation="http://maven.apache.org/SETTINGS/1.2.0 https://maven.apache.org/xsd/settings-1.2.0.xsd">
  <pluginGroups>
  </pluginGroups>
  <proxies>
  </proxies>
  <servers>
  </servers>
  <mirrors>
    <mirror>  
      <id>alimaven</id>   
      <name>aliyun maven</name>     
      <url>http://maven.aliyun.com/nexus/content/groups/public/</url>  
      <mirrorOf>central</mirrorOf>  
	</mirror>
  </mirrors>
  <profiles>
  </profiles>
</settings>
```
