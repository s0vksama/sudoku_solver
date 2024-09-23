import pygame
import configuration as config
import os
import numpy as np

import imageProcessing as Ip

Board = config.sudoku_board1

def print_board(Board):
    for b in Board:
        print(b)

priority = {}
def possibility_cell(row, col, Board):
    x = list(range(1, 10))
    for k in range(9):
        # Remove numbers from the same column
        if Board[k][col] in x:
            x.remove(Board[k][col])

        # Remove numbers from the same row
        if Board[row][k] in x:
            x.remove(Board[row][k])

    # Identify the top-left corner of the 3x3 subgrid
    top_left_row = 3 * (row // 3)
    top_left_col = 3 * (col // 3)

    # Remove numbers from the 3x3 subgrid
    for r in range(top_left_row, top_left_row + 3):
        for c in range(top_left_col, top_left_col + 3):
            if Board[r][c] in x:
                x.remove(Board[r][c])
    if len(x) == 1:
        return x[0]
    else:
        return x

def possibility_mat(Board, poss_mat):
    for i in range(9):
        for j in range(9):
            if Board[i][j] == 0 or Board[i][j] is not int:
                poss_mat[i][j] = possibility_cell(i, j, Board)

    return poss_mat

poss_mat = Board
print_board(Board)
poss_mat = possibility_mat(Board, poss_mat)

print_board(poss_mat)

