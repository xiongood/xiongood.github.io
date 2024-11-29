---
title: centos7安装python
img: https://pub-b24cf0a8c1f14e9386435977aa464959.r2.dev/img/python.jpg
author: 张一雄
summary: 爬取壁纸网站
categories:
 - 后端
tags:
 - python
 - centos7
---

## 检查当前系统中的Python环境：

在终端中输入 `python --version` 来查看当前Python的版本。CentOS 7默认安装了Python 2.7，但许多现代项目需要Python 3。

```shell
python --version
```

## 更新系统和软件包：

在开始安装Python 3之前，建议更新你的系统和软件包到最新版本。可以使用以下命令：

```bash
sudo yum update -y
```

## 安装依赖项：

Python 3需要一些依赖项来正常编译和安装。可以使用以下命令安装这些依赖项：

```bash
sudo yum install -y gcc make openssl-devel bzip2-devel libffi-devel zlib-devel
```

## 下载Python 3源码包：

访问Python官方网站，下载你需要的Python 3版本的源码包。你可以下载最新的稳定版本或者特定版本的源码包。下载后，通过SCP或其他方法将源码包传输到CentOS 7服务器上。
\5. **解压并编译源码包**：

在终端中，导航到源码包所在的目录，并使用以下命令解压和编译源码包：

```bash
wget https://www.python.org/ftp/python/3.10.0/Python-3.10.0.tgz
tar -xzvf Python-3.10.0.tgz
cd Python-3.*  
./configure --enable-optimizations  
make -j $(nproc)
```

这里 `--enable-optimizations` 是一个编译选项，用于启用一些性能优化。`make -j $(nproc)` 命令使用多核并行编译，可以加快编译速度。

## 安装Python 3：

使用以下命令安装Python 3：

```bash
sudo make altinstall
```

注意这里使用的是 `altinstall` 而不是 `install`。`altinstall` 会避免覆盖默认的Python二进制文件，允许你同时拥有Python 2和Python 3。

## 验证安装：

安装完成后，你可以通过输入 `python3 --version` 来验证Python 3是否成功安装。如果一切正常，你应该能看到新安装的Python 3的版本号。

```shell
python3 --version
```

安装包的时候

```shell
pip3 install xxx
```

现在你已经成功在CentOS 7上安装了Python 3。你可以使用 `python3` 命令来运行Python 3程序，或者使用 `pip3` 命令来安装Python 3的包。
