---
title: R语言环境搭建
author: 张一雄
summary: R语言环境搭建
img: http://img.myfox.fun/img/R.png
categories:
 - 周边
tags:
 - R
---

## 下载安装R

### 寻找国内镜像源

```http
https://www.r-project.org/
```

![image-20250613090755048](http://img.myfox.fun/img/image-20250613090755048.png)

![image-20250613090822803](http://img.myfox.fun/img/image-20250613090822803.png)

### 下载

![image-20250613090926867](http://img.myfox.fun/img/image-20250613090926867.png)

![image-20250613091010328](http://img.myfox.fun/img/image-20250613091010328.png)

![image-20250613091041958](http://img.myfox.fun/img/image-20250613091041958.png)

### 安装

略

### 配置环境变量

```txt
C:\Program Files\R\R-4.5.0\bin
```

![image-20250613091507804](http://img.myfox.fun/img/image-20250613091507804.png)

### 验证

cmd 输入 r

![image-20250613091750654](http://img.myfox.fun/img/image-20250613091750654.png)

## 安装R-studio

### 下载

```http
https://posit.co/downloads/
```

![image-20250613092240784](http://img.myfox.fun/img/image-20250613092240784.png)

![image-20250613092317719](http://img.myfox.fun/img/image-20250613092317719.png)

![image-20250613092419613](http://img.myfox.fun/img/image-20250613092419613.png)

### 安装

略

![image-20250613093749864](http://img.myfox.fun/img/image-20250613093749864.png)

### 设置

修改镜像源

![image-20250613094004272](http://img.myfox.fun/img/image-20250613094004272.png)

![image-20250613094142467](http://img.myfox.fun/img/image-20250613094142467.png)

修改字符集

![image-20250613094229662](http://img.myfox.fun/img/image-20250613094229662.png)

修改工作区

![image-20250613094725462](http://img.myfox.fun/img/image-20250613094725462.png)

## 使用例子

画一个圈圈

### 代码

```R
# 绘制圆形函数
draw_circle <- function(radius = 1, center = c(0, 0), color = "black", fill = FALSE, 
                        lwd = 2, lty = 1, main = NULL, xlab = "X轴", ylab = "Y轴", 
                        grid = TRUE) {
  # 如果没有提供标题，则创建一个默认标题
  if(is.null(main)) {
    main <- paste("圆形 (半径:", radius, ", 圆心:", center[1], ",", center[2], ")")
  }
  
  # 设置绘图区域
  plot(NA, NA, 
       xlim = c(center[1] - radius - 0.5, center[1] + radius + 0.5),
       ylim = c(center[2] - radius - 0.5, center[2] + radius + 0.5),
       xlab = xlab, ylab = ylab, main = main,
       asp = 1,  # 保持坐标轴比例相等，确保圆不会变形
       type = "n")
  
  # 如果需要填充，则先绘制填充圆
  if(fill) {
    polygon(
      center[1] + radius * cos(seq(0, 2*pi, length.out = 100)),
      center[2] + radius * sin(seq(0, 2*pi, length.out = 100)),
      col = adjustcolor(color, alpha.f = 0.3),
      border = NA
    )
  }
  
  # 绘制圆的轮廓
  lines(
    center[1] + radius * cos(seq(0, 2*pi, length.out = 100)),
    center[2] + radius * sin(seq(0, 2*pi, length.out = 100)),
    col = color,
    lwd = lwd,
    lty = lty
  )
  
  # 添加网格线
  if(grid) {
    grid(col = "gray", lty = "dotted")
  }
  
  # 添加坐标轴
  abline(h = 0, v = 0, col = "gray", lty = "dotted")
  
  # 返回圆心和半径信息
  invisible(list(center = center, radius = radius))
}

# 使用示例
# 绘制默认圆形
draw_circle()

# 绘制自定义圆形
# draw_circle(
#   radius = 2, 
#   center = c(1, 1), 
#   color = "red", 
#   fill = TRUE,
#   lwd = 3,
#   main = "自定义圆形"
# )

```

### 运行

略

















































