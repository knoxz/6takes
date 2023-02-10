class Player:
    def __init__(self, player_id, pieces, score=0):
        self.player_id = player_id
        self.pieces = pieces
        self.score = score

    def add_score(self, score_increment):
        self.score += score_increment

    def get_score(self):
        return self.score

    def get_pieces(self):
        return self.pieces

    def remove_piece(self, piece_index):
        self.pieces.pop(piece_index)
