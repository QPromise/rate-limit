# coding=utf-8
from flask import Flask
import token_bucket
import leak_bucket

app = Flask(__name__)


@app.route('/')
@token_bucket(rate=2, default=5)
def hello_world():
    '令牌桶算法测试'
    return 'Hello World!'


@app.route('/test')
@leak_bucket(rate=3, default=20)
def hello():
    '漏桶算法测试'
    return 'hello test'


if __name__ == '__main__':
    app.run(port=8070, debug=True)

