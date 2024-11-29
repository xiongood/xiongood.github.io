---
title: windows下部署recketMQ
img: https://pub-b24cf0a8c1f14e9386435977aa464959.r2.dev/img/recket.jpg
categories:
 - 后端
tags:
 - recketMQ
 - java
---

## 说明

版本选择：4.9.6

### 官网文档

```http
https://rocketmq.apache.org/zh/docs/quickStart/01quickstart
```

### github地址

```http
https://github.com/apache/rocketmq/
```

### 软件下载地址

```http
https://dist.apache.org/repos/dist/release/rocketmq/
```

## 启动

### 修改环境变量

ROCKETMQ_HOME

![image-20230607111046166](https://pub-b24cf0a8c1f14e9386435977aa464959.r2.dev/img/20230607111047.png)

### 启动server

```sh
cd bin
start mqnamesrv.cmd
```

### q启动borker

```sh
start mqbroker.cmd
```

![image-20230607111452222](https://pub-b24cf0a8c1f14e9386435977aa464959.r2.dev/img/20230607111453.png)
