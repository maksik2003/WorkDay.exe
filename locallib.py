import datetime

def now(argument):
    '''
    argument может быть:
    :argument date: - только дата
    :argument time: - только время
    :argument date_and_time: - и дата и время
    :argument day: - день
    :argument month: - месяц
    :argument year: - год
    :argument hour: - час
    :argument minute: - минута
    :argument date_for_sqlite: - дата в формате YYYY-MM-DD
    '''
    if argument == 'date':
        return str(datetime.datetime.now().day) + '.' + str(datetime.datetime.now().month) + '.' + str(datetime.datetime.now().year)
        
    elif argument == 'time':
        hour = datetime.datetime.now().hour
        if hour < 10:
            hour = '0' + str(hour)
        
        minute = datetime.datetime.now().minute
        if minute < 10:
            minute = '0' + str(minute)

        return str(hour) + ':' + str(minute)
        
    elif argument == 'date_and_time':
        now_year = datetime.datetime.now().year

        now_month = datetime.datetime.now().month
        if now_month < 10:
            now_month = '0' + str(now_month)

        now_day = datetime.datetime.now().day
        if now_day < 10:
            now_day = '0' + str(now_day)
        
        now_hour = datetime.datetime.now().hour
        if now_hour < 10:
            now_hour = '0' + str(now_hour)

        now_minute = datetime.datetime.now().minute
        if now_minute < 10:
            now_minute = '0' + str(now_minute)
        return  str(now_day) + '.' + str(now_month) + '.' + str(now_year) + ' ' + str(now_hour) + ':' + str(now_minute)
        
    elif argument == 'day':
        return str( datetime.datetime.now().day )
        
    elif argument == 'month':
        return str( datetime.datetime.now().month )
        
    elif argument == 'year':
        return str( datetime.datetime.now().year )
        
    elif argument == 'hour':
        return str( datetime.datetime.now().hour )
        
    elif argument == 'minute':
        return str( datetime.datetime.now().minute )
        
    elif argument == 'date_for_sqlite':
        day = datetime.datetime.now().day
        if day < 10:
            day = '0' + str( day )

        month = datetime.datetime.now().month
        if month < 10:
            month = '0' + str( month )
        
        return now('year') + '-' + str( month ) + '-' + str( day )
    else:
        return now('date_and_time')

def len_month():
    if not int( now('year') ) % 4:
        # Если год не высокосный
        len_of_month = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    elif int( now('year') ) % 4 > 0:
        # Если год высокосный
        len_of_month = [31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    return len_of_month[ int( now('month') ) ]