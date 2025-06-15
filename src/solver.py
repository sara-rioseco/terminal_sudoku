from generator import is_safe


class SudokuSolver:
    def __init__(self, grid: list[list[int]]) -> None:
        if not is_valid_grid(grid):
            raise ValueError("Invalid Sudoku grid provided.")
        self.grid = [row[:] for row in grid]

    def solve(self) -> list[list[int]]:
        if not self._backtrack():
            raise ValueError("Puzzle has no solution.")
        return self.grid

    def _backtrack(self) -> bool:
        for y in range(9):
            for x in range(9):
                if self.grid[y][x] == 0:
                    for num in range(1, 10):
                        if is_safe(self.grid, x, y, num):
                            self.grid[y][x] = num
                            if self._backtrack():
                                return True
                            self.grid[y][x] = 0
                    return False
        return True


def is_valid_grid(grid: list[list[int]]) -> bool:
    # Structure and value checks
    if len(grid) != 9 or any(len(row) != 9 for row in grid):
        return False
    for row in grid:
        if any(not (0 <= val <= 9) for val in row):
            return False

    # Helper to test duplicate absence
    def check_unit(unit):
        nums = [v for v in unit if v != 0]
        return len(nums) == len(set(nums))

    # Check rows and columns
    for i in range(9):
        if not check_unit(grid[i]) or not check_unit([grid[r][i] for r in range(9)]):
            return False

    # Check 3×3 blocks
    for by in range(0, 9, 3):
        for bx in range(0, 9, 3):
            block = [grid[y][x] for y in range(by, by + 3) for x in range(bx, bx + 3)]
            if not check_unit(block):
                return False

    return True
