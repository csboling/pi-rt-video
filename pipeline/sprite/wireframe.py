from abc import ABCMeta, abstractmethod

import numpy as np
from meshpy.tet import MeshInfo, build
from meshpy.geometry import (
    EXT_OPEN,
    generate_surface_of_revolution,
    GeometryBuilder,
)
import pygame

from pipeline.sprite.Sprite import Sprite


class Wireframe(metaclass=ABCMeta):

    @staticmethod
    def adj_to_edges(left, right):
        return np.stack((left, right)).reshape(2, 3, -1).transpose((2, 0, 1))

    # @abstractmethod
    # def vertex_map(self, t):
    #     pass

    # @abstractmethod
    # def uv_map(self, t):
    #     pass

    def gl_draw(self, GL, vertices, uv_map):
        GL.glBegin(GL.GL_QUADS)
        for vertex, uv in zip(vertices, uv_map):
            GL.glTexCoord2f(*uv)
            GL.glVertex3fv(vertex)
        GL.glEnd()


class Projection2DMesh(Sprite):
    def __init__(self, wireframe, vertex_color, edge_color):
        self.wireframe = wireframe
        self.vertex_color = vertex_color
        self.edge_color = edge_color

    def draw(self, surface, pos, t):
        center = np.array(pos)
        vertices, edges = self.wireframe.mesh(t)

        if self.edge_color is not ():
            for edge in edges:
                pygame.draw.aaline(
                    surface, self.edge_color, 
                    (edge[0, :2] + center).astype(int),
                    (edge[1, :2] + center).astype(int)
                )
        if self.vertex_color is not ():
            for vertex in vertices.reshape((3, -1)).T:
                pygame.draw.circle(
                    surface, self.vertex_color,
                    (vertex[:2] + center).astype(int),
                    3
                )


class TextureMap(Sprite):
    def __init__(self, wireframe, texture):
        self.wireframe = wireframe
        self.texture = texture

    def draw(self, frame, pos, t):
        center = np.array(pos)
        vertices, edges = self.wireframe.mesh(t)

        w, h = vertices.shape[1:]
        texture = self.texture((w, h), t)
        u, v = self.wireframe.uv_map()
        uv_coords = np.stack(((w-1)*u, (h-1)*v)).astype(int)
        mapped = texture[
            uv_coords[1, ...], 
            uv_coords[0, ...],
            :
        ]
        positions = (
            center + vertices[:2, ...].transpose(1, 2, 0)
        ).astype(int)
        bounds = np.stack((
            positions[1:, 1:, :],
            positions[:-1, :-1, :],
        ), axis=-1)
        for i in range(w-1):
            for j in range(h-1):
                xs, ys = bounds[j, i, :, :]
                x_start, x_stop = xs
                y_start, y_stop = ys
                frame[y_start:y_stop, x_start:x_stop, :] = mapped[j, i, :]


class FixedMaterialWireframe(Wireframe):
    def __init__(self, grid):
        self._vertices, self._uv, _ = np.dsplit(grid, [3, 5])

    def vertex_map(self, t):
        return self._vertices

    def uv_map(self, t):
        return self._uv


class SquareWireframe(Wireframe):
    def __init__(self, width=1., height=1., center=(0., 0., 0.)):
        x, y, z = center
        self._quads = np.array([
            [
                [x - height / 2, y - width / 2, z],
                [x - height / 2, y + width / 2, z],
                [x + height / 2, y + width / 2, z],
                [x + height / 2, y - width / 2, z],
            ],
        ])
        self._uv = np.array([
            [
                [0, 0],
                [0, 1],
                [1, 1],
                [1, 0],
            ],
        ])

    def quads(self, t):
        return self._quads

    def uv(self, t):
        return self._uv


class CubeWireframe(Wireframe):
    def __init__(self, width=1., height=1., depth=1., center=(0., 0., 0.)):
        x, y, z = center
        self._quads = np.array([
            [
                # back 
                [x + width / 2, y - height / 2, z - depth / 2],
                [x + width / 2, y + height / 2, z - depth / 2],
                [x - width / 2, y + height / 2, z - depth / 2],
                [x - width / 2, y - height / 2, z - depth / 2],
            ],
            [
                # front
                [x + width / 2, y - height / 2, z + depth / 2],
                [x + width / 2, y + height / 2, z + depth / 2],
                [x - width / 2, y + height / 2, z + depth / 2],
                [x - width / 2, y - height / 2, z + depth / 2],
            ],
            [
                # left
                [x - width / 2, y - height / 2, z - depth / 2],
                [x - width / 2, y + height / 2, z - depth / 2],
                [x - width / 2, y + height / 2, z + depth / 2],
                [x - width / 2, y - height / 2, z + depth / 2],
            ],
            [
                #right
                [x + width / 2, y - height / 2, z + depth / 2],
                [x + width / 2, y + height / 2, z + depth / 2],
                [x + width / 2, y + height / 2, z - depth / 2],
                [x + width / 2, y - height / 2, z - depth / 2],
            ],
            [
                #top
                [x - width / 2, y + height / 2, z + depth / 2],
                [x - width / 2, y + height / 2, z - depth / 2],
                [x + width / 2, y + height / 2, z - depth / 2],
                [x + width / 2, y + height / 2, z + depth / 2],
            ],
            [
                #bottom
                [x - width / 2, y - height / 2, z - depth / 2],
                [x - width / 2, y - height / 2, z + depth / 2],
                [x + width / 2, y - height / 2, z + depth / 2],
                [x + width / 2, y - height / 2, z - depth / 2],
            ],
        ])

        self._uv = np.array([
            [
                [0, 0],
                [0, 1],
                [1, 1],
                [1, 0],
            ]
        ]*6)

    def quads(self, t):
        return self._quads

    def uv(self, t):
        return self._uv
                

        # back   = SquareWireframe(width, height, z=-depth / 2)
        # front  = SquareWireframe(width, height, z= depth / 2)
        # bottom = SquareWireframe(width, height, z= depth / 2)
        
        

class SphereWireframe(Wireframe):
    def __init__(self, r, density):
        self.radius = r
        self.density = density

        phi = np.linspace(0, np.pi, self.density)
        rz = np.stack((
            self.radius*np.sin(phi),
            self.radius*np.cos(phi),   
        ), axis=-1)

        geob = GeometryBuilder()
        geob.add_geometry(
            *generate_surface_of_revolution(
                rz,
                closure=EXT_OPEN,
                radial_subdiv=self.density
            )
        )
        mesh_info = MeshInfo()
        geob.set(mesh_info)
        self.mesh = build(mesh_info)
        self._quads = np.array([
            [self.mesh.points[ix] for ix in element]
            for element in self.mesh.elements
        ])
        self._uv = self.calculate_uv(
            self._quads.reshape((-1, 3))
        ).reshape((-1, 4, 2))

    def calculate_uv(self, points):
        d = (-points.T / np.linalg.norm(points, axis=-1)).T
        return np.stack((
            0.5 + d[:, 1]*0.5,
            0.5 + np.arctan2(d[:, 0], d[:, 2]) / (2*np.pi),
        ), axis=-1)

    def quads(self, t):
        return self._quads

    def uv(self, t):
        return self._uv
    

# class WireframeProcessor(Wireframe):
#     def __call__(self, wireframe):
#         self.wireframe = wireframe 
#         return self

#     def (self, t):
#         return self.apply(self.wireframe, t)

#     def uv_map(self):
#         return self.wireframe.uv_map()


class Rotate3D(Wireframe):

    def __init__(self, func):
        self.func = func
        
    def __call__(self, wireframe):
        self.source = wireframe
        return self

    # def apply(self, w, t):
    #     vertices = w.vertex_map(t)
    #     uv = w.uv_map(t)
    #     angle = self.func(t)
    #     return self.rotate(vertices, edges, angle)
 
    def quads(self, t):
        R = self.rotation_matrix(self.func(t))
        return np.einsum('ij,klj->kli', R, self.source.quads(t))

    def uv(self, t):
        R = self.rotation_matrix(self.func(t))
        return np.einsum('ij,klj->kli', R[:2, :2], self.source.uv(t))

    @classmethod
    def rotation_matrix(cls, angle):
        alpha, beta, gamma = angle
        return cls.rotate_z(gamma).dot(
            cls.rotate_y(beta)
        ).dot(
            cls.rotate_x(alpha)
        )
            
    @staticmethod
    def rotate_x(theta):
        return np.array([
            [1, 0, 0],
            [0, np.cos(theta), -np.sin(theta)],
            [0, np.sin(theta), np.cos(theta)],
        ])

    @staticmethod
    def rotate_y(theta):
        return np.array([
            [np.cos(theta), 0, np.sin(theta)],
            [0, 1, 0],
            [-np.sin(theta), 0, np.cos(theta)],
        ])

    @staticmethod
    def rotate_z(theta):
        return np.array([
            [np.cos(theta), -np.sin(theta), 0],
            [np.sin(theta), np.cos(theta), 0],
            [0, 0, 1],
        ])
