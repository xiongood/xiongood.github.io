---
title: postman常用配置
author: 张一雄
summary: 调试的神器，但是现在测试记录默认存在了云端，如果网络不好的话，不建议使用，我就好多次找不到测试记录，而影响了开发进度！
img: https://pub-b24cf0a8c1f14e9386435977aa464959.r2.dev/img/20230816111058.png
categories:
 - 工具
tags:
 - windows
 - postman
---

## 修改主题

![image-20230519171914645](https://pub-b24cf0a8c1f14e9386435977aa464959.r2.dev/img/20230519171915.png)

## 汉化

### 阿里云下载地址

postman安装包+中文补丁

```http
https://www.alipan.com/s/Qnjym6XNZKa
```

### 安装后先关闭自动更新

![image-20240417114654907](https://pub-b24cf0a8c1f14e9386435977aa464959.r2.dev/img/20240417114657.png)

### 查看版本号

![image-20230519171925469](https://pub-b24cf0a8c1f14e9386435977aa464959.r2.dev/img/20230519171926.png)

### 下载对应的版本

```txt
Windows64位
      https://dl.pstmn.io/download/version/版本号/win64​
Windows32位
      https://dl.pstmn.io/download/version/版本号/win32​
Mac Intel Chip
     https://dl.pstmn.io/download/version/版本号/osx_64​
Mac Apple Chip
     https://dl.pstmn.io/download/version/版本号/osx_arm64​
Linux
      https://dl.pstmn.io/download/version/版本号/linux​
```

### 下载汉化包

```http
https://github.com/hlmd/Postman-cn/releases
```

![image-20230519171943150](https://pub-b24cf0a8c1f14e9386435977aa464959.r2.dev/img/20230519171944.png)

### 将下载的包放到安装目录下

![image-20230519171350460](https://pub-b24cf0a8c1f14e9386435977aa464959.r2.dev/img/20230519171351.png)

## 账号

381173411@qq.com

## 问题

### 发送webservice服务出现乱码

修改请求头

```txt
Content-Type application/x-www-form-urlencoded; charset=UTF-8
Accpet text/plain;charset=UTF-8
```

![image-20240514152830386](https://pub-b24cf0a8c1f14e9386435977aa464959.r2.dev/img/20240514152832.png)

























