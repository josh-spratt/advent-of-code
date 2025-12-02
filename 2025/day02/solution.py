from aoc_helpers.input_reader import AocInputReader
import logging

logger = logging.getLogger(__name__)

def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s.%(msecs)03d %(levelname)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    input_reader = AocInputReader("2025/day02/input.txt")
    input_str = input_reader.read_input_to_str()


if __name__ == "__main__":
    main()

