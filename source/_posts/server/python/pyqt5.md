---
title: pyqt的安装及使用
img: https://pub-b24cf0a8c1f14e9386435977aa464959.r2.dev/img/20240416174446.png
author: 张一雄
summary: pyqt的安装及使用
categories:
 - 后端
tags:
 - python
 - pyqt
---

## 安装

在cmd窗口运行

```shell
pip install pyqt5 pyqt5-tools
```

## 使用

### 检验安装的工具是否成功

创建一个python文件，然后进行运行

```python
import sys

from PyQt5 import QtWidgets, QtCore

app = QtWidgets.QApplication(sys.argv)
widget = QtWidgets.QWidget()
widget.resize(400, 100)
widget.setWindowTitle("This is a demo for PyQt Widget.")
widget.show()

exit(app.exec_())

```

出现对如下对话框，则证明安装成功

![image-20240416151326369](https://pub-b24cf0a8c1f14e9386435977aa464959.r2.dev/img/20240416151328.png)

在设置中查看是否已经安装成功

![image-20240416151635871](https://pub-b24cf0a8c1f14e9386435977aa464959.r2.dev/img/20240416151638.png)

### 设置外部文件

#### QTdesigner

配置两个关键参数：

Program：例如 C:\Users\java0\AppData\Local\Programs\Python\Python310\Lib\site-packages\qt5_applications\Qt\bin\designer.exe

![image-20240416153245273](https://pub-b24cf0a8c1f14e9386435977aa464959.r2.dev/img/20240416153247.png)

#### PyUIC

Program：自己的python.exe路径 例如 C:\xxxx\AppData\Local\Programs\Python\Python35-32\python.exe

Arguments：-m PyQt5.uic.pyuic $FileName$ -o $FileNameWithoutExtension$.py

Working directory：

```txt
$ProjectFileDir$
```

![image-20240416154946801](https://pub-b24cf0a8c1f14e9386435977aa464959.r2.dev/img/20240416154949.png)

#### 测试是否成功

```python
# -*- coding: utf-8 -*-
"""第一个程序"""

from PyQt5 import QtWidgets  # 导入PyQt5部件

import sys

app = QtWidgets.QApplication(sys.argv)  # 建立application对象

first_window = QtWidgets.QWidget()  # 建立窗体对象

first_window.resize(400, 300)  # 设置窗体大小

first_window.setWindowTitle("我的第一个pyqt程序")  # 设置窗体标题

first_window.show()  # 显示窗体

sys.exit(app.exec())  # 运行程序
```

![image-20240416155206351](https://pub-b24cf0a8c1f14e9386435977aa464959.r2.dev/img/20240416155208.png)

## 创建窗口

### 创建

![image-20240416155309852](https://pub-b24cf0a8c1f14e9386435977aa464959.r2.dev/img/20240416155312.png)

![image-20240416155344998](https://pub-b24cf0a8c1f14e9386435977aa464959.r2.dev/img/20240416155347.png)

### 生成ui

ctrl+s 保存成ui文件，之后，可以在项目中看到该项目文件

### 生成py文件

右击文件

![image-20240416155948485](https://pub-b24cf0a8c1f14e9386435977aa464959.r2.dev/img/20240416155950.png)

