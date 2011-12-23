class Piece(object):
    colours = { 'white': 0x2654, 'black': 0x265a }

    def __init__(self, colour):
        self.colour = colour

    def __unicode__(self):
        colour_offset = self.__class__.colours[self.colour]
        unicode_point = colour_offset + self.__class__.offset
        return unichr(unicode_point)

class King(Piece):
    offset = 0

class Queen(Piece):
    offset = 1

class Rook(Piece):
    offset = 2

class Bishop(Piece):
    offset = 3

class Knight(Piece):
    offset = 4

class Pawn(Piece):
    offset = 5
