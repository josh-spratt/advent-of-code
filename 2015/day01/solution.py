from aoc_helpers import AocInputReader
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

INPUT_FILE_NAME = "input.txt"


def part1_calculate_end_floor(floor_directions: str) -> int:
    current_floor = 0
    for direction in floor_directions:
        if direction == "(":
            current_floor +=1
        elif direction == ")":
            current_floor -=1
    return current_floor


def part2_identify_basement_position(floor_directions: str) -> int:
    current_floor = 0
    for idx, direction in enumerate(floor_directions):
        if direction == "(":
            current_floor +=1
        elif direction == ")":
            current_floor -=1

        if current_floor < 0:
            return idx + 1


def main() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s.%(msecs)03d %(levelname)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    filepath = Path(__file__).resolve()
    year = filepath.parent.parent.name
    day = filepath.parent.name

    input_reader = AocInputReader(Path(year, day, INPUT_FILE_NAME))
    floor_directions = input_reader.read_input_to_str()
    
    part_1 = part1_calculate_end_floor(floor_directions)
    logger.info("Part 1 -- Floor %d", part_1)

    part2 = part2_identify_basement_position(floor_directions)
    logger.info("Part 2 -- Position %d", part2)


if __name__ == "__main__":
    main()
