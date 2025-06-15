import time
from copy import deepcopy

from src import SudokuGenerator

BLACK = '\033[30m'
WHITE = '\033[37m'
MAGENTA = '\033[35m'
RESET = '\033[0m'
RED = '\033[31m'
GREEN = '\033[32m'
YELLOW = '\033[33m'
BLUE = '\033[34m'


def play_sudoku():
    print_title_and_rules()
    while True:
        difficulty = choose_difficulty()
        generator = SudokuGenerator()
        solution = generator.solution
        puzzle = generator.generate(difficulty)
        start_time = time.time()
        play_loop(puzzle, solution, difficulty, start_time)

        if not play_again_prompt():
            break

def print_title_and_rules():
    print("======= Terminal‑Sudoku =======")
    print("Welcome! Fill the 9×9 board so each row, column, and 3×3 box contains 1–9.\n")

def choose_difficulty() -> str:
    while True:
        level = input("Select difficulty (easy/medium/hard): ").strip().lower()
        if level in ['easy','medium','hard']:
            return level
        print("Invalid choice — please enter easy, medium, or hard.")

def is_correct(solution, x, y, n):
    return solution[y][x] == n

def print_board(board):
    # Column headers with extra spaces after 2 and 5
    header = ""
    for x in range(9):
        header += f"{x} "
        if x in (2, 5):
            header += "  "
    print("   " + header.strip())

    for y, row in enumerate(board):
        line = ""
        for x, val in enumerate(row):
            ch = str(val) if val != 0 else '.'
            line += ch + " "
            if x in (2, 5):
                line += "| "  # block divider with space

        print(f"{y}  " + line.rstrip())
        if y in (2, 5):
            print("   " + "- " * 11)


def play_loop(puzzle, solution, difficulty, start_time):
    print(MAGENTA + "This text is magenta" + RESET)
    grid = deepcopy(puzzle)
    while any(0 in row for row in grid):
        print_board(grid)
        try:
            inp = input("Enter x y number (e.g. 3 4 9): ")
            x_str, y_str, n_str = inp.strip().split()
            x, y, n = map(int, (x_str, y_str, n_str))
        except ValueError:
            print("Invalid input format. Try: x y number")
            continue

        if not (0 <= x < 9 and 0 <= y < 9 and 1 <= n <= 9):
            print("Coordinates or number out of range (0–8 for x,y; 1–9 for number).")
            continue
        if puzzle[y][x] != 0:
            print("That cell is fixed from the puzzle—choose an empty cell.")
            continue
        if not is_correct(solution, x, y, n):
            print("Incorrect number for this position.")
            continue

        grid[y][x] = n

    elapsed = int(time.time() - start_time)
    print_board(grid)
    print(f"You won the level {difficulty} Sudoku in {elapsed} seconds. Congratulations!")

def play_again_prompt() -> bool:
    choice = input("Play again? (y/n): ").strip().lower()
    return choice.startswith('y')

if __name__ == "__main__":
    play_sudoku()