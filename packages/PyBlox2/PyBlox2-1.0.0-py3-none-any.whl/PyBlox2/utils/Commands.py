"""
`Commands` utility

Contents:
    `Commander`: No parents
    `Context`: No parents

Requires:
    `Errors`: `*`
    `.utils`: `Url`

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

import logging

import asyncio

from ..Errors import *
from ..utils import Url


logger = logging.getLogger(__name__)


class Commander:
    """
    Manages looping through the group wall and checking for commands or messages

    Attrs:
        `prefix`
    
    Meths:
        N/A
    """
    async def start_listening(self, client, commands, listening_to):
        self.__commands = commands
        self.__client = client
        self.__listening_to = listening_to
        self.__already_seen = []
        self.__is_first = True
        self.prefix = client.prefix
        self.__access = Url("groups", "/v1/groups/%group_id%/wall/posts?limit=10&sortOrder=Desc", group_id=self.__listening_to.id)
        await self.start_loop()

    async def start_loop(self):
        await self.__client._emit("start_listening", (self.__listening_to,))
        while True:
            await self.__client._emit("check_messages", (self.__listening_to,))
            await self.check_messages()
            await asyncio.sleep(5)

    async def check_messages(self):
        hook = await self.__access.get()
        for msg in hook.json['data']:
            if self.__is_first:
                    self.__already_seen.append(msg["id"])
            if await self.check_entity(msg):
                await self.process_new_message(msg)
        if self.__is_first:
            self.__is_first = False

    async def check_entity(self, msg):
        if not msg["id"] in self.__already_seen:
           self.__already_seen.append(msg["id"])
           return True
        return False

    async def process_new_message(self, msg):
        text = msg["body"]
        flags = str.split(text, " ")
        ctx = await self.generate_context(msg)
        await self.__client._emit("message", ctx)
        if flags[0].startswith(self.prefix):
            flags[0] = flags[0].replace(self.prefix, "")
            await self.process_command(flags, ctx)

    async def process_command(self, flags, ctx):
        function_name = flags.pop(0)
        args = tuple(flags)
        try:
            await self.__client.push_command(function_name, ctx, args)
        except TypeError as e:
            if await self.__client._emit("error", (ctx, e)):
                return
            raise BadArguments(
                function_name
                )

    async def generate_context(self, msg):
        try:
            member = await self.__listening_to.get_member(msg["poster"]["username"])
        except:
            member = await self.__client.get_user(msg["poster"]["username"])
        return Context(member, msg["body"])

class Context:
    """
    Context object for message on group wall

    Attrs:
        `user` -> May return None
        `member` -> May return None
        `content`

    Meths:
        N/A

    This objects checks if its `__user_or_member` has a group to determine wether it is a user or not
    """
    def __init__(self, user, ctt):
        self.__user_or_member = user
        self.content = ctt

    @property
    def member(self):
        if self.__user_or_member.group:
            return self.__user_or_member
        return None

    @property
    def user(self):
        if not self.__user_or_member.group:
            return self.__user_or_member
        return None




