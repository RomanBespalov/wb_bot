from celery import Celery
from celery.schedules import crontab
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

def schedule_periodic_task(user_id, message_text, schedule_delay=10):
    # Вы можете использовать параметры в функции send_task для настройки условий запуска
    app.send_task("tasks.periodic_task", args=(user_id, message_text), countdown=schedule_delay)


@app.task
def periodic_task(user_id, message_text):
    asyncio.run(send_notification_message(user_id, message_text))
from handlers.article import QueryHistory, session


async def send_notification_message(user_id, message_text):
    """Отправляем напоминалку"""
    from main import get_bot
    bot = get_bot()
    user_query_history = session.query(QueryHistory).filter(QueryHistory.user_id == user_id).order_by(QueryHistory.query_time.desc()).first()
    logger.info(user_query_history.subscribed)
    if user_query_history.subscribed is True:
        await bot.send_message(user_id, message_text)
        schedule_periodic_task(user_id, message_text)
