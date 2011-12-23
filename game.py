from board import Board
from google.appengine.ext import db
import logging
import re, pickle
import errors
import copy

class Game(db.Model):
    black_email = db.StringProperty(required=True)
    white_email = db.StringProperty(required=True)
    whose_go = db.StringProperty(required=True)
    pickled_board = db.BlobProperty()
    pickled_last_board = db.BlobProperty()
    history = db.StringListProperty()

    next_go = {'white' : 'black', 'black': 'white'}

    def whose_go_email(self):
        return getattr(self, self.whose_go + '_email')

    def other_email(self):
        return getattr(self, self.__class__.next_go[self.whose_go] + '_email')

    def __init__(self, *args, **kwargs):
        db.Model.__init__(self, *args, **kwargs)

        if self.pickled_board:
            self.board = pickle.loads(self.pickled_board)
            self.last_board = pickle.loads(self.pickled_last_board)
        else:
            self.board = Board()
            self.board.setup_initial_board()
            self.last_board = self.board

    def put(self, *args, **kwargs):
        self.pickled_board = pickle.dumps(self.board)
        self.pickled_last_board = pickle.dumps(self.last_board)

        db.Model.put(self, *args, **kwargs)

    def do_move(self, move):
        move = move.lower()
        logging.debug(move)

        if 'undo' in move:
            self.history.append(move)
            self.board = self.last_board
            self.whose_go = Game.next_go[self.whose_go]

            raise errors.Undo

        match = re.search(r'([a-h][1-8]) ?to ?([a-h][1-8])', move)

        if match:
            matches = match.groups()
            _from = matches[0]
            to = matches[1]

            piece_taken = self.piece_at(to)
            if piece_taken:
                move = move + " (takes %s)" % unicode(piece_taken)
            self.history.append(move)

            self.last_board = copy.deepcopy(self.board)
            self.move_from(_from, to)

            self.whose_go = Game.next_go[self.whose_go]
        else:
            raise errors.InvalidMove

    def piece_at(self, at):
        x, y = self.coords_from_alphanumeric(at)

        return self.board[x][y]

    def move_from(self, _from, to):
        from_x, from_y = self.coords_from_alphanumeric(_from)
        to_x, to_y = self.coords_from_alphanumeric(to)

        self.board[to_x][to_y] = self.board[from_x][from_y]
        self.board[from_x][from_y] = None

    def coords_from_alphanumeric(self, alpha):
        return (int(alpha[1]) - 1, ord(alpha[0]) - 97)
