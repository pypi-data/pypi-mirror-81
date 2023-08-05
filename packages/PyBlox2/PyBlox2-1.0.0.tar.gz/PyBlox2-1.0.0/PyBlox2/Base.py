"""
`Base` is the main module for Data Containers and objects that manage ineractions with the API

Contents:
    `BloxType`: No parents
    `DataContainer`: No parents
    `Emitter`: `DataContainer`
    `CommandEmitter`: `Emitter`

Requires:
    `Errors`: `AttributeNotFetched`

The following code is provided with: 

    The MIT License (MIT)

    Copyright (c) Kyando 2020

    Permission is hereby granted, free of charge, to any person obtaining a copy
    of this software and associated documentation files (the "Software"), to deal
    in the Software without restriction, including without limitation the rights
    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
    copies of the Software, and to permit persons to whom the Software is
    furnished to do so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included in all
    copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
    SOFTWARE.
"""

from .Errors import AttributeNotFetched

class BloxType():
    '''
    The base class for most high level items.

    Can be fetched and has fetchables

    ```
        class MyCustomBloxType(BloxType):

            def __init__(self):
                self.fetchable = []
                self.can_fetch("money")

            def fetch_money(self):
                # Send a request to the API and get the amount of money
                return 200 # For the sake of this example, let's say it's 200

        # In an async context
        MyCustomInstance = MyCustomBloxType()

        MyCustomInstance.money
        >> AttributeNotFetched: Attribute 'money' was accessed before being fetched
        await MyCustomInstance.fetch("money")
        >> 200
        MyCustomInstance.money
        >> 200
    ```

    Will raise "NotImplementedError" if the fetch_{attr} where {attr} is the name of the attribute, function doesn't exist.
   
    '''
    def __init__(self, client):
        self.client = client
        self.fetchable = []

    async def fetch(self, *attrs):
        for attr in attrs:
            if attr in self.fetchable:
                resp = await self._fetcher(attr)
                setattr(self, "_"+attr, resp)
                return resp

    def can_fetch(self, *data):
        self.fetchable.extend(data)

    async def _fetcher(self, attr):
        coro = getattr(self, "fetch_"+attr) 
        if coro == None:
            raise NotImplementedError("Attribute {0} hasn't been implemented yet for {1}".format(attr, self.__class__.__name__))
        return await coro()
    
    def __getattr__(self, attr):
        fetchables = self.fetchable
        if attr in fetchables:
            try:
                return getattr(self, "_"+attr)
            except AttributeError:
                raise AttributeNotFetched(attr)

class DataContainer():
    """
    Abstract class emulating a dict type by using a hidden __data value
    This class still allows access through the object.attribute notation
    """
    def __init__(self):
        self.__data = {}

    def find(self, name):
        if name in self.__data:
            return self.__data[name]
        return None

    def add(self, key, value):
        self.__data[key] = value
        
    def is_empty(self):
        if self.__data:
            return False
        return True

    def __getitem__(self, key):
        return self.find(key)
    
    def __setitem__(self, key, value):
        self.add(key, value)

    def __contains__(self, key):
        if key in self.__data:
            return True
        return False

    def __iter__(self):
        return iter(self.__data)
    
    def __getattr__(self, key):
        if self[key]:
            return self[key]
        return None

class Emitter(DataContainer):
    """
    A DataContainer storing coros in its __data and firing them when necessary with a given playload
    """
    def __init__(self):
       super().__init__()

    async def fire(self, name, payload):
        coro = self.find(name)
        if coro:
            await coro(*payload)
            return True
        return False

class CommandEmitter(Emitter):
    """
    A modified Emitter which fires the coros with a ctx argument and an args argument
    """
    def __init__(self):
       super().__init__()

    async def fire(self, name, ctx, args):
        coro = self.find(name)
        if coro:
            await coro(ctx, *args)



