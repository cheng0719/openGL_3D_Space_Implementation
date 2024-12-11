import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import pygame.freetype  # for 文字顯示
import random

# Initialize the OpenGL environment
def init():
    glClearColor(0.0, 0.5, 0.5, 1.0)  # set the background color to light blue
    glEnable(GL_DEPTH_TEST)           # enable depth testing
    glDepthFunc(GL_LEQUAL)            # set the depth function to less than or equal
    glPointSize(2)                    # set the point size to 2 pixels
    
    # Set the projection matrix
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(70, (800/600), 0.1, 15.0)  # set the perspective projection parameters
    glMatrixMode(GL_MODELVIEW)

# Draw the grid lines of the 3D space
def draw_grid():
    glColor3f(0.5, 0.5, 0.5)  # set the grid line color to gray
    glBegin(GL_LINES)
    
    grid_size = 3  # define the size of the grid
    step = 1.0     # define the step size between grid lines

    for idx in range(grid_size):
        for z in range(0, grid_size + 1):
            glVertex3f(0, idx, z)
            glVertex3f(grid_size, idx, z)

        for z in range(0, grid_size + 1):
            glVertex3f(idx, 0, z)
            glVertex3f(idx, grid_size, z)

        for x in range(0, grid_size + 1):
            glVertex3f(x, idx, 0)
            glVertex3f(x, idx, grid_size)

        for x in range(0, grid_size + 1):
            glVertex3f(x, 0, idx)
            glVertex3f(x, grid_size, idx)

        for y in range(0, grid_size + 1):
            glVertex3f(idx, y, 0)
            glVertex3f(idx, y, grid_size)

        for y in range(0, grid_size + 1):
            glVertex3f(0, y, idx)
            glVertex3f(grid_size, y, idx)

    
    
    glEnd()
    
    # Draw the X axis (red)
    glColor3f(1.0, 0.0, 0.0)
    glBegin(GL_LINES)
    glVertex3f(0, 0, 0)
    glVertex3f(grid_size, 0, 0)
    glEnd()
    
    # Draw the Z axis (blue)
    glColor3f(0.0, 0.0, 1.0)
    glBegin(GL_LINES)
    glVertex3f(0, 0, 0)
    glVertex3f(0, 0, grid_size)
    glEnd()

    # Draw the Y axis (green)
    glColor3f(0.0, 1.0, 0.0)
    glBegin(GL_LINES)
    glVertex3f(0, 0, 0)
    glVertex3f(0, grid_size, 0)
    glEnd()

# Draw text at the specified position
def draw_text(position, text_string, font_size=24):
    font = pygame.freetype.SysFont('Arial', font_size)  # set the font
    # Render the text to a surface
    text_surface, rect = font.render(text_string, (255, 255, 255, 255), bgcolor=(0, 128, 128))
    text_data = pygame.image.tostring(text_surface, "RGBA", True)
    width, height = text_surface.get_size()

    # Draw the text on the screen at the specified position
    glRasterPos3f(*position)
    glDrawPixels(width, height, GL_RGBA, GL_UNSIGNED_BYTE, text_data)

# Generate random points in the 3D space
def generate_random_points(num_points=50):
    points = []
    for _ in range(num_points):
        x = random.uniform(0.0, 3.0)
        y = random.uniform(0.0, 3.0)
        z = random.uniform(0.0, 3.0)
        points.append((x, y, z))
    return points

# Render the 3D scene with the specified points
def render_scene(points):
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)  # clear the color and depth buffers
    glLoadIdentity()

    # Set the camera position and orientation
    global angle_x, angle_y
    gluLookAt(0, 5, 0,    # set the camera position at (0, 5, 0)
              0, 0, 1,    # set the camera target at (0, 0, 1)
              0, 1, 0)    # set the up vector to (0, 1, 0)
    glRotatef(angle_x, 1, 0, 0)  # rotate up and down
    glRotatef(angle_y, 0, 1, 0)  # rotate left and right

    # Draw the grid lines of the 3D space
    draw_grid()

    # Draw the axis labels
    draw_text((3.5, 0, 0), "X")  # display "X" at the end of the X axis
    draw_text((0, 0, 3.5), "Z")  # display "Z" at the end of the Z axis
    draw_text((0, 3.5, 0), "Y")  # display "Y" at the end of the Y axis

    # Draw the axis labels for the grid lines
    for i in range(0, 4):
        if i != 0:  
            draw_text((i, 0, 0), str(i)) 
            draw_text((0, 0, i), str(i))  
            draw_text((0, i, 0), str(i))  
    
    # Draw the points
    glBegin(GL_POINTS)
    glColor3f(1.0, 1.0, 1.0)  # set the point color to white
    for point in points:
        glVertex3f(*point)
    glEnd()
    
    glFlush()  # flush the OpenGL pipeline

def main():
    global angle_x, angle_y
    angle_x, angle_y = 0, 0  # initialize the rotation angles

    # Initialize the Pygame environment
    pygame.init()
    pygame.freetype.init()  # initialize the font module
    screen_size = (800, 600)
    screen = pygame.display.set_mode(screen_size, DOUBLEBUF | OPENGL)
    pygame.display.set_caption("3D Interactive Display with Axis Labels")
    init()

    # Generate random points
    points = generate_random_points()  # TODO: replace this with actual coordinates if you want to display a "static" scene

    # Main loop
    running = True
    last_mouse_pos = None
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            elif event.type == MOUSEMOTION:
                if pygame.mouse.get_pressed()[0]:  # check if the left mouse button is pressed
                    if last_mouse_pos:
                        dx, dy = event.pos[0] - last_mouse_pos[0], event.pos[1] - last_mouse_pos[1]
                        angle_x += dy * 0.5  # adjust the up and down rotation angle
                        angle_y += dx * 0.5  # adjust the left and right rotation angle
                    last_mouse_pos = event.pos
                else:
                    last_mouse_pos = None
        
        # points = generate_random_points()  # TODO: replace this with actual coordinates if you want to display a "dynamic" scene
        render_scene(points)
        pygame.display.flip()  # update the display
    
    pygame.quit()

main()
