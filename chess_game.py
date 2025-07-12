import pygame
from piece import King, Queen, Rook, Bishop, Knight, Pawn 

pygame.init()

class Chess:
    def __init__(self, screen_length=1000):
        self.SCREEN_LENGTH = screen_length # should be multiple of 8
        self.BLOCK_SIZE = self.SCREEN_LENGTH // 8

        self.window = pygame.display.set_mode((self.SCREEN_LENGTH, self.SCREEN_LENGTH))

        pygame.display.set_icon(pygame.image.load('pieces/white_king.png'))  # Set a default icon
        pygame.display.set_caption("Chess")
        self.font = pygame.font.SysFont(None, 32)

        self.selected_pos = None
        self.players_turn = 'white' 

        # load piece images
        self.pieces = {
            'white': {
                'king': pygame.transform.scale(pygame.image.load('pieces/white_king.png'), (self.BLOCK_SIZE, self.BLOCK_SIZE)),
                'queen': pygame.transform.scale(pygame.image.load('pieces/white_queen.png'), (self.BLOCK_SIZE, self.BLOCK_SIZE)),
                'rook': pygame.transform.scale(pygame.image.load('pieces/white_rook.png'), (self.BLOCK_SIZE, self.BLOCK_SIZE)),
                'bishop': pygame.transform.scale(pygame.image.load('pieces/white_bishop.png'), (self.BLOCK_SIZE, self.BLOCK_SIZE)),
                'knight': pygame.transform.scale(pygame.image.load('pieces/white_knight.png'), (self.BLOCK_SIZE, self.BLOCK_SIZE)),
                'pawn': pygame.transform.scale(pygame.image.load('pieces/white_pawn.png'), (self.BLOCK_SIZE, self.BLOCK_SIZE))
            },
            'black': {
                'king': pygame.transform.scale(pygame.image.load('pieces/black_king.png'), (self.BLOCK_SIZE, self.BLOCK_SIZE)),
                'queen': pygame.transform.scale(pygame.image.load('pieces/black_queen.png'), (self.BLOCK_SIZE, self.BLOCK_SIZE)),
                'rook': pygame.transform.scale(pygame.image.load('pieces/black_rook.png'), (self.BLOCK_SIZE, self.BLOCK_SIZE)),
                'bishop': pygame.transform.scale(pygame.image.load('pieces/black_bishop.png'), (self.BLOCK_SIZE, self.BLOCK_SIZE)),
                'knight': pygame.transform.scale(pygame.image.load('pieces/black_knight.png'), (self.BLOCK_SIZE, self.BLOCK_SIZE)),
                'pawn': pygame.transform.scale(pygame.image.load('pieces/black_pawn.png'), (self.BLOCK_SIZE, self.BLOCK_SIZE))
            }
        }

        # setup board state with pieces
        self.board = [[None for _ in range(8)] for _ in range(8)]

        # Initial positions for each piece type
        piece_order = [Rook, Knight, Bishop, Queen, King, Bishop, Knight, Rook]

        for x, PieceClass in enumerate(piece_order):
            self.board[0][x] = PieceClass('black')
            self.board[1][x] = Pawn('black')
            # `None` inbetween
            self.board[6][x] = Pawn('white')
            self.board[7][x] = PieceClass('white')

        # draw board state

        self.draw_board()
        self.draw_pieces()

    def move(self, end_y, end_x):
        if self.selected_pos is not None:

            start_y, start_x = self.selected_pos
            piece = self.board[start_y][start_x]

            if end_y == start_y and end_x == start_x: # not click and drop check
                return
            
            move_type = piece.is_valid_move(self.board, (start_y, start_x), (y, x))
            if move_type == "normal":

                self.board[y][x] = self.board[start_y][start_x]
                self.board[start_y][start_x] = None
                piece.has_moved = True

                self.update_player_turn()   
            elif move_type == "castle_kingside":

                # king movement
                self.board[y][x] = self.board[start_y][start_x]
                self.board[start_y][start_x] = None
                piece.has_moved = True

                # rook movement
                self.board[y][x-1] = self.board[y][x+1]
                self.board[y][x+1] = None
                self.board[y][x-1].has_moved = True

                self.update_player_turn()
            elif move_type == "castle_queenside":

                # king movement
                self.board[y][x] = self.board[start_y][start_x]
                self.board[start_y][start_x] = None
                piece.has_moved = True

                # rook movement
                self.board[y][x+1] = self.board[y][x-2]
                self.board[y][x-2] = None
                self.board[y][x+1].has_moved = True

                self.update_player_turn()

            self.selected_pos = None
            self.draw_board()
            self.draw_pieces()
        else:
            # if piece exists on clicked square and if players_turn matches the color of the piece selected and if piece not already selected
            if self.board[end_y][end_x] is not None and self.players_turn == self.board[end_y][end_x].color:
                self.selected_pos = end_y, end_x
                pygame.draw.rect(self.window, (255, 0, 0), (x * self.BLOCK_SIZE, y * self.BLOCK_SIZE, self.BLOCK_SIZE, self.BLOCK_SIZE), 4)

    def draw_board(self):
        brown = (180, 135, 98)
        white = (255, 255, 255)

        for y in range(0, 8):
            for x in range(0, 8):
                if (x + y) % 2 == 0:
                    color = white
                else:
                    color = brown
                pygame.draw.rect(self.window, color, (x * self.BLOCK_SIZE, y * self.BLOCK_SIZE, self.BLOCK_SIZE, self.BLOCK_SIZE))
    
    def draw_pieces(self):
        for y in range(8):
            for x in range(8):
                piece = self.board[y][x]
                if piece is not None:
                    self.window.blit(self.pieces[piece.color][piece.type], (x * self.BLOCK_SIZE, y * self.BLOCK_SIZE))
    
    def update_player_turn(self):
        if self.players_turn == "white":
            self.players_turn = "black"
        else:
            self.players_turn = "white"


# ------- MANUAL Chess -------

# only execute if chess_game.py file was executed, not if the file is imported
if __name__ == "__main__": 
    env = Chess()
    running = True
    while running:

        # env.draw_board()
        # env.draw_pieces()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                x, y = pos[0] // env.BLOCK_SIZE, pos[1] // env.BLOCK_SIZE
                env.move(y, x)
                # print(f"Clicked on (y, x) format: {y}, {x}")

            elif event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                x, y = pos[0] // env.BLOCK_SIZE, pos[1] // env.BLOCK_SIZE
                env.move(y, x)

        # Square coordinates display
        # pos = pygame.mouse.get_pos()
        # x, y = pos[0], pos[1]
        # x_square, y_square = pos[0] // env.BLOCK_SIZE, pos[1] // env.BLOCK_SIZE
        # text = f"Mouse: ({y_square}, {x_square})"
        # text_surface = env.font.render(text, True, (0, 0, 0))
        # env.window.blit(text_surface, (x, y + 20))

        pygame.display.flip()

    pygame.quit()