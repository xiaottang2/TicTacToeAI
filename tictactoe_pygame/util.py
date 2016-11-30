import os
import pygame
from pygame.locals import *
from Constants import *
def load_image(name, colorkey=None):
    fullname = os.path.join('res', name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error, message:
        print 'Cannot load image:', fullname
        raise SystemExit, message
    image = image.convert()
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey, RLEACCEL)
    return image, image.get_rect()

def calcPosFromCoord(pos):
    # row
    x, y = pos
    XThresh1 = MARGIN + ITEMSIZE
    XThresh2 = MARGIN + 2 * ITEMSIZE + BARWIDTH
    XThresh3 = MARGIN + 3 * ITEMSIZE + 2 * BARWIDTH
    YThresh1 = MARGIN + ITEMSIZE
    YThresh2 = MARGIN + 2 * ITEMSIZE + BARWIDTH
    YThresh3 = MARGIN + 3 * ITEMSIZE + 2 * BARWIDTH

    if DEBUG:
        print "calc position X:{}, Y:{}".format(x, y)
        print "XThresh1: {}".format(XThresh1)
        print "XThresh2: {}".format(XThresh2)
        print "XThresh3: {}".format(XThresh3)
        print "YThresh1: {}".format(YThresh1)
        print "YThresh2: {}".format(YThresh2)
        print "YThresh3: {}".format(YThresh3)
    

    col = 0 if x > MARGIN and x < XThresh1 else (1 if x > XThresh1 and x < XThresh2 else (2 if x > XThresh2 and x < XThresh3 else None))
    row = 0 if y > MARGIN and y < YThresh1 else (1 if y > YThresh1 and y < YThresh2 else (2 if y > YThresh2 and y < YThresh3 else None))    
    if DEBUG:
        print "row: {}, col: {}".format(row, col)
    return (row, col)