---
title: ubuntu安装nginx
---

## 安装

### 首先更新系统包列表：

```
sudo apt update
```

### 安装 Nginx：

```
sudo apt install nginx
```

### 安装完成后，Nginx 通常会自动启动。你可以通过以下命令检查其运行状态：

```
sudo systemctl status nginx
```

### 如果 Nginx 没有运行，可以使用以下命令启动它：

```
sudo systemctl start nginx
```

### 若要设置 Nginx 开机自启动：

```
sudo systemctl enable nginx
```

### 验证 Nginx 是否安装成功，可以在浏览器中访问服务器的 IP 地址，你应该能看到 Nginx 的默认欢迎页面。

如果你的服务器启用了防火墙（如 ufw），需要允许 HTTP 和 HTTPS 流量：

```
sudo ufw allow 'Nginx Full'
```

安装完成后，Nginx 的主要配置文件位于/etc/nginx/nginx.conf，网站配置通常放在/etc/nginx/sites-available/目录下。

## 使用

参考博客：nginx的搭建与使用