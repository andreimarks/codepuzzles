

test_input = "0,3,6".split(",")
input = "0,13,1,8,6,15".split(",")
input_to_use = test_input

numbers = list(map(int, input_to_use))

for i in range(len(numbers),10):
    print("Turn " + str(i))
    print(numbers)
    last_index = i - 1
    last_number = numbers[last_index]
    print("Evaluating: " + str(last_number))
    # If was spoken first time
    if numbers.count(last_number) == 1:
        print("First time to speak: " + str(last_number))
        numbers.append(0)
    else:
        for j in reversed(range(last_index)):
            if j == last_number:
                print(last_index)
                print(j)
                numbers.append(last_index - j)

print(numbers)