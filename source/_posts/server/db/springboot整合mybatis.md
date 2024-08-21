---
title: springboot整合mybatis
img: ../https://pub-b24cf0a8c1f14e9386435977aa464959.r2.dev/img/20230816111548.png
categories:
 - 后端
tags:
 - mybatis
 - java
---



## 实现批量新增

近期一直用mybatisplus，然后发现在mybatis-plus中的批量新增方法，其实也是循环的执行多条语句，这势必会对数据库造成一定的压力，

所以用了mybaits-plus，写批量新增的试试，还是得用mybatis原生的方法。

需要注意的是，不通数据库，对sql语句的大小有不通的限制，当批量的数据过大时，需要分批新增，否则会抛出异常

### mapper类

```java
//批量新增方法
int saveBatch(List<SysUser> list);
```

### xml配置文件

```xml
<insert id="saveBatch"  parameterType="java.util.List" >
    INSERT INTO sys_user (user_name,nick_name) VALUES
    <foreach collection="list" item="item" separator=",">
        (
        #{item.userName},#{item.nickName}
        )
    </foreach>
</insert>
```

### 测试类

```java
import com.example.xiong.entity.SysUser;
import com.example.xiong.mapper.SysUserMapper;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;

import java.util.ArrayList;
import java.util.List;

@SpringBootTest
class MybatisApplicationTests {

    @Autowired
    SysUserMapper sysUserMapper;

    @Test
    void saveBatch(){
        List<SysUser> list = new ArrayList<>();
        for (int i = 0; i < 5; i++) {
            SysUser sysUser = new SysUser();
            sysUser.setUserName("userName"+i);
            sysUser.setNickName("nickName"+i);
            list.add(sysUser);
        }
        sysUserMapper.saveBatch(list);
        int i = sysUserMapper.saveBatch(list);
        System.out.println("保存了"+i+"条");
    }
}

```



## 基础搭建

### pom
```xml
<!-- https://mvnrepository.com/artifact/com.mysql/mysql-connector-j -->
<dependency>
    <groupId>com.mysql</groupId>
    <artifactId>mysql-connector-j</artifactId>
    <version>8.0.33</version>
</dependency>

<!-- https://mvnrepository.com/artifact/org.mybatis.spring.boot/mybatis-spring-boot-starter -->
<dependency>
    <groupId>org.mybatis.spring.boot</groupId>
    <artifactId>mybatis-spring-boot-starter</artifactId>
    <version>3.0.0</version>
</dependency>
```
### 配置文件
```yaml
server:
  port: 8889
spring:
  # 默认连接池
  hikari:
    connection-timeout: 60000 #连接超时时间：毫秒，小于250毫秒，否则被重置为默认值30秒
    idle-timeout: 500000 #空闲连接超时时间，默认值600000（10分钟），大于等于max-lifetime且max-lifetime>0，会被重置为0；不等于0且小于10秒，会被重置为10秒
    max-lifetime: 540000 #连接最大存活时间，不等于0且小于30秒，会被重置为默认值30分钟.设置应该比mysql设置的超时时间短
    maximum-pool-size: 5 #最大连接数，小于等于0会被重置为默认值10；大于零小于1会被重置为minimum-idle的值
    minimum-idle: 1 # 最小空闲连接，默认值10，小于0或大于maximum-pool-size，都会重置为maximum-pool-size
  # 数据源
  datasource:
    url: jdbc:mysql://mysql.sqlpub.com:3306/xiong_mybatis?serverTimezone=UTC&useUnicode=true&characterEncoding=utf-8&AllowPublicKeyRetrieval=True
    username: xiong_mybatis
    password: c519857aae2dafa5

# mybatis 配置
mybatis:
  ## 解决多模块映射错误的问题
  mapper-locations: classpath*:mapper/*.xml
  type-aliases-package: com.example.xiong.entity

# 打印sql
logging:
  level:
    com.example.xiong.mapper: debug
```
### 实体类
```java
import java.io.Serializable;
import java.util.Date;
import lombok.Data;

/**
 * 用户信息表
 * @TableName sys_user
 */
@Data
public class SysUser implements Serializable {
    /**
     * 用户ID
     */
    private Long userId;

    /**
     * 部门ID
     */
    private Long deptId;

    /**
     * 用户账号
     */
    private String userName;

    /**
     * 用户昵称
     */
    private String nickName;

    /**
     * 用户类型（00系统用户）
     */
    private String userType;

    /**
     * 用户邮箱
     */
    private String email;

    /**
     * 手机号码
     */
    private String phonenumber;

    /**
     * 用户性别（0男 1女 2未知）
     */
    private String sex;

    /**
     * 头像地址
     */
    private String avatar;

    /**
     * 密码
     */
    private String password;

    /**
     * 帐号状态（0正常 1停用）
     */
    private String status;

    /**
     * 删除标志（0代表存在 2代表删除）
     */
    private String delFlag;

    /**
     * 最后登录IP
     */
    private String loginIp;

    /**
     * 最后登录时间
     */
    private Date loginDate;

    /**
     * 创建者
     */
    private String createBy;

    /**
     * 创建时间
     */
    private Date createTime;

    /**
     * 更新者
     */
    private String updateBy;

    /**
     * 更新时间
     */
    private Date updateTime;

    /**
     * 备注
     */
    private String remark;

    private static final long serialVersionUID = 1L;
}
```
### mapper 类
```java
-import com.example.xiong.entity.SysUser;
import org.apache.ibatis.annotations.Mapper;

import java.util.List;

-
@Mapper
public interface SysUserMapper {

    int deleteByPrimaryKey(Long id);

}

```

### mybatis的xml
```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE mapper
        PUBLIC "-//mybatis.org//DTD Mapper 3.0//EN"
        "http://mybatis.org/dtd/mybatis-3-mapper.dtd">
<mapper namespace="com.example.xiong.mapper.SysUserMapper">

    <resultMap id="BaseResultMap" type="com.example.xiong.entity.SysUser">
            <id property="userId" column="user_id" jdbcType="BIGINT"/>
            <result property="deptId" column="dept_id" jdbcType="BIGINT"/>
            <result property="userName" column="user_name" jdbcType="VARCHAR"/>
            <result property="nickName" column="nick_name" jdbcType="VARCHAR"/>
            <result property="userType" column="user_type" jdbcType="VARCHAR"/>
            <result property="email" column="email" jdbcType="VARCHAR"/>
            <result property="phonenumber" column="phonenumber" jdbcType="VARCHAR"/>
            <result property="sex" column="sex" jdbcType="CHAR"/>
            <result property="avatar" column="avatar" jdbcType="VARCHAR"/>
            <result property="password" column="password" jdbcType="VARCHAR"/>
            <result property="status" column="status" jdbcType="CHAR"/>
            <result property="delFlag" column="del_flag" jdbcType="CHAR"/>
            <result property="loginIp" column="login_ip" jdbcType="VARCHAR"/>
            <result property="loginDate" column="login_date" jdbcType="TIMESTAMP"/>
            <result property="createBy" column="create_by" jdbcType="VARCHAR"/>
            <result property="createTime" column="create_time" jdbcType="TIMESTAMP"/>
            <result property="updateBy" column="update_by" jdbcType="VARCHAR"/>
            <result property="updateTime" column="update_time" jdbcType="TIMESTAMP"/>
            <result property="remark" column="remark" jdbcType="VARCHAR"/>
    </resultMap>

    <sql id="Base_Column_List">
        user_id,dept_id,user_name,
        nick_name,user_type,email,
        phonenumber,sex,avatar,
        password,status,del_flag,
        login_ip,login_date,create_by,
        create_time,update_by,update_time,
        remark
    </sql>

    <select id="selectByPrimaryKey" parameterType="java.lang.Long" resultMap="BaseResultMap">
        select
        <include refid="Base_Column_List" />
        from sys_user
        where  user_id = #{userId,jdbcType=BIGINT} 
    </select>
    
</mapper>
```

