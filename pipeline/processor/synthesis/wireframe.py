import numpy as np
import pygame

from pipeline.processor.Processor import Processor


class ProjectWireframe(Processor):
    def __init__(self, wireframe, vertex_color, edge_color):
        self.wireframe = wireframe
        self.vertex_color = vertex_color
        self.edge_color = edge_color

    def iterate(self):
        for surface in self.source:
            w, h = self.resolution
            center = np.array([w / 2, h / 2])
            for edge in self.wireframe.edges:
                pygame.draw.aaline(
                    surface, self.edge_color, 
                    (edge[0, :2] + center).astype(int),
                    (edge[1, :2] + center).astype(int)
                )
            for vertex in self.wireframe.vertices.reshape(3, -1).T:
                pygame.draw.circle(
                    surface, self.vertex_color,
                    (vertex[:2] + center).astype(int),
                    3
                )
            yield surface


class Wireframe:
    @staticmethod
    def adj_to_edges(left, right):
        return np.stack((left, right)).reshape(2, 3, -1).transpose((2, 0, 1))


class Square(Wireframe):
    def __init__(self, length, points):
        xs, ys = np.meshgrid(
            np.linspace(-length / 2, length / 2, points),
            np.linspace(-length / 2, length / 2, points)
        )
        self.vertices = np.stack((xs, ys, np.zeros(xs.shape)))
        self.edges = np.concatenate((
            self.adj_to_edges(
                self.vertices[:, :-1, :], 
                self.vertices[:, 1:, :]
            ),
            self.adj_to_edges(
                self.vertices[:, :, :-1], 
                self.vertices[:, :, 1:]
            )
        ))
