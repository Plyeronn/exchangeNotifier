import time
from aiogram import Bot, Dispatcher, executor, types
from config import token, user_id
from aiogram.utils.markdown import hbold, hunderline, hcode, hlink
from aiogram.dispatcher.filters import Text
from parser import get_current_news
import asyncio
import datetime as dt
from threading import Thread



from user import User
from base import Session, engine, Base
from article import Article

bot = Bot(token=token, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)
start_buttons = ["All news", "Last five", "Fresh news"]
users = {}
# try:
# time.sleep(10)
Base.metadata.create_all(engine)
session = Session()
# except Exception as error:

@dp.message_handler(commands="start")
async def start(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*start_buttons)
    
    # if (session.query(User).filter(User.id == message.chat.id) is None):
    add_user(message.chat.id)
    
    await message.answer("News list", reply_markup=keyboard)


@dp.message_handler(Text(equals=start_buttons[0]))
async def get_all_news(message: types.Message):

    # for k, v in sorted(news_dict.items(), key=lambda x : int(x[1]['article_time']), reverse=True):
        #news = f"<b>{v['article_date']}</b> - {v['article_time']}\n<u>{v['article_title']}</u>\n\n<code>{v['article_desc']}</code>\n\n{v['article_url']}"
    for article in session.query(Article).all():   
        news = article_to_text(article)

        await message.answer(news)


@dp.message_handler(Text(equals=start_buttons[1]))
async def get_last_five_news(message: types.Message):
  
    # for k, v in sorted(news_dict.items(), key=lambda x : int(x[1]['article_time']), reverse=False)[-5:]:

    # list(news_dict.items())[-5:]:
    for article in session.query(Article).limit(5):
        art = article_to_text(article)

        await message.answer(art)



# from here
# fresh news for current user?
@dp.message_handler(Text(equals=start_buttons[2]))
async def get_fresh_news(message: types.Message):
    current_news = get_current_news()
    if len(current_news) > 0:
        for k, v in current_news.items():
            news = article_to_text(v)
            update_user_seen(message.chat.id, time.time())
            await message.answer(news)
    else:
        await message.answer("no fresh news")

@dp.message_handler(commands="stop")
async def stop(message: types.Message):
    session.query(User).filter_by(id = message.chat.id).first().status = "inactive"
    print("User leaved channel")
    session.commit()

@dp.message_handler(commands="showuser")
async def stop(message: types.Message):
    users = session.query(User).all()
    print('\n### All users:')
    idmes = f'your id : {message.chat.id}'
    await message.answer(idmes)
    for user in users:    
        timestamp_created = dt.datetime.fromtimestamp(user.time_created).strftime('%Y-%m-%d %H:%M:%S')
        timestamp_seen = dt.datetime.fromtimestamp(user.last_seen).strftime('%Y-%m-%d %H:%M:%S')
        news = f'{user.id} was registered on {timestamp_created} : {user.status} - last seen: {timestamp_seen}'
        # print('\n')
        await message.answer(news)

async def updating_db():
    while True:
        current_news = get_current_news()
        if len(current_news) > 0:
            for k, v in current_news.items():
        # print(v['article_title'])
                if (not news_contain(k)):
                    print(f"\n\n\n\n{k}\n\n\n\n")
                    session.add(Article(k,v['article_title'], v['article_date'], v['article_time'], v['article_link'], v['article_description']))
                    for user in session.query(User).yield_per(10).enable_eagerloads(False): 
                        if user.status == "active":
                            await bot.send_message(user.id, article_to_text(v)) 

        print("DB updated")
        session.commit()
        # await asyncio.sleep(60)
        time.sleep(5)

def article_to_text(article):
    if (isinstance(article,Article)):
        return f"{hbold(article.release_date)}\n\n{hlink(article.title,article.link)}\n\n{article.description}"
    else:
        return f"{hbold(article['article_date'])}\n\n{hlink(article['article_title'],article['article_link'])}"


def update_user_seen(user_id, time):
    session.query(User).filter_by(id = user_id).first().last_seen = time


def add_user(user_id):
    if (not users_contain(user_id)):
        session.add(User(user_id, time.time(), "active"))
        print("User added")
    else:
        session.query(User).filter_by(id = user_id).first().status = "active"
        print("User revoked subscription")
    session.commit()

def news_contain(k) -> bool:
    return session.query(session.query(Article.id).filter_by(id = k).exists()).scalar()
def users_contain(k) -> bool:
    return session.query(session.query(User.id).filter_by(id = k).exists()).scalar()

if __name__ == "__main__":
    # t = Thread(target=updating_db)
    # t.start()
    # loop = asyncio.get_event_loop()
    # # loop.create_task(news_every_minute())
    # loop.create_task(updating_db())
    # loop.run_forever()

    executor.start_polling(dp)
    updating_db()