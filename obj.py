import pygame
import copy


class Obj(pygame.sprite.Sprite):

    def __init__(self, img, x, y, *groups):
        super().__init__(*groups)

        self.image = pygame.image.load(img)
        self.rect = self.image.get_rect()
        self.rect[0] = x
        self.rect[1] = y


class Pipe(Obj):

    def __init__(self, img, x, y, *groups):
        super().__init__(img, x, y, *groups)

        self.vel = 4

    def update(self):
        self.move()

    def move(self):
        self.rect[0] -= self.vel

        if self.rect[0] <= -100:
            self.kill()


class Coin(Obj):

    def __init__(self, img, x, y, *groups):
        super().__init__(img, x, y, *groups)

        self.ticks = 0
        self.vel = 4

    def update(self, *args):
        self.move()
        self.anim()

    def move(self):
        self.rect[0] -= self.vel

    def anim(self):
        self.ticks = (self.ticks + 1) % 6  # Vai fazer isso 6x depois voltar para 0
        self.image = pygame.image.load("assets/" + str(self.ticks) + ".png")


class Bird(pygame.sprite.Sprite):

    def __init__(self, img, *groups):
        super().__init__(*groups)

        self.image = pygame.image.load(img)
        self.rect = self.image.get_rect()
        self.rect[0] = 50
        self.rect[1] = 120
        self.ticks = 0
        self.vel = -8
        self.velHorizontal = 0
        self.grav = 2
        self.pts = 0
        self.distTop = 0
        self.distBottom = 0
        self.distXToPipes = 0
        self.play = True
        self.fitness = 0

    def copy(self):
        new_bird = Bird("assets/bird0.png", self.groups())
        new_bird.rect = self.rect.copy()
        new_bird.ticks = self.ticks
        new_bird.vel = self.vel
        new_bird.velHorizontal = self.velHorizontal
        new_bird.grav = self.grav
        new_bird.pts = self.pts
        new_bird.distTop = self.distTop
        new_bird.distBottom = self.distBottom
        new_bird.distXToPipes = self.distXToPipes
        new_bird.play = self.play
        new_bird.fitness = self.fitness
        return new_bird

    def update(self, *args):
        if self.play:
            self.anim()

        if self.rect[0] > -70:
            self.move()
        else:
            self.kill()

    def anim(self):
        self.ticks = (self.ticks + 1) % 4  # Vai fazer isso 6x depois voltar para 0
        self.image = pygame.image.load("assets/bird" + str(self.ticks) + ".png")

    def move(self):

        if self.play:
            self.fitness += 0.1

        self.vel += self.grav
        self.rect[1] += self.vel
        self.rect[0] += self.velHorizontal
        self.fitness += 0.1

        # Limitador de velocidade de queda e subida
        if self.vel >= 20:
            self.vel = 20
        if self.vel <= -10:
            self.vel = -10

        # bloqueio do passaro no chao e no teto
        if self.rect[1] >= 440:
            self.rect[1] = 440
        elif self.rect[1] <= 0:
            self.rect[1] = 0
            self.vel = 4

    def jump(self):
        self.vel -= 10

    def collision_pipe(self, group):

        if pygame.sprite.spritecollide(self, group, False):
            self.play = False
            self.image = pygame.transform.rotate(self.image, 270)
            self.vel = 1
            self.velHorizontal = -4
            self.fitness -= 10

    def collision_ground(self, group):

        if pygame.sprite.spritecollide(self, group, False):
            self.play = False
            self.velHorizontal = -4
            self.image = pygame.transform.rotate(self.image, 270)
            self.fitness -= 10

    def collision_sky(self):

        if self.rect[1] <= 0:
            self.play = False
            self.image = pygame.transform.rotate(self.image, 270)
            self.vel = 1
            self.velHorizontal = -4
            self.fitness -= 10

    def collision_coin(self, group):

        if pygame.sprite.spritecollide(self, group, True):
            self.pts += 1
            self.fitness += 50

    def getDistance(self, pipesTop_List, pipesBottom_List):
        if self.play:
            actualPipe = 0
            if self.play and len(pipesTop_List) > 0:
                if pipesTop_List[0].rect[0] + 48 < self.rect[0]:
                    actualPipe = 1
                self.distTop = (pipesTop_List[actualPipe].rect[1] + 358 - self.rect[1])
                self.distBottom = (pipesBottom_List[actualPipe].rect[1] - self.rect[1])
                self.distXToPipes = (pipesBottom_List[actualPipe].rect[0] - self.rect[0])


class Text:

    def __init__(self, size, text):
        pygame.font.init()
        self.font = pygame.font.Font("assets/font/flappy-bird-font.ttf", size)
        self.render = self.font.render(text, True, (0, 0, 0))

    def draw(self, window, x, y):
        window.blit(self.render, (x, y))

    def text_update(self, text):
        self.render = self.font.render(text, True, (0, 0, 0))
