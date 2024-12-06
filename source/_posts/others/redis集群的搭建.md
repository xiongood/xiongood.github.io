---
title: redis集群的搭建
author: 张一雄
summary: 集群的方式又好多种，此文档只列举了其中一种。
img: https://img.myfox.fun/img/redis.jpg
categories:
 - 周边
tags:
 - redis
 - linux
---



## 准备

### 说明

Redis集群至少需要3个节点，因为投票容错机制要求超过半数节点认为某个节点挂了该节点才是挂了，所以2个节点无法构成集群。
要保证集群的高可用，需要每个节点都有从节点，也就是备份节点，所以Redis集群至少需要6台服务器。因为我没有那么多服务器，也启动不了那么多虚拟机，所在这里搭建的是伪分布式集群，即一台服务器虚拟运行6个redis实例，修改端口号为（7001-7006），当然实际生产环境的Redis集群搭建和这里是一样的。

redis安装过程请看当前目录下的过程

### 准备过程

#### 1、创建文件夹保存redis节点

```sh
mkdir redis-cluste
```

#### 2.复制配置文件

```sh
mkdir /usr/local/redis-cluste/redis01

cp -r /usr/local/redis/bin/ /usr/local/redis-cluste/redis01/

cp -r /usr/local/redis/etc/* /usr/local/redis-cluste/redis01/bin/

#删除无用代码
rm -rf dump.rdb
```

**修改后的文件目录**

```sh
nodes.conf
redis-benchmark
redis-check-aof
redis-check-rdb
redis-cli
redis.conf
redis-sentinel -> redis-server
redis-server
```

#### 3、修改端口号

```sh
vim redis.conf 
```

修改为

```sh
port 6379  ->  port 7001

# cluster-enabled yes  ->  cluster-enabled yes	(去掉注释)
```

#### 4、复制节点

复制文件夹redis01为redis01至redis07

逐个修改配置文件的端口号

```sh
cp -r  redis01 redis02
```

启动关闭redis

```sh
在配置文件目录下/usr/local/redis-cluste/redis01/bin

./redis-server redis.conf

redis-cli -p 7001 shutdown
```

#### 5、制作shell文件，快速启动

```shell
#!/bin/bash

cd  /usr/local/redis-cluste/redis01/bin

./redis-server ./redis.conf



cd  /usr/local/redis-cluste/redis02/bin

./redis-server ./redis.conf



cd  /usr/local/redis-cluste/redis03/bin

./redis-server ./redis.conf



cd  /usr/local/redis-cluste/redis04/bin

./redis-server ./redis.conf



cd  /usr/local/redis-cluste/redis05/bin

./redis-server ./redis.conf



cd  /usr/local/redis-cluste/redis06/bin

./redis-server ./redis.conf



cd  /usr/local/redis-cluste/redis07/bin

./redis-server ./redis.conf

```

###### 执行权限

```sh
chmod 777 ./start.sh
```

###### 报错

bash: ./start.sh: /bin/bash　^M: 坏的解释器: 没有那个文件或目录

```shell
sed -i 's/\r$//' start.sh
```

###### 执行后查看端口号

```sh
netstat -lntp

ps aux|grep redis
```

#### 6、制作shell文件，快速关闭

```shell
#!/bin/bash
redis-cli -p 7001 shutdown
redis-cli -p 7002 shutdown
redis-cli -p 7003 shutdown
redis-cli -p 7004 shutdown
redis-cli -p 7005 shutdown
redis-cli -p 7006 shutdown
redis-cli -p 7007 shutdown
```

------



## 搭建

### 说明

至此6个redis节点启动成功（准备七个作为备用），接下来正式开启搭建集群，以上都是准备条件。大家不要觉得图片多看起来冗长所以觉得麻烦，其实以上步骤也就一句话的事情：创建6个redis实例（6个节点）并启动。
要搭建集群的话，需要使用一个工具（脚本文件），这个工具在redis解压文件的源代码里。因为这个工具是一个ruby脚本文件，所以这个工具的运行需要ruby的运行环境，就相当于java语言的运行需要在jvm上。所以需要安装ruby

### 搭建过程

#### 1、安装ruby

```sh
#这种方法版本太低，不推荐
yum install ruby
```

**卸载**

```sh
yum erase ruby ruby-libs ruby-mode ruby-rdoc ruby-irb ruby-ri ruby-docs
```

**下载最新版本的ruby并且解压**

```sh
#正常方法
http://www.ruby-lang.org/zh_cn/documentation/installation/

cd ruby-3.0.1

./configure

make

sudo make install

# 启动位置指向
ln -s /usr/local/bin/ruby /usr/bin/ruby

#查看版本
ruby -v
说明
默认情况下，Ruby 安装到 /usr/local 目录。如果想使用其他目录，可以把 --prefix=DIR 选项传给 ./configure 脚本。
```

重装

```sh
yum groupinstall "Development tools"

yum erase ruby ruby-libs ruby-mode ruby-rdoc ruby-irb ruby-ri ruby-docs

yum -y install zlib-devel curl-devel openssl-devel httpd-devel apr-devel apr-util-devel mysql-devel

重复上述安装
```

#### 2、安装gem

然后需要把ruby相关的包安装到服务器，我这里用的是redis-3.0.0.gem，大家需要注意的是：redis的版本和ruby包的版本最好保持一致。
将Ruby包安装到服务器：需要先下载再安装

网上下载后放入服务器，然后安装

下载地址：https://rubygems.org/gems/redis/versions/4.2.5

##### 安装gem

```sh
gem install redis-4.2.5.gem 
```

**返回**

```sh
Successfully installed redis-4.2.5
Parsing documentation for redis-4.2.5
Installing ri documentation for redis-4.2.5
Done installing documentation for redis after 0 seconds
1 gem installed
```

##### 复制脚本工具

**说明**

上一步中已经把ruby工具所需要的运行环境和ruby包安装好了，接下来需要把这个ruby脚本工具复制到usr/local/redis-cluster目录下。那么这个ruby脚本工具在哪里呢？之前提到过，在redis解压文件的源代码里，即redis/src目录下的redis-trib.rb文件

```sh
cd /usr/local/redis-6.0.8/src

cat redis-trib.rb

cp ./redis-trib.rb /usr/local/redis-cluste/
```

#### 创建集群

执行命令

```sh
./redis-trib.rb create --replicas 1 192.168.116.133:7001 192.168.116.133:7002 192.168.116.133:7003 192.168.116.133:7004 192.168.116.133:7005 192.168.116.133:7006
```

报错

WARNING: redis-trib.rb is not longer available!
You should use redis-cli instead.

原因

原本的命令./redis-trib.rb create --replicas 1 172.16.0.71:9001 172.16.0.71:9002 废弃了，提示改用redis-cli

重新执行

```sh
cd /usr/local/redis-6.0.8/src/

cp ./redis-cli /usr/local/redis-cluste/

./redis-cli create --replicas 1 192.168.116.133:7001 192.168.116.133:7002 192.168.116.133:7003 192.168.116.133:7004 192.168.116.133:7005 192.168.116.133:7006
```

报错

Could not connect to Redis at 127.0.0.1:6379: Connection refused

原因：主服务未打开

```sh
cd /usr/local/redis

./bin/redis-server ./etc/redis.conf 

cd /usr/local/redis-cluste/

#启动
./redis-cli --cluster create --cluster-replicas 1  192.168.116.133:7001 192.168.116.133:7002 192.168.116.133:7003 192.168.116.133:7004 192.168.116.133:7005 192.168.116.133:7006

```

**返回**

>>> Performing hash slots allocation on 6 nodes...
>>> Master[0] -> Slots 0 - 5460
>>> Master[1] -> Slots 5461 - 10922
>>> Master[2] -> Slots 10923 - 16383
>>> Adding replica 192.168.116.133:7005 to 192.168.116.133:7001
>>> Adding replica 192.168.116.133:7006 to 192.168.116.133:7002
>>> Adding replica 192.168.116.133:7004 to 192.168.116.133:7003
>>> Trying to optimize slaves allocation for anti-affinity
>>> [WARNING] Some slaves are in the same host as their master
>>> M: 59d0924bc1755d5565033ce00707adc50e30945e 192.168.116.133:7001
>>> slots:[0-5460] (5461 slots) master
>>> M: 6bd1e3c097f5f6092e42db71807c7199bb6d5444 192.168.116.133:7002
>>> slots:[5461-10922] (5462 slots) master
>>> M: 77989ff4487a1a91ffe8ae77cd9e13450ded7a77 192.168.116.133:7003
>>> slots:[10923-16383] (5461 slots) master
>>> S: 8b6aaa5b64dda8e8edc05800f4cdd835ded8af4e 192.168.116.133:7004
>>> replicates 59d0924bc1755d5565033ce00707adc50e30945e
>>> S: 2230987188ffa0e393bc0f9948e68356c86141a1 192.168.116.133:7005
>>> replicates 6bd1e3c097f5f6092e42db71807c7199bb6d5444
>>> S: 83d8dba574db757b064f352b5561c3558e52493b 192.168.116.133:7006
>>> replicates 77989ff4487a1a91ffe8ae77cd9e13450ded7a77
>>> Can I set the above configuration? (type 'yes' to accept): yes
>>> Nodes configuration updated
>>> Assign a different config epoch to each node
>>> Sending CLUSTER MEET messages to join the cluster
>>> Waiting for the cluster to join

>>> Performing Cluster Check (using node 192.168.116.133:7001)
>>> M: 59d0924bc1755d5565033ce00707adc50e30945e 192.168.116.133:7001
>>> slots:[0-5460] (5461 slots) master
>>> 1 additional replica(s)
>>> M: 77989ff4487a1a91ffe8ae77cd9e13450ded7a77 192.168.116.133:7003
>>> slots:[10923-16383] (5461 slots) master
>>> 1 additional replica(s)
>>> S: 8b6aaa5b64dda8e8edc05800f4cdd835ded8af4e 192.168.116.133:7004
>>> slots: (0 slots) slave
>>> replicates 59d0924bc1755d5565033ce00707adc50e30945e
>>> S: 83d8dba574db757b064f352b5561c3558e52493b 192.168.116.133:7006
>>> slots: (0 slots) slave
>>> replicates 77989ff4487a1a91ffe8ae77cd9e13450ded7a77
>>> S: 2230987188ffa0e393bc0f9948e68356c86141a1 192.168.116.133:7005
>>> slots: (0 slots) slave
>>> replicates 6bd1e3c097f5f6092e42db71807c7199bb6d5444
>>> M: 6bd1e3c097f5f6092e42db71807c7199bb6d5444 192.168.116.133:7002
>>> slots:[5461-10922] (5462 slots) master
>>> 1 additional replica(s)
>>> [OK] All nodes agree about slots configuration.
>>> Check for open slots...
>>> Check slots coverage...
>>> [OK] All 16384 slots covered.

**查看状态**

```sh
redis-cli -c -p 7001 cluster info
```

**测试**

```sh
redis-cli -c -p 7001

127.0.0.1:7001> set username mess1
```

**返回**

```sh
-> Redirected to slot [14315] located at 192.168.116.133:7003
OK
```

## 集群的启动与关闭

### 关闭

```sh
ps -ef | grep redis
kill -9 10252 10257 10262 10267 10272 10294

也可执行以下命令来关闭redis进程

pkill -9 redis
```

### 重启

**保留原来的数据：**
逐个关闭redis实例，再逐个的启动即可。

 

**丢弃原来的数据：**
关闭实例，清空实例中数据存放目录的所有内容，然后逐个启动实例，在任意一个实例上执行集群的创建命令即可,本质上就是创建一个新的集群
清空数据存储目录内容：

**手动管理**

```sh
3、将 ip 和 port 所指定的节点添加到集群中

CLUSTER MEET <ip> <port>

4、从集群中移除 node_id 指定的节点

CLUSTER FORGET <node_id>

5、将当前节点设置为 node_id 指定的节点的从节点

CLUSTER REPLICATE <node_id>

6、将节点的配置文件保存到硬盘里面

CLUSTER SAVECONFIG

7、将一个或多个槽（slot）指派（assign）给当前节点

CLUSTER ADDSLOTS <slot> [slot ...]

8、移除一个或多个槽对当前节点的指派

CLUSTER DELSLOTS <slot> [slot ...]

9、 移除指派给当前节点的所有槽，让当前节点变成一个没有指派任何槽的节点

CLUSTER FLUSHSLOTS

10、将槽 slot 指派给 node_id 指定的节点，如果槽已经指派给另一个节点，那么先让另一个节点删除该槽>，然后再进行指派

CLUSTER SETSLOT <slot> NODE <node_id>

11、将本节点的槽 slot 迁移到 node_id 指定的节点中

CLUSTER SETSLOT <slot> MIGRATING <node_id>

12、从 node_id 指定的节点中导入槽 slot 到本节点

CLUSTER SETSLOT <slot> IMPORTING <node_id>

13、取消对槽 slot 的导入（import）或者迁移（migrate）

CLUSTER SETSLOT <slot> STABLE

14、计算键 key 应该被放置在哪个槽上

CLUSTER KEYSLOT <key>

15、返回槽 slot 目前包含的键值对数量

CLUSTER COUNTKEYSINSLOT <slot>

16、返回 count 个 slot 槽中的键

CLUSTER GETKEYSINSLOT <slot> <count>


```

## springboot链接redis集群

创建一个简单的springboot项目（项目在备份中）

### pom.xml

```xml
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-data-redis</artifactId>
</dependency>
<dependency>
    <groupId>redis.clients</groupId>
    <artifactId>jedis</artifactId>
</dependency>
```

### application.yml

```yaml
spring:
  #application:
    #name: redis-cluster
  redis:
    cluster:
      nodes: 192.168.116.133:7001,192.168.116.133:7002,192.168.116.133:7003,192.168.116.133:7004,192.168.116.133:7005,192.168.116.133:7006
      max-redirects: 12  #重链接的最大数量
redis:
  timeout: 10000 #客户端超时时间单位是毫秒 默认是2000
  maxIdle: 300 #最大空闲数
  maxTotal: 1000 #控制一个pool可分配多少个jedis实例,用来替换上面的redis.maxActive,如果是jedis 2.4以后用该属性
  maxWaitMillis: 1000 #最大建立连接等待时间。如果超过此时间将接到异常。设为-1表示无限制。
  minEvictableIdleTimeMillis: 300000 #连接的最小空闲时间 默认1800000毫秒(30分钟)
  numTestsPerEvictionRun: 1024 #每次释放连接的最大数目,默认3
  timeBetweenEvictionRunsMillis: 30000 #逐出扫描的时间间隔(毫秒) 如果为负数,则不运行逐出线程, 默认-1
  testOnBorrow: true #是否在从池中取出连接前进行检验,如果检验失败,则从池中去除连接并尝试取出另一个
  testWhileIdle: true #在空闲时检查有效性, 默认false
  password: 123456 #密码
server:
  port: 8080
```

### 配置类RedisClusterConfig

```java
package com.example.demo.config;

import java.util.HashSet;
import java.util.Set;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.data.redis.connection.RedisClusterConfiguration;
import org.springframework.data.redis.connection.RedisNode;
import org.springframework.data.redis.connection.RedisPassword;
import org.springframework.data.redis.connection.jedis.JedisConnectionFactory;
import org.springframework.data.redis.core.RedisTemplate;
import org.springframework.data.redis.serializer.Jackson2JsonRedisSerializer;
import org.springframework.data.redis.serializer.StringRedisSerializer;

import com.fasterxml.jackson.annotation.JsonAutoDetect;
import com.fasterxml.jackson.annotation.PropertyAccessor;
import com.fasterxml.jackson.databind.ObjectMapper;
import redis.clients.jedis.JedisPoolConfig;


@Configuration
public class RedisClusterConfig {

    @Value("${spring.redis.cluster.nodes}")
    private String clusterNodes;
    @Value("${spring.redis.cluster.max-redirects}")
    private int maxRedirects;
    @Value("${redis.password}")
    private String password;
    @Value("${redis.timeout}")
    private int timeout;
    @Value("${redis.maxIdle}")
    private int maxIdle;
    @Value("${redis.maxTotal}")
    private int maxTotal;
    @Value("${redis.maxWaitMillis}")
    private int maxWaitMillis;
    @Value("${redis.minEvictableIdleTimeMillis}")
    private int minEvictableIdleTimeMillis;
    @Value("${redis.numTestsPerEvictionRun}")
    private int numTestsPerEvictionRun;
    @Value("${redis.timeBetweenEvictionRunsMillis}")
    private int timeBetweenEvictionRunsMillis;
    @Value("${redis.testOnBorrow}")
    private boolean testOnBorrow;
    @Value("${redis.testWhileIdle}")
    private boolean testWhileIdle;

    /**
     * Redis连接池的配置
     *
     * @return JedisPoolConfig
     */
    @Bean
    public JedisPoolConfig getJedisPoolConfig() {
        JedisPoolConfig jedisPoolConfig = new JedisPoolConfig();
        // 最大空闲数
        jedisPoolConfig.setMaxIdle(maxIdle);
        // 连接池的最大数据库连接数
        jedisPoolConfig.setMaxTotal(maxTotal);
        // 最大建立连接等待时间
        jedisPoolConfig.setMaxWaitMillis(maxWaitMillis);
        // 逐出连接的最小空闲时间 默认1800000毫秒(30分钟)
        jedisPoolConfig.setMinEvictableIdleTimeMillis(minEvictableIdleTimeMillis);
        // 每次逐出检查时 逐出的最大数目 如果为负数就是 : 1/abs(n), 默认3
        jedisPoolConfig.setNumTestsPerEvictionRun(numTestsPerEvictionRun);
        // 逐出扫描的时间间隔(毫秒) 如果为负数,则不运行逐出线程, 默认-1
        jedisPoolConfig.setTimeBetweenEvictionRunsMillis(timeBetweenEvictionRunsMillis);
        // 是否在从池中取出连接前进行检验,如果检验失败,则从池中去除连接并尝试取出另一个
        jedisPoolConfig.setTestOnBorrow(testOnBorrow);
        // 在空闲时检查有效性, 默认false
        jedisPoolConfig.setTestWhileIdle(testWhileIdle);
        return jedisPoolConfig;
    }

    /**
     * Redis集群的配置
     *
     * @return RedisClusterConfiguration
     */
    @Bean
    public RedisClusterConfiguration redisClusterConfiguration() {
        RedisClusterConfiguration redisClusterConfiguration = new RedisClusterConfiguration();
        // Set<RedisNode> clusterNodes
        String[] serverArray = clusterNodes.split(",");
        Set<RedisNode> nodes = new HashSet<RedisNode>();
        for (String ipPort : serverArray) {
            String[] ipAndPort = ipPort.split(":");
            nodes.add(new RedisNode(ipAndPort[0].trim(), Integer.valueOf(ipAndPort[1])));
        }
        redisClusterConfiguration.setClusterNodes(nodes);
        redisClusterConfiguration.setMaxRedirects(maxRedirects);
        redisClusterConfiguration.setPassword(RedisPassword.of(password));
        return redisClusterConfiguration;
    }

    /**
     * redis连接工厂类
     *
     * @return JedisConnectionFactory
     */
    @Bean
    public JedisConnectionFactory jedisConnectionFactory() {
        // 集群模式
        JedisConnectionFactory factory = new JedisConnectionFactory(redisClusterConfiguration(), getJedisPoolConfig());
        return factory;
    }

    /**
     * 实例化 RedisTemplate 对象
     *
     * @return RedisTemplate<String, Object>
     */
    @Bean
    public RedisTemplate<String, Object> redisTemplate() {
        RedisTemplate<String, Object> redisTemplate = new RedisTemplate<>();
        // Template初始化
        initDomainRedisTemplate(redisTemplate);
        return redisTemplate;
    }

    /**
     * 设置数据存入 redis 的序列化方式 使用默认的序列化会导致key乱码
     */
    private void initDomainRedisTemplate(RedisTemplate<String, Object> redisTemplate) {
        // 开启redis数据库事务的支持
        redisTemplate.setEnableTransactionSupport(true);
        redisTemplate.setConnectionFactory(jedisConnectionFactory());

        // 如果不配置Serializer，那么存储的时候缺省使用String，如果用User类型存储，那么会提示错误User can't cast to
        // String！
        StringRedisSerializer stringRedisSerializer = new StringRedisSerializer();
        redisTemplate.setKeySerializer(stringRedisSerializer);
        // hash的key也采用String的序列化方式
        redisTemplate.setHashKeySerializer(stringRedisSerializer);

        // jackson序列化对象设置
        Jackson2JsonRedisSerializer<Object> jackson2JsonRedisSerializer = new Jackson2JsonRedisSerializer<>(
                Object.class);
        ObjectMapper om = new ObjectMapper();
        om.setVisibility(PropertyAccessor.ALL, JsonAutoDetect.Visibility.ANY);
        om.enableDefaultTyping(ObjectMapper.DefaultTyping.NON_FINAL);
        jackson2JsonRedisSerializer.setObjectMapper(om);

        // value序列化方式采用jackson
        redisTemplate.setValueSerializer(jackson2JsonRedisSerializer);
        // hash的value序列化方式采用jackson
        redisTemplate.setHashValueSerializer(jackson2JsonRedisSerializer);

        redisTemplate.afterPropertiesSet();
    }
}
```

### 测试类controller

```java
package com.example.demo.controller;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.redis.core.RedisTemplate;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.Date;

/**
 * @author ：zhangYiXiong
 * @date ：Created in 2021/6/2 15:11
 * @description：
 * @version: 1.0
 */
@RestController
public class TestController {

    @Autowired
    private RedisTemplate<String, Object> template;

    @RequestMapping("/test")
    public String test() {
        String k = "springboot"+new Date().getTime();
        template.opsForValue().set(k, "hello world! 你好，世界"+k);
        String str = (String) template.opsForValue().get(k);
        return str;
    }

}
```

# redission

## springboot整合redission

- pom

  ```xml
    <!--整合redission框架start-->
  <dependency>
      <groupId>org.springframework.boot</groupId>
      <artifactId>spring-boot-starter-data-redis</artifactId>
  </dependency>
  <dependency>
      <groupId>org.redisson</groupId>
      <artifactId>redisson-spring-boot-starter</artifactId>
      <version>3.12.5</version>
  </dependency>
  <!--整合redission框架enc-->
  <dependency>
      <groupId>org.apache.commons</groupId>
      <artifactId>commons-lang3</artifactId>
  </dependency>
  ```

- yml配置

  ```yml
  spring:
    #redisson配置,默认连接库0,无密码只配置连接地址即可
    redis:
      host: 127.0.0.1
      database: 0
      password:
  ```

## 使用

- 限流器的使用

  ```java
  package com.cyc.redission.n1;
  
  import org.redisson.api.RRateLimiter;
  import org.redisson.api.RateIntervalUnit;
  import org.redisson.api.RateType;
  import org.redisson.api.RedissonClient;
  import org.springframework.beans.factory.annotation.Autowired;
  import org.springframework.web.bind.annotation.RequestMapping;
  import org.springframework.web.bind.annotation.RestController;
  
  /*
   * 限流器
   * 1.先调用init方法生成5个令牌
   * 2.通过该限流器的名称rateLimiter来获取令牌limiter.tryAcquire()
   * 3.谁抢到,谁先执行,否则返回提示信息,可以用于秒杀场景
   * */
  @RestController
  @RequestMapping("/limiter")
  public class RateLimiterTest {
  
      @Autowired
      private RedissonClient redissonClient;
  
      //初始化限流器
      @RequestMapping("/init")
      public void init() {
          RRateLimiter limiter = redissonClient.getRateLimiter("rateLimiter");
          limiter.trySetRate(RateType.PER_CLIENT, 5, 1, RateIntervalUnit.SECONDS);//每1秒产生5个令牌
      }
  
      //获取令牌
      @RequestMapping("/thread")
      public void thread() {
          RRateLimiter limiter = redissonClient.getRateLimiter("rateLimiter");
          if (limiter.tryAcquire()) {//尝试获取1个令牌
              System.out.println(Thread.currentThread().getName() + "成功获取到令牌");
          } else {
              System.out.println(Thread.currentThread().getName() + "未获取到令牌");
          }
      }
  }
  
  ```

  





