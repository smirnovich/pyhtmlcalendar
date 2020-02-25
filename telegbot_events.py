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
    startKey = types.ReplyKeyboardMarkup(True, False)
    startKey.row('Создать мероприятие')
    messageStart = bot.send_message(message.chat.id, 'Пришлите дату мероприятия в формате DD.MM.YYYY')
    bot.register_next_step_handler(messageStart, eventName)


""" def second_date(message):
    global dateBegin
    dateBegin = message.text
    if (is_date(dateBegin)):
        messageFinish = bot.send_message(message.chat.id, 'Пришлите дату окончания мероприятия в формате DD.MM.YYYY')
        bot.register_next_step_handler(messageFinish, eventName)
    else:
        messageFinish = bot.send_message(message.chat.id, 'Дата неверна! попробуйте еще раз')
        bot.register_next_step_handler(messageFinish, second_date)
    print(dateBegin) """


def eventName(message):
    global dateEnd
    dateEnd = message.text
    if (is_date(dateEnd)):
        checkDelta = datetime.datetime.strptime(dateEnd, '%d.%m.%Y') - datetime.datetime.today()
        if checkDelta.days < 0:
            messageEventName = bot.send_message(message.chat.id, 'Мероприятие уже прошло! начните заново /start')
            bot.register_next_step_handler(messageEventName, start)
        else:
            messageEventName = bot.send_message(message.chat.id, 'Как называется мероприятие?')
            bot.register_next_step_handler(messageEventName, registerEvent)
    else:
        messageFinish = bot.send_message(message.chat.id, 'Дата неверна! попробуйте еще раз')
        bot.register_next_step_handler(messageFinish, start)
    print(dateEnd)
    

def registerEvent(message):
    eventsFile = pd.DataFrame([[dateEnd, dateEnd, message.text]])
    eventsFile.to_csv('./fitosEvents.csv', header=None, index=None, mode='a')
    print(eventsFile)
    messageEventCreated = bot.send_message(message.chat.id, 'Спасибо! внесено в список. Чтобы добавить мероприятие нажмите  /start')
    bot.register_next_step_handler(messageEventCreated, start)
    bot.forward_message(TO_CHAT_ID, message.chat.id, message.message_id)
    newWebCalendar.createHTMLFile('fitosEvents.csv')

if __name__ == '__main__':
    bot.infinity_polling()