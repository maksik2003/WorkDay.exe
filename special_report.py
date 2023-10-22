from date_and_time import my_datetime
import sqlite3
import xlrd, xlwt

"""
Модуль для генерации специального отчета, который будет подаваться в отдел кадров.
Скорее всего придется "читать файл", а после в определенные поля дописывать данные по сорудникам.
В этом файле слишком много настроек, выгоднее которые просто скопировать с какого-то шаблона

pyexcel - может сохранять как?
pyexcel.save_as(dest_file_name='file_name.xlsx') Format may be csv, ods, odt, xlsx, xlsm. Can be xls?
"""

TEST_MODE = True

class special_report:

    def __init__(self, connect, cursor, user=None) -> None:

        self.connect    = connect
        self.cursor     = cursor
        
        if not TEST_MODE:
            self.user       = user
            self.writeLogs()

        elif TEST_MODE:
            print('[!] Тестовый режим. Запись в логи не ведется')

    def writeLogs(self) -> None:
        """Запись логов о генерации специального отчета"""

        time = my_datetime.date_datetime('06.12.2021 09:00', mode = 'now').format_standart
        self.user.insert_log(self.user.my_id, time, 'Generating special report')

    def getDataFromDB(self, start_date, end_date, ou_name) -> dict:
        """Получение данных из БД и составление их в определенном виде"""

        data = {}

        dataList = self.cursor.execute("SELECT username, date, worked_hours FROM SpecialReports WHERE date >= '{start_date}' AND date <= '{end_date}' AND ou_name = '{ou_name}'".format(
            start_date = start_date,
            end_date = end_date,
            ou_name = ou_name
        )).fetchall()

        # Проставляем дни, в которые сотрудник присутствовал
        for user in dataList:
            username        = user[0]
            date            = int(user[1][8:])
            worked_hours    = user[2]

            if username not in data:
                data[username] = {}

            if date not in data[username]:
                data[username][date] = float(worked_hours)

        monthLen = my_datetime.date_datetime(start_date, 'date').monthLen

        # Добавляем каждому сотруднику дни, в которые он отсутствовал
        for user in data:
            for day in range(1, monthLen + 1):
                if day not in data[user]:
                    data[user][day] = 0

        print(data)

    def generateFile(self, templatePath: str) -> None:
        
        book = xlrd.open_workbook(templatePath)
        sheet = book.sheet_by_index(0)

        sheet.write(0,7, 'мяф')
        book.save(r"E:\WorkDay\reportTemplates\templateE2000-copy.xls")

if __name__ == '__main__':
    connect = sqlite3.connect(r'\\x3.corp.motiv\support$\it_lunatic\Разработка\Python\workday.sqlite', check_same_thread=False)
    cursor = connect.cursor()
    report = special_report(connect, cursor)
    report.getDataFromDB('2023-09-01', '2023-09-11', 'Айтими')
    report.generateFile(r"E:\WorkDay\reportTemplates\templateE2000.xls")