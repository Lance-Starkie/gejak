from outStorage import *
import boardHandler as bhdlr

def display_v1(board):
    print()
    print()
    print('  '+' '.join([c for c in ALPHAB[:len(board)]]))
    flip = list(zip(*board))
    size = range(len(flip))
    for row in size:
        buffer = str(size[row]+1)+' '

        buffer += ' '.join(["camX-OMAC"[tile+4] for tile in flip[row]])
        print(buffer)

    print('  '+' '.join(['#*! '[min(3,col.count(0))] for col in board]))

    counts = bhdlr.tile_count(board)

    print(
    {
    '-inf':(f"Black {-counts[0]} to white {counts[1]}."),
    'inf':(f"White {counts[1]} to black {-counts[0]}."),
    "nan":(f"Tied at {counts[1]}.")
    }[str(sum(counts)*float('inf'))]
    )


def to_alg_format(move):
    '''Converts move to algebraic form and returns it.'''
    if move == float('inf'):

        return "nothing"

    elif move[0] == 0:

        return "nothing"

    if move[0] == "Ret":

        return "Ret"

    return (TYPES2[move[0]]

    +ALPHAB[move[1][0]]
    +str(move[1][1]+1)
    )

def alg_input(in_str):
    '''Converts algebraic input to move.'''
    #Cleans input
    if not type(in_str) == str: return False
    if not len(in_str) in (2,3): return False

    #Determines Archer/Piece, also handles retreat input.
    if len(in_str) == 3:
        if in_str == "Ret":

            return ("Ret",(0,0))

        piece = in_str[0]
        in_str = in_str[1:3]

    else:
        piece = ""

    piece = {v: k for k, v in TYPES2.items()}[piece]

    #Cleans coordinate input
    if not in_str[0] in ALPHAB: return False
    if not in_str[1].isnumeric(): return False

    #Determines coordinates:
    tile = (
        ALPHAB.index(in_str[0]),
        abs(int(in_str[1])-1)
    )

    return (piece,tile)
