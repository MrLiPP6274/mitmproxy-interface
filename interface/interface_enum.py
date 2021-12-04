"""
@Time   ：2021/10/27 6:03 下午
@Author ：li
@decs   ：Interface_enum
"""
from enum import Enum


class InterfacePath(Enum):
    TEST1 = '/test/get'  # 调试接口1
    TEST2 = '/test/post'  # 调试接口2

