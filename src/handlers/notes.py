import sys
sys.path.append("../") # src/

from exceptions import exceptions_catcher
from i18n import language_detector
from states import makeNextStateCallback, makePrevStateCallback
from utils.common import respondEvent

from handlers.forms.add_note_form import start_add_note_form

from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.fsm.context import FSMContext


router = Router(name=__name__)


@router.callback_query(F.data.endswith("notes/"))
@language_detector
@exceptions_catcher()
async def notes(event: CallbackQuery, state: FSMContext, _ = str) -> None:
    await state.clear()

    message_text = _(
        "*📕 Notes*"
    )

    keyboard = InlineKeyboardBuilder()
    keyboard.button(text=_("✍️ Add note"), callback_data=makeNextStateCallback(event, "add_note"))
    if prev_state := makePrevStateCallback(event):
        keyboard.button(text=_("⬅️ Back"), callback_data=prev_state)
    keyboard.adjust(1)

    await respondEvent(
        event,
        text=message_text, 
        parse_mode="Markdown",
        reply_markup=keyboard.as_markup()
    )


@router.callback_query(F.data.endswith("add_note/"))
@language_detector
@exceptions_catcher()
async def add_note(event: CallbackQuery, state: FSMContext, _ = str) -> None:
    await start_add_note_form(event, state)
