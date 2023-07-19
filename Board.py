import numpy as np
import pandas as pd

class Board:
    def __init__(self, board):
        self.board = np.array(board)
        self.size =  board.shape[0]
        self.square_size = np.sqrt(self.size)
        self.possibilities = []
        [self.possibilities.append([{np.nan}]*self.size) for i in range(0, self.size)]*self.size
        self.range = set(range(1, self.size+1))
        
    def complete(self):
        [self.possibilities.append([{np.nan}]*self.size) for i in range(0, self.size)]*self.size
        for i in range(0, self.size):
            for j in range(0, self.size):
                if np.isnan(self.board[i, j]) == True:
                    row = {self.board[i, x] for x, cell_x in enumerate(self.board[i, :]) if np.isnan(cell_x) == False}
                    column = {self.board[y, j] for y, cell_y in enumerate(self.board[:, j]) if np.isnan(cell_y) == False}
                    square = set()
                    for a in range(int(self.square_size*np.floor(i/self.square_size)), int(self.square_size*np.floor(i/self.square_size)+self.square_size)):
                        for b in range(int(self.square_size*np.floor(j/self.square_size)), int(self.square_size*np.floor(j/self.square_size)+self.square_size)):
                            if np.isnan(self.board[a, b]) == False:
                                square.add(self.board[a, b])
                    possible = self.range - row.union(column.union(square))
                    #print(f'({i}, {j}): possibilities: {possible}')
                    if len(possible) == 0:
                        print(f'Error! Cell ({i}, {j}) has no possible values!')
                        break
                    elif len(possible) == 1:
                        self.board[i, j] = list(possible)[0]
                    else:
                        self.possibilities[i][j] = possible
        return self.board, self.possibilities

    def compare(self):
        for i in range(0, self.size):
            for j in range(0, self.size):
              #  print(f'({i}, {j})')
                if set.issubset((self.possibilities[i][j]), {np.nan}) == False:
                    row = set()
                    column = set()
                    square = set()
                    #[print(poss_x) for x, poss_x in enumerate(self.possibilities[i])]
                    for x, poss_x in enumerate(self.possibilities[i]):
                        if (poss_x != {np.nan} and x != j):
                            row = row.union(poss_x)
                    for y, poss_y in enumerate(self.possibilities[:][j]):
                        if (poss_y != {np.nan} and y != i):
                            column = column.union(poss_y)
                    for a in range(int(self.square_size*np.floor(i/self.square_size)), int(self.square_size*np.floor(i/self.square_size)+self.square_size)):
                        for b in range(int(self.square_size*np.floor(j/self.square_size)), int(self.square_size*np.floor(j/self.square_size)+self.square_size)):
                            if self.possibilities[a][b] != {np.nan}:
                                square = square.union(self.possibilities[a][b])
                    remainder_row = self.possibilities[i][j] - row
                    remainder_column = self.possibilities[i][j] - column
                    remainder_square = self.possibilities[i][j] - square
                    if len(remainder_row) == 1:
                        self.board[i, j] = list(remainder_row)[0]
                        for y in range(0, self.size):
                            self.possibilities[y][j] -= remainder_row
                        for a in range(int(self.square_size*np.floor(i/self.square_size)), int(self.square_size*np.floor(i/self.square_size)+self.square_size)):
                            for b in range(int(self.square_size*np.floor(j/self.square_size)), int(self.square_size*np.floor(j/self.square_size)+self.square_size)):
                                self.possibilities[a][b] -= remainder_row
                    elif len(remainder_column) == 1:
                        self.board[i, j] = list(remainder_column)[0]
                        for x in range(0, self.size):
                            self.possibilities[i][x] -= remainder_column
                        for a in range(int(self.square_size*np.floor(i/self.square_size)), int(self.square_size*np.floor(i/self.square_size)+self.square_size)):
                            for b in range(int(self.square_size*np.floor(j/self.square_size)), int(self.square_size*np.floor(j/self.square_size)+self.square_size)):
                                self.possibilities[a][b] -= remainder_column
                    elif len(remainder_square) == 1:
                        self.board[i, j] = list(remainder_square)[0]
                        for x in range(0, self.size):
                            self.possibilities[i][x] -= remainder_square
                        for y in range(0, self.size):
                            self.possibilities[y][j] -= remainder_square
        return self.board