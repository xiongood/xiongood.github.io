---
title: win11安装mysql(8.0)
categories:
 - 数据库
tags:
 - mysql
 - windows
---

## 说明

近期看了一些win11安装mysql的博客，感觉他人的博客安装起来都特别的复杂。

有的改配置文件，有的用到了命令行，有的改环境变量……

看的人脑袋都发涨。

我感觉，其实mysql的安装并没有那么复杂，直接傻瓜式安装就可以，于是我就试了试，

如下是我的安装记录，简单易行，傻瓜式安装

## 下载

```http
https://downloads.mysql.com/archives/installer/
```

或者用这个

```http
https://downloads.mysql.com/archives/community/
```

![image-20230519182123603](https://img.myfox.fun/img/20230519182124.png)

## 安装

### 只装服务

![image-20230519182158122](https://img.myfox.fun/img/20230519182159.png)

### 选择安装版本

![image-20230519182242594](https://img.myfox.fun/img/20230519182243.png)

### 一路默认下一步，

### 设置root密码

![image-20230519182349834](https://img.myfox.fun/img/20230519182350.png)

### 一路默认下一步

### 安装完成

![image-20230519182458317](https://img.myfox.fun/img/20230519182459.png)

## 链接使用

### 通过Navicat链接

![image-20230519182605903](https://img.myfox.fun/img/20230519182606.png)

### 启动与关闭

win+r，输入 service.msc（或者：右击我的电脑，选择【服务】，选择【服务和应用程序】，选择【服务】）

![image-20230519182718201](https://img.myfox.fun/img/20230519182719.png)

右击选择停止

![image-20230519182805618](https://img.myfox.fun/img/20230519182806.png)

### 设置开机自启动

![image-20230519182900946](https://img.myfox.fun/img/20230519182901.png)

