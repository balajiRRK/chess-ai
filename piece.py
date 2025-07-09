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
        super().__init__(color, "king")
        has_moved = False

    def is_valid_move(self, board, start, end):
        dy = abs(start[0] - end[0])
        dx = abs(start[1] - end[1])

        has_obstacle = board[end[0]][end[1]] is not None and board[end[0]][end[1]].color == self.color

        if abs(dx) == 2 and dy == 0:
            return self.can_castle(board, start, end)

        return "normal" if max(dx, dy) == 1 and not has_obstacle else "invalid"
    
    def can_castle(self, board, start, end):
        dx = end[1] - start[1]

        # king should not have moved
        if self.has_moved:
            return "invalid"

        # kingside castle
        if dx > 0:

            # check if theres not a same-color rook on the side we"re castling
            if board[end[0]][end[1]+1].color != self.color or board[end[0]][end[1]+1].type != "rook":
                return "invalid"
            
            if board[end[0]][end[1]+1].has_moved:
                return "invalid"
            
            step_x = 1

            y = start[0]
            x = start[1] + step_x
            while (y, x) != end:
                if board[y][x] is not None:
                    return "invalid"
                x += step_x
                
            return "castle_kingside"
            
        # queenside castle
        elif dx < 0:
            
            # check if theres not a same-color rook on the side we"re castling
            if board[end[0]][end[1]-2].color != self.color or board[end[0]][end[1]-2].type != "rook":
                return "invalid"
            
            if board[end[0]][end[1]-2].has_moved:
                return "invalid"
            
            step_x = -1

            y = start[0]
            x = start[1] + step_x
            while (y, x) != end:
                if board[y][x] is not None:
                    return "invalid"
                x += step_x

            return "castle_queenside"
    
class Queen(Piece):
    def __init__(self, color):
        super().__init__(color, "queen")

    def is_valid_move(self, board, start, end):
        return Rook.is_valid_move(self, board, start, end) or Bishop.is_valid_move(self, board, start, end)

class Rook(Piece):
    def __init__(self, color):
        super().__init__(color, "rook")
        has_moved = False

    def is_valid_move(self, board, start, end):
        dy = end[0] - start[0]
        dx = end[1] - start[1]

        if (dx == 0 and dy == 0) or (dx != 0 and dy != 0):
            return "invalid"
        
        # sign checker
        # 1 - 0 = 1 for positive step direction, 0 - 1 = -1 for negative
        step_y = (dy > 0) - (dy < 0) 
        step_x = (dx > 0) - (dx < 0)

        y = start[0] + step_y
        x = start[1] + step_x

        # check for obstacles up until but not including ending position so rook doesn"t jump over pieces
        while (y, x) != end:
            if board[y][x] is not None:
                return "invalid"
            y += step_y
            x += step_x

        # dont capture own piece
        if board[end[0]][end[1]] is not None and board[end[0]][end[1]].color == self.color:
            return "invalid"
        
        return "normal"

class Bishop(Piece):
    def __init__(self, color):
        super().__init__(color, "bishop")

    def is_valid_move(self, board, start, end):
        dy = end[0] - start[0]
        dx = end[1] - start[1]

        if abs(dy) != abs(dx):
            return "invalid"
        
        step_y = 1 if dy > 0 else -1
        step_x = 1 if dx > 0 else -1

        y = start[0] + step_y
        x = start[1] + step_x

        # check for obstacles up until but not including ending position so bishop doesn"t jump over pieces
        while (y, x) != end: 
            if board[y][x] is not None:
                return "invalid"
            y += step_y
            x += step_x
            
        # dont capture own piece
        if board[end[0]][end[1]] is not None and board[end[0]][end[1]].color == self.color:
            return "invalid"
        
        return "normal"

class Knight(Piece):
    def __init__(self, color):
        super().__init__(color, "knight")

    def is_valid_move(self, board, start, end):
        dy = abs(start[0] - end[0])
        dx = abs(start[1] - end[1])

        # dont capture own piece
        if board[end[0]][end[1]] is not None and board[end[0]][end[1]].color == self.color:
            return "invalid"

        if dy == 1 and dx == 2:
            return "normal"
        elif dy == 2 and dx == 1:
            return "normal"


class Pawn(Piece):
    def __init__(self, color):
        super().__init__(color, "pawn")

    def is_valid_move(self, board, start, end):
        dy = start[0] - end[0]
        if self.color == "black": # black pawns move in opposite direction
            dy = -dy
        dx = abs(start[1] - end[1])

        if dx == 0: # moving vertically
            if board[end[0]][end[1]] is None:
                if not self.has_moved:
                    return "normal" if (dy == 1 or dy == 2) else "invalid"
                else:
                    return "normal" if dy == 1 and dx == 0 else "invalid"
        else: # capturing
            if board[end[0]][end[1]] is not None and board[end[0]][end[1]].color != self.color:
                return "normal" if dy == 1 and dx == 1 else "invalid"