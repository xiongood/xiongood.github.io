---
title: windows安装redis
---



## 安装

### 下载地址

```http
https://github.com/tporadowski/redis/releases
```

解压略

## 启动

```
redis-server.exe redis.windows.conf
```



## 设置成服务

### 设置环境变量

![image-20251027124704750](http://img.myfox.fun/img/image-20251027124704750.png)

### 设置成服务

进入redis文件夹执行如下

```cmd
redis-server --service-install redis.windows.conf --loglevel verbose
```

![image-20251027124625168](http://img.myfox.fun/img/image-20251027124625168.png)
