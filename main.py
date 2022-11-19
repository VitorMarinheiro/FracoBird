import pygame
from game import Game

class Main:

    def __init__(self):

        self.window = pygame.display.set_mode([1280, 640])
        pygame.display.set_caption("Fraco Bird")
        pygame.display.set_icon(pygame.transform.scale(pygame.image.load("assets/bird1_.png"), (555, 555)))

        self.loop = True
        self.fps = pygame.time.Clock()

        self.game = Game()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.loop = False

    def draw(self):
        self.game.draw(self.window)
        self.game.update()

    def update(self):
        while self.loop:
            self.fps.tick(30)
            self.events()
            self.draw()
            pygame.display.update()


Main().update()
