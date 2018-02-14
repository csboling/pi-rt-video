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

    def __init__(self, mesh):
        self.mesh = mesh


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


class RectWireframe(Wireframe):
    def __init__(self, width=1., height=1.):
        mesh_info = MeshInfo()
        mesh_info.set_points([
            [-height / 2, -width / 2, z],
            [-height / 2, +width / 2, z],
            [+height / 2, +width / 2, z],
            [+height / 2, -width / 2, z],
        ])
        super().__init__(build(mesh_info))
        

class BoxWireframe(Wireframe):
    def __init__(self, width=1., height=1., depth=1.):
        mesh_info = MeshInfo()
        mesh_info.set_points([
            [-width / 2, -height / 2, -depth / 2],            
            [ width / 2, -height / 2, -depth / 2],
            [ width / 2,  height / 2, -depth / 2],
            [-width / 2,  height / 2, -depth / 2],

            [-width / 2, -height / 2,  depth / 2],
            [ width / 2, -height / 2,  depth / 2],
            [ width / 2,  height / 2,  depth / 2],
            [-width / 2,  height / 2,  depth / 2],
        ])
        mesh_info.set_facets([
            [0, 1, 2, 3],
            [4, 5, 6, 7],
            [0, 4, 5, 1],
            [1, 5, 6, 2],
            [2, 6, 7, 3],
            [3, 7, 4, 0],
        ])
        super().__init__(build(mesh_info))

        
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
        super().__init__(build(mesh_info))
        self.uv = self.calculate_uv(self.verts)

    def calculate_uv(self, points):
        d = (-points.T / np.linalg.norm(points, axis=-1)).T
        return np.stack((
            0.5 + d[:, 1]*0.5,
            0.5 + np.arctan2(d[:, 0], d[:, 2]) / (2*np.pi),
        ), axis=-1)
