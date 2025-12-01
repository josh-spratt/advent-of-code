from aoc_helpers.input_reader import AocInputReader
import logging

logger = logging.getLogger(__name__)

STARTING_DIAL_POSITION = 50


def convert_input_to_signed_integers(input_data: str) -> list[int]:
    logger.info("Converting raw input data to signed integers")
    input_list = input_data.split()
    instructions = []
    for x in input_list:
        if x.startswith("L"):
            instructions.append(-int(x[1:]))
        else:
            instructions.append(int(x[1:]))
    return instructions


def calculate_number_of_times_dial_points_zero(instructions: list[int]) -> int:
    logger.info("Calculating the number of times the dial ends on a zero")
    dial_position = STARTING_DIAL_POSITION
    zeros = 0
    for instruction in instructions:
        dial_position = (dial_position + instruction) % 100
        if dial_position == 0:
            zeros += 1
    return zeros


def calculate_number_of_times_dial_passes_zero(instructions: list[int]) -> int:
    logger.info("Calculating the number of times the dial passes zero")
    dial_position = STARTING_DIAL_POSITION
    zeros = 0
    for instruction in instructions:
        step = 1 if instruction > 0 else -1
        for _ in range(abs(instruction)):
            dial_position = (dial_position + step) % 100
            if dial_position == 0:
                zeros += 1
    return zeros


def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s.%(msecs)03d %(levelname)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    input_reader = AocInputReader("2025/day01/input.txt")
    input_str = input_reader.read_input_to_str()
    instructions = convert_input_to_signed_integers(input_str)

    part1 = calculate_number_of_times_dial_points_zero(instructions)
    logger.info(
        "Part 1 Solution -- The number of times the dial ends on a zero is %s", part1
    )
    part2 = calculate_number_of_times_dial_passes_zero(instructions)
    logger.info(
        "Part 2 Solution -- The number of times the dial passes zero is %s", part2
    )


if __name__ == "__main__":
    main()
