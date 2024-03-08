from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def menu_choice_keyboard(items: list[str]) -> ReplyKeyboardMarkup:
    """
    Создаёт реплай-клавиатуру с кнопками меню
    :param items: список текстов для кнопок
    :return: объект реплай-клавиатуры
    """
    kb = [[KeyboardButton(text=item)] for item in items]
    return ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
