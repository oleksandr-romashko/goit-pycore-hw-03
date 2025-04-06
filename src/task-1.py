import datetime

def get_days_from_today(date: str) -> int | None:
    """
    Calculates number of days between given date and current date.
    :param date: String date representation in a specific date format.
    :return: Number of days between given date and current date.
             Positive value if date is in the past.
             Negative value if date is in the future.
             None in case of improper date value or date format and logs 
             descriptive error message in case of improper date value or date format.
    """

    # Acceptable date format
    date_format = r"%Y-%m-%d"

    # Convert date string into date object
    try:
        target_date = datetime.datetime.strptime(date, date_format).date()
    except ValueError as e:
        # Log error message
        print(f"[ERROR] {e}")
        return None

    # Retrieve current date
    today =  datetime.date.today()

    # Calculate days difference between two dates
    days_diff = (today - target_date).days

    return days_diff

# Examples
print(get_days_from_today("2020-10-09")) # Positive number for day in the past
print(get_days_from_today("2030-10-09")) # Negative number for day in the future
print(get_days_from_today(datetime.date.today().strftime(r"%Y-%m-%d"))) # 0 for today
print(get_days_from_today("abc")) # None on parse error
print(get_days_from_today("24.03.2025")) # None on improper date format
