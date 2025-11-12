import sys
sys.path.append("../") # src/

from exceptions import exceptions_catcher
from i18n import language_detector
from states import makeNextStateCallback, makePrevStateCallback
from utils.common import respondEvent, getCallParams

from handlers.forms.add_note_form import start_add_note_form

from modules.notes import NotesListMenu, NoteCardMenu

from database.tables.users import getUser
from database.tables.notes import getNotes, getNote

from cache import setCacheValue, getCacheValue, deleteCacheKey

from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.fsm.context import FSMContext

import json


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
    keyboard.button(text=_("🗃 Notes list"), callback_data=makeNextStateCallback(event, "notes_list"))
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


@router.callback_query(F.data.split("?")[0].endswith("notes_list/"))
@language_detector
@exceptions_catcher()
async def notes_list(event: CallbackQuery, state: FSMContext, _ = str) -> None:
    await state.clear()

    telegram_id: int = event.from_user.id
    user_notes_cache_key = f"notes-{telegram_id}"

    call_params: dict = getCallParams(call=event)

    try:
        page = int(call_params["page"])
    except KeyError:
        page = 1

    if page == 1:
        deleteCacheKey(user_notes_cache_key)

    try:
        notes = json.loads(getCacheValue(key=user_notes_cache_key))
    except TypeError:
        user: dict = getUser(telegram_id=telegram_id)
        user_id: str = user["id"]
        notes: list = getNotes(user_id=user_id)
        setCacheValue(
            key=user_notes_cache_key,
            value=json.dumps(notes, default=str)
        )

    notes_list_menu = NotesListMenu(notes=notes, _=_)
    message_text: str = notes_list_menu.makeText()
    keyboard: InlineKeyboardBuilder = notes_list_menu.makeKeyboard(event=event, page=page)

    await respondEvent(
        event,
        text=message_text, 
        parse_mode="Markdown",
        reply_markup=keyboard.as_markup()
    )


@router.callback_query(F.data.split("?")[0].endswith("note_card/"))
@language_detector
@exceptions_catcher()
async def note_card(event: CallbackQuery, state: FSMContext, _ = str) -> None:
    await state.clear()

    call_params: dict = getCallParams(call=event)
    note_id = int(call_params["id"])

    note: dict | None = getNote(note_id)

    if note:
        note_card_menu = NoteCardMenu(note=note, _=_)
        message_text: str = note_card_menu.makeText()
    else:
        message_text = _("*🔎 Note not found*")


    keyboard = InlineKeyboardBuilder()
    if prev_state := makePrevStateCallback(event):
        keyboard.button(text=_("⬅️ Back"), callback_data=prev_state)

    await respondEvent(
        event,
        text=message_text, 
        parse_mode="Markdown",
        reply_markup=keyboard.as_markup()
    )
