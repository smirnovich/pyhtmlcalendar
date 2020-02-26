#!/usr/bin/python3

import telebot
from telebot import types
import datetime
from dateutil.parser import parse
#from telegramcalendar import create_calendar
import pandas as pd
import newWebCalendar

#here I store token from Telegram bot in separate file
import mainInfo

bot = telebot.TeleBot(mainInfo.botToken)
TO_CHAT_ID = mainInfo.whomReplay
mess = {}
mess_time = datetime.date.today()
current_shown_dates = {}
eventsFile = pd.DataFrame([])
eventsFile.to_csv('fitosEvents.csv', header=None, index_label=None, mode='a')
dateBegin = 0
timeEvent = 0
dateEnd = 0


def is_date(string, fuzzy=False):
    """
    Return whether the string can be interpreted as a date.

    :param string: str, string to check for date
    :param fuzzy: bool, ignore unknown tokens in string if True
    """
    try: 
        parse(string, fuzzy=fuzzy)
        return True

    except ValueError:
        return False



@bot.message_handler(commands=['start'])
def start(message):
    start = telebot.types.ReplyKeyboardMarkup(True, False)
    #messageStart = bot.send_message(message.chat.id, 'Пришлите дату мероприятия в формате DD.MM.YYYY')
    start.row('Создать мероприятие')
    start.row('Показать список мероприятий')
    start.row('Удалить мероприятие')
    messageStart = bot.send_message(message.from_user.id, 'Выбери действие', reply_markup=start)
    bot.register_next_step_handler(messageStart, getCommand)
""" def second_date(message):
    global dateBegin
    dateBegin = message.text
    if (is_date(dateBegin)):
        messageFinish = bot.send_message(message.chat.id, 'Пришлите дату окончания мероприятия в формате DD.MM.YYYY')
        bot.register_next_step_handler(messageFinish, eventDate)
    else:
        messageFinish = bot.send_message(message.chat.id, 'Дата неверна! попробуйте еще раз')
        bot.register_next_step_handler(messageFinish, second_date)
    print(dateBegin) """

def getCommand(message):
    if message.text == 'Создать мероприятие':
        messageStart = bot.send_message(message.chat.id, 'Пришлите дату мероприятия в формате DD.MM.YYYY')
        bot.register_next_step_handler(messageStart, eventDate)
    elif message.text == 'Показать список мероприятий':
        df = pd.read_csv('fitosEvents.csv',header=None, sep=',')
        listDates = ''
        for i in range(len(df)):
            listDates =listDates+str(i) + ' ' +df[0][i] + ' '+df[2][i]+'\n'
        message1 = bot.send_message(message.chat.id, listDates)
        bot.register_next_step_handler(message1, getCommand)
    elif (message.text == 'Удалить мероприятие'):
        if message.chat.id == mainInfo.whomReplay:
            messageErr = bot.send_message(message.chat.id, 'Введите номер записи для удаления:')
            bot.register_next_step_handler(messageErr, deleteEvent)
        else:
            messageErr = bot.send_message(message.chat.id, 'Данная команда Вам недоступна, выберите другую')
            bot.register_next_step_handler(messageErr, getCommand)
    else:
        bot.send_message(message.chat.id, 'Неверная команда! Выберите из меню')

def deleteEvent(message):
    messageErr = bot.send_message(message.chat.id, 'Мероприятие удалено')
    bot.register_next_step_handler(messageErr, getCommand)


def eventDate(message):
    global dateEnd
    dateEnd = message.text
    if (is_date(dateEnd)):
        checkDelta = datetime.datetime.strptime(dateEnd, '%d.%m.%Y') - datetime.datetime.today()
        if checkDelta.days < 0:
            messageEventName = bot.send_message(message.chat.id, 'Мероприятие уже прошло! введите другую дату')
            bot.register_next_step_handler(messageEventName, eventDate)
        else:
            messageEventName = bot.send_message(message.chat.id, 'В какое время начинается мероприятие?')
            bot.register_next_step_handler(messageEventName, eventTime)
    else:
        messageFinish = bot.send_message(message.chat.id, 'Дата неверна! попробуйте еще раз')
        bot.register_next_step_handler(messageFinish, eventDate)
    print(dateEnd)


def eventTime(message):
    global timeEvent
    timeEvent = message.text
    if (is_date(timeEvent)):
        messageEventName = bot.send_message(message.chat.id, 'Как называется мероприятие?')
        bot.register_next_step_handler(messageEventName, registerEvent)
    else:
        messageFinish = bot.send_message(message.chat.id, 'Время в неверном формате! Попробуйте еще раз')
        bot.register_next_step_handler(messageFinish, eventTime)
    print(timeEvent)
    

def registerEvent(message):
    eventsFile = pd.DataFrame([[dateEnd, timeEvent, message.text]])
    eventsFile.to_csv('./fitosEvents.csv', header=None, index=None, mode='a')
    print(eventsFile)
    messageEventCreated = bot.send_message(message.chat.id, 'Спасибо! внесено в список.')
    bot.register_next_step_handler(messageEventCreated, getCommand)
    bot.forward_message(TO_CHAT_ID, message.chat.id, message.message_id)
    newWebCalendar.createHTMLFile('fitosEvents.csv')

if __name__ == '__main__':
    bot.infinity_polling()
