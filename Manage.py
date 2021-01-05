#!/usr/bin/env python
import os
from Interface import create_app
from Interface.utils import SystemFail, return_json

app = create_app(os.getenv('FLASK_CONFIG') or 'default')


@app.errorhandler(Exception)
def handle_invalid_usage(error):
    print(error)
    return return_json(SystemFail)


if __name__ == '__main__':
    # threaded 开启多线程
    # 使用genvent做协程，解决高并发  待研究
    app.run(host='0.0.0.0', threaded=True)
