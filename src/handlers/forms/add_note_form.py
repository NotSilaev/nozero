import sys
sys.path.append("../../") # src/

from exceptions import exceptions_catcher
from i18n import language_detector
from states import makeNextStateCallback, makePrevStateCallback
from utils.common import respondEvent

from database.tables.users import getUser
from database.tables.notes import createNote

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State


router = Router(name=__name__)


class Note(StatesGroup):
    text = State()


async def start_add_note_form(event: CallbackQuery, state: FSMContext) -> None:
    await note_text_state(event, state)


@router.callback_query(F.data.endswith("note_text_state/"))
@language_detector
@exceptions_catcher()
async def note_text_state(event: CallbackQuery, state: FSMContext, _ = str) -> None:
    await state.set_state(Note.text)

    message_text = _(
        "*✍️ Adding a note*\n\n"
        + "📝 Enter the text of the note"
    )

    keyboard = InlineKeyboardBuilder()
    if prev_state := makePrevStateCallback(event):
        keyboard.button(text=_("❌ Cancel"), callback_data=prev_state)

    await respondEvent(
        event,
        text=message_text,
        parse_mode="Markdown",
        reply_markup=keyboard.as_markup()
    )


@router.message(Note.text)
@language_detector
@exceptions_catcher()
async def note_text_process(event: Message, state: FSMContext, _ = str) -> None:
    text: str = event.text
    await state.update_data(text=text)
    await add_note_form_commit(event, state)


@language_detector
@exceptions_catcher()
async def add_note_form_commit(event: CallbackQuery, state: FSMContext, _ = str) -> None:
    telegram_id: int = event.from_user.id
    user: dict = getUser(telegram_id=telegram_id)
    user_id: str = user["id"]

    note: dict = await state.get_data()
    text: str = note["text"]

    # Creating a note in the database
    createNote(user_id=user_id, text=text)

    message_text = (
        _("*✅ Note added*\n\n")
        + _("📖 Text:") + " " + f"*{text}*"
    )

    keyboard = InlineKeyboardBuilder()
    keyboard.button(text=_("📕 To Notes menu"), callback_data="notes/")

    await respondEvent(
        event,
        text=message_text,
        parse_mode="Markdown",
        reply_markup=keyboard.as_markup()
    )
    await state.clear()
