"""
@Time   ：2021/10/27 7:16 下午
@Author ：maqiang.lipp
@decs   ：接口公共方法
"""
import os
import yaml
import threading
import shutil
import requests
from mitmproxy.http import Request, Response, Headers


FILEPATH = os.path.dirname(os.path.abspath(__file__))


class InterfaceData:
    """
    接口数据类
    """
    def __init__(self, interfacepath):
        self.interfacepath = interfacepath.value
        self.request = self._get_request()
        self.response = self._get_response()

    def _get_request(self):
        requestpath = FILEPATH + '/interface_data' + self.interfacepath + '/request.yaml'
        if os.path.exists(requestpath):
            print('获取本地数据，数据源：{}'.format(requestpath))
            requestdata = yaml.safe_load(open(requestpath, 'r', encoding='utf-8'))
            requestdatalist = [
                requestdata['host'],
                requestdata['port'],
                requestdata['method'].encode(),
                requestdata['scheme'].encode(),
                requestdata['authority'].encode(),
                requestdata['path'].encode(),
                requestdata['http_version'].encode(),
                Headers(self._dict_to_list(requestdata['headers'])) if requestdata['headers'] != '' else None,
                requestdata['content'].encode(),
                Headers(self._dict_to_list(requestdata['trailers'])) if requestdata['trailers'] != '' else None,
                requestdata['timestamp_start'],
                requestdata['timestamp_end']
            ]
            return Request(*requestdatalist)

    def _get_response(self):
        responsepath = FILEPATH + '/interface_data' + self.interfacepath + '/response.yaml'
        if os.path.exists(responsepath):
            print('获取本地数据，数据源：{}'.format(responsepath))
            responsedata = yaml.safe_load(open(responsepath, 'r', encoding='utf-8'))
            responsedatalist = [
                responsedata['http_version'].encode(),
                responsedata['status_code'],
                responsedata['reason'].encode(),
                Headers(self._dict_to_list(responsedata['headers'])) if responsedata['headers'] != '' else None,
                responsedata['content'].encode(),
                Headers(self._dict_to_list(responsedata['trailers'])) if responsedata['trailers'] != '' else None,
                responsedata['timestamp_start'],
                responsedata['timestamp_end']
            ]
            return Response(*responsedatalist)

    def _dict_to_list(self, data: dict):
        li = []
        for key in data:
            li2 = data[key]
            for i in li2:
                li.append((key.encode(), i.encode()))
        return li


class Interface:
    _port = None
    _scipt = None
    _thread = None

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '_instance'):
            with threading.Lock():
                Interface._instance = super().__new__(cls)
        return Interface._instance

    def run(self, scipt, port):
        print('打开mitmdump服务')
        self._scipt = scipt
        self._port = port
        self._thread = threading.Thread(target=self._proxy)
        self._thread.start()

    def stop(self):
        print('关闭mitmdump服务')
        proxies = {
            'http': 'http://127.0.0.1:{}'.format(self._port)
        }
        requests.get('http://shutdown.mitmdump.com/', proxies=proxies)

    def get(self, interfacename):
        print('获取接口数据，接口路径为：{}'.format(interfacename.value))
        return InterfaceData(interfacename)

    def clean_local(self):
        print('清除本地缓存数据')
        dirname = FILEPATH + '/interface_data'
        if os.path.exists(dirname):
            shutil.rmtree(dirname)
        os.mkdir(dirname)

    def _proxy(self):
        gotodir = 'cd {}'.format(FILEPATH)
        args = 'mitmdump -q -p {} -s interface_monitor.py {}'.format(self._port, self._scipt)
        command = gotodir + '\n' + args
        print(gotodir)
        print(args)
        os.system(command)


if __name__ == '__main__':
    pass
