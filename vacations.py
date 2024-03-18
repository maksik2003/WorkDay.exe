import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import datetime

from my_datetime import date_datetime

# Параметры для УЗ, которая будет использоваться для отправки почты
LOGIN = ''
PSW = ''

class Vacation:

    def __init__(self, cursor, connect) -> None:

        self.cursor = cursor
        self.connect = connect

        # Получаем настройки из БД
        login, password, server, port = [x[0] for x in self.cursor.execute("""
            SELECT value_text FROM options
            WHERE name IN ('mail_user', 'mail_user_password', 'mail_server', 'mail_server_port')
            ORDER BY id
        """).fetchall()]

        self.message_from = login + '@motivtelecom.ru'

        self.server = smtplib.SMTP(server, int(port))
        self.server.starttls()
        self.server.login(login, password)

    def createMessage(self, text, to, header=None) -> MIMEMultipart:
        """Формирование сообщения"""
        
        msg = MIMEMultipart()

        # msg['From'] = self.message_from
        msg['From'] = 'Информирование от WorkDay'
        msg['To'] = to
        msg['Subject'] = 'Информирование об отпуске'
        if header:
            msg['Subject'] = 'Информирование об отпуске ' + header
        msg.attach(MIMEText(text))

        return msg.as_string()

    def sendFirstNotification(self, to) -> None:
        """Отправка первичного уведомлении об отпуске (отправляется за 2 недели до отпуска)"""

        msg = self.createMessage(
            text="Через 2 недели у вас начнется отпуск, просьба написать заявление на отпуск (или на перенос отпуска) и отправить руководителю.",
            to=to
        )

        self.server.sendmail(self.message_from, to, msg)

    def sendSecondNotification(self, to) -> None:
        """Отправка 2го уведомления об отпуске, должно отправлятся за 3-4 дня до отпуска"""

        msg = self.createMessage(
            text="Скоро вы выходите в отпуск, не забудьте сообщить об этом коллегам",
            to=to
        )

        self.server.sendmail(self.message_from, to, msg)

    def sendBossNotification(self, to, employee_username, vacation_date) -> None:
        """Отправка уведомления руководителю об отпуске сотрудника"""

        # Форматирование ФИО сотрудника из Иванов Иван Иванович в Иванов И.И.
        employee_username = employee_username.split(' ')[0] + ' ' + employee_username.split(' ')[1][0] + '.' + employee_username.split(' ')[2][0] + '.'
        vacation_date = vacation_date.split('-')[2] + '.' + vacation_date.split('-')[1] + '.' + vacation_date.split('-')[0]
        msg = self.createMessage(
            text="Сотрудник " + employee_username + " с " + vacation_date + " выходит в отпуск. Скоро он должен направить вам заявление на отпуск",
            to=to,
            header=employee_username
        )

        self.server.sendmail(self.message_from, to, msg)

    def log(self, text) -> None:
        self.cursor.execute(f"""
            INSERT INTO logs(id_user, time, param)
            VALUES(53, (SELECT datetime('now', '+5 hours')), '{text}')
        """)
        self.connect.commit()

    def testMessage(self, to):
        
        """Формирование сообщения"""
        
        msg = MIMEMultipart()

        # msg['From'] = self.message_from
        msg['From'] = 'Краснов Владислав Геннадьевич'
        msg['To'] = 'Сотруднику года'
        msg['Subject'] = 'Информирование о премировании'
        msg.attach(MIMEText('Ты лучший сотрудник =)'))

        self.server.sendmail(self.message_from, to, msg.as_string())

    def auto(self) -> None:
        
        bossMail = self.cursor.execute("SELECT email FROM users WHERE id = (SELECT value FROM options WHERE name = 'boss_id')").fetchone()

        if not bossMail:
            self.log('При получении почты руководителя произошла ошибка, возвращено пустое значение')
            raise ValueError('При получении почты руководителя произошла ошибка, возвращено пустое значение')
        
        bossMail = bossMail[0]

        for vac in self.getVacations():
            _id         = vac[0]
            username    = vac[1]
            email       = vac[2]
            first_date  = vac[3]

            self.sendBossNotification(bossMail, username, first_date)
            self.log('Отправлено инфомирование руководителя на почту ' + bossMail + ' о предстоящем отпуске ' + str(_id))

            self.sendFirstNotification(email)
            self.log('Отправлено информирование сотрудника на почту ' + email + 'о его предстоящем отпуске ' + str(_id))

            self.cursor.execute(f"""
                UPDATE vacations
                SET first_notification = 1
                WHERE id = {str(_id)}
            """)
            self.connect.commit()

    def getVacations(self) -> tuple:
        """Получаем список сотрудников и их отпусков в ближайшее время"""

        vacationList = self.cursor.execute("""
            SELECT v.id, u.username, u.email, v.first_date FROM users u, vacations v
            WHERE 
            NOT u.deleted
            AND (v.first_date <= date('now', '+15 days') AND v.first_date >= date('now')) 
            AND NOT v.first_notification
            AND (u.id = v.id_user)
        """).fetchall()

        return vacationList

    def close(self) -> None:
        self.server.quit()

if __name__ == '__main__':

    import sqlite3
    connect = sqlite3.connect(r'\\x3.corp.motiv\support$\it_lunatic\Разработка\Python\workday.sqlite', check_same_thread=False)
    cursor = connect.cursor()

    test = Vacation(cursor, connect)
    # test.auto()
    test.testMessage('lunatic@motivtelecom.ru')
    test.close()

