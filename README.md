# minimap_renderer_web

minimap_renderer项目的web服务支持

### 有问题请加群 967546463

本项目为 https://github.com/benx1n/HikariBot 的扩展支持

请先安装好python环境 python版本大于等于3.10

# 部署流程

LLOneBot插件版本必须大于等于 v3.31.6

go-cq-http 用户需要配置 ffmpeg 

文档： https://docs.go-cqhttp.org/guide/quick_start.html#%E5%AE%89%E8%A3%85-ffmpeg

LL bot请打开这个设置，NapChat如果运行有问题也请看看有没有类似设计

![deed24829cb2739d7855fc3e29e1edde.png](temp%2Fdeed24829cb2739d7855fc3e29e1edde.png)

首先 把 https://github.com/WoWs-Builder-Team/minimap_renderer 项目克隆到本地

把本项目的以下文件复制到minimap_renderer根目录下

`src` 文件夹

`temp` 文件夹

`token.json` 文件

`安装依赖.bat` 文件

`运行.bat` 文件

复制后的根目录有以下文件

![257368cc83c92fe8dcd18558b2644816.png](temp%2F257368cc83c92fe8dcd18558b2644816.png)

src目录里面

![00b17fe4ce2e4966dbed620093b66f79.png](temp%2F00b17fe4ce2e4966dbed620093b66f79.png)


先执行 `安装依赖.bat` 然后执行 `运行.bat`

如果是conda环境部署，请自行复制.bat文件的内容执行

安装依赖遇到报错请执行以下命令

`python.exe -m pip install --upgrade pip http://mirrors.aliyun.com/pypi/simple --trusted-host mirrors.aliyun.com`

重新执行一次`安装依赖.bat`