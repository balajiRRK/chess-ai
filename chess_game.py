import pygame
from piece import King, Queen, Rook, Bishop, Knight, Pawn 

pygame.init()

class Chess:
    def __init__(self, screen_width=800, screen_height=800, block_size=100):
        self.SCREEN_WIDTH = screen_width
        self.SCREEN_HEIGHT = screen_height
        self.BLOCK_SIZE = block_size

        self.window = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        pygame.display.set_icon(pygame.image.load('pieces/white_king.png'))  # Set a default icon
        pygame.display.set_caption("Chess")

        self.selected_pos = None
        self.players_turn = 'white' 

        # load piece images
        self.pieces = {
            'white': {
                'king': pygame.transform.scale(pygame.image.load('pieces/white_king.png'), (100, 100)),
                'queen': pygame.transform.scale(pygame.image.load('pieces/white_queen.png'), (100, 100)),
                'rook': pygame.transform.scale(pygame.image.load('pieces/white_rook.png'), (100, 100)),
                'bishop': pygame.transform.scale(pygame.image.load('pieces/white_bishop.png'), (100, 100)),
                'knight': pygame.transform.scale(pygame.image.load('pieces/white_knight.png'), (100, 100)),
                'pawn': pygame.transform.scale(pygame.image.load('pieces/white_pawn.png'), (100, 100))
            },
            'black': {
                'king': pygame.transform.scale(pygame.image.load('pieces/black_king.png'), (100, 100)),
                'queen': pygame.transform.scale(pygame.image.load('pieces/black_queen.png'), (100, 100)),
                'rook': pygame.transform.scale(pygame.image.load('pieces/black_rook.png'), (100, 100)),
                'bishop': pygame.transform.scale(pygame.image.load('pieces/black_bishop.png'), (100, 100)),
                'knight': pygame.transform.scale(pygame.image.load('pieces/black_knight.png'), (100, 100)),
                'pawn': pygame.transform.scale(pygame.image.load('pieces/black_pawn.png'), (100, 100))
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


    def select_piece(self, y, x):
        # if piece exists on clicked square and if players_turn matches the color of the piece selected and if piece not already selected
        if self.board[y][x] is not None and self.players_turn == self.board[y][x].color:
            self.selected_pos = y, x
            pygame.draw.rect(self.window, (255, 0, 0), (x * self.BLOCK_SIZE, y * self.BLOCK_SIZE, self.BLOCK_SIZE, self.BLOCK_SIZE), 2)
        return
    
    def drop_piece(self, y, x):
        if self.selected_pos is not None:
            prev_y, prev_x = self.selected_pos
            piece = self.board[prev_y][prev_x]

            if piece.is_valid_move(self.board, (prev_y, prev_x), (y, x)):
                print("valid move")
                if y != prev_y or x != prev_x:
                    self.board[y][x] = self.board[prev_y][prev_x]
                    self.board[prev_y][prev_x] = None
                    piece.has_moved = True
                self.update_player_turn()   

            self.selected_pos = None
            self.draw_board()
            self.draw_pieces()


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
        return
    
    def draw_pieces(self):
        for y in range(8):
            for x in range(8):
                piece = self.board[y][x]
                if piece is not None:
                    self.window.blit(self.pieces[piece.color][piece.type], (x * self.BLOCK_SIZE, y * self.BLOCK_SIZE))
        return   
    
    def update_player_turn(self):
        if self.players_turn == 'white':
            self.players_turn = 'black'
        else:
            self.players_turn = 'white'


# ------- MANUAL Chess -------

# only execute if game_env file was executed, not if the file is imported
if __name__ == "__main__": 
    env = Chess()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                x, y = pos[0] // env.BLOCK_SIZE, pos[1] // env.BLOCK_SIZE
                env.select_piece(y, x)

            elif event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                x, y = pos[0] // env.BLOCK_SIZE, pos[1] // env.BLOCK_SIZE
                env.drop_piece(y, x)

        pygame.display.flip()


    pygame.quit()


