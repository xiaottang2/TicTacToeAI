from Bar import Bar
from Circle import Circle
from Cross import Cross
from Button import Button
from Prompt import Prompt
from Text import Text
from Constants import *
import pygame
class Board(object):
    """Game board, responsible to init bars and objects"""   
    def __init__(self, width, height):
        bar_h_1 = Bar()
        bar_h_2 = Bar()
        bar_v_1 = Bar()
        bar_v_2 = Bar()

        self.width = width
        self.height = height
        self.margin = MARGIN
        self.barWidth = BARWIDTH
        self.itemSize = ITEMSIZE
        self.buttonWidth = BUTTONWIDTH
        self.buttonHeight = BUTTONHEIGHT
        self.board_arr = [[CHECKER_EMPTY for i in range(NUM_ROWS)] for j in range(NUM_COLS)]

        rotate = pygame.transform.rotate
        scale = pygame.transform.scale

        bar_h_1.image = rotate(bar_h_1.image, 90)
        bar_h_2.image = rotate(bar_h_2.image, 90)
        bar_h_1.image = scale(bar_h_1.image, ((int(width-2*self.margin)), self.barWidth))
        bar_h_2.image = scale(bar_h_2.image, ((int(width-2*self.margin)), self.barWidth))
        bar_v_1.image = scale(bar_v_1.image, (self.barWidth, (int(width-2*self.margin))))
        bar_v_2.image = scale(bar_v_2.image, (self.barWidth, (int(width-2*self.margin))))


        bar_h_1.rect.midtop = (self.margin, self.margin + self.itemSize + 0.5 * self.barWidth)
        bar_h_2.rect.midtop = (self.margin, self.margin + 2 * self.itemSize + 1.5 * self.barWidth)
        bar_v_1.rect.midtop = (self.margin + self.itemSize + 0.5 * self.barWidth, self.margin)
        bar_v_2.rect.midtop = (self.margin + 2 * self.itemSize + 1.5 * self.barWidth, self.margin)
        
        self.bar_h_1 = bar_h_1
        self.bar_h_2 = bar_h_2
        self.bar_v_1 = bar_v_1
        self.bar_v_2 = bar_v_2

        btn_player_first = Button('player')
        btn_ai_first = Button('AI')
        btn_player_first.rect.midtop = (self.width-self.margin-self.buttonWidth, self.height-3*self.margin-self.buttonHeight)
        btn_ai_first.rect.midtop = (2*self.margin, self.height-3*self.margin-self.buttonHeight)

        self.btn_player_first = btn_player_first
        self.btn_ai_first = btn_ai_first

        self.prompt = False

    def getAllSprites(self):
        # The first 6 sprites are always static
        allSprites = (self.bar_h_1,
                    self.bar_h_2,
                    self.bar_v_1,
                    self.bar_v_2)

        for i in range(NUM_ROWS):
            for j in range(NUM_COLS):
                checker = self.board_arr[i][j]
                if checker == CHECKER_P1:
                    if DEBUG:
                        print "adding a Cross sprite"
                    allSprites += (self.getCrossSprite(i, j),)
                elif checker == CHECKER_P2:
                    if DEBUG:
                        print "adding a Circle sprite"
                        allSprites += (self.getCircleSprite(i, j),)

        if self.prompt:
            # allSprites.append(self.getPromptSprite())
            text = None
            if self.result == WIN:
                text = Text("You win. Click anywhere to restart...", 0.5 * self.width, LINEHEIGHT)
            elif self.result == LOSE:
                text = Text("You lose. Click anywhere to restart...", 0.5 * self.width, LINEHEIGHT)
            elif self.result == DRAW:
                text = Text("It's a draw. Click anywhere to restart...", 0.5 * self.width, LINEHEIGHT)
            else:
                raise "Cannot create text: invalid result"
            text.center = (150, self.height-100)

            allSprites += (text,)
            


        return allSprites

    def getCrossSprite(self, i, j):
        """Args:
             i: row in the board
             j: col in the board
                --------------
                  0 |  1 |  2
                --------------
                  3 |  4 |  5
                --------------
                  6 |  7 |  8
                --------------
           Returns:
             A cross sprite at the position
        """
        cross = Cross()
        row = i
        column = j
        cross.image = pygame.transform.smoothscale(cross.image, (self.itemSize, self.itemSize))
        cross.rect.midtop = (self.margin + (1 + column) * self.itemSize + (K + column) * self.barWidth, self.margin + row * self.itemSize + row * self.barWidth)
        return cross

    def getCircleSprite(self, i, j):
        """Same as getCrossSprite(), only use circle"""
        circle = Circle()
        row = i
        column = j
        circle.image = pygame.transform.smoothscale(circle.image, (self.itemSize, self.itemSize))
        if DEBUG:
            print "scaling Circle to W:{}, H:{}".format(self.itemSize, self.itemSize)
        circle.rect.midtop = (self.margin + (1 + column) * self.itemSize + (K + column) * self.barWidth, self.margin + row * self.itemSize + row * self.barWidth)
        return circle

    def getPromptSprite(self):
        promptSprite = Prompt(self.result)
        if DEBUG:
            pass
            # print "scaling promptSprite to W:{}, H:{}".format(0.6 * self.width, 0.3 * self.height)
        promptSprite.image = pygame.transform.scale(promptSprite.image, (int(self.width), int(self.height)))
        # promptSprite.center = (0.5 * self.width, 0.5 * self.height)
        return promptSprite

    def feedState(self, state):
        # Update the state of the board
        self.board_arr = state.getBoard()


    def setPrompt(self, prompt):
        self.prompt = prompt

    def setWinner(self, winner):
        self.winner = winner
        if winner is None:
            self.result = DRAW
        elif "human" in winner.lower() or winner == CHECKER_P2:
            self.result = WIN
        elif "ai" in winner.lower() or winner == CHECKER_P1:
            self.result = LOSE
        else:
            raise "Not a valid winner!"
