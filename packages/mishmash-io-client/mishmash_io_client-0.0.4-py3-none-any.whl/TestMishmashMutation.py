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

from Mishmash import Mishmash

# params = {"url": 'mishmash-io-dummy-1.cloud-test.mesos', "port": 8980}
params = {"url": '127.0.0.1', "port": 8980}
mishmash = Mishmash(config=params)

mishmash["all_data"] = ["asdf",1,2,3]
