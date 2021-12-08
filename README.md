# 说明
本框架是一个基于mitmproxy工具的调用框架，旨在于更方便的运行mitmproxy，完成接口监听、接口数据处理

本篇说明假设读者有基本的 python、mitmproxy 知识，且已经安装好了一个 python3 开发环境

# 安装使用
## 依赖环境
* python>=3.8
* pyyaml
* requests
* mitmproxy>=7.0.2

## 代码获取
下载代码到本地工程即可使用

## 配置项
你可以在interface/interface_enum.py中设置监听的接口列表

## 使用示例
见demo.py文件

# api
interface.run

```
声明：def run(scipt='InterfaceMonitor', port='8080'):
作用：启动mitmdump监听
参数：scipt - mitmdump addons列表，默认值InterfaceMonitor
     port  - mitmproxy运行端口，默认值8080
返回：无
```

interface.stop
```
声明：def stop():
作用：停止mitmdump监听
参数：无
返回：无
```

interface.get
```
声明：def get(interfacename):
作用：获取接口数据
参数：interfacename - 接口名称
返回：InterfaceData()实例
```

interface.clean_local
```
声明：def clean_local():
作用：清除本地缓存
参数：无
返回：无
```

# Author

**mitmproxy-interface** © [LiPP](https://github.com/MrLiPP6274), Released under the [MIT License](./LICENSE) License

> Blog [@漓白白"](https://www.cnblogs.com/m1031478472/)
> 
> GitHub [@GitHub](https://github.com/MrLiPP6274)
> 
> Email llbai_m@163.com
