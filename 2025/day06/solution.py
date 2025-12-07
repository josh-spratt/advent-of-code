from aoc_helpers.input_reader import AocInputReader
import logging
import math

logger = logging.getLogger(__name__)


def parse_grid(lines):
    """Converts input lines into a grid with uniform width by padding with spaces."""
    if not lines:
        return [], 0, 0
    height = len(lines)
    width = max(len(line) for line in lines)
    return [line.ljust(width) for line in lines], height, width


def find_problem_column_groups(grid, width, height):
    """
    Scans the grid to identify groups of columns that form a single math problem.
    Problems are separated by one or more fully blank columns.
    """
    if width == 0:
        return []

    problem_groups = []
    current_group = []

    for col_idx in range(width):
        is_blank = all(grid[row][col_idx] == " " for row in range(height))
        if is_blank:
            if current_group:
                problem_groups.append(current_group)
                current_group = []
        else:
            current_group.append(col_idx)

    if current_group:
        problem_groups.append(current_group)

    return problem_groups


def get_numbers_part1(grid, column_group, height):
    """
    Part 1: Extracts numbers from horizontal text. Numbers are space-separated
    within each row of the problem's area.
    """
    numbers = []
    if not column_group:
        return numbers

    start_col, end_col = column_group[0], column_group[-1]
    for row_idx in range(height - 1):  # Exclude operator row
        line_slice = grid[row_idx][start_col : end_col + 1]
        numbers.extend(int(n) for n in line_slice.split())
    return numbers


def get_numbers_part2(grid, column_group, height):
    """
    Part 2: Extracts numbers from vertical digits. Each column in the problem
    area represents a single number.
    """
    numbers = []
    for col_idx in column_group:
        digits = "".join(
            grid[row_idx][col_idx]
            for row_idx in range(height - 1)
            if grid[row_idx][col_idx].isdigit()
        )
        if digits:
            numbers.append(int(digits))
    return numbers


def get_operator(grid, column_group, height):
    """Finds the operator (+ or *) in the last row of a problem's column group."""
    if not column_group:
        return None

    start_col, end_col = column_group[0], column_group[-1]
    operator_row = grid[height - 1][start_col : end_col + 1]
    operator = operator_row.strip() or None
    return operator


def calculate(operator, numbers):
    """Applies the operator to a list of numbers."""
    if operator == "+":
        result = sum(numbers)
        return result
    if operator == "*":
        result = math.prod(numbers)
        return result
    return 0


def solve(lines, part):
    """
    A unified solver for both parts. It parses the input into problems and then
    applies the appropriate number-extraction strategy for the specified part.
    """
    grid, height, width = parse_grid(lines)
    problem_column_groups = find_problem_column_groups(grid, width, height)

    number_extractor = get_numbers_part1 if part == 1 else get_numbers_part2

    grand_total = 0
    for group in problem_column_groups:
        operator = get_operator(grid, group, height)
        numbers = number_extractor(grid, group, height)
        if operator and numbers:
            result = calculate(operator, numbers)
            grand_total += result
    return grand_total


def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s.%(msecs)03d %(levelname)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    aoc_input_reader = AocInputReader("2025/day06/input.txt")
    lines = aoc_input_reader.read_input_to_str().splitlines()

    # Part 1
    grand_total_part1 = solve(lines, part=1)
    logger.info("Part 1 Solution -- Grand total: %d", grand_total_part1)

    # Part 2
    grand_total_part2 = solve(lines, part=2)
    logger.info("Part 2 Solution -- Grand total: %d", grand_total_part2)


if __name__ == "__main__":
    main()
