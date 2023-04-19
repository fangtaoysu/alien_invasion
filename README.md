alien_invasion


外星人入侵

# <span style="color: cornflowerblue;">准备工作</span>

>   本游戏来自于《python编程：从入门到实践》的第一个项目：外星人入侵
>
>   其作者是`Eric Matthes`

安装`pygame`包

```css
'''cmd中键入'''
pip3 install pygame
```

## <span style="color: orange;">项目规划</span>

> 玩家控制一艘飞船，飞船初始位置在屏幕底部中央。玩家可以使用箭头键移动飞船，使用空格键射击。
>
> 游戏开始时，随机刷新外星人，外星人走到屏幕底部或撞到玩家飞船，玩家就失去一条生命。
>
> 玩家共三条生命

## <span style="color: orange;">资源</span>

```css
/*下载图片*/
https://pixabay.com/
/*png转bmp*/
https://cdkm.com/cn/png-to-bmp
/*修改图片像素*/
https://www.gaitubao.com/
```

```css
/*后面会用font.Sysfont配置字体，推荐两个字体*/
Snap ITC
Segoe Script
/*方法：在Word中找西文字体，一个一个试*/
```

## <font color='orange'>项目说明</font>

如果能理解本项目的文件之间的配合关系、每个文件的作用，以及用于自主查询项目中涉及的相关方法的能力，那**你将拥有开发2d射击类游戏的能力**，同时可以尝试与本射击游戏强相关的游戏。

若能力不足，需要按项目的文件关系建立文件与文件夹

开发环境：Geany

本项目将提供：

-   源码及必要的注释
-   文件配合与功能的简要说明
-   文件如何打包为`.exe`
-   必要的文字说明

# <font color='cornflowerblue'>常见问题</font>

-   不识别utf-8字符
-   拼写错误
    -   self - slef
    -   下划线 - 句号
-   参数顺序
-   忘记import
-   类方法中未传参数self
-   编码后未保存
-   少右括号

# <font color='cornflowerblue'>打包</font>

在cmd窗口下操作

### <font color='BurlyWood'>安装`pyinstaller`</font>

```css
/*任意位置*/
pip install pyinstaller
/*检验是否安装成功*/
pip list
```

### <font color='BurlyWood'>进入py所在文件</font>

```css
cd path
/*例如*/
cd C:\Users\eng\Documents\项目\alien_invason
```

### <font color='BurlyWood'>整合文件</font>

```css
/* 通过 -p 连接python文件*/
pyinstaller -F -w alien_invasion.py -p alien.py -p bullet.py -p button.py -p game_functions.py -p game_stats.py -p scoreBoard.py -p settings.py -p ship.py
```

### <font color='BurlyWood'>复制资源</font>

将游戏中所需的图片、音乐等文件复制到dist文件夹下，运行dist文件夹下的`.exe`即可

如需分享文件，把dist文件夹打包即可，与其他文件无关
