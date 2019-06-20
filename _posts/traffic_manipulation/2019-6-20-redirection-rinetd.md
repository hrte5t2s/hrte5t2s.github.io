---
layout: post
comments: true
categories: traffic_manipulation
---

## 流量重定向——rinetd

### 假设场景
- 内网机器想访问外网，但是只允许53端口或者22端口通过
- 渗透测试时，通过80拿下内网机器，但是只允许53或者22进入

### 实验环境
- opnsense做为中间防火墙，连接LAN与WAN两个网络，只允许LAN区的DNS port通过
- LAN区一台bodhi linux，`ip:1.1.1.10`
- WAN区一台kali,`ip:10.10.10.15`

### 配置实验环境
1. opnsense配置防火墙规则,只允许53端口通过

![](/image/traffic_manipulation/rinetd/rinetd_1.png)

2. bodhi上测试，ping百度，能解析dns，但是数据包全部丢失

![](/image/traffic_manipulation/rinetd/rinetd_2.png)

3. kali安装并配置rinetd
`apt-get install rinetd`

![](/image/traffic_manipulation/rinetd/rinetd_3.png)

rinetd的配置文件在`/etc/rinetd.conf`

![](/image/traffic_manipulation/rinetd/rinetd_4.png)

在这一行下面填上要转发的端口和地址即可
># bindadress    bindport  connectaddress  connectport

进行如下修改：

![](/image/traffic_manipulation/rinetd/rinetd_5.png)

并启动rinetd，直接在终端输入rinetd 并回车

### 测试
在bodhi上访问kaliip+53端口