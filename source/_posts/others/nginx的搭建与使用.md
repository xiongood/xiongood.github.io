---
title: nginx的搭建与使用
author: 张一雄
summary: 程序员必会中间件之一，其强大程度难以想象！
img: https://pub-b24cf0a8c1f14e9386435977aa464959.r2.dev/img/20230816091827.png
categories:
 - 周边
tags:
 - nginx
 - linux
---

## 环境准备

1.先安装gcc-c++编译器

```sh
yum install gcc-c++
yum install -y openssl openssl-devel
```

2.再安装pcre包

```sh
yum install -y pcre pcre-devel
```

3.再安装zlib包

```sh
yum install -y zlib zlib-devel
```

## 安装nginx

1.在/usr/local/下创建文件nginx文件

```sh
mkdir -p /usr/local/nginx
```

2.在网上下nginx包上传至Linux（https://nginx.org/download/），也可以直接下载

```sh
wget https://nginx.org/download/nginx-1.19.9.tar.gz
```

3.解压并进入nginx目录

```sh
tar -zxvf nginx-1.19.9.tar.gz
cd nginx-1.19.9
```

4.使用nginx默认配置

```sh
# m默认
./configure		#与以下二选一

# 如果使用stream标签进行ssh跳转，需要加这个参数
./configure --with-stream
```

5.编译安装

```sh
make
make install
```

6.查找安装路径

```sh
whereis nginx
```

7.进入sbin目录，可以看到有一个可执行文件nginx，直接**./nginx**执行就OK了。

```sh
cd sbin
./nginx
```

9.查看是否启动成功

```sh
ps -ef | grep nginx
```

## 常用命令

### windows

```shell
# 启动
start nginx

# 配置文件nginx.conf修改重装载命令
nginx -s reload 

# 停止
nginx -s stop
nginx -s quit
# 强力停止
taskkill /f /im nginx.exe
```

### linux

```sh
cd /usr/local/nginx/sbin/

# 重新加载配置
./nginx -s reload

#启动
nginx 

# 停止
./nginx -s quit 	#:此方式停止步骤是待nginx进程处理任务完毕进行停止。
./nginx -s stop 	#:此方式相当于先查出nginx进程id再使用kill命令强制杀掉进程。
```

## 常用配置

### 配置ssh跳转

#### 配置mysql跳转

- 正常

```sh
# 在配置文件最下方新增以下内容，位置与http{}平级
# 输入本机的ip3306+用户名和密码 可以访问192.168.220.137:3306的数据库
stream {
    upstream cloudsocket1 {
    hash $remote_addr consistent;
    # $binary_remote_addr;
    server mysql.sqlpub.com:3306 weight=5 max_fails=3 fail_timeout=30s;	#跳转到的服务器
    }
    server {
    listen 13306;#数据库服务器监听端口
    proxy_connect_timeout 10s;
    proxy_timeout 300s;#设置客户端和代理服务之间的超时时间，如果5分钟内没操作将自动断开。
    proxy_pass cloudsocket1;
    }
}
```

- 报错 找不到stream

```sh
# 安装nginx源
curl -o /etc/yum.repos.d/epel.repo http://mirrors.aliyun.com/repo/epel-7.repo
# 先安装
yum -y install epel-release

#应该是缺少modules模块
yum -y install nginx-all-modules.noarch
然后在用nginx -t就好了
[root@k8s-node2 ~]# nginx -t
nginx: the configuration file /etc/nginx/nginx.conf syntax is ok
nginx: configuration file /etc/nginx/nginx.conf test is successful
```



#### 配置ssh跳转

```sh
# 在配置文件最下方新增以下内容，位置与http{}平级
# 数据本机的ip+122 来登录ssh，可以访问到192.168.1.101:22的服务器，可以用来操作服务器或者传输文件等
stream {
    upstream cloudsocket2 {
    hash $remote_addr consistent;
    # $binary_remote_addr;
    server 192.168.1.101:22 weight=5 max_fails=3 fail_timeout=30s;	#跳转到的服务器
    }
    server {
    listen 122;#连接服务器ssh监听端口
    proxy_connect_timeout 10s;
    proxy_timeout 300s;#设置客户端和代理服务之间的超时时间，如果5分钟内没操作将自动断开。
    proxy_pass cloudsocket2;
    }

}
```

### 配置http跳转

#### 配置负载均衡

```sh
http {
    include       mime.types;
    default_type  application/octet-stream;
    sendfile        on;
    keepalive_timeout  65;

	#健康监测 如果某台服务器down掉，则在周期内部在跳转到该服务器上，当服务重启后，再次恢复其访问
	upstream yuanlai {
	#max_fails 检查1次触发，fail_timeout触发周期为60秒
    	server 192.168.1.100:7009 max_fails=1 fail_timeout=60; 	#指向的地址
		server 192.168.1.105:7009 max_fails=1 fail_timeout=60;	#指向的地址
	}
	server{
		listen 7010;	#监听的端口
		server_name localhost;	#监听的本地地址

		location / {
			#访问上面定义的名称
			proxy_pass http://yuanlai;
			#设置页面响应超时时间3秒
			proxy_read_timeout 3;
			proxy_send_timeout 3;
			proxy_connect_timeout 3;
		}
	}
}

```

#### 转发说明

- proxy_pass

  假设请求：

  ```http
  http://localhost/online/wxapi/test/loginSwitch
  ```

- proxy_pass结尾有/

  ```conf
  location /online/wxapi/ {
          proxy_pass http://localhost:8080/;
          proxy_set_header X-Real-IP $remote_addr;
  }
  ```

  代理后的实际地址：

  ```http
  http://localhost:8080/test/loginSwitch
  ```

  - proxy_pass结尾没有/

  ```conf
  location /online/wxapi/ {
          proxy_pass http://localhost:8080;
          proxy_set_header X-Real-IP $remote_addr;
  }
  ```

  代理后的实际地址：

  ```http
  http://localhost:8080/test/loginSwitch
  ```

  

  - proxy_pass结尾有/web

  ```conf
  location /online/wxapi/ {
          proxy_pass http://localhost:8080/web;
          proxy_set_header X-Real-IP $remote_addr;
  }
  ```

  代理后的实际地址：

  ```http
  http://localhost:8080/webtest/loginSwitch
  ```

  

  - proxy_pass结尾有/web/

  ```conf
  location /online/wxapi/ {
          proxy_pass http://localhost:8080/web/;
          proxy_set_header X-Real-IP $remote_addr;
  }
  ```

  代理后的实际地址：

  ```http
  http://localhost:8080/test/loginSwitch
  ```

  

  proxy_pass结尾有/

  ```conf
  location /online/wxapi/ {
          proxy_pass http://localhost:8080/;
          proxy_set_header X-Real-IP $remote_addr;
  }
  ```

  代理后的实际地址：

  ```http
  http://localhost:8080/web/test/loginSwitch
  ```

  

### 指向本地文件

```sh
worker_processes  1;

events {
    worker_connections  1024;
}

http {
    include       mime.types;
    default_type  application/octet-stream;
    sendfile        on;
    keepalive_timeout  65;

    server {
        listen       9999;
        server_name  localhost;
        
        location / {
        	# 自动构建索引
			autoindex on;
             root  D:\server;
        }
        error_page   500 502 503 504  /50x.html;
        location = /50x.html {
            root   html;
        }
    }
}

```

### 部署vue项目

#### 修改nginx.conf

添加一个server

```conf
server {
    listen       8099;                       #监听端口设置，也就是你vue项目的端口
    server_name  localhost;       
    location / {
      root   /root/project/opmApp/vue/dist;       #前端dist文件夹存放路径
      try_files $uri $uri/ /index.html;           #解决页面刷新报404错误
    }
    
    # 将项目放入nginx目录下
    #location / {
    #       root   html;
	#		try_files $uri $uri/ /index.html;
    #        index  index.html index.htm;
    #}

    error_page 404 /404.html;
        location = /40x.html {
    }
    error_page 500 502 503 504 /50x.html;
        location = /50x.html {
    }
}
```

#### 重启nginx

```
/usr/local/nginx/sbin/nginx -s reload
```

### location配置说明

```sh
= 严格匹配。如果这个查询匹配，那么将停止搜索并立即处理此请求。

~ 为区分大小写匹配(可用正则表达式)

!~为区分大小写不匹配

~* 为不区分大小写匹配(可用正则表达式)

!~*为不区分大小写不匹配

^~ 如果把这个前缀用于一个常规字符串,那么告诉nginx 如果路径匹配那么不测试正则表达式。


location = / {
# 只匹配 / 查询。
}

location / {
# 匹配任何查询，因为所有请求都已 / 开头。但是正则表达式规则和长的块规则将被优先和查询匹配。

}

location ^~ /p_w_picpaths/ {
# 匹配任何已 /p_w_picpaths/ 开头的任何查询并且停止搜索。任何正则表达式将不会被测试。

}

location ~*.(gif|jpg|jpeg)$ {
# 匹配任何已 gif、jpg 或 jpeg 结尾的请求。

}

location ~*.(gif|jpg|swf)$ {
    valid_referers none blocked start.igrow.cn sta.igrow.cn;

    if ($invalid_referer) {
    #防盗链

    	rewrite ^/ http://$host/logo.png;

    }

}
```







