import re

from helpers import get_list_from_file

"""--- Day 7: Handy Haversacks ---
You land at the regional airport in time for your next flight. In fact, it looks like you'll even have time to grab some food: all flights are currently delayed due to issues in luggage processing.

Due to recent aviation regulations, many rules (your puzzle input) are being enforced about bags and their contents; bags must be color-coded and must contain specific quantities of other color-coded bags. Apparently, nobody responsible for these regulations considered how long they would take to enforce!

For example, consider the following rules:

light red bags contain 1 bright white bag, 2 muted yellow bags.
dark orange bags contain 3 bright white bags, 4 muted yellow bags.
bright white bags contain 1 shiny gold bag.
muted yellow bags contain 2 shiny gold bags, 9 faded blue bags.
shiny gold bags contain 1 dark olive bag, 2 vibrant plum bags.
dark olive bags contain 3 faded blue bags, 4 dotted black bags.
vibrant plum bags contain 5 faded blue bags, 6 dotted black bags.
faded blue bags contain no other bags.
dotted black bags contain no other bags.
These rules specify the required contents for 9 bag types. In this example, every faded blue bag is empty, every vibrant plum bag contains 11 bags (5 faded blue and 6 dotted black), and so on.

You have a shiny gold bag. If you wanted to carry it in at least one other bag, how many different bag colors would be valid for the outermost bag? (In other words: how many colors can, eventually, contain at least one shiny gold bag?)

In the above rules, the following options would be available to you:

A bright white bag, which can hold your shiny gold bag directly.
A muted yellow bag, which can hold your shiny gold bag directly, plus some other bags.
A dark orange bag, which can hold bright white and muted yellow bags, either of which could then hold your shiny gold bag.
A light red bag, which can hold bright white and muted yellow bags, either of which could then hold your shiny gold bag.
So, in this example, the number of bag colors that can eventually contain at least one shiny gold bag is 4.

How many bag colors can eventually contain at least one shiny gold bag? (The list of rules is quite long; make sure you get all of it.)"""

class Rule:
    def __init__(self, rule_def):
        self.rule_def = rule_def
        rule_name, rule_contents = self.evaluate_rule(rule_def)

        self.evaluate_name(rule_name) 
        self.evaluate_contents(rule_contents)

    def evaluate_rule(self, rule_def):
        # Set rule name and contents
        pattern = "(.*) bags contain (.*).$"
        match = re.match(pattern, rule_def)
        rule_name = match.group(1)
        rule_contents = match.group(2).split(", ")

        return rule_name, rule_contents


    def evaluate_name(self, rule_name):
        # Set style and color
        pattern = "(\w*) (\w*)"
        match = re.match(pattern, rule_name)
        self.style = match.group(1)
        self.color = match.group(2)

    
    def evaluate_contents(self, rule_contents):
        self.contents = {}

        if rule_contents[0] == "no other bags":
            return

        for bag in rule_contents:
            pattern = "(\w*) (.*) bag"
            match = re.match(pattern, bag)
            count = match.group(1)
            name = match.group(2)
            self.contents[name] = int(count)


    def get_name(self):
        return self.style + " " + self.color


    def contains_bag_type(self, *bag_types):
        return any([True for bag_type in bag_types if bag_type in self.contents.keys()])


def create_rule(rule_def):
    rule = Rule(rule_def)
    return rule.get_name(), rule


def get_rules(input):
    rules = {}

    for line in input:
        name, rule = create_rule(line)
        rules[name] = rule

    return rules


def search_rules_for_contents(rules, items):
    return [rule.get_name() for rule in rules.values() if rule.contains_bag_type(*items)]


def solve_part_one(rules):
    results = search_rules_for_contents(rules, ["shiny gold"])
    results_set = set(results)

    while len(results) > 0:
        results = search_rules_for_contents(rules, results)
        results_set = results_set.union(set(results))

    print(len(results_set))

"""--- Part Two ---
It's getting pretty expensive to fly these days - not because of ticket prices, but because of the ridiculous number of bags you need to buy!

Consider again your shiny gold bag and the rules from the above example:

faded blue bags contain 0 other bags.
dotted black bags contain 0 other bags.
vibrant plum bags contain 11 other bags: 5 faded blue bags and 6 dotted black bags.
dark olive bags contain 7 other bags: 3 faded blue bags and 4 dotted black bags.
So, a single shiny gold bag must contain 1 dark olive bag (and the 7 bags within it) plus 2 vibrant plum bags (and the 11 bags within each of those): 1 + 1*7 + 2 + 2*11 = 32 bags!

Of course, the actual rules have a small chance of going several levels deeper than this example; be sure to count all of the bags, even if the nesting becomes topologically impractical!

Here's another example:

shiny gold bags contain 2 dark red bags.
dark red bags contain 2 dark orange bags.
dark orange bags contain 2 dark yellow bags.
dark yellow bags contain 2 dark green bags.
dark green bags contain 2 dark blue bags.
dark blue bags contain 2 dark violet bags.
dark violet bags contain no other bags.
In this example, a single shiny gold bag must contain 126 other bags.

How many individual bags are required inside your single shiny gold bag?"""

def add_contents(rules, all_bags, origin):
    for bag, count in origin.contents.items():
        for i in range(count):
            all_bags.append(bag)
            add_contents(rules, all_bags, rules[bag])

def solve_part_two(rules):
    all_bags = []
    origin = rules["shiny gold"]
    add_contents(rules, all_bags, origin)

    print(len(all_bags))

input = get_list_from_file("aoc_2020_07_input")
rules = get_rules(input)
solve_part_two(rules)