import pygame
import os
from pygame.locals import *
import sys


class GameState():
    def __init__(self):
        #The definition of a gamestate, "--" means an empty space of the board for the ease of parsing
        self.board = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bP", "bP", "bP", "bP", "bP", "bP", "bP", "bP"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wP", "wP", "wP", "wP", "wP", "wP", "wP", "wP"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"],
        ]

        self.moveFunctions = {'P' : self.getPawnMoves, 'R' : self.getRookMoves, 'N' : self.getKnightMoves, 
                                'B' : self.getBishopMoves, 'Q' : self.getQueenMoves, 'K' : self.getKingMoves} #A list of functions used as a switch statement

        self.whiteToMove = True #Who to move
        self.moveLog = [] #To later display / undo moves
        self.whiteKingLocation = (7, 4)
        self.blackKingLocation = (0, 4) #Keeping track of the kings location
        self.checkMate = False
        self.staleMate = False
        self.inCheck = False
        self.pins = [] 
        self.checks = []





    #Executes a move object
    def makeMove(self, move):
        if self.board[move.startRow][move.startCol] != "--":
            self.board[move.startRow][move.startCol] = "--"
            self.board[move.endRow][move.endCol] = move.pieceMoved
            self.moveLog.append(move) #log the move to display the history
            self.whiteToMove = not self.whiteToMove #swap players
            #updating the kings location
            if move.pieceMoved == 'wK':
                self.whiteKingLocation = (move.endRow, move.endCol)
            
            elif move.pieceMoved == 'bK':
                self.blackKingLocation = (move.endRow, move.endCol)

    #Undoes the last made move from the move log
    def undoMove(self):
        if len(self.moveLog) != 0:
            move = self.moveLog.pop()       #pops the move from the list
            self.board[move.startRow][move.startCol] = move.pieceMoved # moved piece from the last move back to its starting square
            self.board[move.endRow][move.endCol] = move.pieceCaptured # the same goes for the captured piece
            self.whiteToMove = not self.whiteToMove #turns back
            #update the kings location
            if move.pieceMoved == 'wK':
                self.whiteKingLocation = (move.startRow, move.startCol)
            
            elif move.pieceMoved == 'bK':
                self.blackKingLocation = (move.startRow, move.startCol)


    def getValidMoves(self):
        moves = []
        self.inCheck, self.pins, self.checks = self.checkForPinsAndChecks()
        if self.whiteToMove:
            kingRow =  self.whiteKingLocation[0]
            kingCol = self.whiteKingLocation[1]
        else:
            kingRow = self.blackKingLocation[0]
            kingRow = self.blackKingLocation[1]
        if self.inCheck:
            if len(self.checks) == 1: #only one check
                moves = self.getAllPossibleMoves()
                check = self.checks[0]  #saving check info to a variable
                checkRow = check[0]
                checkCol = check[1]
                checkingPiece = self.board[checkRow][checkCol] #enemy piece causing the check
                validSquares = [] #squares that allied pieces can move into
                #if knight, must capture or move the king, it cannot be blocked
                if checkingPiece[1] == 'N':
                    validSquares = [(checkRow, checkCol)]
                else:
                    for i in range (1, 8):
                        validSquare = (kingRow + check[2] * i, kingCol + check[3] * i) #check[2] or check[3] are the offsets
                        validSquares.append(validSquare)
                        if validSquare[0] == checkRow and validSquare[1] == checkCol:
                            break
                #remove all moves that dont block checks or move the king
                for i in range(len(moves) - 1, -1, -1): #always go backwards when removing from a list
                    if moves[i].pieceMoved[i] != 'K': #move does not move king so it must be a block or a capture
                        if not (moves[i].endRow, moves[i].endCol) in validSquares:
                            moves.remove(moves[i])
            else:
                self.getKingMoves(kingRow, kingCol, moves)#double check, king has to move
        else:
            moves = self.getAllPossibleMoves() #not in check so are moves are ok

        return moves

    #Determine if the current player is in check
    def isCheck(self):
        if self.whiteToMove:
            return self.squareUnderAttack(self.whiteKingLocation[0], self.whiteKingLocation[1])
        else:
            return self.squareUnderAttack(self.blackKingLocation[0], self.blackKingLocation[1])

    #Determine if the enemy can attack the square 
    def squareUnderAttack(self, row, col):
        self.whiteToMove = not self.whiteToMove #switch to opponents turn
        oppMoves = self.getAllPossibleMoves()
        self.whiteToMove = not self.whiteToMove #Switching back the turns
        for move in oppMoves:
            if move.endRow == row and move.endCol == col: #Square is under attack
                return True
        return False

    #Conditions for all moves without a check happening
    def getAllPossibleMoves(self):
        moves = [] #list of moves
        for row in range(len(self.board)):
            for col in range(len(self.board[row])):
                turn = self.board[row][col][0] #determines by the first character whose turn it is -> "wP" [w], "bP" [b], "--" [-] -> empty square
                if(turn == 'w' and self.whiteToMove) or (turn == 'b' and not self.whiteToMove):
                    piece = self.board[row][col][1] #determines by the first character which piece it is -> "wP" [P], "bQ" [Q], "--" [-] -> empty square
                    self.moveFunctions[piece](row, col, moves) #Calls the appropriate move function
        return moves

    #Get all possible moves for each individual piece 
    # TODO: Repair pawns being able to move diagonally without captures
    # TODO: Fix a weird bug that dissalows black to capture in the start of the game
    # TODO: Pawn moves
    # TODO: I dont know why the fuck does the pieces can move weirdly, i give up 
    # TODO: The logic seems ok, but regardless the king can move like a fucking knight 
    ############################################################################################################################################          
    
    def getPawnMoves(self, row, col, moves):
        piecePinned = False
        pinOffset = ()
        for i in range(len(self.pins) - 1, -1, -1):
            if self.pins[i][0] == row and self.pins[i][1] == col:
                piecePinned = True
                pinOffset = (self.pins[i][2], self.pins[i][3])
                self.pins.remove(self.pins[i])
                break

        if self.whiteToMove: #white turn to move
            if self.board[row-1][col] == "--": #One square pawn move validation
                if not piecePinned or pinOffset == (-1, 0):
                    moves.append(Move((row, col), (row - 1, col), self.board))
                    if row == 6 and self.board[row - 2][col] == "--": #2 square moves
                        moves.append(Move((row, col), (row-2, col), self.board))
        #captures
            if col - 1 >= 0: #capture to the left
                if self.board[row-1][col-1][0] == 'b':
                    if not piecePinned or pinOffset == (-1, -1):
                        moves.append(Move((row, col), (row-1, col-1), self.board))
            if col + 1 <= 7: #capture to the right
                if self.board[row-1][col+1][0] == 'b':
                    if not piecePinned or pinOffset == (-1, 1):
                        moves.append(Move((row, col), (row - 1, col + 1), self.board)) 

        else: #black pawn moves
            if self.board[row+1][col] == "--": #One square pawn move validation
                if not piecePinned or pinOffset == (1, 0):
                    moves.append(Move((row, col), (row + 1, col), self.board))
                    if row == 1 and self.board[row + 2][col] == "--": #2 square moves
                        moves.append(Move((row, col), (row+2, col), self.board))
        #captures
            if col - 1 >= 0: #capture to the left
                if self.board[row+1][col-1][0] == 'w':
                    if not piecePinned or pinOffset == (1, -1):
                        moves.append(Move((row, col), (row+1, col-1), self.board))
            if col + 1 <= 7: #capture to the right
                if self.board[row+1][col+1][0] == 'w':
                    if not piecePinned or pinOffset == (1, 1):
                        moves.append(Move((row, col), (row + 1, col + 1), self.board)) 
    
    def getRookMoves(self, row, col, moves):
        piecePinned = False
        pinOffset = ()
        for i in range(len(self.pins) - 1, -1, -1):
            if self.pins[i][0] == row and self.pins[i][1] == col:
                piecePinned = True
                pinOffset = (self.pins[i][2], self.pins[i][3])
                if self.board[row][col][1] != 'Q': #cant remove queen from pin on rook moves, onyl remove it on bishop moves
                    self.pins.remove(self.pins[i])
                break

        offsets = ((-1,0), (0,-1), (1,0), (0,1)) #movement offsets for a rook
        color = "b" if self.whiteToMove else "w" #color change dependent on turn
        for o in offsets:
            for i in range(1,8):
                endRow = row + o[0] * i
                endCol = col + o[1] * i
                if 0 <= endRow < 8 and 0 <= endCol < 8:
                    if not piecePinned and pinOffset == o or pinOffset == (-o[0], -o[1]):
                        endPiece = self.board[endRow][endCol]
                        if endPiece == "--": #empty square validation
                            moves.append(Move((row, col), (endRow, endCol), self.board))
                        elif endPiece[0] == color: # enemy piece validation
                            moves.append(Move((row, col), (endRow, endCol), self.board))
                            break
                        else: #friendly piece detection, therefore move is invalid
                            break
                else: #outside of the board validation
                    break
                
    def getKnightMoves(self, row, col, moves):
        piecePinned = False
        for i in range(len(self.pins) - 1, -1, -1):
            if self.pins[i][0] == row and self.pins[i][1] == col:
                piecePinned = True
                self.pins.remove(self.pins[i])
                break

        offsets = ((-2,-1), (-2,1), (-1,-2), (-1,2), (1,-2), (1,2), (2,-1), (2,1))
        color = "w" if self.whiteToMove else "b"
        for o in offsets:
            endRow = row + o[0]
            endCol = col + o[1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                if not piecePinned:
                    endPiece = self.board[endRow][endCol]
                    if endPiece[0] != color:
                        moves.append(Move((row, col), (endRow, endCol), self.board))

    def getBishopMoves(self, row, col, moves):
        piecePinned = False
        pinOffset = ()
        for i in range(len(self.pins) - 1, -1, -1):
            if self.pins[i][0] == row and self.pins[i][1] == col:
                piecePinned = True
                pinOffset = (self.pins[i][2], self.pins[i][3])
                self.pins.remove(self.pins[i])
                break

        offsets = ((-1,-1), (-1,1), (1,-1), (1,1))
        color = "b" if self.whiteToMove else "w"
        for o in offsets:
            for i in range(1,8):
                endRow = row + o[0] * i
                endCol = col + o[1] * i
                if 0 <= endRow < 8 and 0 <= endCol < 8:
                    if not piecePinned or pinOffset == o or pinOffset == (-o[0], -o[1]):
                        endPiece = self.board[endRow][endCol]
                        if endPiece == "--": #empty space validation
                            moves.append(Move((row, col), (endRow, endCol), self.board))
                        elif endPiece[0] == color: # enemy piece validation
                            moves.append(Move((row, col), (endRow, endCol), self.board))
                            break
                        else: #friendly piece - invalid
                            break
                else: #off board
                    break
    def getQueenMoves(self, row, col, moves): #queen is just a rook and a bishop connected together.
        self.getBishopMoves(row, col, moves)
        self.getRookMoves(row, col, moves)

    def getKingMoves(self, row, col, moves):
        rowMoves = (-1, -1, -1, 0, 0, 1, 1, 1)
        colMoves = (-1, 0, 1, -1, 1, -1, 0, 1)
        color = "w" if self.whiteToMove else "b"
        for i in range(8):
            endRow = row + rowMoves[i]
            endCol = col + rowMoves[i]
            if 0 <= endRow < 8 and 0 <= endCol <= 8:
                endPiece = self.board[endRow][endCol]
                if endPiece[0] != color:#not an allied piece
                    if color == 'w':
                        self.whiteKingLocation = (endRow, endCol)
                    else:
                        self.blackKingLocation = (endRow, endCol)
                    
                    inCheck, pins, checks = (endRow, endCol)
                    if not inCheck:
                        moves.append(Move((row, col), (endRow, endCol), self.board))
                    if color == 'w':
                        self.whiteKingLocation = (endRow, endCol)
                    else:
                        self.blackKingLocation = (endRow, endCol)


    def checkForPinsAndChecks(self):
        pins = [] #for allied pinned pieces
        checks = [] #for allied checks
        inCheck = False

        if self.whiteToMove:
            enemyColor = "b"
            allyColor = "w"
            startRow = self.whiteKingLocation[0]
            startCol = self.whiteKingLocation[1]
        else:
            enemyColor = "w"
            allyColor = "b"
            startRow = self.blackKingLocation[0]
            startCol = self.blackKingLocation[1]

        #check for pins and checks using these offsets
        offsets = ((-1,0), (0, -1), (1, 0), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1))
        for j in range(len(offsets)):
            d = offsets[j]
            possiblePin = () #resets possible pins list
            for i in range(1, 8):
                endRow = startRow + d[0] * i
                endCol = startCol + d[0] * i
                if 0 <= endRow < 8 and 0 <= endCol < 8:
                    endPiece = self.board[endRow][endCol]
                    if endPiece[0] == allyColor:
                        if possiblePin == ():
                            possiblePin = (endRow, endCol, d[0], d[1])
                        else:
                            break
                    elif endPiece[0] == enemyColor:
                        pieceType = endPiece[1]
                        if(0 <= j <= 3 and pieceType == 'R') or \
                                (4 <= j <= 7 and pieceType == 'B') or \
                                (i == 1 and pieceType == 'P' and ((enemyColor == 'w' and 6 <= j <= 7) or (enemyColor == 'b' and 4 <= j <= 5))) or \
                                (pieceType == 'Q') or (i == 1 and pieceType == 'K'):
                            if possiblePin == (): #no piece blocking so check
                                inCheck = True
                                checks.append((endRow, endCol, d[0], d[1]))
                                break
                            else: #piece blocking, hence pin 
                                pins.append(possiblePin)
                                break
                        else: #no pin and check
                            break
                else: #off board
                    break
        knightOffsets = ((-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1))
        for m in knightOffsets:
            endRow = startRow + m[0]
            endCol = startCol + m[1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                endPiece = self.board[endRow][endCol]
                if endPiece[0] == enemyColor and endPiece[1] == 'N':
                    inCheck = True
                    checks.append((endRow, endCol, m[0], m[1]))
        return inCheck, pins, checks


class Move():
    ranksToRows = {"1" : 7, "2" : 6, "3" : 5, "4" : 4, "5" : 3, "6" : 2, "7" : 1, "8" : 0} #translates ranks to rows
    rowsToRanks = {v: k for k, v in ranksToRows.items()} #reverse translation of rows to ranks (reverse dictionary)

    filesToCols = {"a" : 0, "b" : 1, "c" : 2, "d" : 3, "e" : 4, "f" : 5, "g" : 6, "h" : 7 }
    colsToFiles = {v: k for k, v in filesToCols.items()}

    def __init__(self, startSquare, endSquare, board):
        self.startRow = startSquare[0]
        self.startCol = startSquare[1] #starting position of a move -> (2,3)
        self.endRow = endSquare[0]
        self.endCol = endSquare[1] #ending position of a move -> (6,2)
        self.pieceMoved = board[self.startRow][self.startCol] #finds a piece on a board associated with the coordinates
        self.pieceCaptured = board[self.endRow][self.endCol] #finds either a piece or an empty square associated with the coordinates
        self.moveID = self.startRow * 1000 + self.startCol * 100 + self.endRow * 10 + self.startCol #generating a unique move id between 0 and 7777
    #Overriding the equal method
    def __eq__(self, other):
        if isinstance(other, Move):
            return self.moveID == other.moveID
        return False

    #TODO: real chess notation!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    def getChessNotation(self):
        return self.getRankFile(self.startRow, self.startCol) + "->" + self.getRankFile(self.endRow, self.endCol)

    #Helper method to return the translated row and column
    def getRankFile(self, row, col):
        return self.colsToFiles[col] + self.rowsToRanks[row]