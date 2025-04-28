---
title: git的使用
summary: 在工作和学习中，遇到了不常见的命令，我就会记录在这个文章下面，持续更新
img: https://gitee.com/xiongood/image/raw/master/git.jpg
categories:
 - 工具
tags:
 - windows
 - git
---

## 常用命令

### 修改名字和邮箱

```shell
# 查看
git config user.name
git config user.email
# 修改
git config --global user.name "your name"
git config --global user.email "your email"
```

### 刷新.gitignore文件

```sh
第一步：
git rm -r --cached .
去掉已经托管的文件
第二步：修改自己的igonre文件内容
第三步：
git add .
git commit -m "更新igonre文件"
git push
```

### 清空账号密码

```shell
git config --system --unset credential.helper
```

## 将某次提交合并到某个分支

### 找到单次提交的 id

我感觉使用 命令倒是不方便

![image-20230612171733974](https://gitee.com/xiongood/image/raw/master/20230612171735.png)

### 合并

```sh
# 切换分支
git checkout dev2.0
# 更新分支
git pull
# 合并 
# 如果有多次提交，按时间顺序合并，否则会出现冲突
git cherry-pick cac4b3f15b7a23a81fd37291e23a19c4a76c6820
# 提交
git push
```

## 关于分组

### 刷新远程分支

```shell
git fetch
```

### 列出所有分支列表

```shell
git branch
# 列出远程分支列表
git branch -r
# 查询所有分支
git branch -a
```

### 切换分支

```shell
git checkout dev
```

## 设置github令牌

### 生成令牌

![image-20240429192612539](https://gitee.com/xiongood/image/raw/master/20240429192614.png)

![image-20240429192635570](https://gitee.com/xiongood/image/raw/master/20240429192637.png)

### 提交代码

### 清空账号密码

提交时让输入账号密码

此时输入自己的邮箱和生成的令牌就可以了

```shell
// cmd窗口 执行命令
git config --system --unset credential.helper
```

## 回退

### 回退只修改未缓存的内容

```sh
git checkout  ./*
```



## 问题

### 提交报错

![image-20240508160601710](https://gitee.com/xiongood/image/raw/master/20240508160603.png)

执行该命令

git config --system --unset credential.helper

之后重新输入账号密码
