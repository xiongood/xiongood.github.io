---
title: autojs手机自动化
author: 张一雄
summary: 油猴插件确实好用，希望网络长城早日放开
img: http://img.myfox.fun/img/autojs.jpg
categories:
 - 周边
tags:
 - autojs
---

## scrcpy

### 下载地址

https://github.com/Genymobile/scrcpy

### 手机需要开启的功能

![image-20241102133401986](https://gitee.com/xiongood/image/raw/master/image-20241102133401986.png)

![image-20241102134333969](https://gitee.com/xiongood/image/raw/master/image-20241102134333969.png)

### 启动命令

```sh
scrcpy
```

## autojs

### 安装vscode

略

### 安装插件

![image-20241102142238240](https://gitee.com/xiongood/image/raw/master/image-20241102142238240.png)

### 启动命令

先在手机上启动autojs

然后通过scrcpy连接上手机

ctrl + shift+p

![image-20241102144505436](https://gitee.com/xiongood/image/raw/master/image-20241102144505436.png)

![image-20241102144624981](https://gitee.com/xiongood/image/raw/master/image-20241102144624981.png)

### 常用命令

![image-20241102145004052](https://gitee.com/xiongood/image/raw/master/image-20241102145004052.png)

## 常用语法

### 自动刷抖音

```js
// 打开一个软件
app.launchApp("抖音")

// 休眠
sleep(5000)

// 向上滑动
"auto"

while(true){
    // 滑动
    swipe(500,2000,500,1000,50)
    sleep(5000)
}
```

### 打开设置  点击我的设备

```js
// // 打开一个应用
app.launchApp("设置") 

 // 点击一段文字
var fanwei_xiaoxi = text("我的设备").findOne().bounds(); 
click(fanwei_xiaoxi.centerX(), fanwei_xiaoxi.centerY());
```

### 打开微信，打开通讯录，打开公众号

```js
home()

sleep(1000)

// click('微信')
launchApp("微信");  
sleep(1000)

click('通讯录')
sleep(1000)

click('公众号')
sleep(1000)
toast('xiong')
```

## 其他

### 包不打印日志

![image-20241102191057962](https://gitee.com/xiongood/image/raw/master/image-20241102191057962.png)
