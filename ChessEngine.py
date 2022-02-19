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
                                'B' : self.getBishopMoves, 'Q' : self.getQueenMoves, 'K' : self.getKingMoves}

        self.whiteToMove = True
        self.moveLog = []


    #Executes a move object
    def makeMove(self, move):
        if self.board[move.startRow][move.startCol] != "--":
            self.board[move.startRow][move.startCol] = "--"
            self.board[move.endRow][move.endCol] = move.pieceMoved
            self.moveLog.append(move) #log the move to display the history
            self.whiteToMove = not self.whiteToMove #swap players

    #undoes the last made move
    def undoMove(self):
        if len(self.moveLog) != 0:
            move = self.moveLog.pop()       #pops the move from the list
            self.board[move.startRow][move.startCol] = move.pieceMoved # moved piece from the last move back to its starting square
            self.board[move.endRow][move.endCol] = move.pieceCaptured # the same goes for the captured piece
            self.whiteToMove = not self.whiteToMove #turns back

    #Conditions for all moves when a check happens
    def getValidMoves(self):
        return self.getAllPossibleMoves() #for now, just return all possible moves
    
    #Conditions for all moves without a check happening
    def getAllPossibleMoves(self):
        moves = [] #list of moves
        for row in range(len(self.board)):
            for col in range(len(self.board[row])):
                turn = self.board[row][col][0] #determines by the first character whose turn it is -> "wP" [w], "bP" [b], "--" [-] -> empty square
                if(turn == 'w' and self.whiteToMove) or (turn == 'b' and not self.whiteToMove):
                    piece = self.board[row][col][1]
                    self.moveFunctions[piece](row, col, moves) #Calls the appropriate move function
        return moves

    #Get all possible moves for each individual piece 
    # TODO: Repair pawns being able to move diagonally without captures              
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
        else:
            if self.board[row+1][col] == "--": #One square moves
                moves.append(Move((row, col), (row+1, col), self.board))
                if row == 1 and self.board[row + 1][col] == "--": #One square
                    moves.append(Move((row, col), (row+2, col), self.board))
                if col - 1 >= 0: #left capture
                    if self.board[row+1][col-1] == 'w':
                        moves.append(Move((row, col), (row+1, col-1), self.board))
                if col + 1 <= 7: #capture to the right
                    if self.board[row+1][col+1] == "w":
                        moves.append(Move((row, col), (row+1, col+1), self.board))
    
    def getRookMoves(self, r, c, moves):
        pass
    
    def getKnightMoves(self, r, c, moves):
        pass

    def getBishopMoves(self, r, c, moves):
        pass

    def getQueenMoves(self, r, c, moves):
        pass

    def getKingMoves(self, r, c, moves):
        pass

class Move():
    ranksToRows = {"1" : 7, "2" : 6, "3" : 5, "4" : 4, "5" : 3, "6" : 2, "7" : 1, "8" : 0} #translates ranks to rows
    rowsToRanks = {v: k for k, v in ranksToRows.items()} #reverse translation of rows to ranks (reverse dictionary)

    filesToCols = {"a" : 0, "b" : 1, "c" : 2, "d" : 3, "e" : 4, "f" : 5, "g" : 6, "h" : 7 }
    colsToFiles = {v: k for k,v in filesToCols.items()}

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