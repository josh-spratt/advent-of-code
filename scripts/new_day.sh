#!/usr/bin/env bash

YEAR="$1"
DAY="$2"

[ -z "$YEAR" ] && { echo "Missing YEAR"; exit 1; }
[ -z "$DAY" ] && { echo "Missing DAY"; exit 1; }

DAY_PAD="$(printf "%02d" "$DAY")"
DIR="$YEAR/day$DAY_PAD"

mkdir -p "$DIR"
: > "$DIR/input.txt"
: > "$DIR/solution.py"

echo "Created $DIR/input.txt and $DIR/solution.py"