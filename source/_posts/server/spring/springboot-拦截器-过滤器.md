---
title: springboot拦截器、过滤器的使用
img: https://gitee.com/xiongood/image/raw/master/springboot.jpg
categories:
 - 后端
tags:
 - java
 - springboot
---

## 说明

二者区别：

![image-20230428102735175](https://gitee.com/xiongood/image/raw/master/20230428102736.png)

### 过滤器

我理解的是，过滤器主要是对请求体进行处理，比如改变请求中的字符集、修改请求中的数据等

### 拦截器

我理解的是，拦截器主要是对请求进行加强，比如验证token、切换数据源等功能都能在此阶段处理

### 其他区别

我认为，因为过滤器不在servlet容器中，所以过滤器是不能用容器中的bean的。

## 拦截器

### 拦截器定义类

```java
import lombok.extern.slf4j.Slf4j;
import org.springframework.web.servlet.HandlerInterceptor;
import org.springframework.web.servlet.ModelAndView;

import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import javax.servlet.http.HttpSession;

/**
 * 登录检查
 * 1.配置到拦截器要拦截哪些请求
 * 2.把这些配置放在容器中
 *
 * 实现HandlerInterceptor接口
 */
@Slf4j
public class MyInterceptor implements HandlerInterceptor  {
    /**
     * 目标方法执行之前
     * 登录检查写在这里，如果没有登录，就不执行目标方法
     * @param request
     * @param response
     * @param handler
     * @return
     * @throws Exception
     */
    @Override
    public boolean preHandle(HttpServletRequest request, HttpServletResponse response, Object handler) throws Exception {
//      获取进过拦截器的路径
        String requestURI = request.getRequestURI();
        log.info("请求地址："+requestURI);
        //      登录检查逻辑
        HttpSession session = request.getSession();
        Object loginUser = session.getAttribute("loginUser");
        if(loginUser !=null){
//          放行
            return true;
        }
//      拦截   就是未登录,自动跳转到登录页面，然后写拦截住的逻辑
        return true;
    }

    /**
     * 目标方法执行完成以后
     * @param request
     * @param response
     * @param handler
     * @param modelAndView
     * @throws Exception
     */
    @Override
    public void postHandle(HttpServletRequest request, HttpServletResponse response, Object handler, ModelAndView modelAndView) throws Exception {
        log.info("执行完方法后……………………………………");
        HandlerInterceptor.super.postHandle(request, response, handler, modelAndView);
    }

    /**
     * 页面渲染以后
     * @param request
     * @param response
     * @param handler
     * @param ex
     * @throws Exception
     */
    @Override
    public void afterCompletion(HttpServletRequest request, HttpServletResponse response, Object handler, Exception ex) throws Exception {
        log.info("页面完成渲染后");
        HandlerInterceptor.super.afterCompletion(request, response, handler, ex);
    }
}
```

### 拦截器配置类

```java
import org.springframework.context.annotation.Configuration;
import org.springframework.web.servlet.config.annotation.InterceptorRegistry;
import org.springframework.web.servlet.config.annotation.WebMvcConfigurer;

/**
 * Web配置类
 */
@Configuration
public class WebConfig implements WebMvcConfigurer {
    /**
     * 添加Web项目的拦截器
     */
    @Override
    public void addInterceptors(InterceptorRegistry registry) {
        // 对所有访问路径，都通过MyInterceptor类型的拦截器进行拦截
        registry.addInterceptor(new MyInterceptor()).addPathPatterns("/**")
                .excludePathPatterns("/login", "/index.html", "/user/login", "/css/**",https://gitee.com/xiongood/image/raw/master/**", "/js/**", "/fonts/**");
        //放行登录页，登陆操作，静态资源
    }
}

```

## 过滤器

### 方式一(注解)

```java
import org.springframework.core.annotation.Order;
import org.springframework.stereotype.Component;

import javax.servlet.*;
import javax.servlet.annotation.WebFilter;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import java.io.IOException;

// 定义filterName 和过滤的url
//这里需要注意的是，urlPatterns是需要过滤的请求地址，这里我写的是urlPatterns = "/test/*，
//那这个过滤器过滤的是RequestMapping=@RequestMapping("/test")下面的所有方法，
//也就是一个controller层，如果想过滤所有数据就这样写：urlPatterns = "/*。
@Order(1)
@Component
@WebFilter(filterName = "myFilter" ,urlPatterns = "/*")
public class CommonFilterAnnotation implements Filter {
    /**
     * filter对象只会创建一次，init方法也只会执行一次。
     * @param filterConfig
     * @throws ServletException
     */
    @Override
    public void init(FilterConfig filterConfig) throws ServletException {
        System.out.println("CommonFilterAnnotation初始化完成....");
    }
    /**
     * 主要的业务代码编写方法
     * @param request
     * @param response
     * @param chain
     * @throws IOException
     * @throws ServletException
     */
    @Override
    public void doFilter(ServletRequest request, ServletResponse response, FilterChain chain)
            throws IOException, ServletException {
        System.out.println("啦啦啦");
        //获取session中保存的对象
        HttpServletRequest req = (HttpServletRequest) request;
        HttpServletResponse resp = (HttpServletResponse) response;

        //获取请求路径
        String servletPath = req.getServletPath();
        System.out.println( "servletPath = " + servletPath );

        if (servletPath.equals( "/test/test" )){
            String path = "/test/test2";
            //改变前端请求的后端路径为path
            req.getRequestDispatcher(path).forward(req,resp);
            //放行
            chain.doFilter( req,resp);
            return;
        }
        //放行请求
        chain.doFilter(request,response);
    }
    /**
     * 在销毁Filter时自动调用。
     */
    @Override
    public void destroy() {
        Filter.super.destroy();
    }
}

```

## 测试类

```java
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;


@RequestMapping("/test")
@RestController
public class TestController {


    @GetMapping("/test")
    public String test(){
        System.out.println("success!------------------------------");
        return "success!";
    }

    @GetMapping("/test2")
    public String test2(){
        System.out.println("test2-------------------------------------------");
        return "test2";
    }
}

```

