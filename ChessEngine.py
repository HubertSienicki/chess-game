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
        self.whiteToMove = True
        self.moveLog = []

    def makeMove(self, move):
        if self.board[move.startRow][move.startCol] != "--":
            self.board[move.startRow][move.startCol] = "--"
            self.board[move.endRow][move.endCol] = move.pieceMoved
            self.moveLog.append(move) #log the move to display the history
            self.whiteToMove = not self.whiteToMove #swap players

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

    #TODO: real chess notation!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    def getChessNotation(self):
        return self.getRankFile(self.startRow, self.startCol) + self.getRankFile(self.endRow, self.endCol)

    #Helper method to return the translated row and column
    def getRankFile(self, row, col):
        return self.colsToFiles[col] + self.rowsToRanks[row]