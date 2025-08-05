---
title: 修改默认python版本
author: 张一雄
summary: 爬取壁纸网站
categories:
 - 后端
tags:
 - python
 - centos7
---

```sh
yum install python3
alternatives --install /usr/bin/python python /usr/bin/python2 1
alternatives --install /usr/bin/python python /usr/bin/python3 2

# 选择版本
alternatives --config python
```

