import numpy as np

def create_board():
    board = np.zeros((8, 8), dtype=str)
    board[1, :] = 'P'
    board[6, :] = 'p'
    board[0, [0, 7]] = board[7, [0, 7]] = 'R'
    board[0, [1, 6]] = board[7, [1, 6]] = 'N'
    board[0, [2, 5]] = board[7, [2, 5]] = 'B'
    board[0, 3] = 'Q'
    board[0, 4] = 'K'
    board[7, 3] = 'q'
    board[7, 4] = 'k'
    return board

board = create_board()
print(board)
class Piece:
    def __init__(self, color):
        self.color = color

    def get_color(self):
        return 'w' if self.color == 'uppercase' else 'b'

class Pawn(Piece):
    def valid_moves(self, position, board):
        row, col = position
        moves = []
        direction = -1 if self.get_color() == 'w' else 1
        # Move forward
        if board[row + direction, col] == '':
            moves.append((row + direction, col))
            # Double move on first move
            if (self.get_color() == 'w' and row == 6) or (self.get_color() == 'b' and row == 1):
                if board[row + 2 * direction, col] == '':
                    moves.append((row + 2 * direction, col))
        # Capture diagonally
        for dc in [-1, 1]:
            if 0 <= col + dc < 8 and board[row + direction, col + dc].islower() if self.get_color() == 'w' else board[row + direction, col + dc].isupper():
                moves.append((row + direction, col + dc))
        return moves

class Rook(Piece):
    def valid_moves(self, position, board):
        moves = []
        row, col = position
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        for dr, dc in directions:
            r, c = row, col
            while 0 <= r + dr < 8 and 0 <= c + dc < 8:
                r += dr
                c += dc
                if board[r, c] == '':
                    moves.append((r, c))
                elif board[r, c].islower() if self.get_color() == 'w' else board[r, c].isupper():
                    moves.append((r, c))
                    break
                else:
                    break
        return moves

class Knight(Piece):
    def valid_moves(self, position, board):
        moves = []
        row, col = position
        directions = [(-2, -1), (-2, 1), (2, -1), (2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2)]
        for dr, dc in directions:
            r, c = row + dr, col + dc
            if 0 <= r < 8 and 0 <= c < 8:
                if board[r, c] == '' or (board[r, c].islower() if self.get_color() == 'w' else board[r, c].isupper()):
                    moves.append((r, c))
        return moves

class Bishop(Piece):
    def valid_moves(self, position, board):
        moves = []
        row, col = position
        directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        for dr, dc in directions:
            r, c = row, col
            while 0 <= r + dr < 8 and 0 <= c + dc < 8:
                r += dr
                c += dc
                if board[r, c] == '':
                    moves.append((r, c))
                elif board[r, c].islower() if self.get_color() == 'w' else board[r, c].isupper():
                    moves.append((r, c))
                    break
                else:
                    break
        return moves

class Queen(Piece):
    def valid_moves(self, position, board):
        return Rook(self.color).valid_moves(position, board) + Bishop(self.color).valid_moves(position, board)

class King(Piece):
    def valid_moves(self, position, board):
        moves = []
        row, col = position
        directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        for dr, dc in directions:
            r, c = row + dr, col + dc
            if 0 <= r < 8 and 0 <= c < 8:
                if board[r, c] == '' or (board[r, c].islower() if self.get_color() == 'w' else board[r, c].isupper()):
                    moves.append((r, c))
        return moves

# Map pieces to their respective classes
piece_classes = {
    'P': Pawn('uppercase'), 'R': Rook('uppercase'), 'N': Knight('uppercase'), 
    'B': Bishop('uppercase'), 'Q': Queen('uppercase'), 'K': King('uppercase'),
    'p': Pawn('lowercase'), 'r': Rook('lowercase'), 'n': Knight('lowercase'), 
    'b': Bishop('lowercase'), 'q': Queen('lowercase'), 'k': King('lowercase')
}
class Game:
    def __init__(self):
        self.board = create_board()
        self.turn = 'w'
        self.pieces = {
            'P': Pawn('uppercase'), 'R': Rook('uppercase'), 'N': Knight('uppercase'), 
            'B': Bishop('uppercase'), 'Q': Queen('uppercase'), 'K': King('uppercase'),
            'p': Pawn('lowercase'), 'r': Rook('lowercase'), 'n': Knight('lowercase'), 
            'b': Bishop('lowercase'), 'q': Queen('lowercase'), 'k': King('lowercase')
        }

    def switch_turn(self):
        self.turn = 'b' if self.turn == 'w' else 'w'
    
    def check_checkmate(self):
        # Implement checkmate logic
        pass

    def get_valid_moves(self, position):
        piece = self.board[position]
        if piece:
            piece_class = self.pieces[piece]
            return piece_class.valid_moves(position, self.board)
        return []

    def move_piece(self, start_pos, end_pos):
        piece = self.board[start_pos]
        if piece and self.is_valid_move(start_pos, end_pos):
            self.board[end_pos] = piece
            self.board[start_pos] = ''
            self.switch_turn()

    def is_valid_move(self, start_pos, end_pos):
        valid_moves = self.get_valid_moves(start_pos)
        return end_pos in valid_moves
import pygame

pygame.init()

screen = pygame.display.set_mode((480, 480))
pygame.display.set_caption('Chess')

def draw_board(screen, board):
    colors = [pygame.Color("white"), pygame.Color("gray")]
    for row in range(8):
        for col in range(8):
            color = colors[(row + col) % 2]
            pygame.draw.rect(screen, color, pygame.Rect(col*60, row*60, 60, 60))
            piece = board[row, col]
            if piece:
                font = pygame.font.Font(None, 74)
                piece_text = font.render(piece, True, pygame.Color("black"))
                screen.blit(piece_text, (col*60 + 15, row*60 + 10))

game = Game()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    draw_board(screen, game.board)
    pygame.display.flip()

pygame.quit()
class Game:
    def __init__(self):
        """
        Initializes the game by setting up the board and the turn.
        """
        self.board = create_board()
        self.turn = 'w'
        self.pieces = {
            'P': Pawn('uppercase'), 'R': Rook('uppercase'), 'N': Knight('uppercase'), 
            'B': Bishop('uppercase'), 'Q': Queen('uppercase'), 'K': King('uppercase'),
            'p': Pawn('lowercase'), 'r': Rook('lowercase'), 'n': Knight('lowercase'), 
            'b': Bishop('lowercase'), 'q': Queen('lowercase'), 'k': King('lowercase')
        }

    def switch_turn(self):
        """
        Switches the turn between players.
        """
        self.turn = 'b' if self.turn == 'w' else 'w'
    
    def check_checkmate(self):
        """
        Checks if the current player is in checkmate.
        """
        pass

    def get_valid_moves(self, position):
        """
        Gets the valid moves for a piece at the given position.

        Parameters:
        position (tuple): The position of the piece on the board.

        Returns:
        list: A list of valid moves.
        """
        piece = self.board[position]
        if piece:
            piece_class = self.pieces[piece]
            return piece_class.valid_moves(position, self.board)
        return []

    def move_piece(self, start_pos, end_pos):
        """
        Moves a piece from start_pos to end_pos if the move is valid.

        Parameters:
        start_pos (tuple): The starting position of the piece.
        end_pos (tuple): The ending position of the piece.
        """
        piece = self.board[start_pos]
        if piece and self.is_valid_move(start_pos, end_pos):
            self.board[end_pos] = piece
            self.board[start_pos] = ''
            self.switch_turn()

    def is_valid_move(self, start_pos, end_pos):
        """
        Checks if a move from start_pos to end_pos is valid.

        Parameters:
        start_pos (tuple): The starting position of the piece.
        end_pos (tuple): The ending position of the piece.

        Returns:
        bool: True if the move is valid, False otherwise.
        """
        valid_moves = self.get_valid_moves(start_pos)
        return end_pos in valid_moves
