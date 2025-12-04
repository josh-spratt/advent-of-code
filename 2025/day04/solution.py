from aoc_helpers.input_reader import AocInputReader
import logging

logger = logging.getLogger(__name__)


def create_print_dept_grid(input_data: str) -> list[list[str]]:
    return [[char for char in x] for x in input_data.split()]


def count_neighboring_paper_rolls(grid: list[list[str]], row: int, column: int) -> int:
    directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
    neighboring_rolls = 0
    number_of_rows = len(grid)
    number_of_columns = len(grid[0])
    for row_movement, column_movement in directions:
        neighbor_row, neighbor_column = row + row_movement, column + column_movement
        if (
            neighbor_row >= 0
            and neighbor_row < number_of_rows
            and neighbor_column >= 0
            and neighbor_column < number_of_columns
        ):
            neighbor_value = grid[neighbor_row][neighbor_column]
            if neighbor_value == "@":
                neighboring_rolls += 1
    return neighboring_rolls


def part1_find_all_accessible_rolls(grid: list[list[str]]) -> int:
    accessible_rolls = 0

    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j] != "@":
                continue
            neighboring_rolls = count_neighboring_paper_rolls(grid, i, j)
            if neighboring_rolls <= 3:
                accessible_rolls += 1

    return accessible_rolls


def part2_recursively_remove_accessible_rolls(grid: list[list[str]]) -> int:
    to_remove = []

    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j] != "@":
                continue
            neighboring_rolls = count_neighboring_paper_rolls(grid, i, j)
            if neighboring_rolls <= 3:
                to_remove.append((i, j))

    if not to_remove:
        return 0

    for i, j in to_remove:
        grid[i][j] = "."

    return len(to_remove) + part2_recursively_remove_accessible_rolls(grid)


def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s.%(msecs)03d %(levelname)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    aoc_input_reader = AocInputReader("2025/day04/input.txt")
    input_text = aoc_input_reader.read_input_to_str()
    print_dept_grid = create_print_dept_grid(input_text)
    part1_solution = part1_find_all_accessible_rolls(print_dept_grid)
    logger.info("Part 1 Solution -- Rolls accessible by forklift: %d", part1_solution)

    part2_solution = part2_recursively_remove_accessible_rolls(print_dept_grid)
    logger.info("Part 2 Solution -- Total rolls removed: %d", part2_solution)


if __name__ == "__main__":
    main()
