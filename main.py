import pygame, sys, math
from pygame import Vector2

width = 600
height = 600
fps = 60

pygame.init()
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()

def draw_point_in_chartesian_plane(pos):
    pos += Vector2(width/2, height/2)
    pygame.draw.circle(screen, 'white', pos, 2)

def draw_line_in_chartesian_plane(pos1, pos2):
    pos1 += Vector2(width/2, height/2)
    pygame.draw.line(screen, 'red', pos1, pos2)

class Circle():
    def __init__(self, radius) -> None:
        # x^2 + y^2 = r^2
        self.radius = radius
        self.color = 'white'
        self.w_center = width/2
        self.h_center = height/2

    def render(self):
        pygame.draw.circle(screen, 'white', (width/2, height/2), self.radius, 1)

    def tangent_point(self, mouse_pos, txt1, txt2):
        x0 = mouse_pos[0] - 300
        y0 = mouse_pos[1] - 300
        d0 = math.sqrt(pow(x0, 2)+pow(y0, 2))

        try:
            const1 = (pow(self.radius, 2)/pow(d0, 2))
            const2 = (math.sqrt(pow(d0, 2) - pow(self.radius, 2)))

            x1 = (const1*x0) + ((self.radius/pow(d0, 2)) * const2 * (-y0))
            x2 = (const1*x0) - ((self.radius/pow(d0, 2)) * const2 * (-y0))

            y1 = (const1*y0) + ((self.radius/pow(d0, 2)) * const2 * (x0))
            y2 = (const1*y0) - ((self.radius/pow(d0, 2)) * const2 * (x0))

            if x0 > 0:
                final_x1 = -width/2
                final_x2 = -width/2
            elif x0 < 0:
                final_x1 = width/2
                final_x2 = width/2

            if y0 > 0 and -self.radius < x0 < 0:
                final_x1 = -width/2
            elif y0 < 0 and 0 < x0 < self.radius:
                final_x1 = width/2

            if y0 > 0 and 0 < x0 < self.radius:
                final_x2 = width/2
            elif y0 < 0 and -self.radius < x0 < 0:
                final_x2 = -width/2

            m1 = (y1 - y0) / (x1 - x0)
            final_y1 = m1 * (final_x1 - x1) + y1
            draw_line_in_chartesian_plane(Vector2(final_x1, final_y1), mouse_pos)

            m2 = (y2 - y0) / (x2 - x0)
            final_y2 = m2 * (final_x2 - x2) + y2
            draw_line_in_chartesian_plane(Vector2(final_x2, final_y2), mouse_pos)

            txt1.update(new_center=(x1+290, y1+290))
            txt2.update(new_center=(x2+290, y2+290))
            txt_error.update(new_txt='')
        except Exception as e:
            print(e)
            txt_error.update(new_txt='No possible tangent line')

class Text():
    def __init__(self, center_pos, txt, size, color = 'white', bg_color = 'black', antialias = True, font = 'arial'):
        self.txt = txt
        self.color = color
        self.bg_color = bg_color
        self.antialias = antialias
        self.center_pos = center_pos
        self.font = pygame.font.SysFont(font, size)
        self.rendered_txt = self.font.render(self.txt, self.antialias, self.color, self.bg_color)
        self.rect = self.rendered_txt.get_rect(center = self.center_pos)

    def render(self):
        screen.blit(self.rendered_txt, self.rect)

    def update(self, new_txt = None, new_center = None, new_color = None, new_bg_color = None):
        if new_txt == None:
            new_txt = self.txt
        else:
            self.txt = new_txt

        if new_center == None:
            new_center = self.center_pos
        else:
            self.center_pos = new_center

        if new_color == None:
            new_color = self.color
        else:
            self.color = new_color

        if new_bg_color == None:
            new_bg_color = self.bg_color
        else:
            self.bg_color = new_bg_color

        self.rendered_txt = self.font.render(self.txt, self.antialias, self.color, self.bg_color)
        self.rect = self.rendered_txt.get_rect(center = self.center_pos)

circle = Circle(100)
txt_p0 = Text(pygame.mouse.get_pos(), 'P0', 14, bg_color=None)
txt_p1 = Text((-20, -20), 'P1', 14, bg_color=None)
txt_p2 = Text((-20, -20), 'P2', 14, bg_color=None)
txt_error = Text((width/2, 100), '', 32, bg_color=None)


while True:

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.fill((25, 25, 25))

    pygame.draw.line(screen, 'white', (width/2, 0), (width/2, height), 2)
    pygame.draw.line(screen, 'white', (0, height/2), (width, height/2), 2)

    circle.render()
    mouse_pos = pygame.mouse.get_pos()
    txt_p0.update(new_center=(Vector2(mouse_pos) + Vector2(10, -10)))
    if 0 < mouse_pos[0] < width:
        circle.tangent_point(mouse_pos, txt_p1, txt_p2)

    txt_p0.render()
    txt_p1.render()
    txt_p2.render()
    txt_error.render()

    pygame.display.flip()
    clock.tick(fps)