---
title: AOP的使用例子
img: https://img.myfox.fun/img/spring.jpg
categories:
 - 后端
tags:
 - AOP
 - java
 - redis
---

## 防重复点击

### 说明

aop+redis

### 编码

#### 方式一

- 编写pom文件

```xml
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 https://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>
    <groupId>com.xiong</groupId>
    <artifactId>demo-aop</artifactId>
    <version>0.0.1-SNAPSHOT</version>
    <name>demo-aop</name>
    <description>demo-aop</description>
    <properties>
        <java.version>1.8</java.version>
        <project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>
        <project.reporting.outputEncoding>UTF-8</project.reporting.outputEncoding>
        <spring-boot.version>2.3.12.RELEASE</spring-boot.version>
    </properties>

    <dependencies>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-web</artifactId>
        </dependency>

        <dependency>
            <groupId>org.projectlombok</groupId>
            <artifactId>lombok</artifactId>
            <optional>true</optional>
        </dependency>

        <!--aop-->
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-aop</artifactId>
        </dependency>
        <dependency>
            <groupId>aopalliance</groupId>
            <artifactId>aopalliance</artifactId>
            <version>1.0</version>
        </dependency>
        <dependency>
            <groupId>org.aspectj</groupId>
            <artifactId>aspectjweaver</artifactId>
            <version>1.8.9</version>
        </dependency>
        <!--aop end-->

        <!--redis start-->
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-data-redis</artifactId>
        </dependency>
        <dependency>
            <groupId>org.apache.commons</groupId>
            <artifactId>commons-pool2</artifactId>
        </dependency>
        <!--redis end-->

        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-test</artifactId>
            <scope>test</scope>
            <exclusions>
                <exclusion>
                    <groupId>org.junit.vintage</groupId>
                    <artifactId>junit-vintage-engine</artifactId>
                </exclusion>
            </exclusions>
        </dependency>
    </dependencies>

    <dependencyManagement>
        <dependencies>
            <dependency>
                <groupId>org.springframework.boot</groupId>
                <artifactId>spring-boot-dependencies</artifactId>
                <version>${spring-boot.version}</version>
                <type>pom</type>
                <scope>import</scope>
            </dependency>
        </dependencies>
    </dependencyManagement>

    <build>
        <plugins>
            <plugin>
                <groupId>org.apache.maven.plugins</groupId>
                <artifactId>maven-compiler-plugin</artifactId>
                <version>3.8.1</version>
                <configuration>
                    <source>1.8</source>
                    <target>1.8</target>
                    <encoding>UTF-8</encoding>
                </configuration>
            </plugin>
            <plugin>
                <groupId>org.springframework.boot</groupId>
                <artifactId>spring-boot-maven-plugin</artifactId>
                <version>${spring-boot.version}</version>
                <configuration>
                    <mainClass>com.xiong.demoaop.DemoAopApplication</mainClass>
                    <skip>true</skip>
                </configuration>
                <executions>
                    <execution>
                        <id>repackage</id>
                        <goals>
                            <goal>repackage</goal>
                        </goals>
                    </execution>
                </executions>
            </plugin>
        </plugins>
    </build>

</project>

```

- yml

```yml
server:
  port: 8000

spring:
  redis:
    # Redis服务器地址
    host: 192.168.43.111
    # Redis服务器端口号
    port: 6379
    # 使用的数据库索引，默认是0
    database: 0
    # 连接超时时间
    timeout: 1800000
    # 设置密码
    password: "123456"
    lettuce:
      pool:
        # 最大阻塞等待时间，负数表示没有限制
        max-wait: -1
        # 连接池中的最大空闲连接
        max-idle: 5
        # 连接池中的最小空闲连接
        min-idle: 0
        # 连接池中最大连接数，负数表示没有限制
        max-active: 20
```

- 编写redis配置类(防止乱码)

```java
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.data.redis.connection.RedisConnectionFactory;
import org.springframework.data.redis.core.RedisTemplate;
import org.springframework.data.redis.serializer.GenericJackson2JsonRedisSerializer;
import org.springframework.data.redis.serializer.RedisSerializer;

import java.net.UnknownHostException;

@Configuration
public class RedisConfig {
    @Bean
    public RedisTemplate<String, Object> redisTemplate(RedisConnectionFactory redisConnectionFactory)
            throws UnknownHostException {
        // 创建模板
        RedisTemplate<String, Object> redisTemplate = new RedisTemplate<>();
        // 设置连接工厂
        redisTemplate.setConnectionFactory(redisConnectionFactory);
        // 设置序列化工具
        GenericJackson2JsonRedisSerializer jsonRedisSerializer =
                new GenericJackson2JsonRedisSerializer();
        // key和 hashKey采用 string序列化
        redisTemplate.setKeySerializer(RedisSerializer.string());
        redisTemplate.setHashKeySerializer(RedisSerializer.string());
        // value和 hashValue采用 JSON序列化
        redisTemplate.setValueSerializer(jsonRedisSerializer);
        redisTemplate.setHashValueSerializer(jsonRedisSerializer);
        return redisTemplate;
    }
}

```

- 编写注解类

```java
/**
 * @功能描述 防止重复提交标记注解
 * @author www.gaozz.club
 * @date 2018-08-26
 */
@Target(ElementType.METHOD) // 作用到方法上
@Retention(RetentionPolicy.RUNTIME) // 运行时有效
public @interface NoRepeatSubmit {

}
```

- 编写切面类

```java
import com.xiong.demoaop.repeatClick.note.NoRepeatSubmit;
import org.aspectj.lang.ProceedingJoinPoint;
import org.aspectj.lang.Signature;
import org.aspectj.lang.annotation.Around;
import org.aspectj.lang.annotation.Aspect;
import org.aspectj.lang.reflect.MethodSignature;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.redis.core.RedisTemplate;
import org.springframework.stereotype.Component;
import java.lang.reflect.Method;
import java.util.Arrays;
import java.util.concurrent.TimeUnit;

/**
 * @功能描述 aop解析注解
 * @author www.gaozz.club
 * @date 2018-08-26
 */
@Aspect //作用是把当前类标识为一个切面供容器读
@Component
public class NoRepeatSubmitAop {

    @Autowired
    RedisTemplate redisTemplate;

    //@Around("execution(* com.example..*Controller.*(..)) && @annotation(nrs)")
    @Around("@annotation(nrs)")
    public Object around(ProceedingJoinPoint point, NoRepeatSubmit nrs) throws Throwable {
        System.out.println("@Before：模拟权限检查...");
        System.out.println("@Before：目标方法为：" + point.getSignature().getDeclaringTypeName() + "." + point.getSignature().getName());
        System.out.println("@Before：参数为：" + Arrays.toString(point.getArgs()));
        System.out.println("@Before：被织入的目标对象为：" + point.getTarget());
        System.out.println("签名："+point.getSignature());
        Signature s = point.getSignature();
        MethodSignature ms = (MethodSignature)s;
        Method m = ms.getMethod();
        System.out.println("方法名："+m.getName());
        // 判断缓存中，是否存在value
        if (null != redisTemplate.opsForValue().get(point.getSignature().toString())){
            return "请稍后点击"; //方法退出
        }else {
            // 设置自动删除的键
            redisTemplate.opsForValue().set(point.getSignature().toString(),"1",10,TimeUnit.SECONDS );
            return point.proceed(); //方法继续
        }
    }

}
```

- 编写测试类

```java
import com.xiong.demoaop.repeatClick.note.NoRepeatSubmit;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/re")
public class ReController {
    // 自定义注解
    @NoRepeatSubmit
    @GetMapping("test")
    public String test(){
        System.out.println("-------------------------------");
        return "success";
    }
}
```

#### 方式二

##### 说明 

@Around 注解的第二种方式

此种方式 不用自定义注解

```java
// public 方法类型
// * 返回值
// com…… 报名
// 第一个 ..  所有的路径
// .（..） 所有的方法
@Around("execution(public * com.xiong..*Controller.*(..))")
```

##### 整体

```java
import com.xiong.demoaop.repeatClick.note.NoRepeatSubmit;
import org.aspectj.lang.ProceedingJoinPoint;
import org.aspectj.lang.Signature;
import org.aspectj.lang.annotation.Around;
import org.aspectj.lang.annotation.Aspect;
import org.aspectj.lang.reflect.MethodSignature;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.redis.core.RedisTemplate;
import org.springframework.stereotype.Component;

import java.lang.reflect.Method;
import java.util.Arrays;
import java.util.concurrent.TimeUnit;

/**
 * @功能描述 aop解析注解
 * @author www.gaozz.club
 * @date 2018-08-26
 */
@Aspect //作用是把当前类标识为一个切面供容器读
@Component
public class NoRepeatSubmitAop {

    @Autowired
    RedisTemplate redisTemplate;

    @Around("execution(* com.xiong..*Controller.*(..))")
    public Object around(ProceedingJoinPoint point) throws Throwable {
        System.out.println("@Before：模拟权限检查...");
        System.out.println("@Before：目标方法为：" + point.getSignature().getDeclaringTypeName() + "." + point.getSignature().getName());
        System.out.println("@Before：参数为：" + Arrays.toString(point.getArgs()));
        System.out.println("@Before：被织入的目标对象为：" + point.getTarget());
        System.out.println("签名："+point.getSignature());
        Signature s = point.getSignature();
        MethodSignature ms = (MethodSignature)s;
        Method m = ms.getMethod();
        System.out.println("方法名："+m.getName());
        // 判断缓存中，是否存在value
        if (null != redisTemplate.opsForValue().get(point.getSignature().toString())){
            return "请稍后点击"; //方法退出
        }else {
            // 设置自动删除的键
            redisTemplate.opsForValue().set(point.getSignature().toString(),"1",10,TimeUnit.SECONDS );
            return point.proceed(); //方法继续
        }
    }

}
```

### 测试

```java
http://localhost:8000/re/test
```

## 加强log

### 编码

- pom

```xml
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 https://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>
    <groupId>com.xiong</groupId>
    <artifactId>demo-aop</artifactId>
    <version>0.0.1-SNAPSHOT</version>
    <name>demo-aop</name>
    <description>demo-aop</description>
    <properties>
        <java.version>1.8</java.version>
        <project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>
        <project.reporting.outputEncoding>UTF-8</project.reporting.outputEncoding>
        <spring-boot.version>2.3.12.RELEASE</spring-boot.version>
    </properties>

    <dependencies>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-web</artifactId>
        </dependency>

        <dependency>
            <groupId>org.projectlombok</groupId>
            <artifactId>lombok</artifactId>
            <optional>true</optional>
        </dependency>

        <!--aop-->
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-aop</artifactId>
        </dependency>
        <dependency>
            <groupId>aopalliance</groupId>
            <artifactId>aopalliance</artifactId>
            <version>1.0</version>
        </dependency>
        <dependency>
            <groupId>org.aspectj</groupId>
            <artifactId>aspectjweaver</artifactId>
            <version>1.8.9</version>
        </dependency>
        <!--aop end-->

        <!--redis start-->
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-data-redis</artifactId>
        </dependency>
        <dependency>
            <groupId>org.apache.commons</groupId>
            <artifactId>commons-pool2</artifactId>
        </dependency>
        <!--redis end-->

        <dependency>
            <groupId>cn.hutool</groupId>
            <artifactId>hutool-all</artifactId>
            <version>5.8.0.M2</version>
        </dependency>


        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-test</artifactId>
            <scope>test</scope>
            <exclusions>
                <exclusion>
                    <groupId>org.junit.vintage</groupId>
                    <artifactId>junit-vintage-engine</artifactId>
                </exclusion>
            </exclusions>
        </dependency>
    </dependencies>

    <dependencyManagement>
        <dependencies>
            <dependency>
                <groupId>org.springframework.boot</groupId>
                <artifactId>spring-boot-dependencies</artifactId>
                <version>${spring-boot.version}</version>
                <type>pom</type>
                <scope>import</scope>
            </dependency>
        </dependencies>
    </dependencyManagement>

    <build>
        <plugins>
            <plugin>
                <groupId>org.apache.maven.plugins</groupId>
                <artifactId>maven-compiler-plugin</artifactId>
                <version>3.8.1</version>
                <configuration>
                    <source>1.8</source>
                    <target>1.8</target>
                    <encoding>UTF-8</encoding>
                </configuration>
            </plugin>
            <plugin>
                <groupId>org.springframework.boot</groupId>
                <artifactId>spring-boot-maven-plugin</artifactId>
                <version>${spring-boot.version}</version>
                <configuration>
                    <mainClass>com.xiong.demoaop.DemoAopApplication</mainClass>
                    <skip>true</skip>
                </configuration>
                <executions>
                    <execution>
                        <id>repackage</id>
                        <goals>
                            <goal>repackage</goal>
                        </goals>
                    </execution>
                </executions>
            </plugin>
        </plugins>
    </build>

</project>

```

- 自定义注解

```java
import java.lang.annotation.ElementType;
import java.lang.annotation.Retention;
import java.lang.annotation.RetentionPolicy;
import java.lang.annotation.Target;

// 作用到方法上
@Target({ElementType.METHOD})
// 运行时有效
@Retention(RetentionPolicy.RUNTIME)
public @interface UpLog {

    String value() default "" ;

}
```

- 切面类

```java
import cn.hutool.core.date.DateUnit;
import cn.hutool.core.date.DateUtil;
import cn.hutool.core.util.StrUtil;
import com.xiong.demoaop.upLog.note.UpLog;
import lombok.extern.slf4j.Slf4j;
import org.aspectj.lang.ProceedingJoinPoint;
import org.aspectj.lang.annotation.Around;
import org.aspectj.lang.annotation.Aspect;
import org.springframework.stereotype.Component;

        import java.util.Date;

@Aspect
@Component
@Slf4j
public class UpLogFun {

    @Around("@annotation(upLog)")
    public Object around(ProceedingJoinPoint point, UpLog upLog) throws Throwable {
        String name  = upLog.value();
        if (StrUtil.isEmpty(name)){
            name = point.getSignature().getName();
        }
        log.info(name+"方法执行开始-----");
        Date startTime = new Date();
        Object o = point.proceed();
        log.info(name+"方法执行结束，总耗时：【"+(DateUtil.between(startTime, new Date(), DateUnit.SECOND))+"】秒-----");
        return o;
    }
}
```

- 测试类

```java
import com.xiong.demoaop.upLog.note.UpLog;
import lombok.extern.slf4j.Slf4j;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@Slf4j
public class LogController {

    @GetMapping("/getAbc")
    @UpLog("ASdfas")
    public String getAbc() throws InterruptedException {
        log.info("方法执行。。。。。");
        Thread.sleep(2360);
        return "方法返回值。。。。";
    }
}
```

### 测试

```http
http://localhost:8000/getAbc
```

## 自动转译字段

### 说明

#### 实体类三个字段

```java
@Data
@TableName(value = "t_user")
public class TUser {

    @TableId(value = "id", type = IdType.INPUT)
    private Long id;

    @TableField(value = "`name`")
    private String name;

    @TableField(value = "sex")
    @Dict(dicCode = "sex")
    private String sex;

}
```

#### 返回值四个字段

多一个转译后的字段

```json
{
  "code": 0,
  "data": {
    "id": 1,
    "name": "张三",
    "sex": "1",
    "sex_dict_text": "男"
  },
  "msg": "执行成功"
}
```

#### 代码逻辑说明

写两个注解，一个放到controller方法上，标明次方法，需要加强

第二个注解放到实体类的字段上，标明此字段需要加强

当进入切面类后，将需要加强的字段，的字段值取出，去数据库查询出对应的字典值

新增字段，并且重新拼装返回值

### 搭建

#### 数据库

```sql
-- ----------------------------
-- Table structure for t_dict
-- ----------------------------
DROP TABLE IF EXISTS `t_dict`;
CREATE TABLE `t_dict`  (
  `id` bigint NOT NULL,
  `dict_code` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NULL DEFAULT NULL COMMENT '字典编码',
  `dict_value` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NULL DEFAULT NULL COMMENT '字典值',
  `dict_key` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NULL DEFAULT NULL COMMENT '字典key',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_bin ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of t_dict
-- ----------------------------
INSERT INTO `t_dict` VALUES (1, 'sex', '男', '1');
INSERT INTO `t_dict` VALUES (2, 'sex', '女', '2');

-- ----------------------------
-- Table structure for t_user
-- ----------------------------
DROP TABLE IF EXISTS `t_user`;
CREATE TABLE `t_user`  (
  `id` bigint NOT NULL,
  `name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NULL DEFAULT NULL,
  `sex` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_bin ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of t_user
-- ----------------------------
INSERT INTO `t_user` VALUES (1, '张三', '1');

SET FOREIGN_KEY_CHECKS = 1;
```

#### pom

新增mybatisplus依赖

```xml
<dependency>
    <groupId>com.baomidou</groupId>
    <artifactId>mybatis-plus-boot-starter</artifactId>
    <version>3.4.0</version>
</dependency>
<dependency>
    <groupId>mysql</groupId>
    <artifactId>mysql-connector-java</artifactId>
    <version>8.0.19</version>
</dependency>
```

#### yml

```yaml
server:
  port: 8080

spring:
  hikari:
    connection-timeout: 60000
    idle-timeout: 500000
    max-lifetime: 540000
    maximum-pool-size: 10
    minimum-idle: 10
  datasource:
    url: jdbc:mysql://mysql.sqlpub.com:3306/java0417?serverTimezone=UTC&useUnicode=true&characterEncoding=utf-8&AllowPublicKeyRetrieval=True
    username: java0417
    password: f345c26699a412e2
  redis:
    # Redis服务器地址
    host: redis-13723.c114.us-east-1-4.ec2.cloud.redislabs.com
    # Redis服务器端口号
    port: 13723
    # 使用的数据库索引，默认是0
    database: 0
    # 连接超时时间
    timeout: 1800000
    # 设置密码
    password: "Nbz7s26fpJTB5TQn8WpSW2pAJeBI9xvf"
    lettuce:
      pool:
        # 最大阻塞等待时间，负数表示没有限制
        max-wait: -1
        # 连接池中的最大空闲连接
        max-idle: 5
        # 连接池中的最小空闲连接
        min-idle: 0
        # 连接池中最大连接数，负数表示没有限制
        max-active: 20

mybatis-plus:
  mapper-locations: mapper/*.xml
  configuration:
    log-impl: org.apache.ibatis.logging.stdout.StdOutImpl
  type-aliases-package: com.xiong.demoaop.entity
```

#### 两个注解类

```java
import java.lang.annotation.ElementType;
import java.lang.annotation.Retention;
import java.lang.annotation.RetentionPolicy;
import java.lang.annotation.Target;

/**
 * 字典注解，放到实体类上，用来标记需要被加强的字段，以及字典名称
 */
@Target(ElementType.FIELD)
@Retention(RetentionPolicy.RUNTIME)
public @interface Dict {

    /**
     * 字段code
     * @return
     */
    String dicCode();

}

```

```java
import java.lang.annotation.ElementType;
import java.lang.annotation.Retention;
import java.lang.annotation.RetentionPolicy;
import java.lang.annotation.Target;


/**
 * 字典注解，放到controller上，加强返回值
 */
@Target(ElementType.METHOD)
@Retention(RetentionPolicy.RUNTIME)
public @interface TranslateDict {

}

```

#### 切面类

```java
import cn.hutool.json.JSONObject;
import cn.hutool.json.JSONUtil;
import com.baomidou.mybatisplus.core.conditions.query.QueryWrapper;
import com.baomidou.mybatisplus.extension.api.R;
import com.xiong.demoaop.dict.note.Dict;
import com.xiong.demoaop.dict.entity.TDict;
import com.xiong.demoaop.dict.service.TDictService;
import lombok.extern.slf4j.Slf4j;
import org.aspectj.lang.ProceedingJoinPoint;
import org.aspectj.lang.annotation.Around;
import org.aspectj.lang.annotation.Aspect;
import org.aspectj.lang.annotation.Pointcut;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;

import java.lang.reflect.Field;

/**
 * @Description: 字典aop类
 * @Author: dangzhenghui
 * @Date: 2019-3-17 21:50
 * @Version: 1.0
 */
@Aspect
@Component
@Slf4j
public class DictAspect {

    @Autowired
    TDictService tDictService;


    // 定义切点Pointcut
    //@Pointcut("execution(public * com.sinoprof.sinoqualitymanage..*.*Controller.*(..))")
    @Pointcut("@annotation(com.xiong.demoaop.dict.note.TranslateDict)")
    public void excudeService() {
    }

    @Around("excudeService()")
    private Object parseDictText(ProceedingJoinPoint pjp) throws Throwable {
        // 执行方法，获取返回值
        Object result = pjp.proceed();
        //加强返回值
        // 判断返回值类型
        if (result instanceof R) {
            // 获取返回值
            Object data = ((R<?>) result).getData();
            // 获取返回值json对象（方便增加字段属性）
            JSONObject jsonObject = JSONUtil.parseObj(data);

            // 获取所有的属性
            Class<?> dataClass = data.getClass();
            Field[] fields=dataClass.getDeclaredFields();
            // 遍历属性
            for (Field field : fields){
                // 判断属性上是否有转译标记
                if (field.getAnnotation(Dict.class) != null) {
                    // 获取字典code
                    String code = field.getAnnotation(Dict.class).dicCode();
                    // 获取属性值
                    Object o = jsonObject.get(field.getName());
                    // 查询字典值
                    TDict tDict = tDictService.getBaseMapper().selectOne(new QueryWrapper<TDict>()
                            .eq("dict_code", code)
                            .eq("dict_key", o.toString()));
                    // 赋值
                    jsonObject.putOpt(field.getName()+"_dict_text",tDict.getDictValue());
                }
            }
            ((R<JSONObject>) result).setData(jsonObject);
        }
        return result;
    }

}
```

#### 实体类

```java
import com.baomidou.mybatisplus.annotation.IdType;
import com.baomidou.mybatisplus.annotation.TableField;
import com.baomidou.mybatisplus.annotation.TableId;
import com.baomidou.mybatisplus.annotation.TableName;
import lombok.Data;

@Data
@TableName(value = "t_dict")
public class TDict {
    @TableId(value = "id", type = IdType.INPUT)
    private Long id;

    /**
     * 字典编码
     */
    @TableField(value = "dict_code")
    private String dictCode;

    /**
     * 字典值
     */
    @TableField(value = "`dict_value`")
    private String dictValue;

    @TableField(value = "dict_key")
    private String dictKey;

}
```

```java
import com.baomidou.mybatisplus.annotation.IdType;
import com.baomidou.mybatisplus.annotation.TableField;
import com.baomidou.mybatisplus.annotation.TableId;
import com.baomidou.mybatisplus.annotation.TableName;
import com.xiong.demoaop.dict.note.Dict;
import lombok.Data;

@Data
@TableName(value = "t_user")
public class TUser {

    @TableId(value = "id", type = IdType.INPUT)
    private Long id;

    @TableField(value = "`name`")
    private String name;

    @TableField(value = "sex")
    @Dict(dicCode = "sex")
    private String sex;
}
```

#### mapper

```java
import com.baomidou.mybatisplus.core.mapper.BaseMapper;
import com.xiong.demoaop.dict.entity.TDict;
import org.apache.ibatis.annotations.Mapper;

@Mapper
public interface TDictMapper extends BaseMapper<TDict> {
}
```

```java
import com.baomidou.mybatisplus.core.mapper.BaseMapper;
import com.xiong.demoaop.dict.entity.TUser;
import org.apache.ibatis.annotations.Mapper;

@Mapper
public interface TUserMapper extends BaseMapper<TUser> {
}
```

#### service

```java
import com.xiong.demoaop.dict.entity.TDict;
import com.baomidou.mybatisplus.extension.service.IService;
public interface TDictService extends IService<TDict>{

}
```

```java
import com.xiong.demoaop.dict.entity.TUser;
import com.baomidou.mybatisplus.extension.service.IService;
public interface TUserService extends IService<TUser>{


}
```

```java
import org.springframework.stereotype.Service;
import com.baomidou.mybatisplus.extension.service.impl.ServiceImpl;
import com.xiong.demoaop.dict.mapper.TDictMapper;
import com.xiong.demoaop.dict.entity.TDict;
import com.xiong.demoaop.dict.service.TDictService;
@Service
public class TDictServiceImpl extends ServiceImpl<TDictMapper, TDict> implements TDictService{

}
```

```java
import org.springframework.stereotype.Service;
import com.baomidou.mybatisplus.extension.service.impl.ServiceImpl;
import com.xiong.demoaop.dict.entity.TUser;
import com.xiong.demoaop.dict.mapper.TUserMapper;
import com.xiong.demoaop.dict.service.TUserService;
@Service
public class TUserServiceImpl extends ServiceImpl<TUserMapper, TUser> implements TUserService{

}
```

#### controller

```java
import com.baomidou.mybatisplus.extension.api.R;
import com.xiong.demoaop.dict.note.TranslateDict;
import com.xiong.demoaop.dict.entity.TUser;
import com.xiong.demoaop.dict.service.TUserService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/dict")
public class DictController {

    @Autowired
    TUserService tUserService;

    @GetMapping("/test")
    @TranslateDict
    public R<TUser> test(){
        TUser tUser = tUserService.getBaseMapper().selectById(1);
        return R.ok(tUser);
    }
}
```

### 测试

```http
http://localhost:8080/dict/test
```

```json
{
  "code": 0,
  "data": {
    "id": 1,
    "name": "张三",
    "sex": "1",
    "sex_dict_text": "男"
  },
  "msg": "执行成功"
}
```

