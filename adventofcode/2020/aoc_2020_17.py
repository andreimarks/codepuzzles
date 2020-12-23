import math

"""--- Day 17: Conway Cubes ---
As your flight slowly drifts through the sky, the Elves at the Mythical Information Bureau at the North Pole contact you. They'd like some help debugging a malfunctioning experimental energy source aboard one of their super-secret imaging satellites.

The experimental energy source is based on cutting-edge technology: a set of Conway Cubes contained in a pocket dimension! When you hear it's having problems, you can't help but agree to take a look.

The pocket dimension contains an infinite 3-dimensional grid. At every integer 3-dimensional coordinate (x,y,z), there exists a single cube which is either active or inactive.

In the initial state of the pocket dimension, almost all cubes start inactive. The only exception to this is a small flat region of cubes (your puzzle input); the cubes in this region start in the specified active (#) or inactive (.) state.

The energy source then proceeds to boot up by executing six cycles.

Each cube only ever considers its neighbors: any of the 26 other cubes where any of their coordinates differ by at most 1. For example, given the cube at x=1,y=2,z=3, its neighbors include the cube at x=2,y=2,z=2, the cube at x=0,y=2,z=3, and so on.

During a cycle, all cubes simultaneously change their state according to the following rules:

If a cube is active and exactly 2 or 3 of its neighbors are also active, the cube remains active. Otherwise, the cube becomes inactive.
If a cube is inactive but exactly 3 of its neighbors are active, the cube becomes active. Otherwise, the cube remains inactive.
The engineers responsible for this experimental energy source would like you to simulate the pocket dimension and determine what the configuration of cubes should be at the end of the six-cycle boot process.

For example, consider the following initial state:

.#.
..#
###
Even though the pocket dimension is 3-dimensional, this initial state represents a small 2-dimensional slice of it. (In particular, this initial state defines a 3x3x1 region of the 3-dimensional space.)

Simulating a few cycles from this initial state produces the following configurations, where the result of each cycle is shown layer-by-layer at each given z coordinate (and the frame of view follows the active cells in each cycle):

Before any cycles:

z=0
.#.
..#
###


After 1 cycle:

z=-1
#..
..#
.#.

z=0
#.#
.##
.#.

z=1
#..
..#
.#.


After 2 cycles:

z=-2
.....
.....
..#..
.....
.....

z=-1
..#..
.#..#
....#
.#...
.....

z=0
##...
##...
#....
....#
.###.

z=1
..#..
.#..#
....#
.#...
.....

z=2
.....
.....
..#..
.....
.....


After 3 cycles:

z=-2
.......
.......
..##...
..###..
.......
.......
.......

z=-1
..#....
...#...
#......
.....##
.#...#.
..#.#..
...#...

z=0
...#...
.......
#......
.......
.....##
.##.#..
...#...

z=1
..#....
...#...
#......
.....##
.#...#.
..#.#..
...#...

z=2
.......
.......
..##...
..###..
.......
.......
.......
After the full six-cycle boot process completes, 112 cubes are left in the active state.

Starting with your given initial configuration, simulate six cycles. How many cubes are left in the active state after the sixth cycle?

"""
# region Abandoned approach -------------------------------
def print_slices(positions):
    x_min = x_max = y_min = y_max = z_min = z_max = 0

    for position in positions.keys():
        x, y, z = position[0], position[1], position[2]
        if x < x_min:
            x_min = x
        if x > x_max:
            x_max = x
        if y < y_min:
            y_min = y
        if y > y_max:
            y_max = y
        if z < z_min:
            z_min = z
        if z > z_max:
            z_max = z

    for z in range(z_min, z_max + 1):
        slice = f"z={z}\n"
        for y in reversed(range(y_min, y_max + 1)):
            for x in range(x_min, x_max + 1):
                position = (x,y,z)
                if position in positions:
                    slice += positions[position]
                else:
                    slice += "."
            slice += "\n"
        print(slice)


def full_range_approach(positions, min_x, max_x, min_y, max_y, min_z, max_z):
    new_positions = positions
    test = []
    for x in range(min_x, max_x):
        for y in range(min_y, max_y):
            for z in range(min_z, max_z):
                position = (x,y,z)
                if position not in positions:
                    positions[position] = new_positions[position] = "."

                # Get neighbor count
                active_neighbors = check_neighbor_activity(positions, position)

                # Get value change
                value = positions[position]
                new_positions[position] = get_value_change(value, active_neighbors)
                #test.append(value)

    print_slices(new_positions)
    print(len([True for val in test if val == "#"]))


def check_neighbor_activity(positions, position):
    x_min, x_max = position[0] - 1, position[0] + 2
    y_min, y_max = position[1] - 1, position[1] + 2
    z_min, z_max = position[2] - 1, position[2] + 2

    active_count = 0
    for x in range(x_min, x_max):
        for y in range(y_min, y_max):
            for z in range(z_min, z_max):
                check_position = (x,y,z)
                if check_position == position:
                    continue
                if check_position in positions and positions[check_position] == "#":
                    active_count += 1

    return active_count


def get_value_change(current_value, neighbor_count):
    if current_value == "#" and not(neighbor_count == 2 or neighbor_count == 3):
        current_value = "."
    elif neighbor_count == 3:
        current_value = "#"

    return current_value

# endregion Abandoned approach -------------------------------

def populate_initial_ranges(input):
    width = len(input[0])
    height = len(input)

    return width, height


def populate_initial_positions(input, positions, width, height):
    for x in range(width):
        for y in range(height):
            if input[y][x] == "#":
                positions[(x, y, 0)] = input[y][x]
    return positions


def get_test_positions(positions):
    test_positions = {}
    for position, value in positions.items():
        test_neighbors(position, test_positions)
    print(test_positions)
    return test_positions


def test_neighbors(position, test_positions):
    x_o, y_o, z_o = position[0], position[1], position[2]
    for x in range(x_o - 1, x_o + 2):
        for y in range(y_o - 1, y_o + 2):
            for z in range(z_o - 1, z_o + 2):
                test_position = (x,y,z)
                if test_position == position:
                    continue
                if not test_position in test_positions:
                    test_positions[test_position] = 1
                else:
                    test_positions[test_position] += 1


def solve_part_one(input):
    input = list(reversed(input.split("\n")))
    width, height = populate_initial_ranges(input)

    positions = {}
    populate_initial_positions(input, positions, width, height)
    # print_slices(positions)

    for i in range(6):
        test_positions = get_test_positions(positions)
        new_positions = {}

        for position, value in test_positions.items():
            if value == 3:
                new_positions[position] = "#"
            if position in positions and (value == 2 or value == 3):
                new_positions[position] = "#"

        positions = new_positions

        print(len([value for value in positions.values()]))
        # print_slices(positions)


test_input = """.#.
..#
###"""
"""
.#. ...
..# #.#
### .##
     #
"""

input_to_use = open("aoc_2020_17_input").read()
#input_to_use = test_input

solve_part_one(input_to_use)
