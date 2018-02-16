from abc import ABCMeta, abstractmethod

import numpy as np
import pygmsh


class Mesh(metaclass=ABCMeta):

    @property
    @abstractmethod
    def points(self):
        pass

    @property
    @abstractmethod
    def faces(self):
        pass

    @property
    @abstractmethod
    def edges(self):
        pass


class BoxMesh(Mesh):
    def __init__(self, width=1., height=1., depth=1.):
        self._points = np.array([
            [ width / 2, height / 2, depth / 2],
            [-width / 2, height / 2, depth / 2],
            [-width / 2,-height / 2, depth / 2],
            [ width / 2,-height / 2, depth / 2],

            [ width / 2,-height / 2,-depth / 2],
            [ width / 2, height / 2,-depth / 2],
            [-width / 2, height / 2,-depth / 2],
            [-width / 2,-height / 2,-depth / 2],
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
            0,1,2, 0,2,3,  0,3,4, 0,4,5,  0,5,6, 0,6,1,
            1,6,7, 1,7,2,  7,4,3, 7,3,2,  4,7,6, 4,6,5
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
