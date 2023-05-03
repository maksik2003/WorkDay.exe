import sqlite3
import datetime
import getpass
import os

def create_db(db_path):
    connect = sqlite3.connect(db_path)
    cursor = connect.cursor()
    
    cursor.execute(
        # Creating table users
        """
            CREATE TABLE IF NOT EXISTS users(
                id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                login TEXT NOT NULL,
                username TEXT NOT NULL
            )
        """
        # isActive - 1 is active, 0 is not active
    )
    connect.commit()
    
    cursor.execute(
        # Creating table root (table with users root)
        """
            CREATE TABLE IF NOT EXISTS root(
                id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                id_user INTEGER NOT NULL UNIQUE,
                start_day BOOL NOT NULL,
                report BOOL NOT NULL,
                admin BOOL NOT NULL,
                inReport BOOL NOT NULL,
                FOREIGN KEY (id_user) REFERENCES users(id)
            )
        """
    )
    connect.commit()

    cursor.execute(
        # Creating table report (table with users report)
        """
            CREATE TABLE IF NOT EXISTS report(
                id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                id_user INTEGER NOT NULL,
                start_day DATE NOT NULL,
                start_dinner DATE NOT NULL,
                end_dinner DATE NOT NULL,
                end_day DATE NOT NULL,
                day_len REAL,
                dinner_len REAL,
                status TEXT,
                delete_reason TEXT,
                FOREIGN KEY (id_user) REFERENCES users(id)
            )
        """
        # status - auto (user forgot close day), edited (anywho change this record), deleted (if deleted)
    )
    connect.commit()

    cursor.execute(
        # Creating table logs
        """
            CREATE TABLE IF NOT EXISTS logs(
                id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                id_user INTEGER NOT NULL,
                time DATE NOT NULL,
                param TEXT NOT NULL,
                last_value TEXT NULL,
                new_value TEXT NULL,
                FOREIGN KEY (id_user) REFERENCES users(id)
            )
        """
        # param - add user, change user, change record, delete record 
        # time - YYYY.MM.DD HH:MM
    )
    connect.commit()

    cursor.execute(
        # Create table themes
        """
            CREATE TABLE IF NOT EXISTS themes (
                id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                id_user INTEGER UNIQUE REFERENCES users (id) NOT NULL,
                text_color TEXT NOT NULL DEFAULT ('#FFFFFF'),
                background TEXT NOT NULL DEFAULT ('#1C1D22'),
                rectangle TEXT NOT NULL DEFAULT ('#252525'),
                hover TEXT NOT NULL DEFAULT ('#75B2EF'),
                hover_negative TEXT NOT NULL DEFAULT ('#DF5D5D'),
                non_active_color TEXT NOT NULL DEFAULT ('#808080'),
                indicator_border TEXT NOT NULL DEFAULT ('#FFFFFF'),
                text_color_inverse TEXT NOT NULL DEFAULT ('#FFFFFF') 
            )
        """
    )
    connect.commit()

    creator_info = cursor.execute('SELECT * FROM users WHERE login = "it_lunatic"')

    if creator_info:
        cursor.execute(
            """
                INSERT INTO users(login, username) VALUES(
                    "it_lunatic",
                    "Пономарев Максим Владимирович"
                )
            """
        )
        connect.commit()

        cursor.execute(
            """
                INSERT INTO root(id_user, start_day, report, admin, inReport) VALUES(1, 0, 0, 1, 0)
            """
        )
        connect.commit()

def migrate_users(db_path):
    # Сбор пользователей из старой БД
    connect = sqlite3.connect(r"\\x3\support$\it_tomilis\Студенты\WorkDay\dontdelete.db")
    cursor = connect.cursor()
    data = cursor.execute('SELECT login, full_name, report_access, in_report FROM students WHERE id_student <> 1').fetchall()
    connect.close()

    # Устанавливаем соединение с новой БД и загружаем пользователей в табл. users и root
    con = sqlite3.connect(db_path)
    cur = con.cursor()
    for line in data:
        if line[2] == 'student':
            root_list = [1, 0, 0, 1]

        elif line[2] == 'report_access':
            root_list = [0, 1, 0, 0]

        elif line[2] == 'None':
            root_list = [1, 0, 0, 0]

        cur.execute(
            """
                INSERT INTO users(login, username) VALUES(
                    "{login}",
                    "{username}"
                )
            """.format(
                login = line[0],
                username = line[1]
            )
        )
        con.commit()

        id_user = cur.execute("SELECT id FROM users WHERE login = '{login}'".format(login = line[0])).fetchone()[0]
        if id_user != 1:
            cur.execute(
                """
                    INSERT INTO root(id_user, start_day, report, admin, inReport) VALUES(
                        {id_user}, {start_day}, {report}, {admin}, {inReport}
                    )
                """.format(
                    id_user = id_user,
                    start_day = root_list[0],
                    report = root_list[1],
                    admin = root_list[2],
                    inReport = root_list[3]
                )
            )
            con.commit()

    con.close()

def migrate_report(db_path):

    connect = sqlite3.connect(r"\\x3\support$\it_tomilis\Студенты\WorkDay\dontdelete.db")
    cursor = connect.cursor()

    data = cursor.execute("""
        SELECT 
            report.id_initiator, 
            report.day, 
            report.day_start, 
            report.dinner_start, 
            report.dinner_end, 
            report.day_end, 
            report.len_of_day, 
            report.len_of_dinner, 
            report.status, 
            report.isDeleted, 
            report.delete_reason,
            students.login
        FROM report, students
        WHERE report.id_initiator = students.id_student
    """).fetchall()

    connect.close()

    con = sqlite3.connect(db_path)
    cur = con.cursor()

    for i in data:
        
        id_inititor = i[0]
        day = i[1]
        def to_format(time):
            if time:
                hours = time // 60
                if hours < 10:
                    hours = '0' + str(hours)

                minute = time % 60
                if minute < 10:
                    minute = '0' + str(minute)

                time = str(hours) + ':' + str(minute)
                return day + ' ' + time
            else:
                return 'NULL'

        day_start = to_format(i[2])
        dinner_start = to_format(i[3])
        dinner_end = to_format(i[4])
        day_end = to_format(i[5])

        len_of_day = i[6]
        len_of_dinner = i[7]

        status = i[8]
        isDeleted = i[9]
        delete_reason = i[10]

        if isDeleted:
            status = 'deleted'

        login = i[11]

        real_id = cur.execute("""
            SELECT id FROM users
            WHERE login = '{login}'
        """.format(
            login = login
        )).fetchone()[0]

        # print(real_id, ' ', day_start, ' ', dinner_start, ' ', dinner_end, ' ', day_end, ' ', len_of_day, ' ', len_of_dinner, ' ', status, ' ', delete_reason)

        cur.execute("""
            INSERT INTO report (id_user, start_day, start_dinner, end_dinner, end_day, day_len, dinner_len, status, delete_reason)
            VALUES(
                "{id_user}",
                "{start_day}",
                "{start_dinner}",
                "{end_dinner}",
                "{end_day}",
                "{len_day}",
                "{len_dinner}",
                "{status}",
                "{delete_reason}"
            )
        """.format(
                id_user = real_id,
                start_day = day_start,
                start_dinner = dinner_start,
                end_dinner = dinner_end,
                end_day = day_end,
                len_day = len_of_day,
                len_dinner = len_of_dinner,
                status = status,
                delete_reason = delete_reason
        ))
        con.commit()

class appError(Exception):
    def __init__(self, *args):
        if args:
            self.message = args[0]
        else:
            self.message = None

    def __str__(self):
        if self.message:
            return '[!] Error: ' + str(self.message)
        
        else:
            return '[!] Error without message'

class user():
    def __init__(self, connect, cursor):
        self.connect = connect
        self.cursor = cursor

        # set user information
        self.my_login = getpass.getuser()

        self.testMode = False            # Тестовый режим (имитация логина + нету записи на кнопках WorkDay)
        if self.testMode:
            self.my_login = 'it_vsy' # Имитация логина, для тестов
        # self.my_login = 'it_vsy'

        if self.my_login.lower() == "Maksim".lower(): # If app started with home PC 
            self.my_login = "it_lunatic"
        
        self.my_info = self.cursor.execute("SELECT id, username FROM users WHERE login = '{login}' AND deleted != 1".format(login = self.my_login)).fetchone()
        if self.my_info: # if DB have record about this user
            self.my_id = self.my_info[0]
            self.my_username = self.my_info[1]

            # set user roots
            self.my_root_list = self.cursor.execute("SELECT start_day, report, admin, inReport FROM root WHERE id_user = {id_user}".format(id_user = self.my_id)).fetchone()
            self.my_root_startday = int(self.my_root_list[0])       # Can i start day
            self.my_root_report = int(self.my_root_list[1])         # Can i check all reports and edit his
            self.my_root_admin = int(self.my_root_list[2])          # If i admin (can edit users and all that can if you have root "report")
            self.my_root_inReport = int(self.my_root_list[3])       # If true, that i show in report
        
    def error(self, error: str):
        error = str(datetime.datetime.now()) + ' ' + error
        login = getpass.getuser()
        path = 'C://users/' + login + '/AppData/Roaming/workday_errors.txt'
        if os.path.exists(path):
            with open(path, 'a', encoding = 'utf-8') as file:
                file.write(error + '\n')
        else:
            with open(path, 'w', encoding = 'utf-8') as file:
                file.write(error + '\n')

    def insert_log(self, id_user: int, time: str, param: str, last_value: str = None, new_value: str = None):
        try:
            self.cursor.execute(
                """
                    INSERT INTO logs(id_user, time, param, last_value, new_value) VALUES(
                        {id_user},
                        "{time}",
                        "{param}",
                        "{last_value}",
                        "{new_value}"
                    )
                """.format(
                    id_user = id_user,
                    time = time,
                    param = param,
                    last_value = last_value,
                    new_value = new_value
                )
            )
            self.connect.commit()

        except Exception as error:
            self.error( str(error) )

    def time_to_db(self, now):
        year = now.year

        month = now.month
        if month < 10:
            month = '0' + str(month)

        day = now.day
        if day < 10:
            day = '0' + str(day)

        hour = now.hour
        if hour < 10:
            hour = '0' + str(hour)

        minute = now.minute
        if minute < 10:
            minute = '0' + str(minute)

        year, month, day, hour, minute = str(year), str(month), str(day), str(hour), str(minute)

        return year + '-' + month + '-' + day + ' ' + hour + ':' + minute

    def add_user(self, login: str, username: str):
        if self.my_root_admin:
            try:
                self.cursor.execute(
                    """
                        INSERT INTO users(login, username) VALUES(
                            "{login}",
                            "{username}"
                        )
                    """.format(
                        login = login,
                        username = username
                    )
                )
                self.connect.commit()

                id_user = self.cursor.execute('SELECT id FROM users WHERE login = "{login}" AND deleted != 1'.format(login = login)).fetchone()[0]

                self.cursor.execute(
                    """
                        INSERT INTO root(id_user, start_day, report, admin, inReport) VALUES(
                            {id_user}, 0, 0, 0, 0
                        )
                    """.format(
                        id_user = id_user
                    )
                )
                self.connect.commit()

                now = datetime.datetime.now()
                new_value = 'Login: ' + login + ' | Username: ' + username
                self.insert_log(id_user = self.my_id, time = self.time_to_db(now), param = 'Add user', new_value = new_value)

            except Exception as error:
                self.error(str(error))

    def change_user(self, id_user: int, param: str, new_value: str):
        if self.my_root_admin:
            # Define which column and table be using
            if param.lower() in ['login', 'username']:
                table = 'users'
                col_name = 'id'

            elif param.lower() in ['start_day', 'report', 'admin', 'inreport']:
                table = 'root'
                col_name = 'id_user'
                new_value = int(new_value)

            
            try:
                # Get old value to write logs
                last_value = self.cursor.execute("SELECT {param} FROM {table} WHERE {col_name} = {id_user}".format(
                    param = param,
                    table = table,
                    col_name = col_name,
                    id_user = id_user
                )).fetchone()[0]

                self.cursor.execute(
                    """
                        UPDATE {table}
                        SET {param} = {new_value}
                        WHERE {col_name} = {id_user}
                    """.format(
                        table = table,
                        param = param,
                        new_value = new_value,
                        col_name = col_name,
                        id_user = id_user
                    )
                )
                self.connect.commit()

                self.insert_log(id_user = self.my_id, time = self.time_to_db(datetime.datetime.now()), param = 'Change user ' + str(id_user), last_value = param + ' = ' + str(last_value), new_value = param + ' = ' + str(new_value))

            except Exception as error:
                self.error(str(error))

    def edit_report_time(self, id_record: int, new_start_day, new_start_dinner, new_end_dinner, new_end_day, new_day_len, new_dinner_len):
        if self.my_root_report or self.my_root_admin:
            try:
                old_value = self.cursor.execute("SELECT start_day, start_dinner, end_dinner, end_day, status FROM report WHERE id = {id_record}".format(
                    id_record = id_record
                )).fetchone()

                if old_value[4] != "deleted":
                    old_value = 'Start day = ' + str(old_value[0]) + ' | Start dinner = ' + str(old_value[1]) + ' | End dinner = ' + str(old_value[2]) + ' | End day = ' + str(old_value[3])
                    new_value = 'Start day = ' + str(new_start_day) + ' | Start dinner = ' + str(new_start_dinner) + ' | End dinner = ' + str(new_end_dinner) + ' | End day = ' + str(new_end_day)

                    self.cursor.execute(
                        """
                            UPDATE report
                            SET start_day = "{start_day}",
                                start_dinner = "{start_dinner}",
                                end_dinner = "{end_dinner}",
                                end_day = "{end_day}",
                                day_len = {day_len},
                                dinner_len = {dinner_len}
                            WHERE id = {id_record}
                        """.format(
                            start_day = new_start_day,
                            start_dinner = new_start_dinner,
                            end_dinner = new_end_dinner,
                            end_day = new_end_day,
                            day_len = new_day_len,
                            dinner_len = new_dinner_len,
                            id_record = id_record
                        )
                    )
                    self.connect.commit()

                    self.insert_log(id_user = self.my_id, time = self.time_to_db( datetime.datetime.now() ), param = 'Changed record time', last_value = old_value, new_value = new_value)
            
            except Exception as error:
                self.error( str(error) )

    def edit_report_status(self, id_record: int, new_status: str):
        if self.my_root_report or self.my_root_admin:
            try:
                old_value = self.cursor.execute("SELECT status, delete_reason FROM report WHERE id = {id_record}".format(
                    id_record = id_record
                )).fetchone()

                if old_value[0] == 'deleted':
                    old_value = 'Status: ' + str(old_value[0]) + ' | Delete reason: ' + str(old_value[1])
                else:
                    old_value = 'Status: ' + str(old_value[0])

                if new_status != 'deleted':
                    self.cursor.execute(
                        """
                            UPDATE report
                            SET status = "{status}"
                            WHERE id = {id_record}
                        """.format(
                            status = new_status,
                            id_record = id_record
                        )
                    )
                    self.connect.commit()
                    self.insert_log(id_user = self.my_id, time = self.time_to_db( datetime.datetime.now() ), param = 'Edited record', last_value = old_value, new_value = new_status)
                
                elif new_status == 'deleted':
                    pass

            except Exception as error:
                self.error( str(error) )

    def delete_report(self, id_record: int, delete_reason: str):
        if self.my_root_report or self.my_root_admin:
            try:
                old_value = self.cursor.execute("SELECT status FROM report WHERE id = {id_report}".format(
                    id_report = id_record
                )).fetchone()[0]
                if old_value != 'deleted':
                    self.cursor.execute(
                        """
                            UPDATE report
                            SET status = 'deleted', delete_reason = '{delete_reason}'
                            WHERE id = {id_record}
                        """.format(
                            id_record = id_record,
                            delete_reason = delete_reason
                        )
                    )
                    self.connect.commit()
                    new_value = 'Status: deleted | Delete reason: ' + delete_reason
                    self.insert_log(id_user = self.my_id, time = self.time_to_db( datetime.datetime.now() ), param = 'Deleted record', last_value = old_value, new_value = new_value)
            
            except Exception as error:
                self.error( str(error) )

class timer():
    def __init__(self):

        self.start_time = 0
        self.end_time = 0

    def start(self):
        if not self.start_time:
            self.start_time = datetime.datetime.now()

        elif self.start_time and not self.end_time: # If day started and not ended
            raise appError('Timer already started')

        elif self.end_time: # If day end
            raise appError('Timer stoped')
    
    def stop(self):
        if self.start_time and not self.end_time: # If day is started and not stoped
            self.end_time = datetime.datetime.now()
        
        elif not self.start_time: # If day is not started
            raise appError('Timer not started')

        elif self.end_time:
            raise appError('Timer already stoped')

    def value(self):
        if self.start_time and not self.end_time: # if day started and not ended
            return datetime.datetime.now() - self.start_time

        elif self.end_time: # If day ended
            return self.end_time - self.start_time

        elif not self.start_time: # If day not started
            raise appError('Timer not started')
            
if __name__ == "__main__":
    db_path = r"\\x3.corp.motiv\support$\it_lunatic\Разработка\Python\workday.sqlite"