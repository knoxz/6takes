pieces_template = [[[1]],  # 1
                   [[1, 1]],  # 2
                   [[1, 1, 1]],  # 3
                   [[1, 0],  # 4
                    [1, 1]],
                   [[1, 1],  # 5
                    [1, 1]],
                   [[1, 1, 0],  # 6
                    [0, 1, 1]],
                   [[0, 1, 0],  # 7
                    [1, 1, 1]],
                   [[1, 0, 0],  # 8
                    [1, 1, 1]],
                   [[1, 1, 1, 1]],  # 9
                   [[1, 1, 0],  # 10
                    [1, 1, 1]],
                   [[1, 0, 1],  # 11
                    [1, 1, 1]],
                   [[1, 1, 0],  # 12
                    [1, 1, 1]],
                   [[1, 0, 0, 0],  # 13
                    [1, 1, 1, 1]],
                   [[0, 1, 0, 0],  # 14
                    [1, 1, 1, 1]],
                   [[0, 1, 1, 1],  # 15
                    [1, 1, 0, 0]],
                   [[0, 1, 0],  # 16
                    [1, 1, 1],
                    [0, 1, 0]],
                   [[1, 0, 0],  # 17
                    [1, 0, 0],
                    [1, 1, 1]],
                   [[0, 0, 1],  # 18
                    [1, 1, 1],
                    [1, 0, 0]],
                   [[0, 0, 1],  # 19
                    [0, 1, 1],
                    [1, 1, 0]],
                   [[0, 1, 0],  # 20
                    [0, 1, 1],
                    [1, 1, 0]],
                   [[1, 1, 1, 1, 1]]]  # 21


def count_ones(matrix):
    count = 0
    for row in matrix:
        for element in row:
            if element == 1:
                count += 1
    return count


class Piece:
    def __init__(self, cells, size, color):
        self.cells = cells
        self.size = size
        self.color = color

    def rotate_90_degrees_clockwise(self):
        self.cells = [list(reversed(row)) for row in zip(*self.cells)]

    def print_piece(self):
        for row in self.cells:
            print(" ".join("X" if cell else "." for cell in row))
        print("")

    def print_all_rotations(self):
        self.print_piece()
        self.rotate_90_degrees_clockwise()
        self.print_piece()
        self.rotate_90_degrees_clockwise()
        self.print_piece()
        self.rotate_90_degrees_clockwise()
        self.print_piece()
        self.rotate_90_degrees_clockwise()

    def __repr__(self):
        return f"Piece(cells={self.cells}, size={self.size}, color={self.color})"

    @staticmethod
    def generated_pieces(color):
        pieces_list = []
        for piece in pieces_template:
            pieces_list.append(Piece(piece, count_ones(piece), color))
        return pieces_list
