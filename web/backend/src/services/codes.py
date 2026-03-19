from src.database.tables.codes import CodesTable

from src.services.mails import MailsService

from src.utils.common import generate_random_code, get_current_datetime

from datetime import datetime


class CodesService:
    @staticmethod
    async def send_code(email: str) -> None:
        code: str = generate_random_code(length=5)
        await CodesTable.create(email=email, code=code)
        MailsService.send_mail(
            recipients=(email, ),
            subject="NOZERO | Your login code",
            content=f"<div><p>Code: {code}</p></div>",
            content_subtype="html"
        )


    @staticmethod
    async def is_code_valid(email, code) -> bool:
        code_data: dict = await CodesTable.get(email=email, code=code)

        if not code_data:
            return False

        now: datetime = get_current_datetime()
        created_at: datetime = code_data["created_at"]
        if (now - created_at).seconds > 60*10:
            return False
        
        return True
