---
title: windows常用配置
author: 张一雄
summary: 遇到不常见的设置，我就会将其记录在此文档下，持续更新
img: https://img.myfox.fun/img/windows.jpg
categories:
 - 工具
tags:
 - windows
---

## 系统下载

### 官方网站

```http
https://www.microsoft.com/zh-cn/software-download/windows11/
```

![image-20230630155810072](https://img.myfox.fun/img/20230630155811.png)



## 激活系统

可能需要翻墙

```http
https://github.com/TGSAN/CMWTAT_Digital_Edition
```

## 关闭自动更新

![image-20231127091028436](https://img.myfox.fun/img/20231127091030.png)

![image-20240308093143517](https://img.myfox.fun/img/20240308093146.png)

## 永久关闭安全中心

Windows+x，以管理员打开命令提示符（cmd），执行以下命令：

```
reg add "HKEY_LOCAL_MACHINE\SOFTWARE\Policies\Microsoft\Windows Defender" /v "DisableAntiSpyware" /d 1 /t REG_DWORD /f
```

看到提示“操作成功完成”即代表Windows Defender已被关闭，可尝试重启电脑

## 设置cmd背景

![image-20241013103855122](https://img.myfox.fun/img/image-20241013103855122.png)

![image-20241013103910733](https://img.myfox.fun/img/image-20241013103910733.png)

![image-20241013103921419](https://img.myfox.fun/img/image-20241013103921419.png)

## 设置右击菜单

### 自动打开更多选项

win+r  输入cmd 打开输入框

输入

```sh
# 自动打开 （输入后按回车） 重启后生效
reg add HKCU\Software\Classes\CLSID\{86ca1aa0-34aa-4e8b-a509-50c905bae2a2}\InprocServer32 /ve /d "" /f
# 删除自动打开
reg delete "HKCU\Software\Classes\CLSID\{86ca1aa0-34aa-4e8b-a509-50c905bae2a2}" /f
```

### 删除不用的右击菜单

下载并且打开 shexview.exe

![image-20240428181951860](https://img.myfox.fun/img/20240428181954.png)

右击全部，选择disable……



## 关闭通知

有的通知实在是麻烦

![image-20230418223847862](https://img.myfox.fun/img/image-20230418223847862.png)

![image-20230418223916312](https://img.myfox.fun/img/image-20230418223916312.png)

## 输入法

自带的舒服法着实不好用

### 删除自带输入法

![image-20230418223945616](https://img.myfox.fun/img/image-20230418223945616.png)

![image-20230418223954195](https://img.myfox.fun/img/image-20230418223954195.png)

![image-20230418223958619](https://img.myfox.fun/img/image-20230418223958619.png)

### 隐藏搜狗输入法

![image-20230418224018582](https://img.myfox.fun/img/image-20230418224018582.png)

## 设置开机启动

### 设置

![image-20230420101903494](https://img.myfox.fun/img/image-20230420101903494.png)

### 任务管理器

![image-20230420102002418](https://img.myfox.fun/img/image-20230420102002418.png)

### 新增开机启动项

win + R 输入

```sh
shell:startup
```

可打开文件夹

![image-20230420102016644](https://img.myfox.fun/img/image-20230420102016644.png)

将开机启动的快捷方式或者脚本，放入该文件夹下，则开机时会 自动启动

![image-20230420102146222](https://img.myfox.fun/img/image-20230420102146222.png)

## 小键盘不开启

修改注册表是一种较为直接且持久的方法，但请注意，修改注册表前务必备份重要数据，以防操作失误导致系统不稳定。

1. **按下`Win + R`键**，打开“运行”对话框。

2. **输入`regedit`**，然后点击“确定”打开注册表编辑器。

3. **在注册表编辑器中**，依次展开`HKEY_USERS` -> `.DEFAULT` -> `Control Panel` -> `Keyboard`。

4. 双击右侧的`InitialKeyboardIndicators`

   。根据当前值的不同，可能需要将其修改为不同的数值：

   - 如果当前值为“0”，直接改为“2”即可。
   - 如果当前值为“2147483648”，表示Num Lock默认关闭且用户是以快速启动模式登录，此时可以尝试改为“2147483650”或“80000002”。

5. **关闭注册表编辑器**，重启电脑。下次启动时，小键盘应该会自动开启。

![image-20240821090644158](https://img.myfox.fun/img/image-20240821090644158.png)

## 关于浏览器

### win11打开ie

![image-20230619165048282](https://img.myfox.fun/img/20230619165049.png)

![image-20230815092844382](https://img.myfox.fun/img/20230815092845.png)

### 安全设置

![image-20230619165230615](https://img.myfox.fun/img/20230619165231.png)

![image-20230619165201344](https://img.myfox.fun/img/20230619165202.png)

### win11打开ie浏览器

#### 桌面右键创建快捷方式

![image-20230815170245783](https://img.myfox.fun/img/20230815170246.png)

#### 输入以下内容

```txt
"C:\Program Files\Internet Explorer\iexplore.exe" https://www.baidu.com/#ie={inputEncoding}&wd=%s -Embedding
```

```txt
"C:\Program Files\Internet Explorer\iexplore.exe" http://127.0.0.1:8080/dz/loginsinoprof.jsp#ie={inputEncoding} -Embedding
```



![image-20230815170406393](https://img.myfox.fun/img/20230815170407.png)

注意：此种方式只能在桌面上打开。

## 设置定时任务

### 开机时启动运行bat文件

#### 打开任务计划程序

taskschd.msc

![image-20230821093212838](https://img.myfox.fun/img/20230821093213.png)

#### 点击常规页签

![image-20230821093327198](https://img.myfox.fun/img/20230821093328.png)

#### 选择触发器

![image-20230821093443802](https://img.myfox.fun/img/20230821093444.png)

#### 选择事件

选择bat文件

![image-20230821093621884](https://img.myfox.fun/img/20230821093622.png)

#### 查看任务

![image-20230821093741773](https://img.myfox.fun/img/20230821093742.png)


## 如何卸载 copilot(预览版)

1、按【Win+R】组合键，打开运行，然后输入【gpedit.msc】命令，按【确定或回车】打开本地组策略编辑器。
2、本地组策略编辑器窗口，依次展开到【用户配置-管理模板-Windows组件-WindowsCopilot】。
3、双击打开【关闭WindowsCopilot】。
4、关闭WindowsCopilot窗口，设置为【已启用】即禁止使用Copilot。

![image-20231116165752021](https://img.myfox.fun/img/20231116165754.png)

## 遇到的问题

