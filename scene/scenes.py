import sys

import pygame
from pygame.locals import DOUBLEBUF, OPENGL
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np


class Point:
    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y

class Scene:
    def __init__(self, title: str, width: int, height: int, max_fps: int) -> None:
        self.title = title
        self.max_fps = max_fps
        self.screen_width = width
        self.screen_height = height
        pygame.init()
        self.display = pygame.display.set_mode(
            (width, height),
            DOUBLEBUF | OPENGL
        )
        self.clock = pygame.time.Clock()

    def run(self) -> None:
        self.setup()
        while True:
            self.events = pygame.event.get()
            for event in self.events:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            self.delta_time = self.clock.tick(self.max_fps)/1000
            self.get_inputs()
            self.update()
            self.render()

            pygame.display.flip()
            pygame.display.set_caption(
                f"{self.title} ({self.clock.get_fps():.2f} fps)"
            )
    
    def setup(self) -> None:
        GLUtils.init_ortho(-1, 1, 1, -1)

    def get_inputs(self) -> None:
        pass

    def update(self) -> None:
        pass

    def render(self) -> None:
        GLUtils.prepare_render()


class GLUtils:
    @staticmethod
    def init_ortho(left: int, right: int, top: int, bottom: int) -> None:
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluOrtho2D(left, right, top, bottom)

    @staticmethod
    def prepare_render() -> None:
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

    @staticmethod
    def draw_point(x: int, y: int, size: int) -> None:
        glPointSize(size)
        glBegin(GL_POINTS)
        glVertex2f(x, y)
        glEnd()

    @staticmethod
    def draw_graph() -> None:
        glPointSize(2)
        glBegin(GL_POINTS)
        for px in np.arange(0, 15, 0.025):
            glColor3f(0, 0, 255)
            glVertex2f(px, np.sin(px))
            glColor3f(0, 255, 0)
            glVertex2f(px, np.cos(px))
        glEnd()

    @staticmethod
    def draw_points(points: list) -> None:
        glPointSize(5)
        glBegin(GL_POINTS)
        for point in points:
            glVertex2f(point.x, point.y)
        glEnd()

    @staticmethod
    def draw_lines(points: list) -> None:
        glPointSize(1)
        glBegin(GL_LINE_STRIP)
        for point in points:
            glVertex2f(point.x, point.y)
        glEnd()

class GLScene(Scene):
    def setup(self) -> None:
        GLUtils.init_ortho(0, 15, -1.5, 1.5)

    def render(self) -> None:
        GLUtils.prepare_render()

class DrawingScene(Scene):
    def __init__(self, title: str, width: int, height: int, max_fps: int) -> None:
        super().__init__(title, width, height, max_fps)
        self.points = []

    def get_inputs(self) -> None:
        for event in self.events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                print("Mouse clickled")
                x, y = pygame.mouse.get_pos()
                self.points.append(Point(
                    2*(x - self.screen_width/2)/self.screen_width,
                    2*(y - self.screen_height/2)/self.screen_height
                ))

    def render(self) -> None:
        super().render()
        GLUtils.draw_points(self.points)
        GLUtils.draw_lines(self.points)

if __name__ == '__main__':
    scene = DrawingScene("OpenGL", 900, 600, 20)
    scene.run()
