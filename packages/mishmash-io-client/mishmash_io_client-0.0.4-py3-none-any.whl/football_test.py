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

import asyncio
from inspect import getsource
from Mishmash import Mishmash

from net.MishmashConnectionParameters import MishmashConnectionParameters
import net.MishmashMessages as MishmashMessages
# params = {"url": '127.0.0.1', "port": 8980}
# params = {"url": '10.3.0.102', "port": 8980}
params = {"url": 'mishmash-io-dummy-1.cloud-test.mesos', "port": 8980}
mishmash = Mishmash(config=params)

print(dir(mishmash))

def func1(a, b):
    c = a + b
    return c


def func2(a, b=7):
    c = a - b
    return c


def func3():
    return "just string"

f = mishmash("asdf", func1, func2)

for i in f:
    print(i)