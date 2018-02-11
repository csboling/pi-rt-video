from abc import ABCMeta, abstractmethod

import numpy as np
import pygame

from pipeline.sprite.Sprite import Sprite


class Wireframe(metaclass=ABCMeta):

    @staticmethod
    def adj_to_edges(left, right):
        return np.stack((left, right)).reshape(2, 3, -1).transpose((2, 0, 1))

    @abstractmethod
    def vertex_map(self, t):
        pass

    @abstractmethod
    def uv_map(self, t):
        pass

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


class SquareWireframe(FixedMaterialWireframe):
    def __init__(self, width=1., height=1.):
        super().__init__(
            np.array([
                [
                    [
                        -height / 2, -width / 2, 0,
                        0, 0,
                    ],
                    [
                        -height / 2,  width / 2, 0,
                        0, 1,
                    ]
                ],
                [
                    [
                        height / 2,  width / 2, 0,
                        1, 1,
                    ],
                    [
                        height / 2, -width / 2, 0,
                        1, 0,
                    ],
                ],
            ])
        )
        

class SphereWireframe(FixedMaterialWireframe):
    def __init__(self, r, density):
        self.radius = r
        self.density = density
        
        theta, phi = np.meshgrid(
            np.linspace(-np.pi, np.pi, self.density),
            np.linspace(-np.pi/2, np.pi/2, self.density),
        )
        super().__init__(
            np.stack(
                (
                    np.sin(theta)*np.cos(phi),
                    np.sin(theta)*np.sin(phi),
                    np.cos(theta),
                    phi / 2*np.pi,
                    1 - theta / np.pi,
                ), 
                axis=-1
            )
        )

    def gl_draw(self, GL, vertices, uv_map):
        GL.glBegin(GL.GL_QUAD_STRIP)
        for vertex, uv in zip(vertices, uv_map):
            GL.glNormal3fv(vertex)
            GL.glTexCoord2f(*uv)
            GL.glVertex3fv(self.radius * vertex)
        GL.glEnd()
    

class WireframeProcessor(Wireframe):
    def __call__(self, wireframe):
        self.wireframe = wireframe 
        return self

    def mesh(self, t):
        return self.apply(self.wireframe, t)

    def uv_map(self):
        return self.wireframe.uv_map()


class Rotate3D(WireframeProcessor):

    def __init__(self, func):
        self.func = func
        
    def apply(self, w, t):
        vertices, edges = w.mesh(t)
        angle = self.func(t)
        return self.rotate(vertices, edges, angle)

    @classmethod
    def rotate(cls, vertices, edges, angle):
        alpha, beta, gamma = angle
        R = cls.rotate_z(gamma).dot(
            cls.rotate_y(beta)
        ).dot(
            cls.rotate_x(alpha)
        )
        rotated_vertices = np.einsum('ij,jkl->ikl', R, vertices)
        rotated_edges = np.einsum('ij,klj->kli', R, edges)
        return (rotated_vertices, rotated_edges)
            
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
