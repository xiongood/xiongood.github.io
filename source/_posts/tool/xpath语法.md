---
title: xpath的使用
img: https://img.myfox.fun/img/xpath.jpg
categories:
 - 工具
tags:
 - xpath
---

## 常用语法

### 根据css获取元素

```js
"//button[@class='page_search_btn ivu-btn ivu-btn-info']"
```

### 根据span中的文字获取元素

```js
"//span[normalize-space(text())='文字内容']"
```

### 获取的元素有多个

```js
"//div[@class='ivu-tabs-tab'][3]"
```

### 获取子元素(子元素为集合)

```js
"//div[@class='ivu-date-picker-cells']/span[1]"
```

### and 和or

选取 `div` 元素中同时满足 `class` 为 `example` 和 `id` 为 `123` 的节点：//div[@class='example' and @id='123'

选取所有 `div` 元素中 `class` 属性值为 `example` 或 `id` 属性值为 `123` 的节点：//div[@class='example' or @id='123']

### 属性是否包含

a标签中class属性值包含nav-link的元素

```js
//a[contains(@class, 'nav-link')]
```

a标签中class属性值以nav开头的元素

```js
//a[starts−with(@class, 'nav')]
```

