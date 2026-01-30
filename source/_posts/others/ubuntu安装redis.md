---
title: ubuntu安装redis
---

## 安装

```sh
# 更新apt
sudo apt update && sudo apt upgrade -y
# 安装redis
sudo apt install redis-server -y

# 查看Redis版本
redis-cli --version
# 查看Redis服务运行状态
sudo systemctl status redis-server
```

## 配置

### 修改redis密码

```sh
vim /etc/redis/redis.conf
```

修改的位置：

```sh
requirepass xiong1991
```

### 设置所有ip均可访问

```sh
vim /etc/redis/redis.conf
```

修改的位置：

```sh
bind 0.0.0.0
```

### 设置开机启动

```sh
# 开启开机自启
sudo systemctl enable redis-server
# 验证自启是否生效（输出enabled即为成功）
sudo systemctl is-enabled redis-server
# 若需要关闭自启，执行：sudo systemctl disable redis-server
```

## 控制

```sh
# 重启
sudo systemctl restart redis-server
```

