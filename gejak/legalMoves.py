from outStorage import *
from collections import deque

def get_legal_moves(board,turn):
    '''Returns all legal moves'''
    legal_moves = deque([])
    legal_tiles = deque([])
    unique_tiles = deque([])
    archers = set([])

    #finding all fully and partially legal tiles, cols are supposed to be cols
    for col_i, col in enumerate(board[1:-1],start = 1):
        for tile_i, tile in enumerate(col):
            if tile == 0:
                if turn in col:
                    legal_tiles.append((col_i,tile_i))
                else:
                    unique_tiles.append((col_i,tile_i))
            if tile*turn >= 2:
                unique_tiles.append((col_i,tile_i))

    #finding all available archer pieces
    for type in list(TYPES.items())[1:]:
        if not any([((type[1]+1)*turn in i) for i in board]):
            archers.add(type[0])

    #generating all legal moves
    for tile in legal_tiles+unique_tiles:
        if not tile in unique_tiles:
            legal_moves.append(('Stone',tile))
        else:
            legal_moves.appendleft(('Stone',tile))
        for archer in archers:
            if not tile in unique_tiles:
                legal_moves.appendleft((archer,tile))

    #and this one generates retreat
    if len(archers) != 3:
        legal_moves.appendleft(('Ret',(0,0)))

    return(legal_moves)
