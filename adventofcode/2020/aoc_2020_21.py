from helpers import get_list_from_file
import re

"""--- Day 21: Allergen Assessment ---
You reach the train's last stop and the closest you can get to your vacation island without getting wet. There aren't even any boats here, but nothing can stop you now: you build a raft. You just need a few days' worth of food for your journey.

You don't speak the local language, so you can't read any ingredients lists. However, sometimes, allergens are listed in a language you do understand. You should be able to use this information to determine which ingredient contains which allergen and work out which foods are safe to take with you on your trip.

You start by compiling a list of foods (your puzzle input), one food per line. Each line includes that food's ingredients list followed by some or all of the allergens the food contains.

Each allergen is found in exactly one ingredient. Each ingredient contains zero or one allergen. Allergens aren't always marked; when they're listed (as in (contains nuts, shellfish) after an ingredients list), the ingredient that contains each listed allergen will be somewhere in the corresponding ingredients list. However, even if an allergen isn't listed, the ingredient that contains that allergen could still be present: maybe they forgot to label it, or maybe it was labeled in a language you don't know.

For example, consider the following list of foods:

mxmxvkd kfcds sqjhc nhms (contains dairy, fish)
trh fvjkl sbzzf mxmxvkd (contains dairy)
sqjhc fvjkl (contains soy)
sqjhc mxmxvkd sbzzf (contains fish)
The first food in the list has four ingredients (written in a language you don't understand): mxmxvkd, kfcds, sqjhc, and nhms. While the food might contain other allergens, a few allergens the food definitely contains are listed afterward: dairy and fish.

The first step is to determine which ingredients can't possibly contain any of the allergens in any food in your list. In the above example, none of the ingredients kfcds, nhms, sbzzf, or trh can contain an allergen. Counting the number of times any of these ingredients appear in any ingredients list produces 5: they all appear once each except sbzzf, which appears twice.

Determine which ingredients cannot possibly contain any of the allergens in your list. How many times do any of those ingredients appear?"""

class Food:

    def __init__(self, line):
        matches = re.match("(.*) \(contains (.*)\)", line)
        self.ingredients = set(matches.group(1).split(" "))
        self.allergens = set(matches.group(2).split(", "))


def solve_part_one(input):
    # Construct food and allergen collections
    foods = [Food(line) for line in input]
    allergens = set()
    ingredients = []
    for food in foods:
        allergens = allergens.union(food.allergens)
        ingredients.extend(list(food.ingredients))

    # Find all potential allergens
    potential_allergens = {}
    for allergen in allergens:
        foods_with_allergen = [food for food in foods if allergen in food.allergens]
        i_set = set.intersection(*[food.ingredients for food in foods_with_allergen])
        potential_allergens[allergen] = i_set

    # Solve
    allergen_ingredients = set.union(*potential_allergens.values())
    print(len([ingredient for ingredient in ingredients if not ingredient in allergen_ingredients]))


test_input = """mxmxvkd kfcds sqjhc nhms (contains dairy, fish)
trh fvjkl sbzzf mxmxvkd (contains dairy)
sqjhc fvjkl (contains soy)
sqjhc mxmxvkd sbzzf (contains fish)""".split("\n")

#input_to_use = test_input
input_to_use = get_list_from_file("aoc_2020_21_input")

solve_part_one(input_to_use) # 2211

