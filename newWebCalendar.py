import datetime
import calendar
import pandas as pd
from sys import platform

###################################################
## Main function to create HTML-page of calendar ##
###################################################
# By parsing csv-file it creates html-page with
# calendar, with marked dates. The calendar's first 
# week is always the week with today date.

# fileNameEvents = 'fitosEvents.csv'
def createHTMLFile(fileNameEvents, iMsg):

    # initializing main variables
    curData = datetime.datetime.today()
    weeks2Show = 6
    mainTable = [[0,0,0,0,0,0,0],
                 [0,0,0,0,0,0,0],
                 [0,0,0,0,0,0,0],
                 [0,0,0,0,0,0,0],
                 [0,0,0,0,0,0,0],
                 [0,0,0,0,0,0,0]]
    month_names = ['Январь','Февраль','Март','Апрель','Май','Июнь','Июль','Август','Сентябрь','Октябрь','Ноябрь','Декабрь']
    if curData.month==1:
        prevMonth = 12
        prevYear = curData.year - 1
    else:
        prevMonth = curData.month - 1
        prevYear = curData.year
    
    if curData.month==12:
        nextMonth = 1
        nextYear = curData.year + 1
    else:
        nextMonth = curData.month + 1
        nextYear = curData.year
       
    if nextMonth==12:
        nextMonth2 = 1
        nextYear2 = nextYear + 1
    else:
        nextMonth2 = nextMonth + 1
        nextYear2 = nextYear

    curCalendar = calendar.TextCalendar(calendar.MONDAY)
    prevMonthArr = calendar.monthcalendar(prevYear,prevMonth)
    curMonthArr  = calendar.monthcalendar(curData.year,curData.month)
    next1Month   = calendar.monthcalendar(nextYear,nextMonth)
    next2Month   = calendar.monthcalendar(nextYear2,nextMonth2)
    
    for i in range(7):
        if curMonthArr[0][i] == 0:
            curMonthArr[0][i] = prevMonthArr[-1][i]
    
    flagNext = 0
    for i in range(7):
        if curMonthArr[-1][i] == 0:
            curMonthArr[-1][i] = next1Month[0][i]
            flagNext = 1
    
    # information to fill the first week
    curMonthToCheckWeek = []
    
    for i in curCalendar.itermonthdays(curData.year,curData.month):
        curMonthToCheckWeek.append(i)
        if i == curData.day:
            break
    flagNext2 = 0
    for i in range(7):
        if next1Month[-1][i] == 0:
            next1Month[-1][i] = next2Month[0][i]
            flagNext2 = 1
    
    for i in range(len(next2Month)-1):
        if flagNext2 == 0:
            next1Month.append(next2Month[i][:])
        else:
            next1Month.append(next2Month[i+1][:])
    
    curWeek = (len(curMonthToCheckWeek)-1)//7
    
    for i in range(7):
        mainTable[0][i] = curMonthArr[curWeek][i]
    
    # filling calendar with other weeks
    for i in range(len(curMonthArr) - curWeek-1):
        mainTable[1 + i][:] = curMonthArr[curWeek+1+i][:]
    
    for i in range(weeks2Show - (len(curMonthArr) - curWeek)):
        if flagNext==1:
            mainTable[len(curMonthArr) - curWeek + i][:] = next1Month[i+1][:]
        else:
            mainTable[len(curMonthArr) - curWeek + i][:] = next1Month[i][:]
    
    # parsing dates
    markDate = [[0,0,0,0,0,0,0],
             [0,0,0,0,0,0,0],
             [0,0,0,0,0,0,0],
             [0,0,0,0,0,0,0],
             [0,0,0,0,0,0,0],
             [0,0,0,0,0,0,0]]
    df = pd.read_csv(fileNameEvents, sep=',', header=None)
    df1 = df
    eventsCount = len(df[0])
    for i in range(eventsCount):
        date1 = df[0][i].split('.')
        date2 = df[3][i].split(':')
        df1[0][0+i:1+i] = df[0][0+i:1+i].replace(df[0][i],datetime.datetime(int(date1[2]),int(date1[1]),int(date1[0]), int(date2[0]), int(date2[1])))
        #df1[1][0+i:1+i] = df[1][0+i:1+i].replace(df[1][i],datetime.date(int(date2[2]),int(date2[1]),int(date2[0])))
    
    # sort starting date    
    #df = df.sort_values(by=0, ascending=True)
    jjj = 0
    flagMarkNextMonth = 0
    strDates = []
    strTimes = []
    strDates2 = []
    for j in range(0,8-curData.isoweekday()):
        if flagMarkNextMonth == 1:
            print(1)
            data2Mark = datetime.date(nextYear,nextMonth, j-jjj)
        else:
            data2Mark = datetime.date(curData.year, curData.month, curData.day+j)
            jjj=j
        if curData.day+j+1 > calendar.monthrange(curData.year, curData.month)[1]:
            flagMarkNextMonth = 1
            
        for i in range(eventsCount):
            #if ((df[0][i] == datetime.date(nextYear,nextMonth,calendar.monthrange(nextYear, nextMonth)[1])) or (df1[0][i] >= datetime.date(curData.year,curData.month, curData.day))):
            if (df[0][i].date()==data2Mark): # or df1[1][i]==data2Mark
                markDate[0][curData.isoweekday()+j-1] = 1
                strDates.append(df[2][i])
                strTimes.append(df[3][i])
                strDates2.append(data2Mark)
    for ij in range(1,weeks2Show):
        for j in range(7):
                   
            if flagMarkNextMonth == 1:
                
                if mainTable[ij][j]+1 > calendar.monthrange(nextYear, nextMonth)[1]:
                    flagMarkNextMonth = 2
                else:
                    data2Mark = datetime.date(nextYear,nextMonth, mainTable[ij][j])
            elif flagMarkNextMonth == 2:
                data2Mark = datetime.date(nextYear2,nextMonth2, mainTable[ij][j])
            elif flagMarkNextMonth == 0:
                data2Mark = datetime.date(curData.year, curData.month, mainTable[ij][j])
                jjj=j
                if mainTable[ij][j]+1 > calendar.monthrange(curData.year, curData.month)[1]:
                    flagMarkNextMonth = 1
               
            for i in range(eventsCount):
                # print(data2Mark)
                #if ((df[0][i] == datetime.date(nextYear,nextMonth,calendar.monthrange(nextYear, nextMonth)[1])) or (df1[0][i] >= datetime.date(curData.year,curData.month, curData.day))):
                if (df[0][i].date()==data2Mark): # or df1[1][i]==data2Mark
                    markDate[ij][j] = 1
                    strDates.append(df[2][i])
                    strTimes.append(df[3][i])
                    strDates2.append(data2Mark)
    
    HTMLFileString = ''
    mainHtmlString = ''
    eventsHtmlString = ''
    p = 0
    
    string1 = '<!DOCTYPE html> <html lang="ru"> <head> <meta charset="UTF-8"> <meta name="viewport" content="width=device-width, initial-scale=1.0"> <meta http-equiv="X-UA-Compatible" content="ie=edge"> <meta http-equiv="Refresh" content="15" /> <title>Calendar</title> <link href="https://fonts.googleapis.com/css?family=Montserrat:400,600,700" rel="stylesheet"> <link rel="stylesheet" type="text/css" href="style.css"> </head> <body> <div class="main-container-wrapper"> <div class="main-container-subwrapper-1"> <div class="calendar-container"> <div class="calendar-container__header"> <button class="calendar-container__btn calendar-container__btn--left" title="Previous"> <i class="icon ion-ios-arrow-back"></i> </button>'
    header1 = '<h2 class="calendar-container__title">'+month_names[curData.month-1]+'</h2>'
    string2 = '<button class="calendar-container__btn calendar-container__btn--right" title="Next"> <i class="icon ion-ios-arrow-forward"></i> </button> </div> <div class="calendar-container__body"> <div class="calendar-table"> <div class="calendar-table__header"> <div class="calendar-table__row"> <div class="calendar-table__col">Пн</div> <div class="calendar-table__col">Вт</div> <div class="calendar-table__col">Ср</div> <div class="calendar-table__col">Чт</div> <div class="calendar-table__col">Пт</div> <div class="calendar-table__col">Сб</div> <div class="calendar-table__col">Вс</div> </div> </div> <div class="calendar-table__body">'

    #first week with today check separately to mark previous days shadowed

    mainHtmlString = mainHtmlString + '<div class="calendar-table__row">'
    flagWasToday = 0
    for j in range(7):
        if mainTable[0][j] == curData.day:
            flagWasToday = 1
            if markDate[0][j] == 1:
                mainHtmlString = mainHtmlString + '<div class="calendar-table__col calendar-table__event calendar-table__today"><div class="calendar-table__item"><span>'+str(mainTable[0][j])+'</span></div></div>'
            else:
                mainHtmlString = mainHtmlString + '<div class="calendar-table__col calendar-table__today"><div class="calendar-table__item"><span>'+str(mainTable[0][j])+'</span></div></div>'
        else:
            if flagWasToday == 0:
                if markDate[0][j] == 1:
                    mainHtmlString = mainHtmlString + '<div class="calendar-table__col calendar-table__event calendar-table__inactive"><div class="calendar-table__item"><span>'+str(mainTable[0][j])+'</span></div></div>'
                else:
                    mainHtmlString = mainHtmlString + '<div class="calendar-table__col calendar-table__inactive"><div class="calendar-table__item"><span>'+str(mainTable[0][j])+'</span></div></div>'
            else:
                if markDate[0][j] == 1:
                    mainHtmlString = mainHtmlString + '<div class="calendar-table__col calendar-table__event"><div class="calendar-table__item"><span>'+str(mainTable[0][j])+'</span></div></div>'
                else:
                    mainHtmlString = mainHtmlString + '<div class="calendar-table__col"><div class="calendar-table__item"><span>'+str(mainTable[0][j])+'</span></div></div>'
    mainHtmlString = mainHtmlString + '</div>'

    for ij in range(1, weeks2Show):
        mainHtmlString = mainHtmlString + '<div class="calendar-table__row">'
        for j in range(7):
            if markDate[ij][j] == 1:
                mainHtmlString = mainHtmlString + '<div class="calendar-table__col calendar-table__event"><div class="calendar-table__item"><span>'+str(mainTable[ij][j])+'</span></div></div>'
                eventsHtmlString = eventsHtmlString + '<li class="events__item"><div class="events__item--left"><span class="events__name">' + strDates[p] + '</span><span class="events__date">' + str(strDates2[p])[5::] + '</span></div><span class="events__tag">'+strTimes[p]+'</span></li>'
                p = p + 1
            else:
                mainHtmlString = mainHtmlString + '<div class="calendar-table__col"><div class="calendar-table__item"><span>'+str(mainTable[ij][j])+'</span></div></div>'
            
        mainHtmlString = mainHtmlString + '</div>'
    
    string3 = '</div> </div> </div> </div> <div class="events-container"> <span class="events__title">Ближайшие события</span> <ul class="events__list">'
    string4 = '</ul> </div> </div> <div class="main-container-subwrapper-2"> <div class="events__veryitem"> <span> '+str(iMsg)+'</span> </div> </div> </div> </body> </html>'
    
    HTMLFileString = string1 + header1 + string2 + mainHtmlString + string3 + eventsHtmlString + string4
    if platform == 'linux':
        f1 = open('index_test.html', mode='w')
    else:
        f1 = open('index_test.html', mode='w')
    f1.write(HTMLFileString)
    f1.close()





