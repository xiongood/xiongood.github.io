---
title: mybatis-plus的简单使用
img: https://pub-b24cf0a8c1f14e9386435977aa464959.r2.dev/img/20230816111548.png
categories:
 - 后端
tags:
 - mybatis-plus
 - java
---



## 搭建

### pom

```xml
<dependency>
    <groupId>org.mybatis.spring.boot</groupId>
    <artifactId>mybatis-spring-boot-starter</artifactId>
    <version>3.0.0</version>
</dependency>
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

### application.yml

```yml
server:
  port: 8889
spring:
  datasource:
    url: jdbc:mysql://mysql.sqlpub.com:3306/java0417?serverTimezone=UTC&useUnicode=true&characterEncoding=utf-8&AllowPublicKeyRetrieval=True
    username: java0417
    password: f345c26699a412e2


mybatis-plus:
  mapper-locations: mapper/*.xml
  configuration:
    log-impl: org.apache.ibatis.logging.stdout.StdOutImpl
  type-aliases-package: com.example.xiong.entity

```

### 代码生成

![image-20230306180652311](https://pub-b24cf0a8c1f14e9386435977aa464959.r2.dev/img/image-20230306180652311.png)

![image-20230306180726894](https://pub-b24cf0a8c1f14e9386435977aa464959.r2.dev/img/image-20230306180726894.png)

## 常用

### 增

#### 普通新增

```java
@Test
void insert(){
    Book book = new Book();
    book.setName("测试2");
    bookService.save(book);

    Book book2 = new Book();
    book2.setName("测试3");
    bookService.getBaseMapper().insert(book2);
}
```

#### 批量新增

```java
@Test
void saveBatch(){
    List<Book> bookList = new ArrayList<>();
    for (int i = 0; i < 3; i++) {
        Book book = new Book();
        book.setName("测试1");
        bookList.add(book);
    }	
    bookService.saveBatch(bookList);
}
```



### 删



### 基础查询

#### 查询全部

```java
@Test
void list(){
    List<Book> list = bookService.list();
    for (Book book : list){
        System.out.println(book.getName());
    }
}
```

#### 根据id查询

```java
@Test
void selectById() {
    // 第一种方式
    SysUser sysUser = sysUserService.getBaseMapper().selectById(1);
    System.out.println(sysUser);
    
    // 第二种方式
    Book byId = bookService.getById(1);
}
```

#### 查询总数

```java
@Test
    void selectCount() {
        QueryWrapper<SysUser> queryWrapper = new QueryWrapper<>();
        queryWrapper.eq("user_Id",1);
        Integer integer = sysUserService.getBaseMapper().selectCount(queryWrapper);
        System.out.println(integer);
    }
```

#### 通过map拼装查询条件

```java
@Test
void selectByMap(){
    Map<String,Object> map = new HashMap<>();
    map.put("user_id",1);
    List<SysUser> sysUsers = sysUserService.getBaseMapper().selectByMap(map);
    System.out.println(sysUsers);
}
```

#### 分页查询、模糊查询

```java
@Test
void selectMapsPage(){
    Page page = new Page();
    page.setSize(10);
    page.setCurrent(1);
    QueryWrapper<Book> queryWrapper = new QueryWrapper();
    queryWrapper.like("name","同");
    page = bookService.getBaseMapper().selectMapsPage(page, queryWrapper);
    System.out.println(page);
}
```

#### 查询集合、比较符、排序

```java
@Test
void selectList(){
    /*
        eq 就是 equal等于
        ne 就是 not equal不等于
        gt 就是 greater than大于
        lt 就是 less than小于
        ge 就是 greater than or equal 大于等于
        le 就是 less than or equal 小于等于
         */
    QueryWrapper<Book> queryWrapper = new QueryWrapper<>();
    queryWrapper.lt("id",10)
        .orderByDesc("id");
    List<Book> books = bookService.getBaseMapper().selectList(queryWrapper);
    
    // 第二种方式
    List<Book> bookList = bookService.list(queryWrapper);
    
    System.out.println(books);
}
```

#### 返回map结合

```java
@Test
void selectMaps(){
    QueryWrapper<Book> queryWrapper = new QueryWrapper<>();
    queryWrapper.lt("id",10)
        .orderByDesc("id");
    List<Map<String, Object>> maps = bookService.getBaseMapper().selectMaps(queryWrapper);
    System.out.println(maps);
}
```

#### 返回object集合

```java
void selectObjs(){
    List<Object> objects = bookService.getBaseMapper().selectObjs(new QueryWrapper<Book>().lt("id", 10));
    System.out.println(objects);
}
```

#### 根据id集合查询

```java
List<Integer> list = new ArrayList();
list.add(1);
list.add(2);
List<Book> books = bookService.getBaseMapper().selectBatchIds(list);
System.out.println(books);
```

#### 查询一个

```java
@Test
void selectOne(){
    // 查询出多条记录会报错
    Book book = bookService.getBaseMapper().selectOne(new QueryWrapper<Book>().eq("id", 4));
    System.out.println(book);
    
    // 第二种方式
    Book book2 = bookService.getOne(new QueryWrapper<Book>().eq("id", 1));
}
```

#### 分组

```java
@Test
void testIosNotNull(){
    List<Book> books = bookService.getBaseMapper().selectList(new QueryWrapper<Book>()
                                                              .select("name")
                                                              .isNotNull("name").groupBy("name")
                                                              .having("MIN(sales) > {0} AND MAX(sales) < {1}",15,30));
    System.out.println(books);
}
```

### 改

### 其他

