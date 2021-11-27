import pygame
import os
from pygame.locals import *
import sys



#Piece class for displaying information on pieces
class Piece():
    def __init__(self, team, type, image, killable=False):
        self.team = team
        self.type = type
        self.image = image
        self.killable = killable


#Creating the screen with the board
class GameScreen():
    def __init__(self):
        self.screenSize = (480,480)
        self.board = [[' ' for i in range(8)] for i in range(8)]

    #Main game class            
    def initGame(self):
        #Creating pieces
        bp = Piece('b', 'p', os.path.join("images", "Chess_pawnBlack.png"))
        wp = Piece('w', 'p', os.path.join("images", "Chess_pawnWhite.png"))
        bb = Piece('b', 'b', os.path.join("images", "Chess_bishopBlack.png"))    
        wb = Piece('w', 'b', os.path.join("images", "Chess_bishopWhite.png"))
        br = Piece('b', 'r', os.path.join("images", "Chess_rookBlack.png"))    
        wr = Piece('w', 'r', os.path.join("images", "Chess_rookWhite.png"))
        bkn = Piece('b', 'kn', os.path.join("images", "Chess_knightBlack.png"))    
        wkn = Piece('w', 'kn', os.path.join("images", "Chess_knightWhite.png"))
        bk = Piece('b', 'k', os.path.join("images", "Chess_kingBlack.png"))    
        wk = Piece('w', 'k', os.path.join("images", "Chess_kingWhite.png"))
        bq = Piece('b', 'q', os.path.join("images", "Chess_queenBlack.png"))    
        wq = Piece('w', 'q', os.path.join("images", "Chess_queenWhite.png"))

        #Defining the starting order of pieces on the grid
        starting_order = {(0,0) : pygame.image.load(br.image),
                          (1,0) : pygame.image.load(bkn.image),
                          (2,0) : pygame.image.load(bb.image),
                          (3,0) : pygame.image.load(bk.image),
                          (4,0) : pygame.image.load(bq.image),
                          (5,0) : pygame.image.load(bb.image),
                          (6,0) : pygame.image.load(bkn.image),
                          (7,0) : pygame.image.load(br.image),
                          (0,1) : pygame.image.load(bp.image),      #####---BLACK PIECES---#####
                          (1,1) : pygame.image.load(bp.image),
                          (2,1) : pygame.image.load(bp.image),
                          (3,1) : pygame.image.load(bp.image),
                          (4,1) : pygame.image.load(bp.image),
                          (5,1) : pygame.image.load(bp.image),
                          (6,1) : pygame.image.load(bp.image),
                          (7,1) : pygame.image.load(bp.image),
                          (0,2): None, (1,2): None, (2,2): None, (3,2): None,
                          (4,2): None, (5,2): None, (6,2): None, (7,2): None,
                          (0,3): None, (1,3): None, (2,3): None, (3,3): None,
                          (4,3): None, (5,3): None, (6,3): None, (7,3): None,
                          (0,4): None, (1,4): None, (2,4): None, (3,4): None,       
                          (4,4): None, (5,4): None, (6,4): None, (7,4): None,
                          (0,5): None, (1,5): None, (2,5): None, (3,5): None,
                          (4,5): None, (5,5): None, (6,5): None, (7,5): None,
                          (0,6) : pygame.image.load(wr.image),
                          (1,6) : pygame.image.load(wkn.image),
                          (2,6) : pygame.image.load(wb.image),
                          (3,6) : pygame.image.load(wk.image),
                          (4,6) : pygame.image.load(wq.image),
                          (5,6) : pygame.image.load(wb.image),
                          (6,6) : pygame.image.load(wkn.image),
                          (7,6) : pygame.image.load(wr.image),
                          (0,7) : pygame.image.load(wp.image),      #####---WHITE PIECES---#####
                          (1,7) : pygame.image.load(wp.image),
                          (2,7) : pygame.image.load(wp.image),
                          (3,7) : pygame.image.load(wp.image),
                          (4,7) : pygame.image.load(wp.image),
                          (5,7) : pygame.image.load(wp.image),
                          (6,7) : pygame.image.load(wp.image),
                          (7,7) : pygame.image.load(wp.image),
                          }

        #Edits board instance
        def create_board(self):
            self.board[0] = [Piece('b', 'r', os.path.join("images", "Chess_rookBlack.png")), Piece('b', 'kn', os.path.join("images", "Chess_knightBlack.png")), 
                            Piece('b', 'b', os.path.join("images", "Chess_bishopBlack.png")), Piece('b', 'q', os.path.join("images", "Chess_queenBlack.png")),
                            Piece('b', 'k', os.path.join("images", "Chess_kingBlack.png")), Piece('b', 'b', os.path.join("images", "Chess_bishopBlack.png")), 
                            Piece('b', 'kn', os.path.join("images", "Chess_knightBlack.png")), Piece('b', 'r', os.path.join("images", "Chess_rookBlack.png")) 
                            ]

            self.board[7] = [Piece('w', 'r', os.path.join("images", "Chess_rookWhite.png")), Piece('w', 'kn', os.path.join("images", "Chess_knightWhite.png")), 
                            Piece('w', 'b', os.path.join("images", "Chess_bishopWhite.png")), Piece('w', 'q', os.path.join("images", "Chess_queenWhite.png")),
                            Piece('w', 'k', os.path.join("images", "Chess_kingWhite.png")), Piece('w', 'b', os.path.join("images", "Chess_bishopWhite.png")), 
                            Piece('w', 'kn', os.path.join("images", "Chess_knightWhite.png")), Piece('w', 'r', os.path.join("images", "Chess_rookWhite.png")) 
                            ]
            for i in range(8):
                self.board[1][i] = Piece('b', 'p', os.path.join("images", "Chess_pawnBlack.png"))
                self.board[6][i] = Piece('w', 'p', os.path.join("images","Chess_pawnWhite.png"))               

#enviroment variables for game instance
WHITE = (255, 255, 255)
GREY = (128, 128, 128)
YELLOW = (204, 204, 0)
BLUE = (50, 255, 255)
BLACK = (0, 0, 0)
WIDTH = 800
WIN = pygame.display.set_mode((WIDTH, WIDTH))

#initializes the gameInstance
class gameInstance():

    def __init__(self, row, col, width):
        self.row = row
        self.col = col
        self.width = width
        self.x = int(row*width)
        self.y = int(col*width)
        self.colour = WHITE

    def draw(self, WIN):
        pygame.draw.rect(WIN, self.colour, (self.x, self.y, WIDTH / 8, WIDTH / 8))
    



