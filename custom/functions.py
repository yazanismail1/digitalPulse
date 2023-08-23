import re

def is_valid_email(text):
    # Define a regular expression pattern for a valid email address
    email_pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'

    # Use the re.match() function to check if the text matches the pattern
    if re.match(email_pattern, text):
        return True
    else:
        return False