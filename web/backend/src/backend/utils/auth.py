import random


def generate_random_code(length: int) -> str:
    if (length < 1) or (length > 256):
        raise ValueError("The code can be from 1 to 256 chars long")

    numbers = [f"{random.randint(0, 9)}" for _ in range(0, length)]
    code = "".join(numbers)
    return code
