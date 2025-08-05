## 安装与卸载
```sh
npm install hexo-cli -g

npm uninstall hexo-cli -g

# 查看版本，确认是否安装成功

hexo -version
```

## 修改环境

![image-20250213123757314](http://img.myfox.fun/img/image-20250213123757314.png)

```json
const map = {
  '&#39;': '\'',
  '&amp;': '&',
  '&gt;': '>',
  '&lt;': '<',
  '&quot;': '"',
  '&#123;': '{',
  '&#125;': '}'
};

```

## 常用命令

```shell
# 运行
hexo s
```
```shell
# 清空
hexo clean
# 编译
hexo g
# 提交到git
hexo d
```



## 修改github服务器

### 修改此文件

_config.yml

### 修改下面的地址即可

deploy:
  type: git
  repo: https://github.com/xiongood/xiongood.github.io.git   #替换成你自己仓库的HTTP URL地址
  branch: main
