import logging

from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, CallbackQuery
from aiogram.utils.markdown import hbold
from aiogram.filters import Command

from keyboards.inline_button import inline_keyboard
from parsing_script import get_product_info

from handlers.start import MENU
from models import SessionLocal, QueryHistory

session = SessionLocal()

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


@router.message(Article.choosing_article, Command('cancel'))
async def cancel(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Операция отменена.")


@router.message(Article.choosing_article)
async def get_info_goods(message: Message, state: FSMContext):
    article = message.text.lower()
    goods = await get_product_info(article)
    if goods == 'Ошибка в обработке данных':
        await message.answer(
            text="Такого артикула не существует.\nПопробуй еще раз",
            reply_markup=inline_keyboard().as_markup(),
        )
        await state.set_state(Article.choosing_article)
    else:
        with SessionLocal() as session:
            session.add(
                QueryHistory(
                    user_id=message.from_user.id,
                    article=article,
                )
            )
            session.commit()

        goods_string = ", \n".join([f"{hbold(key)} - {value}" for key, value in goods.items()])
        await message.answer(
            text=goods_string,
            reply_markup=inline_keyboard().as_markup(),
        )


@router.message(F.text.in_(MENU[2]))
async def get_data_db(message: Message, state: FSMContext):
    query_results = session.query(QueryHistory).all()[-5:]
    if query_results:
        for query in query_results:
            formatted_time = query.query_time.strftime("%Y-%m-%d %H:%M")
            await message.answer(
                text=(
                    f"{hbold('id пользователя')} - {query.user_id}\n"
                    f"{hbold('время запроса')} - {formatted_time}\n"
                    f"{hbold('артикул товара')} - {query.article}\n"
                ),
                reply_markup=inline_keyboard().as_markup(),
            )
    else:
        await message.answer(
                text=("Пока нет данных в БД"),
                reply_markup=inline_keyboard().as_markup(),
            )


from tasks import periodic_task


@router.callback_query(F.data == 'subscribe')
async def send_notification(callback: CallbackQuery):
    user_id = callback.from_user.id
    user_query_history = session.query(QueryHistory).filter(QueryHistory.user_id == user_id).order_by(QueryHistory.query_time.desc()).first()
    if user_query_history and user_query_history.subscribed is False:
        article = user_query_history.article
        periodic_task.apply_async(args=[user_id, article])
        user_query_history.subscribed = True
        session.commit()
        session.close()
        await callback.message.answer('Вы подписались на рассылку!')
        logging.info(f'Пользователь {user_id} подписался на рассылку')
    elif user_query_history is None:
        await callback.message.answer(
            text="Вас нет в базе данных. После первого запроса по артикулу, вы появитесь в БД",
            reply_markup=inline_keyboard().as_markup(),
        )
    else:
        await callback.message.answer(
            text="Вы уже подписаны на рассылку.",
            reply_markup=inline_keyboard().as_markup(),
        )


@router.message(F.text.in_(MENU[1]))
async def unsubscribe(message: Message, state: FSMContext):
    user_id = message.from_user.id
    user_query_history = session.query(QueryHistory).filter(QueryHistory.user_id == user_id).order_by(QueryHistory.query_time.desc()).first()
    if user_query_history and user_query_history.subscribed is True:
        user_query_history.subscribed = False
        session.commit()
        await message.answer(
            text="Вы отписались от рассылки!",
            reply_markup=inline_keyboard().as_markup(),
        )
        logging.info(f'Пользователь {user_id} отписался от рассылки')
    else:
        await message.answer(
            text="Вы не подписаны на рассылку.",
            reply_markup=inline_keyboard().as_markup(),
        )
