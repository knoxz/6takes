class Board:
    def __init__(self, size):
        self.size = size
        self.board = [[0 for i in range(size)] for j in range(size)]

    def place_piece(self, piece, x, y):
        for i in range(len(piece)):
            for j in range(len(piece[i])):
                if piece[i][j] == 1:
                    self.board[x + i][y + j] = 1

    def is_valid_move(self, piece, x, y, player_id):
        for i in range(len(piece)):
            for j in range(len(piece[i])):
                if piece[i][j] == 1:
                    if x + i >= self.size or y + j >= self.size:
                        return False
                    if self.board[x + i][y + j] == 1:
                        return False
                    if (x + i > 0 and self.board[x + i - 1][y + j] == player_id) or \
                            (y + j > 0 and self.board[x + i][y + j - 1] == player_id) or \
                            (x + i < self.size - 1 and self.board[x + i + 1][y + j] == player_id) or \
                            (y + j < self.size - 1 and self.board[x + i][y + j + 1] == player_id):
                        return False
        for i in range(self.size):
            for j in range(self.size):
                if self.board[i][j] == player_id:
                    if (x > 0 and self.board[x - 1][y] == player_id) or \
                            (y > 0 and self.board[x][y - 1] == player_id) or \
                            (x < self.size - 1 and self.board[x + 1][y] == player_id) or \
                            (y < self.size - 1 and self.board[x][y + 1] == player_id):
                        return True
        return False
