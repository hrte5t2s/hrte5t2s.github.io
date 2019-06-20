---
layout: post
comments: true
categories: linux
---

## 安装配置opnsense-firewall记录
### 下载OpnSense防火墙
官网：`https://opnsense.org`
### 安装
新建虚拟机，这里选择freebsd。
启动之后，直接等默认进入

![](/image/opnsense/opnsense1.png)

这里账号密码为`installer`，`opnsense`

之后开始安装
![](/image/opnsense/opnsense2.png)

在安装的过程中要选择硬盘，启动方式，密码之类的安装linux的常规选项

![](/image/opnsense/opnsense3.png)

### 配置
再次重启后进入一下界面

![](/image/opnsense/opnsense4.png)

#### 主要是配置选项1和2
- 选项1是网卡配置，LAN为局域网网卡，WAN为链接的外网网卡。这里检测到了两块，命名为em0和em1，可以根据mac地址确定哪个是那块网卡，然后在设置时，分别输入em0和em1，如果还有网卡，继续输入，如果没有了，直接回车。
- 选项2是对网卡的ip配置，WAN为DHCP，上层网卡分配到的ip，LAN的ip可以配置ip段和子网掩码，并且如果有多个LAN时，还可以配置管理的HTTP页面从哪个网段进行登录。

### web配置
最后就是从设置的ip登录进去，对路由，防火墙进行设置

![](/image/opnsense/opnsense5.png)

