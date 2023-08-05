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

import pprint
import asyncio

from MishmashSet import MishmashSet
from MishmashExceptions import MishmashNoConfigException

from net.ConnectionFactory import ConnectionFactory
from net.MishmashConnectionParameters import MishmashConnectionParameters
from net.MishmashStream import MishmashStream
from net.MishmashMutation import MishmashMutation

ATTR = ["_set", "loop", "connection_parameters", "is_async"]


class Mishmash():
    # TODO copy all configs or just override __copy __deepcopy in new mishmash do i need it ?
    # TODO can i have empty config file
    # TODO add async logic
    # logical operations over sets

    def __init__(self, loop=None, config=None):
        #TODO first is config
        if config:
            self._set = MishmashSet()
            self.connection_parameters = MishmashConnectionParameters(config)
            self.is_async = False
            self.loop = loop
            ConnectionFactory.set_connection(self.connection_parameters)

    def __len__(self):
        return len(self._set)

    def __getitem__(self, name):

        new_mishmash = self.intersection(name)
        if self.is_async:
            print("not implemented async logic")

        return new_mishmash

    # def __eq__(self, s):
    #     print(self._set, s)
    #     return "{}=={}".format(self._set, s)

    def __setitem__(self, name, value):
        base_set = self._set
        # print(base_set, name)
        print(name, value)
        if name:
            base_set = self._set.intersection(name)

        self.upload(base_set, value)

    def __getattr__(self, name):
        if name in ATTR:
            return super().__getattribute__(name)
        # dot notation - triggered when invoking inaccessible methods in an object context
        return self.__getitem__(name)

    def __setattr__(self, name, value):  # TODO smarter way to avoid recursion

        if name in ATTR:
            super().__setattr__(name, value)
        else:
            self.__setitem__(name, value)

    def __call__(self, *args, **kwargs):
        # called when a script tries to call an object as a function => then Mishmash call union

        if not args and not kwargs:
            return self
        elif args and not kwargs:
            return self.union(*args)
        elif kwargs and not args:
            return self.union(kwargs)
        else:
            return self.union([*args, kwargs])

    def __iter__(self):
        for i in self.download():
            yield i

    def new_mishmash(self, new_set):
        # // return new 'child' Mishmash object, inheriting all settings from $this
        # todo more pytonic way to copy params
        res = self.__class__()
        # res.__dict__ = self.__dict__
        res._set = new_set
        res.is_async = self.is_async
        res.loop = self.loop
        res.connection_parameters = self.connection_parameters

        return res

    def args_for_set(self, *args):
        # TODO Add named args to args for set ?#
        # TODO move to utils ??

        # // transform user arguments into MishmashSet values
        tranformed_arg = []
        for arg in args:
            # if self.is_scalar_mishmash(arg):
            #     tranformed_arg.append(self.get_from_scalar(arg)._set)
            # else:
            if isinstance(arg, Mishmash):
                tranformed_arg.append(arg._set)
            else:
                tranformed_arg.append(arg)

        return tranformed_arg

    def union(self, *offset):
        # // return a 'united' set
        return self.new_mishmash(self._set.subset().union(*self.args_for_set(*offset)))

    def intersection(self, *offset):
        # // return a subset
        return self.new_mishmash(self._set.intersection(*self.args_for_set(*offset)))

    def __sync_download(self, stream):
        pass

    async def __async_download(self, stream):

        # async for i in stream.stream(self._set):
        #     s = await i
        #     pprint.pprint(s)
        return await stream.stream(self._set)
    # def __anext__():
    #     pass

    def download(self):
        stream = MishmashStream()

        s = stream.stream(self._set)
        loop = asyncio.get_event_loop()

        while True:
            try:
                yield loop.run_until_complete(s.__anext__())
            except StopAsyncIteration:
                break

    def upload(self, base_set, *values):
        # TODO use kwargs args ?
        print("---------------\n\n\n\n\n", base_set)
        mutation = MishmashMutation()
        print("start mutation")
        m = mutation.mutate(base_set, *values)
        
        if not self.loop:
            self.loop = asyncio.get_event_loop()

        
        try:
            self.loop.run_until_complete(m)
        except Exception as e:
            print(e)
        print("-------------------- end upload\n\n")
