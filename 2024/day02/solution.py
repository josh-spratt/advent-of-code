import logging

YEAR = 2024
DAY = 2
INPUT_PATH = "2024/day02/input.txt"

logger = logging.getLogger(__name__)


def read_input(file_path: str) -> list[list[int]]:
    logger.info("Reading input file")
    with open(file_path, "r") as f:
        return [[int(x) for x in line.split()] for line in f if line.strip()]


def check_line_safe(line: list[int]) -> bool:
    """
    - The levels are either all increasing or all decreasing.
    - Any two adjacent levels differ by at least one and at most three.
    """
    increasing = None

    for i in range(len(line)):
        if i < len(line) - 1:
            current_value = line[i]
            next_value = line[i + 1]
            diff = abs(current_value - next_value)
            if diff == 0 or diff > 3:
                return False

            if next_value > current_value:
                if increasing is None:
                    increasing = True
                elif increasing is False:
                    return False
            elif next_value < current_value:
                if increasing is None:
                    increasing = False
                elif increasing is True:
                    return False

    return True


def check_line_safe_with_dampener(line: list[int]) -> bool:
    """
    - The levels are either all increasing or all decreasing.
    - Any two adjacent levels differ by at least one and at most three.
    - Reactor safety systems tolerate a single bad level
    """
    # First check if it's already safe without removing anything
    if check_line_safe(line):
        return True
    
    # Try removing each element one at a time
    for i in range(len(line)):
        modified_line = line[:i] + line[i+1:]
        if check_line_safe(modified_line):
            return True
    
    return False


def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s.%(msecs)03d %(levelname)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    parsed_input = read_input(INPUT_PATH)
    safe_lines = 0
    safe_lines_with_dampener = 0
    logger.info("Checking if lines are safe or unsafe")
    for line in parsed_input:
        is_safe = check_line_safe(line)
        is_safe_dampened = check_line_safe_with_dampener(line)
        if is_safe == True:
            safe_lines += 1
        if is_safe_dampened == True:
            safe_lines_with_dampener += 1
    logger.info("%s safe lines", safe_lines)
    logger.info("%s safe lines with dampener", safe_lines_with_dampener)


if __name__ == "__main__":
    main()
