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


def main() -> None:
    input_data = inputs.read_input(INPUT_PATH)
    parsed_instructions = translate_instructions(input_data)

    facing_direction = "N"
    location = STARTING_POINT

    for instruction in parsed_instructions:
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
    taxicab_distance = abs(final_location[0]) + abs(final_location[1])

    print("PART 1")
    print(f"taxicab_distance: {taxicab_distance}\n")


if __name__ == "__main__":
    main()
