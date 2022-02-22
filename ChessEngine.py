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


    #Executes a move object
    def makeMove(self, move):
        if self.board[move.startRow][move.startCol] != "--":
            self.board[move.startRow][move.startCol] = "--"
            self.board[move.endRow][move.endCol] = move.pieceMoved
            self.moveLog.append(move) #log the move to display the history
            self.whiteToMove = not self.whiteToMove #swap players

    #Undoes the last made move from the move log
    def undoMove(self):
        if len(self.moveLog) != 0:
            move = self.moveLog.pop()       #pops the move from the list
            self.board[move.startRow][move.startCol] = move.pieceMoved # moved piece from the last move back to its starting square
            self.board[move.endRow][move.endCol] = move.pieceCaptured # the same goes for the captured piece
            self.whiteToMove = not self.whiteToMove #turns back

    #TODO: "Check" conditions
    def getValidMoves(self):
        return self.getAllPossibleMoves() #for now, just return all possible moves
    
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
        if self.whiteToMove: #white turn to move
            if self.board[row-1][col] == "--": #One square pawn move validation
                moves.append(Move((row, col), (row-1, col), self.board)) #Appends all possible one square pawn moves to possible move list
                if row == 6 and self.board[row - 2][col] == "--":
                    moves.append(Move((row, col), (row-2, col), self.board)) #Appends all possible 2 square starting moves to a move list
            if col - 1 >= 0: #Constraint that prevents a pawn from capturing outside of the board
                if self.board[row-1][col-1][0] == 'b': #Searches for a black piece to capture to the left diagonal
                    moves.append(Move((row, col), (row-1, col-1), self.board)) #Appends all currently possible left-diagonal captures for white to the move list for the current position
            if col+1 <= 7: #Prevents from capturing a piece outside of the board
                if self.board[row-1][col+1][0] == 'b': #Black piece to capture to the right diagonal 
                    moves.append(Move((row, col), (row-1, col+1), self.board)) #Appends all possible right-diagonal captures to the move list for the current position
        else: #black pawn moves
            if self.board[row+1][col] == "--": #One square moves
                moves.append(Move((row, col), (row+1, col), self.board))
                if row == 1 and self.board[row + 2][col] == "--": #One square
                    moves.append(Move((row, col), (row+2, col), self.board))
                if col - 1 >= 0: #left capture
                    if self.board[row+1][col-1][0] == 'w':
                        moves.append(Move((row, col), (row+1, col-1), self.board))
                if col + 1 <= 7: #capture to the right
                    if self.board[row+1][col+1][0] == "w":
                        moves.append(Move((row, col), (row+1, col+1), self.board))
    
    def getRookMoves(self, row, col, moves):
        offsets = ((-1,0), (0,-1), (1,0), (0,1)) #movement offsets for a rook
        color = "b" if self.whiteToMove else "w" #color change dependent on turn
        for o in offsets:
            for i in range(1,8):
                endRow = row + o[0] * i
                endCol = col + o[1] * i
                if 0 <= endRow < 8 and 0 <= endCol < 8:
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
        offsets = ((-2,-1), (-2,1), (-1,-2), (-1,2), (1,-2), (1,2), (2,-1), (2,1))
        color = "w" if self.whiteToMove else "b"
        for o in offsets:
            endRow = row + o[0]
            endCol = col + o[1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                endPiece = self.board[endRow][endCol]
                if endPiece[0] != color: #Not an ally piece, therfore its either an empty square or enemy piece
                    moves.append(Move((row, col), (endRow, endCol), self.board))

    def getBishopMoves(self, row, col, moves):
        offsets = ((-1,-1), (-1,1), (1,-1), (1,1))
        color = "b" if self.whiteToMove else "w"
        for o in offsets:
            for i in range(1,8):
                endRow = row + o[0] * i
                endCol = col + o[1] * i
                if 0 <= endRow < 8 and 0 <= endCol < 8:
                    endPiece = self.board[endRow][endCol]
                    if endPiece == "--":
                        moves.append(Move((row, col), (endRow, endCol), self.board))
                    elif endPiece[0] == color:
                        moves.append(Move((row, col), (endRow, endCol), self.board))
                        break
                    else: 
                        break
                else:
                    break
    def getQueenMoves(self, row, col, moves): #queen is just a rook and a bishop connected together.
        self.getBishopMoves(row, col, moves)
        self.getRookMoves(row, col, moves)

    def getKingMoves(self, row, col, moves):
        offsets = ((-1,-1), (-1,0), (-1,1), (0,-1), (0,1), (1,-1), (1,0), (1,1))
        color = "w" if self.whiteToMove else "b"
        for i in range(8):
            endRow = row + offsets[i][0]
            endCol = col + offsets[i][1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                endPiece = self.board[endRow][endCol]
                if endPiece[0] != color:
                    moves.append(Move((row, col), (endRow, endCol), self.board))

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