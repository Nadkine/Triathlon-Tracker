from random import randrange
import numpy as np
import sys

board = []
stack = []
length = 8
width = 8
field_horse={'x':0,'y':0}
possibilities=[[1,2],[-1,2],[1,-2],[-1,-2],[2,1],[-2,1],[2,-1],[-2,-1]]

def random_valid_jump(field_horse,stack,board):
    for i in range(len(possibilities)):
        x = field_horse['x'] + possibilities[i][0]
        y = field_horse['y'] + possibilities[i][1]
        if x <= length-1 and x >= 0 and y <= width-1 and y >= 0 and (board[x][y]=="X"):
            new_board = np.copy(board)
            #toevoegen
            new_horse = {'x':x,'y':y}
            new_stack = np.append(stack,new_horse)
            new_board[x][y] = "O"
            #monitor
            if len(new_stack) > 62:
                print(len(new_stack))
                print(new_stack)
            if len(new_stack)==(length*width):
                print("DONE")
                print(new_stack)
                sys.exit()
            #next
            random_valid_jump(new_horse,new_stack,new_board)
    board[field_horse['x'],field_horse['y']] = 'X'
           
def init_board():
    row = []
    for i in range(length):
        for j in range(width):
            row.append("X")
        board.append(row)
        row = []
    board[0][0] = "O"

init_board()
stack.append({'x':0,'y':0})
random_valid_jump(field_horse,stack,board)