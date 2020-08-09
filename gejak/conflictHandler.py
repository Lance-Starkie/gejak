def mark_column(column, conflict_out = False):
    chunks = [[]]

    for tile in [1]+column+[-1]:
        if tile == 0 or 0 in chunks[-1]:
            chunks.append([tile])
        else:
            chunks[-1].append(tile)

    tile_row = -1
    clear = []

    for chunk in chunks:
        old = 0
        conflict = 0
        start = tile_row + 1

        for tile in chunk:
            tile_row += 1
            if tile*float('inf')!=old:
                conflict += 1
            old = tile*float('inf')

        if conflict > 2:
            clear.extend(list(range(start,tile_row-1)))

    return clear

def clear_column(column):
    counts = [sum([column.count(-i) for i in range(1,5)]),
              sum([column.count(i) for i in range(1,5)])]

    if not 0 in counts:
        clear = mark_column(column)

    else: clear = []
    decount = 0

    if len(clear) == 0:

        return (column,0)

    for i in clear:
        column[i] = 0
        decount += 1

    return (column,decount)

#print(clear_column([0,0,0,0,0,0,0,-4,1]))
