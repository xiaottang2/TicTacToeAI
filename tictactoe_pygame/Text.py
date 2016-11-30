import pygame
from util import load_image
class Text(pygame.sprite.Sprite):
    """a bar object, horizontal or vertical in the canvas. It does not move"""
    def __init__(self, text, width, height):
        pygame.sprite.Sprite.__init__(self)
        self.font = pygame.font.Font(None, 20)
        self.textSurf = self.font.render(text, 1, (255, 255, 255))
        self.Surf = pygame.Surface((width, height))
        W = self.textSurf.get_width()
        H = self.textSurf.get_height()
        self.Surf.blit(self.textSurf,(width/2 - W/2, height/2 - H/2))

        self.image = self.Surf
        self.rect = (0, 0, width, height)

    def update(self):
        pass
