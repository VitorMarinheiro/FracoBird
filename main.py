import pygame
from game import Game


class Main:

    def __init__(self):
        """Inicializador das variáveis necessárias"""

        self.window = pygame.display.set_mode([1280, 640])
        pygame.display.set_caption("Fraco Bird")
        pygame.display.set_icon(
            pygame.transform.scale(pygame.image.load("assets/bird0_2.png"), (555, 555))
        )

        self.loop = True
        self.fps = pygame.time.Clock()

        self.game = Game()

    def events(self):
        """Captura todos os eventos ocorridos no pygame, como clicks, botões e afins"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.loop = False

    def draw(self):
        """Insere na janela do pygame todos os elementos necessários abaixo do self.game"""
        self.game.draw(self.window)
        self.game.update()

    def update(self):
        """Realiza o update do pygame de acordo com o fps definido"""
        while self.loop:
            self.fps.tick(30)
            self.events()
            self.draw()
            pygame.display.update()


Main().update()
