# coding=utf-8
import requests
import time

#先运行app.py，再运行这个。
url1 = 'http://localhost:8070/'
url2 = 'http://localhost:8070/test'
for i in range(50):
    res = requests.get(url1)
    print(res.status_code, '1', res.text)
    res = requests.get(url2)
    print(res.status_code, '2', res.text)
    time.sleep(0.1)
