---
title: Typora常用设置
author: 张一雄
summary: 文本神器！
img: https://pub-b24cf0a8c1f14e9386435977aa464959.r2.dev/img/20230816111139.png
categories:
 - 工具
tags:
 - windows
 - Typora
---

## 更换主题

打开网站

![image-20230614175750873](https://pub-b24cf0a8c1f14e9386435977aa464959.r2.dev/img/20230614175752.png)

选择主题

![image-20230614175925162](https://pub-b24cf0a8c1f14e9386435977aa464959.r2.dev/img/20230614175926.png)

打开后，将css保存到主题文件夹

![image-20230614180102574](https://pub-b24cf0a8c1f14e9386435977aa464959.r2.dev/img/20230614180103.png)

选择相应的主题

![image-20230810155608062](https://pub-b24cf0a8c1f14e9386435977aa464959.r2.dev/img/20230810155609.png)

## Typora+cloudflare图床

- 新增一个bat文件，放到某个文件夹下，该文件夹最好不要有空格

main.exe 为自己开发的文件

```bat
@echo off  
if "%~1"=="" goto :eof  

D:\app\other\upload\main.exe "%~1"  
goto :eof
```

- 将main.exe放到一个文件夹下
- 配置Typora图片

![image-20240820111919217](https://pub-b24cf0a8c1f14e9386435977aa464959.r2.dev/img/image-20240820111919217.png)

## Typora+PicGo-Core+gitee图床搭配使用

### 下载和配置

下载过程可能比较慢，最好有个梯子

![image-20230420142444640](https://pub-b24cf0a8c1f14e9386435977aa464959.r2.dev/img/20230420142445.png)

```json
{
  "picBed": {
    "current": "gitee", // 代表当前的上传图床
    "uploader": "gitee",
    "gitee": {
      "branch": "master", // 分支名，默认是 master
      "customPath": "", // 提交消息，默认为空即可 插件默认提交的是 Upload 图片名 by picGo - 时间
      "customUrl": "", // 没有自己的域名的话，默认为空即可； 如果自定义域名，注意要加http://或者https://
      "path": "img/", // 自定义存储路径，比如 img/ 建议填
      "repo": "xiong-blog-image/images",// 仓库名，格式是 username/reponame <用户名>/<仓库名称> 必填
      "token": "be16d120892396cc7583604dc7373832"// gitee 私人令牌 必填
    }
  },
  "picgoPlugins": {
    "picgo-plugin-gitee-uploader": true,
    "picgo-plugin-super-prefix": true
  }, // PicGo插件预留
  "picgo-plugin-super-prefix": {
    "fileFormat": "YYYYMMDDHHmmss"
  } //super-prefix插件配置
}
```

### 下载插件

```sh
cd C:\Users\jaymie\AppData\Roaming\Typora\picgo\win64
.\picgo.exe install gitee-uploader
.\picgo.exe install super-prefix
```

![image-20230420142909659](https://pub-b24cf0a8c1f14e9386435977aa464959.r2.dev/img/20230420142910.png)

### 测试

点击【验证图片上传选项】
