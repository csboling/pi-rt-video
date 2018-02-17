from abc import abstractmethod
import re

from glumpy import gl, gloo
import numpy as np

from pipeline.synthesis.opengl.prelude import OpenGLProcessor
from pipeline.utils import process_param


class Snippet(gloo.Snippet):
    def __init__(self, *args, preserve_names=None, **kwargs):
        super().__init__(*args, **kwargs)
        if preserve_names is None:
            preserve_names = []
        self.preserve_names = preserve_names

    def mangled_code(self):
        """ Generate mangled code """

        code = self._source_code
        objects = self._objects
        functions = objects["functions"]
        names = objects["uniforms"] + objects["attributes"] + objects["varyings"]
        for _,name,_,_ in functions:
            symbol = self.symbols[name]
            code = re.sub(r"(?<=[^\w])(%s)(?=\()" % name, symbol, code)
        for name, _ in names:
            if name not in self.preserve_names:
                symbol = self.symbols[name]
                code = re.sub(r"(?<=[^\w])(%s)(?=[^\w])" % name, symbol, code)
        return code



class SnippetProgram(gloo.Program):
    def __init__(self, vertex, fragment, *args, **kwargs):
        if isinstance(vertex, Snippet):
            self.vertex_snippet = vertex
        else:
            self.vertex_snippet = Snippet(vertex)
        if isinstance(fragment, gloo.Snippet):
            self.fragment_snippet = fragment
        else:
            self.fragment_snippet = Snippet(fragment)

        vertex_code = self.finalize_snippet(self.vertex_snippet)
        self.list_shader('vertex:', vertex_code)
        fragment_code = self.finalize_snippet(self.fragment_snippet)
        self.list_shader('fragment:', fragment_code)
        super().__init__(
            vertex=vertex_code,
            fragment=fragment_code,
            *args, **kwargs
        )

    @staticmethod
    def list_shader(name, code):
        print(name)
        for line in code.split('\n'):
            print(line)
            
    @staticmethod
    def finalize_snippet(snippet):
        return snippet.code + '''
        void main()
        {{
            {call};
        }}
        '''.format(call=snippet.call)

    def mangle_key(self, key):
        for snippet in [
            self.vertex_snippet,
            *self.vertex_snippet.dependencies,
            self.fragment_snippet,
            *self.fragment_snippet.dependencies,
        ]:
            try:
                return snippet.symbols[key]
            except KeyError:
                continue
        
    def __getitem__(self, key):
        return super().__getitem__(self.mangle_key(key))
        
    def __setitem__(self, key, item):
        return super().__setitem__(self.mangle_key(key), item)
            

class Shader(OpenGLProcessor):
    def __init__(self,
                 vertex, fragment,
                 vertex_count, attributes, uniforms,
                 *args, **kwargs):
        self.program = SnippetProgram(
            vertex=vertex, fragment=fragment,
            *args, **kwargs
        )
        
        self.uniforms = {
            name: process_param(param)
            for name, param in uniforms.items()
        }
        self.attributes = {}
        attr_shapes = []
        for name, (count, param) in attributes.items():
            attr_shapes.append((
                self.program.mangle_key(name),
                np.float32, count
            ))
            self.attributes[name] = process_param(param)

        self.vertex_count = vertex_count
        self.vertex_buffers = np.zeros(
            self.vertex_count, attr_shapes
        ).view(gloo.VertexBuffer)
        
    def __call__(self, surface, t):
        self.load_buffers(t)
        self.draw(t)

    def load_buffers(self, t):
        for name, func in self.attributes.items():
            key = self.program.mangle_key(name)
            self.vertex_buffers[key] = self.as_vertex_buffer(
                func(t),
                self.vertex_buffers[key].shape[-1]
            )
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
