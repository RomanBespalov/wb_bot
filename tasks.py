from celery import Celery
import logging
import asyncio
import sys

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Celery(
    "tasks",
    broker="redis://localhost:6379/0",
    include=["tasks"],
)
app.autodiscover_tasks()


sys.path.append('/Users/romanbespalov/Dev/wb_bot')


def schedule_periodic_task(user_id, article, schedule_delay=300):
    app.send_task("tasks.periodic_task", args=(user_id, article), countdown=schedule_delay)


@app.task
def periodic_task(user_id, article):
    asyncio.run(send_notification_message(user_id, article))


# from handlers.article import QueryHistory, session
from keyboards.inline_button import inline_keyboard
from parsing_script import get_product_info
from aiogram.utils.markdown import hbold

from models import SessionLocal, QueryHistory

session = SessionLocal()


async def send_notification_message(user_id, article):
    """Отправляем напоминалку"""
    from main import get_bot
    bot = get_bot()
    user_query_history = session.query(QueryHistory).filter(QueryHistory.user_id == user_id).order_by(QueryHistory.query_time.desc()).first()
    if user_query_history and user_query_history.subscribed is True:
        goods = get_product_info(article)
        goods_string = ", \n".join([f"{hbold(key)} - {value}" for key, value in goods.items()])
        await bot.send_message(
            user_id,
            text=goods_string,
            reply_markup=inline_keyboard().as_markup(),
        )
        schedule_periodic_task(user_id, article)
