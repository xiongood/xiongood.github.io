---
title: python写的小爬虫
img: https://pub-b24cf0a8c1f14e9386435977aa464959.r2.dev/img/20231201101245.jpg
author: 张一雄
summary: 爬取壁纸网站
categories:
 - 后端
tags:
 - python
---

## python写的小爬虫

```python
import uuid
import requests
from bs4 import BeautifulSoup

def download_image(url, filename):
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        with open(filename, 'wb') as f:
            for chunk in response.iter_content(1024):
                f.write(chunk)
    else:
        print(f"Failed to retrieve image. Status code: {response.status_code}")
for i in range(50):
    url = 'http://www.netbian.com/dongman/index_'+str(i+52)+'.htm'
    response = requests.get(url)

    # 检查请求是否成功

​    if response.status_code == 200:
​        content = response.text
​        soup = BeautifulSoup(content, 'lxml')

        # 解析标题

​        title = soup.title.string
​        paragraphs = soup.find_all('img')
​        for paragraph in paragraphs:
​            src = paragraph['src']
​            if 'small' in src:
​                src = src.replace("small", "")
​                src = src[:49] + src[59:]
​                local_filename = 'D:\pytest\local_image'+str(uuid.uuid4())+'.jpg'  # 替换为你要保存的图片的本地文件名
​                download_image(src, local_filename)
​                print(src)
​    else:
​        print(f"Failed to retrieve the webpage. Status code: {response.status_code}")
```

