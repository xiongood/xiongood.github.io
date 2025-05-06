---
title: apache-cxf的使用
summary: 根据约束文件生成webservice代码的工具，简单快捷，非常好用！
img: https://img.myfox.fun/img/cxf.jpg
categories:
 - 工具
tags:
 - windows
 - apache-cxf
---

## 下载

```http
https://cxf.apache.org/download.html
```

![image-20230523211134482](https://img.myfox.fun/img/20230523211136.png)

## 安装

- 配置环境变量

  ```txt
  CXF_HOME
  D:\app\other\apache-cxf-3.5.5
  ```

  ![image-20230418224945237](https://img.myfox.fun/img/image-20230418224945237.png)

```txt
%CXF_HOME%\bin
```



![image-20230418225139006](https://img.myfox.fun/img/image-20230418225139006.png)

## 使用

- 生成代码

  ```sh
  wsdl2java -encoding utf-8 -d E:\webserviceCode http://10.94.7.13:8080/cross/htj_2crs2_ws27/cross?wsdl
  ```

  ```sh
  # -d 输出路径
  # -client wsdl路径
  wsdl2java  -d D:\server\cxf\output -client D:\server\cxf\input\importPOViewSrv.wsdl
  
  # - 解决中文乱码
  wsdl2java -encoding utf-8 -d D:\server\cxf\output -client D:\server\cxf\input\OSB_SSCM_ZX_HQ_ImportOrderUpdateOrCancelSrv.wsdl
  ```

  

