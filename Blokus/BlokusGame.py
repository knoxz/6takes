from Blokus.Models.Piece import Piece


def rotate_90_degrees_clockwise(matrix):
    return [list(reversed(row)) for row in zip(*matrix)]


def print_piece(piece):
    for row in piece:
        print(" ".join("X" if cell else "." for cell in row))
    print("")


def print_all_rotations(piece_to_print):
    print_piece(piece_to_print)
    rotated = rotate_90_degrees_clockwise(piece_to_print)
    print_piece(rotated)
    rotated = rotate_90_degrees_clockwise(rotated)
    print_piece(rotated)
    rotated = rotate_90_degrees_clockwise(rotated)
    print_piece(rotated)


# 1 Cell


piece = Piece(piece20, 5, "red")
piece.print_all_rotations()
piece.print_piece()
