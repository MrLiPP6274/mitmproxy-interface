"""
@Time   ：1:08 下午
@Author ：li
@decs   ：demo
"""
import time
import interface
from interface.interface_enum import InterfacePath


# 1.清除本地缓存
interface.clean_local()

# 2.运行mitmproxy：默认运行InterfaceMonitor类，默认端口为8080，也可以自己设定
interface.run()
# interface.run(scipt='ResponseMock, InterfaceMonitor', port='8888')

# 3.调用接口，存入数据：程序暂停期间，发起接口请求，将接口数据存入本地
time.sleep(20)

# 4.关闭mitmproxy
interface.stop()

# 5.获取接口数据，获取到的数据等于flow，保留flow.request和flow.response的原汁原味
# request
requestdata = interface.get(InterfacePath.TEST1).request
print(requestdata.url)
print(requestdata.query)
print(requestdata.json())
print(requestdata.headers)

# response
responsedata = interface.get(InterfacePath.TEST1).response
print(responsedata.url)
print(responsedata.json())
print(responsedata.headers)
