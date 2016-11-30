import pygame
from util import load_image
class Cross(pygame.sprite.Sprite):
    """a bar object, horizontal or vertical in the canvas. It does not move"""
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image("cross.png", -1)

    def update(self):
        pass
