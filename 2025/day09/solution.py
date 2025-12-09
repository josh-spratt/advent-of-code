from aoc_helpers.input_reader import AocInputReader
import logging

logger = logging.getLogger(__name__)


def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s.%(msecs)03d %(levelname)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    aoc_input_reader = AocInputReader("2025/day08/input.txt")
    input_text = aoc_input_reader.read_input_to_str()


if __name__ == "__main__":
    main()
