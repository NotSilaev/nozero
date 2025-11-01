from aiogram.types import Message, CallbackQuery


def makeNextStateCallback(event: Message | CallbackQuery, next_state: str, is_start: bool = False) -> str:
    "Generates a callback for the transition to the next state."

    if is_start:
        states_chain = ["start"]
    else:
        if isinstance(event, Message):
            states_chain = []
        elif isinstance(event, CallbackQuery):
            states_chain: list = event.data.rstrip("/").split("/")

    states_chain.append(next_state + "/")
    next_state_callback = "/".join(states_chain)

    return next_state_callback


def makePrevStateCallback(event: Message | CallbackQuery) -> str | None:
    "Generates a callback to return to the previous state."

    if not isinstance(event, CallbackQuery):
        return None

    states_chain: list = event.data.rstrip("/").split("/")
    if len(states_chain) == 1:
        return None

    del states_chain[-1]
    prev_state_callback = "/".join(states_chain) + "/"

    return prev_state_callback

    