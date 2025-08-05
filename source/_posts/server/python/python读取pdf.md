---
title: python读取pdf
author: 张一雄
summary: 爬取壁纸网站
categories:
 - 后端
tags:
 - python
 - pdf
---



## 安装包

```shell
pip install pdfminer.six
```
## 读取pdf
```python
import pdfminer.high_level

text = pdfminer.high_level.extract_text('D:\pypdfTest\MFT_SSCM_DT_HQ_00001_采购计划数据传输服务（MFT）-V0.12.pdf')
texts = text.split('服务提供方')
print(text)

```
## 批量读取
```python
import os
import pdfminer.high_level

def get_file_names(directory):
    return [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]


directory = 'D:\pypdfTest'  # 替换为你的文件夹路径
file_names = get_file_names(directory)
for file_name in file_names:
    #print(directory+"/"+file_name)
    # 读取并解析pdf
    text = pdfminer.high_level.extract_text(directory+"/"+file_name)
    print(text)

#print(file_names)

```
