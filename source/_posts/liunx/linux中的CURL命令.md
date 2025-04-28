---
title: linux中的CURL命令
author: 张一雄
summary: 我们前端程序员所依赖的开发运行工具！
img: https://gitee.com/xiongood/image/raw/master/linux.jpg
categories:
 - 工具
tags:
 - linux
---

`curl` 是 Linux 系统中一个非常强大且常用的命令行工具，用于通过各种网络协议（如 HTTP、HTTPS、FTP 等）与服务器进行数据传输

### 安装

大多数 Linux 发行版默认已经安装了 `curl`。如果没有安装，可以使用相应的包管理器进行安装：

- Debian/Ubuntu：

```bash
sudo apt-get install curl
```

- CentOS/RHEL：

```bash
sudo yum install curl
```

### 基本语法

```bash
curl [选项] [URL]
```

### 常见使用场景及示例

#### 1. 下载文件

- **将文件下载到当前目录**：

```bash
curl -O https://example.com/file.zip
```

`-O`（大写字母 O）选项表示将远程文件下载到当前目录，并使用远程文件名作为本地文件名。

- **指定本地文件名下载**：

```bash
curl -o new_name.zip https://example.com/file.zip
```

`-o`（小写字母 o）选项允许你指定下载文件的本地文件名。

#### 2. 发送 HTTP 请求

- **发送 GET 请求**：

```bash
curl https://api.example.com/data
```

这会向指定的 URL 发送一个 GET 请求，并将服务器的响应输出到终端。

- **发送 POST 请求**：

```bash
curl -X POST -d "param1=value1&param2=value2" https://api.example.com/submit
```

- `-X POST`：指定请求方法为 POST。
- `-d`：用于传递 POST 请求的数据。

#### 3. 显示详细的请求信息

```bash
curl -v https://example.com
```

`-v` 选项会显示详细的请求和响应信息，包括请求头、响应头以及传输过程中的详细信息，有助于调试。

#### 4. 处理请求头

- **设置自定义请求头**：

```bash
curl -H "Content-Type: application/json" https://api.example.com/json-data
```

`-H` 选项用于设置自定义的请求头。

#### 5. 处理认证

- **基本认证**：

```bash
curl -u username:password https://example.com/protected
```

`-u` 选项用于进行基本认证，需要提供用户名和密码。

#### 6. 跟随重定向

```bash
curl -L https://example.com/redirect
```

`-L` 选项会让 `curl` 跟随服务器返回的重定向响应，直到到达最终的目标页面。

#### 7. 下载进度条

```bash
curl -# https://example.com/large-file.zip
```

`-#` 选项会显示一个简单的下载进度条，让你了解下载的进度。

### 常用选项总结

| 选项 | 描述                            |
| ---- | ------------------------------- |
| `-O` | 下载文件并使用远程文件名        |
| `-o` | 下载文件并指定本地文件名        |
| `-X` | 指定请求方法（如 GET、POST 等） |
| `-d` | 传递 POST 请求的数据            |
| `-v` | 显示详细的请求和响应信息        |
| `-H` | 设置自定义请求头                |
| `-u` | 进行基本认证                    |
| `-L` | 跟随重定向                      |
| `-#` | 显示下载进度条                  |

`curl` 命令还有很多其他的选项和功能，可以通过 `man curl` 命令查看完整的手册。