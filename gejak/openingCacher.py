import json

class Openings:
    def __init__(self):
        self.storage = {}

    def serialize_board(self,board,turn):
        '''Stores board as string.'''

        return (None,'B','W')[turn]+''.join([''.join(["camX-OMAC"[tile+4] for tile in col]) for col in board])

    def get_opening(self,turn,board,rating):
        sboard = self.serialize_board(board,turn)

        if sboard in self.storage:

            return (self.storage[sboard][1] <= rating, self.storage[sboard])

        else:

            return (False, None)

    def store_opening(self,turn,board,rating,move,favor):
        sboard = self.serialize_board(board,turn)

        if sboard in self.storage:
            if self.storage[sboard][1] > rating or (self.storage[sboard][1] == rating and self.storage[sboard][2] < favor):
                self.storage[sboard] = (move,rating,favor)
        else:
            self.storage[sboard] = (move,rating,favor)

    def load_openings(self):
        print("Loading Openings...")
        with open('openings.json', 'r') as f:
            self.storage = json.load(f)

        f.close()
        print("Complete")

    def write_openings(self):
        print("Writing")
        with open('openings.json', 'w') as f:
            json.dump(self.storage, f)

        f.close()
        print("Complete")
