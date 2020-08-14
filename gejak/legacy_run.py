import BoardState as b
import cProfile

pr = cProfile.Profile()
pr.enable()

board = b.BoardState(7)
for i in board.run():
    pass

pr.print_stats(sort='tottime')

pr.disable()

for i in range(5):
    input()
