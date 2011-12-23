from piece import Piece, Rook, King, Queen, Pawn, Bishop, Knight

class Board(object):
    def setup_initial_board(self):
        self.table = [ [None for x in range(8)] for y in range(8) ]
        self.setup_colour(reverse=False, colour='black')
        self.setup_colour(reverse=True, colour='white')

    def setup_colour(self, reverse=False, colour='black'):
        royalty, pawns = [7,6] if reverse else [0,1]

        for i, piece in enumerate([Rook, Knight, Bishop, Queen, King, Bishop, Knight, Rook]):
            self.table[royalty][i] = piece(colour=colour)

        self.table[pawns] = [Pawn(colour=colour) for i in range(8)]

    def __getitem__(self, *args):
        return self.table.__getitem__(*args)

    def __setitem__(self, *args):
        return self.table.__setitem__(*args)

    def __unicode__(self):
        line_length = 33
        letters = "    %s  " % "   ".join(chr(i) for i in range(ord('A'), ord('I')))
        header = "  %s  " % ("=" * line_length)
        middle = ''
        for i, row in enumerate(self.table):
            middle += "%s | %s | %s" % (i+1, " | ".join(unicode(cell) if cell else ' ' for cell in row), i+1)
            middle += "\n  %s  \n" % ('-' * line_length)

        return "%s\n%s\n%s%s\n%s" % (letters, header, middle[0:-line_length-5], header, letters)
