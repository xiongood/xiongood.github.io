---
title: 简单的elk实现
author: 张一雄
summary: 简单的elk的实现，方便理解其运行过程及实现原理！
img: https://pub-b24cf0a8c1f14e9386435977aa464959.r2.dev/img/20230816150331.png
categories:
 - 后端
tags:
 - java
 - elk
---

## 说明

软件的版本必须一致，否则会出现意想不到的问题

## 下载地址

```http
https://www.elastic.co/downloads/past-releases
```

## windows下安装

### 安装 es

- 下载解压

- 修改配置文件【elasticsearch.yml】

  ```yml
  # 免认证
  xpack.security.enabled:false
  xpack.security.enrollment.enabled:false
  xpack.security.transport.ssl.enabled:false
  
  # 解决跨域（添加）
  http.cors.enabled: true
  http.cors.allow-origin: "*"
  ingest.geoip.downloader.enabled: false
  ```

- 启动./bin

  ```sh
  elasticsearch.bat
  ```

- 显示以下则证明成功

  ```txt
  [2023-02-13T19:23:09,160][INFO ][o.e.c.r.a.AllocationService] [XIONG] current.health="GREEN" message="Cluster health status changed from [RED] to [GREEN] (reason: [shards started [[.security-7][0]]])." previous.health="RED" reason="shards started [[.security-7][0]]"
  [2023-02-13T19:23:09,355][INFO ][o.e.i.g.DatabaseNodeService] [XIONG] successfully loaded geoip database file [GeoLite2-Country.mmdb]
  [2023-02-13T19:23:09,426][INFO ][o.e.i.g.DatabaseNodeService] [XIONG] successfully loaded geoip database file [GeoLite2-ASN.mmdb]
  [2023-02-13T19:23:10,398][INFO ][o.e.i.g.DatabaseNodeService] [XIONG] successfully loaded geoip database file [GeoLite2-City.mmdb]
  ```

- 测试

  ```http
  http://localhost:9200/
  ```

  ```json
  {
      "name": "XIONG",
      "cluster_name": "elasticsearch",
      "cluster_uuid": "a65wohquR1We8Y7jDo3UMA",
      "version": {
          "number": "8.6.1",
          "build_flavor": "default",
          "build_type": "zip",
          "build_hash": "180c9830da956993e59e2cd70eb32b5e383ea42c",
          "build_date": "2023-01-24T21:35:11.506992272Z",
          "build_snapshot": false,
          "lucene_version": "9.4.2",
          "minimum_wire_compatibility_version": "7.17.0",
          "minimum_index_compatibility_version": "7.0.0"
      },
      "tagline": "You Know, for Search"
  }
  ```

### 安装 ElasticSearch-head

- 安装node.js

- 安装grunt

  ```sh
  npm install grunt -g
  ```

- 下载包

  ```http
  https://github.com/mobz/elasticsearch-head
  ```

- 安装

  解决跨域

  ```sh
  # 解决跨域
  http.cors.enabled: true
  http.cors.allow-origin: "*"
  ```

  

  ```sh
  cd elasticsearch-head
  npm install
  npm run start
  http://127.0.0.1:9100/
  ```

### 安装 kibana

- 下载

  ```http
  https://www.elastic.co/cn/downloads/past-releases
  ```

- 修改配置文件 config.kibana.yml

  ```sh
  # 更多配置信息，详见 https://www.elastic.co/guide/cn/kibana/current/settings.html
      server.port: 5601
      server.host: "127.0.0.1"
      server.name: lqz
      elasticsearch.hosts: ["http://localhost:9200/"]
  ```

- 启动

  ```sh
  ./bin/kibana
  ```

- 访问

  ```http
  http://127.0.0.1:5601/app/kibana
  ```

- 查询页面

  ![image-20230303093358454](D:/data/gitData/notes/notes/01-%E7%9F%A5%E8%AF%86%E5%BA%93/03-%E7%AC%AC%E4%B8%89%E7%AB%A0-%E5%A4%A7%E6%95%B0%E6%8D%AE%E7%AF%87/es-elasticsearch/es-2023-02-13.assets/image-20230303093358454.png)


### 安装logstash

- 下载(可能需要梯子)

  ```http
  https://www.elastic.co/cn/downloads/past-releases#logstash
  ```


 - 修改配置文件

   ./config/logstash-sample.conf

   ```yaml
   # Sample Logstash configuration for creating a simple
   # Beats -> Logstash -> Elasticsearch pipeline.
   
   input {
     tcp {
       mode => "server"
       host => "localhost"
       port => 5044
       codec => json_lines
     }
   }
   output {
     elasticsearch {
       hosts => "localhost:9200"
       index => "springboot-logstash-%{+YYYY.MM.dd}"
     }
   }
   
   ```

- 启动

  cd ./bin

  ```sh
  logstash.bat -f D:\server\logstash-8.6.1-windows-x86_64\logstash-8.6.1\config\logstash-sample.conf
  ```

## linux下安装

### 安装es

- 下载

  ```http
  https://www.elastic.co/cn/downloads/elasticsearch
  ```

### 安装kibana

- 略

### 安装logstash

- 略

## java将日志输入到logstash

- 创建springboot项目

- 添加依赖

  ```xml
  <dependency>
      <groupId>net.logstash.logback</groupId>
      <artifactId>logstash-logback-encoder</artifactId>
      <version>4.9</version>
  </dependency>
  ```

- logback-spring.xml

  ```xml
  <?xml version="1.0" encoding="UTF-8"?>
  <!--该日志将日志级别不同的log信息保存到不同的文件中 -->
  <configuration>
      <include resource="org/springframework/boot/logging/logback/defaults.xml" />
  
      <springProperty scope="context" name="springAppName"
                      source="spring.application.name" />
  
      <!-- 日志在工程中的输出位置 -->
      <property name="LOG_FILE" value="${BUILD_FOLDER:-build}/${springAppName}" />
  
      <!-- 控制台的日志输出样式 -->
      <property name="CONSOLE_LOG_PATTERN"
                value="%clr(%d{yyyy-MM-dd HH:mm:ss.SSS}){faint} %clr(${LOG_LEVEL_PATTERN:-%5p}) %clr(${PID:- }){magenta} %clr(---){faint} %clr([%15.15t]){faint} %m%n${LOG_EXCEPTION_CONVERSION_WORD:-%wEx}}" />
  
      <!-- 控制台输出 -->
      <appender name="console" class="ch.qos.logback.core.ConsoleAppender">
          <filter class="ch.qos.logback.classic.filter.ThresholdFilter">
              <level>INFO</level>
          </filter>
          <!-- 日志输出编码 -->
          <encoder>
              <pattern>${CONSOLE_LOG_PATTERN}</pattern>
              <charset>utf8</charset>
          </encoder>
      </appender>
  
      <!-- 为logstash输出的JSON格式的Appender -->
      <appender name="logstash"
                class="net.logstash.logback.appender.LogstashTcpSocketAppender">
          <destination>127.0.0.1:5044</destination>
          <!-- 日志输出编码 -->
          <encoder
                  class="net.logstash.logback.encoder.LoggingEventCompositeJsonEncoder">
              <providers>
                  <timestamp>
                      <timeZone>UTC</timeZone>
                  </timestamp>
                  <pattern>
                      <pattern>
                          {
                          "severity": "%level",
                          "service": "${springAppName:-}",
                          "trace": "%X{X-B3-TraceId:-}",
                          "span": "%X{X-B3-SpanId:-}",
                          "exportable": "%X{X-Span-Export:-}",
                          "pid": "${PID:-}",
                          "thread": "%thread",
                          "class": "%logger{40}",
                          "rest": "%message"
                          }
                      </pattern>
                  </pattern>
              </providers>
          </encoder>
      </appender>
  
      <!-- 日志输出级别 -->
      <root level="INFO">
          <appender-ref ref="console" />
          <appender-ref ref="logstash" />
      </root>
      
  </configuration>
  
  ```

- 启动springboot项目

- 使用kibana查询 导入到 es中所有的index

  ```http
  http://127.0.0.1:5601/app/dev_tools#/console
  ```

  ![image-20230303105339877](D:/data/gitData/notes/notes/01-%E7%9F%A5%E8%AF%86%E5%BA%93/03-%E7%AC%AC%E4%B8%89%E7%AB%A0-%E5%A4%A7%E6%95%B0%E6%8D%AE%E7%AF%87/es-elasticsearch/es-2023-02-13.assets/image-20230303105339877.png)

## java 查询es中的日志

- pom.xml

  ```xml
  <dependency>
      <groupId>org.elasticsearch.client</groupId>
      <artifactId>elasticsearch-rest-high-level-client</artifactId>
  </dependency>
  <dependency>
      <groupId>org.springframework.data</groupId>
      <artifactId>spring-data-elasticsearch</artifactId>
  </dependency>
  ```

- application.yml

  ```yml
  server:
      port: 8080
  spring:
      elasticsearch:
          rest:
              uris: localhost:9200
              username:
              password:
  ```

  

- service.java

  ```java
  package com.pj.service;
  import com.pj.entity.Log;
  import org.elasticsearch.index.query.MatchAllQueryBuilder;
  import org.elasticsearch.index.query.QueryBuilders;
  import org.elasticsearch.search.sort.FieldSortBuilder;
  import org.elasticsearch.search.sort.SortOrder;
  import org.springframework.beans.factory.annotation.Autowired;
  import org.springframework.data.domain.Page;
  import org.springframework.data.domain.PageImpl;
  import org.springframework.data.domain.PageRequest;
  import org.springframework.data.domain.Pageable;
  import org.springframework.data.elasticsearch.core.ElasticsearchRestTemplate;
  import org.springframework.data.elasticsearch.core.SearchHit;
  import org.springframework.data.elasticsearch.core.SearchHits;
  import org.springframework.data.elasticsearch.core.query.NativeSearchQuery;
  import org.springframework.data.elasticsearch.core.query.NativeSearchQueryBuilder;
  import org.springframework.stereotype.Service;
  import java.util.ArrayList;
  import java.util.List;
  
  @Service
  public class LogServiceImpl {
  
      @Autowired
      private ElasticsearchRestTemplate elasticsearchRestTemplate;
  
      public Object test(){
          // 构建查询条件(搜索全部)
          MatchAllQueryBuilder queryBuilder1 = QueryBuilders.matchAllQuery();
          // 分页
          Pageable pageable = PageRequest.of(0, 5);
          // 排序
          //FieldSortBuilder balance = new FieldSortBuilder("pid").order(SortOrder.DESC);
          // 执行查询
          NativeSearchQuery query = new NativeSearchQueryBuilder()
                  .withQuery(queryBuilder1)
                  .withPageable(pageable)
                  //.withSort(balance)
                  .build();
          SearchHits<Log> searchHits = elasticsearchRestTemplate.search(query, Log.class);
  
          //封装page对象
          List<Log> accounts = new ArrayList<>();
          for (SearchHit<Log> hit : searchHits) {
              accounts.add(hit.getContent());
          }
          Page<Log> page = new PageImpl<>(accounts,pageable,searchHits.getTotalHits());
          //输出分页对象
          System.out.println(page.getTotalPages());
          System.out.println(page.getTotalElements());
          return new Object();
      }
  }
  
  ```

  





















