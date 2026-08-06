from aiogram import BaseMiddleware
from aiogram.types import Message

from db.methods.user import check_user, add_user, update_username

class UserMiddleware(BaseMiddleware):
    def __init__(self) -> None:
        self.counter = 0

    async def __call__(
        self,
        handler,
        event: Message,
        data
    ):
        
        if not check_user(event.from_user.id):
            add_user(event.from_user.id, event.from_user.username)

        update_username(event.from_user.id, event.from_user.username)

        return await handler(event, data)