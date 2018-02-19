from abc import ABCMeta, abstractmethod
import itertools

import meshzoo
import numpy as np
import pygmsh


class Mesh(metaclass=ABCMeta):

    def __init__(self, points=None, faces=None, texcoord=None):
        self._points = points
        self._faces = faces
        self._texcoord = texcoord
    
    @property
    def points(self):
        if self._points is not None:
            return self._points
        else:
            raise NotImplementedError

    @property
    def faces(self):
        if self._faces is not None:
            return self._faces
        else:
            raise NotImplementedError
        
    @property
    def texcoord(self):
        if self._texcoord is not None:
            return self._texcoord
        else:
            raise NotImplementedError

        
class BoxMesh(Mesh):
    def __init__(self, width=1., height=None, depth=None):
        if height is None:
            height = width
        if depth is None:
            depth = width

        positions = np.array([
            [ width,  height,  depth],
            [-width,  height,  depth],
            [-width, -height,  depth],
            [ width, -height,  depth],

            [ width, -height, -depth],
            [ width,  height, -depth],
            [-width,  height, -depth],
            [-width, -height, -depth],
        ]) / 2
        face_indices = [
            0, 1, 2, 3,
            0, 3, 4, 5,
            0, 5, 6, 1,

            1, 6, 7, 2,
            7, 4, 3, 2,
            4, 7, 6, 5,
        ]
        texture_coords = np.array([
            [0, 0],
            [0, 1],
            [1, 1],
            [1, 0],
        ])
        texture_indices = [
            0, 1, 2, 3,
            0, 1, 2, 3,
            0, 1, 2, 3,
            
            3, 2, 1, 0,
            0, 1, 2, 3,
            0, 1, 2, 3,
        ]
        filled = np.resize(
            np.array([0, 1, 2, 0, 2, 3], dtype=np.uint32),
            6 * (2 * 3)
        )
        filled += np.repeat(4 * np.arange(6, dtype=np.uint32), 6)
        
        super().__init__(
            points=positions[face_indices],
            faces=filled,# [
            #     0,1,2, 0,2,3,
            #     0,3,4, 0,4,5,
            #     0,5,6, 0,6,1,

            #     1,6,7, 1,7,2,
            #     7,4,3, 7,3,2,
            #     4,7,6, 4,6,5,
            # ],
            texcoord=texture_coords[texture_indices]
        )

    
class MoebiusMesh(Mesh):
    def __init__(self, *args, **kwargs):
        self._points, self._faces = meshzoo.moebius(*args, **kwargs)


class IcosphereMesh(Mesh):
    def __init__(self, *args, **kwargs):
        points, faces = meshzoo.iso_sphere(*args, **kwargs)
        self._points = points
        self._faces = faces
