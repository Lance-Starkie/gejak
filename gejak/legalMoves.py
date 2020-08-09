from outStorage import *

def get_legal_moves(board,turn):
    '''Returns all legal moves'''
    legal_moves = []
    legal_tiles = []
    unique_tiles = []
    archers = []

    #finding all fully and partially legal tiles, cols are supposed to be cols
    for col in range(1,len(board)-1):
        for tile in range(len(board[col])):
            if board[col][tile] == 0:
                if turn in board[col]:
                    legal_tiles.append((col,tile))
                else:
                    unique_tiles.append((col,tile))
            if board[col][tile]*turn >= 2:
                unique_tiles.append((col,tile))

    #finding all available archer pieces
    for type in list(TYPES.items())[1:]:
        if not any([((type[1]+1)*turn in i) for i in board]):
            archers.append(type[0])

    #generating all legal moves
    for tile in legal_tiles+unique_tiles:
        if not tile in unique_tiles:
            legal_moves.append(('Stone',tile))
        else:
            legal_moves.insert(0,('Stone',tile))
        for archer in archers:
            if not tile in unique_tiles:
                legal_moves.insert(0,(archer,tile))

    #and this one generates retreat
    if len(archers) != 3:
        legal_moves.insert(0,('Ret',(0,0)))

    return(legal_moves)
