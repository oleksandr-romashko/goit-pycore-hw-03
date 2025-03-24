import random

def get_numbers_ticket(min: int, max: int, quantity: int) -> list[int]:
    '''
    Generates unique numbers for a lottery.
    :param min: Minimum number (not less than 1).
    :param max: Maximum number in a set (not greater than 1000).
    :param quantity: How many numbers to choose (should be between min and max values)
    :return: List of random numbers based on input values.
    '''
    # Validate input values guard
    if min < 1 or min > max:
        return []

    if max > 1000 or max < min:
        return []

    if quantity > (max - min + 1):
        return []

    # Generate ticket numbers
    numbers = random.sample(range(min, max + 1), quantity)

    # Sort numbers ASC
    numbers.sort()

    return numbers

# Tests
test_numbers_multiple_values = get_numbers_ticket(10, 20, 4)
assert len(test_numbers_multiple_values) == 4
for number in test_numbers_multiple_values:
    assert (10 <= number <= 20)

test_numbers_single_value = get_numbers_ticket(50, 100, 1)
assert len(test_numbers_single_value) == 1
for number in test_numbers_single_value:
    assert (50 <= number <= 100)

test_numbers_max_numbers_quantity = get_numbers_ticket(200, 300, 100)
assert len(test_numbers_max_numbers_quantity) == 100
for number in test_numbers_max_numbers_quantity:
    assert (200 <= number <= 300)

test_numbers_min_numbers_quantity = get_numbers_ticket(400, 400, 1)
assert len(test_numbers_min_numbers_quantity) == 1
assert test_numbers_min_numbers_quantity == [400]

test_numbers_sort_order_unique_numbers = list(get_numbers_ticket(70, 150, 20))
for i in range(1, len(test_numbers_sort_order_unique_numbers)):
    assert test_numbers_sort_order_unique_numbers[i - 1] < test_numbers_sort_order_unique_numbers[i]

# Usage
min_number = 1
max_number = 49
numbers_quantity = 6

lottery_numbers = get_numbers_ticket(min_number, max_number, numbers_quantity)

print(f"Lottery: min number value: {min_number}, max number value: {max_number}, number of tickets: {numbers_quantity}")
print(f"Your lottery numbers: {lottery_numbers}")
