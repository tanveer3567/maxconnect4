from copy import copy
import random
import sys
from copy import deepcopy
import math

class maxConnect4Game:
    def __init__(self, evaluation):
        self.gameBoard = [[0 for _ in range(7)] for _ in range(6)]
        self.currentTurn = 0
        self.player1Score = 0
        self.player2Score = 0
        self.pieceCount = 0
        self.gameFile = None
        self.evaluation = evaluation
        self.depth = 0  

    def checkPieceCount(self):
        self.pieceCount = sum(1 for row in self.gameBoard for piece in row if piece)

    def printGameBoard(self):
        print ('-----------------')
        for i in range(6):
            for j in range(7):
                print('%d' % self.gameBoard[i][j]),
            print ("\n")
        print ('-----------------')

    def writeGameBoardToFile(self, file, turn):
        for i in range(6):
            for j in range(7):
                file.write('%d' % self.gameBoard[i][j]),
            file.write ("\n")
        file.write(str(turn))
        file.write ("\n")

    def printGameBoardToFile(self):
        for row in self.gameBoard:
            self.gameFile.write(''.join(str(col) for col in row) + '\r\n')
        self.gameFile.write('%s\r\n' % str(self.currentTurn))

    def playPiece(self, column):
        if not self.gameBoard[0][column]:
            for i in range(5, -1, -1):
                if not self.gameBoard[i][column]:
                    self.gameBoard[i][column] = self.currentTurn
                    self.pieceCount += 1
                    return 1

    def playDummyPiece(self, board, column, turn):
        if not board[0][column]:
            for i in range(5, -1, -1):
                if not board[i][column]:
                    board[i][column] = turn
                    return board
        return None

    def aiPlay(self):
        org_board = deepcopy(self.gameBoard)
        new_board = deepcopy(self.gameBoard)
        maxEval = -float('inf')
        alpha = -float('inf')
        beta = float('inf')
        col = None
        for j in range(7):
            new_board = self.playDummyPiece(deepcopy(org_board), j, self.currentTurn)
            if new_board:
                if self.currentTurn == 1:
                    next_turn = 2
                else:
                    next_turn = 1
                eval = self.dfs(new_board, next_turn, 1, alpha, beta)
                if eval > maxEval:
                    maxEval = eval
                    col = j 
                alpha = max(alpha, maxEval)
                if beta <= alpha:
                    break
        self.gameBoard = org_board
        self.playPiece(col)
        print('\n\nmove %d: Player %d, column %d\n' % (self.pieceCount, self.currentTurn, col+1))
        if self.currentTurn == 1:
            self.currentTurn = 2
        elif self.currentTurn == 2:
            self.currentTurn = 1

    def isBoardFull(self, board):
        for j in range(7):
            if board[0][j] == 0:
                return False
        return True

    def dfs(self, new_board, turn, rec_depth, alpha, beta):
        if rec_depth >= self.depth or self.isBoardFull(new_board):
            return self.evaluation.evaluate(new_board, self.currentTurn)

        org_board = new_board
        if turn == self.currentTurn:
            maxEval = -float('inf')
            for j in range(7):
                new_board = self.playDummyPiece(deepcopy(org_board), j, turn)
                if new_board:
                    if turn == 1:
                        next_turn = 2
                    else:
                        next_turn = 1
                    eval = self.dfs(new_board, next_turn, rec_depth+1, alpha, beta)
                    maxEval = max(maxEval, eval)
                    alpha = max(alpha, maxEval)
                    if beta <= alpha:break
            return maxEval
        else:
            minEval = +float('inf')
            for j in range(7):
                new_board = self.playDummyPiece(deepcopy(org_board), j, turn)
                if new_board:
                    if turn == 2:
                        next_turn = 1
                    else:
                        next_turn = 2
                    eval = self.dfs(new_board, next_turn, rec_depth+1, alpha, beta)
                    minEval = min(minEval, eval)
                    beta = min(beta, minEval)
                    if beta <= alpha:break
            return minEval