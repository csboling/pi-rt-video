import random
import re
import struct

import numpy as np

from pipeline.processor.Mosher import Mosher


class ReverseBytes(Mosher):
    def mosh(self, raw):
        yield raw[::-1]


class Wordpadify(Mosher):

    def mosh(self, raw):
        yield raw.replace(b'\x0b', b'\x0d0a')


class Repack(Mosher):

    def __init__(self, chunksize=4, packstr='<{}f', unpackstr='>{}i'):
        self.chunksize = chunksize
        self.packstr = packstr
        self.unpackstr = unpackstr

    def mosh(self, raw):
        chunks, remainder = divmod(len(raw), self.chunksize)
        if remainder:
            raw += raw[:self.chunksize - remainder]
            chunks += 1
        yield struct.pack(
            self.packstr.format(chunks),
            *struct.unpack(self.unpackstr.format(chunks), raw)
        )


class MangleBytes(Mosher):

    def __init__(self, moshers: [Mosher]):
        self.moshers = moshers

    def mosh(self, raw):
        pos = 0
        while pos < len(raw):
            chunksize = random.randint(4096, 65536)
            chunk = raw[pos:pos+chunksize]
            yield self.mangle(chunk)[:chunksize]
            pos += chunksize

    def mangle(self, chunk):
        return next(random.choice(self.moshers).mosh(chunk))


class Replace(Mosher):

    def __init__(self, pattern, substitution):
        self.pattern = pattern
        self.substitution = substitution

    def mosh(self, raw):
        yield re.sub(self.pattern, self.substitution, raw)
