from flask import Flask
from proxy import *
import time

app = Flask(__name__)


@app.route('/')
def pool_restock():
    return proxy_pool_restock()


# https://www.ip138.com/ 查看ip
# https://www.cip.cc/ #查看ip 测试时可以用cip.cc作为请求站点

if __name__ == '__main__':
    start_run(test_data=None)
    app.run()
