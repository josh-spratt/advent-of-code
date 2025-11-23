import logging

YEAR = 2024
DAY = 1
INPUT_PATH = "2024/day01/input.txt"

logger = logging.getLogger(__name__)


def read_raw_input_lists(file_path: str) -> list[tuple]:
    """Read raw input file"""
    with open(file_path, "r") as f:
        logger.info("Loaded input data at: %s", INPUT_PATH)
        return [tuple(x.strip().split("   ")) for x in f.readlines()]


def split_and_sort_location_id_lists(location_ids: list[tuple]) -> list[list]:
    """Returns sorted location ID lists"""
    logger.info("Split and sorted Location ID lists")
    return [
        sorted([int(row[0]) for row in location_ids]),
        sorted([int(row[1]) for row in location_ids]),
    ]


def calculate_counts_in_id_list(id_list: list[int]) -> dict:
    counts = {}
    for id in id_list:
        if id in counts.keys():
            counts[id] += 1
        else:
            counts[id] = 1
    return counts


def calculate_ids_difference_sum(location_ids: list[list]) -> int:
    """Loops through location ID lists and returns sum of absolute
    differences between the same index in each list"""
    logger.info("Looping through ID lists to determine absolute differences")
    final_difference_value = 0
    for i in range(len(location_ids[0])):
        absolute_diff = abs(location_ids[0][i] - location_ids[1][i])
        final_difference_value += absolute_diff
    logger.info("Returning a final value after %s iterations", len(location_ids[0]))
    return final_difference_value


def calculate_list_similarity_score(list_a: list, list_b: dict) -> int:
    logger.info("Calculating list similarity score")
    similarity_score = 0
    for id in list_a:
        if id in list_b.keys():
            similarity_score += id * list_b[id]
    return similarity_score


def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s.%(msecs)03d %(levelname)s %(module)s - %(funcName)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    location_ids = read_raw_input_lists(INPUT_PATH)
    sorted_location_ids = split_and_sort_location_id_lists(location_ids)
    part1_solution_value = calculate_ids_difference_sum(sorted_location_ids)
    logger.info(
        "Part 1, the total distance between the lists: %s", part1_solution_value
    )
    counts_dictionary = calculate_counts_in_id_list(sorted_location_ids[1])
    part2_solution_value = calculate_list_similarity_score(
        set(sorted_location_ids[0]), counts_dictionary
    )
    logger.info("Part 2, the similarity score: %s", part2_solution_value)


if __name__ == "__main__":
    main()
