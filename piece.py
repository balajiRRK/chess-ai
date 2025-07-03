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
        dy = start[0] - end[0]
        dx = start[1] - end[1]

        print(f"(dy, dx): ({dy}, {dx})")
        print(dy > 0 and dx < 0)
        if abs(dy) == abs(dx):

            has_obstacle = False
            if dy > 0 and dx > 0:
                for i in range(1, dy+1): # inclusive so it doesn't capture same-color pieces
                    print(f"(dy, dx): ({dy}, {dx})")
                    print(f"({start[0] - i}, {start[1] - i})")
                    print(board[start[0] - i][start[1] - i])
                    if board[start[0] - i][start[1] - i] is not None and board[start[0] - i][start[1] - i].color == self.color:
                        has_obstacle = True
                        print("has obstacle")
                        print("")

            elif dy > 0 and dx < 0:
                print("right if branch ran")
                for i in range(1, dy+1):
                    print(f"(dy, dx): ({dy}, {dx})")
                    print(f"({start[0] - i}, {start[1] + i})")
                    print(board[start[0] - i][start[1] + i])
                    if board[start[0] - i][start[1] + i] is not None and board[start[0] - i][start[1] + i].color == self.color:
                        has_obstacle = True
                        print("has obstacle")
                        print("")

            elif dy < 0 and dx < 0:
                for i in range(1, abs(dy)+1):
                    print(f"(dy, dx): ({dy}, {dx})")
                    print(f"({start[0] - i}, {start[1] - i})")
                    print(board[start[0] - i][start[1] - i])
                    if board[start[0] + i][start[1] + i] is not None and board[start[0] + i][start[1] + i].color == self.color:
                        has_obstacle = True
                        print("has obstacle")
                        print("")
            
            elif dy < 0 and dx > 0:
                for i in range(1, abs(dy)+1):
                    print(f"(dy, dx): ({dy}, {dx})")
                    print(f"({start[0] - i}, {start[1] - i})")
                    print(board[start[0] - i][start[1] - i])
                    if board[start[0] + i][start[1] - i] is not None and board[start[0] + i][start[1] - i].color == self.color:
                        has_obstacle = True
                        print("has obstacle")
                        print("")


        return True if abs(dy) == abs(dx) and not has_obstacle else False

class Knight(Piece):
    def __init__(self, color):
        super().__init__(color, 'knight')

    def is_valid_move(self, board, start, end):
        dy = abs(start[0] - end[0])
        dx = abs(start[1] - end[1])

        if dy == 1 and dx == 2:
            return True
        elif dy == 2 and dx == 1:
            return True


class Pawn(Piece):
    def __init__(self, color):
        super().__init__(color, 'pawn')

    def is_valid_move(self, board, start, end):
        dy = start[0] - end[0]
        if self.color == 'black': # black pawns move in opposite direction
            dy = -dy
        dx = abs(start[1] - end[1])

        if dx == 0: # moving vertically
            if board[end[0]][end[1]] is None:
                if not self.has_moved:
                    return True if (dy == 1 or dy == 2) else False
                else:
                    return True if dy == 1 and dx == 0 else False
        else: # capturing
            if board[end[0]][end[1]] is not None:
                return True if dy == 1 and dx == 1 else False