---
title: springboot整合sa-token
categories:
 - 后端
tags:
 - sa-token
 - java
 - springboot
---

## 说明

springSecurity是老外的老牌的安全框架，在实际工作中百分之八九十的项目，用的都是这个框架。

springSecurity，用的都是各种自定义的过滤器，对于新手来说，学习成本比较高。

而sa-token 相对于springSecurity来说，更加轻量，更容易上手。最重要的是这是国人开发的安全框架，其设计思想更符合中国人的思维，
而且文档都是中文，对国人的开发人员来说非常的友好。

我已经关注sa-token好多年了，并且曾将其引入到了实际生产项目中。

下面做一些使用说明

## 表结构设计

### 设计图

![image-20230511095101617](https://img.myfox.fun/img/20230511095102.png)

### sql

```sql
ET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for sys_permissions
-- ----------------------------
DROP TABLE IF EXISTS `sys_permissions`;
CREATE TABLE `sys_permissions`  (
  `id` int NOT NULL COMMENT 'id',
  `permission_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '权限名称',
  `permission_code` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '权限代码',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci COMMENT = '权限表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of sys_permissions
-- ----------------------------
INSERT INTO `sys_permissions` VALUES (1, '读', 'P-RADE');
INSERT INTO `sys_permissions` VALUES (2, '写', 'p_WRITE');

-- ----------------------------
-- Table structure for sys_role
-- ----------------------------
DROP TABLE IF EXISTS `sys_role`;
CREATE TABLE `sys_role`  (
  `id` int NOT NULL COMMENT 'id',
  `role_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '角色名称',
  `role_code` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '角色编码',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci COMMENT = '角色表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of sys_role
-- ----------------------------
INSERT INTO `sys_role` VALUES (1, '管理员', 'R-ADMIN');
INSERT INTO `sys_role` VALUES (2, '用户', 'R-USER');

-- ----------------------------
-- Table structure for sys_role_permission
-- ----------------------------
DROP TABLE IF EXISTS `sys_role_permission`;
CREATE TABLE `sys_role_permission`  (
  `id` int NOT NULL COMMENT 'id',
  `role_code` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '角色编号',
  `permission_code` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '权限编号',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci COMMENT = '角色权限关联表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of sys_role_permission
-- ----------------------------
INSERT INTO `sys_role_permission` VALUES (1, 'R-ADMIN', 'P-RADE');
INSERT INTO `sys_role_permission` VALUES (2, 'R-ADMIN', 'P-WRITE');
INSERT INTO `sys_role_permission` VALUES (3, 'R-USER', 'P-RADE');

-- ----------------------------
-- Table structure for sys_user
-- ----------------------------
DROP TABLE IF EXISTS `sys_user`;
CREATE TABLE `sys_user`  (
  `id` int NOT NULL COMMENT 'id',
  `username` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '登录名',
  `password` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '登录密码',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci COMMENT = '用户表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of sys_user
-- ----------------------------
INSERT INTO `sys_user` VALUES (1, 'admin', '123456');
INSERT INTO `sys_user` VALUES (2, 'user', '123456');

-- ----------------------------
-- Table structure for sys_user_role
-- ----------------------------
DROP TABLE IF EXISTS `sys_user_role`;
CREATE TABLE `sys_user_role`  (
  `id` int NOT NULL COMMENT 'id',
  `user_id` int NULL DEFAULT NULL COMMENT '用户id',
  `role_no` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '角色编码',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci COMMENT = '用户角色关联表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of sys_user_role
-- ----------------------------
INSERT INTO `sys_user_role` VALUES (1, 1, 'R-ADMIN');
INSERT INTO `sys_user_role` VALUES (2, 2, 'R-USER');

SET FOREIGN_KEY_CHECKS = 1;
```

## 基础架构

整合 springboot+mybatisplus+hutool+lombok

数据库mysql

不再粘贴写代码，源码在：

```http
https://gitee.com/erhu02/demo
```

![image-20230511172412894](https://img.myfox.fun/img/20230511172413.png)

## 实现登录认证

### 官网

```http
https://sa-token.cc/doc.html#/
```

### 添加依赖

```xml
<!-- Sa-Token 权限认证，在线文档：https://sa-token.cc -->
<dependency>
    <groupId>cn.dev33</groupId>
    <artifactId>sa-token-spring-boot-starter</artifactId>
    <version>1.34.0</version>
</dependency>
<!-- Sa-Token 整合 jwt -->
<dependency>
    <groupId>cn.dev33</groupId>
    <artifactId>sa-token-jwt</artifactId>
    <version>1.34.0</version>
</dependency>
```

### 配置文件

```yaml
sa-token:
  # token名称 (同时也是cookie名称)
  token-name: satoken
  # token有效期，单位s 默认30天, -1代表永不过期
  timeout: 2592000
  # token临时有效期 (指定时间内无操作就视为token过期) 单位: 秒
  activity-timeout: -1
  # 是否允许同一账号并发登录 (为true时允许一起登录, 为false时新登录挤掉旧登录)
  is-concurrent: true
  # 在多人登录同一账号时，是否共用一个token (为true时所有登录共用一个token, 为false时每次登录新建一个token)
  is-share: true
  # token风格
  token-style: uuid
  # 是否输出操作日志
  is-log: false
```

### 创建请求拦截器

addInterceptors：拦截器主要方法

getStpLogicJwt：token转换为jwt风格

```java
import cn.dev33.satoken.context.SaHolder;
import cn.dev33.satoken.filter.SaServletFilter;
import cn.dev33.satoken.interceptor.SaInterceptor;
import cn.dev33.satoken.jwt.StpLogicJwtForSimple;
import cn.dev33.satoken.router.SaRouter;
import cn.dev33.satoken.stp.StpLogic;
import cn.dev33.satoken.stp.StpUtil;
import com.xiong.demo.utils.R;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.web.servlet.config.annotation.InterceptorRegistry;
import org.springframework.web.servlet.config.annotation.WebMvcConfigurer;

/**
 * @Auther: 张一雄
 * @Date: 2023/5/11 18:12
 * @Description: SaTokenConfigure
 * @Version 1.0.0
 */
@Configuration
public class SaTokenConfigure implements WebMvcConfigurer {
    @Override
    public void addInterceptors(InterceptorRegistry registry) {
        // 注册 Sa-Token 拦截器，定义详细认证规则
        registry.addInterceptor(new SaInterceptor(handler -> {
            // 指定一条 match 规则
            SaRouter
                    .match("/**")    // 拦截的 path 列表，可以写多个 */
                    .notMatch("/auth/doLogin")        // 排除掉的 path 列表，可以写多个
                    .check(r -> StpUtil.checkLogin());        // 要执行的校验动作，可以写完整的 lambda 表达式

            // 根据路由划分模块，不同模块不同鉴权
            SaRouter.match("/user/**", r -> StpUtil.checkPermission("user"));
            SaRouter.match("/admin/**", r -> StpUtil.checkPermission("admin"));
            SaRouter.match("/goods/**", r -> StpUtil.checkPermission("goods"));
            SaRouter.match("/orders/**", r -> StpUtil.checkPermission("orders"));
            SaRouter.match("/notice/**", r -> StpUtil.checkPermission("notice"));
            SaRouter.match("/comment/**", r -> StpUtil.checkPermission("comment"));
        })).addPathPatterns("/**");
    }


    // Sa-Token 整合 jwt (Simple 简单模式)
    @Bean
    public StpLogic getStpLogicJwt() {
        return new StpLogicJwtForSimple();
    }
}
```

### 创建统一异常拦截类

其实 还可以搞一个自定义异常类

```java
import cn.dev33.satoken.util.SaResult;
import com.xiong.demo.utils.R;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.RestControllerAdvice;

/**
 * @Auther: 张一雄
 * @Date: 2023/5/11 18:24
 * @Description: GlobalExceptionHandler
 * @Version 1.0.0
 */
@RestControllerAdvice
public class GlobalExceptionHandler {
    // 全局异常拦截
    @ExceptionHandler
    public R handlerException(Exception e) {
        e.printStackTrace();
        return R.error(e.getMessage());
    }
}
```

### 接下来写登录方法

#### 接口

```java
import com.example.xiong.entity.SysUser;
import com.xiong.demo.utils.R;

/**
 * @Auther: 张一雄
 * @Date: 2023/5/11 17:33
 * @Description: AuthService
 * @Version 1.0.0
 */
public interface AuthService {

    R doLogin(SysUser sysUser) ;
}

```

### 实现类

整合了 生成jwt风格token及解析jwt的代码

没有写对密码的加密解密功能

```java
import cn.dev33.satoken.stp.SaLoginConfig;
import cn.dev33.satoken.stp.SaLoginModel;
import cn.dev33.satoken.stp.StpUtil;
import com.baomidou.mybatisplus.core.conditions.query.QueryWrapper;
import com.example.xiong.entity.SysUser;
import com.example.xiong.service.impl.AuthService;
import com.example.xiong.service.impl.SysUserService;
import com.xiong.demo.utils.R;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

/**
 * @Auther: 张一雄
 * @Date: 2023/5/11 17:33
 * @Description: AuthServiceImpl
 * @Version 1.0.0
 */
@Service
@Slf4j
public class AuthServiceImpl implements AuthService {

    @Autowired
    SysUserService sysUserService;

    /**
     * 详细描述: 登录
     * @author 张一雄
     * @return { com.example.xiong.utils.R }
     * @exception/throws
     * 创建日期: 2023/5/11 17:35
     */
    public R doLogin(SysUser sysUser) {
        // 查询
        SysUser sysUser1 = sysUserService.getOne(new QueryWrapper<SysUser>().eq("username", sysUser.getUsername()));
        // 对比

        // 普通登录
        //StpUtil.login(sysUser.getId());

        // jwt 风格
        SaLoginModel loginModel = SaLoginConfig.setTimeout(1000*60*30)
                                .setExtra("name",sysUser1.getUsername())
                                .setExtra("age",18);

        StpUtil.login(sysUser1.getId(), loginModel);
        //得到token
        String tokenValue = StpUtil.getTokenValue();
        // 解析jwt的token
        String name = (String) StpUtil.getExtra("name");
        // 解析token
        // 返回值
        return R.ok(name,tokenValue);



        //StpUtil.logout();// 当前会话注销登录
        //StpUtil.isLogin();// 获取当前会话是否已经登录，返回true=已登录，false=未登录
        //StpUtil.checkLogin();// 检验当前会话是否已经登录, 如果未登录，则抛出异常：`NotLoginException`

        // 获取当前会话账号id, 如果未登录，则抛出异常：`NotLoginException`
        //StpUtil.getLoginId();

        // 类似查询API还有：
        //StpUtil.getLoginIdAsString();    // 获取当前会话账号id, 并转化为`String`类型
        //StpUtil.getLoginIdAsInt();       // 获取当前会话账号id, 并转化为`int`类型
        //StpUtil.getLoginIdAsLong();      // 获取当前会话账号id, 并转化为`long`类型

        // ---------- 指定未登录情形下返回的默认值 ----------
        // 获取当前会话账号id, 如果未登录，则返回null
        //StpUtil.getLoginIdDefaultNull();

        // 获取当前会话账号id, 如果未登录，则返回默认值 （`defaultValue`可以为任意类型）
        //StpUtil.getLoginId(T defaultValue);


        // 获取当前会话的token值
        //StpUtil.getTokenValue();

        // 获取当前`StpLogic`的token名称
        //StpUtil.getTokenName();

        // 获取指定token对应的账号id，如果未登录，则返回 null
        //StpUtil.getLoginIdByToken(String tokenValue);

        // 获取当前会话剩余有效期（单位：s，返回-1代表永久有效）
        //StpUtil.getTokenTimeout();

        // 获取当前会话的token信息参数
        //StpUtil.getTokenInfo();

    }
}

```

### controller类

第一个

```java
import cn.dev33.satoken.stp.StpUtil;
import com.example.xiong.entity.SysUser;
import com.example.xiong.service.impl.AuthService;
import com.xiong.demo.utils.R;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

/**
 * @Auther: 张一雄
 * @Date: 2023/5/11 17:32
 * @Description: UserController
 * @Version 1.0.0
 */
@RestController
@RequestMapping("/auth/")
public class AuthController {

    @Autowired
    AuthService authService;

    /**
     * 详细描述: 登录
     * @author 张一雄
     * @return { com.example.xiong.utils.R }
     * @exception/throws
     * 创建日期: 2023/5/11 17:36
     */
    @PostMapping("doLogin")
    public R doLogin(@RequestBody SysUser sysUser) {
        return authService.doLogin(sysUser);
    }

    /**
     * 详细描述: 判断当前用户是否登录
     * @author 张一雄
     * @return { java.lang.String }
     * @exception/throws
     * 创建日期: 2023/5/11 17:40
     */
    @RequestMapping("isLogin")
    public String isLogin() {
        return "当前会话是否登录：" + StpUtil.isLogin();
    }
}
```

第二个

```java
import com.example.xiong.service.impl.SysUserService;
import com.xiong.demo.utils.R;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

/**
 * @Auther: 张一雄
 * @Date: 2023/5/11 17:15
 * @Description: TestController
 * @Version 1.0.0
 */
@RestController
@RequestMapping("/test")
public class TestController {

    @Autowired
    SysUserService sysUserService;

    @GetMapping("count")
    public R count(){
        long count = sysUserService.count();
        return R.ok("总条数："+count);
    }
}
```



### 测试

- 登录

```http
POST http://localhost:8080/auth/doLogin
```

```json
{
    "username":"admin",
    "password":"123456"
}
```

返回信息

```json
{
    "status": 200,
    "message": "xiong",
    "data": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJsb2dpblR5cGUiOiJsb2dpbiIsImxvZ2luSWQiOjEsInJuU3RyIjoiZmJ6THhOWkQzTko0bjl2cVBEMUdockg1eVBmeFZFUzYiLCJuYW1lIjoieGlvbmciLCJhZ2UiOjE4fQ.PHbejqIrgXdhlHigDegMTe8xk-Wx47tghMvZzka54U0",
    "timestamp": "2023-05-11 18:47:47"
}
```

- 测试普通请求

```http
GET http://localhost:8080/test/count
```

测试 postman中已经有了 cookies信息

![image-20230511185825257](https://img.myfox.fun/img/20230511185826.png)

如果没有cookies,则写下请求头中也可以通过认证

![image-20230511185905431](https://img.myfox.fun/img/20230511185906.png)





























