import re

sanitizing_pattern = re.compile(r"[^+\d]")
formatted_pattern = re.compile(r"^(\+?38)?(\d+)$")

sanitizing_pattern_alternative = re.compile(r"\D")

# Solution using re.sub() function only an grouping backreference
def normalize_phone(phone_number: str) -> str:
    """
    Converts given phone numbers into appropriate Ukrainian phone number format,
    allowing only plus symbol ('+') and digits. 
    :param phone_number: Phone number string in a different format, e.g.:
        "    +38(050)123-32-34"
        "     0503451234"
        "(050)8889900"
        "38050-111-22-22"
        "38050 111 22 11   "
    :return: Normalized phone number string in international Ukrainian (+38) format.
    """
    # Replace all non-allowed characters
    sanitized_str = re.sub(sanitizing_pattern, "", phone_number)

    # Format phone numbers to match Ukrainian international format
    formatted_str = re.sub(formatted_pattern, r"+38\2", sanitized_str)

    return formatted_str

# Solution using re.sub() function only an grouping backreference
def normalize_phone_alternative(phone_number: str) -> str:
    """
    Converts given phone numbers into appropriate Ukrainian phone number format,
    allowing only plus symbol ('+') and digits. 
    :param phone_number: Phone number string in a different format, e.g.:
        "    +38(050)123-32-34"
        "     0503451234"
        "(050)8889900"
        "38050-111-22-22"
        "38050 111 22 11   "
    :return: Normalized phone number string in international Ukrainian (+38) format.
    """
    # Replace all non-digit characters
    sanitized_str = re.sub(sanitizing_pattern_alternative, "", phone_number)

    # Format phone numbers to match Ukrainian international format
    formatted_str = "+38" + sanitized_str.lstrip("38")

    return formatted_str

# Tests
assert normalize_phone("+380501233234") == "+380501233234"
assert normalize_phone("    +38(050)123-32-34") == "+380501233234"
assert normalize_phone("     0503451234") == "+380503451234"
assert normalize_phone("(050)8889900") == "+380508889900"
assert normalize_phone("38050-111-22-22") == "+380501112222"
assert normalize_phone("38050 111 22 11   ") == "+380501112211"

assert normalize_phone_alternative("+380501233234") == "+380501233234"
assert normalize_phone_alternative("    +38(050)123-32-34") == "+380501233234"
assert normalize_phone_alternative("     0503451234") == "+380503451234"
assert normalize_phone_alternative("(050)8889900") == "+380508889900"
assert normalize_phone_alternative("38050-111-22-22") == "+380501112222"
assert normalize_phone_alternative("38050 111 22 11   ") == "+380501112211"

# Usage
print("First solution:")
print(normalize_phone("+380501233234"))
print(normalize_phone("    +38(050)123-32-34"))
print(normalize_phone("     0503451234"))
print(normalize_phone("(050)8889900"))
print(normalize_phone("38050-111-22-22"))
print(normalize_phone("38050 111 22 11   "))

print("\nSecond solution:")
print(normalize_phone_alternative("+380501233234"))
print(normalize_phone_alternative("    +38(050)123-32-34"))
print(normalize_phone_alternative("     0503451234"))
print(normalize_phone_alternative("(050)8889900"))
print(normalize_phone_alternative("38050-111-22-22"))
print(normalize_phone_alternative("38050 111 22 11   "))
