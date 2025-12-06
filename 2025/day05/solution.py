from aoc_helpers.input_reader import AocInputReader
import logging

logger = logging.getLogger(__name__)


class IngredientFreshnessChecker:
    def __init__(self, input_text: str):
        self.fresh_ingredient_ranges: list[tuple[int, int]] = []
        self.available_ingredient_ids: list[int] = []
        self._parse_input(input_text)

    def _parse_input(self, input_text: str) -> None:
        """Parses the input text to populate ranges and IDs."""
        split_ranges_and_ids = tuple(x.split() for x in input_text.split("\n\n"))

        for ran in split_ranges_and_ids[0]:
            start = int(ran.split("-")[0])
            end = int(ran.split("-")[1])
            self.fresh_ingredient_ranges.append((start, end))

        self.available_ingredient_ids = [int(id) for id in split_ranges_and_ids[1]]

    def count_fresh_ingredients(self) -> int:
        """
        Part 1: Counts how many of the available ingredients are fresh.
        """
        fresh_ingredients = 0
        for ingredient in self.available_ingredient_ids:
            for start, end in self.fresh_ingredient_ranges:
                if start <= ingredient <= end:
                    fresh_ingredients += 1
                    break
        return fresh_ingredients

    def count_total_possible_fresh_ingredients(self) -> int:
        """
        Part 2: Counts how many unique ingredient IDs could possibly be fresh.
        """
        # Sort ranges by start position
        sorted_ranges = sorted(self.fresh_ingredient_ranges, key=lambda x: x[0])

        # Merge overlapping ranges
        merged_ranges = []
        for start, end in sorted_ranges:
            if merged_ranges and start <= merged_ranges[-1][1]:
                # Overlapping or adjacent - extend the last range
                merged_ranges[-1] = (
                    merged_ranges[-1][0],
                    max(merged_ranges[-1][1], end),
                )
            else:
                # No overlap - add new range
                merged_ranges.append((start, end))

        # Count total ingredients in merged ranges
        total_possible_fresh_ingredients = 0
        for start, end in merged_ranges:
            num_ingredients = end - start + 1
            total_possible_fresh_ingredients += num_ingredients

        return total_possible_fresh_ingredients


def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s.%(msecs)03d %(levelname)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    aoc_input_reader = AocInputReader("2025/day05/input.txt")
    input_text = aoc_input_reader.read_input_to_str()

    checker = IngredientFreshnessChecker(input_text)

    fresh_ingredients = checker.count_fresh_ingredients()
    logger.info("Part 1 Solution -- Available fresh ingredients: %d", fresh_ingredients)
    fresh_ingredients_possible = checker.count_total_possible_fresh_ingredients()
    logger.info(
        "Part 2 Solution -- Total fresh ingredient IDs: %d", fresh_ingredients_possible
    )


if __name__ == "__main__":
    main()
