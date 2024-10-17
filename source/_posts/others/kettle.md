## kettle 安装



## 输入输出的使用

### 简单的例子

#### 输入一个csv文件

![image-20241015145636999](https://pub-b24cf0a8c1f14e9386435977aa464959.r2.dev/img/image-20241015145636999.png)

#### 输出一个xls文件

![image-20241015145844078](https://pub-b24cf0a8c1f14e9386435977aa464959.r2.dev/img/image-20241015145844078.png)

设置数字保留小数

![image-20241015145942237](https://pub-b24cf0a8c1f14e9386435977aa464959.r2.dev/img/image-20241015145942237.png)

### 设置每次处理数据数

![image-20241015150034534](https://pub-b24cf0a8c1f14e9386435977aa464959.r2.dev/img/image-20241015150034534.png)

### 分发与复制

分发，则将数据轮询给子节点；复制则是每个子节点都获取完整的数据

![image-20241015150153114](https://pub-b24cf0a8c1f14e9386435977aa464959.r2.dev/img/image-20241015150153114.png)



### 将excel的两个sheet页放到一个excel中

选择excel

![image-20241015152314908](https://pub-b24cf0a8c1f14e9386435977aa464959.r2.dev/img/image-20241015152314908.png)

选择工作表

![image-20241015152408444](https://pub-b24cf0a8c1f14e9386435977aa464959.r2.dev/img/image-20241015152408444.png)

选择字段

![image-20241015152824858](https://pub-b24cf0a8c1f14e9386435977aa464959.r2.dev/img/image-20241015152824858.png)

设置输出

![image-20241015153133078](https://pub-b24cf0a8c1f14e9386435977aa464959.r2.dev/img/image-20241015153133078.png)

### 连接mysql数据库

1、将驱动放到lib文件夹下

此处有个bug、mysql8需要要5.1.48版本的驱动，否则会报错

![image-20241015154141266](https://pub-b24cf0a8c1f14e9386435977aa464959.r2.dev/img/image-20241015154141266.png)

2、重启客户端

​	略

3、连接数据库

![image-20241015154423757](https://pub-b24cf0a8c1f14e9386435977aa464959.r2.dev/img/image-20241015154423757.png)

![image-20241015162153000](https://pub-b24cf0a8c1f14e9386435977aa464959.r2.dev/img/image-20241015162153000.png)

4、共享数据库

让所有的转换流程都能用到此数据库

![image-20241015162439498](https://pub-b24cf0a8c1f14e9386435977aa464959.r2.dev/img/image-20241015162439498.png)

### 数据库转换excel例子

1、输入一个查询sql

![image-20241015163050588](https://pub-b24cf0a8c1f14e9386435977aa464959.r2.dev/img/image-20241015163050588.png)

2、构建输出节点

![image-20241015163435165](https://pub-b24cf0a8c1f14e9386435977aa464959.r2.dev/img/image-20241015163435165.png)

### 数据库表输出到表

1、没有目标表的时候 需要创建表

![image-20241015165210143](https://pub-b24cf0a8c1f14e9386435977aa464959.r2.dev/img/image-20241015165210143.png)

### 数据库更新、插入更新

此功能不能删除数据

![image-20241015170415386](https://pub-b24cf0a8c1f14e9386435977aa464959.r2.dev/img/image-20241015170415386.png)

### 删除数据库的数据

![image-20241015170918737](https://pub-b24cf0a8c1f14e9386435977aa464959.r2.dev/img/image-20241015170918737.png)

## 转换控件的使用

### 字符串拼接

转换

![image-20241015172525502](https://pub-b24cf0a8c1f14e9386435977aa464959.r2.dev/img/image-20241015172525502.png)

输出

![image-20241015172615799](https://pub-b24cf0a8c1f14e9386435977aa464959.r2.dev/img/image-20241015172615799.png)

### 值映射

![image-20241015173340523](https://pub-b24cf0a8c1f14e9386435977aa464959.r2.dev/img/image-20241015173340523.png)

## 流程控件的使用

### switch/case

![image-20241016094801293](https://pub-b24cf0a8c1f14e9386435977aa464959.r2.dev/img/image-20241016094801293.png)

### 过滤记录

![image-20241016095935041](https://pub-b24cf0a8c1f14e9386435977aa464959.r2.dev/img/image-20241016095935041.png)

## 查询控件

### 数据库查询 左连接

![image-20241016101707656](https://pub-b24cf0a8c1f14e9386435977aa464959.r2.dev/img/image-20241016101707656.png)

### 流查询 左连接

![image-20241016102759645](https://pub-b24cf0a8c1f14e9386435977aa464959.r2.dev/img/image-20241016102759645.png)

## 连接控件

## 作业的使用

### 基础知识

![image-20241016111940811](https://pub-b24cf0a8c1f14e9386435977aa464959.r2.dev/img/image-20241016111940811.png)