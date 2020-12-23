from helpers import get_list_from_file
import re

"""--- Day 18: Operation Order ---
As you look out the window and notice a heavily-forested continent slowly appear over the horizon, you are interrupted by the child sitting next to you. They're curious if you could help them with their math homework.

Unfortunately, it seems like this "math" follows different rules than you remember.

The homework (your puzzle input) consists of a series of expressions that consist of addition (+), multiplication (*), and parentheses ((...)). Just like normal math, parentheses indicate that the expression inside must be evaluated before it can be used by the surrounding expression. Addition still finds the sum of the numbers on both sides of the operator, and multiplication still finds the product.

However, the rules of operator precedence have changed. Rather than evaluating multiplication before addition, the operators have the same precedence, and are evaluated left-to-right regardless of the order in which they appear.

For example, the steps to evaluate the expression 1 + 2 * 3 + 4 * 5 + 6 are as follows:

1 + 2 * 3 + 4 * 5 + 6
  3   * 3 + 4 * 5 + 6
      9   + 4 * 5 + 6
         13   * 5 + 6
             65   + 6
                 71
Parentheses can override this order; for example, here is what happens if parentheses are added to form 1 + (2 * 3) + (4 * (5 + 6)):

1 + (2 * 3) + (4 * (5 + 6))
1 +    6    + (4 * (5 + 6))
     7      + (4 * (5 + 6))
     7      + (4 *   11   )
     7      +     44
            51
Here are a few more examples:

2 * 3 + (4 * 5) becomes 26.
5 + (8 * 3 + 9 + 3 * 4 * 3) becomes 437.
5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4)) becomes 12240.
((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2 becomes 13632.
Before you can help with the homework, you need to understand it yourself. Evaluate the expression on each line of the homework; what is the sum of the resulting values?

"""
def eval_ltr(string):
    #print("Evaluating: " + string)
    while string_contains_parens(string):
        string = eval_paren(string)

    while "*" in string or "+" in string:
        orig_string = string
        match = re.match("(\d+ [\*|\+] \d+)", string)
        substring = match.group(0)
        value = eval(substring)
        string = string.replace(substring, str(value), 1)
        if orig_string == string:
            print("HELP")

    #print("Returning: " + string)
    return string

def string_contains_parens(string):
    return "(" in string

def eval_paren(string):
    start = end = 0
    for index, i in enumerate(string):
        if i == "(":
            start = index
        elif i == ")":
            end = index
            break
    substring = string[start:end+1]
    no_parens = substring.replace("(", "").replace(")", "")
    return string.replace(substring, str(eval_ltr(no_parens)), 1)


def solve_part_one(input):
    print(sum([int(eval_ltr(line)) for line in input_to_use]))

test_input = """2 * 3 + (4 * 5)
5 + (8 * 3 + 9 + 3 * 4 * 3)
5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))
((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2""".split("\n")

#input_to_use = test_input
input_to_use = get_list_from_file("aoc_2020_18_input")

solve_part_one(input_to_use)

# First attempt: 45283905003863
# Second attempt: 45283905029161 -- made sure to only replace first instance of string...

# 5 + 8 + ((5 * 9 * 7 * 9) * 8 * 8) + (8 * 7 + 8 * (6 + 9 * 3 * 2) * 6 + 6) + 3 * 9
# 5 + 8 + 181440 + 34566 + 3 * 9

# 8 * ((4 + 9 + 9) + 8) * (5 * 4 * (9 + 3 * 3 + 6) + 3) * (8 * 7 * 9 + (8 + 8 * 3 + 9 * 7) * (3 + 7 + 9) * 7) + 6
# 8 * 30 * 843 * 120099 + 6

# 3 * (2 + (9 * 2 * 2 + 8) * (7 * 6 * 7 * 3) * (3 * 9 * 7) * (6 * 6)) * 9 * 8 + 6
# 3 * 276051888 * 9 * 8 + 6
#59627207814
#59627207814

# 4 * (8 * (5 + 2 * 2 + 4) + 4 + (2 + 8 * 3 + 7 + 8)) + (4 + 7 + 9 * 4 + 8 * (8 * 6 * 6 * 9)) + 6 * 8 * ((3 + 3 * 7 * 2 + 7 + 5) * 2 * 5)
# 228874 * 8 * 960
# 1757752320
# 1757752320









