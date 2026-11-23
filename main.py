import argparse
import random
import sys

from lib import write_grid
from pathlib import Path

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


def write_image(matrix, iteration, output_directory):
    directory = Path(output_directory)
    directory.mkdir(parents=True, exist_ok=True)
    size = max(540, 2 * len(matrix) + 1)
    filename = directory / f"grid_{iteration:04d}.png"
    write_grid(matrix=matrix, filename=filename, size=size)


def fail(message):
    print(f"Error: {message}", file=sys.stderr)
    sys.exit(1)


def parse_matrix(text):
    lines = [line for line in text.splitlines() if line.strip()]
    if not lines:
        fail("la grille est vide")
    try:
        size = int(lines[0])
    except ValueError:
        fail("la première ligne doit contenir la taille de la grille")
    if size <= 0:
        fail("la taille de la grille doit être strictement positive")
    rows = lines[1:]
    if len(rows) != size:
        fail(f"{size} lignes attendues, {len(rows)} reçues")
    matrix = []
    for number, row in enumerate(rows, start=1):
        cells = row.split()
        if len(cells) != size:
            fail(f"ligne {number} : {size} cellules attendues, {len(cells)} reçues")
        for cell in cells:
            if cell not in ("0", "1"):
                fail(f"ligne {number} : cellule invalide '{cell}' (0 ou 1 attendu)")
        matrix.append([int(cell) for cell in cells])
    return matrix


def read_matrix_from_stdin():
    return parse_matrix(sys.stdin.read())




    
def generate_random_matrix(nb_cells, seed):
    rng = random.Random(seed)
    return [
        [rng.choice([0, 1]) for _ in range(nb_cells)]
        for _ in range(nb_cells)
    ]


def format_text(matrix, iteration):
    lines = [f"iteration: {iteration}"]
    lines += [" ".join(str(cell) for cell in row) for row in matrix]
    return "\n".join(lines)


def simulate(matrix, max_iterations, periodic):
    yield 0, matrix
    for iteration in range(1, max_iterations + 1):
        matrix = next_generation(matrix, periodic)
        yield iteration, matrix


def write_images(generations, output_directory):
    count = 0
    for iteration, matrix in generations:
        write_image(matrix, iteration, output_directory)
        count += 1
    return count


def main():
    args = parse_args()
    if sys.stdin.isatty():
        matrix = generate_random_matrix(args.nb_cells, args.seed)
    else:
        matrix = read_matrix_from_stdin()
    generations = simulate(matrix, args.max_iterations, args.periodic)
    if args.output_type == "text":
        for iteration, last_matrix in generations:
            pass
        print(format_text(last_matrix, iteration))
    else:
        try:
            count = write_images(generations, args.output_directory)
        except OSError as error:
            print(f"Erreur : impossible d'écrire dans '{args.output_directory}' ({error})", file=sys.stderr)
            sys.exit(1)
        print(f"Generation of {count} images in directory {args.output_directory}")


if __name__ == "__main__":
    main()