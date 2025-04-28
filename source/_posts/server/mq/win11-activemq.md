---
title: activemq的部署与使用
img: https://gitee.com/xiongood/image/raw/master/activemq.jpg
categories:
 - 后端
tags:
 - activemq
 - java
---



## 说明

### 官网
```http request
https://activemq.apache.org/components/classic/download/
```
### 其他版本
```http request
https://activemq.apache.org/download-archives
```

### jdk版本对应关系

```http
https://activemq.apache.org/getting-started#Pre-InstallationRequirements
```

![image-20230625172804505](https://gitee.com/xiongood/image/raw/master/20230625172805.png)

![image-20230607154249549](https://gitee.com/xiongood/image/raw/master/20230607154250.png)

## windows版启动

### 直接启动

![image-20230607161848692](https://gitee.com/xiongood/image/raw/master/20230607161849.png)

### 访问

```http
http://localhost:8161/
```

账号密码 都为 admin

![image-20230607162019968](https://gitee.com/xiongood/image/raw/master/20230607162021.png)

### 后台静寂启动

![image-20230607162341347](https://gitee.com/xiongood/image/raw/master/20230607162342.png)

## 配置

### 设置生产消费者的账密

在java中使用

修改conf目录下的 activemq.xml 文件

在broker 节点下新增如下配置

```xml
<plugins>
    <simpleAuthenticationPlugin>
        <users>
            <authenticationUser username="xiong" password="123456" groups="users,admins"/>
        </users>
    </simpleAuthenticationPlugin>
</plugins>
```

![image-20230607162620537](https://gitee.com/xiongood/image/raw/master/20230607162621.png)

### 设置延时发送消息

定时或者延时发送消息 需要开启此处，否则不生效，修改后需要重启服务

修改conf目录下的 activemq.xml 文件，在broker 节点上新增schedulerSupport="true"

```xml
<broker xmlns="http://activemq.apache.org/schema/core" brokerName="localhost" dataDirectory="${activemq.data}" schedulerSupport="true">
</broker>   
```

## springboot整合mq

### pom

```xml
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-activemq</artifactId>
</dependency>
<dependency>
    <groupId>org.apache.activemq</groupId>
    <artifactId>activemq-pool</artifactId>
    <version>5.15.3</version>
</dependency>
```

### application.yml

```yaml
server:
  port: 8080
  #servlet:
  #  context-path: /demo

#spring:
#  profiles:
#    active: dev

logging:
  config: classpath:logback.xml

spring:
  activemq:
    user: xiong
    password: 123456
    broker-url: failover:(tcp://localhost:61616)
    #brokerurl: failover:(tcp://172.16.194.98:61666,tcp://172.16.194.99:61666,tcp://172.16.194.100:61666)?initialReconnectDelay=3000&timeout=3000&jms.connectResponseTimeout=3000&randomize=true
    #是否信任所有包(如果传递的是对象则需要设置为true，默认是传字符串)
    packages:
      trust-all: true
    #连接池
    pool:
      enabled: true
      max-connections: 5
      idle-timeout: 30000
    #      expiry-timeout: 0
    jms:
      #默认使用queue模式，使用topic则需要设置为true
      pub-sub-domain: true

      # 是否信任所有包
      #spring.activemq.packages.trust-all=
      # 要信任的特定包的逗号分隔列表（当不信任所有包时）
      #spring.activemq.packages.trusted=
      # 当连接请求和池满时是否阻塞。设置false会抛“JMSException异常”。
      #spring.activemq.pool.block-if-full=true
      # 如果池仍然满，则在抛出异常前阻塞时间。
      #spring.activemq.pool.block-if-full-timeout=-1ms
      # 是否在启动时创建连接。可以在启动时用于加热池。
      #spring.activemq.pool.create-connection-on-startup=true
      # 是否用Pooledconnectionfactory代替普通的ConnectionFactory。
      #spring.activemq.pool.enabled=false
      # 连接过期超时。
      #spring.activemq.pool.expiry-timeout=0ms
      # 连接空闲超时
      #spring.activemq.pool.idle-timeout=30s
      # 连接池最大连接数
      #spring.activemq.pool.max-connections=1
      # 每个连接的有效会话的最大数目。
      #spring.activemq.pool.maximum-active-session-per-connection=500
      # 当有"JMSException"时尝试重新连接
      #spring.activemq.pool.reconnect-on-exception=true
      # 在空闲连接清除线程之间运行的时间。当为负数时，没有空闲连接驱逐线程运行。
      #spring.activemq.pool.time-between-expiration-check=-1ms
      # 是否只使用一个MessageProducer
      #spring.activemq.pool.use-anonymous-producers=true
```

### 配置文件

```java
import org.apache.activemq.ActiveMQConnectionFactory;
import org.apache.activemq.RedeliveryPolicy;
import org.apache.activemq.command.ActiveMQQueue;
import org.apache.activemq.command.ActiveMQTopic;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.jms.annotation.EnableJms;
import org.springframework.jms.config.DefaultJmsListenerContainerFactory;
import org.springframework.jms.config.JmsListenerContainerFactory;

import javax.jms.Queue;
import javax.jms.Topic;

/**
 * 描述:
 * activemq 有两种模式 queue 和 topic
 * queue 模式是单对单，有多个消费者的情况下则是使用轮询监听
 * topic 模式/广播模式/发布订阅模式 是一对多，发送消息所有的消费者都能够监听到
 *
 * @author gblfy
 * @date 2022-11-02
 */
@EnableJms
@Configuration
public class ActiveMQConfig {
    //队列名
    private static final String queueName = "active.queue";
    //主题名
    private static final String topicName = "active.topic";

    @Value("${spring.activemq.user:}")
    private String username;
    @Value("${spring.activemq.password:}")
    private String password;
    @Value("${spring.activemq.broker-url:}")
    private String brokerUrl;

    @Bean
    public Queue acQueue() {
        return new ActiveMQQueue(queueName);
    }

    @Bean
    public Topic acTopic() {
        return new ActiveMQTopic(topicName);
    }

    @Bean
    public ActiveMQConnectionFactory connectionFactory() {
        return new ActiveMQConnectionFactory(username, password, brokerUrl);
    }

    @Bean
    public JmsListenerContainerFactory<?> jmsListenerContainerQueue(ActiveMQConnectionFactory connectionFactory) {
        DefaultJmsListenerContainerFactory bean = new DefaultJmsListenerContainerFactory();
        // 关闭Session事务，手动确认与事务冲突
        bean.setSessionTransacted(false);
        // 设置消息的签收模式（自己签收）
        /**
         * AUTO_ACKNOWLEDGE = 1 ：自动确认
         * CLIENT_ACKNOWLEDGE = 2：客户端手动确认
         * DUPS_OK_ACKNOWLEDGE = 3： 自动批量确认
         * SESSION_TRANSACTED = 0：事务提交并确认
         * 但是在activemq补充了一个自定义的ACK模式:
         * INDIVIDUAL_ACKNOWLEDGE = 4：单条消息确认
         **/
        bean.setSessionAcknowledgeMode(4);
        //此处设置消息重发规则，redeliveryPolicy() 中定义
        connectionFactory.setRedeliveryPolicy(redeliveryPolicy());
        bean.setConnectionFactory(connectionFactory);
        return bean;
    }

    @Bean
    public JmsListenerContainerFactory<?> jmsListenerContainerTopic(ActiveMQConnectionFactory connectionFactory) {
        DefaultJmsListenerContainerFactory bean = new DefaultJmsListenerContainerFactory();
        // 关闭Session事务，手动确认与事务冲突
        bean.setSessionTransacted(false);
        bean.setSessionAcknowledgeMode(4);
        //设置为发布订阅方式, 默认情况下使用的生产消费者方式
        bean.setPubSubDomain(true);
        bean.setConnectionFactory(connectionFactory);
        return bean;
    }

    /**
     * 消息的重发规则配置
     */
    @Bean
    public RedeliveryPolicy redeliveryPolicy() {
        RedeliveryPolicy redeliveryPolicy = new RedeliveryPolicy();
        // 是否在每次尝试重新发送失败后,增长这个等待时间
        redeliveryPolicy.setUseExponentialBackOff(true);
        // 重发次数五次， 总共六次
        redeliveryPolicy.setMaximumRedeliveries(5);
        // 重发时间间隔,默认为1000ms（1秒）
        redeliveryPolicy.setInitialRedeliveryDelay(1000);
        // 重发时长递增的时间倍数2
        redeliveryPolicy.setBackOffMultiplier(2);
        // 是否避免消息碰撞
        redeliveryPolicy.setUseCollisionAvoidance(false);
        // 设置重发最大拖延时间-1表示无延迟限制
        redeliveryPolicy.setMaximumRedeliveryDelay(-1);
        return redeliveryPolicy;
    }
}
```

### 消费者queue

```java
import org.apache.activemq.command.ActiveMQMessage;
import org.springframework.jms.annotation.JmsListener;
import org.springframework.stereotype.Component;

import javax.jms.JMSException;
import javax.jms.Session;

/**
 * TODO
 *
 * @author gblfy
 * @Date 2022-11-02
 **/
@Component
public class QueueListener {

    /**
     * queue 模式 单对单，两个消费者监听同一个队列则通过轮询接收消息
     * containerFactory属性的值关联config类中的声明
     *
     * @param msg
     */
    @JmsListener(destination = "active.queue", containerFactory = "jmsListenerContainerQueue")
    public void queueListener(ActiveMQMessage message, Session session, String msg) throws JMSException {
        try {
            System.out.println("active queue 接收到消息 " + msg);
            //手动签收
            message.acknowledge();
        } catch (Exception e) {
            //重新发送
            session.recover();
        }
    }
}


```

### 消费者topic

```java
import org.apache.activemq.command.ActiveMQMessage;
import org.springframework.jms.annotation.JmsListener;
import org.springframework.stereotype.Component;

import javax.jms.JMSException;
import javax.jms.Session;

/**
 * TODO
 *
 * @author gblfy
 * @Date 2022-11-02
 **/
@Component
public class TopicListener {

    /**
     * topic 模式/广播模式/发布订阅模式 一对多，多个消费者可同时接收到消息
     * topic 模式无死信队列，死信队列是queue模式
     * containerFactory属性的值关联config类中的声明
     *
     * @param msg
     */
    @JmsListener(destination = "active.topic", containerFactory = "jmsListenerContainerTopic")
    public void topicListener(ActiveMQMessage message, Session session, String msg) throws JMSException {
        try {
            // System.out.println("接收到消息：" + DateUtil.getStringDate(new Date(), "yyyy-MM-dd HH:mm:ss"));
            System.out.println("active topic 接收到消息 " + msg);
            System.out.println("");
            //手动签收
            message.acknowledge();
        } catch (Exception e) {
            //重新发送
            session.recover();
        }
    }

    @JmsListener(destination = "active.topic", containerFactory = "jmsListenerContainerTopic")
    public void topicListener2(ActiveMQMessage message, Session session, String msg) throws JMSException {
        try {
            // System.out.println("接收到消息：" + DateUtil.getStringDate(new Date(), "yyyy-MM-dd HH:mm:ss"));
            System.out.println("active topic2 接收到消息 " + msg);
            System.out.println("");
            //手动签收
            message.acknowledge();
        } catch (Exception e) {
            //重新发送
            session.recover();
        }
    }
}


```

### 生产者

```java
package fun.myfox.cleandemo.controller;

import cn.hutool.json.JSONUtil;
import fun.myfox.cleandemo.utils.R;
import org.apache.activemq.ScheduledMessage;
import org.apache.activemq.command.ActiveMQQueue;
import org.apache.activemq.command.ActiveMQTopic;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.jms.core.JmsMessagingTemplate;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import javax.jms.Destination;
import java.text.ParseException;
import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.HashMap;
import java.util.Map;

/**
 * 发送消息
 *
 * @author gblfy
 * @date 2022-11-02
 */
@RestController
@RequestMapping(value = "/active")
public class SendController {
    // 也可以注入JmsTemplate，JmsMessagingTemplate对JmsTemplate进行了封装
    @Autowired
    private JmsMessagingTemplate jmsMessagingTemplate;

    /**
     * 发送消息接口
     * 发送queue消息 ：http://127.0.0.1:8080/active/send?msg=ceshi1234
     * 发送topic 消息： http://127.0.0.1:8080/active/topic/send?msg=ceshi1234
     * 发送queue消息(延迟time毫秒) ：http://localhost:8080/active/test
     *
     * @param type url中参数,非必须
     * @param msg  消息
     * @param time 延迟时间，单位毫秒
     * @return 发送结果
     */
    @RequestMapping({"/send", "/{type}/send"})
    public R send(@PathVariable(value = "type", required = false) String type,
                  @RequestParam("msg") String msg,
                  @RequestParam(value = "time", required = false) Long time) {
        try {
            Destination destination;
            if (type == null) {
                type = "";
            }
            switch (type) {
                case "topic":
                    // 发送广播消息
                    destination = new ActiveMQTopic("active.topic");
                    break;
                default:
                    // 发送 队列消息
                    destination = new ActiveMQQueue("active.queue");
                    break;
            }

            if (time != null && time > 0) {
                // 发送延时消息
                Map<String, Object> headers = new HashMap<>();
                headers.put(ScheduledMessage.AMQ_SCHEDULED_DELAY, time);
                jmsMessagingTemplate.convertAndSend(destination, msg, headers);
            } else {
                // 发送普通消息
                jmsMessagingTemplate.convertAndSend(destination, msg);
            }
            return R.success("消息发送成功");
        } catch (Exception e) {
            return R.error("消息发送失败：" + e.getMessage());
        }
    }

    /**
     * 发送延时消息
     * 说明：延迟队列需要在 <broker>标签上增加属性 schedulerSupport="true"
     *
     * @return 发送结果
     */
    @GetMapping("/test")
    public R test() {
        try {
            sendDelayedMessage("xiong5", 5000);
            sendDelayedMessage("xiong10", 10000);
            sendDelayedMessage("xiong15", 15000);
            return R.success("延时消息发送成功");
        } catch (Exception e) {
            return R.error("延时消息发送失败：" + e.getMessage());
        }
    }

    /**
     * 发送延时消息的辅助方法
     *
     * @param name  消息内容
     * @param delay 延迟时间，单位毫秒
     */
    private void sendDelayedMessage(String name, long delay) {
        Map<String, Object> headers = new HashMap<>();
        headers.put(ScheduledMessage.AMQ_SCHEDULED_DELAY, delay);
        Map<String, String> map = new HashMap<>();
        map.put("name", name);
        jmsMessagingTemplate.convertAndSend("active.queue", JSONUtil.toJsonStr(map), headers);
    }







    /**
     * 发送消息在指定时间点发出
     *
     * @param type    url中参数,非必须
     * @param msg     消息
     * @param sendTime 指定的发送时间，格式：yyyy-MM-dd HH:mm:ss
     * @return 发送结果
     *
     * http://127.0.0.1:8080/active/sendAtTime?msg=test&sendTime=2025-02-09 10:00:00
     * http://127.0.0.1:8080/active/topic/sendAtTime?msg=test&sendTime=2025-02-09 10:00:00
     */
    @RequestMapping({"/sendAtTime", "/{type}/sendAtTime"})
    public R sendAtTime(@PathVariable(value = "type", required = false) String type,
                        @RequestParam("msg") String msg,
                        @RequestParam("sendTime") String sendTime) {
        try {
            Destination destination;
            if (type == null) {
                type = "";
            }
            switch (type) {
                case "topic":
                    // 发送广播消息
                    destination = new ActiveMQTopic("active.topic");
                    break;
                default:
                    // 发送 队列消息
                    destination = new ActiveMQQueue("active.queue");
                    break;
            }

            // 解析指定的发送时间
            SimpleDateFormat sdf = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss");
            Date targetDate = sdf.parse(sendTime);
            Date now = new Date();
            long delay = targetDate.getTime() - now.getTime();

            if (delay <= 0) {
                return R.error("指定的时间已经过去，请选择一个未来的时间点");
            }

            // 发送延时消息
            Map<String, Object> headers = new HashMap<>();
            headers.put(ScheduledMessage.AMQ_SCHEDULED_DELAY, delay);
            jmsMessagingTemplate.convertAndSend(destination, msg, headers);

            return R.success("消息将在指定时间发送");
        } catch (ParseException e) {
            return R.error("时间格式错误，请使用 yyyy-MM-dd HH:mm:ss 格式");
        } catch (Exception e) {
            return R.error("消息发送失败：" + e.getMessage());
        }
    }
}
```

## 测试

     发送queue消息 ：http://127.0.0.1:8080/active/send?msg=ceshi1234
     发送topic 消息： http://127.0.0.1:8080/active/topic/send?msg=ceshi1234
     发送queue消息(延迟time毫秒) ：http://localhost:8080/active/test
