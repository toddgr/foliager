from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

def display():
    glClear(GL_COLOR_BUFFER_BIT)
    glBegin(GL_TRIANGLES)
    glVertex2f(-1.0, -1.0)
    glVertex2f(1.0, -1.0)
    glVertex2f(0.0, 1.0)
    glEnd()
    glFlush()

def main():
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB)
    glutInitWindowSize(400, 400)
    glutInitWindowPosition(100, 100)
    glutCreateWindow(b"OpenGL in Python")
    glClearColor(0.0, 0.0, 0.0, 0.0)
    glMatrixMode(GL_PROJECTION)
    gluOrtho2D(-2.0, 2.0, -2.0, 2.0)
    glMatrixMode(GL_MODELVIEW)
    glutDisplayFunc(display)
    glutMainLoop()

if __name__ == "__main__":
    main()
