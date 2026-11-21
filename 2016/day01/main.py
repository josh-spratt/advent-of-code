from aoc import inputs
from pathlib import Path

INPUT_PATH = Path("input.txt")
STARTING_POINT = [0, 0]


def translate_instructions(instructions: str):
    parsed = instructions.split(", ")
    
    parsed_instructions = []
    for instruction in parsed:
        parsed_instructions.append(
            {
                "direction": instruction[0],
                "magnitude": int(instruction[1:])
            }
        )

    return parsed_instructions


def part1(input: str) -> int:
    facing_direction = "N"
    location = STARTING_POINT

    for instruction in input:
        if facing_direction == "N":
            if instruction["direction"] == "R":
                location[0] += instruction["magnitude"]
                facing_direction = "E"
            else:
                location[0] -= instruction["magnitude"]
                facing_direction = "W"
        elif facing_direction == "E":
            if instruction["direction"] == "R":
                location[1] -= instruction["magnitude"]
                facing_direction = "S"
            else:
                location[1] += instruction["magnitude"]
                facing_direction = "N"
        elif facing_direction == "S":
            if instruction["direction"] == "R":
                location[0] -= instruction["magnitude"]
                facing_direction = "W"
            else:
                location[0] += instruction["magnitude"]
                facing_direction = "E"
        elif facing_direction == "W":
            if instruction["direction"] == "R":
                location[1] += instruction["magnitude"]
                facing_direction = "N"
            else:
                location[1] -= instruction["magnitude"]
                facing_direction = "S"
    final_location = location
    return abs(final_location[0]) + abs(final_location[1])


def part2(input: str) -> int:
    facing_direction = "N"
    location = [0, 0]
    visited_locations = []

    for instruction in input:
        if facing_direction == "N":
            if instruction["direction"] == "R":
                for i in range(1, instruction["magnitude"] + 1):
                    location[0] += 1
                    visited_locations.append(tuple(location))
                    facing_direction = "E"
            else:
                for i in range(1, instruction["magnitude"] + 1):
                    location[0] -= 1
                    visited_locations.append(tuple(location))
                    facing_direction = "W"
        elif facing_direction == "E":
            if instruction["direction"] == "R":
                for i in range(1, instruction["magnitude"] + 1):
                    location[1] -= 1
                    visited_locations.append(tuple(location))
                    facing_direction = "S"
            else:
                for i in range(1, instruction["magnitude"] + 1):
                    location[1] += 1
                    visited_locations.append(tuple(location))
                    facing_direction = "N"
        elif facing_direction == "S":
            if instruction["direction"] == "R":
                for i in range(1, instruction["magnitude"] + 1):
                    location[0] -= 1
                    visited_locations.append(tuple(location))
                    facing_direction = "W"
            else:
                for i in range(1, instruction["magnitude"] + 1):
                    location[0] += 1
                    visited_locations.append(tuple(location))
                    facing_direction = "E"
        elif facing_direction == "W":
            if instruction["direction"] == "R":
                for i in range(1, instruction["magnitude"] + 1):
                    location[1] += 1
                    visited_locations.append(tuple(location))
                    facing_direction = "N"
            else:
                for i in range(1, instruction["magnitude"] + 1):
                    location[1] -= 1
                    visited_locations.append(tuple(location))
                    facing_direction = "S"

    seen = set()
    for location in visited_locations:
        if location in seen:
            return abs(location[0]) + abs(location[1])
        else:
            seen.add(location)


def main() -> None:
    input_data = inputs.read_input(INPUT_PATH)
    parsed_instructions = translate_instructions(input_data)
    taxicab_distance = part1(parsed_instructions)

    print("PART 1")
    print(f"taxicab_distance: {taxicab_distance}\n")

    taxicab_distance_part_2 = part2(parsed_instructions)

    print("PART 2")
    print(f"taxicab_distance: {taxicab_distance_part_2}\n")

if __name__ == "__main__":
    main()
