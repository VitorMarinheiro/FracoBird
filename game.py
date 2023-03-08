from operator import attrgetter
import random
import pygame
import numpy as np
from ia import LayerDense, ActivationReLu
from obj import Obj, Pipe, Bird, Text, Chart, Button


class Game:

    def __init__(self):

        self.window = 0
        self.tam_population = 70
        self.generation = 0
        self.best_score = 0
        self.score = 0
        self.start_game([])
        self.score_value = 0
        self.text_score = Text(70, str(self.score_value), "flappy-bird-font")
        self.text_generation = Text(15, "", "OpenSans-Regular")
        self.text_population = Text(15, "", "OpenSans-Regular")
        self.text_best_score = Text(15, "", "OpenSans-Regular")
        self.text_score_hist = Text(15, "HISTÓRICO DE PONTUAÇÃO", "OpenSans-Regular")
        self.graph = Chart(350, 510, 100, 500)
        self.playing = True
        self.ticks = 0
        self.re_lu = ActivationReLu()
        self.hist_y = []
        self.all_dead = False
        self.count_dead_time = 0

    def draw(self, window):
        self.window = window
        self.background.draw(window)
        self.pipe_group.draw(window)
        self.bird_group.draw(window)
        self.ground_group.draw(window)
        self.text_score.draw(window, 620, 50)
        self.text_generation.draw(window, 10, 570)
        self.text_population.draw(window, 10, 590)
        self.text_best_score.draw(window, 10, 610)
        self.text_score_hist.draw(window, 500, 610)
        self.graph.draw(window)
        self.button.draw(window)

    def validate_population_alive(self):
        for bird in self.population:
            if bird.play:
                return True
        return False

    def update(self):
        vivos = 0
        if self.validate_population_alive():
            self.spawn_pipes()
            self.move_ground()
            self.move_bg()
            for bird in self.population:
                if bird.play:
                    vivos += 1
                    bird.getDistance(self.pipes_top_list, self.pipes_bottom_list, self.window)
                    bird.dense1.forward(np.array([bird.distTop, bird.distBottom, bird.distXToPipes]))
                    bird.dense2.forward(self.re_lu.forward(bird.dense1.output))
                    if self.re_lu.forward(bird.dense2.output) > 0:
                        bird.jump()

                    bird.collision_ground(self.ground_group)
                    bird.collision_pipe(self.pipe_group)
                    bird.collision_sky()

                    # Seta valor de score
                    for bird in self.population:
                        if bird.play:
                            if bird.pts > self.score:
                                self.score = bird.pts
                                if self.score > self.best_score:
                                    self.best_score = self.score
        else:

            # Delay para mostrar animacao de ultimo morto
            self.all_dead = True
            self.count_dead_time += 1

            # Reseta game apos delay
            if self.count_dead_time > 20:
                max_attr = max(self.population, key=attrgetter('fitness'))
                self.hist_y.append(self.score + 1)
                self.population[0] = max_attr
                self.start_game(self.population)
                self.ticks = 0
                self.graph.update(self.generation, self.hist_y)
                self.score = 0
                self.count_dead_time = 0
                self.all_dead = False

        # Update sprites
        self.ground_group.update()
        self.pipe_group.update()
        self.bird_group.update()
        self.text_score.text_update(str(self.score))
        self.text_population.text_update("Indivíduos Vivos: " + str(vivos))
        self.text_generation.text_update("Geração: " + str(self.generation))
        self.text_best_score.text_update("Melhor Pontuação: " + str(self.best_score))

        # Captura eventos de clique
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            self.button.handle_event(event)

    def start_game(self, listOfBirds):
        self.generation += 1

        self.background = pygame.sprite.Group()
        self.ground_group = pygame.sprite.Group()
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

        self.button = Button(900, 525, 150, 50, "GRADES")

        # Reseta a populacao
        new_population = []

        for index_population in range(0, self.tam_population):
            new_bird = Bird("assets/bird0_0.png", self.bird_group)
            new_bird.dense1 = LayerDense(3, 6)
            new_bird.dense2 = LayerDense(6, 1)
            if len(listOfBirds) > 0:
                new_bird.dense1.weights = listOfBirds[0].dense1.weights.copy()
                new_bird.dense2.weights = listOfBirds[0].dense2.weights.copy()
            new_population.append(new_bird)

        # Aplica mutacao
        for index in range(0, self.tam_population):
            if (len(listOfBirds) > 0) and (index > 0):
                new_population[index].dense1.random_weights()
                new_population[index].dense2.random_weights()

        self.population = new_population[:]
        self.pipes_top_list = []
        self.pipes_bottom_list = []
        self.coin_list = []
        self.create_pipe()

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

    def spawn_pipes(self):

        self.ticks += 1

        # Remove pipes mortos da lista de pipesTop e pipesBottom
        if self.ticks >= 1:
            for i, pipe in enumerate(self.pipes_top_list):
                if pipe.rect[0] <= -100:
                    self.pipes_top_list.pop(i)
                    self.pipes_bottom_list.pop(i)

        # de 1,5 seggundo em segundo
        if self.ticks >= 60:
            self.ticks = 0
            self.create_pipe()

    def create_pipe(self):
        self.pipe_bottom = Pipe("assets/pipe1.png", 1280, random.randrange(250, 430), self.pipe_group)
        self.pipe_top = Pipe("assets/pipe2.png", 1280, self.pipe_bottom.rect[1] - 510, self.pipe_group)
        self.pipes_top_list.append(self.pipe_top)
        self.pipes_bottom_list.append(self.pipe_bottom)
