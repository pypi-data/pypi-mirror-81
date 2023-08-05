# Copyright 2019 MISHMASH I O OOD
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from flask import json
from flask import request
import asyncio
from flask import Flask
import time
from Mishmash import Mishmash
from datetime import date
import requests

params = {"url": '10.3.0.102', "port": 8980}
#
# params = {"url": '127.0.0.1', "port": 8980}
config = {

    "metrics": {
        "url": 'http://os-id.mishmash.local:5050/master/state',
        "timeout": 1
    },
    "rbac": {
        "url": 'https://jsonplaceholder.typicode.com/todosF',
        "timeout": 0
    }
}


def set_data():
    mishmash = Mishmash(None, params)

    for i in range(1, 2):
        for k in config:
            mishmash[k][str(date.today())] = requests.get(config[k]["url"]).json()
            time.sleep(config[k]["timeout"])


app = Flask(__name__)
loop = asyncio.get_event_loop()
mishmash = Mishmash(loop, params)

set_data()

@app.route('/', defaults={'u_path': ''}, methods=['POST'])
@app.route('/<path:u_path>', methods=['POST'])
def process_log_request(u_path):

    if not u_path:
        return None

    res = json.loads(request.get_data())
    paths = list(u_path.split('/'))
    print("-------------- ", res)
    mishmash[paths][str(date.today())] = res
    print("mutation end")
    return res


if __name__ == '__main__':
    app.run()
