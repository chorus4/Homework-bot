from aiogram import Router

from handlers.welcome import router as welcome_router
from handlers.classes import router as classes_router

from middlewares.user import UserMiddleware

main_router = Router()

handlers = [
  welcome_router,
  classes_router
]

main_router.include_routers(*handlers)
main_router.message.outer_middleware(UserMiddleware())