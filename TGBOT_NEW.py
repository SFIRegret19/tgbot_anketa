from telegram import ReplyKeyboardMarkup, Bot, ReplyMarkup, Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler, CallbackContext
from credits1 import bot_token
from PIL import Image, ImageFont, ImageDraw
import datetime
import random

bot = Bot(token=bot_token)
updater = Updater(token=bot_token)
dispatcher = updater.dispatcher

FIRST = 0
SECOND = 1
THIRD = 2
FOURTH = 4
FIFTH = 5
SIX = 6
SEVENS = 7
EIGHTS = 8
NINES = 9
TEN = 10

user = ''

font_size = ''
coord_x = ''
coord_y = ''
color = ''
colors = {
    'Белый':(255,255,255),
    'Красный':(255,0,0),
    'Зелёный':(0,255,0),
    'Синий':(0,0,255),
    'Чёрный':(0,0,0)
}
genderx = {
    'Мужчина':"Male",
    'Женщина':"Female"
}
timex_job = {
    '1 год':'1 year',
    '< 1 года':'< 1 year',
    '> 1 года':'> 1 year'
}
USERS = {

}
# 1) Имя
# 2) Фамилия
# 3) Возраст
# 4) ПОЛ
# 5) фото

def start(update, context):
    context.bot.send_message(update.effective_chat.id, 'Привет! Как тебя зовут (На английском)?')
    return FIRST


def name(update, context):
    global user
    context.bot.send_message(update.effective_chat.id, 'Приятно познакомиться, а какая фамилия (На английском)?')
    wall = open('wall.txt','a')
    wall.write(str(update.message.from_user['id']) + ' - ' + update.message.text + ', ')
    user += ('Name: ' + update.message.text + ' | ')
    return SECOND

def gender(update,context):
    global user
    reply_keyboard = [['Мужчина', 'Женщина']]
    update.message.reply_text('Укажите свой пол, вы мужчина или женщина?', reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
    wall = open('wall.txt','a')
    wall.write(update.message.text + ', ')
    user += ('Surname: ' + update.message.text + ' | ')
    return THIRD

def time_job(update,context):
    global user
    reply_keyboard = [['< 1 года', '1 год', '> 1 года']]
    update.message.reply_text('Ваш опыт работы?', reply_markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
    wall = open('wall.txt','a')
    wall.write(genderx[update.message.text] + ', ')
    user += ('Gender: ' + genderx[update.message.text] + ' | ')
    return FOURTH

def final(update, context):
    global user
    context.bot.send_message(update.effective_chat.id, 'Анкета готова')
    wall = open('wall.txt','a')
    wall.write(timex_job[update.message.text] + '\n')
    user += ('Time job: ' + timex_job[update.message.text])
    USERS[str(update.message.from_user['id'])] = user
    print(USERS)
    return ConversationHandler.END


start_handler = CommandHandler('start', start)
name_handler = MessageHandler(Filters.text, name)
final_handler = MessageHandler(Filters.text, final)
gender_handler = MessageHandler(Filters.text, gender)
time_job_handler = MessageHandler(Filters.text, time_job)


conv_handler = ConversationHandler(
    entry_points=[start_handler],
    states={
        FIRST: [name_handler],
        SECOND: [gender_handler],
        THIRD: [time_job_handler],
        FOURTH: [final_handler],

    }, fallbacks=[]
)

dispatcher.add_handler(conv_handler)

updater.start_polling()
updater.idle()
