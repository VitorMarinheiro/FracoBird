import numpy as np

from IA import Layer_Dense, Activation_ReLU
from obj import Obj, Pipe, Coin, Bird, Text
from operator import attrgetter
import pygame
import random


class Game:

    def __init__(self):

        self.tamPopulation = 50
        self.startGame([])
        self.scoreValue = 0
        self.score = Text(70, str(self.scoreValue))
        self.textPopulation = Text(20, str(self.tamPopulation))
        self.playing = True
        self.ticks = 0
        self.ReLU = Activation_ReLU()

    def draw(self, window):
        self.background.draw(window)
        self.pipe_group.draw(window)
        self.bird_group.draw(window)
        self.coin_group.draw(window)
        self.ground_group.draw(window)
        self.score.draw(window, 620, 50)
        self.textPopulation.draw(window, 1200, 600)

    def validatePopulationAlive(self):
        for bird in self.population:
            if bird.play:
                return True
        return False

    def update(self):
        vivos = 0
        if self.validatePopulationAlive():
            self.spaw_pipes()
            self.move_ground()
            self.move_bg()
            for bird in self.population:
                if bird.play:
                    vivos += 1
                    bird.getDistance(self.pipesTop_list, self.pipesBottom_list)

                    bird.dense1.forward(np.array([bird.distTop, bird.distBottom, bird.distXToPipes, bird.rect[1]]))
                    bird.dense2.forward(self.ReLU.forward(bird.dense1.output))
                    if self.ReLU.forward(bird.dense2.output) > 0:
                        bird.jump()

                    bird.collision_ground(self.ground_group)
                    bird.collision_pipe(self.pipe_group)
                    bird.collision_coin(self.coin_group)
                    bird.collision_sky()
                    self.scoreValue = bird.pts
        else:
            max_attr = max(self.population, key=attrgetter('fitness'))
            print(max_attr.fitness)
            self.population[0] = max_attr
            self.startGame(self.population)
            self.ticks = 0

        # Update sprites
        self.ground_group.update()
        self.pipe_group.update()
        self.bird_group.update()
        self.coin_group.update()
        self.score.text_update(str(self.scoreValue))
        self.textPopulation.text_update(str(vivos))

    def startGame(self, listOfBirds):
        self.background = pygame.sprite.Group()
        self.ground_group = pygame.sprite.Group()
        self.coin_group = pygame.sprite.Group()
        self.pipe_group = pygame.sprite.Group()
        self.bird_group = pygame.sprite.Group()

        self.bg = Obj("assets/sky.png", 0, 0, self.background)
        self.bg2 = Obj("assets/sky.png", 360, 0, self.background)
        self.bg3 = Obj("assets/sky.png", 720, 0, self.background)
        self.bg4 = Obj("assets/sky.png", 1080, 0, self.background)
        self.bg5 = Obj("assets/sky.png", 1440, 0, self.background)
        self.ground = Obj("assets/ground.png", 0, 480, self.ground_group)
        self.ground2 = Obj("assets/ground.png", 360, 480, self.ground_group)
        self.ground3 = Obj("assets/ground.png", 720, 480, self.ground_group)
        self.ground4 = Obj("assets/ground.png", 1080, 480, self.ground_group)
        self.ground5 = Obj("assets/ground.png", 1440, 480, self.ground_group)

        # reseta a populacao
        newPopulation = []

        for indexPopulation in range(0, self.tamPopulation):
            newBird = Bird("assets/bird0.png", self.bird_group)
            newBird.dense1 = Layer_Dense(4, 2)
            newBird.dense2 = Layer_Dense(2, 1)
            if len(listOfBirds) > 0:
                newBird.dense1.weights = listOfBirds[0].dense1.weights.copy()
                newBird.dense2.weights = listOfBirds[0].dense2.weights.copy()
            newPopulation.append(newBird)

        # Aplica mutacao
        for index in range(0, self.tamPopulation):
            if (len(listOfBirds) > 0) and (index > 0):
                newPopulation[index].dense1.randomWeights()
                newPopulation[index].dense2.randomWeights()

        self.population = newPopulation[:]
        self.pipesTop_list = []
        self.pipesBottom_list = []
        self.coin_list = []
        self.createPipe()

    def move_bg(self):
        self.bg.rect[0] -= 1
        self.bg2.rect[0] -= 1
        self.bg3.rect[0] -= 1
        self.bg4.rect[0] -= 1
        self.bg5.rect[0] -= 1

        # movimenta o backgound
        if self.bg.rect[0] <= -360:
            self.bg.rect[0] = 0
        if self.bg2.rect[0] <= 0:
            self.bg2.rect[0] = 360
        if self.bg3.rect[0] <= 360:
            self.bg3.rect[0] = 720
        if self.bg4.rect[0] <= 720:
            self.bg4.rect[0] = 1080
        if self.bg5.rect[0] <= 1080:
            self.bg5.rect[0] = 1440

    def move_ground(self):

        self.ground.rect[0] -= 4
        self.ground2.rect[0] -= 4
        self.ground3.rect[0] -= 4
        self.ground4.rect[0] -= 4
        self.ground5.rect[0] -= 4

        # movimenta o chao
        if self.ground.rect[0] <= -360:
            self.ground.rect[0] = 0
        if self.ground2.rect[0] <= 0:
            self.ground2.rect[0] = 360
        if self.ground3.rect[0] <= 360:
            self.ground3.rect[0] = 720
        if self.ground4.rect[0] <= 720:
            self.ground4.rect[0] = 1080
        if self.ground5.rect[0] <= 1080:
            self.ground5.rect[0] = 1440

    def spaw_pipes(self):

        self.ticks += 1

        # Remove pipes mortos
        if self.ticks >= 1:
            for pipe in self.pipesTop_list:
                if pipe.rect[0] <= -50:
                    self.pipesTop_list.remove(pipe)

        # de 2 em 2 segundo
        if self.ticks >= 90:
            self.ticks = 0
            self.createPipe()

    def createPipe(self):
        self.pipeBottom = Pipe("assets/pipe1.png", 1280, random.randrange(250, 430), self.pipe_group)
        self.pipeTop = Pipe("assets/pipe2.png", 1280, self.pipeBottom.rect[1] - 550, self.pipe_group)
        coin = Coin("assets/0.png", 1308, self.pipeBottom.rect[1] - 120, self.coin_group)
        self.pipesTop_list.append(self.pipeTop)
        self.pipesBottom_list.append(self.pipeBottom)
        self.coin_list.append(coin)
