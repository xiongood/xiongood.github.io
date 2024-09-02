---
title: 数据库连接池-druid
img: https://pub-b24cf0a8c1f14e9386435977aa464959.r2.dev/img/20230816111833.png
categories:
 - 后端
tags:
 - java
 - druid
---

## springboot默认连接池(Hikari)

```yaml
server:
  port: 8080
spring:
  hikari:
    connection-timeout: 60000 #连接超时时间：毫秒，小于250毫秒，否则被重置为默认值30秒
    idle-timeout: 500000 #空闲连接超时时间，默认值600000（10分钟），大于等于max-lifetime且max-lifetime>0，会被重置为0；不等于0且小于10秒，会被重置为10秒
    max-lifetime: 540000 #连接最大存活时间，不等于0且小于30秒，会被重置为默认值30分钟.设置应该比mysql设置的超时时间短
    maximum-pool-size: 10 #最大连接数，小于等于0会被重置为默认值10；大于零小于1会被重置为minimum-idle的值
    minimum-idle: 5 # 最小空闲连接，默认值10，小于0或大于maximum-pool-size，都会重置为maximum-pool-size
    auto-commit: true               # 自动提交
    pool-name: DateSourceHikariCP   # 连接池名字
    connection-test-query: SELECT 1

  datasource:
    url: jdbc:mysql://mysql.sqlpub.com:3306/java0417?serverTimezone=UTC&useUnicode=true&characterEncoding=utf-8&AllowPublicKeyRetrieval=True
    username: java0417
    password: f345c26699a412e2


mybatis-plus:
  mapper-locations: mapper/*.xml
  configuration:
    log-impl: org.apache.ibatis.logging.stdout.StdOutImpl
  type-aliases-package: com.example.xiong.entity

```

## druid 的使用

### pom

```xml
<dependency>
    <groupId>com.alibaba</groupId>
    <artifactId>druid-spring-boot-starter</artifactId>
    <version>1.2.17</version>
</dependency>
```

### 默认配置

```yaml
server:
  port: 8080

spring:
  datasource:
    druid:
      type: com.alibaba.druid.pool.DruidDataSource #数据库连接中修改数据源类型
      # druid参数调优（可选）,若配置如下参数则必须手动添加配置类
      initialSize: 5 # 初始化大小，最小，最大
      minIdle: 5
      maxActive: 10
      maxWait: 60000 # 配置获取连接等待超时的时间
      minEvictableIdleTimeMillis: 300000 # 配置一个连接在池中最小生存的时间，单位是毫秒
      timeBetweenEvictionRunsMillis: 60000  # 配置间隔多久才进行一次检测，检测需要关闭的空闲连接，单位是毫秒
      # 打开PSCache，并且指定每个连接上PSCache的大小
      poolPreparedStatements: true
      # 测试连接
      testOnBorrow: false
      testOnReturn: false
      testWhileIdle: true
      ## 配置监控统计拦截的filters
      # asyncInit是1.1.4中新增加的配置，如果有initialSize数量较多时，打开会加快应用启动时间
      asyncInit: true
      filters: stat,config
      maxPoolPreparedStatementPerConnectionSize: 20
      useGlobalDataSourceStat: true
      connectionProperties: druid.stat.mergeSql=true;druid.stat.slowSqlMillis=500
      ## 数据源
      driver-class-name: com.mysql.cj.jdbc.Driver
      url: jdbc:mysql://mysql.sqlpub.com:3306/java0417?serverTimezone=UTC&useUnicode=true&characterEncoding=utf-8&AllowPublicKeyRetrieval=True
      username: java0417
      password: f345c26699a412e2


mybatis-plus:
  mapper-locations: mapper/*.xml
  configuration:
    log-impl: org.apache.ibatis.logging.stdout.StdOutImpl
  type-aliases-package: com.example.xiong.entity

```

### 手动配置

#### yml

```yaml
server:
  port: 8889

spring:
  datasource:
    type: com.alibaba.druid.pool.DruidDataSource #数据库连接中修改数据源类型
    # druid参数调优（可选）,若配置如下参数则必须手动添加配置类
    initialSize: 5 # 初始化大小，最小，最大
    minIdle: 5
    maxActive: 10
    maxWait: 60000 # 配置获取连接等待超时的时间
    minEvictableIdleTimeMillis: 300000 # 配置一个连接在池中最小生存的时间，单位是毫秒
    timeBetweenEvictionRunsMillis: 60000  # 配置间隔多久才进行一次检测，检测需要关闭的空闲连接，单位是毫秒
    # 打开PSCache，并且指定每个连接上PSCache的大小
    poolPreparedStatements: true
    # 测试连接
    testOnBorrow: false
    testOnReturn: false
    testWhileIdle: true
    ## 配置监控统计拦截的filters
    # asyncInit是1.1.4中新增加的配置，如果有initialSize数量较多时，打开会加快应用启动时间
    asyncInit: true
    filters: stat,config
    maxPoolPreparedStatementPerConnectionSize: 20
    useGlobalDataSourceStat: true
    connectionProperties: druid.stat.mergeSql=true;druid.stat.slowSqlMillis=500
    ## 数据源
    driver-class-name: com.mysql.cj.jdbc.Driver
    url: jdbc:mysql://mysql.sqlpub.com:3306/java0417?serverTimezone=UTC&useUnicode=true&characterEncoding=utf-8&AllowPublicKeyRetrieval=True
    username: java0417
    password: f345c26699a412e2


mybatis-plus:
  mapper-locations: mapper/*.xml
  configuration:
    log-impl: org.apache.ibatis.logging.stdout.StdOutImpl
  type-aliases-package: com.example.xiong.entity

```

#### 新增两个配置类

- 第一个

```java
package com.example.xiong.conf;

import com.alibaba.druid.pool.DruidDataSource;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.context.annotation.Primary;

import java.sql.SQLException;

/**
 * Druid连接池调优配置信息：只有配置数据库连接池调优信息才需要该类
 *
 *
 * @author wyj
 * @date 2022/8/16 15:54
 */
@Configuration
public class DruidConfig {
    private Logger logger = LoggerFactory.getLogger(DruidConfig.class);

    @Value("${spring.datasource.url}")
    private String dbUrl;

    @Value("${spring.datasource.username}")
    private String username;

    @Value("${spring.datasource.password}")
    private String password;

    @Value("${spring.datasource.driver-class-name}")
    private String driverClassName;

    @Value("${spring.datasource.initial-size}")
    private int initialSize;

    @Value("${spring.datasource.min-idle}")
    private int minIdle;

    @Value("${spring.datasource.max-active}")
    private int maxActive;

    @Value("${spring.datasource.max-wait}")
    private int maxWait;

    @Value("${spring.datasource.time-between-eviction-runs-millis}")
    private int timeBetweenEvictionRunsMillis;

    @Value("${spring.datasource.min-evictable-idle-time-millis}")
    private int minEvictableIdleTimeMillis;

    @Value("${spring.datasource.test-while-idle}")
    private boolean testWhileIdle;

    @Value("${spring.datasource.test-on-borrow}")
    private boolean testOnBorrow;

    @Value("${spring.datasource.test-on-return}")
    private boolean testOnReturn;

    @Value("${spring.datasource.pool-prepared-statements}")
    private boolean poolPreparedStatements;

    @Value("${spring.datasource.max-pool-prepared-statement-per-connection-size}")
    private int maxPoolPreparedStatementPerConnectionSize;

    @Value("${spring.datasource.filters}")
    private String filters;

    @Primary  //在同样的DataSource中，首先使用被标注的DataSource
    @Bean
    public DruidDataSource dataSourceDefault(){
        DruidDataSource datasource = new DruidDataSource();

        datasource.setUrl(this.dbUrl);
        datasource.setUsername(username);
        datasource.setPassword(password);
        datasource.setDriverClassName(driverClassName);

        //configuration
        datasource.setInitialSize(initialSize);
        datasource.setMinIdle(minIdle);
        datasource.setMaxActive(maxActive);
        datasource.setMaxWait(maxWait);
        datasource.setTimeBetweenEvictionRunsMillis(timeBetweenEvictionRunsMillis);
        datasource.setMinEvictableIdleTimeMillis(minEvictableIdleTimeMillis);
        datasource.setTestWhileIdle(testWhileIdle);
        datasource.setTestOnBorrow(testOnBorrow);
        datasource.setTestOnReturn(testOnReturn);
        datasource.setPoolPreparedStatements(poolPreparedStatements);
        datasource.setMaxPoolPreparedStatementPerConnectionSize(maxPoolPreparedStatementPerConnectionSize);
        try {
            datasource.setFilters(filters);
        } catch (SQLException e) {
            logger.error("druid configuration initialization filter", e);
        }
        return datasource;
    }
}

```

- 第二个

```java
package com.example.xiong.conf;

import com.alibaba.druid.support.http.StatViewServlet;
import com.alibaba.druid.support.http.WebStatFilter;
import org.springframework.boot.web.servlet.FilterRegistrationBean;
import org.springframework.boot.web.servlet.ServletRegistrationBean;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

import java.util.HashMap;
import java.util.Map;

/**
 * Druid连接池监控配置信息
 * 提示：druid-spring-boot-starter jar包的版本高于1.1.10时才需要配置该类
 * 1.若低于1.1.10版本时直接访问：IP:端口/druid/index.html即可
 * 2.若高于1.0.10版本时访问:IP:端口/druid/login.html即可 账号密码根据自己设置的来
 *
 * @author wyj
 * @date 2022/8/16 15:54
 */
@Configuration
public class DruidMonitorConfig {

    //因为Springboot内置了servlet容器，所以没有web.xml，替代方法就是将ServletRegistrationBean注册进去
    //加入后台监控
    @Bean  //这里其实就相当于servlet的web.xml
    public ServletRegistrationBean<StatViewServlet> statViewServlet() {
        ServletRegistrationBean<StatViewServlet> bean =
                new ServletRegistrationBean<>(new StatViewServlet(), "/druid/*");

        //后台需要有人登录，进行配置
        //bean.addUrlMappings(); 这个可以添加映射，我们在构造里已经写了
        //设置一些初始化参数
        Map<String, String> initParas = new HashMap<>();
        initParas.put("loginUsername", "admin");//它这个账户密码是固定的
        initParas.put("loginPassword", "123456");
        //允许谁能防伪
        initParas.put("allow", "");//这个值为空或没有就允许所有人访问，ip白名单
        //initParas.put("allow","localhost");//只允许本机访问，多个ip用逗号,隔开
        //initParas.put("deny","");//ip黑名单，拒绝谁访问 deny和allow同时存在优先deny
        initParas.put("resetEnable", "false");//禁用HTML页面的Reset按钮
        bean.setInitParameters(initParas);
        return bean;
    }

    //再配置一个过滤器，Servlet按上面的方式注册Filter也只能这样
    @Bean
    public FilterRegistrationBean<WebStatFilter> webStatFilter() {
        FilterRegistrationBean<WebStatFilter> bean = new FilterRegistrationBean<>();
        //可以设置也可以获取,设置一个阿里巴巴的过滤器
        bean.setFilter(new WebStatFilter());
        bean.addUrlPatterns("/*");
        //可以过滤和排除哪些东西
        Map<String, String> initParams = new HashMap<>();
        //把不需要监控的过滤掉,这些不进行统计
        initParams.put("exclusions", "*.js,*.css,/druid/*");
        bean.setInitParameters(initParams);
        return bean;
    }
}

```

### 测试

```http
http://127.0.0.1:8889/druid/api.html
```



