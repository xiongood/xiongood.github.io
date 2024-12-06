---
title: python常用方法
img: https://img.myfox.fun/img/python.jpg
author: 张一雄
summary: 人生苦短，我用python
categories:
 - 后端
tags:
 - python
---

## 常用方法

### 关于字符串

#### 类型转换

```python
item1 ="3.3"
try:
    item1 = float(item1)
    item1 = int(item1)
    item1 = str(item1)
except :
    pass
```

#### 替换字符串

```python
msg = "Hello world! Hello / Python!"

# 替换字符，字符串直接调用replace方法
msg2 = msg.replace('/', '\\')

print(msg2)
```

### 关于数组

#### 创建数组

```python
arr = [1, 2, 3, 4, 5]
print(arr)
```

#### 循环数组

```python
arr = [1, 2, 3, 4, 5]
for item in arr:
    print(item)
```

#### 判断数组中是否包含某元素

```python
arr = [1, 2, 3, 4, 5]
print(10 in arr)
print(10 not in arr)
```

### 关于日期

#### 获取当前日期

```python
from datetime import datetime, timedelta

# 获取当前日期
today = datetime.today()

# 格式化日期为YYYYMM形式
formatted_date = today.strftime('%Y-%m-%d')

```



## 控制电脑

#### 复制粘贴及按键

```python
import pyautogui
import pyperclip

path = "被粘贴的内容"

# 复制需要上传的文件路径
pyperclip.copy(path)
# 粘贴路径
pyautogui.hotkey('ctrl','v')
# 点击回车
pyautogui.press('enter')
```

## 命令

### 打包成exe可执行文件

- 下载工具包

  ```cmd
  pip install pyinstaller
  ```

- 执行命令

  ```cmd
   pyinstaller --onefile --noconsole  .\main.py
  ```

  
