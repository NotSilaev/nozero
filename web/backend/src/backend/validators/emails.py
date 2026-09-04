import re


class EmailsValidator:
    def __init__(self, email: str) -> None:
        self.email = email

    def is_email_valid(self) -> bool:
        EMAIL_REGEX = re.compile(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}(?:\.[a-zA-Z]{2,})?$")
        if EMAIL_REGEX.match(self.email):
            return True
        return False
