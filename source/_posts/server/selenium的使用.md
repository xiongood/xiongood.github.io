---
title: selenium的使用
author: 张一雄
summary: selenium是一款自动化测试工具，我用此工具做了个自动签到的工具！
img: https://pub-b24cf0a8c1f14e9386435977aa464959.r2.dev/img/20230816085751.png
tags:
  - selenium
categories:
  - 后端
---

selenium是一款自动化测试工具，我用此工具做了个自动签到的工具！

## 下载谷歌浏览器驱动

### 地址

版本号，要与本地的谷歌浏览器一致

```http
https://chromedriver.chromium.org/downloads
```

![image-20230815113403248](https://pub-b24cf0a8c1f14e9386435977aa464959.r2.dev/img/20230815113404.png)

### 加入环境变量

![image-20230815113604564](https://pub-b24cf0a8c1f14e9386435977aa464959.r2.dev/img/20230815113605.png)

## 整合selenium

我用的 springboot3.0

### pom

```xml
<!-- https://mvnrepository.com/artifact/org.seleniumhq.selenium/selenium-java -->
<dependency>
    <groupId>org.seleniumhq.selenium</groupId>
    <artifactId>selenium-java</artifactId>
    <version>4.11.0</version>
</dependency>
<!-- https://mvnrepository.com/artifact/org.seleniumhq.selenium/selenium-api -->
<dependency>
    <groupId>org.seleniumhq.selenium</groupId>
    <artifactId>selenium-api</artifactId>
    <version>4.11.0</version>
</dependency>

<dependency>
    <groupId>org.testng</groupId>
    <artifactId>testng</artifactId>
    <version>7.8.0</version>
</dependency>
```

### 实现打开浏览器并且登录功能

```java
package com.xiong.demojdk17.controller;


import lombok.extern.slf4j.Slf4j;
import org.openqa.selenium.By;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.chrome.ChromeDriver;
import org.openqa.selenium.chrome.ChromeOptions;

import java.io.File;

/**
 * @Auther: 张一雄
 * @Date: 2023/7/21 15:41
 * @Description: Test
 * @Version 1.0.0
 */
@Slf4j
public class TestController {
    public static void main(String[] args)  {
        try {
            // 驱动位置
            File file = new File("D:\\app\\other\\chromedriver\\chromedriver.exe");
            // 指定驱动
            System.setProperty("webdriver.chrome.driver",file.getAbsolutePath());
            // 只能本地ip
            System.setProperty("webdriver.chrome.whitelistedIps", "");
            ChromeOptions chromeOptions = new ChromeOptions();
            //解决 403 出错问题
            chromeOptions.addArguments("--remote-allow-origins=*");
            ChromeDriver driver = new ChromeDriver(chromeOptions);
            // 打开地址
            driver.get("https://www.xxx.com/");
            // 给输入框赋值
            WebElement text_name = driver.findElement(By.id("email"));
            WebElement text_pwd = driver.findElement(By.id("password"));
            driver.findElement(By.id("email")).clear();
            text_name.sendKeys("loginname");
            driver.findElement(By.id("password")).clear();
            text_pwd.sendKeys("password");
            // 点击登录
            WebElement login_submit = driver.findElement(By.id("login_submit"));
            login_submit.click();
            Thread.sleep(10000);
            WebElement checkin = driver.findElement(By.id("checkin"));
            if (null != checkin){
                checkin.click();
            }
            // 关闭会话
            driver.close();
        }catch (Exception e){
            log.error("出现异常！");
            e.printStackTrace();
            log.error(e.getMessage());
        }

    }
}

```

## 其他

### linux 安装驱动

```shell
# 安装浏览器
wget https://dl.google.com/linux/direct/google-chrome-stable_current_x86_64.rpm
yum install ./google-chrome-stable_current_x86_64.rpm
# 查看浏览器版本
google-chrome -version 
# 安装驱动（对应版本）
wget https://edgedl.me.gvt1.com/edgedl/chrome/chrome-for-testing/116.0.5845.96/linux64/chromedriver-linux64.zip
# 解压
unzip chromedriver_linux64.zip
# 权限
chmod 755 chromedriver

cp chromedriver /usr/bin/
```

