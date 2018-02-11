import numpy as np
import pygame

from pipeline.sprite.Sprite import Sprite


class Wireframe(Sprite):
    def __init__(self, vertex_color, edge_color):
        self.vertex_color = vertex_color
        self.edge_color = edge_color

    @staticmethod
    def adj_to_edges(left, right):
        return np.stack((left, right)).reshape(2, 3, -1).transpose((2, 0, 1))

    def draw(self, surface, pos, t):
        center = np.array(pos)
        vertices, edges = self.render(t)
        for edge in edges:
            pygame.draw.aaline(
                surface, self.edge_color, 
                (edge[0, :2] + center).astype(int),
                (edge[1, :2] + center).astype(int)
            )
        for vertex in vertices:
            pygame.draw.circle(
                surface, self.vertex_color,
                (vertex[:2] + center).astype(int),
                3
            )


class ConstantWireframe(Wireframe):
    
    def render(self, t):
        return self.vertices, self.edges


class SquareWireframe(ConstantWireframe):
    def __init__(self, length, points, *args, **kwargs):
        super().__init__(*args, **kwargs)
        xs, ys = np.meshgrid(
            np.linspace(-length / 2, length / 2, points),
            np.linspace(-length / 2, length / 2, points)
        )
        grid_vertices = np.stack((xs, ys, np.zeros(xs.shape)))
        self.vertices = grid_vertices.reshape(3, -1).T
        self.edges = np.concatenate((
            self.adj_to_edges(
                grid_vertices[:, :-1, :], 
                grid_vertices[:, 1:, :]
            ),
            self.adj_to_edges(
                grid_vertices[:, :, :-1], 
                grid_vertices[:, :, 1:]
            )
        ))
        

class WireframeProcessor(Wireframe):
    def __call__(self, wireframe):
        self.wireframe = wireframe 
        return self

    @property
    def vertex_color(self):
        return self.wireframe.vertex_color

    @property
    def edge_color(self):
        return self.wireframe.edge_color

    def render(self, t):
        return self.apply(self.wireframe, t)


class Rotate3D(WireframeProcessor):

    def __init__(self, func):
        self.func = func
        
    def apply(self, w, t):
        vertices, edges = w.render(t)
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
        rotated_vertices = np.einsum('ij,kj->ki', R, vertices)
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

