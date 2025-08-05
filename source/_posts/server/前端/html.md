---
title: html常用方法
categories:
 - 前端
tags:
 - jquery
 - html
---

## 常用jquery、js

### 下载js

```txt
http://ajax.aspnetcdn.com/ajax/jQuery/jquery-版本号.js
http://ajax.aspnetcdn.com/ajax/jQuery/jquery-版本号.min.js
http://ajax.aspnetcdn.com/ajax/jQuery/jquery-版本号-vsdoc.js
http://ajax.aspnetcdn.com/ajax/jQuery/jquery-版本号.min.map
```

### 节点寻找

```js
//获取所有兄弟节点
$(“#myDiv”).siblings();
//获取下一个兄弟节点
$(“#myDiv”).next();
//获取前一个兄弟节点
$(“#myDiv”).prev();

// 查询子子节点中所有的input标签
$(obj).find("input");
```

### 设置标签是否可见（一）

```js
// 不可见的元素
<div id="myDiv" style="display: none;color: red"></div>
// 使用style 隐藏一个标签
$("#divId").css("display","none")
// 使用style 显示一个标签
$(".list-bottom").css("display","block")
```

### 设置标签是否可见（二）

```js
// 隐藏一个标签
$(".onLoad").hide();
// 显示一个标签
$(".onLoad").show();
```

### 增加和删除class

```js
// 添加class
$("#divId2").addClass("active")
// 删除class
$("#divId2").removeClass("active")
```

### 给标签添加属性

#### 设置按钮是否可用

```js
// 设置按钮不可用
$('#btn1').attr("disabled","true")
// 设置按钮可用
$('#btn1').removeAttr("disabled")
```

### 计算

#### 保留两位小数

四舍五入

```javascript
let num1 = 10;  
let num2 = 3;  
let result = (num1 / num2).toFixed(2);  
console.log(result);  // 输出: "3.33"
```

### js替换字符串

#### 只替换第一个字符

```javascript
// 更换时间格式
"yyyy-MM-dd-hh-mm-ss".replace("-","/")	//结果"yyyy/MM-dd-hh-mm-ss"
"yyyy-MM-dd-hh-mm-ss".replace(/-/g,"/")	//结果"yyyy/MM/dd/hh/mm/ss"
// 将分号换成换行
var resultText = "字符串;字符串"
resultText.replace(";", ";<br/>")
```

#### 替换所有的字符

- 方式一，ie浏览器有时候不能使用

```javascript
var resultText = "字符串;字符串" 
returnMsg=returnMsg.replaceAll(";", ";<br/>")
```

- 方式二，使用正则

```javascript
var str = "Hello, world! Hello, everyone!";  
var newStr = str.replace(/Hello/g, "Hi");  
console.log(newStr); // 输出: "Hi, world! Hi, everyone!"
```

### 返回上一页

```html
<a href="javascript:window.location.replace(document.referrer);">回退且刷新上一页</a>
<a href="javascript:window.history.back();">回退上一页</a>
```

### 子页面

#### 调用父页面方法

```js
//方法一
// 此方法调用顶级窗口中的方法，调用祖宗的方法
window.parent.parentFun()
//方法二
// 此方法调用父窗口的方法，只调用自己的父窗口。如果父窗口是顶级窗口则调用顶级窗口的方法
window.parent.opener.parentFun()
```

#### 调用子页面方法（一）

```js
$("#iframeId")[0].contentWindow.childFun();
```

#### 打开新的页面

```java
// 语法
window.open(url, [name], [configration])

// 例子
var url = "/servlet/dz.com.sino.ies.purchase.zyconfig.servlet.DzZyPurchaseConfigServlet?act=showOrg2&orgNames="+orgNames+"&orgCodes="+orgCodes;
        var style="width=700px,height=400px,top=190px,left=280px,toolbar=no,menubar=no,scrollbars=no, resizable=no,location=no, status=yes";
        window.open(url, "_blank", style);

// 说明
```

| **窗口name值** | **描述**                      |
| -------------- | ----------------------------- |
| _blank         | 默认的，在新窗口打开链接的url |
| _self          | 在当前窗口打开链接url         |
| _parent        | 在父窗口打开链接url           |
| _top           | 在顶级窗口打开url             |
| framename      | 在指定的框架中打开链接url     |

##### 之后调用父类方法

```javascript
window.parent.opener.parentFun()
```

#### 只能打开一个子页面

- 方式一（只打开一个重新打开时不刷新）

```js
// 只能打开一个子页面
let myWindow = null;  
function openMyWindow() {  
    if (myWindow === null || myWindow.closed) {  
        myWindow = window.open('https://example.com', '_blank');  
    } else {  
        // 如果窗口已经打开，则可以选择将其带到前端或执行其他操作  
        myWindow.focus();  
    }  
}
```

方拾二（不能重复的打开多个页面）

```js
//将_blank用其他的替换掉
//myWindow = window.open(url, "_blank", style);
myWindow = window.open(url, "impwindow", style);
```



### input

#### 设置input不可用

```html
 <input type="text" value="不可用" disabled > 
```

#### 设置只读

```html
 <input type="text" value="只读" readonly="true"  > 
```

### select 下拉框

- js

```javascript
// 获取select对象
var obj = document.getElementById("")
// 获取选中的下标
var index =obj.selectedIndex;
// 获取选中展示的值
var text = obj.options[index].text;
// 将展示的值赋值给value
obj.options[index].value = text;
```

- jquery

```javascript
//选中的文本
$('#testSelect option:selected').text();
//选中的值
$('#testSelect option:selected').val();
//索引
$("#testSelect ").get(0).selectedIndex;
```

### checkbox 复选框

#### 获取选中(未选中)的复选框

```javascript
// 获取所有选中的复选框
var checkboxes = document.querySelectorAll('input[type="checkbox"]:checked');
for (var i = 0; i < checkboxes.length; i++) {
    var id = checkboxes[i].id
}
// 获取所有未选中的复选框
var uncheckedCheckboxes = document.querySelectorAll('input[type="checkbox"]:not(:checked)');
```

#### 判断是否选中状态

- js

```javascript
var checkbox = document.getElementById('myCheckbox');
if (checkbox.checked) {
  // checkbox被选中
  console.log('选中状态');
} else {
  // checkbox未被选中
  console.log('未选中状态');
}
```

- jquery

```javascript
var checkbox = $('#myCheckbox');
if (checkbox.is(':checked')) {
  console.log('选中状态');
} else {
  console.log('未选中状态');
}
```

#### 设置和取消选中状态

- js

```javascript
var checkbox = document.getElementById('myCheckbox');
checkbox.checked = true; // 设置为选中状态
checkbox.checked = false; // 取消选中状态
```

- jquery

```javascript
$('#myCheckbox').prop('checked', true); // 使用jQuery设置为选中状态
$('#myCheckbox').prop('checked', false); // 使用jQuery取消选中状态
```

#### 防止触发checkbox的`change`事件

- js

```javascript
var checkbox = document.getElementById('myCheckbox');
checkbox.addEventListener('change', function(event) {
  event.preventDefault();
  event.stopPropagation();
});
// 设置checkbox为选中状态，但不触发change事件
checkbox.checked = true;
```

- jquery

```javascript
// 暂时解绑change事件处理函数
$('#myCheckbox').off('change');

// 设置checkbox为选中状态，不触发change事件
$('#myCheckbox').prop('checked', true);

// 重新绑定change事件处理函数
$('#myCheckbox').on('change', function() {
  // 处理change事件
});
```

### 关于对象

#### 复制对象

```js
var newObj = JSON.parse(JSON.stringify(oldObj));
```

#### 对象转json字符串

```javascript
let jsonStr = JSON.stringify(obj);
```

#### 字符串转对象

```js
var data = JSON.stringify(dataListStr)
```

### 定时任务

#### 定时任务一

```js
window.setTimeout(function (){
    //在这里编写需要定时执行的代码
},3000)
```

#### 定时任务二

```js
$(document).ready(function() {
setInterval(function() {
    //在这里编写需要定时执行的代码
}, 5000);
});
```

#### 暂停线程

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document</title>
</head>
<body>

    <button onclick="abc()">点我</button>
    
</body>

<script>

//async 
    async function abc (){

        const delay = ms => new Promise(resolve => setTimeout(resolve, ms));
        var i = 0;
        while(true) {
            console.log(i);
            i++;
            if(i>3){
                break
            }
           await delay(1000);
        }
        console.log("end");
    }


</script>
</html>
```

### 循环

```js
// 方式一
for (var i in list) {
	var obj = list[j];
}

// 方式二
for (var i = 0; i < list.length; i++) {
    var obj = list[j];
}
```

### ajax

#### 发送json

- 前端

```javascript
// 创建结合
var dataList = [];
// 创建对象
for (var i=0;i<itemCodes.length;i++){
    var data = {}
    var itemCode = itemCodes[i].value; // 物料编码
    data.itemCode = itemCode;
    // 将对象放入数组
    dataList.push(data);
}
// 返回值
var returnMsg =""
// 请求
$.ajax({
    async:false, // 同步请求
    type:'post',
    url:'/servlet/dz.com.sino.ies.purchase.zyconfig.servlet.DzZyPurchaseConfigServlet?act=check',
    contentType: 'application/json; charset=UTF-8', // 设置编码集
    data:JSON.stringify(dataList),  // json
    success:function(msg){
        returnMsg = msg;
    },
    error:function(){
        returnMsg= "发送请求出现异常！！;"
    }
});
```

- 后端

```java
String msg = "";
// 设置编码集
req.setCharacterEncoding("UTF-8"); 
// 接收数据
StringBuilder sb = new StringBuilder();
BufferedReader reader = req.getReader();
char[] charBuffer = new char[128];
int bytesRead;
while ((bytesRead = reader.read(charBuffer)) != -1) {
    sb.append(charBuffer, 0, bytesRead);
}
String jsonData = sb.toString();
// 将接收到的json转成对象
List<DzZyPurchaseConfigLineDTO> dtoList = JacksonHelper.fromJSONList(jsonData, DzZyPurchaseConfigLineDTO.class);
// 处理逻辑 略

// 返回数据
res.setContentType("text/html;charset=GBK");
PrintWriter writer = res.getWriter();
writer.write(msg);
writer.flush();
writer.close();
```

#### 发送text

- 前端

```javascript
$.ajax({
    url:"/servlet/dz.com.sino.ies.purchase.zyconfig.servlet.DzZyPurchaseConfigServlet?act=doDisable",
    type: "POST",
    dataType:"text",
    data:{"configIds": "checkValue"},
    success:function(data){
        if(data == ""){
            alert("失效数据成功!");
        }else{
            alert("失效数据失败!");
        }
    }
});
```

- 后端

```java
String configIds = req.getParameter("configIds");
res.setContentType("text/html;charset=GBK");
String retStr = dao.doDisable(configIds);
PrintWriter writer = res.getWriter();
writer.write(retStr);
writer.flush();
writer.close();
```

## 常用css

### 元素位置

```html
<!--relative 相对位置-->
<div style="position: relative; top: 100px">
<!--absolute 绝对位置-->
<div style="position: absolute; top: 100px">
```

### 文字居中

```html
<!--文字居中样式-->
<div style="text-align:center;">
```

### 文字不换行

```css
.tmp {
    white-space: nowrap; /*强制单行显示*/
    text-overflow: ellipsis; /*超出部分省略号表示*/
    overflow: hidden; /*超出部分隐藏*/
    width: 240px; /*设置显示的最大宽度*/
}
```

### 文字换行

```css
.text-huanhang {
    width:200px; /*最大宽度*/
    word-wrap: break-word; /* 允许单词内断行 */
    white-space: normal;   /* 处理空白符，自动换行 */
}
```

## 不常用

### 自适应手机屏幕 小屏幕 

```html
<!DOCTYPE html>
<html>
<head>
    // 自适应
    <meta name="viewport" content="width=device-width,initial-scale=1.0, minimum-scale=1.0, maximum-scale=1.0, user-scalable=no"/>
    <title>每日提醒</title>
</head>
<body>
    <iframe src="http://localhost/weatherpage" width="100%" height="600" frameborder="0"></iframe>
</body>
</html>
```

### 引入其他网页

```html
<!DOCTYPE html>
<html>
<head>
    <meta name="viewport" content="width=device-width,initial-scale=1.0, minimum-scale=1.0, maximum-scale=1.0, user-scalable=no"/>
    <title>每日提醒</title>
</head>
<body>
    <iframe src="http://localhost/weatherpage" width="100%" height="600" frameborder="0"></iframe>
</body>
</html>
```

### 可以输入的下拉框

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document</title>
</head>
<body>
    <input id="type" type="text" list="typeList" placeholder="请选择">
    <datalist id="typeList">
        　　<option>Dimond</option>
        　　<option>vertical</option>
    </datalist>
</body>
<script>
</script>
</html>
```

### 获取滚动条高度

```js
console.log("滚动条的垂直位置")
var scrollTop=$(".content").scrollTop();
console.log(scrollTop);

console.log('div的高度');
var height = $(".content").height();
console.log(height);

console.log('容器的总高度');
var scrollHeight=$(".content")[0].scrollHeight;
console.log(scrollHeight);

//如果滚动垂直位置+div的高度大于或者等于容器总高度，就是到底了
if(scrollTop+height>=scrollHeight){
    console.log("到底了");
}

```

### html 转义字符

空格： &nbsp;

### url中特殊的字符

例子

```http
http://localhost:8080/insert?filepath=C%3A%5CTEST%5CTaskRecord%5Ctest.txt
```

列表

```txt
空格 用%20代替

" 用%22代替

# 用%23代替

% 用%25代替

&用%26代替

( 用%28代替

) 用%29代替

+ 用%2B代替

, 用%2C代替

/ 用%2F代替

: 用%3A代替

; 用%3B代替

< 用%3C代替

= 用%3D代替

> 用%3E代替

? 用%3F代替

@ 用%40代替

\ 用%5C代替

| 用%7C代替
```

