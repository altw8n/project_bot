import logging
import sqlite3
from telegram.ext import Application, MessageHandler, filters
from data import db_session
from data.users import User
from telegram.ext import CommandHandler, ConversationHandler
from telegram import ReplyKeyboardMarkup, KeyboardButton
import random
from bs4 import BeautifulSoup
import requests
import base64



logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG
)

logger = logging.getLogger(__name__)

db_session.global_init("db/database.db")
db_sess = db_session.create_session()


reply_keyboard_start = [['/anecdote'],
                  ['/chat']]
reply_keyboard_2 = [['/search']]
reply_keyboard_3 = [['/signup']]
reply_keyboard_4 = [['/searching']]
reply_keyboard_5 = [['про компьютеры'],
                  ['про программистов'], ['советские'], ['/chat']]

markup = ReplyKeyboardMarkup(reply_keyboard_start, one_time_keyboard=False)
markup_2 = ReplyKeyboardMarkup(reply_keyboard_2, one_time_keyboard=False)
markup_3 = ReplyKeyboardMarkup(reply_keyboard_3, one_time_keyboard=True)
markup_4 = ReplyKeyboardMarkup(reply_keyboard_4, one_time_keyboard=False)
markup_5 = ReplyKeyboardMarkup(reply_keyboard_5, one_time_keyboard=False)

data = []


async def start(update, context):
    await update.message.reply_text(
        "Привет, что будешь делать?\n"
        "Отправь /anecdote если хочешь чтобы бот рассказал анекдот\n"
        "Или отправь /chat если хочешь чтобы бот подобрал тебе собеседников ",
        reply_markup=markup
    )


def user_exist(id):
    con = sqlite3.connect("db/database.db")
    cur = con.cursor()
    result = cur.execute("SELECT * FROM `users` WHERE `user_id` = ?", (id,)).fetchall()
    return bool(len(result))


def len_db():
    db_session.global_init("db/database.db")
    db_sess = db_session.create_session()
    count = 0
    for user in db_sess.query(User):
        count += 1
    return count


def text_format(name, desc, username):
    f1 = f'''{name}'''
    f2 = f'''О себе: {desc}'''
    f3 = f'''--> {username}'''
    return f1 + '\n' + f2 + '\n' + f3


n = 1


async def search(update, context):
    global n
    if n > len_db():
        n = 1
    user = db_sess.query(User).filter(User.id == n).first()
    chat_id = update.effective_chat.id
    file_id = user.photo_id
    await update.message.reply_html(text_format(user.name, user.description, user.username))
    await context.bot.send_photo(chat_id=chat_id, photo=file_id)
    n += 1


async def searching(update, context):
    user = update.effective_user
    if user_exist(user.id):
        await update.message.reply_text('Вы зарегестрированы')
        await update.message.reply_text("Начинаем поиск", reply_markup=markup_2)
    else:
        await update.message.reply_text('Вы не зарегестрированы')
        await update.message.reply_text("Зарегестрируйся", reply_markup=markup_3)


async def signup(update, context):
    await update.message.reply_text(
        "Как вас зовут?")
    return 1


async def first_response(update, context):
    name = update.message.text
    data.append(name)
    await update.message.reply_text(
        f"{name}, расскажите немного о себе")
    return 2


async def second_response(update, context):
    about = update.message.text
    data.append(about)
    await update.message.reply_text(
        f"{data[0]}, отправьте фото")
    return 3


async def last_response(update, context):
    global data
    photo1 = update.message.photo
    file_id = photo1[0].file_id
    chat_id = update.effective_chat.id
    print(file_id)
    #logger.info(about)
    db_session.global_init("db/database.db")
    db_sess = db_session.create_session()

    user_1 = update.effective_user
    user = User()
    user.name = data[0]
    user.user_id = user_1.id
    user.description = data[1]
    user.username = str(user_1.mention_html())
    user.chat_id = chat_id
    user.photo_id = file_id

    db_sess.add(user)
    db_sess.commit()
    await update.message.reply_text(
        "Регистрация прошла успешно")
    await update.message.reply_text("Начинаем поиск?", reply_markup=markup_2)
    print(data)
    data = []
    return ConversationHandler.END


async def stop(update, context):
    await update.message.reply_text("Всего доброго!")
    return ConversationHandler.END


async def anecdote(update, context):
    await update.message.reply_text("Выберите категорию", reply_markup=markup_5)


async def anecdote_type(update, context):
    if update.message.text == 'про компьютеры':
        r = requests.get('https://anekdotme.ru/anekdoti_sovetskie/page_13/')
        an = []
        page = BeautifulSoup(r.text, "html.parser")
        find = page.select('.anekdot_text')
        for text in find:
            page = (text.getText().strip())
            an.append(page)
        n = random.randint(1, len(an))
        await update.message.reply_text(an[n])
    elif update.message.text == 'про программистов':
        r = requests.get('https://anekdotme.ru/anekdoti_sovetskie/page_13/')
        an = []
        page = BeautifulSoup(r.text, "html.parser")
        find = page.select('.anekdot_text')
        for text in find:
            page = (text.getText().strip())
            an.append(page)
        n = random.randint(1, len(an))
        await update.message.reply_text(an[n])

    elif update.message.text == 'советские':
        anecdotes = []
        r = requests.get('https://anekdotme.ru/anekdoti_sovetskie/page_13/')
        page = BeautifulSoup(r.text, "html.parser")
        find = page.select('.anekdot_text')
        for text in find:
            page = (text.getText().strip())
            anecdotes.append(page)
        await update.message.reply_text(anecdotes[random.randint(1, 29)])


async def chat(update, context):
    user = update.effective_user
    await update.message.reply_html(
        rf"Привет {user.mention_html()}! жми на кнопку и начинаем", reply_markup=markup_4)


def main(): 
    application = Application.builder().token("6005111103:AAHcDu1ZeLJB5uc9ytEIjy1D1eQ5GcxVa6A").build()

    db_session.global_init("db/database.db")
    db_sess = db_session.create_session()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("search", search))
    application.add_handler(CommandHandler("searching", searching))
    application.add_handler(CommandHandler("anecdote", anecdote))
    application.add_handler(CommandHandler("chat", chat))


    conv_handler = ConversationHandler(

        entry_points=[CommandHandler('signup', signup)],

        states={
            1: [MessageHandler(filters.TEXT & ~filters.COMMAND, first_response)],
            2: [MessageHandler(filters.TEXT & ~filters.COMMAND, second_response)],
            3: [MessageHandler(filters.PHOTO & ~filters.COMMAND, last_response)]
        },

        fallbacks=[CommandHandler('stop', stop)]
    )

    application.add_handler(conv_handler)

    text_handler = MessageHandler(filters.TEXT, anecdote_type)

    application.add_handler(text_handler)

    application.run_polling()


if __name__ == '__main__':
    main()
