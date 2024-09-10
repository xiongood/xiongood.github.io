安装

```sh
# 下载
sudo yum install memcached libmemcached -y
# 配置
vim /etc/sysconfig/memcached
```

默认的例子

```sh
PORT="11211"
USER="memcached"
MAXCONN="1024"
CACHESIZE="64"
OPTIONS=""
```

常用命令

```sh
# 启动
sudo systemctl start memcached
# 开机自己启动
sudo systemctl enable memcached
# 查看状态
sudo systemctl status memcached
# 停止
sudo systemctl stop memcached

```

