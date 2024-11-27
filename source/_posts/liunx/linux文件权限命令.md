---
title: linux权限命令
author: 张一雄
summary: 我们前端程序员所依赖的开发运行工具！
img: https://pub-b24cf0a8c1f14e9386435977aa464959.r2.dev/img/20230816091455.png
categories:
 - 工具
tags:
 - linux
---

## 方式一

### 给所属用户增加权限

```sh
chmod u+w test.txt 
chmod u+r test.txt 
chmod u+x test.txt 
```

### 给所属用户减少权限

```sh
chmod u-w test.txt 
chmod u-r test.txt 
chmod u-x test.txt 
```

### 给所属组增加权限

```sh
chmod g+w test.txt 
chmod g+r test.txt 
chmod g+x test.txt 
```

### 给所属组减少权限

```sh
chmod g-w test.txt 
chmod g-r test.txt 
chmod g-x test.txt 
```

### 给其他人增加权限

```sh
chmod o+w test.txt 
chmod o+r test.txt 
chmod o+x test.txt 
```

### 给其他人减少权限

```sh
chmod o-w test.txt 
chmod o-r test.txt 
chmod o-x test.txt 
```

## 方式二

### 777

```
chmod 777 test.txt
```

7 代表可读可写可执行，第一个7是所属人，第二个7是所属分组，第三个是其他人

1：可执行

2：可写

3：可写可执行

4：可读

5：可读可执行

6：可写可读

7：可写可读可执行