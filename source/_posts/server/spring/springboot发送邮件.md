---
title: springboot发送邮件
img: https://pub-b24cf0a8c1f14e9386435977aa464959.r2.dev/img/20230816145442.png
categories:
 - 后端
tags:
 - email
 - java
---

## 源码地址

```java
https://gitee.com/erhu02/demo
```

## 搭建

### pom

```xml
<!--邮件发送需要的依赖-->
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-mail</artifactId>
</dependency>

<!--邮件发送模板需要的依赖-->
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-thymeleaf</artifactId>
</dependency>

```

### yml

```yaml
spring:
  mail:
    host: smtp.163.com
    username: java0417@163.com
    #配置邮件客户端后生成的密码
    password: VOLUQQCWCVXBQCUM
    default-encoding: UTF-8
```

密码不是登录密码，获取方式：

![image-20230510183446216](https://pub-b24cf0a8c1f14e9386435977aa464959.r2.dev/img/20230510183447.png)

![image-20230510183505194](https://pub-b24cf0a8c1f14e9386435977aa464959.r2.dev/img/20230510183506.png)

### 接口

```java
import javax.mail.MessagingException;


public interface IMailService {
    /**
     * 简单文本邮件
     * @param toUser 邮件接收者
     */
    void simpleMil(String toUser);

    /**
     * html邮件
     * @param toUser
     */
    void htmlMail(String toUser) throws MessagingException;

    /**
     * 带附件邮件
     * @param toUser
     */
    void attachmentMail(String toUser) throws MessagingException;

    /**
     * 带图片邮件
     * @param toUser
     */
    void imgMail(String toUser) throws MessagingException;

    /**
     * 模板邮件
     * @param toUser
     */
    void templateMail(String toUser) throws MessagingException;
}

```

### 实现类

```java
import com.xiong.demo.email.service.IMailService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.core.io.FileSystemResource;
import org.springframework.mail.SimpleMailMessage;
import org.springframework.mail.javamail.JavaMailSender;
import org.springframework.mail.javamail.MimeMessageHelper;
import org.springframework.stereotype.Service;
import org.thymeleaf.TemplateEngine;
import org.thymeleaf.context.Context;

import javax.mail.MessagingException;
import javax.mail.internet.MimeMessage;
import java.io.File;


@Service
public class MailServiceImpl implements IMailService {

    /**
     * 发送邮件接口
     */
    @Autowired
    private JavaMailSender jms;

    /**
     * 发送模板邮件时解析模板
     */
    @Autowired
    private TemplateEngine templateEngine;

    /**
     * 读取配置文件中的邮件发送者账号
     */
    @Value("${spring.mail.username}")
    private String from;

    /**
     * 简单文本邮件
     *
     * @param toUser 邮件接收者
     */
    @Override
    public void simpleMil(String toUser) {
        //初始化简单的邮件对象
        SimpleMailMessage message = new SimpleMailMessage();
        //邮件发送者
        message.setFrom(from);
        //邮件接收者
        message.setTo(toUser);
        //邮件标题
        message.setSubject("文字格式邮件");
        //邮件内容
        message.setText("文字格式内容");
        //发送邮件
        jms.send(message);
    }

    /**
     * html邮件
     */
    @Override
    public void htmlMail(String toUser) throws MessagingException {
        MimeMessage message = jms.createMimeMessage();
        MimeMessageHelper helper = new MimeMessageHelper(message, true);
        helper.setFrom(from);
        helper.setTo(toUser);
        helper.setSubject("html格式标题");
        String content = "<p style='color:yellow;'>这是一封html格式的文件</p><h1>这是一封html格式的文件</h1>";
        //true表示以html格式发送邮件
        helper.setText(content, true);
        jms.send(message);
    }

    /**
     * 带附件邮件
     */
    @Override
    public void attachmentMail(String toUser) throws MessagingException {
        MimeMessage message = jms.createMimeMessage();
        MimeMessageHelper helper = new MimeMessageHelper(message, true);
        helper.setFrom(from);
        helper.setTo(toUser);
        helper.setSubject("带附件");
        helper.setText("这是一封带附件的邮件");
        //加载文件路径
        FileSystemResource fs = new FileSystemResource(new File(this.getClass()
                .getResource("/").getPath() + "\\test.jpg"));
        //添加附件
        helper.addAttachment("自己菜与大佬菜的区别.jpg", fs);
        jms.send(message);
    }

    /**
     * 带图片邮件
     */
    @Override
    public void imgMail(String toUser) throws MessagingException {
        MimeMessage message = jms.createMimeMessage();
        MimeMessageHelper helper = new MimeMessageHelper(message, true);
        helper.setFrom(from);
        helper.setTo(toUser);
        helper.setSubject("带图片邮件");
        //设置资源的cid
        String content = "<html><body>小菜鸡图片<img src='cid:img'/></body></html>";
        helper.setText(content, true);
        FileSystemResource fs = new FileSystemResource(new File(this.getClass().getResource("/").getPath()
                + "\\test.jpg"));
        helper.addInline("img", fs);
        jms.send(message);
    }

    /**
     * 模板邮件
     */
    @Override
    public void templateMail(String toUser) throws MessagingException {
        MimeMessage message = jms.createMimeMessage();
        MimeMessageHelper helper = new MimeMessageHelper(message, true);
        helper.setFrom(from);
        helper.setTo(toUser);
        helper.setSubject("模板邮件");
        Context context = new Context();
        context.setVariable("username", "段誉");
        //thymeleaf模板默认会从src/resources/templates目录下寻找文件，填入我们定义的模板名，不需要写后缀
        String template = templateEngine.process("MailTemplate", context);
        helper.setText(template, true);
        jms.send(message);
    }
}
```

### 测试类

用了swagger，不需要的话，直接删掉就行

```java
import com.xiong.demo.email.service.IMailService;
import com.xiong.demo.utils.R;
import io.swagger.annotations.Api;
import io.swagger.annotations.ApiOperation;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.HashMap;
import java.util.Map;


@RequestMapping("/mail")
@RestController
@Api(tags = "测试邮件文档")
public class EmailController {

    @Autowired
    private IMailService mailService;

    @GetMapping("/simple")
    @ApiOperation(value = "发送普通邮件")
    public R sendSimpleMail() {
        Map<String, Object> map = new HashMap<>();
        try {
            mailService.simpleMil("erhu02@sina.com");
           return R.ok();
        } catch (Exception e) {
            e.printStackTrace();
            return R.error();
        }
    }

    @GetMapping("/html")
    @ApiOperation(value = "发送html邮件")
    public Map<String, Object> htmlMail(){
        Map<String, Object> map =new HashMap<>();
        try {
            mailService.htmlMail("erhu02@sina.com");
            map.put("res", "success");
        } catch (Exception e) {
            e.printStackTrace();
            map.put("res", "error");
        }
        return map;
    }

    @GetMapping("/attachments")
    @ApiOperation(value = "发送带附件邮件")
    public Map<String, Object> attachmentsMail(){
        Map<String, Object> map =new HashMap<>();
        try {
            mailService.attachmentMail("erhu02@sina.com");
            map.put("res", "success");
        } catch (Exception e) {
            e.printStackTrace();
            map.put("res", "error");
        }
        return map;
    }

    @GetMapping("/img")
    @ApiOperation(value = "发送带图片邮件")
    public Map<String, Object> imgMail(){
        Map<String, Object> map =new HashMap<>();
        try {
            mailService.imgMail("erhu02@sina.com");
            map.put("res", "success");
        } catch (Exception e) {
            e.printStackTrace();
            map.put("res", "error");
        }
        return map;
    }

    @GetMapping("/template")
    @ApiOperation(value = "发送模板邮件")
    public Map<String, Object> templateMail(){
        Map<String, Object> map =new HashMap<>();
        try {
            mailService.templateMail("erhu02@sina.com");
            map.put("res", "success");
        } catch (Exception e) {
            e.printStackTrace();
            map.put("res", "error");
        }
        return map;
    }
}
```

### 模板

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Insert title here</title>
</head>
<body>
  <h1>您好，<span th:text="${username}"></span>:这是来自测试的邮件模板！</h1>
</body>
</html>
```

### 目录结构

![image-20230510183815242](https://pub-b24cf0a8c1f14e9386435977aa464959.r2.dev/img/20230510183816.png)

## 测试

![image-20230510183918249](https://pub-b24cf0a8c1f14e9386435977aa464959.r2.dev/img/20230510183919.png)







