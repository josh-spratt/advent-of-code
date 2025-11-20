def part1(data):
    return "Part 1 not implemented"

def part2(data):
    return "Part 2 not implemented"

if __name__ == "__main__":
    try:
        with open("../input.txt") as f:
            data = f.read().strip()
        print(f"Part 1: {part1(data)}")
        print(f"Part 2: {part2(data)}")
    except FileNotFoundError:
        print("input.txt not found")
