---
title: python 操作word文档
img: https://pub-b24cf0a8c1f14e9386435977aa464959.r2.dev/img/python.jpg
author: 张一雄
summary: python 操作word文档
categories:
 - 后端
tags:
 - python 
---



## python 操作word文档

```
from docx import Document

# 打开一个已存在的Word文档
doc = Document("D:\\bbb.docx")

# 遍历文档中的段落
for para in doc.paragraphs:
    print(para.text)

# 遍历文档中的表格
for table in doc.tables:
    for row in table.rows:
        for cell in row.cells:
            print(cell.text)

## 修改所有的标题
# 定义新的标题文本
new_title_text = '新的标题文本'

# 遍历文档中的每一个段落
for para in doc.paragraphs:
    # 检查段落是否是标题（假设标题使用了内置的标题样式）
    if para.style.name.startswith('Heading'):
        # 修改标题的文本内容
        para.text = "测试的标题"

## 修改表格中的内容
# 遍历文档中的每一个表格
for table in doc.tables:
    # 遍历表格中的每一行
    for row in table.rows:
        # 遍历行中的每一个单元格
        for cell in row.cells:
            # 修改单元格的内容
            cell.text = '1'
# 保存
doc.save('D:\\bbb.docx')
```
