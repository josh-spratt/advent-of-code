from aoc_helpers.input_reader import AocInputReader
import logging
import re

logger = logging.getLogger(__name__)


def split_product_id_ranges(product_id_data: str) -> list[str]:
    """Take the raw data and create a list of ranges (as strings)"""
    logger.info("Splitting product ID ranges into a list")
    return [x.strip() for x in product_id_data.split(",")]


def build_product_id_list(product_id_range: str) -> list[str]:
    """Take the range and create a list of product ids"""
    starting_point = int(product_id_range.split("-")[0])
    ending_point = int(product_id_range.split("-")[1])
    return [str(x) for x in list(range(starting_point, ending_point + 1))]


def split_product_id_and_check_for_repetition(product_id: str) -> bool:
    """Split the product id string in half and check if it repeats"""
    length = len(product_id)
    mid = length // 2
    front = product_id[: mid + (length % 2)]
    back = product_id[mid + (length % 2) :]
    if front == back:
        return True
    return False


def part1_sum_invalid_ids(product_id_ranges: list[str]) -> int:
    logger.info("Summing invalid product IDs")
    invalid_id_sum = 0
    for product_id_range in product_id_ranges:
        product_id_list = build_product_id_list(product_id_range)
        for product_id in product_id_list:
            if split_product_id_and_check_for_repetition(product_id):
                invalid_id_sum += int(product_id)
    return invalid_id_sum


def part2_sum_invalid_ids(product_id_ranges: list[str]) -> int:
    logger.info("Summing invalid product IDs")
    invalid_id_sum = 0
    for product_id_range in product_id_ranges:
        product_id_list = build_product_id_list(product_id_range)
        for product_id in product_id_list:
            if bool(re.fullmatch(r"(.+)\1+", product_id)):
                invalid_id_sum += int(product_id)
    return invalid_id_sum


def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s.%(msecs)03d %(levelname)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    input_reader = AocInputReader("2025/day02/input.txt")
    input_str = input_reader.read_input_to_str()
    product_id_ranges = split_product_id_ranges(input_str)
    part1_invalid_id_sum = part1_sum_invalid_ids(product_id_ranges)
    logger.info("Part 1 Solution -- The sum of invalid IDs is %s", part1_invalid_id_sum)
    part2_invalid_id_sum = part2_sum_invalid_ids(product_id_ranges)
    logger.info("Part 2 Solution -- The sum of invalid IDs is %s", part2_invalid_id_sum)


if __name__ == "__main__":
    main()
