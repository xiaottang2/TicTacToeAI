import os, sys
import pygame
from pygame.locals import *
from tictactoe_pygame import Game

if not pygame.font: print "Warning: fonts disabled"
if not pygame.mixer: print "Warning: Sound disabled"



def main():

    player1 = Game.AIPlayer()
    player2 = Game.HumanPlayer()
    game = Game.Game(player1, player2, False)
    player1.loadPolicy()

    game.init()

    again = True
    while again:
        winner = game.start()
        again = game.promptIfAgain(winner)
        game.reset()



if __name__ == '__main__': main()