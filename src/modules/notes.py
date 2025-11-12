import sys
sys.path.append("../") # src/

from states import getCurrentStateCallback, makeNextStateCallback, makePrevStateCallback
from utils.pagination import Paginator

from aiogram.types import CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder

from datetime import datetime


class NotesListMenu:
    "Creating the notes list menu."

    def __init__(self, notes: list, _ = str) -> None:
        self.notes = notes
        self._ = _

    def makeText(self) -> str:
        notes_count = len(self.notes)

        text = (
            self._("*🗃 Notes list*") + "\n\n"
            + self._("📑 Notes count:") + " " f"*{notes_count}*"
        )

        return text

    def makeKeyboard(self, event: CallbackQuery, page: int) -> InlineKeyboardBuilder:
        "Generates an inline keyboard list of notes with navigation."

        back_callback = None
        if prev_state := makePrevStateCallback(event):
            back_callback: str = prev_state

        if not self.notes:
            keyboard = InlineKeyboardBuilder()
            if back_callback:
                keyboard.button(text=self._("⬅️ Back"), callback_data=back_callback)
            return keyboard

        keyboard_items = []
        for note in self.notes:
            note_id: int = note["id"]
            note_text: str = note["text"]

            if len(note_text) <= 15:
                note_title: str = note_text
            else:
                note_title: str = note_text[:15] + "..."

            keyboard_items.append({
                "text": note_title,
                "callback_data": makeNextStateCallback(
                    getCurrentStateCallback(event), 
                    next_state="note_card",
                    next_state_params={"id": note_id}
                )
            })

        paginator = Paginator(
            array=keyboard_items, 
            offset=5,
            page_callback=getCurrentStateCallback(event),
            back_callback=back_callback,
            _=self._
        )

        keyboard: InlineKeyboardBuilder = paginator.getPageKeyboard(page=page)
    
        return keyboard


class NoteCardMenu:
    "Creating the note card menu."

    def __init__(self, note: dict, _ = str) -> None:
        self.note = note
        self._ = _

    def makeText(self) -> str:
        note_id: int = self.note["id"]
        note_text: str = self.note["text"]
        note_created_at: datetime = self.note["created_at"]

        text = (
           "*" + self._("🔖 Note") + " " + f"№{note_id}" + "*" + "\n\n"
           + self._("📖 Text:") + " " + f"*{note_text}*" + "\n\n"
           + self._("📅 Created at:") + " " + f"*{note_created_at}*"
        )

        return text
