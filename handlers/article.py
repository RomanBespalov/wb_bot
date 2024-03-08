from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message
from aiogram.utils.markdown import hbold

from keyboards.inline_button import inline_keyboard
from parsing_script import get_product_info

from handlers.start import MENU


router = Router()


class Article(StatesGroup):
    choosing_article = State()


@router.message(F.text.in_(MENU[0]))
async def input_article(message: Message, state: FSMContext):
    await message.answer(
        text="Спасибо. Теперь, пожалуйста, введи артикул товара",
        reply_markup=inline_keyboard().as_markup(),
    )
    await state.set_state(Article.choosing_article)


@router.message(Article.choosing_article)
async def get_info_goods(message: Message, state: FSMContext):
    article = message.text.lower()
    goods = get_product_info(article)
    if goods == 'Ошибка артикула':
        await message.answer(
            text="Такого артикула не существует.\nПопробуй еще раз",
            reply_markup=inline_keyboard().as_markup(),
        )
        await state.set_state(Article.choosing_article)
    else:
        goods_string = ", \n".join([f"{hbold(key)} - {value}" for key, value in goods.items()])
        await message.answer(
            text=goods_string,
            reply_markup=inline_keyboard().as_markup(),
        )
