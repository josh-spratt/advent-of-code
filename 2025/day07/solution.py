from aoc_helpers.input_reader import AocInputReader
import logging

logger = logging.getLogger(__name__)


def create_tachyon_manifold_diagram(input_text: str) -> list[list[str]]:
    return [[x for x in y] for y in input_text.splitlines()]


def simulate_beam_splitting(grid: list[list[str]]) -> list[list[str]]:
    rows = len(grid)
    columns = len(grid[0]) if grid else 0
    for i in range(rows):
        for j in range(columns):
            try:
                cell_above = grid[i - 1][j]
            except IndexError:
                cell_above = None
            if grid[i][j] == "S":
                grid[i][j] = "|"
            if grid[i][j] == ".":
                if cell_above == "|":
                    grid[i][j] = "|"
                else:
                    grid[i][j] = grid[i][j]
            elif grid[i][j] == "^":
                if cell_above == "|":
                    grid[i][j - 1] = "|"
                    grid[i][j + 1] = "|"
                else:
                    grid[i][j] = grid[i][j]
    return grid


def identify_splits_in_grid(grid: list[list[str]]) -> int:
    split_count = 0
    rows = len(grid)
    columns = len(grid[0]) if grid else 0
    for i in range(1, rows):
        for j in range(columns):
            if grid[i][j] == "^" and grid[i - 1][j] == "|":
                split_count += 1
    return split_count


def find_start_position(grid: list[list[str]]) -> tuple[int, int]:
    """Find the 'S' starting position in the grid."""
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j] == "S":
                return (i, j)
    raise ValueError("No starting position 'S' found in grid")


def simulate_quantum_beam_splitting(grid: list[list[str]]) -> list[list[int]]:
    rows = len(grid)
    columns = len(grid[0]) if grid else 0

    # Create a grid to track the number of timelines passing through each cell
    timeline_counts = [[0 for _ in range(columns)] for _ in range(rows)]

    # Find starting position and initialize with 1 timeline
    start_row, start_col = find_start_position(grid)
    timeline_counts[start_row][start_col] = 1

    # Process row by row, moving timelines downward
    for i in range(rows):
        for j in range(columns):
            current_count = timeline_counts[i][j]
            if current_count == 0:
                continue

            # Move down one row
            next_row = i + 1
            if next_row >= rows:
                continue

            # Check what's at the current position
            if grid[i][j] == "S":
                # Starting position: continue straight down
                timeline_counts[next_row][j] += current_count
            elif grid[i][j] == "^":
                # Splitter: split timelines to left and right
                if j - 1 >= 0:
                    timeline_counts[next_row][j - 1] += current_count
                if j + 1 < columns:
                    timeline_counts[next_row][j + 1] += current_count
            else:
                # Regular cell: continue straight down
                timeline_counts[next_row][j] += current_count

    return timeline_counts


def count_quantum_timelines(grid: list[list[str]]) -> int:
    rows = len(grid)
    columns = len(grid[0]) if grid else 0

    # Simulate the quantum beam splitting
    timeline_counts = simulate_quantum_beam_splitting(grid)

    # Sum up all timelines that exit the bottom of the grid
    total_timelines = sum(timeline_counts[rows - 1][j] for j in range(columns))

    return total_timelines


def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s.%(msecs)03d %(levelname)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    aoc_input_reader = AocInputReader("2025/day07/input.txt")
    input_text = aoc_input_reader.read_input_to_str()

    grid = create_tachyon_manifold_diagram(input_text)
    split_grid = simulate_beam_splitting(grid)
    part1 = identify_splits_in_grid(split_grid)
    logger.info("Part 1 Solution -- Number of splits: %d", part1)

    grid2 = create_tachyon_manifold_diagram(input_text)
    part2 = count_quantum_timelines(grid2)
    logger.info("Part 2 Solution -- Number of timelines: %d", part2)


if __name__ == "__main__":
    main()
