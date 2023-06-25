from re import match

class Validator():
    def is_accepted_password(password):
        return len(password) > 6 and any(char.isdigit() for char in password)

    def is_accepted_email(email):
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(match(pattern, email))