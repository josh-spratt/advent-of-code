from aoc_helpers.input_reader import AocInputReader
import logging
from collections import Counter

logger = logging.getLogger(__name__)


def parse_junction_box_positions(input_text: str) -> list[tuple[int, int, int]]:
    """Convert input text to list of coordinates"""
    return [
        tuple(map(int, line.split(","))) for line in input_text.strip().splitlines()
    ]


def squared_straight_line_distance(
    box_a: tuple[int, int, int],
    box_b: tuple[int, int, int],
) -> int:
    """Calculate squared Euclidean distance between two 3D points"""
    return (
        (box_a[0] - box_b[0]) ** 2
        + (box_a[1] - box_b[1]) ** 2
        + (box_a[2] - box_b[2]) ** 2
    )


def find_circuit_root(
    circuit_parent: list[int],
    box_index: int,
) -> int:
    """Finds the root representative of a set, compressing the path along the way."""
    if circuit_parent[box_index] != box_index:
        circuit_parent[box_index] = find_circuit_root(
            circuit_parent,
            circuit_parent[box_index],
        )
    return circuit_parent[box_index]


def connect_circuits_if_needed(
    circuit_parent: list[int],
    circuit_size: list[int],
    box_a: int,
    box_b: int,
) -> bool:
    """Merges two sets (circuits) if they're not already connected."""
    root_a = find_circuit_root(circuit_parent, box_a)
    root_b = find_circuit_root(circuit_parent, box_b)

    if root_a == root_b:
        return False  # already in the same circuit

    # attach smaller tree under larger tree
    if circuit_size[root_a] < circuit_size[root_b]:
        root_a, root_b = root_b, root_a

    circuit_parent[root_b] = root_a
    circuit_size[root_a] += circuit_size[root_b]
    return True


def build_all_possible_connections(
    junction_box_positions: list[tuple[int, int, int]],
) -> list[tuple[int, int, int]]:
    """Creates all possible pairs of boxes with their distances."""
    total_boxes = len(junction_box_positions)
    possible_connections: list[tuple[int, int, int]] = []

    for i in range(total_boxes):
        for j in range(i + 1, total_boxes):
            dist2 = squared_straight_line_distance(
                junction_box_positions[i],
                junction_box_positions[j],
            )
            possible_connections.append((dist2, i, j))

    possible_connections.sort()  # sorts by dist2, then i, then j
    return possible_connections


def connect_closest_circuits(
    junction_box_positions: list[tuple[int, int, int]],
    number_of_pairs_to_process: int,
) -> list[int]:
    """Processes the first N closest pairs"""
    total_boxes = len(junction_box_positions)

    circuit_parent = list(range(total_boxes))
    circuit_size = [1] * total_boxes

    possible_connections = build_all_possible_connections(junction_box_positions)

    # Only process the first N PAIRS — not successful unions
    pairs_to_process = min(number_of_pairs_to_process, len(possible_connections))

    for k in range(pairs_to_process):
        _, box_a, box_b = possible_connections[k]
        connect_circuits_if_needed(
            circuit_parent,
            circuit_size,
            box_a,
            box_b,
        )

    return circuit_parent


def compute_three_largest_circuit_product(
    circuit_parent: list[int],
) -> int:
    """Finds the three largest connected components and multiplies their sizes."""
    if not circuit_parent:
        raise ValueError("No junction boxes provided")

    # Ensure all parents are compressed to roots
    for i in range(len(circuit_parent)):
        find_circuit_root(circuit_parent, i)

    circuit_counts = Counter(circuit_parent)
    largest_circuit_sizes = sorted(circuit_counts.values(), reverse=True)

    while len(largest_circuit_sizes) < 3:
        largest_circuit_sizes.append(1)

    return (
        largest_circuit_sizes[0] * largest_circuit_sizes[1] * largest_circuit_sizes[2]
    )


def find_last_connection_for_full_circuit(
    junction_box_positions: list[tuple[int, int, int]],
) -> int:
    """Finds when all boxes merge into a single circuit and returns the product of the X-coordinates of that final pair."""
    total_boxes = len(junction_box_positions)
    circuit_parent = list(range(total_boxes))
    circuit_size = [1] * total_boxes

    # Build all possible connections, sorted by distance
    possible_connections = build_all_possible_connections(junction_box_positions)

    last_connection = None

    for _, box_a, box_b in possible_connections:
        root_a = find_circuit_root(circuit_parent, box_a)
        root_b = find_circuit_root(circuit_parent, box_b)

        if root_a == root_b:
            continue  # already in the same circuit

        # Union
        connect_circuits_if_needed(circuit_parent, circuit_size, box_a, box_b)
        last_connection = (box_a, box_b)

        # Check if everything is now in one circuit
        # all roots should be the same
        root_set = {find_circuit_root(circuit_parent, i) for i in range(total_boxes)}
        if len(root_set) == 1:
            break

    if last_connection is None:
        raise ValueError("Could not merge all boxes into a single circuit")

    box_a, box_b = last_connection
    return junction_box_positions[box_a][0] * junction_box_positions[box_b][0]


def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s.%(msecs)03d %(levelname)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    aoc_input_reader = AocInputReader("2025/day08/input.txt")
    input_text = aoc_input_reader.read_input_to_str()

    junction_box_positions = parse_junction_box_positions(input_text)

    circuit_parent = connect_closest_circuits(
        junction_box_positions,
        number_of_pairs_to_process=1000,
    )

    part1 = compute_three_largest_circuit_product(circuit_parent)

    logger.info(
        "Part 1 Solution -- Product of three largest circuits: %d",
        part1,
    )

    # Part 2
    part2 = find_last_connection_for_full_circuit(junction_box_positions)
    logger.info(
        "Part 2 Solution -- Product of X coordinates of last merged pair: %d", part2
    )


if __name__ == "__main__":
    main()
