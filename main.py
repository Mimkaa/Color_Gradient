import pygame as pg
import sys
from settings import *
from objects import *
from os import path
class Game:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        pg.key.set_repeat(500, 100)
        self.load_data()

    def load_data(self):
        self.font=path.join("PixelatedRegular-aLKm.ttf")
    def draw_text(self, text, font_name, size, color, x, y, align="nw"):
        font = pg.font.Font(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        if align == "nw":
            text_rect.topleft = (x, y)
        if align == "ne":
            text_rect.topright = (x, y)
        if align == "sw":
            text_rect.bottomleft = (x, y)
        if align == "se":
            text_rect.bottomright = (x, y)
        if align == "n":
            text_rect.midtop = (x, y)
        if align == "s":
            text_rect.midbottom = (x, y)
        if align == "e":
            text_rect.midright = (x, y)
        if align == "w":
            text_rect.midleft = (x, y)
        if align == "center":
            text_rect.center = (x, y)
        self.screen.blit(text_surface, text_rect)
        return text_rect

    def new(self):
        # initialize all variables and do all the setup for a new game
        self.all_sprites = pg.sprite.Group()

        self.color_grad = Color_Gradient((WHITE, GREEN, BLUE, RED, TURQUOISE), 100, self)

    def run(self):
        # game loop - set self.playing = False to end the game
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000
            self.events()
            self.update()
            self.draw()

    def quit(self):
        pg.quit()
        sys.exit()

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
        # update portion of the game loop
        self.all_sprites.update()
        self.color_grad.update()

    def draw_grid(self):
        for x in range(0, WIDTH, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (0, y), (WIDTH, y))

    def draw(self):
        self.screen.fill(BGCOLOR)
        # self.draw_grid()
        # self.all_sprites.draw(self.screen)

        self.color_grad.draw(self.screen)

        # fps
        self.draw_text(str(int(self.clock.get_fps())), self.font, 40, WHITE, 50, 50, align="center")
        pg.display.flip()

    def events(self):
        # catch all events here
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.quit()
                



# create the game object
g = Game()
g.new()
g.run()
