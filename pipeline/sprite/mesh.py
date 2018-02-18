from abc import ABCMeta, abstractmethod

import numpy as np
import pygmsh


class Mesh(metaclass=ABCMeta):

    def __init__(self, points=None, edges=None, faces=None):
        self._points = points
        self._edges = edges
        self._faces = faces
    
    @property
    def points(self):
        if self._points is not None:
            return self._points
        else:
            raise NotImplementedError

    @property
    def edges(self):
        if self._edges is not None:
            return self._edges
        else:
            raise NotImplementedError

    @property
    def faces(self):
        if self._faces is not None:
            return self._faces
        else:
            raise NotImplementedError


class BoxMesh(Mesh):
    def __init__(self, width=1., height=None, depth=None):
        if height is None:
            height = width
        if depth is None:
            depth = width
        self._points = np.array([
            [ width,  height,  depth],
            [-width,  height,  depth],
            [-width, -height,  depth],
            [ width, -height,  depth],

            [ width, -height, -depth],
            [ width,  height, -depth],
            [-width,  height, -depth],
            [-width, -height, -depth],
        ]) / 2
        self._edges = [
            [0, 1, 2, 3, 0],
            [4, 5, 6, 7, 4],
            [0, 5],
            [1, 6],
            [2, 7],
            [3, 4],
        ]
            
        self._faces = np.array([
            0,1,2, 0,2,3,
            0,3,4, 0,4,5,
            0,5,6, 0,6,1,
            
            1,6,7, 1,7,2,
            7,4,3, 7,3,2,
            4,7,6, 4,6,5,
        ])

    @property
    def points(self):
        return self._points

    @property
    def faces(self):
        return self._faces
    
    @property
    def edges(self):
        return self._edges

    
class DenseRectangleMesh(Mesh):
    def __init__(self):
        self.geom = pygmsh.built_in.Geometry()

        self.geom.add_rectangle(
            0., 1.,
            0., 1.,
            0., 0.1
        )
        ref = 1.0
        self._points, self._cells, _, _, _ = pygmsh.generate_mesh(self.geom)

    @property
    def points(self):
        return self._points

    @property
    def faces(self):
        return self._cells['triangle']

    @property
    def edges(self):
        return self._cells['line']


class SphereMesh(Mesh):
    def __init__(self, radius=1., density=12):
        self.radius = radius
        self.density = density

        theta, phi = np.meshgrid(
            np.linspace(-np.pi, np.pi, self.density),
            np.linspace(-np.pi, np.pi, self.density) / 2,
        )
        self._points = np.stack(
            (
                np.sin(theta) * np.cos(phi),
                np.sin(theta) * np.sin(phi),
                np.cos(theta),
            ),
            axis=-1
        ).reshape((-1, 3))
        self._edges = [
            [
                (k*self.density + i, k*self.density + i+1)
                for i in range(self.density)
            ] + [(k*(self.density) - 1, k*self.density)]
            for k in range(self.density)
        ]
        self._faces = []
