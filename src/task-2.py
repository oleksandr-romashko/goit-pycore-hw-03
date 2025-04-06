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
    if min < 1:
        return []

    if min > max or max > 1000:
        return []

    if quantity < 1 or max - min + 1 < quantity:
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
    assert 10 <= number <= 20

test_numbers_extreme_values = get_numbers_ticket(1, 1000, 20)
assert len(test_numbers_extreme_values) == 20
for number in test_numbers_extreme_values:
    assert 1 <= number <= 1000

test_numbers_min_value_is_less_than_one = get_numbers_ticket(0, 20, 4)
assert test_numbers_min_value_is_less_than_one == []

test_numbers_max_is_less_than_one = get_numbers_ticket(20, 0, 4)
assert test_numbers_max_is_less_than_one == []

test_numbers_max_is_less_than_min_value = get_numbers_ticket(20, 10, 4)
assert test_numbers_max_is_less_than_min_value == []

test_numbers_max_is_greater_than_1000 = get_numbers_ticket(100, 1001, 4)
assert test_numbers_max_is_less_than_min_value == []

test_numbers_single_value = get_numbers_ticket(50, 100, 1)
assert len(test_numbers_single_value) == 1
for number in test_numbers_single_value:
    assert 50 <= number <= 100

test_numbers_min_numbers_quantity = get_numbers_ticket(400, 400, 1)
assert len(test_numbers_min_numbers_quantity) == 1
assert test_numbers_min_numbers_quantity == [400]

test_numbers_max_possible_numbers_quantity = get_numbers_ticket(200, 300, 101)
assert len(test_numbers_max_possible_numbers_quantity) == 101
for number in test_numbers_max_possible_numbers_quantity:
    assert 200 <= number <= 300

test_numbers_quantity_is_zero = get_numbers_ticket(400, 400, 0)
assert test_numbers_quantity_is_zero == []

test_numbers_quantity_is_greater_than_possible = get_numbers_ticket(400, 400, 2)
assert test_numbers_quantity_is_greater_than_possible == []

test_numbers_ASC_sort_order = list(get_numbers_ticket(70, 150, 20))
for i in range(1, len(test_numbers_ASC_sort_order)):
    assert test_numbers_ASC_sort_order[i - 1] < test_numbers_ASC_sort_order[i]

test_numbers_has_unique_values = list(get_numbers_ticket(500, 600, 101))
unique_values = []
for el in test_numbers_has_unique_values:
    assert el not in unique_values
    unique_values.append(el)

# Usage example
min_number = 1
max_number = 49
numbers_quantity = 6

lottery_numbers = get_numbers_ticket(min_number, max_number, numbers_quantity)

print(f"Lottery: min number value: {min_number}, max number value: {max_number}, number of tickets: {numbers_quantity}")
print(f"Your lottery numbers: {lottery_numbers}")
