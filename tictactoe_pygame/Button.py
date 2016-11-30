import pygame
from util import load_image
class Button(pygame.sprite.Sprite):
    def __init__(self, name):
        pygame.sprite.Sprite.__init__(self)
        self.name = name
        if name == 'player':
            self.imagename = "btn_player_first.png"
            self.imagename_un = "btn_player_first_un.png"
        elif name == 'AI':
            self.imagename = "btn_ai_first.png"
            self.imagename_un = "btn_ai_first_un.png"
        
        self.available = True
        self.image, self.rect = load_image(self.imagename)

    def update(self):
        if self.available:
            self.image, _ = load_image(self.imagename)
        else:
            self.image, _ = load_image(self.imagename_un)