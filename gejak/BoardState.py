import boardHandler as bhdlr
import consoleManager as cons
import legalMoves as glm
import random as ran
import math
from collections import deque
from openingCacher import Openings
from minimax import minimax
from outStorage import *

class BoardState:
    def __init__(self,size):
        self.Board = []
        self.board_hist = []
        self.openings = Openings()
        self.openings.load_openings()
        self.focal_moves = [deque([False for i in range(5)]),deque([False for i in range(5)])]
        for col in range(size):
            self.Board+=[[0,]*size]
        self.turn = 1 #Turns stored as 1 or -1

    def run(self,white_move = 0,black_move = 0,display = cons.display_v1, yield_disp = None):
        if (yield_disp := display(self.Board)) != None: yield yield_disp
        for k in range(5000):
            moves = glm.get_legal_moves(self.Board,self.turn)

            if self.turn == -1:
                self.cpu_move(.55)
                #self.call_move(player_1)
            else:
                self.cpu_move(.55)
                #self.call_move(player_2)
                #player_move()
            self.turn*=-1
            if (yield_disp := display(self.Board)) != None: yield yield_disp

            if bhdlr.end_check(self.Board,self.board_hist):
                end_count = sum(bhdlr.tile_count(self.Board))

                if end_count > 0:
                    print(f"White wins by {end_count} point{('s')*(end_count>1)}!")
                elif end_count < 0:
                    print(f"Black wins by {-end_count} point{('s')*(-end_count>1)}!")
                else:
                    print("Tie Game.")
                break


    def call_move(self,data):
        if data[0] == "cpu":
            self.cpu_move(data[1])
        elif data[0] == "player":
            self.player_move()

    def opening_mining(self,advanced):
        for k in range(4):
            moves = glm.get_legal_moves(self.Board,self.turn)
            self.cpu_move(advanced,novel = True)
            self.turn*=-1

        print("Complete")

    def cpu_move(self,advanced,random = False,depth = 1,novel = False):
        '''Does move using minimax algorithm, stored openings, or randomness.'''
        #loads openings
        if len(self.board_hist) == 0:
            advanced = .5
        if len(self.board_hist) in range(1,5):
            opening = self.openings.get_opening(self.turn,self.Board,math.log(advanced,0.1)+depth)
        else:
            opening = (False,None)

        #uses stored opening move
        if opening[0] and not novel:
            moves = glm.get_legal_moves(self.Board,self.turn)
            move = opening[1][0]
            move_data = [opening[1][1]]

            if not (move[0],tuple(move[1])) in moves:
                print("Data Invalid.")
                move = ran.choice(moves)

        else:
            #includes stored opening move as likely candidate for good move
            if opening[1] != None:
                self.focal_move(opening[1][0])
            move_data = minimax(self.Board, self.turn, self.board_hist, depth, True, advanced = advanced, focal_moves = self.focal_moves)
            self.focal_move(move_data[1])
            move = move_data[1]

            #stores openings
            if len(self.board_hist) in range(1,5):
                self.openings.store_opening(self.turn,self.Board,(math.log(advanced,0.1)+1)/depth,move,move_data[0])
                self.openings.write_openings()
            if random:
                moves = glm.get_legal_moves(self.Board,self.turn)
                move = ran.choice(moves)

        self.process_move(move, favor = move_data[0])

    def player_move(self):
        '''Makes move based on player input'''
        input_passed = False
        moves = glm.get_legal_moves(self.Board,self.turn)

        while not input_passed:
            print("Please give input in algebraic form. (ex. 'd3','Ag4,'Cb1)")
            move = cons.alg_input(input())

            if not move:
                print("Input not valid.")
                print(move)
            else:
                if move in moves:
                    input_passed = True

                else:
                    print("Illegal move.")

        self.process_move(move)

    def process_move(self, move, threat = True, favor = None):

        if favor == None:
            favor, focal = minimax(self.Board,self.turn,self.board_hist,1,True,0.3, focal_moves = self.focal_moves)
            self.focal_move(focal)

        bhdlr.do_move(self.Board,move,self.turn,self.board_hist)
        print((0,"White plays ","Black plays ")[self.turn]+cons.to_alg_format(move))
        if threat:
            threat = minimax(self.Board,self.turn,self.board_hist,2,True,advanced = 0.3, focal_moves = self.focal_moves)[1]

            self.focal_move(threat)
            print(f"threatening {cons.to_alg_format(threat)}.")
        else:
            print(f"{cons.to_alg_format(move)}.")
        if favor:
            if favor>(len(self.Board)/2):
                print(("White favor.","White winning.")[abs(favor)>(len(self.Board)*2)])
            elif favor<-(len(self.Board)/2):
                print(("Black favor.","Black winning.")[abs(favor)>(len(self.Board)*2)])

    def focal_move(self, move):
        self.focal_moves[(0,0,1)[self.turn]].appendleft(move)
        del self.focal_moves[(0,0,1)[self.turn]][-1]
