import ChessEngine
import pygame as py

WIDTH = HEIGHT = 512 #Window sizings
DIMENSION = 8 #Chessboard dimensions
SQUARESIZE = HEIGHT // DIMENSION
MAX_FPS = 30
IMAGES = {}

#Loading pieces 
#The pieces can be accesed using an id
def LoadImages():
    pieces = ['wP','bP','wN','bN','wR','bR','wB','bB','wK','bK','wQ','bQ']
    for piece in pieces:
        IMAGES[piece] = py.transform.scale(py.image.load("images/" + piece + ".png"), (SQUARESIZE,SQUARESIZE))

def main():
    py.init()
    screen = py.display.set_mode((WIDTH, HEIGHT))
    clock = py.time.Clock()
    screen.fill(py.Color("white"))
    gs = ChessEngine.GameState()
    LoadImages()
    running = True

    while running:
        for e in py.event.get():
            if e.type == py.QUIT:
                running = False
        drawGameState(screen, gs)
        clock.tick(MAX_FPS)
        py.display.flip()

#creating an instance of the game
def drawGameState(screen, gs):
    #draw the board
    drawBoard(screen)
    #draw pieces
    drawPieces(screen, gs.board)

#Draw the board
def drawBoard(screen):
    #Colors of the squares on the board
    colors = [py.Color("white"), py.Color("grey")]

    for x in range(DIMENSION):
        for y in range(DIMENSION):
            color = colors[((x+y)%2)]
            py.draw.rect(screen, color, py.Rect(y*SQUARESIZE, x*SQUARESIZE, SQUARESIZE, SQUARESIZE))

#Draw pieces using the current gamestate
def drawPieces(screen, board):
    for x in range(DIMENSION):
        for y in range(DIMENSION):
            piece = board[x][y]
            if piece != "--":   #Not an empty square
                screen.blit(IMAGES[piece], py.Rect(y*SQUARESIZE, x*SQUARESIZE, SQUARESIZE, SQUARESIZE))
        
if __name__ == "__main__":
    main()