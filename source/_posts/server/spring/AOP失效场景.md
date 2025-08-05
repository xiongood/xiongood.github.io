---
title: AOP失效场景
categories:
 - 后端
tags:
 - AOP
 - java
---



## AOP中的坑

### 失效原理

springAop中的坑是真的多，坑主要出现在其失效的场景中。

如果要谈aop的失效的场景，首先应该聊的是其底层原理。

aop主要是通过继承父类，加强其子类的方式来实现对原方法的加强。

而正是这个机制让aop产生了许多的失效的场景。

### 失效场景

首先我们只要知道什么样的方法不能被子类重写，也就知道了aop失效的一部分情况：

比如 final 修饰的、static 修饰的 、private 修饰的和构造方法

- 不能被重写的其他方式：

访问修饰符的限制一定要大于等于被重写方法的访问修饰符；
重写方法一定不能抛出新的检查异常或者比被重写方法申明更加宽泛的检查型异常，譬如父类方法声明了一个检查异常 IOException，在重写这个方法时就不能抛出 Exception，只能抛出 IOException 的子类异常，可以抛出非检查异常。


已上的不能被重写的方法，对于aop来说都是会失效的。

- 调用与被调用的方法在同一个类中

显而易见，如果当前在一个类中有两个方法A、B，其中B被aop加强了，然后A调用B，此时A调用的是当前类中的方法，而不是其子类加强后的方法，所以会失效

- 引用公共模块时，如果包路径不相同则会失效。

因为spring boot中会默认扫面包路径下的类来加入到ioc的容器中，如果公共类的中的包路径和引用模块的路径不相同，导致公共模块下的对象不能被ioc管理，导致aop失效（下附解决方法）

- 其他

以上为我遇到的一些坑，如果有其他的我会继续补充

## aop 的使用例子

### 加强日志

- 需求说明

加强某写方法。计算方法执行时间，并用日志进行打印

- pom

```xml
<dependency>
    <groupId>cn.hutool</groupId>
    <artifactId>hutool-all</artifactId>
    <version>5.8.0.M2</version>
</dependency>

<dependency>
    <groupId>org.projectlombok</groupId>
    <artifactId>lombok</artifactId>
    <version>1.18.22</version>
</dependency>

<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-aop</artifactId>
</dependency>
```

- 自定义注解

```java
package com.xiong.uplog;

import java.lang.annotation.ElementType;
import java.lang.annotation.Retention;
import java.lang.annotation.RetentionPolicy;
import java.lang.annotation.Target;

// 作用到方法上
@Target({ElementType.METHOD})
// 运行时有效
@Retention(RetentionPolicy.RUNTIME)
public @interface UpLog {

    String value() default "" ;

}
```

- 注解实现

```java
package com.xiong.uplog;

import cn.hutool.core.date.DateUnit;
import cn.hutool.core.date.DateUtil;
import cn.hutool.core.util.StrUtil;
import lombok.extern.slf4j.Slf4j;
import org.aspectj.lang.ProceedingJoinPoint;
import org.aspectj.lang.annotation.Around;
import org.aspectj.lang.annotation.Aspect;
import org.springframework.stereotype.Component;

import java.util.Date;

@Aspect
@Component
@Slf4j
public class UpLogFun {

    @Around("@annotation(upLog)")
    public Object around(ProceedingJoinPoint point, UpLog upLog) throws Throwable {
            String name  = upLog.value();
            if (StrUtil.isEmpty(name)){
                name = point.getSignature().getName();
            }
            log.info(name+"方法执行开始-----");
            Date startTime = new Date();
            Object o = point.proceed();
    log.info(name+"方法执行结束，总耗时：【"+(DateUtil.between(startTime, new Date(), DateUnit.SECOND))+"】秒-----");
            return o;
    }
}
```

- 测试

```java
package com.xiong.testController;

import com.xiong.uplog.UpLog;
import lombok.extern.slf4j.Slf4j;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@Slf4j
public class TestController {

    @GetMapping("/getAbc")
    @UpLog("ASdfas")
    public String getAbc() throws InterruptedException {
        log.info("方法执行。。。。。");
        Thread.sleep(2360);
        return "方法返回值。。。。";
    }
}
```

### 多模块报错解决方法

- 将切面注入到springioc的容器中

```java
package com.xiong.conf;

import org.springframework.context.annotation.Configuration;
import org.springframework.context.annotation.Import;

@Import({
    	// 切面实现类路径
        com.xiong.uplog.UpLogFun.class
})
@Configuration
public class BatchConfigure {
}

```
