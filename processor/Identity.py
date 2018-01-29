from pipeline.processor.Processor import Processor


class Identity(Processor):

    def iterate(self):
        yield from iter(self.source)
