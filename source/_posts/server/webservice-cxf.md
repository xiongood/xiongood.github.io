---
title: webservice与cxf
author: 张一雄
summary: webservice感觉是很老的技术了，但是有些项目正常跑了十几年了，所以还是得知道这个技术才行。
categories:
 - 后端
tags:
 - webservice
 - cxf
---

## 搭建一个服务端

### pom

```xml
<!--webservice start-->
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-web-services</artifactId>
</dependency>
<dependency>
    <groupId>org.apache.cxf</groupId>
    <artifactId>cxf-spring-boot-starter-jaxws</artifactId>
    <version>3.4.3</version>
</dependency>
<dependency>
    <groupId>org.apache.cxf</groupId>
    <artifactId>cxf-rt-transports-http-jetty</artifactId>
    <version>3.4.3</version>
</dependency>
<dependency>
    <groupId>org.apache.cxf.xjc-utils</groupId>
    <artifactId>cxf-xjc-runtime</artifactId>
    <version>3.1.0</version>
</dependency>
<!--webservice end-->
```

### 编写入参

```java
import lombok.Data;

import javax.xml.bind.annotation.XmlAccessType;
import javax.xml.bind.annotation.XmlAccessorType;
import javax.xml.bind.annotation.XmlElement;
import javax.xml.bind.annotation.XmlType;
import java.util.Date;


@XmlAccessorType(XmlAccessType.FIELD)
// name值不能重复
@XmlType(name = "SysUser", propOrder = {
    "id",
    "userName",
    "age",
    "sex",
    "createDate"
})
@Data
public class SysUser {

    @XmlElement(name = "ID", required = true)
    protected Long id;
    @XmlElement(name = "USER_NAME", required = true)
    protected String userName;
    @XmlElement(name = "AGE", required = true)
    protected int age;
    @XmlElement(name = "SEX", required = true)
    protected int sex;
    @XmlElement(name = "CREATE_DATE", required = true)
    protected Date createDate;

}

```

```java
import lombok.Data;

import javax.xml.bind.annotation.*;


// 输入参数类
@XmlAccessorType(XmlAccessType.FIELD)
@XmlType(name = "Input", propOrder = {
        "sysUser"
})
//xml转字符串工具
@XmlRootElement
@Data
public class Input {

    @XmlElement(name = "SYS_USER", required = true)
    protected SysUser sysUser;


}

```

### 编写出参

```java
import lombok.Data;

import javax.xml.bind.annotation.*;


// 输出参数类
@XmlAccessorType(XmlAccessType.FIELD)
@XmlType(name = "Output", propOrder = {
    "code",
    "message",
    "data"
})
@XmlRootElement
@Data
public class Output {

    @XmlElement(name = "CODE", required = true, nillable = true)
    protected String code;
    @XmlElement(name = "MESSAGE", required = true, nillable = true)
    protected String message;

    @XmlElement(name = "DATA", required = true, nillable = true)
    protected Object data;


}

```

### 编写服务类

```java
import com.xiong.demo.entity.Input;
import com.xiong.demo.entity.Output;
import org.apache.cxf.bindings.xformat.ObjectFactory;
import org.springframework.stereotype.Service;

import javax.jws.WebMethod;
import javax.jws.WebParam;
import javax.jws.WebResult;
import javax.jws.WebService;
import javax.jws.soap.SOAPBinding;
import javax.xml.bind.annotation.XmlSeeAlso;

/**
 * @Auther: 张一雄
 * @Date: 2023/5/16 09:52
 * @Version 1.0.0
 */
@Service
@WebService(serviceName = "MyService", // 与接口中指定的name一致, 都可以不写
        targetNamespace = "http://test.com/MyService" // 与接口中的命名空间一致,一般是接口的包名倒，都可以不用写
)
@XmlSeeAlso({ObjectFactory.class})
@SOAPBinding(parameterStyle = SOAPBinding.ParameterStyle.BARE)
public class MyService {

    @WebMethod(action = "process")
    @WebResult( name = "processResponse", partName = "processResponse", targetNamespace = "http://test.com/MyService")
    public Output process(@WebParam(partName = "process",name = "process",targetNamespace = "http://test.com/MyService") Input payload) {
        System.out.println("服务被调通……………………………………………………………………………………");
        System.out.println(payload.getSysUser().getCreateDate());
        Output output = new Output();
        output.setCode("200");
        output.setMessage("请求成功");
        output.setData("请求成功");
        return output;
    }
}
```

### 编写配置类

```java
import service.com.xiong.demo.MyService;
import org.apache.cxf.Bus;
import org.apache.cxf.jaxws.EndpointImpl;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

import javax.xml.ws.Endpoint;


@Configuration
public class CxfConfig {

    @Autowired
    MyService myService;

    @Autowired
    private Bus bus;

    /**
     * 发布服务
     * @return
     */
    @Bean
    public Endpoint userServiceEndpoint() {
        System.out.println("服务发布");
        //这里指定的端口不能跟应用的端口冲突, 单独指定
        String path = "http://127.0.0.1:9090/MyService";

        EndpointImpl userEndpoint = new EndpointImpl(bus, myService);
        userEndpoint.publish(path);

        System.out.println("服务成功，path: " + path);
        System.out.println(String.format("在线的wsdl：%s?wsdl", path));
        return userEndpoint;
    }
}

```

### 测试

- 启动后访问

```http
http://127.0.0.1:9090/MyService?wsdl
```

## 使用soapUI调用

![image-20230517094358805](https://img.myfox.fun/img/20230517094359.png)

![image-20230517094505621](https://img.myfox.fun/img/20230517094506.png)

## 使用postman 调用

![image-20230517094719640](https://img.myfox.fun/img/20230517094720.png)

## 保存wsdl 文件

保存wsdl文件后，其他协作人员，可以根据wsdl文件生成代码，来编写客户端 或者再写个服务端

打开http://127.0.0.1:9090/MyService?wsdl，然后ctrl+s

![image-20230516180414991](https://img.myfox.fun/img/20230516180416.png)

## wsdl文件生成代码

### 安装并配置apache-cxf

略

### 执行命令

```sh
# -d 输出路径
# -client wsdl路径
wsdl2java -encoding utf-8 -d D:\server\cxf\output -client D:\server\cxf\input\ImportPOSignatureSrv.wsdl
```

### 生成的代码如下

### ![image-20230517103156819](https://img.myfox.fun/img/20230517103157.png)

## 根据生成的代码搭建客户端

### 创建springboot项目

### pom

```xml
<!--webservice start-->
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-web-services</artifactId>
</dependency>
<dependency>
    <groupId>org.apache.cxf</groupId>
    <artifactId>cxf-spring-boot-starter-jaxws</artifactId>
    <version>3.4.3</version>
</dependency>
<dependency>
    <groupId>org.apache.cxf</groupId>
    <artifactId>cxf-rt-transports-http-jetty</artifactId>
    <version>3.4.3</version>
</dependency>
<dependency>
    <groupId>org.apache.cxf.xjc-utils</groupId>
    <artifactId>cxf-xjc-runtime</artifactId>
    <version>3.1.0</version>
</dependency>
<!--webservice end-->
```

### 将生成的代码，放到项目中

注：需要修改日期格式

![image-20230517103419664](C:/Users/java0/AppData/Roaming/Typora/typora-user-images/image-20230517103419664.png)

### 编写service

```java
import com.xiong.demo.entity.Input;
import com.xiong.demo.entity.MyService;
import com.xiong.demo.entity.MyService_Service;
import com.xiong.demo.entity.Output;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Component;

import java.net.URL;

@Slf4j
@Component
public class PublicSecurityService {
    
    // 发送
    public Output post(Input input) {
        try {
            MyService_Service serviceService = new MyService_Service(new URL("http://127.0.0.1:9090/MyService?wsdl"));
            MyService myServicePort = serviceService.getMyServicePort();
            Output process = myServicePort.process(input);
            return process;
        } catch (Exception e) {
            log.error("invoke WS userAddNew method error: {}", e.getMessage());
        }
        return null;
    }
}
```

### 编写controller

```java
import com.xiong.demo.entity.Input;
import com.xiong.demo.entity.Output;
import com.xiong.demo.entity.SysUser;
import com.xiong.demo.service.PublicSecurityService;
import com.xiong.demo.utils.R;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.Date;

@RequestMapping("/test")
@RestController
public class TestController {

    @Autowired
    PublicSecurityService publicSecurityService;

    @GetMapping("/test")
    public R test(){
        Input input = new Input();
        SysUser sysUser = new SysUser();
        sysUser.setCREATEDATE(new Date());
        input.setSYSUSER(sysUser);
        Output output = publicSecurityService.post(input);
        System.out.println("------------------");
        System.out.println(output.getMESSAGE());
        System.out.println("------------------");
        System.out.println("success!");
        return R.ok();
    }
}
```

### 测试

```http
http://localhost:8082/test/test
```

## 使用生成的代码搭建服务端

### 创建springboot项目

### pom

```xml
<!--webservice start-->
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-web-services</artifactId>
        </dependency>
        <dependency>
            <groupId>org.apache.cxf</groupId>
            <artifactId>cxf-spring-boot-starter-jaxws</artifactId>
            <version>3.4.3</version>
        </dependency>
        <dependency>
            <groupId>org.apache.cxf</groupId>
            <artifactId>cxf-rt-transports-http-jetty</artifactId>
            <version>3.4.3</version>
        </dependency>
        <dependency>
            <groupId>org.apache.cxf.xjc-utils</groupId>
            <artifactId>cxf-xjc-runtime</artifactId>
            <version>3.1.0</version>
        </dependency>
```

### 导入生成的代码

![image-20230517115330669](https://img.myfox.fun/img/20230517115332.png)

### 实现生成的接口

```java
import com.xiong.demo.entity.Input;
import com.xiong.demo.entity.MyService;
import com.xiong.demo.entity.Output;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;

import javax.jws.WebService;

/**
 * @Auther: 张一雄
 * @Date: 2023/5/17 10:44
 * @Description: ServerService
 * @Version 1.0.0
 */

@Service
@Slf4j
@WebService(
        serviceName = "MyService", // 服务名
        portName = "MyServicePort", // port名
        targetNamespace = "http://test.com/MyService", // 命名空间
        endpointInterface = "com.xiong.demo.entity.MyService") // 接口路径
public class ServerServiceImpl implements MyService { //实现生成的接口

    // 实现方法
    @Override
    public Output process(Input process) {
        System.out.println("服务被调通……………………………………………………………………………………");
        System.out.println(process.getSYSUSER().getCREATEDATE());
        Output output = new Output();
        output.setCODE("200");
        output.setMESSAGE("请求成功");
        output.setDATA("请求成功");
        return output;
    }
}

```

### 发布接口

```java
import com.xiong.demo.entity.MyService;
import lombok.extern.slf4j.Slf4j;
import org.apache.cxf.Bus;
import org.apache.cxf.bus.spring.SpringBus;
import org.apache.cxf.jaxws.EndpointImpl;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Configuration
@Slf4j
public class CxfConfig {

    //@Autowired
    //private Bus bus;

    @Autowired
    MyService myService;


    @Bean(name = Bus.DEFAULT_BUS_ID)
    public SpringBus springBus() {
        return new SpringBus();
    }

    /*服务端接口发布*/
    @Bean
    public void publishServices() {
            try {
                String path = "http://127.0.0.1:8084/MyService";
                EndpointImpl endpoint = new EndpointImpl(springBus(), myService);
                endpoint.publish(path);
                System.out.println("服务成功，path: " + path);
                System.out.println(String.format("在线的wsdl：%s?wsdl", path));
            } catch (Exception e) {
                e.printStackTrace();
                System.out.println(e.getMessage());
            }
    }
}

```

### 测试

```http
http://127.0.0.1:8084/MyService?wsdl
```

### 用soupUI和postman测试

















