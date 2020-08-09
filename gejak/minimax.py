import boardHandler as bhdlr
import legalMoves as glm
import random as ran
from copy import deepcopy

def minimax(board, turn, board_hist, depth, main = False, alpha = -float("inf"), beta = float("inf"), sample = 1.0, advanced = False, focal_moves = None):
    '''Minimax Function'''
    best_move = None
    moves = glm.get_legal_moves(board,turn)

    if focal_moves != None:
        temp_moves = [moves.pop(0) for move in focal_moves[(0,0,1)[turn]] if move in moves]
        temp_moves.extend(moves)
        moves = temp_moves

    if sample != 1.0:
        moves = ran.sample(moves, int(sample*len(moves)))

    if any((
        depth == 0,
        bhdlr.end_check(board,board_hist),
        len(moves) == 0
        )):
        if not advanced:

            return (bhdlr.board_eval(board,board_hist),(bhdlr.board_eval(board,board_hist),(0,(0,0))))[main]

        else:

            pmx = bhdlr.partial_minimax(board,board_hist,turn,advanced)
            pure_eval = bhdlr.board_eval(board,board_hist,True)

            return ((pmx+pure_eval)/2,((pmx+pure_eval)/2,(0,(0,0))))[main]

    elapsed_moves = 0

    if turn == 1:
        value = -float("inf")

        for move in moves:
            new_board_hist = deepcopy(board_hist)
            new_board = deepcopy(board)

            if main:
                for i in range(2,5):
                    if int(elapsed_moves) == int((i-len(moves))/i):
                        print("h"+"m"*i)
            else:
                elapsed_moves += 1

            bhdlr.do_move(new_board,move,turn,new_board_hist)
            eval = float(minimax(new_board,turn*-1,new_board_hist,depth-1,False,alpha,beta,sample**2,advanced,focal_moves))
            if value <= eval:
                best_move = move
                value = eval

            if value >= beta:

                return (value,(value,best_move))[main]

            alpha = max(alpha,value)

    else:
        value = float("inf")

        for move in moves:
            new_board_hist = deepcopy(board_hist)
            new_board = deepcopy(board)

            if main:
                for i in range(2,5):
                    if int(elapsed_moves) == int((i-len(moves))/i):
                        print("h"+"m"*i)
            else:
                elapsed_moves += 1

            bhdlr.do_move(new_board,move,turn,new_board_hist)
            eval = float(minimax(new_board,turn*-1,new_board_hist,depth-1,False,alpha,beta,sample**2,advanced,focal_moves))
            if value >= eval:
                best_move = move
                value = eval

            if value <= alpha:

                return (value,(value,best_move))[main]

            beta = min(beta,value)

    return (value,(value,best_move))[main]
