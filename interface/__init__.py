"""
@Time   ：2021/10/27 7:15 下午
@Author ：li
@decs   ：__init__.py
"""
from interface_method import Interface


def run(scipt='InterfaceMonitor', port='8080'):
    """
    启动mitmdump监听
    :param scipt:监听方法
    :param port:监听端口
    :return:None
    """
    Interface().run(scipt, port)


def stop():
    """
    停止mitmdump监听
    :return:None
    """
    Interface().stop()


def get(interfacename):
    """
    获取接口数据
    :param interfacename:Enum接口名称
    :return: 接口数据
    """
    return Interface().get(interfacename)


def clean_local():
    """
    清除本地缓存
    :return:
    """
    Interface().clean_local()


if __name__ == '__main__':
    run()
