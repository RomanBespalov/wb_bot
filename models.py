from sqlalchemy import create_engine, Column, Integer, String, DateTime, Boolean
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime
import pytz

Base = declarative_base()


class QueryHistory(Base):
    __tablename__ = 'query_history'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=True)
    query_time = Column(DateTime, default=datetime.now(pytz.timezone('Asia/Yerevan')))
    article = Column(String, nullable=True)
    subscribed = Column(Boolean, default=False)


timezone = pytz.timezone('Asia/Yerevan')

engine = create_engine("postgresql+psycopg2://wb_bot:wb_bot_2024@localhost/wb_bot")
Base.metadata.create_all(bind=engine)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

QueryHistory.objects = sessionmaker(autocommit=False, autoflush=False, bind=engine)()
