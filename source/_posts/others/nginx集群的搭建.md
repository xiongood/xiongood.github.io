---
title: nginx集群的搭建
author: 张一雄
summary: nginx的集群搭建，平时用不到这功能，仅供学习测试使用！
categories:
 - 周边
tags:
 - nginx
 - linux

---

## 准备

两台服务器都装nginx和keepalived

## 安装keepalived

keepalived 用来配置 虚拟ip

```sh
# 安装
yum install keepalived -y
# 查看是否安装完毕
rpm -q -q keepalived
```

## 配置keepalived

做nginx高可用主要是修改这个配置文件，nginx中的配置文件不需要修改

```sh
cd /etc/keepalived
vim keepalived.conf
```

### 修改主节点配置

```conf
global_defs {
 notification_email {
 acassen@firewall.loc
 failover@firewall.loc
 sysadmin@firewall.loc
 }
 notification_email_from Alexandre.Cassen@firewall.loc
 smtp_server 192.168.130.155
 smtp_connect_timeout 30
 router_id LVS_DEVEL
 script_user root
 enable_script_security 
}
vrrp_script chk_http_port {
	#脚本要放到这个位置
 script "/usr/local/src/nginx_check.sh"
 interval 2 #（检测脚本执行的间隔）
 weight 2
}
vrrp_instance VI_1 {
 state MASTER # 备份服务器上将 MASTER 改为 BACKUP
 interface ens33 //网卡
 virtual_router_id 51 # 主、备机的 virtual_router_id 必须相同
 priority 100 # 主、备机取不同的优先级，主机值较大，备份机值较小
 advert_int 1
 authentication {
 auth_type PASS
 auth_pass 1111
 }
 virtual_ipaddress {
 192.168.130.1 // VRRP H 虚拟地址
 }
}

```

### 修改从节点配置

```conf
global_defs {
 notification_email {
 acassen@firewall.loc
 failover@firewall.loc
 sysadmin@firewall.loc
 }
 notification_email_from Alexandre.Cassen@firewall.loc
 smtp_server 192.168.130.122
 smtp_connect_timeout 30
 router_id LVS_DEVEL
 script_user root
 enable_script_security 
}
vrrp_script chk_http_port {
	#脚本要放到这个位置
 script "/usr/local/src/nginx_check.sh"
 interval 2 #（检测脚本执行的间隔）
 weight 2
}
vrrp_instance VI_1 {
 state BACKUP # 备份服务器上将 MASTER 改为 BACKUP
 interface ens33 //网卡
 virtual_router_id 51 # 主、备机的 virtual_router_id 必须相同
 priority 90 # 主、备机取不同的优先级，主机值较大，备份机值较小
 advert_int 1
 authentication {
 auth_type PASS
 auth_pass 1111
 }
 virtual_ipaddress {
 192.168.130.1 // VRRP H 虚拟地址
 }
 
}

```

### 添加脚本

```sh
vim /usr/local/src/nginx_check.sh
```

```sh
#!/bin/bash
A=`ps -C nginx –no-header |wc -l`
if [ $A -eq 0 ];then
	# nginx的启动脚本的位置
 /usr/local/nginx/sbin/nginx
 sleep 2
 if [ `ps -C nginx --no-header |wc -l` -eq 0 ];then
 killall keepalived
 fi
fi
```

## 启动

启动两台服务器上的nginx和keepalive

### 启动nginx和keepalive

```sh
#启动nginx
/usr/local/nginx/sbin/nginx

#启动keepalived
systemctl start keepalived.service
#查看日志
tail -f /var/log/messages

#查看是否启动
ps -ef  | grep keepalived
```

## 测试

```http
# 访问
http://192.168.130.1/
```

关闭主节点的nginx和keepaliced后仍然可以访问













