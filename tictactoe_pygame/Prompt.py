import pygame
from util import load_image
from Constants import *
class Prompt(pygame.sprite.Sprite):
    """a bar object, horizontal or vertical in the canvas. It does not move"""
    def __init__(self, result):
        pygame.sprite.Sprite.__init__(self)
        if result == WIN:
        	self.image, self.rect = load_image("prompt_win.png")
        elif result == DRAW:
        	self.image, self.rect = load_image("prompt_draw.png")
        elif result == LOSE:
        	self.image, self.rect = load_image("prompt_lose.png")
        else:
        	raise "Not valid result!"

    def update(self):
        pass

    
