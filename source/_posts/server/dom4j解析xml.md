---
title: dom4j解析xml
author: 张一雄
summary: 解析xml的神器，用webservice的时候，经常会解析xml，这是就是dom4j大展神威的时候
img: https://img.myfox.fun/img/xml.jpg
categories:
 - 后端
tags:
 - xml
 - dom4j
 - java
 - jaxb
---

## 说明

最近因为一直在搞webService，所以一直在和xml打交道。所以想写一篇关于xml解析的dom4j的工具使用博客

本篇使用dom4j 2.1.4

主要介绍如何用基于注解的方式，对bean和xml进行转换

```xml
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<soapenv:myRoot xmlns:impl="http://impl.service.importPOConfirmStateUpdateSrv.zx.interfaces.sinointerfaces.sinoprof.com/" 
                xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" 
                xmlns:ns1="http://www.tibco.com/namespaces/bc/2002/04/partyinfo.xsd">
    <header>
        <ns1:name>测试报文</ns1:name>
        <from>保姆</from>
        <to>厨子</to>
    </header>
    <body>
        <name>信件</name>
        <param xsi:type="Param1" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
            <name>信件名称</name>
        </param>
    </body>
</soapenv:myRoot>
```

## BeanToXml

### 首先指定命名空间

创建package-info.java（必须叫这个名字）

命名空间会自动添加到根节点上

```java
@XmlSchema(
        xmlns={
                @XmlNs(prefix="soapenv", namespaceURI="http://schemas.xmlsoap.org/soap/envelope/"),
                @XmlNs(prefix="impl", namespaceURI="http://impl.service.importPOConfirmStateUpdateSrv.zx.interfaces.sinointerfaces.sinoprof.com/"),
                @XmlNs(prefix="ns1", namespaceURI="http://www.tibco.com/namespaces/bc/2002/04/partyinfo.xsd"),
        }
)
package com.xiong.demo.test2;

import javax.xml.bind.annotation.XmlNs;
import javax.xml.bind.annotation.XmlSchema;
```

如同这样

![image-20230525175733597](https://img.myfox.fun/img/20230525175734.png)

### 创建 header

```java
package com.xiong.demo.test2;

import lombok.Data;

import javax.xml.bind.annotation.XmlAccessType;
import javax.xml.bind.annotation.XmlAccessorType;
import javax.xml.bind.annotation.XmlElement;
import javax.xml.bind.annotation.XmlType;

/**
 * @Auther: 张一雄
 * @Date: 2023/5/25 17:39
 * @Description: MyHeader
 * @Version 1.0.0
 */
@XmlAccessorType(XmlAccessType.FIELD)
@XmlType(name = "MyHeader",
        propOrder = {
                "name",
                "from",
                "to"
        })
@Data
public class MyHeader {

    @XmlElement(name = "ns1:name", required = true)
    private String name = "测试报文";

    @XmlElement(name = "from", required = true)
    private String from = "保姆";

    @XmlElement(name = "to", required = true)
    private String to = "厨子";

}

```

对用的报文

![image-20230525180138254](https://img.myfox.fun/img/20230525180139.png)

### 创建body

#### 创建body之前

先创建两个 对象，作为body的参数，然后我们在后续测试时，可以动态的切换两个对象

```java
package com.xiong.demo.test2;

import lombok.Data;

import javax.xml.bind.annotation.XmlAccessType;
import javax.xml.bind.annotation.XmlAccessorType;
import javax.xml.bind.annotation.XmlElement;
import javax.xml.bind.annotation.XmlType;

/**
 * @Auther: 张一雄
 * @Date: 2023/5/25 17:41
 * @Description: Param1
 * @Version 1.0.0
 */
@XmlAccessorType(XmlAccessType.FIELD)
@XmlType(name = "Param1",
        propOrder = {
                "name"
        })
@Data
public class Param1 {
    @XmlElement(name = "name", required = true)
    private String name = "信件名称";
}

```

```java
package com.xiong.demo.test2;

import lombok.Data;

import javax.xml.bind.annotation.XmlAccessType;
import javax.xml.bind.annotation.XmlAccessorType;
import javax.xml.bind.annotation.XmlElement;
import javax.xml.bind.annotation.XmlType;

/**
 * @Auther: 张一雄
 * @Date: 2023/5/25 17:41
 * @Description: Param1
 * @Version 1.0.0
 */
@XmlAccessorType(XmlAccessType.FIELD)
@XmlType(name = "Param2",
        propOrder = {
                "name",
                "context"
        })
@Data
public class Param2 {
    @XmlElement(name = "name", required = true)
    private String name = "信件名称";

    @XmlElement(name = "context", required = true)
    private String context = "信件内容";

}

```

#### 创建body

```java
package com.xiong.demo.test2;

import lombok.Data;
import javax.xml.bind.annotation.*;

/**
 * @Auther: 张一雄
 * @Date: 2023/5/25 17:39
 * @Description: MyBody
 * @Version 1.0.0
 */

@XmlAccessorType(XmlAccessType.FIELD)
@XmlType(name = "Body",
        propOrder = {
                "name",
                "param"
        })
// 这里要把可能被切换到的对象的class写进去，否则会抛出异常
@XmlSeeAlso({Param2.class, Param1.class})
@Data
public class MyBody<T> {

    @XmlElement(name = "name", required = true)
    private String name = "信件";

    private T param; // 这里动态的切换对象

}

```

body 对应的报文

![image-20230525180500435](https://img.myfox.fun/img/20230525180501.png)

### 写根目录

```java
package com.xiong.demo.test2;

import lombok.Data;

import javax.xml.bind.annotation.*;

/**
 * @Auther: 张一雄
 * @Date: 2023/5/25 17:37
 * @Description: MyRoot
 * @Version 1.0.0
 */

@XmlAccessorType(XmlAccessType.FIELD)
@XmlType(propOrder = {
        "header",
        "body"
})
// 标签名称
@XmlRootElement(name = "soapenv:myRoot" )
@Data
public class MyRoot {

    // 标签名称
    @XmlElement(name = "header", required = true)
    public MyHeader header = new MyHeader();

    // 标签名称
    @XmlElement(name = "body", required = true)
    public MyBody body = new MyBody();
}
```

在报文中的体现如下：

![image-20230525180018730](https://img.myfox.fun/img/20230525180019.png)

### 转成xml

```java
@Test
    public void toXml(){
        try {
            // 拼装报文切换body中的参数
            MyRoot myRoot = new MyRoot();
            MyBody<Param1> myBody = new MyBody<>();
            Param1 param1 = new Param1();
            myBody.setParam(param1);
            myRoot.setBody(myBody);

            // 打印 xml
            String encoding = "UTF-8";
            StringWriter writer = new StringWriter();
            JAXBContext context = JAXBContext.newInstance(MyRoot.class);
            Marshaller marshal = context.createMarshaller();
            marshal.setProperty(Marshaller.JAXB_FORMATTED_OUTPUT, true);
            marshal.setProperty(Marshaller.JAXB_FRAGMENT, false);
            marshal.setProperty(Marshaller.JAXB_ENCODING, encoding);
            marshal.marshal(myRoot, writer);
            String xmlContext = new String(writer.getBuffer());
            System.out.println(xmlContext);
        }catch (Exception e){
            e.printStackTrace();
        }

    }
```

## xmlToBean

关于xml转bean，其中有个坑，就是如果有命名空间且比较负载的时时候，用此方法无法正确解析

建议使用dom4j原生方法进行解析

```java
static String xml = "<soapenv:myRoot >\n" +
            "    <header>\n" +
            "        <ns1:name>测试报文</ns1:name>\n" +
            "        <from>保姆</from>\n" +
            "        <to>厨子</to>\n" +
            "    </header>\n" +
            "    <body>\n" +
            "        <name>信件</name>\n" +
            "        <param xsi:type=\"Param1\" >\n" +
            "            <name>信件名称</name>\n" +
            "        </param>\n" +
            "    </body>\n" +
            "</soapenv:myRoot>";


    @Test
    public void toBean() throws JAXBException, FileNotFoundException, ParserConfigurationException, SAXException {
        Object unmarshall = unmarshall(MyRoot.class, xml);
        System.out.println(unmarshall);
    }
    
    public static Object unmarshall(Class<?> cla , String content) throws JAXBException, ParserConfigurationException, SAXException {

        JAXBContext jaxbContext = JAXBContext.newInstance(cla);
        Unmarshaller unmarshaller = jaxbContext.createUnmarshaller();
        StringReader reader = new StringReader(content);

        SAXParserFactory sax = SAXParserFactory.newInstance();
        sax.setNamespaceAware(false);
        XMLReader xmlReader = sax.newSAXParser().getXMLReader();

        Source source = new SAXSource(xmlReader, new InputSource(reader));
        Object o = unmarshaller.unmarshal(source);

        return o ;
    }
```



