class Piece:
    def __init__(self, color, type):
        self.color = color
        self.type = type
        self.has_moved = False

    # object representation for debugging purposes
    def __repr__(self):
        return f"{self.color.upper()} {self.type.upper()}"
    
    def is_valid_move(self, board, start, end):
        return

class King(Piece):
    def __init__(self, color):
        super().__init__(color, 'king')

    def is_valid_move(self, board, start, end):
        dy = abs(start[0] - end[0])
        dx = abs(start[1] - end[1])

        return max(dx, dy) == 1
    
class Queen(Piece):
    def __init__(self, color):
        super().__init__(color, 'queen')

    def is_valid_move(self, board, start, end):
        return Rook.is_valid_move(self, board, start, end) or Bishop.is_valid_move(self, board, start, end)

class Rook(Piece):
    def __init__(self, color):
        super().__init__(color, 'rook')

    def is_valid_move(self, board, start, end):
        dy = abs(start[0] - end[0])
        dx = abs(start[1] - end[1])

        return True if (dx != 0 and dy == 0) or (dx == 0 and dy != 0) else False

class Bishop(Piece):
    def __init__(self, color):
        super().__init__(color, 'bishop')

    def is_valid_move(self, board, start, end):
        dy = abs(start[0] - end[0])
        dx = abs(start[1] - end[1])

        return True if dy == dx else False

class Knight(Piece):
    def __init__(self, color):
        super().__init__(color, 'knight')

    def is_valid_move(self, board, start, end):
        dy = start[0] - end[0]
        dx = abs(start[1] - end[1])

        return False

class Pawn(Piece):
    def __init__(self, color):
        super().__init__(color, 'pawn')

    def is_valid_move(self, board, start, end):
        dy = start[0] - end[0]
        dx = abs(start[1] - end[1])

        if not self.has_moved:
            return True if (dy == 1 or dy == 2) and dx == 0 else False
        else:
            return True if dy == 1 and dx == 0 else False

    
