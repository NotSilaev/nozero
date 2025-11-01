import sys
sys.path.append("../") # src/

from exceptions import exceptions_catcher
from i18n import language_detector
from utils.common import respondEvent, getUserName, makeGreetingMessage

from database.tables.users import createUser, getUser

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart


router = Router(name=__name__)


@router.message(CommandStart())
@router.callback_query(F.data == "start")
@router.message(F.text & (~F.text.startswith("/")))
@language_detector
@exceptions_catcher()
async def start(event: Message | CallbackQuery, _ = str) -> None:
    telegram_user: User = event.from_user
    telegram_id: int = telegram_user.id
    user_name: str = getUserName(user=telegram_user, _=_)

    user: dict = getUser(telegram_id=telegram_id)
    if not user:
        # Creating a user in the database
        createUser(telegram_id=telegram_id)

    greeting: str = makeGreetingMessage(_=_)

    message_text = _(
        f"*{greeting}*, {user_name}"
    )

    await respondEvent(
        event,
        text=message_text, 
        parse_mode="Markdown"
    )
