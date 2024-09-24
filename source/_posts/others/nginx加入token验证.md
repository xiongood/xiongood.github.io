## 环境配置

### 关闭防火墙

```sh
sudo systemctl stop firewalld
sudo systemctl disable firewalld
```



## 安装nginx

`带 ngx_http_auth_request_module`

### 安装依赖项

```sh
yum -y install gcc gcc-c++ pcre-devel zlib-devel openssl-devel
```

### 下载并且解压

```sh
wget https://mirrors.huaweicloud.com/nginx/nginx-1.9.9.tar.gz
tar -zxvf nginx-1.9.9.tar.gz 
cd nginx-1.9.9
# 根据需要添加其他模块  
#--prefix选项用于指定Nginx的安装目录。
./configure --prefix=/usr/local/nginx --with-http_auth_request_module --with-http_ssl_module --with-http_realip_module 

make  
make install
```

### 验证及启动

```sh
# 验证配置文件
/usr/local/nginx/sbin/nginx -t
# 启动
/usr/local/nginx/sbin/nginx
# 停止
/usr/local/nginx/sbin/nginx -s stop
```

## 配置token验证

在Nginx中增加token验证，通常涉及到几个步骤，包括配置Nginx以解析HTTP请求中的token，验证这个token的有效性，以及根据验证结果允许或拒绝访问。这里将提供一个基本的实现思路，它依赖于Nginx的第三方模块如`ngx_http_auth_request_module`或者`ngx_http_lua_module`来实现更复杂的逻辑。

### 使用`ngx_http_auth_request_module`

1. **安装Nginx并确认`ngx_http_auth_request_module`已启用**：这个模块通常在Nginx编译时加入。如果你没有启用这个模块，需要重新编译Nginx。

2. **配置Nginx以使用`auth_request`指令**：这个指令会向指定的URL发送一个子请求，并根据子请求的响应状态码来决定是否允许主请求。

   ```nginx
   
   #user  nobody;
   worker_processes  1;
   
   #error_log  logs/error.log;
   #error_log  logs/error.log  notice;
   #error_log  logs/error.log  info;
   
   #pid        logs/nginx.pid;
   
   
   events {
       worker_connections  1024;
   }
   
   
   http {
       include       mime.types;
       default_type  application/octet-stream;
       sendfile        on;
       keepalive_timeout  65;
   
   
       server {  
   	    	listen 80;  
   	  	server_name  localhost;  
           	# 请求的地址
   	    	location /protected/ {  
   	    		# 先校验令牌是否有效
   	    		auth_request /auth;  
   		     	# 只有在认证请求返回 2xx 时才继续处理请求  
   		     	error_page 401 = @error401;  
   		 		# 将地址指向本地文件
   		 		alias   /opt/data/;  
   		   		autoindex on;  
   	    	}  
   
           # 验证令牌
   		location = /auth {  
   	        # 认证服务的 URL  
   	        internal;  
               # 令牌验证服务器
   	        proxy_pass http://192.168.18.1:8081/validate;  
   	        proxy_pass_request_body off;  
   	        proxy_set_header Content-Length "";  
   	        proxy_set_header X-Original-URI $request_uri;  
   	  
   	        # 从认证服务接收的响应头（可选）  
   	        proxy_set_header Host $host;  
   	        proxy_set_header X-Real-IP $remote_addr;  
   	        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;  
   	        proxy_set_header X-Forwarded-Proto $scheme;  
   	  
   	        # 认证服务应返回 200 或 401  
   	        proxy_intercept_errors on;  
   	    }  
   
           # 令牌失败时返回值
   	    	location @error401 {  
   	        # 认证失败时的处理  
   	        return 401 'Authorization Required';  
   	     } 
   	}
   
   
       
   }
   
   ```
   
   注意：你需要将`http://auth-service/validate-token`替换为实际验证token的URL。

### 后端令牌校验逻辑

pom

```xml
<dependency>
			<groupId>org.springframework.boot</groupId>
			<artifactId>spring-boot-starter-web</artifactId>
		</dependency>
		<dependency>
			<groupId>org.projectlombok</groupId>
			<artifactId>lombok</artifactId>
			<version>1.18.26</version>
		</dependency>

		<dependency>
			<groupId>cn.hutool</groupId>
			<artifactId>hutool-all</artifactId>
			<version>5.4.0</version>
		</dependency>
		<dependency>
			<groupId>io.jsonwebtoken</groupId>
			<artifactId>jjwt</artifactId>
			<version>0.9.1</version> <!-- 请检查是否有更新的版本 -->
		</dependency>
```

java

```java
package com.pj.controller;

import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestHeader;
import org.springframework.web.bind.annotation.RestController;


@RestController
public class TestController {

    @GetMapping("/validate")
    public ResponseEntity<String> validateJwt(@RequestHeader("Authorization") String authorizationHeader) {
        // 从Authorization头中提取JWT令牌
        String jwt = authorizationHeader.replace("Bearer ", "");

        try {
            // 如果令牌正确：
            if ("123".equals(jwt)){
                // 如果JWT有效，返回成功响应
                return ResponseEntity.ok("领票有效");
            }else {
                // 如果令牌无效
                return ResponseEntity.status(HttpStatus.UNAUTHORIZED).body("令牌无效");
            }
        } catch (Exception e) {
            // 如果JWT无效或解析失败，返回错误响应
            return ResponseEntity.status(HttpStatus.UNAUTHORIZED).body("令牌无效");

        }
    }
}

```

### 测试

```http
// 服务器
localhost:8081/validate
// nginx
http://192.168.18.135/protected/
```

![image-20240923140808416](https://pub-b24cf0a8c1f14e9386435977aa464959.r2.dev/img/image-20240923140808416.png)
