""" --- Day 1: Report Repair ---
After saving Christmas five years in a row, you've decided to take a vacation at a nice resort on a tropical island. Surely, Christmas will go on without you.

The tropical island has its own currency and is entirely cash-only. The gold coins used there have a little picture of a starfish; the locals just call them stars. None of the currency exchanges seem to have heard of them, but somehow, you'll need to find fifty of these coins by the time you arrive so you can pay the deposit on your room.

To save your vacation, you need to get all fifty stars by December 25th.

Collect stars by solving puzzles. Two puzzles will be made available on each day in the Advent calendar; the second puzzle is unlocked when you complete the first. Each puzzle grants one star. Good luck!

Before you leave, the Elves in accounting just need you to fix your expense report (your puzzle input); apparently, something isn't quite adding up.

Specifically, they need you to find the two entries that sum to 2020 and then multiply those two numbers together.

For example, suppose your expense report contained the following:

1721
979
366
299
675
1456
In this list, the two entries that sum to 2020 are 1721 and 299. Multiplying them together produces 1721 * 299 = 514579, so the correct answer is 514579.

Of course, your expense report is much larger. Find the two entries that sum to 2020; what do you get if you multiply them together? """

def get_list_from_file(filename):
    with open(filename, "r") as file:
        return file.read().splitlines();

def solve_part_one():
    input = [int(i) for i in get_list_from_file("aoc_2020_01A_input")];
    input.sort(reverse=True);

    for i in input:
        target = 2020 - i;
        if target in input:
            break;

    print(i);
    print(target);
    print(i * target);

"""--- Part Two ---
The Elves in accounting are thankful for your help; one of them even offers you a starfish coin they had left over from a past vacation. They offer you a second one if you can find three numbers in your expense report that meet the same criteria.

Using the above example again, the three entries that sum to 2020 are 979, 366, and 675. Multiplying them together produces the answer, 241861950.

In your expense report, what is the product of the three entries that sum to 2020?"""

def solve_part_two():
    input = [int(i) for i in get_list_from_file("aoc_2020_01A_input")];
    input.sort();

    for index, i in enumerate(input):
        a = i;
        remainder = 2020 - a;

        for jndex, j in enumerate(input[(index+1):]):
            b = j;
            remainder = remainder - b;

            if remainder < 0:
                break;
            if remainder in input[(jndex+1):]:
                c = remainder;
                print(a);
                print(b);
                print(c);
                print(a*b*c);
                return;


solve_part_two();