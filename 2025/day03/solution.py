from aoc_helpers.input_reader import AocInputReader
import logging

logger = logging.getLogger(__name__)


class Battery:
    def __init__(self, joltage: int):
        self.joltage = joltage


class BatteryBank:
    def __init__(self, batteries: list[Battery]):
        self.batteries = batteries

    @staticmethod
    def from_str(battery_bank_str: str):
        """Create BatteryBank from string."""
        batteries = [Battery(int(char)) for char in battery_bank_str]
        return BatteryBank(batteries)

    def find_largest_n_batteries(self, n: int) -> int:
        selected_digits = []
        search_start = 0
        joltage_chars = [str(b.joltage) for b in self.batteries]
        for selection_index in range(n):
            remaining_needed = n - selection_index - 1
            search_end = len(joltage_chars) - remaining_needed
            max_digit = -1
            max_idx = -1
            for idx in range(search_start, search_end):
                digit = int(joltage_chars[idx])
                if digit > max_digit:
                    max_digit = digit
                    max_idx = idx
            selected_digits.append(max_digit)
            search_start = max_idx + 1
        return int("".join(str(d) for d in selected_digits))


class EscalatorPowerSupply:
    def __init__(self, battery_banks: list[BatteryBank]):
        self.battery_banks = battery_banks

    @staticmethod
    def from_str_list(battery_bank_strs: list[str]):
        """Create EscalatorPowerSupply from list of strings."""
        banks = [BatteryBank.from_str(s) for s in battery_bank_strs]
        return EscalatorPowerSupply(banks)

    def part1_total(self) -> int:
        """Calculate part 1 total."""
        return sum(bank.find_largest_n_batteries(2) for bank in self.battery_banks)

    def part2_total(self) -> int:
        """Calculate part 2 total."""
        return sum(bank.find_largest_n_batteries(12) for bank in self.battery_banks)


def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s.%(msecs)03d %(levelname)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    aoc_input_reader = AocInputReader("2025/day03/input.txt")
    input_text = aoc_input_reader.read_input_to_str()
    battery_bank_strings = input_text.split()
    escalator_power_supply = EscalatorPowerSupply.from_str_list(battery_bank_strings)
    part1_result = escalator_power_supply.part1_total()
    part2_result = escalator_power_supply.part2_total()
    logger.info("Part 1 Solution -- Total output joltage is %d", part1_result)
    logger.info("Part 2 Solution -- Total output joltage is %d", part2_result)


if __name__ == "__main__":
    main()
