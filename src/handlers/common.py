import sys
sys.path.append("../") # src/

from exceptions import exceptions_catcher
from i18n import language_detector
from states import makeNextStateCallback
from utils.common import respondEvent, getUserName, makeGreetingMessage

from database.tables.users import createUser, getUser

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, StateFilter
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.fsm.context import FSMContext


router = Router(name=__name__)


@router.message(CommandStart())
@router.callback_query(F.data.endswith("start/"))
@router.message(F.text & (~F.text.startswith("/")), StateFilter(None))
@language_detector
@exceptions_catcher()
async def start(event: Message | CallbackQuery, state: FSMContext, _ = str) -> None:
    await state.clear()

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

    keyboard = InlineKeyboardBuilder()
    keyboard.button(text=_("📕 Notes"), callback_data=makeNextStateCallback(event, "notes", is_start=True))

    await respondEvent(
        event,
        text=message_text, 
        parse_mode="Markdown",
        reply_markup=keyboard.as_markup()
    )
