class Pipeline:
    def __init__(self, stages):
        self.stages = stages

    def run(self, sink):
        sink(pipeline=self.stages).consume()
