from aoc_helpers.input_reader import AocInputReader


def parse_input_to_coordinates(input: str) -> list[tuple[int, int]]:
    return [tuple(int(y) for y in x.split(",")) for x in input.split()]


def max_rectangle_area_part1(red_tiles: list[tuple[int, int]]) -> int:
    """Part 1: largest rectangle with only red tiles"""
    max_area = 0
    n = len(red_tiles)
    for i in range(n - 1):
        x1, y1 = red_tiles[i]
        for j in range(i + 1, n):
            x2, y2 = red_tiles[j]
            width = abs(x2 - x1) + 1
            height = abs(y2 - y1) + 1
            area = width * height
            if area > max_area:
                max_area = area
    return max_area


def generate_red_green_grid(red_tiles):
    """Generate a compressed grid with red+green tiles marked."""
    # Step 1: Coordinate compression on RED tiles only
    all_x = sorted(set(x for x, y in red_tiles))
    all_y = sorted(set(y for x, y in red_tiles))
    
    x_to_idx = {x: i for i, x in enumerate(all_x)}
    y_to_idx = {y: i for i, y in enumerate(all_y)}
    
    # Step 2: Create compressed grid
    width = len(all_x)
    height = len(all_y)
    grid = [[0] * width for _ in range(height)]
    
    # Step 3: Mark red tiles in compressed space
    for x, y in red_tiles:
        grid[y_to_idx[y]][x_to_idx[x]] = 1
    
    # Step 4: Fill in green tiles (edges between consecutive red tiles in compressed space)
    n = len(red_tiles)
    for i in range(n):
        x1, y1 = red_tiles[i]
        x2, y2 = red_tiles[(i + 1) % n]
        
        idx_x1, idx_y1 = x_to_idx[x1], y_to_idx[y1]
        idx_x2, idx_y2 = x_to_idx[x2], y_to_idx[y2]
        
        # Fill between the two points in the compressed grid
        if idx_x1 == idx_x2:  # vertical edge
            for idx_y in range(min(idx_y1, idx_y2), max(idx_y1, idx_y2) + 1):
                grid[idx_y][idx_x1] = 1
        elif idx_y1 == idx_y2:  # horizontal edge
            for idx_x in range(min(idx_x1, idx_x2), max(idx_x1, idx_x2) + 1):
                grid[idx_y1][idx_x] = 1
        else:
            print(f"ERROR: Tile {i} at ({x1},{y1}) doesn't connect straight to tile {(i+1)%n} at ({x2},{y2})")
            raise ValueError("Red tiles only connect in straight lines")

    return grid, 0, 0


def largest_rectangle_in_binary_matrix(matrix):
    if not matrix:
        return 0
    max_area = 0
    ncols = len(matrix[0])
    heights = [0] * ncols
    for row in matrix:
        for j in range(ncols):
            heights[j] = heights[j] + 1 if row[j] == 1 else 0

        # compute largest rectangle in histogram
        stack = []
        extended_heights = heights + [0]
        for i, h in enumerate(extended_heights):
            while stack and extended_heights[stack[-1]] >= h:
                H = extended_heights[stack.pop()]
                W = i if not stack else i - stack[-1] - 1
                max_area = max(max_area, H * W)
            stack.append(i)
    return max_area


def max_rectangle_area_part2(red_tiles):
    # Work in compressed space from the start
    all_x = sorted(set(x for x, y in red_tiles))
    all_y = sorted(set(y for x, y in red_tiles))
    
    x_to_idx = {x: i for i, x in enumerate(all_x)}
    y_to_idx = {y: i for i, y in enumerate(all_y)}
    
    width = len(all_x)
    height = len(all_y)
    
    # Mark boundary in compressed space
    boundary = set()
    n = len(red_tiles)
    for i in range(n):
        x1, y1 = red_tiles[i]
        x2, y2 = red_tiles[(i + 1) % n]
        
        idx_x1, idx_y1 = x_to_idx[x1], y_to_idx[y1]
        idx_x2, idx_y2 = x_to_idx[x2], y_to_idx[y2]
        
        # Mark edge in compressed space
        if idx_x1 == idx_x2:  # vertical
            for idx_y in range(min(idx_y1, idx_y2), max(idx_y1, idx_y2) + 1):
                boundary.add((idx_x1, idx_y))
        elif idx_y1 == idx_y2:  # horizontal
            for idx_x in range(min(idx_x1, idx_x2), max(idx_x1, idx_x2) + 1):
                boundary.add((idx_x, idx_y1))
    
    # Flood fill from outside to find interior
    # Everything not reachable from outside (and not boundary) is interior
    visited = [[False] * width for _ in range(height)]
    
    def flood_outside(start_x, start_y):
        stack = [(start_x, start_y)]
        while stack:
            x, y = stack.pop()
            if x < 0 or x >= width or y < 0 or y >= height:
                continue
            if visited[y][x] or (x, y) in boundary:
                continue
            visited[y][x] = True
            stack.extend([(x+1, y), (x-1, y), (x, y+1), (x, y-1)])
    
    # Flood from all edges
    for x in range(width):
        flood_outside(x, 0)
        flood_outside(x, height - 1)
    for y in range(height):
        flood_outside(0, y)
        flood_outside(width - 1, y)
    
    # Build valid tiles set (boundary + interior)
    valid = set(boundary)
    for y in range(height):
        for x in range(width):
            if not visited[y][x]:
                valid.add((x, y))
    
    # Try all pairs of red tiles
    max_area = 0
    for i in range(len(red_tiles)):
        x1, y1 = red_tiles[i]
        idx_x1, idx_y1 = x_to_idx[x1], y_to_idx[y1]
        
        for j in range(i + 1, len(red_tiles)):
            x2, y2 = red_tiles[j]
            idx_x2, idx_y2 = x_to_idx[x2], y_to_idx[y2]
            
            min_idx_x = min(idx_x1, idx_x2)
            max_idx_x = max(idx_x1, idx_x2)
            min_idx_y = min(idx_y1, idx_y2)
            max_idx_y = max(idx_y1, idx_y2)
            
            # Check if all compressed cells are valid
            all_valid = True
            for idx_y in range(min_idx_y, max_idx_y + 1):
                for idx_x in range(min_idx_x, max_idx_x + 1):
                    if (idx_x, idx_y) not in valid:
                        all_valid = False
                        break
                if not all_valid:
                    break
            
            if all_valid:
                # Calculate actual area using original coordinates
                width_actual = abs(x2 - x1) + 1
                height_actual = abs(y2 - y1) + 1
                area = width_actual * height_actual
                max_area = max(max_area, area)
    
    return max_area


def main():
    aoc_input_reader = AocInputReader("2025/day09/input.txt")
    input_text = aoc_input_reader.read_input_to_str()
    red_tiles = parse_input_to_coordinates(input_text)

    # Part 1
    max_area_part1 = max_rectangle_area_part1(red_tiles)
    print("Part 1:", max_area_part1)

    # Part 2
    max_area_part2 = max_rectangle_area_part2(red_tiles)
    print("Part 2:", max_area_part2)


if __name__ == "__main__":
    main()
