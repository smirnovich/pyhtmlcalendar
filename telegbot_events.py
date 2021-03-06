#!/usr/bin/python3

import telebot
from telebot import types
import datetime
from dateutil.parser import parse
#from telegramcalendar import create_calendar
import pandas as pd
import newWebCalendar
import time
import threading
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
updateTimer = 0
lastImportantMessage = 'Здесь выводятся важные сообщения'

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

def csvEmpty(str):
    """
    Return whether csv-file has any string or not

    :param string: str, name of the csv-file, e.g. 'myEvents.csv'
    :param fuzzy: bool, ignore unknown tokens in string if True
    """
    try:
        df = pd.read_csv(str,header=None, sep=',')
        return False
    except ValueError:
        return True




@bot.message_handler(commands=['start'])
def start(message):
    start = telebot.types.ReplyKeyboardMarkup(True, False)
    #messageStart = bot.send_message(message.chat.id, 'Пришлите дату мероприятия в формате DD.MM.YYYY')
    start.row('Создать мероприятие')
    start.row('Показать список мероприятий')
    start.row('Срочное сообщение')
    if message.chat.id==TO_CHAT_ID:
        start.row('Удалить мероприятие')
    messageStart = bot.send_message(message.from_user.id, 'Выберите действие', reply_markup=start)
    bot.register_next_step_handler(messageStart, getCommand)
"""
Draft for future releases:

# processing continuos events
def second_date(message):


# administration processing
def admin(message):
"""
# important messages (below the calendar)
# add ability to set what time it can be alive (up to a day)
def breakingMessage(message):
    newWebCalendar.createHTMLFile('fitosEvents.csv', message.text)
    global lastImportantMessage 
    lastImportantMessage = str(message.text)
    messageErr = bot.send_message(message.chat.id, 'Сообщение опубликовано')
    bot.register_next_step_handler(messageErr, getCommand)


# autoupdate for html-file need to run in parallel
def updateCalendar():
    global updateTimer
    if updateTimer == 5:
        updateTimer = 0
        newWebCalendar.createHTMLFile('fitosEvents.csv', lastImportantMessage)
       # print(datetime.datetime.today())
      #  print('Calendar updated')
    else:
        time.sleep(4)
        updateTimer = updateTimer + 1
    thread1 = threading.Thread(target=updateCalendar)
    thread1.start()
 

def getCommand(message):
    if message.text == 'Создать мероприятие':
        messageStart = bot.send_message(message.chat.id, 'Пришлите дату мероприятия в формате DD.MM.YYYY')
        bot.register_next_step_handler(messageStart, eventDate)
    elif message.text == 'Показать список мероприятий':
        if (csvEmpty('fitosEvents.csv')):
            messageStart = bot.send_message(message.chat.id, 'Все мероприятия прошли, а новых еще не создали')
            bot.register_next_step_handler(messageStart, getCommand)
        else:
            df = pd.read_csv('fitosEvents.csv',header=None, sep=',')
            listDates = ''
            for i in range(len(df)):
                listDates =listDates+str(i) + ') ' +df[0][i] + ' '+df[2][i]+'\n'
            message1 = bot.send_message(message.chat.id, listDates)
            bot.register_next_step_handler(message1, getCommand)
    elif (message.text == 'Удалить мероприятие'):
        if message.chat.id == mainInfo.whomReplay:
            if (csvEmpty('fitosEvents.csv')):
                messageStart = bot.send_message(message.chat.id, 'Все мероприятия прошли, а новых еще не создали')
                bot.register_next_step_handler(messageStart, getCommand)
            else:
                messageErr = bot.send_message(message.chat.id, 'Введите номер записи для удаления:')
                bot.register_next_step_handler(messageErr, deleteEvent)
        else:
            messageErr = bot.send_message(message.chat.id, 'Данная команда Вам недоступна, выберите другую')
            bot.register_next_step_handler(messageErr, getCommand)
    elif(message.text == 'Срочное сообщение'):
        message1 = bot.send_message(message.chat.id, 'Введите сообщение')
        bot.register_next_step_handler(message1, breakingMessage)
    else:
        bot.send_message(message.chat.id, 'Неверная команда! Выберите из меню')

def deleteEvent(message):
    # csv-file editing (admin privelege)
    if message.text.isdigit()==False:
        messageErr = bot.send_message(message.chat.id, 'Введены некорректные данные. Начните сначала')
        bot.register_next_step_handler(messageErr, getCommand)
    else:
        df = pd.read_csv('fitosEvents.csv', header=None)
        # Backup deleted events
        f1 = open('fitosDeletedEvents.csv', 'a')
        f1.write(df[0][int(message.text)]+' '+df[1][int(message.text)]+' '+df[2][int(message.text)]+' '+df[3][int(message.text)]+'\n')
        f1.close()
        df = df.drop([int(message.text)])
        df.to_csv('fitosEvents.csv', sep=',',header=None, index=None)
        messageErr = bot.send_message(message.chat.id, 'Мероприятие удалено')
        bot.register_next_step_handler(messageErr, getCommand)
        newWebCalendar.createHTMLFile('fitosEvents.csv', lastImportantMessage)

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
    eventsFile = pd.DataFrame([[dateEnd,dateEnd,message.text,timeEvent]])
    eventsFile.to_csv('./fitosEvents.csv', header=None, index=None, mode='a')
    print(eventsFile)
    messageEventCreated = bot.send_message(message.chat.id, 'Спасибо! внесено в список.')
    bot.register_next_step_handler(messageEventCreated, getCommand)
    bot.forward_message(TO_CHAT_ID, message.chat.id, message.message_id)
    newWebCalendar.createHTMLFile('fitosEvents.csv',lastImportantMessage)

# updateCalendar()
thread1 = threading.Thread(target=updateCalendar)
thread1.start()

if __name__ == '__main__':
    bot.infinity_polling()
    
