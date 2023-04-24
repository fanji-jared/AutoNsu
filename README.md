# AutoNsu前言：

本程序使用python语言编写，用于自动登录Nsu校园网，
以此来优化大家的联网体验

# 文件介绍：

- [最初版本源码](./2022-11-9最初版)
<br>里面又分为了有ui版本(最初还设计了php云控，挺拉的)和无ui版本
<br>* 可惜在配置方面，密码必须从控制台的请求中抓取，然后放到代码中

- [最终版本源码](./2022-11-9最初版)
<br>这个版本主要是在最初版本的无ui版本的基础上进行开发
<br>* 将主程序与配置脚本相分离，可以直接在setConfig.py中配置相关信息，运行后生成配置文件
<br>** 解决了前一个版本的密码痛点，setConfig.py中可以直接配置原文密码

- [打包后的使用版本](./使用版本)
<br>如果你对源码不感兴趣，想要直接使用
<br>那就点击下载[主程序](./使用版本/AutoNsu.exe)与[配置脚本](./使用版本/setConfig.py)
<br>并阅读以下使用教程

# 使用教程：

1.首先将下载下来的两个文件拖动到桌面上
<br>
2.打开setConfig.py，编辑好相应的用户名和密码以及你要上线的套餐名称(TC)
<br>
3.运行此配置脚本，可以用cmd运行
<br>
```python
python setConfig.py
```
建议：可以右键创建一个主程序的快捷方式，将快捷方式拖动到* 公共自启动文件夹 *(win+r打开运行窗口输入以下代码打开)。
这样开机就能自动联网了！爽！
```shell
shell:Common Startup
```
注意：必须将主程序AutoNsu.exe放置在桌面

# 贡献：

欢迎贡献！请随意 fork 该仓库并提交 pull requests。

# 许可证：

本项目采用 GNU 许可证。有关详情，请参见 LICENSE 文件。
