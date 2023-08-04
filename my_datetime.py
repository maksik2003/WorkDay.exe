import datetime
import re

class date_datetime:
    def __init__(self, date, mode: str = 'date'):
        # Определяем шаблон и переделываем в класс datetime
        self.mode = mode
        if self.mode == 'date':
            if re.match('(\d{1,2}).(\d{1,2}).(\d{4})', date) is not None:
                self.date = datetime.datetime(
                    year = int(date.split('.')[2]),
                    month = int(date.split('.')[1]),
                    day = int(date.split('.')[0])
                )
            
            elif re.match('(\d{4})-(\d{1,2})-(\d{1,2})', date) is not None:
                self.date = datetime.datetime(
                    year = int(date.split('-')[0]),
                    month = int(date.split('-')[1]),
                    day = int(date.split('-')[2])
                )

            elif date == 'today':
                self.date = datetime.datetime.now()

            else:
                print('Неверный формат')

        elif self.mode == 'class':
            self.date = date

        elif self.mode == 'time':
            if re.match('(\d{1,2}).(\d{1,2}).(\d{4}) (\d{2}):(\d{2})', date) is not None:
                self.date = datetime.datetime(
                    year = int(date.split(' ')[0].split('.')[2]),
                    month = int(date.split(' ')[0].split('.')[1]),
                    day = int(date.split(' ')[0].split('.')[0]),
                    hour = int(date.split(' ')[1].split(':')[0]),
                    minute = int(date.split(' ')[1].split(':')[1])
                )
            
            elif re.match('(\d{4})-(\d{1,2})-(\d{1,2}) (\d{2}):(\d{2})', date) is not None:
                self.date = datetime.datetime(
                    year = int(date.split(' ')[0].split('-')[0]),
                    month = int(date.split(' ')[0].split('-')[1]),
                    day = int(date.split(' ')[0].split('-')[2]),
                    hour = int(date.split(' ')[1].split(':')[0]),
                    minute = int(date.split(' ')[1].split(':')[1])
                )

        self.main()

    def main(self):
        # Определяем какой день недели
        self.weekday_list = ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота', 'Воскресенье']
        self.weekday_id = datetime.datetime.isoweekday(self.date) # Возвращает ID дня недели от 1 до 7 (Понедельник - Воскресенье соответственно)
        self.weekday_name = self.weekday_list[ self.weekday_id - 1 ]

        # Определяем название месяца в родительском падеже (Января, Февраля и т.д.)
        self.months_list_r = ['Января', 'Февраля', 'Марта', 'Апреля', 'Мая', 'Июня', 'Июля', 'Августа', 'Сентября', 'Октября', 'Ноября', 'Декабря']
        self.months_list = ['Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь', 'Июль', 'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь']
        self.month_name = self.months_list[ self.date.month - 1 ]
        self.month_name_r = self.months_list_r[ self.date.month - 1 ]

        # Определяем является ли день выходным
        if self.weekday_id in [6, 7]:
            self.isDayoff = True
        
        else:
            self.isDayoff = False

        # Возвращаем форматы
        month = self.date.month
        if month < 10:
            month = '0' + str(month)

        day = self.date.day
        if day < 10:
            day = '0' + str(day)
        
        self.format_standart = str(day) + '.' + str(month) + '.' + str(self.date.year)
        self.format_db = str(self.date.year) + '-' + str(month) + '-' + str(day)
        self.format_report = str(day) + ' ' + str(self.month_name_r) + ' ' + str(self.date.year)

        if self.mode in ['class', 'time']:
            hours = self.date.hour
            if hours < 10:
                hours = '0' + str(hours)

            minutes = self.date.minute
            if minutes < 10:
                minutes = '0' + str(minutes)
            self.format_standart += ' ' + str(hours) + ':' + str(minutes)
            self.format_db += ' ' + str(hours) + ':' + str(minutes)

        self.firstMonthDay = datetime.datetime(year = self.date.year, month = self.date.month, day = 1)

        # Проверяем високосный ли год
        if not self.date.year % 4:
            self.monthLen = [31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
            self.leapYear = True
        else:
            self.monthLen = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
            self.leapYear = False
            
        self.lastMonthDay = datetime.datetime(year = self.date.year, month = self.date.month, day = self.monthLen[self.date.month - 1])

    def add_day(self, days: int = 1):
        delta = datetime.timedelta(days = days)
        self.date += delta
        self.main()