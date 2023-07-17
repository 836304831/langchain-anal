# 项目介绍
为了能更好做基于语言大模型的应用，本项目对业界比较火的工具langchain做源码的分析。旨在更好的应用大预言模型为人类提供质量更好、效率更高、交互更加便捷的服务。

# 功能介绍
源码分析用到的图片、代码和配置等信息，均放在anal目录下；源码中的步骤介绍在该项目下对应的代码文件中。

## 模块关系图的使用
模块关系图的工具使用已经录制成视频，在[B站](https://www.bilibili.com/video/BV1iP411v7vY/?spm_id_from=333.999.0.0&vd_source=cd62f6bf001b64bc3c0e062e4c37bc6b) 
和[知乎文章](https://zhuanlan.zhihu.com/p/639056301) 及 [知乎视频](https://www.zhihu.com/zvideo/1655946356811079680) 都可以找到，工具的步骤如下：

    1. 安装graphviz
        从官网中下载(graphviz)[http]，安装python环境一样安装
    2. 模块关系图工具安装
        pip install pydeps
    3. 工具的使用
        pydeps xx.py -T png -o yy.png --max-bacon 3 --cluster

## 类关系图的使用
    
    1. 安装pyreverse
        pip install pylint   # pylint中包含了，pyreverse工具
    2. 工具的使用
        pyreverse -ASmy -o png ./xx.py   # 具体的参数可以通过"pyreverse -h"查看

# 已完成的部分
0. langchain的整体介绍, [B站视频](https://www.bilibili.com/video/BV1fF41197XT/?spm_id_from=333.999.0.0&vd_source=cd62f6bf001b64bc3c0e062e4c37bc6b) ,[知乎视频](https://www.zhihu.com/zvideo/1658864628527525888) ,[知乎文章](https://zhuanlan.zhihu.com/p/640848809)
1. chat_models源码分析, [B站视频](https://www.bilibili.com/video/BV1fF41197XT?p=2&vd_source=cd62f6bf001b64bc3c0e062e4c37bc6b) ,[知乎视频](https://www.zhihu.com/zvideo/1661208710797172736)
2. promptTemplate源码分析, [B站视频](https://www.bilibili.com/video/BV1fF41197XT?p=3&vd_source=cd62f6bf001b64bc3c0e062e4c37bc6b) ,[知乎视频](https://www.zhihu.com/zvideo/1663740505211957248)
