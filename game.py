from board import Board
from google.appengine.ext import db
import logging
import re, pickle
import errors

class Game(db.Model):
    black_email = db.StringProperty(required=True)
    white_email = db.StringProperty(required=True)
    whose_go = db.StringProperty(required=True)
    pickled_board = db.BlobProperty()

    next_go = {'white' : 'black', 'black': 'white'}

    def whose_go_email(self):
        return getattr(self, self.whose_go + '_email')

    def other_email(self):
        return getattr(self, self.__class__.next_go[self.whose_go] + '_email')

    def __init__(self, *args, **kwargs):
        db.Model.__init__(self, *args, **kwargs)

        if self.pickled_board:
            self.board = pickle.loads(self.pickled_board)
        else:
            self.board = Board()
            self.board.setup_initial_board()

    def put(self, *args, **kwargs):
        self.pickled_board = pickle.dumps(self.board)

        db.Model.put(self, *args, **kwargs)

    def do_move(self, move):
        move = move.lower()
        logging.debug(move)
        match = re.search(r'([a-h][1-8]) ?to ?([a-h][1-8])', move)

        if match:
            matches = match.groups()
            _from = matches[0]
            to = matches[1]
            self.move_from(_from, to)

            self.whose_go = Game.next_go[self.whose_go]
        else:
            raise errors.InvalidMove

    def move_from(self, _from, to):
        from_x, from_y = self.coords_from_alphanumeric(_from)
        to_x, to_y = self.coords_from_alphanumeric(to)

        self.board[from_x][from_y], self.board[to_x][to_y] = None, self.board[from_x][from_y]

    def coords_from_alphanumeric(self, alpha):
        return (int(alpha[1]) - 1, ord(alpha[0]) - 97)
