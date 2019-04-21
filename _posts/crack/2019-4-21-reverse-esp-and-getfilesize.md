---
layout: post
comments: true
title: esp定律脱壳+绕过文件大小自校验
categories: crack
---

## esp定律脱壳+绕过文件大小自校验
> 目标程序有壳，且存在文件大小自校验，如果改变文件大小，则不能运行。防止别人修改脱壳。

### 1.esp定律脱壳
首先看一下文件

![](/image/crack/reverse-esp-and-getfilesize/1.png)

peid查壳：

![](/image/crack/reverse-esp-and-getfilesize/2.png)

拖入od观察到寄存器情况

![](/image/crack/reverse-esp-and-getfilesize/3.png)

F8单步运行后变化

![](/image/crack/reverse-esp-and-getfilesize/4.png)

证明可以用esp定律脱壳

在寄存器esp的值上右键，在数据窗口中跟随

![](/image/crack/reverse-esp-and-getfilesize/5.png)

选中数据窗口中的值，右键设置硬件访问断点

![](/image/crack/reverse-esp-and-getfilesize/6.png)

F9运行，然后F8，直到反汇编区出现变化

![](/image/crack/reverse-esp-and-getfilesize/7.png)

右键->分析->从模块中删除分析

![](/image/crack/reverse-esp-and-getfilesize/8.png)

右键用ODdump脱壳

![](/image/crack/reverse-esp-and-getfilesize/9.png)

保存文件。此时壳已经脱掉

![](/image/crack/reverse-esp-and-getfilesize/10.png)

但是双击后没有反应，因为有文件自校验，实际上是文件打开后又关闭掉

### 2.绕过文件大小自校验

将脱壳后的新程序拖入OD，设置API断点

![](/image/crack/reverse-esp-and-getfilesize/11.png)

![](/image/crack/reverse-esp-and-getfilesize/12.png)
设置好后运行，程序断在设置的断点。
![](/image/crack/reverse-esp-and-getfilesize/13.png)
在堆栈窗口中右键，在反汇编窗口中跟随
![](/image/crack/reverse-esp-and-getfilesize/14.png)
重新下断点，并且删除掉原来断点，重新运行
发现调用getfilesize后进行了cmp比较，之后跳转实现，一共比较了三次。我们将3次跳转全部nop掉
![](/image/crack/reverse-esp-and-getfilesize/16.png)
保存文件
![](/image/crack/reverse-esp-and-getfilesize/17.png)

### 验证
1_1程序能正常打开
![](/image/crack/reverse-esp-and-getfilesize/18.png)