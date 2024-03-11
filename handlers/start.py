from aiogram import Router, types
from aiogram.filters import CommandStart
from aiogram.utils.markdown import hbold

from keyboards.menu_choice import menu_choice_keyboard
from keyboards.inline_button import inline_keyboard


MENU = [
    "Получить информацию по товару",
    "Остановить уведомления",
    "Получить информацию из БД",
]

router = Router()


@router.message(CommandStart())
async def command_start_handler(message: types.Message) -> None:
    await message.answer(f"Привет, {hbold(message.from_user.full_name)}!\n"
                         f"Выбери пункт меню, чтобы начать\n\n"
                         f"Команды:\n"
                         f"Стартовая команда - /start\n"
                         f"Для отмены текщуего действия - /cancel\n",
                         reply_markup=menu_choice_keyboard(MENU),
                         )
    await message.answer(
        text="Также ты можешь подписаться на рассылку👇",
        reply_markup=inline_keyboard().as_markup(),
    )
