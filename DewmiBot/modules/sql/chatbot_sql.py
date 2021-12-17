import threading

from sqlalchemy import Column, String
from DewmiBot.modules.sql import BASE, SESSION

class Chatbot(BASE):
    __tablename__ = "chatbot"
    chat_id = Column(String(14), primary_key=True)

    def __init__(self, chat_id):
        self.chat_id = chat_id


Chatbot.__table__.create(checkfirst=True)


def addchatbot(chat_id: str):
    chatbotty = Chatbot(str(chat_id))
    SESSION.add(chatbotty)
    SESSION.commit()


def rmchatbot(chat_id: str):
    rmchatbotty = SESSION.query(Chatbot).get(str(chat_id))
    if rmchatbotty:
        SESSION.delete(rmchatbotty)
        SESSION.commit()


def get_all_chat_id():
    stark = SESSION.query(Chatbot).all()
    SESSION.close()
    return stark


def is_chatbot_indb(chat_id: str):
    try:
        s__ = SESSION.query(Chatbot).get(str(chat_id))
        if s__:
            return str(s__.chat_id)
    finally:
        SESSION.close()
