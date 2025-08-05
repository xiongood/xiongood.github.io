---
title: mybatis-plus-分页
categories:
 - 后端
tags:
 - mybatis-plus
 - java
---

## 插件

### 配置插件

```java
import com.baomidou.mybatisplus.annotation.DbType;
import com.baomidou.mybatisplus.autoconfigure.ConfigurationCustomizer;
import com.baomidou.mybatisplus.extension.plugins.MybatisPlusInterceptor;
import com.baomidou.mybatisplus.extension.plugins.PaginationInterceptor;
import com.baomidou.mybatisplus.extension.plugins.inner.PaginationInnerInterceptor;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Configuration
public class MyBatisPlusConfig {

    /**
     * 新的分页插件,一缓和二缓遵循mybatis的规则,需要设置 MybatisConfiguration#useDeprecatedExecutor = false 避免缓存出现问题(该属性会在旧插件移除后一同移除)
     */
    @Bean
    public MybatisPlusInterceptor mybatisPlusInterceptor() {
        MybatisPlusInterceptor interceptor = new MybatisPlusInterceptor();
        interceptor.addInnerInterceptor(new PaginationInnerInterceptor(DbType.MYSQL));
        return interceptor;
    }
}
```

### 测试

```java
@Test
void testPage(){
    Page<SysUser> page = new Page<>(1,5);
    QueryWrapper<SysUser> queryWrapper = new QueryWrapper<>();
    queryWrapper.orderByDesc("user_id");
    page = sysUserService.page(page);
    System.out.println(page);
}
```

## PageHelper

### pom

```xml
<dependency>
    <groupId>com.github.pagehelper</groupId>
    <artifactId>pagehelper-spring-boot-starter</artifactId>
    <version>1.4.6</version>
</dependency>
```

### 测试

```java
@Test
void testPage2(){
    // 设置分页参数，第一页，分页条数为10
    PageHelper.startPage(1, 10);
    // 开始查询
    List<SysUser> list = sysUserService.getBaseMapper().selectList(new QueryWrapper<SysUser>().orderByDesc("user_id"));
    // 将查询结果包装到PageInfo，PageInfo中包含了页码，查询结果，当前页码等信息
    PageInfo pageInfo = new PageInfo<>(list);
    System.out.println(pageInfo);
}
```



