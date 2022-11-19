from obj import Obj, Pipe, Coin, Bird, Text
import pygame
import random

class Game:

    def __init__(self):

        self.background = pygame.sprite.Group()
        self.ground_group = pygame.sprite.Group()
        self.coin_group = pygame.sprite.Group()
        self.pipe_group = pygame.sprite.Group()
        self.bird_group = pygame.sprite.Group()

        self.bg = Obj("assets/sky.png", 0, 0, self.background)
        self.bg2 = Obj("assets/sky.png", 360, 0, self.background)
        self.ground = Obj("assets/ground.png", 0, 480, self.ground_group)
        self.ground2 = Obj("assets/ground.png", 360, 480, self.ground_group)
        self.bird = Bird("assets/bird0.png", 50, 120, self.bird_group)

        self.pipes1_list = []
        self.pipes2_list = []
        self.coin_list = []

        self.pipe = Pipe("assets/pipe1.png", -2000, random.randrange(290, 430), self.pipe_group)
        self.pipe2 = Pipe("assets/pipe2.png", -2000, self.pipe.rect[1] - 550, self.pipe_group)
        self.pipes1_list.append(self.pipe)
        self.pipes2_list.append(self.pipe2)

        self.score = Text(100, "0")

        self.ticks = 0

    def draw(self, window):
        self.background.draw(window)
        self.pipe_group.draw(window)
        self.bird_group.draw(window)
        self.coin_group.draw(window)
        self.ground_group.draw(window)
        self.score.draw(window, 150, 50)

    def update(self):
        if self.bird.play:
            self.spaw_pipes()
            self.move_ground()
            self.move_bg()
            self.bird.collision_ground(self.ground_group)
            self.bird.collision_pipe(self.pipe_group)
            self.bird.collision_coin(self.coin_group)
            self.score.text_update(str(self.bird.pts))
        else:
            # Para os canos e moedas
            for i in self.pipes1_list:
                i.vel = 0
            for i in self.pipes2_list:
                i.vel = 0
            for i in self.coin_list:
                i.vel = 0

        self.ground_group.update()
        self.pipe_group.update()
        self.bird_group.update()
        self.coin_group.update()

    def move_bg(self):
        self.bg.rect[0] -= 1
        self.bg2.rect[0] -= 1

        if self.bg.rect[0] <= -360:
            self.bg.rect[0] = 0
        if self.bg2.rect[0] <= 0:
            self.bg2.rect[0] = 360

    def move_ground(self):
        self.ground.rect[0] -= 4
        self.ground2.rect[0] -= 4

        if self.ground.rect[0] <= -360:
            self.ground.rect[0] = 0
        if self.ground2.rect[0] <= 0:
            self.ground2.rect[0] = 360

    def spaw_pipes(self):
        self.ticks += 1

        # de 2 em 2 segundo
        if self.ticks >= 60:
            self.ticks = 0
            self.pipe = Pipe("assets/pipe1.png", 360, random.randrange(290, 430), self.pipe_group)
            self.pipe2 = Pipe("assets/pipe2.png", 360, self.pipe.rect[1] - 550, self.pipe_group)
            coin = Coin("assets/0.png", 388, self.pipe.rect[1] - 120, self.coin_group)
            self.pipes1_list.append(self.pipe)
            self.pipes2_list.append(self.pipe2)
            self.coin_list.append(coin)