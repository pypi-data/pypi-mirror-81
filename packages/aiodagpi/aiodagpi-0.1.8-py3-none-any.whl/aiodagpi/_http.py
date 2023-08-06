'''The MIT License (MIT)

Copyright (c) 2020 Raj Sharma

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
SOFTWARE.'''

import aiohttp
from aiodagpi.exceptions import *

codes = {
    401:InvalidToken()
}

class http:
    def __init__(self):
        self.codes = codes
        self.session = None

    async def makesession(self):
        if not self.session:
            self.session = aiohttp.ClientSession()

    async def closesession(self):
        if self.session:
            await self.session.close()
            self.session = None

    async def get(self, url, headers=None):
        await self.makesession()
        async with self.session.get(url=url, headers=headers) as cs:
            if cs.status == 200:
                return await cs.json()
            elif cs.status in self.codes:
                toraise = self.codes[cs.status]
                raise toraise()
            else:
                raise UnCaughtError(code=cs.status, error=cs.reason)
