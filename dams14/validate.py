"""Module for functions which compare and validate types of data"""

import re

EMAIL_REGEX = "[^@]+@[^@]+\.[^@]+"


def check_equal(item1, item2):
    """Checks that two pieces of data are structurally equivalent --
    useful for password verification"""

    if type(item1) is type(item2):
        return item1 == item2
    return False


def is_email(string):
    """Takes a string and returns True is it is a valid email"""
    return bool(re.search(EMAIL_REGEX, str(string)))


def validate_email(email1, email2):
    """Checks that two emails are valid and equal"""

    if is_email(email1) and is_email(email2):
        # Check that the emails match regardless of case
        return email1.upper() == email2.upper()
    return False
