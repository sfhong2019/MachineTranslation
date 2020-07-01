# /usr/bin/env python
# coding=utf-8
from typing import List, Dict

import http.client
import hashlib
import urllib.request
import urllib.parse
import random
import json
import time

from threading import Thread, current_thread
import queue


# api翻译
class MachineTranslation:
    def __init__(self):
        # use for multi-thread
        self.q = queue.Queue()

    @staticmethod
    def translate_by_api(to_lang: str='zh', input: str='apple') -> str:
        ret = ''
        appid = '20190605000305156'         # appid
        secretKey = '35gcTMJqQF0stnj3TVTS'  # 密钥

        url = 'http://api.fanyi.baidu.com/api/trans/vip/translate'

        http_client = None
        salt = random.randint(32768, 65536)
        sign = appid + input + str(salt) + secretKey
        m1 = hashlib.new('md5')
        m1.update(sign.encode('utf-8'))
        sign = m1.hexdigest()
        url = url + '?q=' + urllib.request.quote(
            input) + '&from=' + 'auto' + '&to=' + to_lang + '&appid=' + appid + '&salt=' + str(salt) + '&sign=' + sign

        try:
            http_client = http.client.HTTPConnection('api.fanyi.baidu.com')
            http_client.request('GET', url)
            # response是HTTPResponse对象
            response = http_client.getresponse()
            result = response.read()

            data = json.loads(result)
            output = data['trans_result'][0]['dst']
            ret = output

        finally:
            if http_client:
                http_client.close()

        return ret

    def translate_by_api_bing(self, from_lang: str='en', to_lang: str='zh', input: str='apple', split: str='\n') -> str:
        ret = ''
        res: List[str] = []
        lines: List[str] = input.split(split)

        thread_count: int = 0
        thread_pool: List[Thread] = []

        start = time.time()
        for line in lines:
            t = Thread(target=self._do_translate_bing,
                       kwargs={'params': {'from': from_lang, 'to': to_lang, 'text': line}},
                       name=str(thread_count))
            thread_count += 1
            t.setDaemon(True)
            thread_pool.append(t)
            t.start()

        for t in thread_pool:
            t.join()
        print('time consume by bing api: {}'.format(time.time() - start))

        while self.q.qsize() > 0:
            res.append(self.q.get())

        res.sort(key=lambda k: k[0])
        for _, text in res:
            ret += text
            if _ < len(lines)-1:
                ret += '\n'

        return ret

    def _do_translate_bing(self, params=None):
        url = 'cn.bing.com'
        conn = http.client.HTTPConnection(url)
        ct = current_thread()

        if len(params['text']) == 0:
            self.q.put((int(ct.getName()), ''))
            return

        # 向服务器发送请求
        method = "POST"
        req_url = "/ttranslatev3/"
        header_data = {
            "Content-Type": "application/x-www-form-urlencoded",
        }
        test_data = urllib.parse.urlencode({
            "from": params['from'],
            "to": params['to'],
            "text": params['text'],
        })
        conn.request(method=method, url=req_url, body=test_data, headers=header_data)

        # 获取响应消息体
        response = conn.getresponse()
        data: bytes = response.read()
        data: Dict = json.loads(data)
        # print(type(data))
        # print(data)
        conn.close()

        if isinstance(data, list) and 'translations' in data[0].keys():
        # if data['statusCode'] == 200:
            self.q.put((int(ct.getName()), data[0]['translations'][0]['text']))
        else:
            # 失败手动重试1次
            time.sleep(0.2)
            conn.request(method=method, url=req_url, body=test_data, headers=header_data)
            response = conn.getresponse()
            data: bytes = response.read()
            data: Dict = json.loads(data)
            if isinstance(data, list) and 'translations' in data[0].keys():
                self.q.put((int(ct.getName()), data[0]['translations'][0]['text']))
            else:
                self.q.put((int(ct.getName()), 'translation fail'))


if __name__ == '__main__':
    mt = MachineTranslation()
    text = "hello everyone i'm j\nto them i'm going to introduce our paper t v kia\nmy collaborators are remote and tamara\nreform unz top hill\nnow every introduced the tv created as it to you\nthe first large scale localized compositional radioactive answering did has said\nthis data is available at your project page\nthere are four advantages of our data set it\nthe first is large scale\nwith more than one hundred fifty sounds of key pairs\nsecond\nits compositional"
    t = mt.translate_by_api_bing('en', 'zh', text)
    print(text)
    print(t)
