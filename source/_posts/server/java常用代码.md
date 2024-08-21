---
title: java常用代码
author: 张一雄
summary: 简单的elk的实现，方便理解其运行过程及实现原理！
img: https://pub-b24cf0a8c1f14e9386435977aa464959.r2.dev/img/20240105175742.png
categories:
 - 后端
tags:
 - java
---

# 常用

## spring

### 获取bean

```java
ApplicationContext wac = SpringContextUtils.getApplicationContext();
wac.getBean("beanName");
```



### 项目启动时调用某方法

```java
@Component
public class PostConstruct {
    @PostConstruct
    public void test() {
        System.out.println("PostConstruct:开始运行...");
    }
}
```

### 直接获得request和response

```java
// request
HttpServletRequest request = 
((ServletRequestAttributes) RequestContextHolder.getRequestAttributes()).getRequest();
// response
HttpServletResponse response1 = 
((ServletRequestAttributes) RequestContextHolder.getRequestAttributes()).getResponse();
```

### 获取配置文件中的内容

#### 方式一（java获取）

```java
@PropertySource("classpath:application.properties")
@Configuration
public class Config {
    @Value("${test.info: infoStr}")
    private String infoStr;
}
```

```yml
test:
  info: infoStr
```

#### 方式二（yml获取）

```yml
date:
  pghost: 192.168.1.106
  orahost: 192.168.1.109

spring:
  datasource:
    jdbc-url: jdbc:oracle:thin:@${date.orahost}:1521:helowin

```

#### 方式三（附加一种单例模式）

```java
import java.io.IOException;
import java.util.Properties;

// 饿汉式-静态代码块类型 单例模式
public class Singleton3 {
    private Singleton3(){};
    private String info;
    private Singleton3(String info){
        this.info = info;
    }
    public static final Singleton3 INSTANCE ;
    static{
        try {
            Properties properties = new Properties();
            properties.load(Singleton3.class.getClassLoader().getResourceAsStream("application.properties"));
            INSTANCE= new Singleton3(properties.getProperty("test.info"));

        } catch (IOException e) {
            throw  new RuntimeException();
        }
    }

    public String getInfo() {
        return info;
    }

    public void setInfo(String info) {
        this.info = info;
    }

    @Override
    public String toString() {
        return "Singleton3{" +
                "info='" + info + '\'' +
                '}';
    }
}
```

```yml
test:
  info: infoStr
```

#### 方式四(springboot)

```java
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.core.env.Environment;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class CaptchaController {
    @Autowired
    private Environment environment;

    @GetMapping("getInfo")
    private String getInfo(){

        return environment.getProperty("test.info");
    }
}
```

```yml
test:
  info: infoStr
```

#### 方式五（作为配置文件）

```java
import lombok.Data;
import org.springframework.boot.context.properties.ConfigurationProperties;
import org.springframework.stereotype.Component;

/**
 * @author ：ZhangYiXiong
 * @date ：Created in 2022/4/15 星期五 17:53
 * @description：
 * @modified By：
 * @version:
 */
@Component
@ConfigurationProperties("test")
@Data
public class TestConfig {
    private String info;
}
```

```java
import com.example.captsha.config.TestConfig;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@Slf4j
public class CaptchaController {

    @Value("info")
    private  String  infoaa;

    @Autowired
    TestConfig testConfig;

    @GetMapping("getinfo2")
    public String getInfo2(){
        log.info(testConfig.getInfo());
        log.info(infoaa);
        return  infoaa;
    }
}
```

```yml
test:
  info: infoStr
```

#### 方式六（不同的环境）

application.yml

```yml
spring:
  profiles:
    active: prod
```

application-dev.yml

```yml
test:
  info: infoStr-dev
```

application-prod.yml

```yml
test:
  info: infoStr-dev
```

工具类 YamlConfigurerUtil

```java
package com.example.captsha.config;

import java.util.Properties;

public class YamlConfigurerUtil {
    private static Properties ymlProperties = new Properties();

    public YamlConfigurerUtil(Properties properties) {
        ymlProperties = properties;
    }

    public static String getStrYmlVal(String key) {
        return ymlProperties.getProperty(key);
    }

    public static Integer getIntegerYmlVal(String key) {
        return Integer.valueOf(ymlProperties.getProperty(key));
    }
}
```

配置类BeanConfiguration

```java
package com.example.captsha.config;

import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.config.YamlPropertiesFactoryBean;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.core.io.ClassPathResource;
import org.springframework.core.io.Resource;
import org.springframework.util.StringUtils;

import java.util.Properties;

@Configuration
@Slf4j
public class BeanConfiguration {

    @Bean
    public YamlConfigurerUtil ymlConfigurerUtil() {
        //1:加载配置文件
        Resource app = new ClassPathResource("application.yml");
        Resource appDev = new ClassPathResource("application-dev.yml");
        Resource appProd = new ClassPathResource("application-prod.yml");
        YamlPropertiesFactoryBean yamlPropertiesFactoryBean = new YamlPropertiesFactoryBean();
        // 2:将加载的配置文件交给 YamlPropertiesFactoryBean
        yamlPropertiesFactoryBean.setResources(app);
        // 3：将yml转换成 key：val
        Properties properties = yamlPropertiesFactoryBean.getObject();
        String active = null;
        if (properties != null) {
            active = properties.getProperty("spring.profiles.active");
        }
        if (StringUtils.isEmpty(active)) {
            log.error("未找到spring.profiles.active配置！");
        } else {
            //判断当前配置是什么环境
            if ("dev".equals(active)) {
                yamlPropertiesFactoryBean.setResources(app, appDev);
            } else if ("prod".equals(active)) {
                yamlPropertiesFactoryBean.setResources(app, appProd);
            }
        }
        // 4: 将Properties 通过构造方法交给我们写的工具类
        return new YamlConfigurerUtil(yamlPropertiesFactoryBean.getObject());
    }
}
```

调用类 controller

```java
package com.example.captsha.controller;

import com.example.captsha.config.YamlConfigurerUtil;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class TestController {

    @GetMapping("/msg")
    public String getMessage() {
        return YamlConfigurerUtil.getStrYmlVal("test.info");
    }
}
```



### 定时任务

```java
// 5秒执行一次
@Scheduled（cron="0/5 * * * *？"）

// 该方法执行完后，一秒执行一次
@Scheduled(fixedDelay = 1000,initialDelay = 0)

// 每隔两秒执行一次该方法
@Scheduled（fixedRate=2000）
    
// 启动类需要注解
@EnableScheduling
@EnableAsync
```



## 关于list

### 根据某个属性分组、转Map

```java
public static void main(String[] args) {
        List<Apple> appleList = new ArrayList<>();//存放apple对象集合

        Apple apple1 =  new Apple(1,"苹果1",new BigDecimal("3.25"),10);
        Apple apple12 = new Apple(1,"苹果2",new BigDecimal("1.35"),20);
        Apple apple2 =  new Apple(2,"香蕉",new BigDecimal("2.89"),30);
        Apple apple3 =  new Apple(3,"荔枝",new BigDecimal("9.99"),40);

        appleList.add(apple1);
        appleList.add(apple12);
        appleList.add(apple2);
        appleList.add(apple3);

        //List 以ID分组 Map<Integer,List<Apple>>
        Map<Integer, List<Apple>> groupBy = appleList.stream().collect(Collectors.groupingBy(Apple::getId));
        System.out.println("groupBy:"+groupBy);
    	//list转map
    	Map<Integer, Apple> appleMap = appleList.stream().collect(Collectors.toMap(Apple::getId, a -> a,(k1,k2)->k1));
    
                    Map<String, Double> odlMap = oldList.stream().collect(Collectors.toMap(PaiDan2GBean::getCgi, a -> a.getUlTbfSucRate(),(k1, k2)->k1));

        System.out.println(appleMap);

    }
```

### 过滤

```java
public static void main(String[] args) {
        List<Apple> appleList = new ArrayList<>();//存放apple对象集合

        Apple apple1 =  new Apple(1,"苹果1",new BigDecimal("3.25"),10);
        Apple apple12 = new Apple(1,"苹果2",new BigDecimal("1.35"),20);
        Apple apple2 =  new Apple(2,"香蕉",new BigDecimal("2.89"),30);
        Apple apple3 =  new Apple(3,"荔枝",new BigDecimal("9.99"),40);

        appleList.add(apple1);
        appleList.add(apple12);
        appleList.add(apple2);
        appleList.add(apple3);

        //过滤出符合条件的数据
        List<Apple> filterList = appleList.stream().filter(a -> a.getName().equals("香蕉")).collect(Collectors.toList());
        System.err.println("filterList:"+filterList);
    }

```

### 根据某字段求和

``` java
public static void main(String[] args) {
        List<Apple> appleList = new ArrayList<>();//存放apple对象集合

        Apple apple1 =  new Apple(1,"苹果1",new BigDecimal("3.25"),10);
        Apple apple12 = new Apple(1,"苹果2",new BigDecimal("1.35"),20);
        Apple apple2 =  new Apple(2,"香蕉",new BigDecimal("2.89"),30);
        Apple apple3 =  new Apple(3,"荔枝",new BigDecimal("9.99"),40);

        appleList.add(apple1);
        appleList.add(apple12);
        appleList.add(apple2);
        appleList.add(apple3);

        ///计算 总金额
        BigDecimal totalMoney = appleList.stream().map(Apple::getMoney).reduce(BigDecimal.ZERO, BigDecimal::add);
        System.err.println("totalMoney:"+totalMoney.toString());  //totalMoney:17.48
    }
```

### 取交集和差集

```java
List<Integer> accountIdListOne = new ArrayList<>();
        accountIdListOne.add(1);
        accountIdListOne.add(2);
        accountIdListOne.add(3);

        List<Integer> accountIdListTwo = new ArrayList<>();
        accountIdListTwo.add(3);
        accountIdListTwo.add(4);
        accountIdListTwo.add(5);
        accountIdListTwo.add(6);

        // 并集
        List<Integer> accountIdList = accountIdListOne.stream().filter(accountIdListTwo::contains).collect(Collectors.toList());
        System.out.println(accountIdList.toString());

        // 差集(其实不是差集,注意测试)
        List<Integer> noRecoverList = accountIdListTwo.stream().filter(word -> !accountIdListOne.contains(word)).collect(Collectors.toList());
        System.out.println(noRecoverList);
```

### List去重

```java
List<String> collect = list.stream().distinct().collect(Collectors.toList());
```

```java
List<Person> list = ps.stream().collect(Collectors.collectingAndThen(Collectors.toCollection(()
          -> new TreeSet<>(Comparator.comparing(Person::getName))), ArrayList::new));
```

### 每次只取100条进行处理

```java
if(null != paramsList && paramsList.size()>1){
    int numberBatch = 100; //每一次插入的最大行数
    double number = paramsList.size() * 1.0 / numberBatch;
    int n = ((Double)Math.ceil(number)).intValue(); //向上取整
    for(int il = 0; il < n; il++){
        int end = numberBatch * (il + 1);
        if(end > paramsList.size()){
            end = paramsList.size(); //如果end不能超过最大索引值
        }
        fourGKpiPcService.saveFourGKpiPc(paramsList.subList(numberBatch * il , end));//插入数据库
    }
}else {
    log.info("t_oneminute_data138 数据为空！！");
}
```

### list平均分成五分

```java
List<List<Chapter>> partition = Lists.partition(list, 5)
```

### 取出并删除list中的某个元素

```java
public static void main(String[] args) {
    List<Integer> list = new ArrayList(); // 创建一个包含整数类型的列表

    list.add(1); // 添加元素到列表中
    list.add(2);
    list.add(3);
    list.add(4);

    int elementToRemove = 3; // 要移除的元素值为3

    Iterator<Integer> iterator = list.iterator(); // 获取迭代器对象
    while (iterator.hasNext()) {
        Integer num = iterator.next();

        if (num == elementToRemove) {
            iterator.remove(); // 从列表中移除指定元素
        }
    }

    System.out.println("移除后的列表内容：" + list);
}
```

## 关于日期

###  日期格式（2023-05-08T14:37:00.706+08:00）

```java
public static void main(String[] args) {
    /*
    <dependency>
        <groupId>org.apache.cxf.xjc-utils</groupId>
        <artifactId>cxf-xjc-runtime</artifactId>
        <version>3.1.0</version>
    </dependency>
    */
    System.out.println(org.apache.cxf.xjc.runtime.DataTypeAdapter.parseDateTime("2023-05-08T14:37:00.706+08:00"));
    System.out.println(org.apache.cxf.xjc.runtime.DataTypeAdapter.printDateTime(new Date()));

    // java原生
    Calendar c = Calendar.getInstance();
    c.setTime(new Date());
    System.out.println(DatatypeConverter.printDateTime(c));

    System.out.println(DatatypeConverter.parseDateTime("2023-05-08T14:37:00.706+08:00").getTime());
}
```

### 日期与字符串转换

```java
public static void main(String[] args) {
    //创建SimpleDateFormat对象实例并定义好转换格式
    SimpleDateFormat sdf = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss");
    System.out.println("把当前时间转换成字符串：" + sdf.format(new Date()));
    Date date = null;
    try {
        // 注意格式需要与上面一致，不然会出现异常
        date = sdf.parse("2005-12-15 15:30:23");
    } catch (
        ParseException e) {
        e.printStackTrace();
    }
    System.out.println("字符串转换成时间:" + date);
}
```

## 关于hutool

### 加密

#### md5

```java
SecureUtil.md5(charSequence.toString());
```

### http发送get请求

```java
// 最简单的HTTP请求，可以自动通过header等信息判断编码，不区分HTTP和HTTPS
String result1= HttpUtil.get("https://www.baidu.com");

// 当无法识别页面编码的时候，可以自定义请求页面的编码
String result2= HttpUtil.get("https://www.baidu.com", CharsetUtil.CHARSET_UTF_8);

//可以单独传入http参数，这样参数会自动做URL编码，拼接在URL中
HashMap<String, Object> paramMap = new HashMap<>();
paramMap.put("city", "北京");

String result3= HttpUtil.get("https://www.baidu.com", paramMap);
```

### 处理时间格式

#### 支持的格式

```txt
- yyyy/MM/dd HH:mm:ss
- yyyy.MM.dd HH:mm:ss
- yyyy年MM月dd日 HH时mm分ss秒
- yyyy-MM-dd
- yyyy/MM/dd
- yyyy.MM.dd
- HH:mm:ss
- HH时mm分ss秒
- yyyy-MM-dd HH:mm
- yyyy-MM-dd HH:mm:ss.SSS
- yyyyMMddHHmmss
- yyyyMMddHHmmssSSS
- yyyyMMdd
- EEE, dd MMM yyyy HH:mm:ss z
- EEE MMM dd HH:mm:ss zzz yyyy
- yyyy-MM-dd'T'HH:mm:ss'Z'
- yyyy-MM-dd'T'HH:mm:ss.SSS'Z'
- yyyy-MM-dd'T'HH:mm:ssZ
- yyyy-MM-dd'T'HH:mm:ss.SSSZ
- yyyy-MM-dd HH:mm:ss
```

#### 字符串转日期

```java
String dateStr = "2017-03-01";
Date date = DateUtil.parse(dateStr);
Date date2340 = DateUtil.parse(dateStr,"yyyy-MM-dd HH:mm:ss");

//结果 2017/03/01
String format = DateUtil.format(date, "yyyy/MM/dd");

//常用格式的格式化，结果：2017-03-01
String formatDate = DateUtil.formatDate(date);

//结果：2017-03-01 00:00:00
String formatDateTime = DateUtil.formatDateTime(date);

//结果：00:00:00
String formatTime = DateUtil.formatTime(date);
```

#### 时间偏移

##### 计算

```java
String dateStr = "2017-03-01 22:33:23";
Date date = DateUtil.parse(dateStr);

//结果：2017-03-03 22:33:23
Date newDate = DateUtil.offset(date, DateField.DAY_OF_MONTH, 2);

//常用偏移，结果：2017-03-04 22:33:23
DateTime newDate2 = DateUtil.offsetDay(date, 3);

//常用偏移，结果：2017-03-01 19:33:23
DateTime newDate3 = DateUtil.offsetHour(date, -3);
```

##### 简便方法

```java
//昨天
DateUtil.yesterday()
//明天
DateUtil.tomorrow()
//上周
DateUtil.lastWeek()
//下周
DateUtil.nextWeek()
//上个月
DateUtil.lastMonth()
//下个月
DateUtil.nextMonth()
```

#### 计算时间差

```java
String dateStr1 = "2017-03-01 22:33:23";
Date date1 = DateUtil.parse(dateStr1);

String dateStr2 = "2017-04-01 23:33:23";
Date date2 = DateUtil.parse(dateStr2);

//相差一个月，31天
long betweenDay = DateUtil.between(date1, date2, DateUnit.DAY);
System.out.println(betweenDay);
```

## mybatis

### 循坏的使用

```xml
<insert id="saveRrcKpiInfoList" >
    INSERT INTO tableName (ecgi,rrc,alarm_level,alarm_time,create_time) VALUES
    <foreach collection="list" item="item" separator=",">
        (   	
        #{item.ecgi},#{item.rrc},#{item.alarmLevel},#{item.alarmTime},now()
        ) 
    </foreach>
</insert>
```

### 判断的使用

```xml
<!-- 方式一-->
<choose>
    <when test="item.dateTime != null">
        #{item.dateTime}
    </when>
    <otherwise>
        now(),
    </otherwise>
</choose>

<!-- 方式二-->
<update id="updateMatchmakerActivities" parameterType="com.yuanlai.entiy.activity.MatchmakerActivities">
    update matchmaker_activities
    <trim prefix="SET" suffixOverrides=",">
        <if test="activityNo != null">activity_no = #{activityNo},</if>
    </trim>
    where id = #{id}
</update>
```

## mybatis-plus

### 查询条件

```txt
eq 就是 equal等于
ne 就是 not equal不等于
gt 就是 greater than大于
lt 就是 less than小于
ge 就是 greater than or equal 大于等于
le 就是 less than or equal 小于等于
```

## maven

### maven 常用命令

```shell
#重新下载依赖
mvn dependency:purge-local-repository

#查看maven所有依赖
mvn dependency:tree

#打包
mvn package
	#其他命令
	#清除并打包
    mav clean package
    ## 开发环境打包
    mvn clean package -P dev

#清理target下的目录
mav clean

#编译
mvn compile

#安装jar包到本地仓库
mvn install

#部署，这个后面再研究具体怎么整
mvn deploy

#将jar包压入maven
#手动引入本地jar 包
mvn install:install-file -Dfile=你的存放ojdbc6.jar文件的位置 -DgroupId=com.oracle -DartifactId=ojdbc6 -Dversion=版本号 -Dpackaging=jar -DgeneratePom=true

start cmd /k "mvn -s D:\app\other\apache-maven-3.8.6\conf\settings_sino.xml -Dmaven.repo.local=D:\data\mavenData3  install:install-file -Dfile=PdfRenderer-0.9.1.jar -DgroupId=com.kinggrid -DartifactId=PdfRenderer -Dversion=0.9.1 -Dpackaging=jar"


```

### 动态控制配置文件

#### 1、文件结构

```text
├─src
│  └─main
│      ├─java
│      └─resources
│          │  application.yml
│          │
│          ├─dev
│          │      application.yml
│          │
│          ├─prod
│          │      application.yml
│          │
│          └─sit
│                  application.yml
```

2、pom文件

```xml
<dependencies>
</dependencies>

<profiles>
        <profile>
           
            <id>dev</id>
            <properties>
                <package.environment>dev</package.environment>
            </properties>
             <!-- 默认环境 -->
            <activation>
                <activeByDefault>true</activeByDefault>
            </activation>
        </profile>
        <profile>
            <!-- 测试环境 -->
            <id>sit</id>
            <properties>
                <package.environment>sit</package.environment>
            </properties>
        </profile>
        <profile>
            <!-- 生产环境 -->
            <id>prod</id>
            <properties>
                <package.environment>prod</package.environment>
            </properties>
        </profile>
    </profiles>
    <build>
        <resources>
            <resource>
                <directory>${basedir}/src/main/resources/${package.environment}/</directory>
            </resource>
            <!-- 把此路径下的所有的xml都打包进去 要不然无法打包xml -->
             <resource>
				<directory>src/main/resources</directory>
				<includes>
					<include>com/opm/**/*.xml</include>
				</includes>
				<filtering>true</filtering>
             </resource>
        </resources>
        <!--
        <testResources>
            <testResource>
                <directory>${basedir}/src/test/resources/${package.environment}</directory>
            </testResource>
        </testResources>
		-->
    </build>

```

说明：打包时，在maven页签中选择相应的profiles 便可以 或者输入

```shell
## 开发环境打包
mvn clean package -P dev

## 测试环境打包
mvn clean package -P test

## 生产环境打包
mvn clean package -P pro
```



#### 打包好自动替换文件

```xml
<dependencies>
</dependencies>


<profiles>
       <profile>
           <!-- 本地开发环境 -->
      <id>dev</id>
           <properties>
               <package.environment>dev</package.environment>
           </properties>
           <activation>
               <activeByDefault>true</activeByDefault>
           </activation>
       </profile>

       <profile>
           <!-- 生产环境 -->
      <id>prod</id>
           <properties>
               <package.environment>prod</package.environment>
           </properties>
      <build>
               <plugins>
                   <plugin>
                   <artifactId>maven-antrun-plugin</artifactId>
                       <version>1.8</version>
                       <executions>
                           <execution>
                               <phase>package</phase>
                               <goals>
                                   <goal>run</goal>
                               </goals>
                               <configuration>
                                   <tasks>
                                       <!-- 替换class 文件-->
                           <copy file="${basedir}/src/main/resources/test/SaTokenConfigure.class" tofile="${basedir}/target/classes/com/yuanlai/project/common/config/saToken/SaTokenConfigure.class" overwrite="true"/>
                                       <delete dir="${basedir}/target/classes/product"/>
                                   </tasks>
                               </configuration>
                           </execution>
                       </executions>
                   </plugin>
               </plugins>
           </build>
       </profile>
   </profiles>

  <build>
        <resources>  
            <resource>
                <directory>${basedir}/src/main/resources/${package.environment}/</directory>
            </resource>
            <!-- 把此路径下的所有的xml都打包进去 要不然无法打包xml -->
             <resource>
				<directory>src/main/resources</directory>
				<includes>
					<include>com/opm/**/*.xml</include>
				</includes>
				<filtering>true</filtering>
             </resource>
        </resources>
      	<!--
        <testResources>
            <testResource>
                <directory>${basedir}/src/test/resources/${package.environment}</directory>
            </testResource>
        </testResources>
		-->
    </build>
```

### springboot，jar转war-方法一（不推荐）

说明：在idea需要配置tomcat才能启动

1、添加依赖

```xml
<dependency>
   <groupId>org.springframework.boot</groupId>
   <artifactId>spring-boot-starter-tomcat</artifactId>
   <scope>provided</scope>
</dependency>
<dependency>
   <groupId>javax.servlet</groupId>
   <artifactId>javax.servlet-api</artifactId>
   <version>4.0.1</version>
   <scope>provided</scope>
</dependency>
```

2、添加插件

```xml
<plugin>
    <artifactId>maven-war-plugin</artifactId>
    <version>2.6</version>
    <configuration>
    	<!--如果想在没有web.xml文件的情况下构建WAR，请设置为false。-->
    	<failOnMissingWebXml>false</failOnMissingWebXml>
    </configuration>
</plugin>
```

3、修改启动类

```java
@SpringBootApplication
public class XxlJobAdminApplication  extends SpringBootServletInitializer  {

   public static void main(String[] args) {
        SpringApplication.run(XxlJobAdminApplication.class, args);
   }

   @Override
   protected SpringApplicationBuilder configure(SpringApplicationBuilder builder) {
      return builder.sources(XxlJobAdminApplication.class);
   }

}
```

### springboot，jar转war-方法二（推荐）

说明：此种方法可以直接用idea直接启动而不用配置tomcat

说明：参考opmApp项目

- 修改pom

```xml
<!-- 新增 ……-->
<packaging>war</packaging>
```

- 修改启动类

```java
package com.example.testtomcat;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.boot.builder.SpringApplicationBuilder;
import org.springframework.boot.web.servlet.support.SpringBootServletInitializer;

@SpringBootApplication
public class TestTomcatApplication extends SpringBootServletInitializer {

    @Override
    protected SpringApplicationBuilder configure(SpringApplicationBuilder builder) {
        return builder.sources(TestTomcatApplication.class);
    }

    public static void main(String[] args) {
        SpringApplication.run(TestTomcatApplication.class, args);
    }

}
```





### 锁定依赖版本

```xml
<!--在配置文件pom.xml中先声明要使用哪个版本的相应jar包，声明后其他版本的jar包一律不依赖-->
<!--如果是应用在同一个工程内有多个模块时，提取出一个父亲模块来管理子模块共同依赖的 jar 包版本，则子模块相同jar包不需要指定version信息-->
<properties> 
<spring.version>4.2.4.RELEASE</spring.version> 
<hibernate.version>5.0.7.Final</hibernate.version> 
<struts.version>2.3.24</struts.version> </properties> 
</properties> 
<!-- 锁定版本，struts2-2.3.24、spring4.2.4、hibernate5.0.7 --> 
<dependencyManagement> 
	<dependencies> 
		<dependency> 
			<groupId>org.springframework</groupId> 
			<artifactId>spring-context</artifactId>
			<version>${spring.version}</version> 
		</dependency> 
	</dependencies>
 </dependencyManagement>
```

### 移除依赖

```xml
<!--如果我们不想通过 A->B->C>D1 引入 D1 的话，那么我们在声明引入 A 的时候将 D1 排除掉
举个例子：将 zookeeper 的 jline 依赖排除-->
<dependency>
    <groupId>org.apache.hadoop</groupId>
    <artifactId>zookeeper</artifactId>
    <version>3.3.1</version>
    <exclusions>
        <exclusion>
            <groupId>jline</groupId>
            <artifactId>jline</artifactId>
        </exclusion>
    </exclusions>
</dependency>

1、第一声明优先原则
#在pom.xml配置文件中，如果有两个名称相同版本不同的依赖声明，那么先写的会生效。
所以，先声明自己要用的版本的jar包即可。
2、最短路径优先
直接依赖优先于传递依赖，如果传递依赖的jar包版本冲突了，那么可以自己声明一个指定版本的依赖jar，即可解决冲突。



<!--例子-->
 <!-- SpringBoot整合zookeeper客户端 -->
<dependency>
    <groupId>org.springframework.cloud</groupId>
    <artifactId>spring-cloud-starter-zookeeper-discovery</artifactId>
    <!--先排除自带的zookeeper3.5.3-->
    <exclusions>
        <exclusion>
            <groupId>org.apache.zookeeper</groupId>
            <artifactId>zookeeper</artifactId>
        </exclusion>
    </exclusions>
</dependency>
<!--添加zookeeper3.4.9版本-->
<dependency>
    <groupId>org.apache.zookeeper</groupId>
    <artifactId>zookeeper</artifactId>
    <version>3.4.9</version>
</dependency>
```



### 指定包名

```xml
<build>
    <!-- 指定包名 -->
    <finalName>wangye</finalName>
    <plugins>
        <plugin>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-maven-plugin</artifactId>
            <configuration>
                <excludes>
                    <exclude>
                        <groupId>org.projectlombok</groupId>
                        <artifactId>lombok</artifactId>
                    </exclude>
                </excludes>
            </configuration>
        </plugin>
    </plugins>
</build>
```

### 标签含义

``` xml
<!-- 依赖只在测试阶段使用 -->
<scope>test</scope>
```

### 插件

#### 资源插件		

``` xml

```

### seting文件

```xml
<?xml version="1.0" encoding="UTF-8"?>

<settings xmlns="http://maven.apache.org/SETTINGS/1.0.0"
          xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
          xsi:schemaLocation="http://maven.apache.org/SETTINGS/1.0.0 http://maven.apache.org/xsd/settings-1.0.0.xsd">

  <localRepository>D:\maven3\cloud</localRepository>

  <pluginGroups>
  </pluginGroups>

  <proxies>
  </proxies>

  <servers>
  </servers>
  
  <mirrors>	 
	 <mirror>
		<id>alimaven</id>
		<mirrorOf>central</mirrorOf>
		<name>aliyun maven</name>
		<url>http://maven.aliyun.com/nexus/content/repositories/central/</url>
	</mirror>
  </mirrors>

  <profiles>
  </profiles>

</settings>

```

### 问题

#### idea无法下载依赖

```sh
#idea->seting->maven->import->VM 中添加 和
#idea->seting->maven->Runner->VM 中添加
-Dmaven.wagon.http.ssl.insecure=true -Dmaven.wagon.http.ssl.allowall=true -Dmaven.wagon.http.ssl.ignore.validity.dates=true -DarchetypeCatalog=internal
```

#### idea无法下载

- 报错信息

  ```txt
  Could not transfer artifact …………………….yar
  ```

- 解决

  ```txt
  
  ```

## tomcat

### 配置文件解析

```xml
<?xml version="1.0" encoding="UTF-8"?>

<Server port="8005" shutdown="SHUTDOWN">
  <Listener className="org.apache.catalina.startup.VersionLoggerListener" />

  <Listener className="org.apache.catalina.core.AprLifecycleListener" SSLEngine="on" />

  <Listener className="org.apache.catalina.core.JreMemoryLeakPreventionListener" />
  <Listener className="org.apache.catalina.mbeans.GlobalResourcesLifecycleListener" />
  <Listener className="org.apache.catalina.core.ThreadLocalLeakPreventionListener" />

  <GlobalNamingResources>

    <Resource name="UserDatabase" auth="Container"
              type="org.apache.catalina.UserDatabase"
              description="User database that can be updated and saved"
              factory="org.apache.catalina.users.MemoryUserDatabaseFactory"
              pathname="conf/tomcat-users.xml" />
  </GlobalNamingResources>
    
  <Service name="Catalina">
      
    <Connector port="8080" protocol="HTTP/1.1"
               connectionTimeout="20000"
               redirectPort="8443" />
    
    <Engine name="Catalina" defaultHost="localhost">

      
      <Realm className="org.apache.catalina.realm.LockOutRealm">
       
        <Realm className="org.apache.catalina.realm.UserDatabaseRealm"
               resourceName="UserDatabase"/>
      </Realm>

      <Host name="localhost"  appBase="webapps"
            unpackWARs="true" autoDeploy="true">

        <!--path:项目的服务名称 http://localhost:8080/abc/doc.html -->
        <!--docBase:指向webapps文件夹下面的 解压好了的项目文件  apache-tomcat-8.5.75-test\webapps\task -->
        <!--reloadable:是否可重新加载 -->
        <Context path="/abc" docBase="task" reloadable="false" />
		
        <Valve className="org.apache.catalina.valves.AccessLogValve" directory="logs"
               prefix="localhost_access_log" suffix=".txt"
               pattern="%h %l %u %t &quot;%r&quot; %s %b" /> <!-- tomcat日志的打印规则 -->

      </Host>
    </Engine>
  </Service>
</Server>

```

### tomcat日志乱码

```
修改conf文件夹下的logging.properties
将所有的UTF-8 改为GBK 或者其他的
```



## GIT

### 刷新.gitignore

```sh
# 有时候需要突然修改 .gitignore 文件，随后要立即生效
 #清除缓存 
git rm -r --cached .
# 强制清除缓存（二选一）
git rm -r -f --cached .


# 重新提交
git add .
#提交和注释  
git commit -m "update .gitignore" 
#可选，如果需要同步到remote上的话
git push origin master
```

## 中文文档

### consul

```http
https://www.springcloud.cc/spring-cloud-consul.html
```

### spring版本对应

```http
https://start.spring.io/actuator/info
```

### springcloud

```http
https://www.bookstack.cn/read/spring-cloud-docs/docs-project-QuickStart.md
```

### springboot

```http
http://felord.cn/_doc/_springboot/2.1.5.RELEASE/_book/
```

## 正则表达式

### 判断时间格式 YYYY-MM-DD

```java
String datePattern = "\\d{4}-\\d{2}-\\d{2}";
Pattern pattern = Pattern.compile(datePattern);
Matcher matcher = pattern.matcher("2023-02-02");
if (!matcher.matches()){
    sout("开始时间格式有误")
}
```



# 不常用

## 乱码处理

注意：UTF8和GBK互相转换时，会出现转换失败的情况，比如UTF8转成了GBK之后，无法正确的再转回UTF8。这种转码不可逆的情况，暂时无法解决，最好的方法是保持整个架构的编码一致！

### 各种乱码的样子

```txt
编码： GBK ==> GBK = 对啊这就是一个测试啊逗比
编码： GBK ==> UTF-8 = �԰������һ�����԰�����
编码： GBK ==> GB2312 = 对啊这就是一个测试啊逗比
编码： GBK ==> ISO-8859-1 = ¶Ô°¡Õâ¾ÍÊÇÒ»¸ö²âÊÔ°¡¶º±È

编码： UTF-8 ==> GBK = 瀵瑰晩杩欏氨鏄竴涓祴璇曞晩閫楁瘮
编码： UTF-8 ==> UTF-8 = 对啊这就是一个测试啊逗比
编码： UTF-8 ==> GB2312 = 瀵瑰��杩�灏辨��涓�涓�娴�璇�����姣�
编码： UTF-8 ==> ISO-8859-1 = å¯¹åè¿å°±æ¯ä¸ä¸ªæµè¯åéæ¯

编码： GB2312 ==> GBK = 对啊这就是一个测试啊逗比
编码： GB2312 ==> UTF-8 = �԰������һ�����԰�����
编码： GB2312 ==> GB2312 = 对啊这就是一个测试啊逗比
编码： GB2312 ==> ISO-8859-1 = ¶Ô°¡Õâ¾ÍÊÇÒ»¸ö²âÊÔ°¡¶º±È

编码： ISO-8859-1 ==> GBK = ????????????
编码： ISO-8859-1 ==> UTF-8 = ????????????
编码： ISO-8859-1 ==> GB2312 = ????????????
编码： ISO-8859-1 ==> ISO-8859-1 = ????????????
```

### 转码

```java

import java.io.UnsupportedEncodingException;
 
/**
 * 判断字符编码
 *
 * @author guyinyihun
 */
public class CharacterCodingUtil {
 
 
    private final static String ENCODE = "GBK";
 
    /**
     * 判断是否为ISO-8859-1
     *
     * @return
     */
    public static boolean checkISO(String str) {
        boolean flag = java.nio.charset.Charset.forName("ISO-8859-1").newEncoder().canEncode(str);
        return flag;
    }
 
    /**
     * 判断是否为UTF-8
     *
     * @return
     */
    public static boolean checkUTF(String str) {
 
        boolean flag = java.nio.charset.Charset.forName("UTF-8").newEncoder().canEncode(str);
        return flag;
    }
 
    public static boolean checkUnicode(String str) {
 
        boolean flag = java.nio.charset.Charset.forName("unicode").newEncoder().canEncode(str);
        return flag;
    }
 
    /**
     * <p>
     * Title: getEncoding
     * </p>
     * <p>
     * Description: 判断字符编码
     * </p>
     *
     * @param str
     * @return
     */
    public static String getEncoding(String str) {
        String encode = "unicode";
        try {
            if (str.equals(new String(str.getBytes(encode), encode))) {
                String s = encode;
                return s;
            }
        } catch (Exception exception) {
        }
        encode = "ISO-8859-1";
        try {
            if (str.equals(new String(str.getBytes(encode), encode))) {
                String s1 = encode;
                return s1;
            }
        } catch (Exception exception1) {
        }
        encode = "UTF-8";
        try {
            if (str.equals(new String(str.getBytes(encode), encode))) {
                String s2 = encode;
                return s2;
            }
        } catch (Exception exception2) {
        }
        encode = "GBK";
        try {
            if (str.equals(new String(str.getBytes(encode), encode))) {
                String s3 = encode;
                return s3;
            }
        } catch (Exception exception3) {
        }
        return "";
    }
 
    /**
     * <p>
     * Title: isoToutf8
     * </p>
     * <p>
     * Description: ISO-8859-1 编码 转 UTF-8
     * </p>
     *
     * @param str
     * @return
     */
    public static String isoToutf8(String str) {
        try {
            return new String(str.getBytes("ISO-8859-1"), "UTF-8");
        } catch (UnsupportedEncodingException e) {
            e.printStackTrace();
            return str;
        }
    }
 
    /**
     * <p>
     * Title: utf8Toiso
     * </p>
     * <p>
     * Description: UTF-8 编码 转 ISO-8859-1
     * </p>
     *
     * @param str
     * @return
     */
    public static String utf8Toiso(String str) {
        try {
            return new String(str.getBytes("utf-8"), "iso-8859-1");
        } catch (UnsupportedEncodingException e) {
            e.printStackTrace();
            return str;
        }
    }
 
    /**
     * <p>Title: unicodeToCn</p>
     * <p>Description: unicode 转 中文</p>
     *
     * @param unicode
     * @return
     */
    public static String unicodeToCn(String unicode) {
        /** 以 \ u 分割，因为java注释也能识别unicode，因此中间加了一个空格 */
        String[] strs = unicode.split("\\\\u");
        String returnStr = "";
        // 由于unicode字符串以 \ u 开头，因此分割出的第一个字符是""。
        for (int i = 1; i < strs.length; i++) {
            returnStr += (char) Integer.valueOf(strs[i], 16).intValue();
        }
        return returnStr;
    }
 
 
    /**
     * <p>Title: cnToUnicode</p>
     * <p>Description: 中文转 unicode</p>
     *
     * @param cn
     * @return
     */
    public static String cnToUnicode(String cn) {
        char[] chars = cn.toCharArray();
        String returnStr = "";
        for (int i = 0; i < chars.length; i++) {
            returnStr += "\\u" + Integer.toString(chars[i], 16);
        }
        return returnStr;
    }
 
    /**
     * URL 解码
     *
     * @return String
     * @author lifq
     * @date 2015-3-17 下午04:09:51
     */
    public static String getURLDecoderString(String str) {
        String result = "";
        if (null == str) {
            return "";
        }
        try {
            result = java.net.URLDecoder.decode(str, ENCODE);
        } catch (UnsupportedEncodingException e) {
            e.printStackTrace();
        }
        return result;
    }
 
    /**
     * URL 转码
     *
     * @return String
     * @author lifq
     * @date 2015-3-17 下午04:10:28
     */
    public static String getURLEncoderString(String str) {
        String result = "";
        if (null == str) {
            return "";
        }
        try {
            result = java.net.URLEncoder.encode(str, ENCODE);
        } catch (UnsupportedEncodingException e) {
            e.printStackTrace();
        }
        return result;
    }
 
}

```



### 让java的方法的参数，可有可无

在Java中，如果你想让方法的参数是可选的，有几种方式可以实现：

1. **使用重载（Overloading）**:
   重载是Java提供的一种特性，允许同一个类中有多个同名但参数列表不同的方法。你可以为方法提供不同数量的参数，从而允许调用者选择传递哪些参数。

```java
public class MyClass {  
    public void myMethod() {  
        // 无参数的实现  
    }  
  
    public void myMethod(String param1) {  
        // 一个参数的实现  
    }  
  
    public void myMethod(String param1, int param2) {  
        // 两个参数的实现  
    }  
}
```

使用这种方式，调用者可以选择调用`myMethod()`、`myMethod("someString")`或`myMethod("someString", 123)`。

2. **使用默认参数值（从Java 8开始）**:
   在Java 8及更高版本中，你可以在方法定义时为参数提供默认值。这样，调用者在调用方法时可以省略这些参数，它们将使用默认值。

```java
public class MyClass {  
    public void myMethod(String param1 = "defaultValue", int param2 = 0) {  
        // 方法实现  
    }  
}
```

在这个例子中，调用者可以选择调用`myMethod()`、`myMethod("customValue")`或`myMethod("customValue", 456)`。省略的参数将使用默认值。

3. **使用Java的可变参数（Varargs）**:
   可变参数允许你传递任意数量的参数给方法。这在处理不确定数量的参数时非常有用。

```java
public class MyClass {  
    public void myMethod(String... params) {  
        // 方法实现，可以使用params数组来处理参数  
    }  
}
```

在这个例子中，调用者可以传递任意数量的字符串参数给`myMethod()`，例如`myMethod()`、`myMethod("param1")`或`myMethod("param1", "param2", "param3")`。

4. **使用Java的Optional类（从Java 8开始）**:
   `Optional`是一个可以为null的容器对象。如果方法的参数是可选的，并且你希望明确地表示它是否存在，可以使用`Optional`。

```java
import java.util.Optional;  
  
public class MyClass {  
    public void myMethod(Optional<String> param) {  
        // 方法实现，可以使用param.isPresent()来检查参数是否存在  
    }  
}
```

在这个例子中，调用者可以选择传递一个`Optional.of("someValue")`或`Optional.empty()`给`myMethod()`。

每种方法都有其适用的场景，你可以根据具体需求选择最合适的方式。通常，如果参数是真正可选的，并且没有默认值，使用重载或可变参数可能更合适。如果参数有默认值，使用默认参数值可能更简洁。如果需要明确地表示参数是否存在，可以考虑使用`Optional`。

## 其他

### 定时删除电脑文件

```java
 public void deleteFile() throws Exception{
        String filePath = ToolsUtils.getFtpInfo("path_215");
        filePath =filePath.substring(0,filePath.length()-1);
        List<String> list = new ArrayList<>();
        if(null!=filePath&&!"".equals(filePath)){
            File file = new File(filePath);
            //判断文件或目录是否存在
            if(!file.exists()){
                log.info("【"+filePath + " not exists】");
            }
            //获取该文件夹下所有的文件
            File[] fileArray= file.listFiles();
            File fileName = null;
            if(null == fileArray){
                log.error("查询出来的文件为空");
                return;
            }
            for(int i =0;i<fileArray.length;i++){
                fileName = fileArray[i];
                //判断此文件是否存在
                if(fileName.isDirectory()){
                    log.info("【目录："+fileName.getName()+"】");
                }else{
                    Path path= Paths.get(fileName.getPath());
                    BasicFileAttributeView basicview= Files.getFileAttributeView(path, BasicFileAttributeView.class, LinkOption.NOFOLLOW_LINKS );
                    BasicFileAttributes attr = basicview.readAttributes();
                    // 两天前
                    Long date2DayAgo =  DateUtil.offsetDay(new Date(), 3).getTime();
                    Long creatTime  = attr.creationTime().toMillis();
                    // 删除两天前的文件数据
                    if (creatTime <= date2DayAgo){
                        fileName.delete();
                        list.add(fileName.getName());
                    }
                }
            }
            log.info("删除4g5g一分钟文件："+list);
        }
    }
```

### ftp工具类

```java
package com.jfkj.ihandle.task.roamin;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.net.SocketException;
import java.text.ParseException;
import java.util.ArrayList;
import java.util.List;

import org.apache.commons.net.ftp.FTPClient;
import org.apache.commons.net.ftp.FTPFile;

/**
 * @describe 读取FTP上的文件
 * @auto zhangling
 * @date 2013-11-18 下午4:07:34
 */
public class FtpUtils {

    private FTPClient ftpClient;
    private String strencoding;
    private String ip = "192.168.1.249"; // 服务器IP地址
    private String userName = "anonymous"; // 用户名
    private String userPwd = ""; // 密码
    private int port = 21; // 端口号
    private String path = "Alam/192.168.1.229/"; // 读取文件的存放目录

    /**
     * init ftp servere
     */
    public FtpUtils() {
        this.reSet();
    }

    public void reSet() {
// 以当前系统时间拼接文件名
        strencoding = "GBK";
        this.connectServer(ip, port, userName, userPwd, path);
    }

    /**
     * @param ip
     * @param port
     * @param userName
     * @param userPwd
     * @param path
     * @throws SocketException
     * @throws IOException function:连接到服务器
     */
    public void connectServer(String ip, int port, String userName, String userPwd, String path) {
        ftpClient = new FTPClient();
        try {
// 连接
            ftpClient.connect(ip, port);
// 登录
            ftpClient.login(userName, userPwd);
            if (path != null && path.length() > 0) {
// 跳转到指定目录
                ftpClient.changeWorkingDirectory(path);
            }
        } catch (SocketException e) {
            e.printStackTrace();
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    /**
     * @throws IOException function:关闭连接
     */
    public void closeServer() {
        if (ftpClient.isConnected()) {
            try {
                ftpClient.logout();
                ftpClient.disconnect();
            } catch (IOException e) {
                e.printStackTrace();
            }
        }
    }

    /**
     * @param path
     * @return function:读取指定目录下的文件名
     * @throws IOException
     */
    public List<String> getFileList(String path) throws ParseException {
        List<String> fileLists = new ArrayList<String>();
// 获得指定目录下所有文件名
        FTPFile[] ftpFiles = null;
        try {
            ftpFiles = ftpClient.listFiles(path);
        } catch (IOException e) {
            e.printStackTrace();
        }
        for (int i = 0; ftpFiles != null && i < ftpFiles.length; i++) {
            FTPFile file = ftpFiles[i];
            if (file.isFile()) {
                System.out.println("文件夹下面的文件====="+file.getName());
                fileLists.add(file.getName());
            }else if(file.isDirectory()){
                System.out.println("文件夹名称为====="+file.getName());
                List<String> childLists = getFileList(path + file.getName()+"/");
                for(String childFileName : childLists){
                    fileLists.add(childFileName);
                    String fileType = childFileName.substring(childFileName.lastIndexOf(".")+1,
                                                              childFileName.length());
                    System.out.println("文件类型为："+fileType);
                    FtpUtils ftp = new FtpUtils();
                    if(fileType.equals("txt")){
                        System.out.println("文件名为："+childFileName);
                        String content = "";
                        content = ftp.readFile(path + file.getName()+"/"+childFileName);
                        System.out.println("文件内容为："+content);
                    }
                }
            }
        }
        return fileLists;
    }

    /**
     * @param fileName
     * @return function:从服务器上读取指定的文件
     * @throws ParseException
     * @throws IOException
     */
    public String readFile(String fileName) throws ParseException {
        InputStream ins = null;
        StringBuilder builder = null;
        try {
// 从服务器上读取指定的文件
            ins = ftpClient.retrieveFileStream(fileName);
            BufferedReader reader = new BufferedReader(new InputStreamReader(ins, strencoding));
            String line;
            builder = new StringBuilder(150);
            while ((line = reader.readLine()) != null) {
                System.out.println(line);
                builder.append(line);
            }
            reader.close();
            if (ins != null) {
                ins.close();
            }
// 主动调用一次getReply()把接下来的226消费掉. 这样做是可以解决这个返回null问题
            ftpClient.getReply();
        } catch (IOException e) {
            e.printStackTrace();
        }
        return builder.toString();
    }

    /**
     * @param fileName function:删除文件
     */
    public void deleteFile(String fileName) {
        try {
            ftpClient.deleteFile(fileName);
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    /**
     * @param args
     * @throws ParseException
     */
    public static void main(String[] args) throws ParseException {
        FtpUtils ftp = new FtpUtils();
        List<String> str = ftp.getFileList("");
        System.out.println("目录下包含的文件名称为："+str);
        for(String a : str){
            System.out.println("文件名为："+a);
        }
        ftp.closeServer();
    }
}
```

### 防跨域配置类

```java
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.web.cors.CorsConfiguration;
import org.springframework.web.cors.reactive.CorsWebFilter;
import org.springframework.web.cors.reactive.UrlBasedCorsConfigurationSource;
import org.springframework.web.util.pattern.PathPatternParser;

@Configuration
public class CorsConfig {

    //解决跨域
    @Bean
    public CorsWebFilter corsWebFilter() {
        CorsConfiguration config = new CorsConfiguration();
        config.addAllowedMethod("*");
        config.addAllowedOrigin("*");
        config.addAllowedHeader("*");

        UrlBasedCorsConfigurationSource source = new UrlBasedCorsConfigurationSource(new PathPatternParser());
        source.registerCorsConfiguration("/**",config);

        return new CorsWebFilter(source);
    }
}

```

### DES加密

```java
import org.apache.commons.codec.binary.Base64;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.security.Key;


import javax.crypto.Cipher;
import javax.crypto.SecretKeyFactory;
import javax.crypto.spec.DESKeySpec;


/**
 * 加密解密工具包
 */
public class CyptoUtils {

    public static final String ALGORITHM_DES = "DES/ECB/PKCS5Padding";
    private static Logger logger = LoggerFactory.getLogger(CyptoUtils.class);


    /**
     * DES算法，加密
     *
     * @param data 待加密字符串
     * @param key  加密私钥，长度不可以小于8位
     * @return 加密后的字节数组，一般结合Base64编码使用
     * @throws Exception
     */
    public static String encode(String key,String data) {
        if(data == null)
            return null;
        try{
            DESKeySpec dks = new DESKeySpec(key.getBytes());
            SecretKeyFactory keyFactory = SecretKeyFactory.getInstance("DES");
            //key的长度不可以小于8位字节
            Key secretKey = keyFactory.generateSecret(dks);
            Cipher cipher = Cipher.getInstance(ALGORITHM_DES);
            //IvParameterSpec iv = new IvParameterSpec("12345678".getBytes());
            //AlgorithmParameterSpec paramSpec = iv;
            cipher.init(Cipher.ENCRYPT_MODE, secretKey);
            byte[] bytes = cipher.doFinal(data.getBytes());
            return byte2hex(bytes);
        }catch(Exception e){
            e.printStackTrace();
            return data;
        }
    }

    /**
     * DES算法，解密
     *
     * @param data 待解密字符串
     * @param key  解密私钥，长度不可以小于8位
     * @return 解密后的字节数组
     * @throws Exception 异常
     */
    public static String decode(String key,String data) throws Exception {
        if(data == null)
            return null;
        try {
            DESKeySpec dks = new DESKeySpec(key.getBytes());
            SecretKeyFactory keyFactory = SecretKeyFactory.getInstance("DES");
            //key的长度不可以小于8位字节
            Key secretKey = keyFactory.generateSecret(dks);
            Cipher cipher = Cipher.getInstance(ALGORITHM_DES);
            cipher.init(Cipher.DECRYPT_MODE, secretKey);
            byte[] d = null;
            String  str = null;
            try {
                d = cipher.doFinal(hex2byte(data.getBytes()));
                str = new String(d);
            }catch (Exception e){
                logger.error("DES解密报错->"+e.getMessage());
                return null;
            }

            return str;
            //return Base64.encode(data.getBytes());
        } catch (Exception e){
            e.printStackTrace();
            return data;
        }
    }

    /**
     * 二行制转字符串
     * @param b
     * @return
     */
    private static String byte2hex(byte[] b) {
        /*StringBuilder hs = new StringBuilder();
        String stmp;
        for (int n = 0; b!=null && n < b.length; n++) {
            stmp = Integer.toHexString(b[n] & 0XFF);
            if (stmp.length() == 1)
                hs.append('0');
            hs.append(stmp);
        }
        return hs.toString().toUpperCase();*/
        return Base64.encodeBase64String(b);
    }

    private static byte[] hex2byte(byte[] b) {
        byte[] b2 = org.apache.commons.codec.binary.Base64.decodeBase64(b);
        /*if((b.length%2)!=0)
            throw new IllegalArgumentException();
        byte[] b2 = new byte[b.length/2];
        for (int n = 0; n < b.length; n+=16) {
            String item = new String(b,n,2);
            b2[n/2] = (byte)Integer.parseInt(item,2);
        }*/
        return b2;
    }


    public static void main(String[] args) throws Exception {
        String a = encode("4SF6BJ3D8TDOT8NOCZ8T7P1K","wy_yixiaoqin");
        System.out.println(a);
        System.out.println(decode("4SF6BJ3D8TDOT8NOCZ8T7P1K","uUSd6LuoXsGAXxtoCFleBoEdzOYxHJeU"));
    }
}

```

### 生成验证码图片

```java
import java.awt.Color;
import java.awt.Font;
import java.awt.Graphics;
import java.awt.Graphics2D;
import java.awt.RenderingHints;
import java.awt.geom.AffineTransform;
import java.awt.image.BufferedImage;
import java.io.ByteArrayOutputStream;
import java.io.File;
import java.io.FileOutputStream;
import java.io.IOException;
import java.util.Arrays;
import java.util.Random;
import javax.imageio.ImageIO;
import sun.misc.BASE64Decoder;
import sun.misc.BASE64Encoder;

/**
     * Base64编码的验证码图片
     * @param w
     * @param h
     * @param code
     * @return
     * @throws Exception
     */
public static String imageToBase64(int w, int h, String code) throws Exception {
    int verifySize = code.length();
    BufferedImage image = new BufferedImage(w, h, BufferedImage.TYPE_INT_RGB);
    Random rand = new Random();
    Graphics2D g2 = image.createGraphics();
    g2.setRenderingHint(RenderingHints.KEY_ANTIALIASING, RenderingHints.VALUE_ANTIALIAS_ON);
    Color[] colors = new Color[5];
    Color[] colorSpaces = new Color[] { Color.WHITE, Color.CYAN, Color.GRAY, Color.LIGHT_GRAY, Color.MAGENTA,
                                       Color.ORANGE, Color.PINK, Color.YELLOW };
    float[] fractions = new float[colors.length];
    for (int i = 0; i < colors.length; i++) {
        colors[i] = colorSpaces[rand.nextInt(colorSpaces.length)];
        fractions[i] = rand.nextFloat();
    }
    Arrays.sort(fractions);

    g2.setColor(Color.GRAY);// 设置边框色
    g2.fillRect(0, 0, w, h);

    Color c = getRandColor(200, 250);
    g2.setColor(c);// 设置背景色
    g2.fillRect(0, 2, w, h - 4);

    // 绘制干扰线
    Random random = new Random();
    g2.setColor(getRandColor(160, 200));// 设置线条的颜色
    for (int i = 0; i < 20; i++) {
        int x = random.nextInt(w - 1);
        int y = random.nextInt(h - 1);
        int xl = random.nextInt(6) + 1;
        int yl = random.nextInt(12) + 1;
        g2.drawLine(x, y, x + xl + 40, y + yl + 20);
    }

    // 添加噪点
    float yawpRate = 0.05f;// 噪声率
    int area = (int) (yawpRate * w * h);
    for (int i = 0; i < area; i++) {
        int x = random.nextInt(w);
        int y = random.nextInt(h);
        int rgb = getRandomIntColor();
        image.setRGB(x, y, rgb);
    }

    shear(g2, w, h, c);// 使图片扭曲

    g2.setColor(getRandColor(100, 160));
    int fontSize = h - 4;
    Font font = new Font("Arial", Font.ITALIC, fontSize);
    g2.setFont(font);
    char[] chars = code.toCharArray();
    for (int i = 0; i < verifySize; i++) {
        AffineTransform affine = new AffineTransform();
        affine.setToRotation(Math.PI / 4 * rand.nextDouble() * (rand.nextBoolean() ? 1 : -1),
                             (w / verifySize) * i + fontSize / 2, h / 2);
        g2.setTransform(affine);
        g2.drawChars(chars, i, 1, ((w - 10) / verifySize) * i + 5, h / 2 + fontSize / 2 - 10);
    }
    g2.dispose();
    ByteArrayOutputStream baos = new ByteArrayOutputStream();
    ImageIO.write(image, "gif", baos);
    return new BASE64Encoder().encode(baos.toByteArray());
}
```

### 内网穿透

#### ngrok国际版

```cmd
# 如下网址可以获取token，用github登录
ngrok.com
# 打开软件后输入命令
#私有token  22IjmrmeQMpMB5u59GG7ThfyPAf_6mhU6yiKfZt3PapjwLEiY
ngrok authtoken 22IjmrmeQMpMB5u59GG7ThfyPAf_6mhU6yiKfZt3PapjwLEiY
ngrok http 8080
```

#### 闪库

# 控制电脑程序

## 浏览器

### 打开默认浏览器

```java
Desktop.getDesktop().browse(new URI("https://www.baidu.com"));
```

