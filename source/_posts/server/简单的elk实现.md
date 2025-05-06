---
title: 简单的elk实现
author: 张一雄
summary: 简单的elk的实现，方便理解其运行过程及实现原理！
img: https://img.myfox.fun/img/elk.jpg
categories:
 - 后端
tags:
 - java
 - elk
---

## 说明

<font color="red">注：软件的版本必须一致，否则会出现意想不到的问题</font>

## Elasticsearch 和 JVM 版本对应关系

```http
https://www.elastic.co/cn/support/matrix#matrix_jvm
```

## 下载地址

```http
https://www.elastic.co/downloads/past-releases
```

## windows下安装

### 安装 es

<font color="red">目前使用7.16.3版本</font>

- 下载解压

- 修改配置文件【elasticsearch.yml】

  <font color="red">注：使用8.17.1 版本，不用修改下面配置</font>

  

  ```yml
  # 免认证
  xpack.security.enabled: false
  #xpack.security.enrollment.enabled: false
  xpack.security.transport.ssl.enabled: false
  
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
    "name" : "XIONG",
    "cluster_name" : "elasticsearch",
    "cluster_uuid" : "7666b60AR6S6NNuDcQruuw",
    "version" : {
      "number" : "7.16.3",
      "build_flavor" : "default",
      "build_type" : "zip",
      "build_hash" : "4e6e4eab2297e949ec994e688dad46290d018022",
      "build_date" : "2022-01-06T23:43:02.825887787Z",
      "build_snapshot" : false,
      "lucene_version" : "8.10.1",
      "minimum_wire_compatibility_version" : "6.8.0",
      "minimum_index_compatibility_version" : "6.0.0-beta1"
    },
    "tagline" : "You Know, for Search"
  }
  ```

### 安装 ElasticSearch-head 可以不装

ElasticSearch-head 是一个基于 Web 的 Elasticsearch 集群管理工具，它为 Elasticsearch 提供了图形化的用户界面，方便用户与 Elasticsearch 集群进行交互和管理

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

Kibana 是一款为 Elasticsearch 设计的开源数据可视化和探索工具，它与 Elasticsearch 紧密集成，为用户提供了强大的界面来分析、可视化和管理存储在 Elasticsearch 中的数据。

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
  # 此过程有点慢
  ./bin/kibana
  ```

- 访问

  感觉有点慢，等了很久

  ```http
  http://localhost:5601
  ```

- 查询页面

  ![image-20250213101318474](http://img.myfox.fun/img/image-20250213101318474.png)

### 安装logstash

它是一个开源的数据收集、处理和传输工具。

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
       index => "springboot-logstash-%{+YYYY.MM.dd}" # es中的inde新名称 可以去掉后面的日期格式。
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


- DemoController.java

  ```java
  package fun.myfox.cleandemo.controller;
  
  
  import fun.myfox.cleandemo.entity.Log;
  import fun.myfox.cleandemo.service.LogEntryRepository;
  import fun.myfox.cleandemo.service.LogServiceImpl;
  import fun.myfox.cleandemo.utils.R;
  import lombok.extern.slf4j.Slf4j;
  import org.springframework.beans.factory.annotation.Autowired;
  import org.springframework.web.bind.annotation.GetMapping;
  import org.springframework.web.bind.annotation.RequestMapping;
  import org.springframework.web.bind.annotation.RestController;
  
  import java.io.IOException;
  import java.util.Date;
  
  
  /**
   * @author 张一雄
   */
  @RestController
  @RequestMapping("/demo")
  @Slf4j
  public class DemoController {
  
      @Autowired
      LogServiceImpl logService;
      @Autowired
      private LogEntryRepository logEntryRepository;
  
  
      // 查询方式1
      @GetMapping("/query")
      public R<Object> query() {
          logService.query();
          return R.success("success");
      }
  
  
      // 查询方式2
      @GetMapping("/queryLog")
      public R<Object> queryLog() throws IOException {
          // 查询所有日志数据
          Iterable<Log> allLogs = logEntryRepository.findAll();
          for (Log allLog : allLogs) {
              System.out.println(allLog.getPid());
              System.out.println(allLog.getRest());
          }
  
          // 根据日志级别查询
          // 这里可以使用自定义查询方法或使用QueryBuilder构建复杂查询
          return R.success("success");
      }
  
  
      // 创建index
      @GetMapping("/checkAndCreateIndex")
      public R<Object> checkAndCreateIndex() throws IOException {
          logService.checkAndCreateIndex();
          return R.success("success");
      }
  
  
      // 写入测试日志
      @GetMapping("/writeLog")
      public R<Object> writeLog() {
          log.info("测试日志 info"+new Date().getTime());
          log.error("测试日志 error"+new Date().getTime());
          return R.success("success");
      }
  
  }
  
  ```

- 实体类Log

  ```java
  package fun.myfox.cleandemo.entity;
  
  import lombok.Data;
  import lombok.ToString;
  import org.springframework.data.annotation.Id;
  import org.springframework.data.elasticsearch.annotations.Document;
  import org.springframework.data.elasticsearch.annotations.Field;
  import org.springframework.data.elasticsearch.annotations.FieldType;
  
  @Data
  @ToString
  // 这里的索引名要和实际的索引名一致,查询时的索引默认为 类名，可以通过此处进行修改
  @Document(indexName = "springboot-logstash-2025.02.13")
  public class Log {
      private String severity;
      private String service;
      private String trace;
      private String span;
      @Field(type = FieldType.Keyword)
      private String exportable;
      @Id
      private String pid;
      private String thread;
      private String rest;
  }
  
  ```

- service.java

  ```java
  package fun.myfox.cleandemo.service;
  
  import fun.myfox.cleandemo.entity.Log;
  import org.elasticsearch.client.RestHighLevelClient;
  import org.elasticsearch.client.indices.CreateIndexResponse;
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
  import org.elasticsearch.client.indices.CreateIndexRequest;
  import org.elasticsearch.client.indices.GetIndexRequest;
  import org.elasticsearch.client.RequestOptions;
  import java.io.IOException;
  
  @Service
  public class LogServiceImpl {
  
      @Autowired
      private ElasticsearchRestTemplate elasticsearchRestTemplate;
  
  
      // 查询数据
      public Object query(){
          // 构建查询条件(搜索全部)
          MatchAllQueryBuilder queryBuilder1 = QueryBuilders.matchAllQuery();
          // 分页
          Pageable pageable = PageRequest.of(0, 5);
          // 排序
          FieldSortBuilder balance = new FieldSortBuilder("pid").order(SortOrder.DESC);
          // 执行查询
          NativeSearchQuery query = new NativeSearchQueryBuilder()
                  .withQuery(queryBuilder1)
                  .withPageable(pageable)
                  .withSort(balance)
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
  
  
      @Autowired
      private RestHighLevelClient restHighLevelClient;
  
      // 检查并创建索引
      public void checkAndCreateIndex() throws IOException {
          String indexName = "log"; // 这里要和你实体类对应的索引名一致
          GetIndexRequest getIndexRequest = new GetIndexRequest(indexName);
          boolean exists = restHighLevelClient.indices().exists(getIndexRequest, RequestOptions.DEFAULT);
          if (!exists) {
              CreateIndexRequest createIndexRequest = new CreateIndexRequest(indexName);
              CreateIndexResponse createIndexResponse = restHighLevelClient.indices().create(createIndexRequest, RequestOptions.DEFAULT);
              if (!createIndexResponse.isAcknowledged()) {
                  throw new RuntimeException("Failed to create index: " + indexName);
              }
          }
      }
  }
  
  ```

  

- service2.java

  ```java
  package fun.myfox.cleandemo.service;
  
  import fun.myfox.cleandemo.entity.Log;
  import org.springframework.data.elasticsearch.repository.ElasticsearchRepository;
  
  public interface LogEntryRepository extends ElasticsearchRepository<Log, String> {
  }
  ```

- R.java

  ```java
  package fun.myfox.cleandemo.utils;
  
  import lombok.Data;
  
  /**
   * @author 张一雄
   */
  @Data
  public class R<T> {
  
      private String code;
      private String message;
      private T data;
  
      public R(String code, T data, String message) {
          this.code = code;
          this.message = message;
          this.data = data;
      }
  
      public static <T> R<T> success(T data) {
          return new R<>(StatusCode.SUCCESS, data, "success");
      }
  
      public static <T> R<T> error(String message) {
          return new R<>(StatusCode.ERROR, null, message);
      }
  
  }
  
  ```

- StatusCode.java

  ```java
  package fun.myfox.cleandemo.utils;
  
  public class StatusCode {
  
      public static final String SUCCESS = "200";
      public static final String ERROR = "500";
  
  }
  
  ```

  

## kibana 查询

```txt
GET _search
{
  "query": {
    "match_all": {}
  }
}

# 分页查询
GET /springboot-logstash-2025.02.13/_search
{

    "query": {

        "match_all": {}

    },
    "size": 100

}

# 创建时间倒序查询
GET /springboot-logstash-2025.02.13/_search
{
    "query": {
        "match_all": {}
    },
    "size": 100,
    "sort": [
        {
            "@timestamp": {
                "order": "desc"
            }
        }
    ]
}


# 根据某字段 模糊查询
GET /springboot-logstash-2025.02.13/_search
{
    "query": {
        "match": {
            "rest": "测试"
        }
    }
}

# 高亮显示
GET /springboot-logstash-2025.02.13/_search
{
    "query": {
        "match": {
            "rest": "测试"
        }
    },
    "highlight": {
        "fields": {
            "rest": {}
        }
    }
}


GET /springboot_logs/_search
{

    "query": {

        "match_all": {}

    }

}
```



## 面试题

持久化？

集群？

性能？









