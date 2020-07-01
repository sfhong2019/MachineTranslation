#!/usr/bin/python
# -*- coding: UTF-8 -*-

import http.client
import urllib.parse


class POST:
    def do_post(self, url=None, params=None):
        # 与服务器建立链接
        url = 'localhost:8899'
        conn = http.client.HTTPConnection(url)

        # 向服务器发送请求
        method = "POST"
        req_url = "/translate/"
        header_data = {
            "Content-Type": "application/x-www-form-urlencoded",
        }
        test_data = urllib.parse.urlencode({
            "to_lang": params['to_lang'],
            "input_text": params['input_text'],
        })
        conn.request(method=method, url=req_url, body=test_data, headers=header_data)

        # 获取响应消息体
        response = conn.getresponse()
        print(response.status, response.reason)
        data = response.read()
        print(data)

        # 获取响应头部信息，列表形式
        res_header = response.getheaders()
        print(res_header)

        # 取出响应头部的Set-Cookie的值
        response_head = response.getheader('Set-Cookie')
        print(response_head)
        conn.close()


if __name__ == '__main__':
    translate_corpus = [
        ('en', '今天天气不错.'),
    ]

    from time import sleep
    from random import random
    p = POST()
    for to_lang, input_text in translate_corpus:
        p.do_post(params={'to_lang': to_lang, 'input_text': input_text})
        sleep(1+random()*2)


