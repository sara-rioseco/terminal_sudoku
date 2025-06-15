import time
from copy import deepcopy
from src import SudokuGenerator


MAGENTA = '\033[35m'
RESET = '\033[0m'
RED = '\033[31m'
GREEN = '\033[32m'


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
    print(MAGENTA + "======== Terminal‑Sudoku ========" + RESET)
    print("Welcome to Terminal Sudoku!\nFill the 9×9 board so each row,\ncolumn, and 3×3 box contains 1–9.\n")

def choose_difficulty() -> str:
    while True:
        level = input("Select difficulty (easy/medium/hard): ").strip().lower()
        if level in ['easy','medium','hard']:
            return level
        print("Invalid choice — please enter easy, medium, or hard.")

def is_correct(solution, x, y, n):
    return solution[y][x] == n

def is_empty(puzzle, x, y):
    return puzzle[y][x] == 0

def find_sample_cell(grid):
    for y in range(9):
        for x in range(9):
            if not is_empty(grid, x, y):
                return x, y, grid[y][x]
    return None

def print_board(board):
    # Column headers with extra spaces after 2 and 5
    print()
    header = MAGENTA + ""
    for x in range(9):
        header += MAGENTA + f"{x} " + RESET
        if x in (2, 5):
            header += "  "
    print("        " + header.strip() + RESET)

    for y, row in enumerate(board):
        line = ""
        for x, val in enumerate(row):
            ch = str(val) if val != 0 else '.'
            line += ch + " "
            if x in (2, 5):
                line += MAGENTA + "| " + RESET  # block divider with space

        print(MAGENTA + f"     {y}  "+ RESET + line.rstrip())
        if y in (2, 5):
            print("        " + MAGENTA + "- " * 11 + RESET)
    print()


def play_loop(puzzle, solution, difficulty, start_time):
    grid = deepcopy(puzzle)
    while any(0 in row for row in grid):
        print_board(grid)
        sample = find_sample_cell(grid)
        prompt = "Enter x coordinate, y coordinate,and number\nseparated by a space (e.g. 3 4 9): "
        if sample:
            sample_x, sample_y, sample_value = sample
            prompt = f'Enter x coordinate, y coordinate,and number\nseparated by a space (e.g. {sample_x} {sample_y} {sample_value}): '
        try:
            inp = input(prompt)
            x_str, y_str, n_str = inp.strip().split()
            x, y, n = map(int, (x_str, y_str, n_str))
        except ValueError:
            print(RED + "Invalid input format. Try: x y number" + RESET)
            continue

        if not (0 <= x < 9 and 0 <= y < 9 and 1 <= n <= 9):
            print(RED + "Coordinates or number out of range (0–8 for x,y; 1–9 for number)." + RESET)
            continue
        if puzzle[y][x] != 0:
            print(RED + "That cell is fixed from the puzzle—choose an empty cell." + RESET)
            continue
        if not is_correct(solution, x, y, n):
            print(RED + "Incorrect number for this position." + RESET)
            continue

        grid[y][x] = n

    elapsed = int(time.time() - start_time)
    minutes = elapsed // 60
    seconds = elapsed % 60
    print_board(grid)
    print(GREEN + f"You won the level {difficulty} Sudoku in {minutes} minutes and {seconds} seconds. Congratulations!" + RESET)
    print()

def play_again_prompt() -> bool:
    choice = input("Play again? (y/n): ").strip().lower()
    print()
    return choice.startswith('y')


if __name__ == "__main__":
    play_sudoku()