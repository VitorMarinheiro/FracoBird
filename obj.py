import pygame


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

        if self.rect[0] <= -100:
            self.kill()

    def anim(self):
        self.ticks = (self.ticks + 1) % 6  # Vai fazer isso 6x depois voltar para 0
        self.image = pygame.image.load("assets/" + str(self.ticks) + ".png")


class Bird(Obj):

    def __init__(self, img, x, y, *groups):
        super().__init__(img, x, y, *groups)

        self.ticks = 0
        self.vel = -8
        self.grav = 2
        self.pts = 0

        self.play = True

    def update(self, *args):
        if self.play:
            self.anim()

        self.move()

    def anim(self):
        self.ticks = (self.ticks + 1) % 4  # Vai fazer isso 6x depois voltar para 0
        self.image = pygame.image.load("assets/bird" + str(self.ticks) + ".png")

    def move(self):
        key = pygame.key.get_pressed()

        self.vel += self.grav
        self.rect[1] += self.vel

        # Limitador de velocidade de queda e subida
        if self.vel >= 20:
            self.vel = 20
        if self.vel <= -10:
            self.vel = -10

        # pulo
        if self.play:
            if key[pygame.K_SPACE]:
                self.vel -= 10

        # bloqueio do passaro no chao e no teto
        if self.rect[1] >= 440:
            self.rect[1] = 440
        elif self.rect[1] <= 0:
            self.rect[1] = 0
            self.vel = 4

    def collision_pipe(self, group):

        if pygame.sprite.spritecollide(self, group, False):
            self.play = False
            self.image = pygame.transform.rotate(self.image, 270)

    def collision_ground(self, group):

        if pygame.sprite.spritecollide(self, group, False):
            self.play = False

    def collision_coin(self, group):

        if pygame.sprite.spritecollide(self, group, True):
            self.pts += 1


class Text:

    def __init__(self, size, text):
        pygame.font.init()
        self.font = pygame.font.Font("assets/font/flappy-bird-font.ttf", size)
        self.render = self.font.render(text, True, (0, 0, 0))

    def draw(self, window, x, y):
        window.blit(self.render, (x, y))

    def text_update(self, text):
        self.render = self.font.render(text, True, (0, 0, 0))
