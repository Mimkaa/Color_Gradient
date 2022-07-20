import math
import pygame as pg
from settings import *

vec = pg.Vector2

def distance(x1,y1,x2,y2):
    dist = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
    return dist

def vec2int(v):
    return [int(v.x), int(v.y)]

def find_the_closest_out_of_a_sequence(coords,seque):
    dict_dist={}
    seque=[vec(el) for el in seque]
    for el in seque:
        dict_dist[tuple(vec2int(el))] = distance(el.x,el.y,coords.x,coords.y)

    the_lowest_dist = float("inf")
    index = 0
    for n, v in enumerate(dict_dist.values()):
        if v < the_lowest_dist:
            the_lowest_dist = v
            index = n

    return index

class Color_Gradient:
    def __init__(self, colors, surf_nums, game):
        self.colors = colors
        self.surfs = [pg.Surface((10, 10)) for i in range(surf_nums)]
        self.colors = []
        for n, s in enumerate(self.surfs):
            s.fill(self.linear_color_gradient_mult(colors, n/100))
            self.colors.append(self.linear_color_gradient_mult(colors, n/100))
        self.current_color = 20
        self.game = game
        self.rects = []

    def linear_color_gradient(self, start_color, end_color, t):
        # t is how far we are in the linear interpolation
        return [start_color[j] + t * (end_color[j] - start_color[j]) for j in range(3)]

    def linear_color_gradient_mult(self, colors, t):
        length_of_each = 1 / len(colors)
        grad = [i * length_of_each for i in range(len(colors))]

        # find the closest value(lower then our t) and the index of it
        closest = float('inf')
        closest_index = 0
        rev_grad = reversed(grad)
        for n, i in enumerate(rev_grad):
            if i <= t:
                closest = i
                closest_index = (len(grad) - 1) - n
                break

        to_go = (t - closest) / length_of_each

        return self.linear_color_gradient(colors[closest_index], colors[(closest_index + 1) % len(colors)], to_go)

    def update(self):
        self.rects.clear()
        offset = (WIDTH - (10 * len(self.surfs))) / 2
        for n, s in enumerate(self.surfs):
            rect = s.get_rect()
            rect.topleft = (n * 10 + offset ,HEIGHT - 50)
            self.rects.append(rect)
        # set the color we are checking
        rect_toplefts = [r.topleft for r in self.rects]
        if pg.mouse.get_pressed()[0]:
            self.current_color = find_the_closest_out_of_a_sequence(vec(pg.mouse.get_pos()),  rect_toplefts)

    def draw(self, surf):

        rect = pg.Rect(WIDTH//4 , HEIGHT//4, WIDTH//2, HEIGHT//2)
        pg.draw.rect(surf, self.colors[self.current_color], rect)
        color = self.colors[self.current_color]
        self.game.draw_text(f'RGB: {[int(i) for i in self.colors[self.current_color]]}', self.game.font, 50, (int(255 - color[0]), int(255 - color[1]), int(255 - color[2])), rect.centerx, rect.centery, align="center")

        offset = (WIDTH - (10 * len(self.surfs))) / 2
        for n, s in enumerate (self.surfs):
            surf.blit(s, (n * 10 + offset ,HEIGHT - 50))
        pg.draw.rect(surf, (int(255 - color[0]), int(255 - color[1]), int(255 - color[2])), self.rects[self.current_color], 1)