import argparse
import random

from lib import write_grid

def positive_int(value):
    number = int(value)
    if number <= 0:
        raise argparse.ArgumentTypeError(
            f"{value} doit être un entier strictement positif")
    return number


def non_negative_int(value):
    number = int(value)
    if number < 0:
        raise argparse.ArgumentTypeError(
            f"{value} doit être un entier positif ou nul")
    return number


def parse_args():
    parser = argparse.ArgumentParser(description="Jeu de la vie de Conway")
    parser.add_argument("-n", "--nb_cells", type=positive_int, default=10,
                        help="nombre de cellules par côté (grille aléatoire)")
    parser.add_argument("-m", "--max_iterations", type=non_negative_int,
                        default=20,
                        help="numéro de la dernière itération à calculer")
    parser.add_argument("-s", "--seed", type=int, default=42,
                        help="graine du générateur aléatoire")
    parser.add_argument("-o", "--output_directory", default="outputs",
                        help="dossier de sortie des images")
    parser.add_argument("-t", "--output_type", choices=["image", "text"],
                        default="image",
                        help="type de sortie : image ou text")
    parser.add_argument("-p", "--periodic", action="store_true",
                        help="active les conditions aux limites périodiques")
    return parser.parse_args()

def count_neighbors(matrix, row, col, periodic=False):
    size = len(matrix)
    total = 0
    for d_row in (-1, 0, 1):
        for d_col in (-1, 0, 1):
            if d_row == 0 and d_col == 0:
                continue
            neighbor_row = row + d_row
            neighbor_col = col + d_col
            
            if periodic:
                total += matrix[neighbor_row % size][neighbor_col % size]
            elif 0 <= neighbor_row < size and 0 <= neighbor_col < size:
                total += matrix[neighbor_row][neighbor_col]
    return total

def next_generation(matrix, periodic=False):
    size = len(matrix)
    new_matrix = []
    for row in range(size):
        new_row = []
        for col in range(size):
            neighbors = count_neighbors(matrix, row, col, periodic)
            if matrix[row][col] == 1:
                new_row.append(1 if neighbors in (2, 3) else 0)
            else:
                new_row.append(1 if neighbors == 3 else 0)
        new_matrix.append(new_row)
    return new_matrix

def main():
    nb_cells = 50

    rng = random.Random(4200)

    matrix = [
        [rng.choice([0, 1]) for _ in range(nb_cells)]
        for _ in range(nb_cells)
    ]

    iter = 0
    filename = f"outputs/grid_{iter:04d}.png"
    write_grid(matrix=matrix, filename=filename)

if __name__ == "__main__":
    main()
