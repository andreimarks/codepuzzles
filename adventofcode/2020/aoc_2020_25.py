""""--- Day 25: Combo Breaker ---
You finally reach the check-in desk. Unfortunately, their registration systems are currently offline, and they cannot check you in. Noticing the look on your face, they quickly add that tech support is already on the way! They even created all the room keys this morning; you can take yours now and give them your room deposit once the registration system comes back online.

The room key is a small RFID card. Your room is on the 25th floor and the elevators are also temporarily out of service, so it takes what little energy you have left to even climb the stairs and navigate the halls. You finally reach the door to your room, swipe your card, and - beep - the light turns red.

Examining the card more closely, you discover a phone number for tech support.

"Hello! How can we help you today?" You explain the situation.

"Well, it sounds like the card isn't sending the right command to unlock the door. If you go back to the check-in desk, surely someone there can reset it for you." Still catching your breath, you describe the status of the elevator and the exact number of stairs you just had to climb.

"I see! Well, your only other option would be to reverse-engineer the cryptographic handshake the card does with the door and then inject your own commands into the data stream, but that's definitely impossible." You thank them for their time.

Unfortunately for the door, you know a thing or two about cryptographic handshakes.

The handshake used by the card and the door involves an operation that transforms a subject number. To transform a subject number, start with the value 1. Then, a number of times called the loop size, perform the following steps:

Set the value to itself multiplied by the subject number.
Set the value to the remainder after dividing the value by 20201227.
The card always uses a specific, secret loop size when it transforms a subject number. The door always uses a different, secret loop size.

The cryptographic handshake works like this:

The card transforms the subject number of 7 according to the card's secret loop size. The result is called the card's public key.
The door transforms the subject number of 7 according to the door's secret loop size. The result is called the door's public key.
The card and door use the wireless RFID signal to transmit the two public keys (your puzzle input) to the other device. Now, the card has the door's public key, and the door has the card's public key. Because you can eavesdrop on the signal, you have both public keys, but neither device's loop size.
The card transforms the subject number of the door's public key according to the card's loop size. The result is the encryption key.
The door transforms the subject number of the card's public key according to the door's loop size. The result is the same encryption key as the card calculated.
If you can use the two public keys to determine each device's loop size, you will have enough information to calculate the secret encryption key that the card and door use to communicate; this would let you send the unlock command directly to the door!

For example, suppose you know that the card's public key is 5764801. With a little trial and error, you can work out that the card's loop size must be 8, because transforming the initial subject number of 7 with a loop size of 8 produces 5764801.

Then, suppose you know that the door's public key is 17807724. By the same process, you can determine that the door's loop size is 11, because transforming the initial subject number of 7 with a loop size of 11 produces 17807724.

At this point, you can use either device's loop size with the other device's public key to calculate the encryption key. Transforming the subject number of 17807724 (the door's public key) with a loop size of 8 (the card's loop size) produces the encryption key, 14897079. (Transforming the subject number of 5764801 (the card's public key) with a loop size of 11 (the door's loop size) produces the same encryption key: 14897079.)

What encryption key is the handshake trying to establish?"""

def transform_number(subject_number, start_value):
    start_value = start_value * subject_number
    return start_value % 20201227

def transform_number_with_loop(loop_size, subject_number):
    value = 1
    for i in range(loop_size):
        value = value * subject_number
        value = value % 20201227
    return value

test_input = """5764801
17807724""".split("\n")

input = """10705932
12301431""".split("\n")

#input_to_use = test_input
input_to_use = input

card_public_key = int(input_to_use[0])
door_public_key = int(input_to_use[1])

card_loop_size = door_loop_size = 0
loop_size = 1
start_value = 1

#77484: 8322708
#loop_size = 77484
#start_value = 8322708

while card_loop_size == 0 and door_loop_size == 0:
    #key = transform_number(loop_size, 7)
    key = transform_number(7, start_value)
    print(str(loop_size) + ": " + str(key))
    if card_loop_size == 0 and card_public_key == key:
        card_loop_size = loop_size
    elif door_loop_size == 0 and door_public_key == key:
        door_loop_size = loop_size
    loop_size += 1
    start_value = key


if card_loop_size != 0:
    print(transform_number_with_loop(card_loop_size, door_public_key))
elif door_loop_size != 0:
    print(transform_number_with_loop(door_loop_size, card_public_key))

print("Card Loop Size: " + str(card_loop_size))
print("Door Loop Size: " + str(door_loop_size))
"""
!= 10244418 -> 
== 11328376
Card Loop Size: 0
Door Loop Size: 529361
"""