from helpers import get_list_from_file

"""--- Day 11: Seating System ---
Your plane lands with plenty of time to spare. The final leg of your journey is a ferry that goes directly to the tropical island where you can finally start your vacation. As you reach the waiting area to board the ferry, you realize you're so early, nobody else has even arrived yet!

By modeling the process people use to choose (or abandon) their seat in the waiting area, you're pretty sure you can predict the best place to sit. You make a quick map of the seat layout (your puzzle input).

The seat layout fits neatly on a grid. Each position is either floor (.), an empty seat (L), or an occupied seat (#). For example, the initial seat layout might look like this:

L.LL.LL.LL
LLLLLLL.LL
L.L.L..L..
LLLL.LL.LL
L.LL.LL.LL
L.LLLLL.LL
..L.L.....
LLLLLLLLLL
L.LLLLLL.L
L.LLLLL.LL
Now, you just need to model the people who will be arriving shortly. Fortunately, people are entirely predictable and always follow a simple set of rules. All decisions are based on the number of occupied seats adjacent to a given seat (one of the eight positions immediately up, down, left, right, or diagonal from the seat). The following rules are applied to every seat simultaneously:

If a seat is empty (L) and there are no occupied seats adjacent to it, the seat becomes occupied.
If a seat is occupied (#) and four or more seats adjacent to it are also occupied, the seat becomes empty.
Otherwise, the seat's state does not change.
Floor (.) never changes; seats don't move, and nobody sits on the floor.

After one round of these rules, every seat in the example layout becomes occupied:

#.##.##.##
#######.##
#.#.#..#..
####.##.##
#.##.##.##
#.#####.##
..#.#.....
##########
#.######.#
#.#####.##
After a second round, the seats with four or more occupied adjacent seats become empty again:

#.LL.L#.##
#LLLLLL.L#
L.L.L..L..
#LLL.LL.L#
#.LL.LL.LL
#.LLLL#.##
..L.L.....
#LLLLLLLL#
#.LLLLLL.L
#.#LLLL.##
This process continues for three more rounds:

#.##.L#.##
#L###LL.L#
L.#.#..#..
#L##.##.L#
#.##.LL.LL
#.###L#.##
..#.#.....
#L######L#
#.LL###L.L
#.#L###.##
#.#L.L#.##
#LLL#LL.L#
L.L.L..#..
#LLL.##.L#
#.LL.LL.LL
#.LL#L#.##
..L.L.....
#L#LLLL#L#
#.LLLLLL.L
#.#L#L#.##
#.#L.L#.##
#LLL#LL.L#
L.#.L..#..
#L##.##.L#
#.#L.LL.LL
#.#L#L#.##
..L.L.....
#L#L##L#L#
#.LLLLLL.L
#.#L#L#.##
At this point, something interesting happens: the chaos stabilizes and further applications of these rules cause no seats to change state! Once people stop moving around, you count 37 occupied seats.

Simulate your seating area by applying the seating rules repeatedly until no seats change state. How many seats end up occupied?"""

def pad_input(input):
    input = ["*" + line + "*" for line in input]
    buffer = "*" * len(input[0])
    input.insert(0, buffer)
    input.append(buffer)
    print(input)

    return input

def run_turn(input, output, indices, width):
    global run
    run += 1

    for index in indices:
        # if seat is empty and no occupied seats, occupy
        if input[index] == "L" and count_occupied_neighbors(input, index, width) == 0:
            output[index] = "#"
        # if seat is occupied and four or more seats adjacent to it are also occupied, become empty
        elif input[index] == "#" and count_occupied_neighbors(input, index, width) >= 4:
            output[index] = "L"
        else:
            output[index] = input[index]

    if (output == input):
        draw_map(output, width)
        print(str(run))
        print(len([i for i in output if i == "#"]))
    else:
        run_turn(output, input, indices, width)


def count_occupied_neighbors(test, index, width):
    indices = [index - width - 1, 
               index - width, 
               index - width + 1,
               index - 1,
               index + 1,
               index + width - 1,
               index + width,
               index + width + 1]
    return len([i for i in indices if test[i] == "#"])

def draw_map(input, width):
    input_string = "".join(input)
    lines = [input_string[i:i+width] for i in range(0, len(input_string), width)]
    print("\n".join(lines).replace("*", ""))

def solve_part_one(input, output, indices, width):
    run_turn(input, output, indices, width)

"""--- Part Two ---
As soon as people start to arrive, you realize your mistake. People don't just care about adjacent seats - they care about the first seat they can see in each of those eight directions!

Now, instead of considering just the eight immediately adjacent seats, consider the first seat in each of those eight directions. For example, the empty seat below would see eight occupied seats:

.......#.
...#.....
.#.......
.........
..#L....#
....#....
.........
#........
...#.....
The leftmost empty seat below would only see one empty seat, but cannot see any of the occupied ones:

.............
.L.L.#.#.#.#.
.............
The empty seat below would see no occupied seats:

.##.##.
#.#.#.#
##...##
...L...
##...##
#.#.#.#
.##.##.
Also, people seem to be more tolerant than you expected: it now takes five or more visible occupied seats for an occupied seat to become empty (rather than four or more from the previous rules). The other rules still apply: empty seats that see no occupied seats become occupied, seats matching no rule don't change, and floor never changes.

Given the same starting layout as above, these new rules cause the seating area to shift around as follows:

L.LL.LL.LL
LLLLLLL.LL
L.L.L..L..
LLLL.LL.LL
L.LL.LL.LL
L.LLLLL.LL
..L.L.....
LLLLLLLLLL
L.LLLLLL.L
L.LLLLL.LL
#.##.##.##
#######.##
#.#.#..#..
####.##.##
#.##.##.##
#.#####.##
..#.#.....
##########
#.######.#
#.#####.##
#.LL.LL.L#
#LLLLLL.LL
L.L.L..L..
LLLL.LL.LL
L.LL.LL.LL
L.LLLLL.LL
..L.L.....
LLLLLLLLL#
#.LLLLLL.L
#.LLLLL.L#
#.L#.##.L#
#L#####.LL
L.#.#..#..
##L#.##.##
#.##.#L.##
#.#####.#L
..#.#.....
LLL####LL#
#.L#####.L
#.L####.L#
#.L#.L#.L#
#LLLLLL.LL
L.L.L..#..
##LL.LL.L#
L.LL.LL.L#
#.LLLLL.LL
..L.L.....
LLLLLLLLL#
#.LLLLL#.L
#.L#LL#.L#
#.L#.L#.L#
#LLLLLL.LL
L.L.L..#..
##L#.#L.L#
L.L#.#L.L#
#.L####.LL
..#.#.....
LLL###LLL#
#.LLLLL#.L
#.L#LL#.L#
#.L#.L#.L#
#LLLLLL.LL
L.L.L..#..
##L#.#L.L#
L.L#.LL.L#
#.LLLL#.LL
..#.L.....
LLL###LLL#
#.LLLLL#.L
#.L#LL#.L#
Again, at this point, people stop shifting around and the seating area reaches equilibrium. Once this occurs, you count 26 occupied seats.

Given the new visibility method and the rule change for occupied seats becoming empty, once equilibrium is reached, how many seats end up occupied?"""

def run_turn_two(input, output, indices, width):
    global run
    run += 1
    #print(run)
    draw_map(input, width)

    for index in indices:
        # if seat is occupied and five or more seats in LOS are also occupied, become empty
        if input[index] == "#" and count_has_visible_neighbors(input, index, width, 5):
            output[index] = "L"
        # if seat is empty and no occupied seats in LOS, occupy
        elif input[index] == "L" and not count_has_visible_neighbors(input, index, width, 1):
            output[index] = "#"
        else:
            output[index] = input[index]

    #draw_map(output, width)

    if (output == input):
        draw_map(output, width)
        print(str(run))
        print(len([i for i in output if i == "#"]))
    else:
        run_turn_two(output, input, indices, width)


def count_has_visible_neighbors(test, index, width, target):
    directions = [-width - 1, 
                  -width, 
                  -width + 1,
                  -1,
                  +1,
                  width - 1,
                  width,
                  width + 1]

    visible_neighbors = 0
    for direction in directions:
    #    if index == 15:
    #        print(test[index])
        visible_neighbors += check_for_neighbor_in_direction(test, index, direction)
        if visible_neighbors >= target:
            return True # reached the target of visible neighbors
    
    return False # no visible neighbors

def check_for_neighbor_in_direction(test, current_index, direction):
    test_index = current_index + direction
    found = test[test_index]
    if found == "*" or found =="L":
        return 0
    if found == "#":
        return 1 
    
    return check_for_neighbor_in_direction(test, test_index, direction)
    
run = 0

test_input = """L.LL.LL.LL
LLLLLLL.LL
L.L.L..L..
LLLL.LL.LL
L.LL.LL.LL
L.LLLLL.LL
..L.L.....
LLLLLLLLLL
L.LLLLLL.L
L.LLLLL.LL""".split("\n")

input = get_list_from_file("aoc_2020_11_input")
#input = test_input
input = pad_input(input) # Add extra buffer

width = len(input[0])
input = list("".join(input)) # Create list
output = list(input)
indices = [index for index, val in enumerate(input) if val != "*"] # Get indices we want to evaluate

draw_map(input, width)
run_turn_two(input, output, indices, width)
#2128