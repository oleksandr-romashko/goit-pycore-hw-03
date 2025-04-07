import logging
from datetime import datetime, date, timedelta

logging.basicConfig(level=logging.WARNING)

DATE_FORMAT = "%Y.%m.%d"

def is_leap_year(year):
    """Returns True if the year is a leap year."""
    return (year % 4 == 0 and (year % 100 != 0 or year % 400 == 0))

def get_upcoming_birthdays(
        users: list[dict[str, str]],
        today=None,
        upcoming_period_days=7
    ) -> list[dict[str, str]]:
    """
    Returns a list of users who have birthdays within the upcoming period from today.

    Each user is a dict with keys "name" and "birthday" in format "YYYY.MM.DD".
    The returned list contains dicts with "name" and the upcoming
    "congratulation_date" in string format (YYYY-MM-DD).

    :param users: List of users with "name" and "birthday" keys.
    :param today: The date to start checking from (default: current date).
    :param upcoming_period_days: Number of days ahead to check for birthdays (default: 7).
    :return: List of users with upcoming birthdays sorted by date.
    """
    # Assign today each time function is called, not once during function definition
    if today is None:
        today = date.today()

    # Empty users guard
    if not users:
        return []

    user_congratulations = []

    for user in users:
        # Retrieve date from birthday string
        try:
            birthday = datetime.strptime(user.get("birthday"), DATE_FORMAT).date()
        except ValueError as e:
            logging.warning("Date parsing failed for user '%s': %s", user.get("name"), e)
            continue

        # Handle the case if birthday is today or upcoming
        # Handle the case for February 29 birthday
        if birthday.month == 2 and birthday.day == 29:
            if is_leap_year(today.year):
                # For leap years, keep February 29
                congratulation_date = birthday.replace(year=today.year)
            else:
                # For non-leap years, set birthday to March 1
                congratulation_date = birthday.replace(year=today.year, month=3, day=1)
        else:
            # For other birthdays, just replace the year
            congratulation_date = birthday.replace(year=today.year)

        # Handle the case if birthday has passed, adjust to next year
        if congratulation_date < today:
            # If it's a February 29 birthday in a non-leap year, adjust it to March 1 of next year
            if congratulation_date.month == 2 and congratulation_date.day == 29:
                if not is_leap_year(today.year + 1):
                    congratulation_date = congratulation_date.replace(year=today.year + 1, month=3, day=1)
                else:
                    congratulation_date = congratulation_date.replace(year=today.year + 1)
            else:
                # Otherwise just move it to the next year
                congratulation_date = congratulation_date.replace(year=today.year + 1)

        # Filter dates in upcoming period range and add them to the congratulations list
        if today <= congratulation_date <= today + timedelta(upcoming_period_days):
            
            # Shift weekend congratulation to the following Monday
            if congratulation_date.weekday() == 5:  # Saturday
                congratulation_date += timedelta(days=2)
            elif congratulation_date.weekday() == 6:  # Sunday
                congratulation_date += timedelta(days=1)
            
            # Add congratulation to the list
            user_congratulations.append(
                {
                    "name":user.get("name"), 
                    "congratulation_date": congratulation_date
                })

    # Sort congratulations by date
    user_congratulations.sort(key=lambda user: user["congratulation_date"])

    # Convert congratulations date to string date representation
    for user in user_congratulations:
        user["congratulation_date"] = user["congratulation_date"].strftime(DATE_FORMAT)

    return user_congratulations


# TESTS

# Happy path
today_test_date = date(2024,1,22)  # Test with January 22, 2024
users_test_list_happy_path = [
    {"name": "Alice Adams", "birthday": "1995.01.30"},      # in 8 days
    {"name": "Jane Smith", "birthday": "1990.01.27"},       # in 5 days (weekend - Sat -> move to Mon)
    {"name": "John Doe", "birthday": "1985.01.23"},         # tomorrow (in 1 day - week day (Tuesday))
    {"name": "Charlie Clark", "birthday": "1987.01.22"},    # today
    {"name": "Emily Evans", "birthday": "1988.01.21"},      # yesterday (weekend - Sun)
    {"name": "Bob Brown", "birthday": "1985.01.01"}         # at the beginning of a year
]
expected_happy_path = [
    {"name": "Charlie Clark", "congratulation_date": "2024.01.22"},
    {"name": "John Doe", "congratulation_date": "2024.01.23"},
    {"name": "Jane Smith", "congratulation_date": "2024.01.29"}
]

result_happy_path = get_upcoming_birthdays(users_test_list_happy_path, today=today_test_date)
assert result_happy_path == expected_happy_path, f"Expected {expected_happy_path}, but got {result_happy_path}"

# Test for an empty user list (no birthdays)
result_empty_list = get_upcoming_birthdays([])
assert result_empty_list == [], f"Expected {[]}, but got {result_empty_list}"

# Test for invalid date string format handling (DD.MM.YYYY vs. YYYY.MM.DD)
users_test_list_with_bad_date_string_format = [
    {"name": "John Doe", "birthday": "23.01.1985"},     # Invalid format (DD.MM.YYYY)
    {"name": "John Doe", "birthday": "1985.01.23"},    # Valid format
]
expected_for_bad_date_string_format = [
    {"name": "John Doe", "congratulation_date": "2024.01.23"}
]

result_bad_date_string_format = get_upcoming_birthdays(
    users_test_list_with_bad_date_string_format, today=today_test_date)
assert result_bad_date_string_format == expected_for_bad_date_string_format, \
    f"Expected {expected_for_bad_date_string_format}, but got {result_bad_date_string_format}"

# Test for across-year birthday change (Dec 31 to Jan 1 transition)
# Sorting check: Ensure the birthday on Dec 31 comes before Jan 1
today_test_date_new_year = date(2024, 12, 31)  # Test with December 31, 2024
users_test_list_new_year = [
    {"name": "Alice Adams", "birthday": "1995.01.01"},      # New Year's Day next year
    {"name": "Eve Evans", "birthday": "1990.12.31"},        # Last day of the year
    {"name": "Bob Brown", "birthday": "1990.12.25"},        # Christmas (within the year)
    {"name": "Charlie Clark", "birthday": "1987.12.20"}     # Already past this year
]
expected_for_new_year = [
    {"name": "Eve Evans", "congratulation_date": "2024.12.31"},     # Last day of the year
    {"name": "Alice Adams", "congratulation_date": "2025.01.01"}    # First birthday in the new year
]

result_new_year = get_upcoming_birthdays(users_test_list_new_year, today=today_test_date_new_year)
assert result_new_year == expected_for_new_year, f"Expected {expected_for_new_year}, but got {result_new_year}"

# Test for February 29 birthday in a leap year (2024)
today_test_date_leap = date(2024, 2, 28)  # Test with February 28, 2024 (leap year)
users_test_list_leap_year = [
    {"name": "Leap Year Larry", "birthday": "1992.02.29"},  # Leap year birthday
    {"name": "Normal Year Nancy", "birthday": "1993.02.28"} # Regular birthday (Feb 28)
]
expected_for_leap_year = [
    {"name": "Normal Year Nancy", "congratulation_date": "2024.02.28"}, # Always valid for Feb 28
    {"name": "Leap Year Larry", "congratulation_date": "2024.02.29"}    # February 29 for leap year
]

result_leap_year = get_upcoming_birthdays(users_test_list_leap_year, today=today_test_date_leap)
assert result_leap_year == expected_for_leap_year, f"Expected {expected_for_leap_year}, but got {result_leap_year}"

# Test for February 29 birthday in a non-leap year (2023), adjusting to March 1st
today_test_date_non_leap = date(2023, 2, 28)  # Test with February 28, 2023 (non-leap year)
users_test_list_non_leap_year = [
    {"name": "Leap Year Larry", "birthday": "1992.02.29"},  # Leap year birthday
    {"name": "Normal Year Nancy", "birthday": "1993.02.28"} # Regular birthday (Feb 28)
]
expected_for_non_leap_year = [
    {"name": "Normal Year Nancy", "congratulation_date": "2023.02.28"}, # Always valid for Feb 28
    {"name": "Leap Year Larry", "congratulation_date": "2023.03.01"}    # Move to March 1st for non-leap year
]

result_non_leap_year = get_upcoming_birthdays(users_test_list_non_leap_year, today=today_test_date_non_leap)
assert result_non_leap_year == expected_for_non_leap_year, f"Expected {expected_for_non_leap_year}, but got {result_non_leap_year}"

# USAGE
print("Список привітань на цьому тижні:", result_happy_path)