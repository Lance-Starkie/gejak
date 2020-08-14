from outStorage import *
import minimax as mmx
import conflictHandler as chdlr
import legalMoves as glm
import random as ran
from jsonCopy import jcopy

def update_square(board,square,id = 0):
    if square:
        board[square[0]][square[1]] = id
        board[square[0]], decount = chdlr.clear_column(board[square[0]])
        if decount > 0 and abs(id) == 1:
            board[square[0]][square[1]] = (1,id,-1)[(
                int(square[1] > ((len(board)-1)/2.0))
                +int(square[1]>=((len(board)-1)/2.0))
                )]
            board[square[0]], decount = chdlr.clear_column(board[square[0]])
        elif decount > 0:
            board[square[0]][square[1]] = id
            board[square[0]], decount = chdlr.clear_column(board[square[0]])

def do_archer_stones(board,square,archer,turn):
    '''Places stones resulting from placing an archer.'''
    vectors = (
    (),
    ((-1,0),(1,0)),
    ((-1,turn),(1,turn)),
    ((-1,-turn),(1,-turn))
    )[TYPES[archer]]

    for vector in vectors:
        update_square(board,line_of_sight(board,square,vector),turn)

def do_move(board,move,turn,board_hist):
    '''Places peices and clears board for an entire move.'''

    if not end_check(board,board_hist):
        if move[0] == "Ret":
            retreat(board,turn)
            board_hist = hist_append(board,board_hist)
        else:
            do_archer_stones(board,move[1],move[0],turn)
            tile_index = int(any([((TYPES[move[0]]+1)*turn in col) for col in board]))
            update_square(board,move[1],(turn*(TYPES[move[0]]+1),turn)[tile_index])
            board_hist = hist_append(board,board_hist)

def line_of_sight(board,square,vector):
    '''Return location of last occurance of an empty square before first non-empty square starting from the first empty square.'''

    out_square = (square[0],square[1])
    i_square = out_square
    value = board[out_square[0]][out_square[1]]

    while (
        all([i_square[n] in range(len(board)) for n in range(2)])
        and (value == 0)
    ):
        value = board[i_square[0]][i_square[1]]
        if value == 0: out_square = i_square
        i_square = [sum(operands) for operands in zip(i_square,vector)]

    if out_square == (square[0],square[1]): return ()

    return out_square

def end_check(board,board_hist):
    locked_counts = [0,0]
    full = len(board)-2

    for col in board[1:-1]:
        if col.count(0) > 1: full-=1
        if not 0 in col:
            locked_counts[0] += sum([col.count(-i) for i in range(1,5)])
            locked_counts[1] += sum([col.count(i) for i in range(1,5)])

    if not 0 in board[1] or board[2]:
        locked_counts[0] += sum([board[1].count(-i) for i in range(1,5)])
        locked_counts[1] += sum([board[1].count(i) for i in range(1,5)])

    if not 0 in board[-1] or board[-2]:
        locked_counts[0] += sum([board[-1].count(-i) for i in range(1,5)])
        locked_counts[1] += sum([board[-1].count(i) for i in range(1,5)])


    if max(locked_counts)>int((len(board)**2)/2.0):

        return True

    if full >= len(board)-2-round(len(board)/4.0):

        return True

    #Checks for repeated moves to end game.
    for i in range(2,5):
        if len(board_hist) > i*2:
            if all(
            [board_hist[-(j+i)] == board_hist[-j] for j in range(1,i+1)]
            ):

                return True

    return False

def tile_count(board):
    counts = [0,0]

    for column in board:
        counts[0] -= sum([column.count(-i) for i in range(1,5)])
        counts[1] += sum([column.count(i) for i in range(1,5)])

    return counts

def board_eval(board,board_hist, monte = False):
    '''Gives evaluation of board.'''

    #Checks for endstate to return non-infinite evaluation.
    e = 0
    if monte:
        f = monte_carlo_eval(board,board_hist,5)

    if end_check(board,board_hist):

        e = sum(tile_count(board))*30

    counts = [0,0]

    for column in board:
        if 0 in column:
            if column.count(0) == 1 and len(column)>((([1]+column+[-1])[::-1].index(-1))+([1]+column+[-1]).index(1)):
                counts[0] -= 3*sum([column.count(-i) for i in range(1,5)])
                counts[1] += 3*sum([column.count(i) for i in range(1,5)])
            else:
                counts[0] -= column.count(-1)
                counts[1] += column.count(1)
        else:
            counts[0] -= 3*sum([column.count(-i) for i in range(1,5)])
            counts[1] += 3*sum([column.count(i) for i in range(1,5)])
        if 1 in column:
            counts[0] -= int(2*column.count(0))/len(board)
            counts[1] += int(2*column.count(0))/len(board)
        if -1 in column:
            counts[0] -= int(2*column.count(0))/len(board)
            counts[1] += int(2*column.count(0))/len(board)

    if monte:

        return ((sum(counts)+f)/2.0)+e

    return sum(counts)+e

def hist_append(board,board_hist):
    board_hist.append([])
    for col in board:
        board_hist[-1].extend(col)

    return board_hist

def partial_minimax(board,board_hist,turn,sampling = 0.9):
    '''Returns score based on partially sampled minimax'''

    return float(mmx.minimax(board,turn,board_hist,float('inf'),sample = sampling))

def monte_carlo_eval(board,board_hist,n):
    '''Runs Monte Carlo on gamestate n times and scores based on result'''
    total = 0

    for i in range(n):
        new_board_hist, new_board = jcopy((board_hist,board))

        for i in range(20):
            moves = glm.get_legal_moves(board,(len(board_hist)%2)*-2+1)
            move = ran.choice(moves)

            do_move(new_board,move,(len(board_hist)%2)*-2+1,new_board_hist)

            if end_check(new_board,new_board_hist):
                total += sum(tile_count(new_board))
                break

    return total/float(n)

def retreat(board,turn):

    for col in range(len(board)):
        for tile in range(len(board[col])):
            if int(board[col][tile]*turn) in range(2,5):
                board[col][tile] = 0
