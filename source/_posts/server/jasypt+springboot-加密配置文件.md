---
title: jasypt-加密配置文件
author: 张一雄
summary: 加密配置文件，有些公司有这种特殊的需要，防止隐私数据的泄露，简单的配置就能实现程序的自动解密。
img: https://gitee.com/xiongood/image/raw/master/springboot.jpg
categories:
 - 工具
tags:
 - java
 - springboot
 - jasypt
---

## 说明

一般情况下，我们会把数据库或者其他服务的账户密码写在配置文件中，方便后期的维护，可是如果我们用明文写这些敏感信息的话，就会带来一定的信息泄露的风险。

jasypt 则是一个对配置文件进行加密的开源工具，在读取配置文件时，自动对密文进行解密，无需手动编写解密代码

## 牛刀小试

### 新增pom依赖

```xml
<dependency>
    <groupId>com.github.ulisesbocchio</groupId>
    <artifactId>jasypt-spring-boot-starter</artifactId>
    <version>3.0.5</version>
</dependency>
```

### 测试加密解密方法
```java
 public static void main(String[] args) {
        BasicTextEncryptor textEncryptor = new BasicTextEncryptor();
        textEncryptor.setPassword("salt");
        //要加密的数据（数据库的用户名或密码）
        //encrypt是加密方法，decrypt是解密方法
        String password = textEncryptor.encrypt("sa_token");
        System.out.println("password:"+password);
        System.out.println(textEncryptor.decrypt(password));
    }
```

## 整合springboot

### 修改启动类

主要目的时新增密钥的配置，该方法可以卸载配置类中
```java
import org.jasypt.encryption.StringEncryptor;
import org.jasypt.encryption.pbe.PooledPBEStringEncryptor;
import org.jasypt.encryption.pbe.config.SimpleStringPBEConfig;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.context.annotation.Bean;
import org.springframework.core.env.Environment;

@SpringBootApplication
public class CleanApplication {

    public static void main(String[] args) {
        Environment env = new SpringApplication(CleanApplication.class).run(args).getEnvironment();
        System.out.println("启动成功: http://localhost:"+ env.getProperty("server.port") );
    }

    // 新增此方法
    @Bean("jasyptStringEncryptor")
    public StringEncryptor stringEncryptor() {
        PooledPBEStringEncryptor encryptor = new PooledPBEStringEncryptor();
        SimpleStringPBEConfig config = new SimpleStringPBEConfig();
        config.setPassword("salt");
        config.setPoolSize("1");
        encryptor.setConfig(config);
        return encryptor;
    }
}
```

### 配置文件
加密的配置文件可以直接使用，密文用ENC()包裹
```yaml
server:
  port: 8080

logging:
  config: classpath:logback.xml

spring:
  datasource:
    url: jdbc:mysql://localhost:3306/sa_token?serverTimezone=UTC&useUnicode=true&characterEncoding=utf-8&AllowPublicKeyRetrieval=True
    username: ENC(auxEZuqUeoCKkYwe2E0N83iAlEBt77g3)
    password: ENC(dmNYRQiesto9yxgg+IBnLaXfChFdFtSp0JCsfmsN1uI=)

mybatis-plus:
  mapper-locations: mapper/*.xml
  configuration:
    log-impl: org.apache.ibatis.logging.stdout.StdOutImpl
    #log-impl: com.example.xiong.conf.StdOutImpl
  type-aliases-package: com.xiong.demo.entity

## 可以在这里写密钥，不过把密钥写在配置文件中，相当于钥匙和锁放在了一起
## 一般都是将密钥写死在代码中
#jasypt:
#  encryptor:
#    password: salt
```

