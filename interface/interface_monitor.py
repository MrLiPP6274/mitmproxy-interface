"""
@Time   ：2021/10/27 7:16 下午
@Author ：li
@decs   ：mitmdump监听
"""
import os
import sys
import yaml
from mitmproxy import http, ctx
from interface_enum import InterfacePath


FILEPATH = os.path.dirname(os.path.abspath(__file__))
INTERFACEENUM = InterfacePath


class InterfaceMonitor:
    """
    接口数据监听
    """
    def request(self, flow: http.HTTPFlow):
        path = flow.request.path.split('?')[0]
        if path in INTERFACEENUM._value2member_map_:
            print('监听到接口请求：{}'.format(path))
            di = {
                'host': flow.request.host,
                'port': flow.request.port,
                'method': flow.request.method,
                'scheme': flow.request.scheme,
                'authority': flow.request.authority,
                'path': flow.request.path,
                'http_version': flow.request.http_version,
                'headers': self.MultiDict_to_Dict(flow.request.headers),
                'content': flow.request.text,
                'trailers': self.MultiDict_to_Dict(flow.request.trailers),
                'timestamp_start': flow.request.timestamp_start,
                'timestamp_end': flow.request.timestamp_end
            }
            self.data_into_yaml(di, path, 'request')

    def response(self, flow: http.HTTPFlow):
        path = flow.request.path.split('?')[0]
        if path in INTERFACEENUM._value2member_map_:
            print('监听到接口响应：{}'.format(path))
            di = {
                'http_version': flow.response.http_version,
                'status_code': flow.response.status_code,
                'reason': flow.response.reason,
                'headers': self.MultiDict_to_Dict(flow.response.headers),
                'content': flow.response.text,
                'trailers': self.MultiDict_to_Dict(flow.response.trailers),
                'timestamp_start': flow.response.timestamp_start,
                'timestamp_end': flow.response.timestamp_end
            }
            self.data_into_yaml(di, path, 'response')

    def MultiDict_to_Dict(self, data):
        if data is None:
            return ''
        di = {}
        for key in data.keys():
            di[key] = data.get_all(key)
        return di

    def data_into_yaml(self, data, interfacepath, types):
        dirpath = FILEPATH + '/interface_data' + interfacepath
        if not os.path.exists(dirpath):
            os.makedirs(dirpath)

        yamlname = types + '.yaml'
        yamlpath = os.path.join(dirpath, yamlname)

        print('存入接口数据到{}'.format(yamlpath))
        with open(yamlpath, 'w') as f:
            f.write(yaml.safe_dump(data))
            f.flush()
            f.close()


class Shutdown:
    """
    关闭mitmproxy
    """
    def request(self, flow: http.HTTPFlow):
        if flow.request.pretty_url == "http://shutdown.mitmdump.com/":
            flow.response = http.Response.make(
                200,
                'mitmdump shutdown'.encode(),
                {"Content-Type": "text/html"}
            )

    def response(self, flow: http.HTTPFlow):
        if flow.request.pretty_url == "http://shutdown.mitmdump.com/":
            print('mitmdump shutdown')
            ctx.master.shutdown()


class ResponseMock:
    def response(self, flow: http.HTTPFlow):
        path = flow.request.path.split('?')[0]
        interfacename = INTERFACEENUM.TEST
        if path == interfacename.value:
            print('ResponseMock: {}'.format(path))
            flow.response.text = self.maploacl(interfacename)

    def maploacl(self, interface):
        filedi = {
            InterfacePath.TEST: 'test.txt',
        }
        mockpath = FILEPATH + '/interface_mock/' + filedi[interface]
        with open(mockpath, 'r') as f:
            text = f.read()
        return text


def set_addons():
    li = sys.argv[6].split(',')
    li.append('Shutdown')
    print('mitmdump addons 列表：' + str(li))
    for i in range(len(li)):
        li[i] = globals()[li[i]]()
    return li


addons = set_addons()
