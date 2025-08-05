---
title: sentinel的简单使用
categories:
 - 后端
tags:
 - 微服务
 - sentinel
 - java
---

## 安装与启动

### 官方文档

```http
https://sentinelguard.io/zh-cn/docs/dashboard.html
```

### 下载

```http
https://github.com/alibaba/Sentinel/releases
```

### 启动

```sh
java -Dserver.port=8080 -Dcsp.sentinel.dashboard.server=localhost:8080 -Dproject.name=sentinel-dashboard -jar ./sentinel-dashboard.jar
```

### 访问

```htto
localhost:8080
```

账号密码都是sentinel

## 搭建服务

### pom

```xml
<!--sentinel-->
<dependency>
    <groupId>com.alibaba.cloud</groupId>
    <artifactId>spring-cloud-starter-alibaba-sentinel</artifactId>
</dependency>
<!--持久化到nacos-->
<dependency>
    <groupId>com.alibaba.csp</groupId>
    <artifactId>sentinel-datasource-nacos</artifactId>
</dependency>
```

### application.yml

```yaml
server:
  port: 8001
spring:
  application:
    name: demo-sentinel
  profiles:
    active: dev
  cloud:
    nacos:
      discovery:
        server-addr: localhost:8848
        namespace: public
        group: DEFAULT_GROUP
        username: nacos
        password: nacos
    sentinel:
      enabled: true
      transport:
        port: 8719 #端口配置会在应用对应的机器上启动一个 Http Server，该 Server 会与 Sentinel 控制台做交互
        dashboard: localhost:8080
      # 将限流的数据持久化到nacos
      datasource:
        ds:
          nacos:
            dataId: ${spring.application.name}-flow-rules
            groupId: DEFAULT_GROUP
            data‐type: json
            rule‐type: flow

logging:
  config: classpath:logback.xml


```

### 新增公共异常处理

```java
import com.alibaba.csp.sentinel.adapter.spring.webmvc.callback.BlockExceptionHandler;
import com.alibaba.csp.sentinel.slots.block.BlockException;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.xiong.demo.utils.R;
import org.springframework.http.HttpStatus;
import org.springframework.http.MediaType;
import org.springframework.stereotype.Component;

import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import java.io.IOException;
import java.io.PrintWriter;

/**
 * @Auther: 张一雄
 * @Date: 2023/5/29 16:02
 * @Description: DefaultBlockExceptionHandler
 * @Version 1.0.0
 */
@Component
public class DefaultBlockExceptionHandler implements BlockExceptionHandler {
    public DefaultBlockExceptionHandler() {
    }

    public void handle(HttpServletRequest request, HttpServletResponse response, BlockException e) throws IOException {
        /*response.setStatus(429);
        PrintWriter out = response.getWriter();
        out.print("Blocked by Sentinel (flow limiting)");
        out.flush();
        out.close();*/
        ObjectMapper mapper = new ObjectMapper();
        response.setStatus(HttpStatus.OK.value());
        response.setContentType(MediaType.APPLICATION_JSON_UTF8_VALUE);
        mapper.writeValue(response.getWriter(), R.error("进入流控报错"));

    }
}

```

### 新增配置类

```java
import com.xiong.demo.utils.R;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

/**
 * @Auther: 张一雄
 * @Date: 2023/5/29 14:10
 * @Description: TestController
 * @Version 1.0.0
 */

@RestController
@RequestMapping("/test")
public class TestController {


    @GetMapping("/test")
    public R test(){
        return R.ok("test------------------------");
    }

}

```

## sentinel配置

### 说明

首先访问一下项目的接口，在sentinel的控制台才能出现该项目

### 配置

配置美秒请求次数超过一，则报错

![image-20230529164233926](https://img.myfox.fun/img/20230529164235.png)

### 测试

![image-20230529164327298](https://img.myfox.fun/img/20230529164328.png)

## 配置持久化

### 新增配置

首先配置文件和 pom引入了相关配置后（上面有写），需要在nacos中新增一个配置文件

```json
[
  {
    "resource": "/test/test",
    "controlBehavior": 0,
    "count": 15.0,
    "grade": 1,
    "limitApp": "default",
    "strategy": 0
  }
]
```

![image-20230529164452579](https://img.myfox.fun/img/20230529164453.png)

### 测试

修改配置文件，sentinel中的配置会跟着一起改变，

但是修改sentinel中的文件，nacos中的不会跟着改变

如果需要双向绑定，需要修改sentinel的源码（我只知道这中方式）

## 其他测试

### 测试熔断

![image-20230529165058041](https://img.myfox.fun/img/20230529165059.png)

### 在nacos新增熔断规则

#### application.yml

```yaml
    sentinel:
      enabled: true
      transport:
        port: 8719 #端口配置会在应用对应的机器上启动一个 Http Server，该 Server 会与 Sentinel 控制台做交互
        dashboard: localhost:8080
      # 将限流的数据持久化到nacos（需要配置中心新增配置）
      datasource:
        flow-ds: # 名字随便写，流程配置
          nacos:
            dataId: ${spring.application.name}-flow-rules
            groupId: DEFAULT_GROUP
            data‐type: json
            rule‐type: flow #表示数据源中规则属于哪种类型，如flow、degrade、param-flow、gw-flow等。
         #熔断配置
        degrade-ds: # 名字随便写，
          nacos:
            dataId: ${spring.application.name}-degrade-rules
            groupId: DEFAULT_GROUP
            data‐type: json
            rule‐type: degrade
```

#### nacos新增配置文件

![image-20230529171542454](https://img.myfox.fun/img/20230529171543.png)

### json如何编写

在页面上可以找到

![image-20230529171729159](https://img.myfox.fun/img/20230529171730.png)
