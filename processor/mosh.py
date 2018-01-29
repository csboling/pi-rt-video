import struct

import numpy as np

from pipeline.processor.Mosher import Mosher


class Wordpadify(Mosher):

    def mosh(self, raw):
        yield raw.replace(b'\x0b', b'\x0d0a')


class ByteSwap(Mosher):

    def __init__(self, chunksize=4, packstr='<{}f', unpackstr='>{}i'):
        self.chunksize = chunksize
        self.packstr = packstr
        self.unpackstr = unpackstr

    def mosh(self, raw):
        yield struct.pack(
            self.packstr.format(len(raw) // self.chunksize),
            *struct.unpack(self.unpackstr.format(len(raw) // self.chunksize), raw)
        )
