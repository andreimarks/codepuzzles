import re
import copy
from pprint import pprint

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

class Rule:

    def __init__(self, id, line):
        #print(str(id) + ": " + line)
        self.id = id
        self.line = " " + line + " "
        self.substituted = self.line
        self.rules = None
        self.subrule_keys = None
        self.subrules = None
        self.value_swaps = None
        self.value = None
        self.possible_values = None

    def set_subrule_keys(self, rules):
        #print("set_subrule keys for: " + str(self.id))

        sequences = self.line.split(" | ")

        self.subrule_keys = []
        for sequence in sequences:
            sequence = sequence.replace("\"", "").split(" ")
            if not (sequence[0] == "a" or sequence[0] == "b"):
                sequence = list(map(int, sequence))
                self.subrule_keys.append(sequence)
            else:
                self.subrule_keys = None

        #print(self.subrule_keys)
        return

    def set_subrules(self, rules):
        #print("set_subrules for: " + str(self.id))
        options = []

        if self.subrule_keys is None:
            return

        for option in self.subrule_keys:
            keys = []
            for key in option:
                keys.append(rules[key])
            options.append(keys)

        self.subrules = options
        #print(self.subrules)

    def set_available_value_swaps(self, rules):
        if self.subrules is None:
            self.possible_values = re.match(".*(a|b).*", self.line).group(1)
            return

        if self.value_swaps is None:
            self.value_swaps = copy.deepcopy(self.subrules)

        print("set_available_rules_for: " + str(self.id))
        for index, rule in enumerate(self.subrules):
            print(len(rule))
            ready_to_set_values = True
            if len(rule) > 1:
                for jndex, subrule in enumerate(rule):
                    print(subrule)
                    if rules[subrule.id].get_possible_values() is None:
                        print("Waiting on " + str(rules[subrule.id].id))
                        ready_to_set_values = False
                        continue
                    self.value_swaps[index][jndex] = subrule.get_possible_values()
            else:
                if rules[rule.id].get_possible_values() is None:
                    print("Waiting on " + rule.line)
                    ready_to_set_values = False
                    continue
                self.value_swaps[index] = rule.get_possible_values()

        if (ready_to_set_values):
            self.possible_values = [""]
            for i, option in enumerate(self.value_swaps):
                print(option)
                if len(option) > 1:
                    """
                    for j, value in enumerate(option):
                        self.possible_values[i]
                        """
                    pass
                else:
                    self.possible_values[i] += option

        print(self.value_swaps)

    def get_possible_values(self):
        print("get_possible_values for: " + str(self.id))
        return self.possible_values


def process_rules_oop(input):
    rules = {}
    for line in input:
        match = re.match("(\d+): (.*)", line)
        key = int(match.group(1))
        value = match.group(2).replace("\"", "")
        rules[key] = Rule(key, value)

    return rules

def set_subrule_keys(rules):
    for rule in rules.values():
        rule.set_subrule_keys(rules)

def set_subrules(rules):
    for rule in rules.values():
        rule.set_subrules(rules)

def set_value_swaps(rules):
    for i in range(3):
        print("Set value swaps: " + str(i) + "_---------------------------")
        for rule in rules.values():
            print(rule.subrules)
            rule.set_available_value_swaps(rules)

def substitute_rules(rules):
    print(rules)
    for value in rules.values():
        substitute_rule_keys(rules, value)
    return rules

def substitute_rule_keys(rules, value):
    print("substitute keys in: " + str(value))
    if isinstance(value, list):
        string = str(value)
        print(string)
        lst = list(string)
        print(lst)


def substitute_rule(rules, key):

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
    print(rules)
    rule_zero = rules[0][0]
    print(rule_zero)
    rule_options = [""]
    get_string_options(rules, rule_options, rule_zero, 0)
    print(rule_options)

    return rule_options


def get_string_options(rules, rule_options, rule, current_index):
    print(rule)

    first_pass = True
    for key in rule:
        print(key)
        if isinstance(key, list) and not isinstance(key[0], list):
            for item in key:
                print(item)
                if not first_pass:
                    rule_options.append(rule_options[current_index])
                    current_index += 1
                get_string_options(rules, rule_options, item, current_index)

        # if we're at the letters, we just add it to the current string
        value = rules[key]
        if isinstance(value, str):
            rule_options[current_index] += value
        #if isinstance(value, list):

        else:
            #current_string += "_dosomething_"
            print(value)
            get_string_options(rules, rule_options, value, current_index)
        #print(current_string)


def evaluate_message(message, rules):
    print("Evaluating message: " + message)
    pointer = 0;

    while pointer < len(message):
        pass
        #check_against_rules(rules, message, pointer)

    for rule in rules[0]:
        print(len(rule))
        for subrule in rule:
            print(subrule)

def replace_strings(rules):
    #print("replace keys -------------------------")
    for rule in rules.keys():
        if rules[rule].line == " a " or rules[rule].line == " b ":
            #print(rule)
            #print("Here")
            search_for = " " + str(rule) + " "
            #print(search_for)
            replace_with = rules[rule].line
            #print(replace_with)
            for key, value in rules.items():
                #print(str(key) + ": " + str(value.substituted))
                rules[key].substituted = rules[key].substituted.replace(search_for, replace_with)
                #print(str(key) + ": " + str(rules[key].substituted))

    #print("replace others -------------------------")
    for rule in sorted(rules.keys(), reverse=True):
        search_for = " " + str(rule) + " "
        replace_with = " ( " + rules[rule].substituted + " ) "
        for key, value in rules.items():
            #print(str(key) + ": " + str(value.substituted))
            rules[key].substituted = rules[key].substituted.replace(search_for, replace_with)
            #print(str(key) + ": " + str(value.substituted))

    return rules


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
rules_input = input_to_use[0].split("\n")
messages_input = input_to_use[1].split("\n")

rules = process_rules_oop(rules_input)
print(rules)
for i in range(2):
    rules = replace_strings(rules)
for rule in sorted(rules.keys(), reverse = True):
    rules[rule].substituted = rules[rule].substituted.replace(" ", "").replace("(a)", "a").replace("(b)", "b").replace("(aa)", "aa").replace("(bb)", "bb").replace("(ab)", "ab").replace("(ba)", "ba")
    #print(str(rules[rule].id) + ": " + rules[rule].substituted)

print(rules[0].substituted)