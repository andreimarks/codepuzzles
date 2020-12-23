import re

"""--- Day 19: Monster Messages ---
You land in an airport surrounded by dense forest. As you walk to your high-speed train, the Elves at the Mythical Information Bureau contact you again. They think their satellite has collected an image of a sea monster! Unfortunately, the connection to the satellite is having problems, and many of the messages sent back from the satellite have been corrupted.

They sent you a list of the rules valid messages should obey and a list of received messages they've collected so far (your puzzle input).

The rules for valid messages (the top part of your puzzle input) are numbered and build upon each other. For example:

0: 1 2
1: "a"
2: 1 3 | 3 1
3: "b"
Some rules, like 3: "b", simply match a single character (in this case, b).

The remaining rules list the sub-rules that must be followed; for example, the rule 0: 1 2 means that to match rule 0, the text being checked must match rule 1, and the text after the part that matched rule 1 must then match rule 2.

Some of the rules have multiple lists of sub-rules separated by a pipe (|). This means that at least one list of sub-rules must match. (The ones that match might be different each time the rule is encountered.) For example, the rule 2: 1 3 | 3 1 means that to match rule 2, the text being checked must match rule 1 followed by rule 3 or it must match rule 3 followed by rule 1.

Fortunately, there are no loops in the rules, so the list of possible matches will be finite. Since rule 1 matches a and rule 3 matches b, rule 2 matches either ab or ba. Therefore, rule 0 matches aab or aba.

Here's a more interesting example:

0: 4 1 5
1: 2 3 | 3 2
2: 4 4 | 5 5
3: 4 5 | 5 4
4: "a"
5: "b"
Here, because rule 4 matches a and rule 5 matches b, rule 2 matches two letters that are the same (aa or bb), and rule 3 matches two letters that are different (ab or ba).

Since rule 1 matches rules 2 and 3 once each in either order, it must match two pairs of letters, one pair with matching letters and one pair with different letters. This leaves eight possibilities: aaab, aaba, bbab, bbba, abaa, abbb, baaa, or babb.

Rule 0, therefore, matches a (rule 4), then any of the eight options from rule 1, then b (rule 5): aaaabb, aaabab, abbabb, abbbab, aabaab, aabbbb, abaaab, or ababbb.

The received messages (the bottom part of your puzzle input) need to be checked against the rules so you can determine which are valid and which are corrupted. Including the rules and the messages together, this might look like:

0: 4 1 5
1: 2 3 | 3 2
2: 4 4 | 5 5
3: 4 5 | 5 4
4: "a"
5: "b"

ababbb
bababa
abbbab
aaabbb
aaaabbb
Your goal is to determine the number of messages that completely match rule 0. In the above example, ababbb and abbbab match, but bababa, aaabbb, and aaaabbb do not, producing the answer 2. The whole message must match all of rule 0; there can't be extra unmatched characters in the message. (For example, aaaabbb might appear to match rule 0 above, but it has an extra unmatched b on the end.)

How many messages completely match rule 0?"""

def process_rules(input):
    rules = {}
    for line in input:
        match = re.match("(\d+): (.*)", line)
        key = match.group(1)
        values = match.group(2).replace("\"", "").split(" | ")

        if "a" in values or "b" in values:
            rules[int(key)] = values
            continue

        rules[int(key)] = [list(map(int, value.split(" ")))
                           for value in values]

    #print(rules)
    return rules


def substitute_rules(rules):
    for key in sorted(rules.keys()):
        substitute_rule(rules, key)
    return rules

def substitute_rule(rules, key):
    #print("substitute rule for: " + str(key))

    #print(rules[key])
    for i, option in enumerate(rules[key]):
        for j, suboption in enumerate(option):
            #print(str(i) + ":" + str(j))
            #print(rules[key][i][j])
            value = rules[key][i][j]
            if isinstance(value, str):
                continue

            if not re.match("\d", str(value)) is None:
                substitute_rule(rules, value)
                rules[key][i][j] = rules[value]
    #print("Rule for: " + str(key))
    #print(rules[key])


def generate_rule_options(rules):
    rule_options = []
    rule_zero = rules[0]

    for rule in rule_zero[0]:
        rule_options.append(generate_allowed_strings(rule))

def generate_allowed_strings(rule):
    allowed_strings = None

    return allowed_strings

def evaluate_message(message, rules):
    print("evaluating message: " + message)
    pointer = 0;

    for rule in rules[0]:
        print(len(rule))
        for subrule in rule:
            print(subrule)

test_input = """0: 4 1 5
1: 2 3 | 3 2
2: 4 4 | 5 5
3: 4 5 | 5 4
4: "a"
5: "b"

ababbb
bababa
abbbab
aaabbb
aaaabbb""".split("\n\n")

input_to_use = test_input
#input_to_use = open("aoc_2020_19_input").read().split("\n\n")

rules = process_rules(input_to_use[0].split("\n"))
rules = substitute_rules(rules)
rule_options = generate_rule_options(rules)

messages = input_to_use[1].split("\n")

for message in messages:
        #evaluate_message(message, rules)
    pass