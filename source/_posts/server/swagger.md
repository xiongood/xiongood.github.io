---
title: springboot整合swagger
author: 张一雄
summary: 调试工具，但是现在springboot3.0现在还不能使用哦
img: https://img.myfox.fun/img/springboot.jpg
categories:
 - 后端
tags:
 - swagger
 - java
---

## 搭建

### pom

```xml
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 https://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>
    <groupId>com.xiong</groupId>
    <artifactId>demo-swagger</artifactId>
    <version>0.0.1-SNAPSHOT</version>
    <name>demo-swagger</name>
    <description>demo-swagger</description>
    <properties>
        <java.version>1.8</java.version>
        <project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>
        <project.reporting.outputEncoding>UTF-8</project.reporting.outputEncoding>
        <spring-boot.version>2.7.5</spring-boot.version>
    </properties>
    <dependencies>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-web</artifactId>
        </dependency>
        <dependency>
            <groupId>cn.hutool</groupId>
            <artifactId>hutool-all</artifactId>
            <version>5.8.16</version>
        </dependency>

        <dependency>
            <groupId>io.springfox</groupId>
            <artifactId>springfox-swagger-ui</artifactId>
            <version>3.0.0</version>
        </dependency>
        <dependency>
            <groupId>com.github.xiaoymin</groupId>
            <artifactId>swagger-bootstrap-ui</artifactId>
            <version>1.9.4</version>
        </dependency>
        <!--去掉swagger报错-->
        <dependency>
            <groupId>io.springfox</groupId>
            <artifactId>springfox-swagger2</artifactId>
            <version>3.0.0</version>
            <exclusions>
                <exclusion>
                    <groupId>io.swagger</groupId>
                    <artifactId>swagger-models</artifactId>
                </exclusion>
            </exclusions>
        </dependency>
        <dependency>
            <groupId>io.swagger</groupId>
            <artifactId>swagger-models</artifactId>
            <version>1.5.21</version>
        </dependency>
    </dependencies>
</project>
```

### yml

```yaml
server:
  port: 8080

spring:
  mvc:
    pathmatch:
      matching-strategy: ant_path_matcher
```

### 配置文件-1

```java
import org.springframework.boot.autoconfigure.condition.ConditionalOnClass;
import org.springframework.web.servlet.config.annotation.ResourceHandlerRegistry;
import org.springframework.web.servlet.config.annotation.WebMvcConfigurer;
import springfox.documentation.spring.web.SpringfoxWebMvcConfiguration;

@ConditionalOnClass(SpringfoxWebMvcConfiguration.class)
public class SwaggerBootstrapUiConfiguration implements WebMvcConfigurer {

    @Override
    public void addResourceHandlers(ResourceHandlerRegistry registry) {
        registry.addResourceHandler("doc.html").addResourceLocations("classpath:/META-INF/resources/");
        registry.addResourceHandler("/webjars/**").addResourceLocations("classpath:/META-INF/resources/webjars/");
    }
}

```

### 配置文件-2

```java
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.web.bind.annotation.RequestMethod;
import springfox.documentation.builders.ApiInfoBuilder;
import springfox.documentation.builders.PathSelectors;
import springfox.documentation.builders.RequestHandlerSelectors;
import springfox.documentation.service.ApiInfo;
import springfox.documentation.service.Contact;
import springfox.documentation.service.ResponseMessage;
import springfox.documentation.spi.DocumentationType;
import springfox.documentation.spring.web.plugins.Docket;
import springfox.documentation.swagger2.annotations.EnableSwagger2;

import java.util.ArrayList;
import java.util.List;

@Configuration
@EnableSwagger2
public class SwaggerConfiguration {

    @Bean
    public Docket projectTestApi() {
        return new Docket(
                DocumentationType.SWAGGER_2).groupName("第一个文档")
                .apiInfo(apiInfo())
                .select()
                // controller 的文件路径
                .apis(RequestHandlerSelectors.basePackage("com.xiong.demo.controller"))
                .paths(PathSelectors.any())
                .build().useDefaultResponseMessages(false)
                .globalResponseMessage(RequestMethod.GET, globalResponseList())
                .globalResponseMessage(RequestMethod.POST, globalResponseList()
                )
                ;
    }

    @Bean
    public Docket projectTestApi2() {
        return new Docket(
                DocumentationType.SWAGGER_2).groupName("第二个文档")
                .apiInfo(apiInfo())
                .select()
                // controller 的文件路径
                .apis(RequestHandlerSelectors.basePackage("com.xiong.demo.controller"))
                .paths(PathSelectors.any())
                .build().useDefaultResponseMessages(false)
                .globalResponseMessage(RequestMethod.GET, globalResponseList())
                .globalResponseMessage(RequestMethod.POST, globalResponseList()
                )
                ;
    }


    private ApiInfo apiInfo() {
        return new ApiInfoBuilder()
                .title("java规则接口文档")
                .termsOfServiceUrl("")
                .contact(new Contact("张一雄", "", "xxxx@qq.com"))
                .version("1.0")
                .build();
    }

    private List<ResponseMessage> globalResponseList() {
        List<ResponseMessage> responseMessages = new ArrayList<>();
        return responseMessages;
    }
}
```

### 测试类

```java
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;


@RequestMapping("/test")
@RestController
public class TestController {


    @GetMapping("/test")
    public String test(){
        System.out.println("success!");
        return "success!";
    }

}
```

### 启动类

```java
package com.xiong.demo;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.core.env.Environment;

@SpringBootApplication
public class SwaggerApplication {

    public static void main(String[] args) {
        Environment env = new SpringApplication(SwaggerApplication.class).run(args).getEnvironment();;
        System.out.println("启动成功: http://localhost:"+ env.getProperty("server.port")+"/doc.html" );
    }
}
```



## 常用注解

### 实体类

```java
import io.swagger.annotations.ApiModel;
import io.swagger.annotations.ApiModelProperty;
import lombok.Data;

/**
 * @Auther: 张一雄
 * @Date: 2023/5/9 10:35
 * @Description: AppInfo
 * @Version 1.0.0
 */
@Data
@ApiModel(value="AppInfo",description="App信息实体类")
public class AppInfo {

    @ApiModelProperty("App的id")
    private Integer id;

    @ApiModelProperty("软件名称")
    private String softwareName;

}

```

### 接口文档注解

```java
package com.xiong.demo.controller;

import com.xiong.demo.entity.AppInfo;
import io.swagger.annotations.*;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.multipart.MultipartFile;

import javax.servlet.http.HttpServletRequest;
import java.io.IOException;


@RequestMapping("/test")
@RestController
@Api(tags = "c-测试controller注解"  //描述
        , description = "c-测试类 description" // 名称
        ,hidden = false )// 是否隐藏
public class TestController {


    /**
     * 详细描述: 常规接口文档
     * @author 张一雄
     * @param name
     * @return { java.lang.String }
     * @exception/throws
     * 创建日期: 2023/5/9 10:29
     */
    @GetMapping("/testApiOperation")
    @ApiOperation(value = "1-测试方法value"
            //tags = "1-测试方法tags"  //描述
            ,hidden = false // 是否隐藏
    )
    public String testApiOperation(String name){
        System.out.println("success!");
        return "success!";
    }

    /**
     * 详细描述:ApiImplicitParam显示参数的信息
     * @author 张一雄
     * @param resumeID
     * @return { java.lang.String }
     * @exception/throws
     * 创建日期: 2023/5/9 10:29
     */
    @ApiOperation(value = "2-单条件查询"
           // tags = "2-测试方法tags"  //描述
            ,hidden = false // 是否隐藏
            )
    @ApiImplicitParam(value = "2-更新id",
            name = "resumeID", // 参数明
            paramType = "query", // 查询类型
            dataType = "String") //参数类型
    @GetMapping(value="/testApilmplicitParam")
    public String testApilmplicitParam(String resumeID){
        return resumeID;
    }

    /**
     * 详细描述: ApiImplicitParams 显示多参数信息
     * @author 张一雄
     * @return { java.lang.String }
     * @exception/throws
     * 创建日期: 2023/5/9 10:29
     */
    @GetMapping(value="/testApiImplicitParams")
    @ApiOperation(value = "3-多条件查询"
            //tags = "3-测试方法tags"  //描述
            ,hidden = false // 是否隐藏
            )
    @ApiImplicitParams({
            @ApiImplicitParam(value="姓名",name="name",dataType="Stirng",paramType = "query"),
            @ApiImplicitParam(value="简历状态",name="status",dataType="Stirng",paramType = "query"),
            @ApiImplicitParam(value="简历来源",name="source",dataType="Stirng",paramType = "query"),
            @ApiImplicitParam(value="开始时间",name="startTime",dataType="Stirng",paramType = "query"),
            @ApiImplicitParam(value="结束时间",name="endTime",dataType="Stirng",paramType = "query")
    })
    public String testApiImplicitParams(String name,String status,String source,String startTime,String endTime){
        return "success";
    }


    /**
     * 详细描述: 描述参数信息
     * @author 张一雄
     * @return { java.lang.String }
     * @exception/throws
     * 创建日期: 2023/5/9 10:34
     */
    @ApiOperation(value = "4-描述参数信息",hidden = false)
    @GetMapping(value="uploadFile",consumes = "multipart/*",headers = "content-type=multipart/form-data")
    public String uploadFile(
                @ApiParam(value = "上传文件",required = true) MultipartFile file
                ,@ApiParam(value = "测试id") String resumeID
                , HttpServletRequest request
            )throws IOException {
        return "success";
    }

    /**
     * 详细描述: 测试实体类 的参数信息
     * @author 张一雄
     * @param appInfo
     * @return { com.xiong.demo.entity.AppInfo }
     * @exception/throws
     * 创建日期: 2023/5/9 10:39
     */
    @ApiOperation(value = "5-测试实体类",hidden = false,position= 5,tags = "测试实体类")
    @GetMapping("/testEntity")
    public AppInfo testEntity(AppInfo appInfo){

        return new AppInfo();
    }

}

```

