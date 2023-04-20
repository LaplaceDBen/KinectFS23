import pygame
from OpenGL.GL import *
from OpenGL.GLU import *

def draw_grass():
    glBegin(GL_QUADS)
    glColor3f(0.0, 1.0, 0.0)
    glVertex3f(-1.0, 0.0, -1.0)
    glVertex3f(-1.0, 0.0, 1.0)
    glVertex3f(1.0, 0.0, 1.0)
    glVertex3f(1.0, 0.0, -1.0)
    glEnd()

def draw_house(x, y):
    glPushMatrix()
    glTranslatef(x, 0.0, y)
    glBegin(GL_QUADS)
    glColor3f(1.0, 0.0, 0.0)
    glVertex3f(-0.5, 0.0, -0.5)
    glVertex3f(-0.5, 0.5, -0.5)
    glVertex3f(0.5, 0.5, -0.5)
    glVertex3f(0.5, 0.0, -0.5)
    glEnd()
    glPopMatrix()

def main():
    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, pygame.DOUBLEBUF | pygame.OPENGL)

    gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)
    glTranslatef(0.0, -0.5, -5)

    house_positions = [(0.0, 0.0), (1.0, 1.0)]

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        draw_grass()

        for i, (x, y) in enumerate(house_positions):
            draw_house(x, y)

        pygame.display.flip()

if __name__ == "__main__":
    main()
