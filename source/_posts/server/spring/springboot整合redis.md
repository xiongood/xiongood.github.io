---
title: springboot整合redis
categories:
 - 后端
tags:
 - redis
 - java
---

## 搭建

### pom

```xml
<!-- SpringBoot Web模块 -->
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-web</artifactId>
</dependency>


<dependency>
    <groupId>org.projectlombok</groupId>
    <artifactId>lombok</artifactId>
    <scope>annotationProcessor</scope>
</dependency>

<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-data-redis</artifactId>
</dependency>

<dependency>
    <groupId>org.apache.commons</groupId>
    <artifactId>commons-pool2</artifactId>
    <version>2.11.1</version> <!-- 请根据需要选择合适的版本号 -->
</dependency>

```

### application.yml

```yaml
server:
    # 端口号 
    port: 8080
spring:
    redis:
        # Redis服务器地址
        host: 192.168.159.128
        # Redis服务器端口号
        port: 6379
        # 使用的数据库索引，默认是0
        database: 0
        # 连接超时时间
        timeout: 1800000
        # 设置密码
        password: "123456"
        lettuce:
            pool:
                # 最大阻塞等待时间，负数表示没有限制
                max-wait: -1
                # 连接池中的最大空闲连接
                max-idle: 5
                # 连接池中的最小空闲连接
                min-idle: 0
                # 连接池中最大连接数，负数表示没有限制
                max-active: 20
```

### controller

```java
package com.pj.controller;


import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.redis.core.RedisTemplate;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/test")
public class TestController {

    @Autowired
    RedisTemplate redisTemplate;

    @GetMapping("/test")
    public void testOne() {
        redisTemplate.opsForValue().set("name","张一雄");
        String name = (String) redisTemplate.opsForValue().get("name");
        System.out.println(name);
    }

}

```

## 测试

```http
http://localhost:8000/redis/test
```

### 发现乱码

![image-20230425110819062](https://img.myfox.fun/img/20230425110820.png)

### 解决乱码

新增配置类

```java
package com.pj.config;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.data.redis.connection.RedisConnectionFactory;
import org.springframework.data.redis.core.RedisTemplate;
import org.springframework.data.redis.serializer.JdkSerializationRedisSerializer;
import org.springframework.data.redis.serializer.StringRedisSerializer;


@Configuration
public class RedisConfig {

    @Bean
    public RedisTemplate<String, Object> redisTemplate(RedisConnectionFactory connectionFactory) {
        RedisTemplate<String, Object> redisTemplate = new RedisTemplate<>();
        redisTemplate.setConnectionFactory(connectionFactory);
        // 设置key和value的序列化方式
        redisTemplate.setKeySerializer(new StringRedisSerializer()); // 设置key的序列化器为StringRedisSerializer
        redisTemplate.setValueSerializer(new JdkSerializationRedisSerializer()); // 设置value的序列化器为JdkSerializationRedisSerializer
        redisTemplate.setHashKeySerializer(new StringRedisSerializer()); // 设置hash key的序列化器为StringRedisSerializer
        redisTemplate.setHashValueSerializer(new JdkSerializationRedisSerializer()); // 设置hash value的序列化器为JdkSerializationRedisSerializer
        redisTemplate.afterPropertiesSet(); // 初始化RedisTemplate
        return redisTemplate; // 返回配置好的RedisTemplate
    }
}
```

### 在测测试

```http
http://localhost:8000/redis/test
```

![image-20230425111112821](https://img.myfox.fun/img/20230425111113.png)

## redis API

### string

- 存自动过期的字符串

  ```java
  // 10 秒过期
  redisTemplate.opsForValue().set("key","value",10,TimeUnit.SECONDS );
  ```

  















