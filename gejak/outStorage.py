import random as ran

TYPES = {
    'Stone':0,
    'Main':1,
    'Advance':2,
    'Close':3
}

TYPES2 = {
    "Stone":"",
    "Main":"M",
    "Advance":"A",
    "Close":"C"
}

ALPHAB = "abcdefghijklmnopqrstuvwxyz"

def rand_type():

    return ran.choice(list(TYPES.items()))[0]
