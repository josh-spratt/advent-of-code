#!/bin/bash

YEAR=$1
DAY=$2

if [ -z "$YEAR" ] || [ -z "$DAY" ]; then
    echo "Usage: ./new_day.sh <YEAR> <DAY>"
    exit 1
fi

# Pad day with zero if needed
DAY=$(printf "%02d" $DAY)

BASE_DIR="$YEAR/$DAY"

if [ -d "$BASE_DIR" ]; then
    echo "Directory $BASE_DIR already exists."
    exit 1
fi

mkdir -p "$BASE_DIR/python"
mkdir -p "$BASE_DIR/rust/src"

# Create Python template
cat <<EOF > "$BASE_DIR/python/solution.py"
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
EOF

# Create Rust template
cat <<EOF > "$BASE_DIR/rust/src/main.rs"
fn main() {
    let input = include_str!("../../input.txt");
    println!("Part 1: {}", part1(input));
    println!("Part 2: {}", part2(input));
}

fn part1(_input: &str) -> String {
    "Part 1 not implemented".to_string()
}

fn part2(_input: &str) -> String {
    "Part 2 not implemented".to_string()
}
EOF

# Create Cargo.toml
cat <<EOF > "$BASE_DIR/rust/Cargo.toml"
[package]
name = "aoc-$YEAR-$DAY"
version = "0.1.0"
edition = "2021"

[dependencies]
EOF

# Create empty input file
touch "$BASE_DIR/input.txt"

echo "Created structure for $YEAR Day $DAY"
