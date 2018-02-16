from abc import abstractmethod

from glumpy import gl, gloo
import numpy as np

from pipeline.synthesis.opengl.prelude import OpenGLProcessor
from pipeline.utils import process_param


class Shader(OpenGLProcessor):
    def __init__(self,
                 vertex, fragment,
                 vertex_count, attributes, uniforms,
                 *args, **kwargs):
        self.uniforms = {
            name: process_param(param)
            for name, param in uniforms.items()
        }
        self.attributes = {}
        attr_shapes = []
        for name, (count, param) in attributes.items():
            attr_shapes.append((name, np.float32, count))
            self.attributes[name] = process_param(param)

        self.vertex_count = vertex_count
        self.vertex_buffers = np.zeros(
            self.vertex_count, attr_shapes
        ).view(gloo.VertexBuffer)
        self.program = gloo.Program(
            vertex=vertex, fragment=fragment,
            *args, **kwargs
        )

    def __call__(self, surface, t):
        self.load_buffers(t)
        self.draw(t)

    def load_buffers(self, t):
        for name, func in self.attributes.items():
            v = self.as_vertex_buffer(
                func(t),
                self.vertex_buffers[name].shape[-1]
            )
            self.vertex_buffers[name] = v
        self.program.bind(self.vertex_buffers)
        for name, func in self.uniforms.items():
            self.program[name] = func(t)

    @abstractmethod
    def draw(self, t):
        pass

    @staticmethod
    def as_vertex_buffer(points, depth):
        return np.array(points, dtype=np.float32).reshape((-1, depth))
    
    @staticmethod
    def as_index_buffer(points):
        return np.array(points, dtype=np.uint32).view(gloo.IndexBuffer)

