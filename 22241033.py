#task1
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random
import math

# Screen size
WIDTH = 920
HEIGHT = 640

# Day/Night
IS_DAY = True
SKY_COLOR = [0.9, 0.7, 0.8]
DAY_COLOR = (0.9, 0.7, 0.8)
NIGHT_COLOR = (0.0, 0.1, 0.2)

# Colors
GRASS_COLOR = (0.1, 0.3, 0.1)
HOUSE_COLOR = (0.2, 0.2, 0.3)
ROOF_COLOR = (0.1, 0.1, 0.2)
DOOR_COLOR = (0.3, 0.2, 0.1)
WINDOW_COLOR = (0.4, 0.5, 0.7)
RAIN_COLOR = (0.4, 0.4, 1.0)
BLACK = (0, 0, 0)

# Rain
RAIN_COUNT = 120
RAIN_DROPS = []
RAIN_SPEED = 1
WIND_EFFECT = 0

# Creating rain drops
for i in range(RAIN_COUNT):
    x = random.randint(0, WIDTH)
    y = random.randint(0, HEIGHT)
    RAIN_DROPS.append([x, y])


def draw_point(x, y, size):
    glPointSize(size)
    glBegin(GL_POINTS)
    glVertex2f(x, y)
    glEnd()


def draw_rectangle(x1, y1, x2, y2):
    glBegin(GL_TRIANGLES)
    glVertex2f(x1, y1)
    glVertex2f(x2, y1)
    glVertex2f(x1, y2)
    glEnd()
    
    glBegin(GL_TRIANGLES)
    glVertex2f(x1, y2)
    glVertex2f(x2, y2)
    glVertex2f(x2, y1)
    glEnd()


def draw_background():
    global SKY_COLOR
    
    if IS_DAY:
        if SKY_COLOR[0] < DAY_COLOR[0]:
            SKY_COLOR[0] += 0.002
            SKY_COLOR[1] += 0.001
            SKY_COLOR[2] += 0.001
    else:
        if SKY_COLOR[0] > NIGHT_COLOR[0]:
            SKY_COLOR[0] -= 0.002
            SKY_COLOR[1] -= 0.001
            SKY_COLOR[2] -= 0.001
    
    glClearColor(SKY_COLOR[0], SKY_COLOR[1], SKY_COLOR[2], 1.0)
    glClear(GL_COLOR_BUFFER_BIT)
    glColor3f(GRASS_COLOR[0], GRASS_COLOR[1], GRASS_COLOR[2])
    for i in range(140):
        glBegin(GL_LINES)
        glVertex2f(0, i)
        glVertex2f(WIDTH, i)
        glEnd()


def draw_house():
    #body
    glColor3f(HOUSE_COLOR[0], HOUSE_COLOR[1], HOUSE_COLOR[2])
    draw_rectangle(270, 0, 650, 310)
    
    # Roof
    glColor3f(ROOF_COLOR[0], ROOF_COLOR[1], ROOF_COLOR[2])
    glBegin(GL_TRIANGLES)
    glVertex2f(220, 310)
    glVertex2f(700, 310)
    glVertex2f(WIDTH // 2, 520)
    glEnd()
    
    #Door
    glColor3f(DOOR_COLOR[0], DOOR_COLOR[1], DOOR_COLOR[2])
    draw_rectangle(405, 0, 515, 170)
    
    #Windows
    glColor3f(WINDOW_COLOR[0], WINDOW_COLOR[1], WINDOW_COLOR[2])
    draw_rectangle(310, 180, 390, 260)  #Left
    draw_rectangle(530, 180, 610, 260)  #Right


def draw_outlines():
    glColor3f(BLACK[0], BLACK[1], BLACK[2])
    glLineWidth(8)
    
    #House
    glBegin(GL_LINES)
    glVertex2f(270, 0)
    glVertex2f(650, 0)
    glVertex2f(650, 0)
    glVertex2f(650, 310)
    glVertex2f(650, 310)
    glVertex2f(270, 310)
    glVertex2f(270, 310)
    glVertex2f(270, 0)
    glEnd()
    
    # Roof
    glBegin(GL_LINE_LOOP)
    glVertex2f(220, 310)
    glVertex2f(700, 310)
    glVertex2f(WIDTH // 2, 520)
    glEnd()
    
    # Door
    glBegin(GL_LINES)
    glVertex2f(405, 0)
    glVertex2f(515, 0)
    glVertex2f(515, 0)
    glVertex2f(515, 170)
    glVertex2f(515, 170)
    glVertex2f(405, 170)
    glVertex2f(405, 170)
    glVertex2f(405, 0)
    glEnd()
    
    # Window
    glBegin(GL_LINES)
    # Left window
    glVertex2f(310, 180)
    glVertex2f(390, 180)
    glVertex2f(390, 180)
    glVertex2f(390, 260)
    glVertex2f(390, 260)
    glVertex2f(310, 260)
    glVertex2f(310, 260)
    glVertex2f(310, 180)
    glVertex2f(310, 220)
    glVertex2f(390, 220)
    
    # Right window
    glVertex2f(530, 180)
    glVertex2f(610, 180)
    glVertex2f(610, 180)
    glVertex2f(610, 260)
    glVertex2f(610, 260)
    glVertex2f(530, 260)
    glVertex2f(530, 260)
    glVertex2f(530, 180)
    glVertex2f(530, 220)
    glVertex2f(610, 220)
    glEnd()
    
    #Doorknob
    draw_point(495, 85, 8)


def draw_rain():
    glColor3f(RAIN_COLOR[0], RAIN_COLOR[1], RAIN_COLOR[2])
    glLineWidth(2)
    glBegin(GL_LINES)
    for drop in RAIN_DROPS:
        x, y = drop
        glVertex2f(x, y)
        glVertex2f(x + 10 * WIND_EFFECT, y - 10)
    glEnd()


def update_rain():
    for drop in RAIN_DROPS:
        drop[0] += WIND_EFFECT
        drop[1] -= RAIN_SPEED

        if drop[1] < 0:
            drop[1] = HEIGHT
        if drop[0] < 0:
            drop[0] = WIDTH
        if drop[0] > WIDTH:
            drop[0] = 0


def setup_projection():
    glViewport(0, 0, WIDTH, HEIGHT)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0.0, WIDTH, 0.0, HEIGHT, 0.0, 1.0)
    glMatrixMode(GL_MODELVIEW)


def special_key_listener(key, x, y):
    global WIND_EFFECT, IS_DAY
    
    if key == GLUT_KEY_RIGHT:
        WIND_EFFECT = min(WIND_EFFECT + 0.05, 0.35)
        print(f"Wind: {WIND_EFFECT}")
    elif key == GLUT_KEY_LEFT:
        WIND_EFFECT = max(WIND_EFFECT - 0.05, -0.35)
        print(f"Wind: {WIND_EFFECT}")
    elif key == GLUT_KEY_UP:
        IS_DAY = True
        print("Day time")
    elif key == GLUT_KEY_DOWN:
        IS_DAY = False
        print("Night time")
    
    glutPostRedisplay()


def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    setup_projection()
    
    draw_background()
    draw_house()
    draw_outlines()
    draw_rain()
    update_rain()
    
    glutSwapBuffers()


def main():
    glutInit()
    glutInitDisplayMode(GLUT_RGBA)
    glutInitWindowSize(WIDTH, HEIGHT)
    glutInitWindowPosition(0, 0)
    glutCreateWindow(b"Rainy House Scene")
    
    glutDisplayFunc(display)
    glutIdleFunc(display)
    glutSpecialFunc(special_key_listener)
    
    glutMainLoop()


if __name__ == "__main__":
    main()
    
    
    
    
    
    
    
#task2
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random
import time

# ===== Global Variables =====
WINDOW_WIDTH, WINDOW_HEIGHT = 800, 600
BOUNDARY_MIN_X, BOUNDARY_MIN_Y = 50, 50
BOUNDARY_MAX_X, BOUNDARY_MAX_Y = 750, 550


points = []
is_frozen = False
is_blinking = False      
blink_start_time = 0
blink_state = True


class MovingPoint:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        # Random direction
        self.dx = random.choice([-1, 1])
        self.dy = random.choice([-1, 1])
        # Random color
        self.color = (random.uniform(0.3, 1.0),random.uniform(0.3, 1.0),random.uniform(0.3, 1.0))
        self.speed = 2.0
        self.visible = True
    
    def update(self):
        if is_frozen:
            return
            
        #Move
        self.x += self.dx * self.speed
        self.y += self.dy * self.speed

        #Bounce
        if self.x <= BOUNDARY_MIN_X:
            self.x = BOUNDARY_MIN_X
            self.dx = -self.dx
        elif self.x >= BOUNDARY_MAX_X:
            self.x = BOUNDARY_MAX_X
            self.dx = -self.dx
            
        if self.y <= BOUNDARY_MIN_Y:
            self.y = BOUNDARY_MIN_Y
            self.dy = -self.dy
        elif self.y >= BOUNDARY_MAX_Y:
            self.y = BOUNDARY_MAX_Y
            self.dy = -self.dy
    
    def draw(self):
        if self.visible:
            glPointSize(8)
            glBegin(GL_POINTS)
            glColor3f(self.color[0], self.color[1], self.color[2])
            glVertex2f(self.x, self.y)
            glEnd()


def convert_coordinate(x, y):
    a = x
    b = WINDOW_HEIGHT - y
    return a, b

# ===== Draw Functions =====
def draw_point(x, y, size):
    """Draws a single point at (x, y) with given size."""
    glPointSize(size)
    glBegin(GL_POINTS)
    glVertex2f(x, y)
    glEnd()

def draw_boundary():
    glLineWidth(2)
    glBegin(GL_LINE_LOOP)
    glColor3f(1.0, 1.0, 1.0)
    glVertex2f(BOUNDARY_MIN_X, BOUNDARY_MIN_Y)
    glVertex2f(BOUNDARY_MAX_X, BOUNDARY_MIN_Y)
    glVertex2f(BOUNDARY_MAX_X, BOUNDARY_MAX_Y)
    glVertex2f(BOUNDARY_MIN_X, BOUNDARY_MAX_Y)
    glEnd()

def draw_all_points():
    for point in points:
        point.draw()

def update_blink_effect():
    global blink_state
    
    if is_blinking:
        current_time = time.time()
        # Blink every 0.5 sec
        blink_state = (int(current_time * 2) % 2) == 0
        
        for point in points:
            point.visible = blink_state
    else:
        for point in points:
            point.visible = True

def update_all_points():
    for point in points:
        point.update()

def keyboard_listener(key, x, y):
    if key == b' ':  #Spacebar
        is_frozen = not is_frozen
        if is_frozen:
            print("frozen")
        else:
            print("unfrozen")
    
    glutPostRedisplay()

def special_key_listener(key, x, y):
    if is_frozen:
        return
        
    if key == GLUT_KEY_UP:
        # Increase20%
        for point in points:
            point.speed *= 1.2
        print("Speed increased")
        
    elif key == GLUT_KEY_DOWN:
        # Decrease20%
        for point in points:
            point.speed /= 1.2
        print("Speed decreased")
    
    glutPostRedisplay()

def mouse_listener(button, state, x, y):
    if is_frozen:
        print("System frozen")
        return
        
    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        # Toggle blinking for all points
        is_blinking = not is_blinking
        if is_blinking:
            print("Blinking started")
        else:
            print("Blinking stopped")
            
    elif button == GLUT_RIGHT_BUTTON and state == GLUT_DOWN:
        gl_x, gl_y = convert_coordinate(x, y)
        
        # Check if click is inside boundary
        if (BOUNDARY_MIN_X <= gl_x <= BOUNDARY_MAX_X and 
            BOUNDARY_MIN_Y <= gl_y <= BOUNDARY_MAX_Y):
            new_point = MovingPoint(gl_x, gl_y)
            points.append(new_point)
            print(f"New point created at ({gl_x}, {gl_y})")
           
        else:
            print("Click outside boundary - point not created")
    
    glutPostRedisplay()

# ===== Projection Setup =====
def setup_projection():
    """Defines a 2D orthographic coordinate system."""
    glViewport(0, 0, WINDOW_WIDTH, WINDOW_HEIGHT)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0.0, WINDOW_WIDTH, 0.0, WINDOW_HEIGHT, 0.0, 1.0)
    glMatrixMode(GL_MODELVIEW)

# ===== Display & Animation =====
def display():
    """Main display callback for rendering each frame."""
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    setup_projection()
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glClear(GL_COLOR_BUFFER_BIT)
    

    draw_boundary()
    draw_all_points()

    glutSwapBuffers()

def animate():
    if not is_frozen:
        update_all_points()
    update_blink_effect()
    
    glutPostRedisplay()

# ===== Main Function =====
def main():
    glutInit()
    glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE)
    glutInitWindowSize(WINDOW_WIDTH, WINDOW_HEIGHT)
    glutInitWindowPosition(100, 100)
    glutCreateWindow(b"Task2")

    # Register callback functions
    glutDisplayFunc(display)
    glutIdleFunc(animate)
    glutKeyboardFunc(keyboard_listener)
    glutSpecialFunc(special_key_listener)
    glutMouseFunc(mouse_listener)
 
    glutMainLoop()

# ===== Entry Point =====
if __name__ == "__main__":
    main()