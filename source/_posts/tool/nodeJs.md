---
title: nodejs的使用
author: 张一雄
summary: 我们前端程序员所依赖的开发运行工具！
img: https://pub-b24cf0a8c1f14e9386435977aa464959.r2.dev/img/nodejs.jpg
categories:
 - 工具
tags:
 - node-js
---

## windows

### 安装node

```http
https://nodejs.org/zh-cn
```

```http
https://nodejs.org/en/download/releases
```

![image-20230518101259936](https://pub-b24cf0a8c1f14e9386435977aa464959.r2.dev/img/20230518101301.png)

![image-20230518101349322](https://pub-b24cf0a8c1f14e9386435977aa464959.r2.dev/img/20230518101350.png)

直接安装

### node常用命令

#### 设置数据源

```sh
# 查看
npm config get registry
# 设置
npm config set registry http://registry.npm.taobao.org/
```

### 查看包信息

```sh
# 查看某包所有版本号
npm view axios versions
npm info axios versions

# 查看某包最新版本号
npm view axios version
npm info axios version

# 查询某项目中的所有包的树形结构
npm ls
```



#### 情况映射

```sh
# 查看
npm config get proxy
# 设置
npm config rm proxy
npm config rm https-proxy
```

### 安装nvm

可以动态的管理node的版本，项目多的时候，还是比较实用的功能

```http
https://github.com/coreybutler/nvm-windows/releases
```

正常安装

```sh
nvm -v
```

#### 配置数据源

安装路径找到settings.txt，新增：

```sh
# 这个有问题
node_mirror: https://npm.taobao.org/mirrors/node/
npm_mirror: https://npm.taobao.org/mirrors/npm/
# 这两个没问题
node_mirror: https://npmmirror.com/mirrors/node/
npm_mirror: https://npmmirror.com/mirrors/npm/
```

### 使用nvm

#### 安装node

```sh
# 查询可安装版本
nvm list available
# 安装
nvm install 16.20.0
# 使用对应版本
nvm use 16.20.0
```

#### 常用命令

![image-20230517181008038](https://pub-b24cf0a8c1f14e9386435977aa464959.r2.dev/img/20230517181009.png)

## linux

