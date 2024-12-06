---
title: idea常用配置
summary: java程序员离不开的工具，期待国产的开发工具能早日发扬光大
img: https://img.myfox.fun/img/idea.jpg
categories:
 - 工具
tags:
 - windows
 - idea
---

## 常用配置

### 设置中文   版本：2024+

![image-20240820164249659](https://img.myfox.fun/img/image-20240820164249659.png)

### 显示空格

![image-20231124104635860](https://img.myfox.fun/img/20231124104637.png)

### 修改主题

![image-20230418225305217](https://img.myfox.fun/img/image-20230418225305217.png)

### 设置控制台展示行数

![image-20230424140701242](https://img.myfox.fun/img/20230424140702.png)

### 查询的时候排除某些文件

![image-20241203173001017](https://pub-b24cf0a8c1f14e9386435977aa464959.r2.dev/img/image-20241203173001017.png)

### 修改配色方案

我用的这两个

BFC519	353939

![image-20230727155309595](https://img.myfox.fun/img/20230727155310.png)

### 修改滚动条颜色

#### 方式一

![image-20230426214421842](https://img.myfox.fun/img/20230426214423.png)

#### 方式二

- 效果展示

![image-20230418225407360](https://img.myfox.fun/img/image-20230418225407360.png)

- 导出配置

![image-20230418225432179](https://img.myfox.fun/img/image-20230418225432179.png)

- 导出的原配置文件

![image-20230418225454717](https://img.myfox.fun/img/image-20230418225454717.png)

- 修改为

![image-20230418225508378](https://img.myfox.fun/img/image-20230418225508378.png)

- 将以下配置 放到scheme标签里面即可

```xml
<colors>
  <option name="ScrollBar.background" value="000000"/>
  <option name="ScrollBar.trackColor" value="000000"/>
  <option name="ScrollBar.thumbColor" value="FFFFFFBE"/>
  <option name="ScrollBar.thumbBorderColor" value="000000"/>
  <option name="ScrollBar.hoverTrackColor" value="000000"/>
  <option name="ScrollBar.hoverThumbColor" value="FFFFFFBE"/>
  <option name="ScrollBar.hoverThumbBorderColor" value="000000"/>
  <option name="ScrollBar.Transparent.trackColor" value="E6E6E600"/>
  <option name="ScrollBar.Transparent.thumbColor" value="FFFFFFBE"/>
  <option name="ScrollBar.Transparent.thumbBorderColor" value="000000"/>
  <option name="ScrollBar.Transparent.hoverTrackColor" value="E6E6E65A"/>
  <option name="ScrollBar.Transparent.hoverThumbColor" value="FFFFFFBE"/>
  <option name="ScrollBar.Transparent.hoverThumbBorderColor" value="000000"/>
  <option name="ScrollBar.Mac.trackColor" value="000000"/>
  <option name="ScrollBar.Mac.thumbColor" value="FFFFFFBE"/>
  <option name="ScrollBar.Mac.thumbBorderColor" value="000000"/>
  <option name="ScrollBar.Mac.hoverTrackColor" value="000000"/>
  <option name="ScrollBar.Mac.hoverThumbColor" value="FFFFFFBE"/>
  <option name="ScrollBar.Mac.hoverThumbBorderColor" value="000000"/>
  <option name="ScrollBar.Mac.Transparent.trackColor" value="E6E6E65A"/>
  <option name="ScrollBar.Mac.Transparent.thumbColor" value="FFFFFFBE"/>
  <option name="ScrollBar.Mac.Transparent.thumbBorderColor" value="000000"/>
  <option name="ScrollBar.Mac.Transparent.hoverTrackColor" value="E6E6E65A"/>
  <option name="ScrollBar.Mac.Transparent.hoverThumbColor" value="FFFFFFBE"/>
  <option name="ScrollBar.Mac.Transparent.hoverThumbBorderColor" value="000000"/>
</colors>
```

- 完整版配置

```xml
<scheme name="Dark" version="142" parent_scheme="Darcula">
	<metaInfo>
		<property name="created">2023-03-02T15:29:51</property>
		<property name="ide">idea</property>
		<property name="ideVersion">2022.3.2.0.0</property>
		<property name="modified">2023-03-02T15:29:54</property>
		<property name="originalScheme">_@user_Dark</property>
	</metaInfo>
	<colors>
		<option name="ADDED_LINES_COLOR" value="549159"/>
		<option name="ANNOTATIONS_COLOR" value="8d9199"/>
		<option name="ANNOTATIONS_LAST_COMMIT_COLOR" value="ced0d6"/>
		<option name="CARET_ROW_COLOR" value="2b2d30"/>
		<option name="CONSOLE_BACKGROUND_KEY" value="1e1f22"/>
		<option name="DELETED_LINES_COLOR" value="868a91"/>
		<option name="DIFF_SEPARATORS_BACKGROUND" value="2b2d30"/>
		<option name="DOCUMENTATION_COLOR" value="2b2d30"/>
		<option name="ERROR_HINT" value="402929"/>
		<option name="IGNORED_ADDED_LINES_BORDER_COLOR" value="549159"/>
		<option name="IGNORED_DELETED_LINES_BORDER_COLOR" value="868a91"/>
		<option name="IGNORED_MODIFIED_LINES_BORDER_COLOR" value="375fad"/>
		<option name="INDENT_GUIDE" value="313438"/>
		<option name="INFORMATION_HINT" value="2b2d30"/>
		<option name="LINE_NUMBERS_COLOR" value="4e5157"/>
		<option name="LINE_NUMBER_ON_CARET_ROW_COLOR" value="9da0a8"/>
		<option name="LOOKUP_COLOR" value="2b2d30"/>
		<option name="METHOD_SEPARATORS_COLOR" value="43454a"/>
		<option name="MODIFIED_LINES_COLOR" value="375fad"/>
		<option name="NOTIFICATION_BACKGROUND" value="25324d"/>
		<option name="PROMOTION_PANE" value="25324d"/>
		<option name="QUESTION_HINT" value="25324d"/>
		<option name="RECENT_LOCATIONS_SELECTION" value="2b2d30"/>
		<option name="RIGHT_MARGIN_COLOR" value="393b40"/>
		<option name="SELECTED_INDENT_GUIDE" value="6f737a"/>
		<option name="VCS_ANNOTATIONS_COLOR_1" value="2f5194"/>
		<option name="VCS_ANNOTATIONS_COLOR_2" value="2d416b"/>
		<option name="VCS_ANNOTATIONS_COLOR_3" value="283754"/>
		<option name="VCS_ANNOTATIONS_COLOR_4" value="242d42"/>
		<option name="VCS_ANNOTATIONS_COLOR_5" value="22252e"/>
		<option name="VISUAL_INDENT_GUIDE" value="2b2d30"/>
		<option name="WHITESPACES_MODIFIED_LINES_COLOR" value="52433d"/>
		<option name="ScrollBar.background" value="000000"/>
		<option name="ScrollBar.trackColor" value="000000"/>
		<option name="ScrollBar.thumbColor" value="FFFFFFBE"/>
		<option name="ScrollBar.thumbBorderColor" value="000000"/>
		<option name="ScrollBar.hoverTrackColor" value="000000"/>
		<option name="ScrollBar.hoverThumbColor" value="FFFFFFBE"/>
		<option name="ScrollBar.hoverThumbBorderColor" value="000000"/>
		<option name="ScrollBar.Transparent.trackColor" value="E6E6E600"/>
		<option name="ScrollBar.Transparent.thumbColor" value="FFFFFFBE"/>
		<option name="ScrollBar.Transparent.thumbBorderColor" value="000000"/>
		<option name="ScrollBar.Transparent.hoverTrackColor" value="E6E6E65A"/>
		<option name="ScrollBar.Transparent.hoverThumbColor" value="FFFFFFBE"/>
		<option name="ScrollBar.Transparent.hoverThumbBorderColor" value="000000"/>
		<option name="ScrollBar.Mac.trackColor" value="000000"/>
		<option name="ScrollBar.Mac.thumbColor" value="FFFFFFBE"/>
		<option name="ScrollBar.Mac.thumbBorderColor" value="000000"/>
		<option name="ScrollBar.Mac.hoverTrackColor" value="000000"/>
		<option name="ScrollBar.Mac.hoverThumbColor" value="FFFFFFBE"/>
		<option name="ScrollBar.Mac.hoverThumbBorderColor" value="000000"/>
		<option name="ScrollBar.Mac.Transparent.trackColor" value="E6E6E65A"/>
		<option name="ScrollBar.Mac.Transparent.thumbColor" value="FFFFFFBE"/>
		<option name="ScrollBar.Mac.Transparent.thumbBorderColor" value="000000"/>
		<option name="ScrollBar.Mac.Transparent.hoverTrackColor" value="E6E6E65A"/>
		<option name="ScrollBar.Mac.Transparent.hoverThumbColor" value="FFFFFFBE"/>
		<option name="ScrollBar.Mac.Transparent.hoverThumbBorderColor" value="000000"/>
	</colors>
	<attributes>
		<option name="BREADCRUMBS_CURRENT">
			<value>
				<option name="FOREGROUND" value="dfe1e5"/>
				<option name="BACKGROUND" value="2b2d30"/>
			</value>
		</option>
		<option name="BREADCRUMBS_DEFAULT">
			<value>
				<option name="FOREGROUND" value="9da0a8"/>
			</value>
		</option>
		<option name="BREADCRUMBS_HOVERED">
			<value>
				<option name="FOREGROUND" value="dfe1e5"/>
				<option name="BACKGROUND" value="2b2d30"/>
			</value>
		</option>
		<option name="BREADCRUMBS_INACTIVE">
			<value>
				<option name="FOREGROUND" value="6f737a"/>
			</value>
		</option>
		<option name="CODE_LENS_BORDER_COLOR">
			<value>
				<option name="EFFECT_COLOR" value="868a91"/>
			</value>
		</option>
		<option name="FOLLOWED_HYPERLINK_ATTRIBUTES">
			<value>
				<option name="FOREGROUND" value="a571e6"/>
				<option name="EFFECT_COLOR" value="a571e6"/>
				<option name="EFFECT_TYPE" value="1"/>
			</value>
		</option>
		<option name="MATCHED_BRACE_ATTRIBUTES">
			<value>
				<option name="FOREGROUND" value="ced9d2"/>
				<option name="BACKGROUND" value="326146"/>
				<option name="FONT_TYPE" value="1"/>
			</value>
		</option>
		<option name="TEXT">
			<value>
				<option name="FOREGROUND" value="a9b7c6"/>
				<option name="BACKGROUND" value="1e1f22"/>
			</value>
		</option>
		<option name="WARNING_ATTRIBUTES">
			<value>
				<option name="BACKGROUND" value="3d3322"/>
				<option name="ERROR_STRIPE_COLOR" value="be9117"/>
				<option name="EFFECT_TYPE" value="2"/>
			</value>
		</option>
	</attributes>
</scheme>
```

- 导入配置文件

![image-20230418225619238](https://img.myfox.fun/img/image-20230418225619238.png)

### 字体

#### 修改字体大小

![image-20230418230147995](https://img.myfox.fun/img/image-20230418230147995.png)

#### 修改菜单区字体大小

![image-20230418230301334](https://img.myfox.fun/img/image-20230418230301334.png)

#### 滚轮修改字体大小

修改快捷键、修改鼠标滑轮

![image-20231023213647766](https://img.myfox.fun/img/20231023213649.png)

#### 修改字符集

![image-20230418225636040](https://img.myfox.fun/img/image-20230418225636040.png)

### sql关键字大写

#### 中文

![image-20230925111509575](https://img.myfox.fun/img/20230925111510.png)

#### 英文

![image-20230418225650349](https://img.myfox.fun/img/image-20230418225650349.png)



### 展示所有打开的(页签)类

#### 中文

![image-20240820165053730](https://img.myfox.fun/img/image-20240820165053730.png)

#### 英文

![image-20230418225719612](https://img.myfox.fun/img/image-20230418225719612.png)

### 设置最大打开文件(页签)数

- 英文

![image-20230418225737784](https://img.myfox.fun/img/image-20230418225737784.png)

- 中文

![image-20240402150056381](https://img.myfox.fun/img/20240402150058.png)

### 显示多行(页签)选项卡

![image-20230418225819468](https://img.myfox.fun/img/image-20230418225819468.png)

### 关闭代码作者提示

关闭前

![image-20240426115415348](https://img.myfox.fun/img/20240426115417.png)

关闭设置

![image-20240426115500084](https://img.myfox.fun/img/20240426115503.png)

### 显示折叠忽略的代码

未修改时

![image-20231010111200715](https://img.myfox.fun/img/20231010111202.png)

修改：

![image-20231010111346306](https://img.myfox.fun/img/20231010111347.png)

### 修改快捷键

![image-20230418225845822](https://img.myfox.fun/img/image-20230418225845822.png)

### 修改创建类时生成的注释

![image-20230508224553402](https://img.myfox.fun/img/20230508224554.png)

### 自定义快捷键

![image-20241022162635954](https://img.myfox.fun/img/image-20241022162635954.png)

### 自定义配置注释

- 第一步

![image-20230418225856427](https://img.myfox.fun/img/image-20230418225856427.png)

```txt
**
 * 简述:
 * 详细描述:
 * @author 张一雄
 $param$
 $return$
 * @exception/throws
 * 新增日期：$date$ $time$
 */
```

- 第二步

![image-20230418225941907](https://img.myfox.fun/img/image-20230418225941907.png)

```txt
groovyScript("if(\"${_1}\".length() == 2) {return '';} else {def result=''; def params=\"${_1}\".replaceAll('[\\\\[|\\\\]|\\\\s]', '').split(',').toList();for(i = 0; i < params.size(); i++) {if(i==0){result+='* @param ' + params[i] + '  '}else{result+='\\n' +'\\t'+ ' * @param ' + params[i] + '  '}}; return result;}", methodParameters()); 
```

```txt
groovyScript("def returnType = \"${_1}\"; def result = '* @return { ' + returnType + ' }'; return result;", methodReturnType()); 
```

```txt
date()
time()
```

- 使用

输入 /m +回车

### 不区分大小写提示

![image-20230418230040022](https://img.myfox.fun/img/image-20230418230040022.png)

### 取消代码检查

![image-20230418230051091](https://img.myfox.fun/img/image-20230418230051091.png)

### 打开软件时进入选择项目页面

- 中文

![image-20240820165626356](https://img.myfox.fun/img/image-20240820165626356.png)

- 英文

![image-20230418230109316](https://img.myfox.fun/img/image-20230418230109316.png)

### 显示数据库注释

![image-20230418230321964](https://img.myfox.fun/img/image-20230418230321964.png)

### 翻译

#### 微软

![image-20230418230339726](https://img.myfox.fun/img/image-20230418230339726.png)

#### 有道

![image-20230418230350890](https://img.myfox.fun/img/image-20230418230350890.png)

```txt
有道翻译开发者ID：
6d7759105b83707f
秘钥：
R2OWuOKu0JLNCg9w7xDxPtsBjwXj79Pc
```

### 复制进XML后格式变了

![image-20241023154836537](https://img.myfox.fun/img/image-20241023154836537.png)

## mybatisX

![image-20240821174120186](https://img.myfox.fun/img/image-20240821174120186.png)

## 关于jdk

### 修改项目jdk

- 项目模块

![image-20240402105147053](https://img.myfox.fun/img/20240402105150.png)

![image-20240402105212734](https://img.myfox.fun/img/20240402105215.png)

![image-20240402105239916](https://img.myfox.fun/img/20240402105243.png)

- 编译

![image-20240402105340387](https://img.myfox.fun/img/20240402105344.png)

- maven

![image-20240402105453308](https://img.myfox.fun/img/20240402105500.png)

![image-20240402105549647](https://img.myfox.fun/img/20240402105555.png)

## 关于终端

### 设置终端光标类型

![image-20230613144208819](https://img.myfox.fun/img/20230613144210.png)

## 关于tomcat

### 修改内存

```txt
-Xms512m -Xmx512m -XX:MaxNewSize=512m -XX:MaxPermSize=512m  
```

![image-20230927165150538](https://img.myfox.fun/img/20230927165151.png)

![image-20230927165213272](https://img.myfox.fun/img/20230927165214.png)



## 关于maven

### 设置maven默认配置

![image-20230420151932801](https://img.myfox.fun/img/20230420151934.png)

![image-20230420152059050](https://img.myfox.fun/img/20230420152100.png)

### 卡在解析maven依赖项

![image-20230421113516967](https://img.myfox.fun/img/20230421113518.png)

解决：

```txt
-Xms1024m -Xmx2048m
```

![image-20230421113611432](https://img.myfox.fun/img/20230421113612.png)

## 关于git

### 提交时显示目录结构

![image-20230418230432603](https://img.myfox.fun/img/image-20230418230432603.png)

### 去掉提交时的代码检查

- 方式一

  ![image-20240417164524080](https://img.myfox.fun/img/20240417164526.png)

- 方式二

![image-20230516230938085](https://img.myfox.fun/img/20230516230939.png)

### 合并分支

![image-20240425115227379](https://img.myfox.fun/img/20240425115230.png)

### 将dev中某个版本合并到master上

#### 将此版本合并到master

![image-20240425173751313](https://img.myfox.fun/img/20240425173753.png)

1、切换到master分支

2、将dev中所有的代码合并到master中

![image-20240425173900507](https://img.myfox.fun/img/20240425173902.png)



3、回滚master中的代码，带指定提交的版本

![image-20240425173952217](https://img.myfox.fun/img/20240425173954.png)

![image-20240425174008330](https://img.myfox.fun/img/20240425174030.png)

5、提交代码

![image-20240425174109596](https://img.myfox.fun/img/20240425174111.png)

### 将本地代码回滚到pull之前

不影响远程的代码，还可以在将新代码pull下来

![image-20240425174616175](https://img.myfox.fun/img/20240425174618.png)

### 紧回滚某一次提交

选中版本，选择还原提交，此中方法，不影响其他的提交，但是如果和其他的提交有冲突，则会收到影响

![image-20240425175344352](https://img.myfox.fun/img/20240425175346.png)

## 关于SVN

### 解决频繁弹出登录框

#### 方式一

![image-20230418230504001](https://img.myfox.fun/img/image-20230418230504001.png)

![image-20230418230509769](https://img.myfox.fun/img/image-20230418230509769.png)

#### 方式二

![image-20230418230531704](https://img.myfox.fun/img/image-20230418230531704.png)

### 不对某些文件版本控制

![image-20230418230550047](https://img.myfox.fun/img/image-20230418230550047.png)

![image-20230418230554401](https://img.myfox.fun/img/image-20230418230554401.png)

## 关于数据库

### 链接数据库

- 正常填写链接不上

![image-20240402113612555](https://img.myfox.fun/img/20240402113614.png)

- 手动填写下面的地址，可以解决

加两个斜杠

jdbc:oracle:thin:@//10.92.82.81:11521/B2BUAT

![image-20240402113652344](https://img.myfox.fun/img/20240402113654.png)

### 下载数据库驱动太慢

![image-20230418230618768](https://img.myfox.fun/img/image-20230418230618768.png)

#### 方式一

修改配置文件

C:\Users\java0\AppData\Roaming\JetBrains\IntelliJIdea2022.3\jdbc-drivers\jdbc-drivers.xml

```xml

<!--
<artifact name="Apache Phoenix Client">
    <version version="4.15">
      <item url="https://repository.apache.org/content/repositories/releases/org/apache/phoenix/phoenix-client/4.15.0-HBase-1.5/phoenix-client-4.15.0-HBase-1.5.jar"/>
    </version>
  </artifact>
-->

  <artifact name="Apache Phoenix Client">
    <version version="4.15">
      <item url="https://maven.aliyun.com/repository/public/org/apache/phoenix/phoenix-client/4.15.0-HBase-1.5/phoenix-client-4.15.0-HBase-1.5.jar"/>
    </version>
  </artifact>
```

#### 方式二

![image-20230418230715744](https://img.myfox.fun/img/image-20230418230715744.png)

![image-20230418230723312](https://img.myfox.fun/img/image-20230418230723312.png)

## 问题

### 卡在打卡项目页面

![image-20230918093755702](https://img.myfox.fun/img/20230918093757.png)

#### 解决：

删除.idea文件后重启

## 下载

### 官网

```http
https://www.jetbrains.com.cn/
```

### 选择语言

划到最下方

![image-20230510222906286](https://img.myfox.fun/img/20230510222907.png)

### 选择版本

没有梯子有时候打不开

![image-20240906105832371](https://img.myfox.fun/img/image-20240906105832371.png)

![image-20230510223038569](https://img.myfox.fun/img/20230510223039.png)
