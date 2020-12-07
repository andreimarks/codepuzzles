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
            self.contents[name] = count


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
    results = []
    results.extend([rule.get_name() for rule in rules.values() if rule.contains_bag_type(*items)])
    return results


def solve_part_one(input):
    rules = get_rules(input)
    results = search_rules_for_contents(rules, ["shiny gold"])
    results_set = set(results)

    while len(results) > 0:
        results = search_rules_for_contents(rules, results)
        results_set = results_set.union(set(results))

    print(len(results_set))

input = get_list_from_file("aoc_2020_07_input")