import random
from copy import deepcopy


class SudokuGenerator:

    def __init__(self):
        self.solution = [[0] * 9 for _ in range(9)]
        fill_grid(self.solution)

    def get_cell(self, x: int, y: int) -> int:
        return self.solution[y][x]

    def insert_number(self, x: int, y: int, number: int):
        if not (0 <= x < 9 and 0 <= y < 9):
            raise ValueError(f"Indices x={x}, y={y} must be between 0 and 8.")
        if not (0 <= number <= 9):
            raise ValueError("Number must be between 0 and 9 (0 for empty).")

        self.solution[y][x] = number
        print(f"Inserted {number!r} at position (x={x}, y={y})")

        return self.solution

    def generate(self, difficulty):
        clues = {
            'easy': random.randint(36, 45),
            'medium': random.randint(27, 35),
            'hard': random.randint(19, 26),
        }[difficulty]

        puzzle = deepcopy(self.solution)
        positions = [(x, y) for y in range(9) for x in range(9)]
        random.shuffle(positions)

        for x, y in positions:
            if sum(1 for row in puzzle for v in row if v != 0) <= clues:
                break
            backup = puzzle[y][x]
            puzzle[y][x] = 0
            if solutions_count(deepcopy(puzzle)) != 1:
                puzzle[y][x] = backup

        return puzzle


def fill_grid(grid):
    def solver():
        for y in range(9):
            for x in range(9):
                if grid[y][x] == 0:
                    random.shuffle(nums := list(range(1, 10)))
                    for n in nums:
                        if is_safe(grid, x, y, n):
                            grid[y][x] = n
                            if solver():
                                return True
                    grid[y][x] = 0
                    return False
        return True

    solver()


def is_safe(grid: list[list[int]], x: int, y: int, num: int) -> bool:
    # Check row
    if any(grid[y][col] == num for col in range(9)):
        return False
    # Check column
    if any(grid[row][x] == num for row in range(9)):
        return False
    # Check 3×3 subgrid
    box_x, box_y = (x // 3) * 3, (y // 3) * 3
    for dy in range(3):
        for dx in range(3):
            if grid[box_y + dy][box_x + dx] == num:
                return False
    return True


def solutions_count(grid: list[list[int]], limit: int = 1) -> int:
    def backtrack() -> int:
        for y in range(9):
            for x in range(9):
                if grid[y][x] == 0:
                    count = 0
                    for num in range(1, 10):
                        if is_safe(grid, x, y, num):
                            grid[y][x] = num
                            count += backtrack()
                            if count >= limit:
                                grid[y][x] = 0
                                return count
                    grid[y][x] = 0
                    return count
        # No empty cells → one complete solution
        return 1

    return backtrack()


