---
title: springboot整合redis
img: https://pub-b24cf0a8c1f14e9386435977aa464959.r2.dev/img/20230816091932.png
categories:
 - 后端
tags:
 - redis
 - java
---

## 搭建

### pom

```xml
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-aop</artifactId>
</dependency>
<dependency>
    <groupId>aopalliance</groupId>
    <artifactId>aopalliance</artifactId>
    <version>1.0</version>
</dependency>
<dependency>
    <groupId>org.aspectj</groupId>
    <artifactId>aspectjweaver</artifactId>
    <version>1.8.9</version>
</dependency>
```

### application.yml

```yaml
spring:
  redis:
    # Redis服务器地址
    host: 192.168.43.111
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
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.redis.core.RedisTemplate;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/redis")
public class RedisController {

    @Autowired
    RedisTemplate redisTemplate;

    @GetMapping("test")
    public void testOne() {
        redisTemplate.opsForValue().set("name","xiong");
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

![image-20230425110819062](https://pub-b24cf0a8c1f14e9386435977aa464959.r2.dev/img/20230425110820.png)

### 解决乱码

新增配置类

```java
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.data.redis.connection.RedisConnectionFactory;
import org.springframework.data.redis.core.RedisTemplate;
import org.springframework.data.redis.serializer.GenericJackson2JsonRedisSerializer;
import org.springframework.data.redis.serializer.RedisSerializer;

import java.net.UnknownHostException;

@Configuration
public class RedisConfig {
    @Bean
    public RedisTemplate<String, Object> redisTemplate(RedisConnectionFactory redisConnectionFactory)
            throws UnknownHostException {
        // 创建模板
        RedisTemplate<String, Object> redisTemplate = new RedisTemplate<>();
        // 设置连接工厂
        redisTemplate.setConnectionFactory(redisConnectionFactory);
        // 设置序列化工具
        GenericJackson2JsonRedisSerializer jsonRedisSerializer =
                new GenericJackson2JsonRedisSerializer();
        // key和 hashKey采用 string序列化
        redisTemplate.setKeySerializer(RedisSerializer.string());
        redisTemplate.setHashKeySerializer(RedisSerializer.string());
        // value和 hashValue采用 JSON序列化
        redisTemplate.setValueSerializer(jsonRedisSerializer);
        redisTemplate.setHashValueSerializer(jsonRedisSerializer);
        return redisTemplate;
    }
}

```

### 在测测试

```http
http://localhost:8000/redis/test
```

![image-20230425111112821](https://pub-b24cf0a8c1f14e9386435977aa464959.r2.dev/img/20230425111113.png)

## redis API

### string

- 存自动过期的字符串

  ```java
  // 10 秒过期
  redisTemplate.opsForValue().set("key","value",10,TimeUnit.SECONDS );
  ```

  















