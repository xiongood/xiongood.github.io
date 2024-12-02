---
title: python更换镜像源
author: 张一雄
summary: python更换镜像源
img: https://pub-b24cf0a8c1f14e9386435977aa464959.r2.dev/img/python.jpg
categories:
 - 周边
tags:
 - python
---

##  更换镜像源

pip默认会从Python官方包索引（PyPI）下载包，但由于网络原因，国内访问国外网站可能会很慢。因此，更换为国内镜像源可以显著加速下载速度。常用的国内镜像源包括：

- 清华大学：`https://pypi.tuna.tsinghua.edu.cn/simple/`
- 阿里云：`https://mirrors.aliyun.com/pypi/simple/`
- 豆瓣：`https://pypi.douban.com/simple/`

永久更改pip镜像源：

- Windows：
  - 在文件管理器中，输入`%APPDATA%`并回车，进入`C:\Users\电脑用户\AppData\Roaming`文件夹。
  - 新建`pip`文件夹，并在该文件夹中新建`pip.ini`配置文件。
  - 在`pip.ini`文件中添加以下内容：
  - ```Plaintext
    [global]  
    index-url = https://mirrors.aliyun.com/pypi/simple/
    ```

## 清空所有下载的包

### windows

```sh
pip freeze | ForEach-Object { pip uninstall -y $_.Split('=')[0] }
```



