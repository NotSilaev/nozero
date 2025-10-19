import sys
sys.path.append("../") # src/

from exceptions import exceptions_catcher
from i18n import language_detector
from utils.common import respondEvent, getUserName, makeGreetingMessage

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
    user: User = event.from_user
    user_name: str = getUserName(user=user, _=_)

    greeting: str = makeGreetingMessage(_=_)

    message_text = _(
        f"*{greeting}*, {user_name}"
    )

    await respondEvent(
        event,
        text=message_text, 
        parse_mode="Markdown"
    )
