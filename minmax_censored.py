#!/usr/bin/env python
# coding: utf-8

# # Designing a Game Playing AI Using MinMax with α - β Pruning
# ## Introduction
# 
# Our objective is to use Min-Max with alpha / beta pruning to find a winning strategy for either player. Moreover, both players will try to win as fast as possible.

# In[1]:


import numpy as np
import itertools




# ## Tic Tac Toe

# This class implememnts a TicTacToa game. The followng are the methods:
# * make_copy   : returns a copy of the game object.
# * move(ii,jj) : the player who's turn it is will check cell ii,jj
# * children    : returns a list of all game objects that result from 1 move
# * result      : returns the result, always between \[-1,1\]. A negative result indicates a player 2 win, 0 indicates a tie.
# * final_move  : return true if the current game is at a final state.

# In[2]:


class game_TicTacToe:
    def __init__(self):
        self.ROWS = 3
        self.COLS = 3
        self.board = np.zeros((self.ROWS, self.COLS))
        self.player = 1;
        self.numMoves = 1;

    def make_copy(self):
        newGame = game_TicTacToe()
        newGame.board = self.board.copy()
        newGame.player = self.player
        return newGame

    def move(self, ii, jj):
        if self.board[ii, jj] == 0:
            self.board[ii, jj] = self.player
        self.player *= -1
        self.numMoves += 1;
        return

    def children(self):
        children = []
        for ii, jj in np.argwhere(self.board == 0):
            newGame = self.make_copy()
            newGame.move(ii, jj)
            children.append(newGame)
        return children

    def result(self):
        PL1 = 3.0
        PL2 = -3.0
        if max(np.sum(self.board, axis=0)) == PL1 or max(np.sum(self.board, axis=1)) == PL1 or np.trace(
                self.board) == PL1 or np.trace(np.fliplr(self.board)) == PL1:
            return 1 / self.numMoves
        if min(np.sum(self.board, axis=0)) == PL2 or min(np.sum(self.board, axis=1)) == PL2 or np.trace(
                self.board) == PL2 or np.trace(np.fliplr(self.board)) == PL2:
            return -1 / self.numMoves
        return 0

    def final_move(self):
        return self.ROWS * self.COLS == len(np.nonzero(self.board)[0]) or (self.result() != 0)




# # Show_game
# 
# Given a list of "boards" (every game class has a board field) this method will draw the game. For instance it might draw the following TicTacToa game:

# In[23]:


"""
Given a list of "boards" (every game class has a board field) this method will draw the game. 
For instance it might draw the following TicTacToa game:
"""


# In[4]:


def show_game(plays,gameType='TicTacToe'):
    if np.sum(np.sum(np.abs(plays[0]))) != 0:
        plays.reverse()
    def ticks(player):
        if player == 1:
            return 'X'
        if player == -1:
            if gameType == 'TicTacToe':
                return 'O'
            return 'X'
        return ' '
    gameStr = ''
    for play in plays:
        playStr = []
        ROWS,COLS =  np.shape(play)
        for i in range(0,ROWS):
            playStr.append('|'.join([' '+ticks(play[i,j])+' ' for j in range(0,COLS)]))
        playStr = '\n-----------\n'.join(playStr)
        gameStr += playStr
        gameStr +='\n\n'
    return gameStr


# # Min Max
# 
# Class MinMax that has an alpha beta method.
# 
# Params: game object, current alpha, current beta, and True if it's the max turn.
# Returns: a list of the boards of the best game alpha and beta could play, and the result of the game (same as the result of the game object that has the last board)

# In[16]:


GLOBAL_NUM_CALLS = 0


# In[29]:


# min max alpha beta
class minmax_alphabeta(object):


    def __init__(self,game):
        self.game = game
        self.bestPlay = list()
        return

    # get a strategy to win the game    
    def minmax(self, game=None, maximizingPlayer=True):
        global GLOBAL_NUM_CALLS
        GLOBAL_NUM_CALLS += 1
        if game == None:
            game = self.game
        if game.final_move() is True:
            self.bestPlay.append(game.board)
            return self.bestPlay, float(game.result())

        else:
            if maximizingPlayer:
                bestval = -np.inf
                for child in game.children():
                    bestPlay, value = self.minmax(child, False)
                    bestval = max(bestval, value)
                return bestPlay, bestval
            else:
                bestval = np.inf
                for child in game.children():
                    bestPlay, value = self.minmax(child, True)
                    bestval = min(bestval, value)
                return bestPlay, bestval

    # get a strategy to win the game
    def alpabeta(self, game=None, a=-np.inf, b=np.inf, maximizingPlayer=True):
        global GLOBAL_NUM_CALLS
        GLOBAL_NUM_CALLS += 1
        if game == None:
            game = self.game
            
        if game.final_move() is True:
            self.bestPlay.append(game.board)
            return self.bestPlay, float(game.result())

        if maximizingPlayer:
            bestval = -np.inf
            for child in game.children():
                bestPlay, value = self.alpabeta(child, a, b, False)
                bestval = max(bestval, value)
                a = max(a, bestval)
                if b <= a:
                    break
            return bestPlay, bestval
        else:
            bestval = np.inf
            for child in game.children():
                bestPlay, value = self.alpabeta(child, a, b, True)
                bestval = min(bestval, value)
                b = min(b, bestval)
                if b <= a:
                    break
            return bestPlay, bestval


# ## Tic Tac Toe Strategy
# Is there a winning strategy for either player in TicTacToa?
# How long can the the loosing player strech the game for?


# In[ ]:


GLOBAL_NUM_CALLS = 0
game = game_TicTacToe()
# This sequence of moves starts the game at this position for faster testing
#  X | O | X
# -----------
#  O | X | O
# -----------
#    |   |
game.move(0,0)
game.move(0,1)
game.move(0,2)
game.move(1,0)
game.move(1,1)
game.move(1,2)
minmax = minmax_alphabeta(game)
bestPlay, res = minmax.minmax()
# Comment out this if you do not wish to see the board sequence for the entire process
print(show_game(bestPlay))
if res == 0:
    print('A perfect game results in a tie')
else:
    print('player '+str(int(-np.sign(res)*1/2 +1.5))+' wins in turn '+str(int(1/res)))
print('There were '+str(GLOBAL_NUM_CALLS)+' calls!')


# In[ ]:


# This runs the minmax algorithm on an empty game board
GLOBAL_NUM_CALLS = 0
minmax = minmax_alphabeta(game_TicTacToe())
bestPlay, res = minmax.alpabeta()
# Comment out this if you do not wish to see the board sequence for the entire process
print(show_game(bestPlay))
if res == 0:
    print('A perfect game results in a tie')
else:
    print('player '+str(int(-np.sign(res)*1/2 +1.5))+' wins in turn '+str(int(1/res)))
print('There were '+str(GLOBAL_NUM_CALLS)+' calls!')






