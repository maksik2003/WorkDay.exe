# -*- coding: utf-8 -*-

# Небольшая информация:
# На 20.07.2023 приложение содержит в себе 3496 строк (включая самописные библиотеки)

from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtCore import QThread
import colors as color
import styleSheet
import sqlite3
import db
import datetime
import re
import report
from socket import gethostname
import os.path, os

import hiddenSoft_report
from vacations import Vacation

colors = color.color_theme()
APP_VERSION = 10
APP_NAME = 'WorkDay'

class Ui_error(object):
        def setup_error(self, Widget):
                super().__init__()

                if self.databaseExists:
                        color_theme = self.cursor.execute("""
                                SELECT text_color, background, rectangle, hover, hover_negative, non_active_color, indicator_border, text_color_inverse
                                FROM themes
                                WHERE id_user = {id_user}
                        """.format(
                                id_user = 0
                        )).fetchone()

                        if color_theme:
                                # Установка цвета
                                colors.my_theme(
                                        text_color = color_theme[0],
                                        background = color_theme[1],
                                        rectangle = color_theme[2],
                                        hover = color_theme[3],
                                        hover_negative = color_theme[4],
                                        non_active_color = color_theme[5],
                                        indicator_border = color_theme[6],
                                        text_color_inverse = color_theme[7]
                                )

                self.styleSheet = styleSheet.styleSheet(colors)
                
                Widget.setObjectName("Widget")
                Widget.resize(500, 200)
                Widget.setMinimumSize(QtCore.QSize(500, 200))
                Widget.setMaximumSize(QtCore.QSize(500, 200))
                Widget.setStyleSheet("""
                        QWidget {{
                                background-color: {background};
                        }}
                """.format(
                        background = colors.background
                ))

                self.font = QtGui.QFont()
                self.font.setFamily("Montserrat")
                self.font.setPointSize(10)
                self.font.setWeight(700)

                self.label = QtWidgets.QLabel(Widget)
                self.label.setGeometry(QtCore.QRect(10, 50, 480, 20))
                self.label.setFont(self.font)
                self.label.setStyleSheet(self.styleSheet.label_inverse)
                self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                self.label.setObjectName("label")

                self.btn = QtWidgets.QPushButton(Widget)
                self.btn.setEnabled(True)
                self.btn.setGeometry(QtCore.QRect(200, 110, 100, 30))
                self.btn.setFont(self.font)
                self.btn.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
                self.btn.setStyleSheet(self.styleSheet.btn)
                self.btn.setObjectName("btn")

                self.retranslateUi_error(Widget)

        def retranslateUi_error(self, Widget):
                Widget.setWindowTitle('WorkDay - Admin')

                self.label.setText('Отказано в доступе')
                self.btn.setText('Понял')

        def open_update_folder(self, path):
                os.system('explorer.exe "{path}"'.format(
                        path = path
                ))

class Ui_genReportForm(QtWidgets.QMainWindow, object):

        def __init__(self):
                super().__init__()
                self.Ui_genReportShow(self)

        def Ui_genReportShow(self, Form):
                # super().__init__()

                Form.setObjectName('Form')
                w = 400
                h = 225
                Form.resize(w, h)
                Form.setMinimumSize(QtCore.QSize(w, h))
                Form.setMaximumSize(QtCore.QSize(w, h))

                Form.setStyleSheet("""
                        QWidget {{
                                background-color: {background};
                        }}
                """.format(
                        background = colors.background
                ))

                self.font = QtGui.QFont()
                self.font.setFamily("Montserrat")
                self.font.setPointSize(10)
                self.font.setWeight(700)

                y = 60
                self.btn_default_report = QtWidgets.QPushButton(Form)
                self.btn_default_report.setEnabled(True)
                self.btn_default_report.setGeometry(QtCore.QRect(50, y, 300, 50))
                self.btn_default_report.setFont(self.font)
                self.btn_default_report.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
                self.btn_default_report.setObjectName("btn_default_report")
                self.btn_default_report.setText('Стандартный отчет')

                y += 65
                self.btn_special_report = QtWidgets.QPushButton(Form)
                self.btn_special_report.setEnabled(True)
                self.btn_special_report.setGeometry(QtCore.QRect(50, y, 300, 50))
                self.btn_special_report.setFont(self.font)
                self.btn_special_report.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
                self.btn_special_report.setObjectName("btn_special_report")
                self.btn_special_report.setText('Отчет для отдела кадров')

                self.label = QtWidgets.QLabel(Form)
                self.label.setGeometry(QtCore.QRect(0, 20, w, 20))
                self.label.setFont(self.font)
                self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                self.label.setObjectName("label")
                self.label.setText('Выберите нужный отчет')

                Form.setWindowTitle('Выбор вида отчета')

class Ui_Form(object):
        def setupUi(self, Form):
                Form.setObjectName("Form")
                Form.resize(720, 590)
                Form.setMinimumSize(QtCore.QSize(720, 590))
                Form.setMaximumSize(QtCore.QSize(720, 590))
                bg = colors.background
                Form.setStyleSheet("""
                        QWidget {{
                                background-color: {background};
                        }}
                """.format(
                        background = bg
                ))

                self.font = QtGui.QFont()
                self.font.setFamily("Montserrat")
                self.font.setPointSize(10)
                self.font.setWeight(700)
                
                lineEdit_font = QtGui.QFont()
                lineEdit_font.setFamily("Montserrat")
                lineEdit_font.setWeight(700)

                self.tabWidget = QtWidgets.QTabWidget(Form)
                self.tabWidget.setGeometry(QtCore.QRect(10, 80, 710, 500))
                self.tabWidget.setFont(self.font)
                self.tabWidget.setTabPosition(QtWidgets.QTabWidget.TabPosition.North)
                self.tabWidget.setTabShape(QtWidgets.QTabWidget.TabShape.Rounded)
                self.tabWidget.setObjectName("tabWidget")
                self.tabWidget.setStyleSheet(self.styleSheet.tab_widget)

                self.reports = QtWidgets.QWidget()
                self.reports.setObjectName("reports")

                self.label_period_bg = QtWidgets.QLabel(self.reports)
                self.label_period_bg.setGeometry(QtCore.QRect(10, 10, 400, 40))
                self.label_period_bg.setText("")
                self.label_period_bg.setObjectName("label_period_bg")
                self.label_period_bg.setStyleSheet(self.styleSheet.label_bg)

                self.label_period = QtWidgets.QLabel(self.reports)
                self.label_period.setGeometry(QtCore.QRect(10, 10, 80, 40))
                self.label_period.setFont(self.font)
                self.label_period.setStyleSheet(self.styleSheet.label_text)
                self.label_period.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                self.label_period.setObjectName("label_period")

                self.lineEdit_enddate = QtWidgets.QLineEdit(self.reports)
                self.lineEdit_enddate.setGeometry(QtCore.QRect(200, 15, 90, 30))
                self.lineEdit_enddate.setFont(lineEdit_font)
                self.lineEdit_enddate.setStyleSheet(self.styleSheet.input_datetime)
                self.lineEdit_enddate.setMaxLength(10)
                self.lineEdit_enddate.setCursorPosition(0)
                self.lineEdit_enddate.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                self.lineEdit_enddate.setObjectName("lineEdit_enddate")

                self.btn_this_month = QtWidgets.QPushButton(self.reports)
                self.btn_this_month.setEnabled(True)
                self.btn_this_month.setGeometry(QtCore.QRect(300, 15, 101, 30))
                self.btn_this_month.setFont(self.font)
                self.btn_this_month.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
                self.btn_this_month.setStyleSheet(self.styleSheet.inverse_btn)
                self.btn_this_month.setObjectName("btn_this_month")

                self.line_start_end_date = QtWidgets.QFrame(self.reports)
                self.line_start_end_date.setGeometry(QtCore.QRect(185, 30, 10, 2))
                self.line_start_end_date.setFrameShape(QtWidgets.QFrame.Shape.HLine)
                self.line_start_end_date.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
                self.line_start_end_date.setObjectName("line_start_end_date")
                self.line_start_end_date.setStyleSheet("""
                        Line {{
                                background-color: {background};
                                border: none;
                                border-radius: 1px;
                        }}
                """.format(
                        background = colors.background
                ))
                self.lineEdit_startdate = QtWidgets.QLineEdit(self.reports)
                self.lineEdit_startdate.setGeometry(QtCore.QRect(90, 15, 90, 30))
                self.lineEdit_startdate.setFont(lineEdit_font)
                self.lineEdit_startdate.setStyleSheet(self.styleSheet.input_datetime)
                self.lineEdit_startdate.setMaxLength(10)
                self.lineEdit_startdate.setCursorPosition(0)
                self.lineEdit_startdate.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                self.lineEdit_startdate.setObjectName("lineEdit_startdate")

                self.btn_generate_report = QtWidgets.QPushButton(self.reports)
                self.btn_generate_report.setGeometry(QtCore.QRect(419, 10, 130, 40))
                self.btn_generate_report.setFont(self.font)
                self.btn_generate_report.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
                self.btn_generate_report.setWhatsThis("<html><head/><body><p align=\"center\">Сгенерировать отчет в Excel формате</p></body></html>")
                self.btn_generate_report.setStyleSheet(self.styleSheet.btn)
                self.btn_generate_report.setObjectName("btn_generate_report")

                self.label_report_bg = QtWidgets.QLabel(self.reports)
                self.label_report_bg.setGeometry(QtCore.QRect(10, 60, 400, 351))
                self.label_report_bg.setStyleSheet(self.styleSheet.label_bg)
                self.label_report_bg.setObjectName("label_report_bg")

                self.label_title_date = QtWidgets.QLabel(self.reports)
                self.label_title_date.setGeometry(QtCore.QRect(20, 60, 110, 40))
                self.label_title_date.setFont(self.font)
                self.label_title_date.setStyleSheet(self.styleSheet.label_text)
                self.label_title_date.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                self.label_title_date.setObjectName("label_title_date")

                self.label_title_weekday = QtWidgets.QLabel(self.reports)
                self.label_title_weekday.setGeometry(QtCore.QRect(130, 60, 130, 40))
                self.label_title_weekday.setFont(self.font)
                self.label_title_weekday.setStyleSheet(self.styleSheet.label_text)
                self.label_title_weekday.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                self.label_title_weekday.setObjectName("label_title_weekday")

                self.label_report_count = QtWidgets.QLabel(self.reports)
                self.label_report_count.setGeometry(QtCore.QRect(260, 60, 130, 40))
                self.label_report_count.setFont(self.font)
                self.label_report_count.setStyleSheet(self.styleSheet.label_text)
                self.label_report_count.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                self.label_report_count.setObjectName("label_report_count")

                self.label_edit_bg = QtWidgets.QLabel(self.reports)
                self.label_edit_bg.setGeometry(QtCore.QRect(420, 59, 270, 301))
                self.label_edit_bg.setStyleSheet(self.styleSheet.label_bg)
                self.label_edit_bg.setObjectName("label_edit_bg")

                # Рисуем заголовок
                self.label_edit_title = QtWidgets.QLabel(self.reports)
                self.label_edit_title.setGeometry(QtCore.QRect(420, 60, 270, 40))
                self.label_edit_title.setFont(self.font)
                self.label_edit_title.setStyleSheet(self.styleSheet.label_text)
                self.label_edit_title.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                self.label_edit_title.setObjectName("label_edit_title")
                self.label_edit_title.show()

                # Устанавливаем заголовок "Дата"
                self.label_edit_date = QtWidgets.QLabel(self.reports)
                self.label_edit_date.setGeometry(QtCore.QRect(430, 100, 60, 30))
                self.label_edit_date.setFont(self.font)
                self.label_edit_date.setStyleSheet(self.styleSheet.label_text)
                self.label_edit_date.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeading|QtCore.Qt.AlignmentFlag.AlignLeft|QtCore.Qt.AlignmentFlag.AlignVCenter)
                self.label_edit_date.setObjectName("label_edit_date")
                self.label_edit_date.show()

                self.lineEdit_edit_date = QtWidgets.QLineEdit(self.reports)
                self.lineEdit_edit_date.setGeometry(QtCore.QRect(580, 100, 90, 30))
                self.lineEdit_edit_date.setFont(lineEdit_font)
                self.lineEdit_edit_date.setStyleSheet(self.styleSheet.input_datetime)
                self.lineEdit_edit_date.setMaxLength(10)
                self.lineEdit_edit_date.setCursorPosition(10)
                self.lineEdit_edit_date.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                self.lineEdit_edit_date.setObjectName("lineEdit_edit_date")

                self.label_edit_worktime = QtWidgets.QLabel(self.reports)
                self.label_edit_worktime.setGeometry(QtCore.QRect(430, 130, 111, 30))
                self.label_edit_worktime.setFont(self.font)
                self.label_edit_worktime.setStyleSheet(self.styleSheet.label_text)
                self.label_edit_worktime.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeading|QtCore.Qt.AlignmentFlag.AlignLeft|QtCore.Qt.AlignmentFlag.AlignVCenter)
                self.label_edit_worktime.setObjectName("label_edit_worktime")

                self.label_edit_dinnertime = QtWidgets.QLabel(self.reports)
                self.label_edit_dinnertime.setGeometry(QtCore.QRect(430, 190, 111, 30))
                self.label_edit_dinnertime.setFont(self.font)
                self.label_edit_dinnertime.setStyleSheet(self.styleSheet.label_text)
                self.label_edit_dinnertime.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeading|QtCore.Qt.AlignmentFlag.AlignLeft|QtCore.Qt.AlignmentFlag.AlignVCenter)
                self.label_edit_dinnertime.setObjectName("label_edit_dinnertime")

                self.lineEdit_edit_end_day = QtWidgets.QLineEdit(self.reports)
                self.lineEdit_edit_end_day.setGeometry(QtCore.QRect(580, 160, 90, 30))
                self.lineEdit_edit_end_day.setFont(lineEdit_font)
                self.lineEdit_edit_end_day.setStyleSheet(self.styleSheet.input_datetime)
                self.lineEdit_edit_end_day.setMaxLength(5)
                self.lineEdit_edit_end_day.setObjectName("lineEdit_edit_end_day")
                self.lineEdit_edit_end_day.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

                self.label_edit_start_day = QtWidgets.QLabel(self.reports)
                self.label_edit_start_day.setGeometry(QtCore.QRect(430, 160, 15, 30))
                self.label_edit_start_day.setFont(self.font)
                self.label_edit_start_day.setStyleSheet(self.styleSheet.label_text)
                self.label_edit_start_day.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                self.label_edit_start_day.setObjectName("label_edit_start_day")

                self.lineEdit_edit_start_day = QtWidgets.QLineEdit(self.reports)
                self.lineEdit_edit_start_day.setGeometry(QtCore.QRect(450, 160, 90, 30))
                self.lineEdit_edit_start_day.setFont(lineEdit_font)
                self.lineEdit_edit_start_day.setStyleSheet(self.styleSheet.input_datetime)
                self.lineEdit_edit_start_day.setMaxLength(5)
                self.lineEdit_edit_start_day.setObjectName("lineEdit_edit_start_day")
                self.lineEdit_edit_start_day.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

                self.label_edit_end_day = QtWidgets.QLabel(self.reports)
                self.label_edit_end_day.setGeometry(QtCore.QRect(550, 160, 20, 30))
                self.label_edit_end_day.setFont(self.font)
                self.label_edit_end_day.setStyleSheet(self.styleSheet.label_text)
                self.label_edit_end_day.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                self.label_edit_end_day.setObjectName("label_edit_end_day")

                self.btn_generate_addrecord = QtWidgets.QPushButton(self.reports)
                self.btn_generate_addrecord.setGeometry(QtCore.QRect(560, 10, 130, 40))
                self.btn_generate_addrecord.setFont(self.font)
                self.btn_generate_addrecord.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
                self.btn_generate_addrecord.setObjectName("btn_generate_addrecord")
                self.btn_generate_addrecord.setStyleSheet(self.styleSheet.btn)

                self.lineEdit_edit_end_dinner = QtWidgets.QLineEdit(self.reports)
                self.lineEdit_edit_end_dinner.setGeometry(QtCore.QRect(580, 220, 90, 30))
                self.lineEdit_edit_end_dinner.setFont(lineEdit_font)
                self.lineEdit_edit_end_dinner.setStyleSheet(self.styleSheet.input_datetime)
                self.lineEdit_edit_end_dinner.setMaxLength(5)
                self.lineEdit_edit_end_dinner.setObjectName("lineEdit_edit_end_dinner")
                self.lineEdit_edit_end_dinner.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

                self.label_edit_start_dinner = QtWidgets.QLabel(self.reports)
                self.label_edit_start_dinner.setGeometry(QtCore.QRect(430, 220, 15, 30))
                self.label_edit_start_dinner.setFont(self.font)
                self.label_edit_start_dinner.setStyleSheet(self.styleSheet.label_text)
                self.label_edit_start_dinner.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                self.label_edit_start_dinner.setObjectName("label_edit_start_dinner")

                self.lineEdit_edit_start_dinner = QtWidgets.QLineEdit(self.reports)
                self.lineEdit_edit_start_dinner.setGeometry(QtCore.QRect(450, 220, 90, 30))
                self.lineEdit_edit_start_dinner.setFont(lineEdit_font)
                self.lineEdit_edit_start_dinner.setStyleSheet(self.styleSheet.input_datetime)
                self.lineEdit_edit_start_dinner.setMaxLength(5)
                self.lineEdit_edit_start_dinner.setObjectName("lineEdit_edit_start_dinner")
                self.lineEdit_edit_start_dinner.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

                self.label_edit_end_dinner = QtWidgets.QLabel(self.reports)
                self.label_edit_end_dinner.setGeometry(QtCore.QRect(550, 220, 20, 30))
                self.label_edit_end_dinner.setFont(self.font)
                self.label_edit_end_dinner.setStyleSheet(self.styleSheet.label_text)
                self.label_edit_end_dinner.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                self.label_edit_end_dinner.setObjectName("label_edit_end_dinner")

                self.btn_save_edit = QtWidgets.QPushButton(self.reports)
                self.btn_save_edit.setEnabled(True)
                self.btn_save_edit.setGeometry(QtCore.QRect(430, 320, 120, 30))
                self.btn_save_edit.setFont(self.font)
                self.btn_save_edit.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
                self.btn_save_edit.setObjectName("btn_save_edit")
                self.btn_save_edit.setStyleSheet(self.styleSheet.inverse_btn)

                self.lineEdit_delete_reason = QtWidgets.QLineEdit(self.reports)
                self.lineEdit_delete_reason.setGeometry(QtCore.QRect(430, 385, 250, 30))
                self.lineEdit_delete_reason.setFont(lineEdit_font)
                self.lineEdit_delete_reason.setStyleSheet(self.styleSheet.input_text)
                self.lineEdit_delete_reason.setObjectName("lineEdit_delete_reason")

                self.btn_cancel_edit = QtWidgets.QPushButton(self.reports)
                self.btn_cancel_edit.setEnabled(True)
                self.btn_cancel_edit.setGeometry(QtCore.QRect(560, 320, 120, 30))
                self.btn_cancel_edit.setFont(self.font)
                self.btn_cancel_edit.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
                self.btn_cancel_edit.setObjectName("btn_cancel_edit")
                self.btn_cancel_edit.setStyleSheet(self.styleSheet.inverse_btn)

                self.checkbox_timeoff = QtWidgets.QCheckBox(self.reports)
                self.checkbox_timeoff.setGeometry(QtCore.QRect(430, 280, 351, 40))
                self.checkbox_timeoff.setFont(self.font)
                self.checkbox_timeoff.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
                self.checkbox_timeoff.setStyleSheet(self.styleSheet.checkbox)
                self.checkbox_timeoff.setCheckable(True)
                self.checkbox_timeoff.setChecked(False)
                self.checkbox_timeoff.setObjectName("checkbox_timeoff")

                self.checkbox_autostop = QtWidgets.QCheckBox(self.reports)
                self.checkbox_autostop.setEnabled(True)
                self.checkbox_autostop.setGeometry(QtCore.QRect(430, 250, 351, 40))
                self.checkbox_autostop.setFont(self.font)
                self.checkbox_autostop.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
                self.checkbox_autostop.setStyleSheet(self.styleSheet.checkbox)
                self.checkbox_autostop.setCheckable(True)
                self.checkbox_autostop.setChecked(False)
                self.checkbox_autostop.setObjectName("checkbox_autostop")

                self.btn_delete_record = QtWidgets.QPushButton(self.reports)
                self.btn_delete_record.setEnabled(True)
                self.btn_delete_record.setGeometry(QtCore.QRect(430, 420, 110, 30))
                self.btn_delete_record.setFont(self.font)
                self.btn_delete_record.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
                self.btn_delete_record.setObjectName("btn_delete_record")
                self.btn_delete_record.setStyleSheet(self.styleSheet.inverse_btn)

                self.label_delete_bg = QtWidgets.QLabel(self.reports)
                self.label_delete_bg.setGeometry(QtCore.QRect(420, 370, 270, 91))
                self.label_delete_bg.setStyleSheet(self.styleSheet.label_bg)
                self.label_delete_bg.setObjectName("label_delete_bg")

                self.label_report_bg_2 = QtWidgets.QLabel(self.reports)
                self.label_report_bg_2.setGeometry(QtCore.QRect(220, 420, 190, 40))
                self.label_report_bg_2.setStyleSheet(self.styleSheet.label_bg)
                self.label_report_bg_2.setObjectName("label_report_bg_2")

                self.label_report_allhours = QtWidgets.QLabel(self.reports)
                self.label_report_allhours.setGeometry(QtCore.QRect(220, 420, 121, 40))
                self.label_report_allhours.setFont(self.font)
                self.label_report_allhours.setStyleSheet(self.styleSheet.label_text)
                self.label_report_allhours.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                self.label_report_allhours.setObjectName("label_report_allhours")

                self.label_report_count_hours = QtWidgets.QLabel(self.reports)
                self.label_report_count_hours.setGeometry(QtCore.QRect(340, 420, 71, 40))
                self.label_report_count_hours.setFont(self.font)
                self.label_report_count_hours.setStyleSheet(self.styleSheet.label_text)
                self.label_report_count_hours.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                self.label_report_count_hours.setObjectName("label_report_count_hours")

                self.btn_report_up = QtWidgets.QPushButton(self.reports)
                self.btn_report_up.setGeometry(QtCore.QRect(10, 420, 40, 40))
                self.btn_report_up.setFont(self.font)
                self.btn_report_up.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
                self.btn_report_up.setWhatsThis("<html><head/><body><p align=\"center\">Сгенерировать отчет в Excel формате</p></body></html>")
                self.btn_report_up.setStyleSheet(self.styleSheet.btn)
                self.btn_report_up.setText("")
                icon = QtGui.QIcon()
                icon.addPixmap(QtGui.QPixmap("./img/arrow_up.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
                self.btn_report_up.setIcon(icon)
                self.btn_report_up.setObjectName("btn_report_up")

                self.btn_report_down = QtWidgets.QPushButton(self.reports)
                self.btn_report_down.setGeometry(QtCore.QRect(60, 420, 40, 40))
                self.btn_report_down.setFont(self.font)
                self.btn_report_down.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
                self.btn_report_down.setWhatsThis("<html><head/><body><p align=\"center\">Сгенерировать отчет в Excel формате</p></body></html>")
                self.btn_report_down.setStyleSheet(self.styleSheet.btn)
                icon1 = QtGui.QIcon()
                icon1.addPixmap(QtGui.QPixmap("./img/arrow_down.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
                self.btn_report_down.setIcon(icon1)
                self.btn_report_down.setObjectName("btn_report_down")

                # Счетчик страниц
                self.label_page = QtWidgets.QLabel(self.reports)
                self.label_page.setGeometry(QtCore.QRect(100, 420, 70, 40))
                self.label_page.setFont(self.font)
                self.label_page.setStyleSheet(self.styleSheet.label_inverse)
                self.label_page.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                self.label_page.setObjectName("label_page")

                self.label_delete_bg.raise_()
                self.label_page.raise_()
                self.label_period_bg.raise_()
                self.label_period.raise_()
                self.lineEdit_enddate.raise_()
                self.btn_this_month.raise_()
                self.line_start_end_date.raise_()
                self.lineEdit_startdate.raise_()
                self.btn_generate_report.raise_()
                self.label_report_bg.raise_()
                self.label_title_date.raise_()
                self.label_title_weekday.raise_()
                self.label_report_count.raise_()
                # self.label_report_date.raise_()
                # self.label_report_weekday.raise_()
                # self.btn_count.raise_()
                
                self.label_edit_bg.raise_()
                self.lineEdit_edit_date.raise_()
                self.label_edit_worktime.raise_()
                self.label_edit_dinnertime.raise_()
                self.lineEdit_edit_end_day.raise_()
                self.label_edit_start_day.raise_()
                self.lineEdit_edit_start_day.raise_()
                self.label_edit_end_day.raise_()
                self.btn_generate_addrecord.raise_()
                self.lineEdit_edit_end_dinner.raise_()
                self.label_edit_start_dinner.raise_()
                self.lineEdit_edit_start_dinner.raise_()
                self.label_edit_end_dinner.raise_()
                self.btn_save_edit.raise_()
                self.lineEdit_delete_reason.raise_()
                self.btn_cancel_edit.raise_()
                self.checkbox_timeoff.raise_()
                self.checkbox_autostop.raise_()
                self.btn_delete_record.raise_()
                self.label_report_bg_2.raise_()
                self.label_report_allhours.raise_()
                self.label_report_count_hours.raise_()
                self.btn_report_up.raise_()
                self.btn_report_down.raise_()

                self.tabWidget.addTab(self.reports, "")

                self.users = QtWidgets.QWidget()
                self.users.setStyleSheet("""
                        QTabWidget::tab {{
                                margin-left: 10px;
                        }}
                """)
                self.users.setObjectName("users")

                self.label_permissions_title = QtWidgets.QLabel(self.users)
                self.label_permissions_title.setGeometry(QtCore.QRect(10, 20, 331, 20))
                self.label_permissions_title.setFont(self.font)
                self.label_permissions_title.setStyleSheet(self.styleSheet.label_text)
                self.label_permissions_title.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                self.label_permissions_title.setObjectName("label_permissions_title")

                self.checkbox_start_day = QtWidgets.QCheckBox(self.users)
                self.checkbox_start_day.setGeometry(QtCore.QRect(20, 40, 200, 41))
                self.checkbox_start_day.setFont(self.font)
                self.checkbox_start_day.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
                self.checkbox_start_day.setStyleSheet(self.styleSheet.checkbox)
                self.checkbox_start_day.setCheckable(True)
                self.checkbox_start_day.setChecked(False)
                self.checkbox_start_day.setObjectName("checkbox_start_day")

                self.checkbox_report = QtWidgets.QCheckBox(self.users)
                self.checkbox_report.setGeometry(QtCore.QRect(20, 60+10, 200, 41))
                self.checkbox_report.setFont(self.font)
                self.checkbox_report.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
                self.checkbox_report.setStyleSheet(self.styleSheet.checkbox)
                self.checkbox_report.setCheckable(True)
                self.checkbox_report.setChecked(False)
                self.checkbox_report.setObjectName("checkbox_report")

                self.checkbox_admin = QtWidgets.QCheckBox(self.users)
                self.checkbox_admin.setGeometry(QtCore.QRect(20, 80+20, 200, 41))
                self.checkbox_admin.setFont(self.font)
                self.checkbox_admin.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
                self.checkbox_admin.setStyleSheet(self.styleSheet.checkbox)
                self.checkbox_admin.setCheckable(True)
                self.checkbox_admin.setChecked(False)
                self.checkbox_admin.setObjectName("checkbox_admin")

                self.checkbox_inreport = QtWidgets.QCheckBox(self.users)
                self.checkbox_inreport.setGeometry(QtCore.QRect(20, 100+30, 200, 41))
                self.checkbox_inreport.setFont(self.font)
                self.checkbox_inreport.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
                self.checkbox_inreport.setStyleSheet(self.styleSheet.checkbox)
                self.checkbox_inreport.setCheckable(True)
                self.checkbox_inreport.setChecked(False)
                self.checkbox_inreport.setObjectName("checkbox_inreport")

                self.checkbox_hiddenSoft_R = QtWidgets.QCheckBox(self.users)
                self.checkbox_hiddenSoft_R.setGeometry(QtCore.QRect(20, 120+40, 200, 41))
                self.checkbox_hiddenSoft_R.setFont(self.font)
                self.checkbox_hiddenSoft_R.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
                self.checkbox_hiddenSoft_R.setStyleSheet(self.styleSheet.checkbox)
                self.checkbox_hiddenSoft_R.setCheckable(True)
                self.checkbox_hiddenSoft_R.setChecked(False)
                self.checkbox_hiddenSoft_R.setObjectName("checkbox_hiddenSoft_R")

                self.checkbox_hiddenSoft_RW = QtWidgets.QCheckBox(self.users)
                self.checkbox_hiddenSoft_RW.setGeometry(QtCore.QRect(20, 140+50, 200, 41))
                self.checkbox_hiddenSoft_RW.setFont(self.font)
                self.checkbox_hiddenSoft_RW.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
                self.checkbox_hiddenSoft_RW.setStyleSheet(self.styleSheet.checkbox)
                self.checkbox_hiddenSoft_RW.setCheckable(True)
                self.checkbox_hiddenSoft_RW.setChecked(False)
                self.checkbox_hiddenSoft_RW.setObjectName("checkbox_hiddenSoft_RW")

                self.checkbox_specialReport = QtWidgets.QCheckBox(self.users)
                self.checkbox_specialReport.setGeometry(QtCore.QRect(20, 160+60, 200, 41))
                self.checkbox_specialReport.setFont(self.font)
                self.checkbox_specialReport.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
                self.checkbox_specialReport.setStyleSheet(self.styleSheet.checkbox)
                self.checkbox_specialReport.setCheckable(True)
                self.checkbox_specialReport.setChecked(False)
                self.checkbox_specialReport.setObjectName("checkbox_specialReport")

                self.btn_adduser_save = QtWidgets.QPushButton(self.users)
                self.btn_adduser_save.setEnabled(True)
                self.btn_adduser_save.setGeometry(QtCore.QRect(370, 260, 220, 30))
                self.btn_adduser_save.setFont(self.font)
                self.btn_adduser_save.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
                self.btn_adduser_save.setStyleSheet(self.styleSheet.inverse_btn)
                self.btn_adduser_save.setObjectName("btn_adduser_save")

                self.label_permissions_bg = QtWidgets.QLabel(self.users)
                self.label_permissions_bg.setGeometry(QtCore.QRect(10, 10, 330, 230+60))
                self.label_permissions_bg.setStyleSheet(self.styleSheet.label_bg)
                self.label_permissions_bg.setObjectName("label_permissions_bg")

                self.lineEdit_username = QtWidgets.QLineEdit(self.users)
                self.lineEdit_username.setGeometry(QtCore.QRect(370, 50, 311, 40))
                self.lineEdit_username.setFont(lineEdit_font)
                self.lineEdit_username.setStyleSheet(self.styleSheet.input_text)
                self.lineEdit_username.setObjectName("lineEdit_username")

                self.btn_adduser_cancel = QtWidgets.QPushButton(self.users)
                self.btn_adduser_cancel.setEnabled(True)
                self.btn_adduser_cancel.setGeometry(QtCore.QRect(600, 260, 80, 30))
                self.btn_adduser_cancel.setFont(self.font)
                self.btn_adduser_cancel.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
                self.btn_adduser_cancel.setStyleSheet(self.styleSheet.inverse_btn)
                self.btn_adduser_cancel.setObjectName("btn_adduser_cancel")

                self.label_add_user_title = QtWidgets.QLabel(self.users)
                self.label_add_user_title.setGeometry(QtCore.QRect(360, 20, 330, 20))
                self.label_add_user_title.setFont(self.font)
                self.label_add_user_title.setStyleSheet(self.styleSheet.label_text)
                self.label_add_user_title.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                self.label_add_user_title.setObjectName("label_add_user_title")

                self.lineEdit_login = QtWidgets.QLineEdit(self.users)
                self.lineEdit_login.setGeometry(QtCore.QRect(370, 100, 310, 40))
                self.lineEdit_login.setFont(lineEdit_font)
                self.lineEdit_login.setStyleSheet(self.styleSheet.input_text)
                self.lineEdit_login.setObjectName("lineEdit_login")

                self.lineEdit_organization = QtWidgets.QLineEdit(self.users)
                self.lineEdit_organization.setGeometry(QtCore.QRect(370, 150, 310, 40))
                self.lineEdit_organization.setFont(lineEdit_font)
                self.lineEdit_organization.setStyleSheet(self.styleSheet.input_text)
                self.lineEdit_organization.setObjectName("lineEdit_organization")

                self.lineEdit_birthday = QtWidgets.QLineEdit(self.users)
                self.lineEdit_birthday.setGeometry(QtCore.QRect(370, 200, 310, 40))
                self.lineEdit_birthday.setFont(lineEdit_font)
                self.lineEdit_birthday.setStyleSheet(self.styleSheet.input_text)
                self.lineEdit_birthday.setObjectName("lineEdit_birthday")
                self.lineEdit_birthday.setMaxLength(10)

                self.label_adduser_bg = QtWidgets.QLabel(self.users)
                self.label_adduser_bg.setGeometry(QtCore.QRect(360, 10, 330, 290))
                self.label_adduser_bg.setStyleSheet(self.styleSheet.label_bg)
                self.label_adduser_bg.setObjectName("label_adduser_bg")

                self.label_adduser_bg.raise_()
                self.lineEdit_organization.raise_()
                self.lineEdit_birthday.raise_()
                self.label_permissions_bg.raise_()
                self.label_add_user_title.raise_()
                self.label_permissions_title.raise_()
                self.checkbox_report.raise_()
                self.checkbox_inreport.raise_()
                self.checkbox_start_day.raise_()
                self.checkbox_admin.raise_()
                self.btn_adduser_save.raise_()
                self.lineEdit_username.raise_()
                self.btn_adduser_cancel.raise_()
                self.lineEdit_login.raise_()
                self.label_edit_title.raise_()
                self.label_edit_date.raise_()
                self.checkbox_hiddenSoft_R.raise_()
                self.checkbox_hiddenSoft_RW.raise_()
                self.checkbox_specialReport.raise_()

                self.tabWidget.addTab(self.users, "")
                self.combobox_username = QtWidgets.QComboBox(Form)
                self.combobox_username.setGeometry(QtCore.QRect(20, 20, 330, 50))
                self.combobox_username.setFont(self.font)
                self.combobox_username.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
                self.combobox_username.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
                self.combobox_username.setStyleSheet(self.styleSheet.combobox)
                self.combobox_username.setEditable(False)
                self.combobox_username.setFrame(False)
                self.combobox_username.setObjectName("combobox_username")
                self.combobox_username.setMaxVisibleItems(45)
                
                self.label_errors = QtWidgets.QLabel(Form)
                self.label_errors.setGeometry(QtCore.QRect(310, 20, 390, 50))
                self.label_errors.setFont(self.font)
                self.label_errors.setStyleSheet("""
                        QLabel {{
                                background-color: transparent;
                                color: {hover_negative};
                        }}
                """.format(
                        hover_negative = colors.hover_negative
                ))
                self.label_errors.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight|QtCore.Qt.AlignmentFlag.AlignTop|QtCore.Qt.AlignmentFlag.AlignTrailing)
                self.label_errors.setObjectName("label_errors")

                self.btn_changeuser_save = QtWidgets.QPushButton(self.users)
                self.btn_changeuser_save.setEnabled(True)
                self.btn_changeuser_save.setGeometry(QtCore.QRect(20, 200+60, 210, 30))
                self.btn_changeuser_save.setFont(self.font)
                self.btn_changeuser_save.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
                self.btn_changeuser_save.setStyleSheet(self.styleSheet.inverse_btn)
                self.btn_changeuser_save.setObjectName("btn_changeuser_save")

                self.btn_changeuser_cancel = QtWidgets.QPushButton(self.users)
                self.btn_changeuser_cancel.setEnabled(True)
                self.btn_changeuser_cancel.setGeometry(QtCore.QRect(240, 200+60, 90, 30))
                self.btn_changeuser_cancel.setFont(self.font)
                self.btn_changeuser_cancel.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
                self.btn_changeuser_cancel.setStyleSheet(self.styleSheet.inverse_btn)
                self.btn_changeuser_cancel.setObjectName("btn_changeuser_cancel")

                self.label_deluser_bg = QtWidgets.QLabel(self.users)
                self.label_deluser_bg.setGeometry(QtCore.QRect(10, 290+20, 330, 120))
                self.label_deluser_bg.setFont(self.font)
                self.label_deluser_bg.setStyleSheet(self.styleSheet.label_bg)
                self.label_deluser_bg.setObjectName("label_deluser_bg")

                self.label_deluser_title = QtWidgets.QLabel(self.users)
                self.label_deluser_title.setGeometry(QtCore.QRect(10, 300+20, 330, 20))
                self.label_deluser_title.setFont(self.font)
                self.label_deluser_title.setStyleSheet(self.styleSheet.label_text)
                self.label_deluser_title.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                self.label_deluser_title.setObjectName("label_deluser_title")

                self.lineEdit_deluser_reason = QtWidgets.QLineEdit(self.users)
                self.lineEdit_deluser_reason.setGeometry(QtCore.QRect(20, 330+20, 310, 30))
                self.lineEdit_deluser_reason.setFont(lineEdit_font)
                self.lineEdit_deluser_reason.setStyleSheet(self.styleSheet.input_text)
                self.lineEdit_deluser_reason.setObjectName("lineEdit_deluser_reason")

                self.btn_deleteuser = QtWidgets.QPushButton(self.users)
                self.btn_deleteuser.setEnabled(True)
                self.btn_deleteuser.setGeometry(QtCore.QRect(20, 370+20, 170, 30))
                self.btn_deleteuser.setFont(self.font)
                self.btn_deleteuser.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
                self.btn_deleteuser.setStyleSheet(self.styleSheet.inverse_btn)
                self.btn_deleteuser.setObjectName("btn_deleteuser")

                self.tab_workday()
                self.tab_hidden_software()
                self.retranslateUi(Form)
                self.tabWidget.setCurrentIndex(0)
                QtCore.QMetaObject.connectSlotsByName(Form)

        def tab_workday(self):
                self.workday = QtWidgets.QWidget()
                self.workday.setObjectName("workday")
                self.tabWidget.addTab(self.workday, "")

                # Фоны
                self.btns_bg = QtWidgets.QLabel(self.workday)
                self.btns_bg.setGeometry(QtCore.QRect(10, 10, 330, 130))
                self.btns_bg.setObjectName("btns_bg")
                self.btns_bg.setStyleSheet(self.styleSheet.label_bg)

                self.info_bg = QtWidgets.QLabel(self.workday)
                self.info_bg.setGeometry(QtCore.QRect(10, 160, 330, 110))
                self.info_bg.setObjectName("info_bg")
                self.info_bg.setStyleSheet(self.styleSheet.label_bg)

                self.info_sum_bg = QtWidgets.QLabel(self.workday)
                self.info_sum_bg.setGeometry(QtCore.QRect(10, 280, 330, 50))
                self.info_sum_bg.setObjectName("info_sum_bg")
                self.info_sum_bg.setStyleSheet(self.styleSheet.label_bg)

                self.status_bg = QtWidgets.QLabel(self.workday)
                self.status_bg.setGeometry(QtCore.QRect(360, 10, 330, 320))
                self.status_bg.setObjectName("status_bg")
                self.status_bg.setStyleSheet(self.styleSheet.label_bg)

                # Кнопки
                self.btn_start = QtWidgets.QPushButton(self.workday)
                self.btn_start.setObjectName("btn_start")
                self.btn_start.setFont(self.font)
                self.btn_start.setGeometry(QtCore.QRect(20, 20, 310, 30))
                self.btn_start.setStyleSheet(self.styleSheet.inverse_btn_off)
                self.btn_start.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
                self.btn_start.setEnabled(False)
                
                self.btn_dinner = QtWidgets.QPushButton(self.workday)
                self.btn_dinner.setObjectName("btn_dinner")
                self.btn_dinner.setFont(self.font)
                self.btn_dinner.setGeometry(QtCore.QRect(20, 60, 310, 30))
                self.btn_dinner.setStyleSheet(self.styleSheet.inverse_btn_off)
                self.btn_dinner.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
                self.btn_dinner.setEnabled(False)
                
                self.btn_end = QtWidgets.QPushButton(self.workday)
                self.btn_end.setObjectName("btn_end")
                self.btn_end.setFont(self.font)
                self.btn_end.setGeometry(QtCore.QRect(20, 100, 310, 30))
                self.btn_end.setStyleSheet(self.styleSheet.inverse_btn_off)
                self.btn_end.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
                self.btn_end.setEnabled(False)

                # Label с обозначениями
                self.label_time_start = QtWidgets.QLabel(self.workday)
                self.label_time_start.setGeometry(QtCore.QRect(20, 170, 130, 30))
                self.label_time_start.setFont(self.font)
                self.label_time_start.setStyleSheet(self.styleSheet.label_text)
                self.label_time_start.setObjectName("label_time_start")
                
                self.label_time_dinner = QtWidgets.QLabel(self.workday)
                self.label_time_dinner.setGeometry(QtCore.QRect(20, 200, 130, 30))
                self.label_time_dinner.setFont(self.font)
                self.label_time_dinner.setStyleSheet(self.styleSheet.label_text)
                self.label_time_dinner.setObjectName("label_time_dinner")
                
                self.label_time_end = QtWidgets.QLabel(self.workday)
                self.label_time_end.setGeometry(QtCore.QRect(20, 230, 130, 30))
                self.label_time_end.setFont(self.font)
                self.label_time_end.setStyleSheet(self.styleSheet.label_text)
                self.label_time_end.setObjectName("label_time_end")
                
                self.label_sum = QtWidgets.QLabel(self.workday)
                self.label_sum.setGeometry(QtCore.QRect(20, 290, 180, 30))
                self.label_sum.setFont(self.font)
                self.label_sum.setStyleSheet(self.styleSheet.label_text)
                self.label_sum.setObjectName("label_sum")

                # Label со значениями начало/обед/конца
                self.info_start = QtWidgets.QLabel(self.workday)
                self.info_start.setGeometry(QtCore.QRect(200, 170, 130, 30))
                self.info_start.setFont(self.font)
                self.info_start.setStyleSheet(self.styleSheet.label_text)
                self.info_start.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeading|QtCore.Qt.AlignmentFlag.AlignRight|QtCore.Qt.AlignmentFlag.AlignVCenter)
                self.info_start.setObjectName("info_start")
                
                self.info_dinner = QtWidgets.QLabel(self.workday)
                self.info_dinner.setGeometry(QtCore.QRect(200, 200, 130, 30))
                self.info_dinner.setFont(self.font)
                self.info_dinner.setStyleSheet(self.styleSheet.label_text)
                self.info_dinner.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeading|QtCore.Qt.AlignmentFlag.AlignRight|QtCore.Qt.AlignmentFlag.AlignVCenter)
                self.info_dinner.setObjectName("info_dinner")
                
                self.info_end = QtWidgets.QLabel(self.workday)
                self.info_end.setGeometry(QtCore.QRect(200, 230, 130, 30))
                self.info_end.setFont(self.font)
                self.info_end.setStyleSheet(self.styleSheet.label_text)
                self.info_end.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeading|QtCore.Qt.AlignmentFlag.AlignRight|QtCore.Qt.AlignmentFlag.AlignVCenter)
                self.info_end.setObjectName("info_end")
                
                self.info_sum = QtWidgets.QLabel(self.workday)
                self.info_sum.setGeometry(QtCore.QRect(220, 290, 110, 30))
                self.info_sum.setFont(self.font)
                self.info_sum.setStyleSheet(self.styleSheet.label_text)
                self.info_sum.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeading|QtCore.Qt.AlignmentFlag.AlignRight|QtCore.Qt.AlignmentFlag.AlignVCenter)
                self.info_sum.setObjectName("info_sum")
                
                self.status_title = QtWidgets.QLabel(self.workday)
                self.status_title.setGeometry(QtCore.QRect(360, 20, 330, 30))
                self.status_title.setFont(self.font)
                self.status_title.setStyleSheet(self.styleSheet.label_text)
                self.status_title.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeading|QtCore.Qt.AlignmentFlag.AlignHCenter|QtCore.Qt.AlignmentFlag.AlignVCenter)
                self.status_title.setObjectName("status_title")

        def tab_hidden_software(self):
                self.hidden_software = QtWidgets.QWidget()
                self.hidden_software.setObjectName('hidden_software')
                self.tabWidget.addTab(self.hidden_software, '')

                self.label_find_bg = QtWidgets.QLabel(self.hidden_software)
                self.label_find_bg.setGeometry(QtCore.QRect(10, 10, 400, 40))
                self.label_find_bg.setObjectName("label_find_bg")
                self.label_find_bg.setStyleSheet(self.styleSheet.label_bg)

                self.label_find = QtWidgets.QLabel(self.hidden_software)
                self.label_find.setGeometry(QtCore.QRect(10, 10, 80, 40))
                self.label_find.setFont(self.font)
                self.label_find.setStyleSheet(self.styleSheet.label_text)
                self.label_find.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                self.label_find.setObjectName("label_period")
                self.label_find.setText("Поиск:")

                lineEdit_FindFont = QtGui.QFont()
                lineEdit_FindFont.setFamily("Montserrat")
                lineEdit_FindFont.setWeight(700)

                self.lineEdit_find = QtWidgets.QLineEdit(self.hidden_software)
                self.lineEdit_find.setGeometry(QtCore.QRect(90, 15, 310, 30))
                self.lineEdit_find.setFont(lineEdit_FindFont)
                self.lineEdit_find.setStyleSheet(self.styleSheet.input_text)
                self.lineEdit_find.setMaxLength(8)
                self.lineEdit_find.setCursorPosition(0)
                self.lineEdit_find.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                self.lineEdit_find.setObjectName("lineEdit_find")
                self.lineEdit_find.setPlaceholderText("Имя ПК")

                self.label_FindResult_bg = QtWidgets.QLabel(self.hidden_software)
                self.label_FindResult_bg.setGeometry(QtCore.QRect(10, 60, 150, 350))
                self.label_FindResult_bg.setStyleSheet(self.styleSheet.label_bg)
                self.label_FindResult_bg.setObjectName("label_FindResult_bg")

                self.btn_addHiddenPC = QtWidgets.QPushButton(self.hidden_software)
                self.btn_addHiddenPC.setGeometry(QtCore.QRect(419, 10, 130, 40))
                self.btn_addHiddenPC.setFont(self.font)
                self.btn_addHiddenPC.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
                self.btn_addHiddenPC.setStyleSheet(self.styleSheet.btn_off)
                self.btn_addHiddenPC.setEnabled(False)
                self.btn_addHiddenPC.setObjectName("btn_addHiddenPC")
                self.btn_addHiddenPC.setText("Добавить ПК")

                self.label_title_findResults = QtWidgets.QLabel(self.hidden_software)
                self.label_title_findResults.setGeometry(QtCore.QRect(10, 60, 150, 40))
                self.label_title_findResults.setFont(self.font)
                self.label_title_findResults.setStyleSheet(self.styleSheet.label_text)
                self.label_title_findResults.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                self.label_title_findResults.setObjectName("label_title_findResults")
                self.label_title_findResults.setText('Введите запрос')

                self.btn_generateReportHiddenSoft = QtWidgets.QPushButton(self.hidden_software)
                self.btn_generateReportHiddenSoft.setGeometry(QtCore.QRect(560, 10, 130, 40))
                self.btn_generateReportHiddenSoft.setFont(self.font)
                self.btn_generateReportHiddenSoft.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
                self.btn_generateReportHiddenSoft.setObjectName("btn_generateReportHiddenSoft")
                self.btn_generateReportHiddenSoft.setStyleSheet(self.styleSheet.btn_off)
                self.btn_generateReportHiddenSoft.setEnabled(False)
                self.btn_generateReportHiddenSoft.setText('Excel отчет')

                self.label_PCInfo_bg = QtWidgets.QLabel(self.hidden_software)
                self.label_PCInfo_bg.setGeometry(QtCore.QRect(170, 60, 520, 270))
                self.label_PCInfo_bg.setStyleSheet(self.styleSheet.label_bg)
                self.label_PCInfo_bg.setObjectName("label_PCInfo_bg")

                self.label_title_PCInfo = QtWidgets.QLabel(self.hidden_software)
                self.label_title_PCInfo.setGeometry(QtCore.QRect(170, 60, 520, 40))
                self.label_title_PCInfo.setFont(self.font)
                self.label_title_PCInfo.setStyleSheet(self.styleSheet.label_text)
                self.label_title_PCInfo.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                self.label_title_PCInfo.setObjectName("label_title_PCInfo")
                self.label_title_PCInfo.setText('Выберите ПК')

                self.label_whenPCadd = QtWidgets.QLabel(self.hidden_software)
                self.label_whenPCadd.setGeometry(QtCore.QRect(180, 100, 520, 40))
                self.label_whenPCadd.setFont(self.font)
                self.label_whenPCadd.setStyleSheet(self.styleSheet.label_text)
                self.label_whenPCadd.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeft)
                self.label_whenPCadd.setObjectName("label_whenPCadd")

                self.label_whoAddPC = QtWidgets.QLabel(self.hidden_software)
                self.label_whoAddPC.setGeometry(QtCore.QRect(180, 120, 520, 40))
                self.label_whoAddPC.setFont(self.font)
                self.label_whoAddPC.setStyleSheet(self.styleSheet.label_text)
                self.label_whoAddPC.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeft)
                self.label_whoAddPC.setObjectName("label_whoAddPC")

                self.label_whenPCadd_time = QtWidgets.QLabel(self.hidden_software)
                self.label_whenPCadd_time.setGeometry(QtCore.QRect(180, 100, 500, 40))
                self.label_whenPCadd_time.setFont(self.font)
                self.label_whenPCadd_time.setStyleSheet(self.styleSheet.label_text)
                self.label_whenPCadd_time.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight)
                self.label_whenPCadd_time.setObjectName("label_whenPCadd_time")

                self.label_whoAddPC_username = QtWidgets.QLabel(self.hidden_software)
                self.label_whoAddPC_username.setGeometry(QtCore.QRect(180, 120, 500, 40))
                self.label_whoAddPC_username.setFont(self.font)
                self.label_whoAddPC_username.setStyleSheet(self.styleSheet.label_text)
                self.label_whoAddPC_username.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight)
                self.label_whoAddPC_username.setObjectName("label_whoAddPC_username")

                self.label_AddPC_namePC = QtWidgets.QLabel(self.hidden_software)
                self.label_AddPC_namePC.setGeometry(QtCore.QRect(180, 110, 120, 30))
                self.label_AddPC_namePC.setFont(self.font)
                self.label_AddPC_namePC.setStyleSheet(self.styleSheet.label_text)
                self.label_AddPC_namePC.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeft)
                self.label_AddPC_namePC.setObjectName("label_AddPC_namePC")
                self.label_AddPC_namePC.setText('Имя ПК')
                self.label_AddPC_namePC.setHidden(True)

                self.lineEdit_AddPC_namePC = QtWidgets.QLineEdit(self.hidden_software)
                self.lineEdit_AddPC_namePC.setGeometry(QtCore.QRect(330, 105, 350, 30))
                self.lineEdit_AddPC_namePC.setFont(lineEdit_FindFont)
                self.lineEdit_AddPC_namePC.setStyleSheet(self.styleSheet.input_text)
                self.lineEdit_AddPC_namePC.setCursorPosition(0)
                self.lineEdit_AddPC_namePC.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeft)
                self.lineEdit_AddPC_namePC.setObjectName("lineEdit_AddPC_namePC")
                self.lineEdit_AddPC_namePC.setPlaceholderText("Имя ПК")
                self.lineEdit_AddPC_namePC.setHidden(True)
                self.lineEdit_AddPC_namePC.setMaxLength(8)

                self.label_AddressPC = QtWidgets.QLabel(self.hidden_software)
                self.label_AddressPC.setGeometry(QtCore.QRect(180, 145, 120, 30))
                self.label_AddressPC.setFont(self.font)
                self.label_AddressPC.setStyleSheet(self.styleSheet.label_text)
                self.label_AddressPC.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeft)
                self.label_AddressPC.setObjectName("label_AddressPC")
                self.label_AddressPC.setText('Адрес:')
                self.label_AddressPC.setHidden(True)

                self.lineEdit_AddressPC = QtWidgets.QLineEdit(self.hidden_software)
                self.lineEdit_AddressPC.setGeometry(QtCore.QRect(330, 140, 350, 30))
                self.lineEdit_AddressPC.setFont(lineEdit_FindFont)
                self.lineEdit_AddressPC.setStyleSheet(self.styleSheet.input_text)
                self.lineEdit_AddressPC.setCursorPosition(0)
                self.lineEdit_AddressPC.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeft)
                self.lineEdit_AddressPC.setObjectName("lineEdit_AddressPC")
                self.lineEdit_AddressPC.setPlaceholderText("Адрес установки")
                self.lineEdit_AddressPC.setHidden(True)

                self.label_PCusername = QtWidgets.QLabel(self.hidden_software)
                self.label_PCusername.setGeometry(QtCore.QRect(180, 180, 120, 30))
                self.label_PCusername.setFont(self.font)
                self.label_PCusername.setStyleSheet(self.styleSheet.label_text)
                self.label_PCusername.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeft)
                self.label_PCusername.setObjectName("label_PCusername")
                self.label_PCusername.setText('Пользователь:')
                self.label_PCusername.setHidden(True)

                self.lineEdit_PCusername = QtWidgets.QLineEdit(self.hidden_software)
                self.lineEdit_PCusername.setGeometry(QtCore.QRect(330, 175, 350, 30))
                self.lineEdit_PCusername.setFont(lineEdit_FindFont)
                self.lineEdit_PCusername.setStyleSheet(self.styleSheet.input_text)
                self.lineEdit_PCusername.setCursorPosition(0)
                self.lineEdit_PCusername.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeft)
                self.lineEdit_PCusername.setObjectName("lineEdit_PCusername")
                self.lineEdit_PCusername.setPlaceholderText("ФИО пользователя")
                self.lineEdit_PCusername.setHidden(True)

                self.label_PCcase = QtWidgets.QLabel(self.hidden_software)
                self.label_PCcase.setGeometry(QtCore.QRect(180, 215, 120, 30))
                self.label_PCcase.setFont(self.font)
                self.label_PCcase.setStyleSheet(self.styleSheet.label_text)
                self.label_PCcase.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeft)
                self.label_PCcase.setObjectName("label_PCcase")
                self.label_PCcase.setText('Кейс:')
                self.label_PCcase.setHidden(True)

                self.lineEdit_PCcase = QtWidgets.QLineEdit(self.hidden_software)
                self.lineEdit_PCcase.setGeometry(QtCore.QRect(330, 210, 350, 30))
                self.lineEdit_PCcase.setFont(lineEdit_FindFont)
                self.lineEdit_PCcase.setStyleSheet(self.styleSheet.input_text)
                self.lineEdit_PCcase.setCursorPosition(0)
                self.lineEdit_PCcase.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeft)
                self.lineEdit_PCcase.setObjectName("lineEdit_PCcase")
                self.lineEdit_PCcase.setPlaceholderText("Номер кейса")
                self.lineEdit_PCcase.setHidden(True)

                self.label_PCsoft = QtWidgets.QLabel(self.hidden_software)
                self.label_PCsoft.setGeometry(QtCore.QRect(180, 250, 120, 30))
                self.label_PCsoft.setFont(self.font)
                self.label_PCsoft.setStyleSheet(self.styleSheet.label_text)
                self.label_PCsoft.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeft)
                self.label_PCsoft.setObjectName("label_PCsoft")
                self.label_PCsoft.setText('Программы:')
                self.label_PCsoft.setHidden(True)

                self.lineEdit_PCsoft = QtWidgets.QLineEdit(self.hidden_software)
                self.lineEdit_PCsoft.setGeometry(QtCore.QRect(330, 245, 350, 30))
                self.lineEdit_PCsoft.setFont(lineEdit_FindFont)
                self.lineEdit_PCsoft.setStyleSheet(self.styleSheet.input_text)
                self.lineEdit_PCsoft.setCursorPosition(0)
                self.lineEdit_PCsoft.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeft)
                self.lineEdit_PCsoft.setObjectName("lineEdit_PCsoft")
                self.lineEdit_PCsoft.setPlaceholderText("Название ПО")
                self.lineEdit_PCsoft.setHidden(True)

                self.btn_savePC = QtWidgets.QPushButton(self.hidden_software)
                self.btn_savePC.setEnabled(True)
                self.btn_savePC.setGeometry(QtCore.QRect(430, 290, 120, 30))
                self.btn_savePC.setFont(self.font)
                self.btn_savePC.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
                self.btn_savePC.setStyleSheet(self.styleSheet.inverse_btn)
                self.btn_savePC.setObjectName("btn_savePC")
                self.btn_savePC.setText("Сохранить")
                self.btn_savePC.setHidden(True)

                self.btn_cancelPC = QtWidgets.QPushButton(self.hidden_software)
                self.btn_cancelPC.setEnabled(True)
                self.btn_cancelPC.setGeometry(QtCore.QRect(560, 290, 120, 30))
                self.btn_cancelPC.setFont(self.font)
                self.btn_cancelPC.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
                self.btn_cancelPC.setStyleSheet(self.styleSheet.inverse_btn)
                self.btn_cancelPC.setObjectName("btn_cancelPC")
                self.btn_cancelPC.setText("Отмена")
                self.btn_cancelPC.setHidden(True)

                self.label_PCdelete_bg = QtWidgets.QLabel(self.hidden_software)
                self.label_PCdelete_bg.setGeometry(QtCore.QRect(170, 340, 520, 50))
                self.label_PCdelete_bg.setStyleSheet(self.styleSheet.label_bg)
                self.label_PCdelete_bg.setObjectName("label_PCdelete_bg")
                self.label_PCdelete_bg.setHidden(True)

                self.lineEdit_PCdelete = QtWidgets.QLineEdit(self.hidden_software)
                self.lineEdit_PCdelete.setGeometry(QtCore.QRect(180, 350, 370, 30))
                self.lineEdit_PCdelete.setFont(lineEdit_FindFont)
                self.lineEdit_PCdelete.setStyleSheet(self.styleSheet.input_text)
                self.lineEdit_PCdelete.setCursorPosition(0)
                self.lineEdit_PCdelete.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeft)
                self.lineEdit_PCdelete.setObjectName("lineEdit_PCsoft")
                self.lineEdit_PCdelete.setPlaceholderText("Причина удаления")
                self.lineEdit_PCdelete.setHidden(True)

                self.btn_deletePC = QtWidgets.QPushButton(self.hidden_software)
                self.btn_deletePC.setEnabled(False)
                self.btn_deletePC.setGeometry(QtCore.QRect(560, 350, 120, 30))
                self.btn_deletePC.setFont(self.font)
                self.btn_deletePC.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
                self.btn_deletePC.setStyleSheet(self.styleSheet.inverse_btn_off)
                self.btn_deletePC.setObjectName("btn_deletePC")
                self.btn_deletePC.setText("Удалить")
                self.btn_deletePC.setHidden(True)
                
        def retranslateUi(self, Form):
                Form.setWindowTitle("WorkDay")

                # Выбор периода
                self.label_period.setText("Период:")                            # Label с надписью период
                self.lineEdit_startdate.setPlaceholderText("DD.MM.YYYY")        # Форма для написания даты начала периода
                self.lineEdit_enddate.setPlaceholderText("DD.MM.YYYY")          # Форма с датой конца периода
                self.btn_this_month.setText("Этот месяц")                       # Кнопка для автомамтического установления периода в текущий месяц (первое и последнее число)

                self.btn_generate_report.setText("Отчет за период")             # Кнопка для получения отчета за выбранный период

                # Показ отчета
                self.label_title_date.setText('')                               # Когда выбирается период данный label изменяется на заголовок "Дата"
                self.label_title_weekday.setText('Выберите период')             # При старте и не выбранном периоде выводит текст "Выберите период", а после выбора становится заголовком "Неделя"
                self.label_report_count.setText('')                             # Когда выбирается период данный label изменяется на заголовок "Отработано"

                # Редактирование отчета
                self.label_edit_title.setText("Редактирование записи")          # Заголовок
                self.label_edit_date.setText("Дата")                            # Label для показа что означает поля для ввода
                self.label_edit_worktime.setText("Рабочее время:")
                self.label_edit_dinnertime.setText("Обед:")
                self.lineEdit_edit_date.setPlaceholderText("dd.mm.yyyy".upper())        # Формат ввода даты
                self.lineEdit_edit_end_day.setPlaceholderText("hh:mm".upper())
                self.label_edit_start_day.setText("с")
                self.lineEdit_edit_start_day.setText('')
                self.lineEdit_edit_start_day.setPlaceholderText("hh:mm".upper())
                self.label_edit_end_day.setText("до")
                self.btn_generate_addrecord.setText("Добавить запись")
                self.lineEdit_edit_end_dinner.setText('')
                self.lineEdit_edit_end_dinner.setPlaceholderText("hh:mm".upper())
                self.label_edit_start_dinner.setText("с")
                self.lineEdit_edit_start_dinner.setText('')
                self.lineEdit_edit_start_dinner.setPlaceholderText("hh:mm".upper())
                self.label_edit_end_dinner.setText("до")
                self.btn_save_edit.setText("Сохранить")
                self.lineEdit_delete_reason.setPlaceholderText("Причина удаления")
                self.btn_cancel_edit.setText("Отмена")
                self.checkbox_timeoff.setText("Отгул")
                self.checkbox_autostop.setText("Автоматическое завершение")
                self.btn_delete_record.setText("Удалить")
                self.label_report_allhours.setText("В периоде:")
                self.label_report_count_hours.setText("198")
                self.tabWidget.setTabText(self.tabWidget.indexOf(self.reports), "Отчетность")

                self.label_permissions_title.setText("Разрешения")
                self.checkbox_report.setText("Редактирование отчета")
                self.checkbox_inreport.setText("Отображение в отчете")
                self.checkbox_start_day.setText("Запуск таймера")
                self.checkbox_admin.setText("Администратор")
                self.checkbox_hiddenSoft_R.setText('Скрытое ПО - R')
                self.checkbox_hiddenSoft_RW.setText('Скрытое ПО - RW')
                self.checkbox_specialReport.setText('Специальный отчет')

                self.btn_adduser_save.setText("Добавить")
                self.lineEdit_username.setPlaceholderText("ФИО")
                self.btn_adduser_cancel.setText("Отмена")
                self.label_add_user_title.setText("Добавить пользователя")
                self.lineEdit_login.setPlaceholderText("Логин")
                self.lineEdit_organization.setPlaceholderText('Организация')
                self.lineEdit_birthday.setPlaceholderText('Дата рождения')
                self.tabWidget.setTabText(self.tabWidget.indexOf(self.users), "Пользователь")
                self.label_errors.setText("") # Label для вывода информации
                self.btn_changeuser_save.setText('Сохранить')
                self.btn_changeuser_cancel.setText('Отмена')

                # Удаление пользователя
                self.label_deluser_title.setText('Удалить пользователя')
                self.btn_deleteuser.setText('Удалить')
                self.lineEdit_deluser_reason.setPlaceholderText('Причина удаления')

                # Вкладка WorkDay
                self.tabWidget.setTabText(self.tabWidget.indexOf(self.workday), "WorkDay")

                # Вкладка с пиратским ПО
                self.tabWidget.setTabText(self.tabWidget.indexOf(self.hidden_software), "Пиратское ПО")
                
                self.btn_start.setText('К работе приступил')
                self.btn_dinner.setText('Ушел на обед')
                self.btn_end.setText('Работать закончил')

                self.label_time_start.setText('Время начала')
                self.label_time_dinner.setText('Время обеда')
                self.label_time_end.setText('Время конца')
                self.label_sum.setText('Всего отработано часов:')

                self.info_start.setText('--.--.---- --:--')
                self.info_dinner.setText('--:--')
                self.info_end.setText('--.--.---- --:--')
                self.info_sum.setText('--:--')

                self.status_title.setText('Статусы')

# Путь до БД, расположен на хомяке it_lunatic (возможно далее будет изменен)
database_path = r'\\x3.corp.motiv\support$\it_lunatic\Разработка\Python\workday.sqlite'

class MainWindow(QtWidgets.QMainWindow, Ui_Form, Ui_error):
        def __init__(self):
                super().__init__()
                self.databaseExists = True

                # Проверка наличия БД
                if not os.path.exists(database_path):
                        self.styleSheet = styleSheet.styleSheet(colors)
                        self.databaseExists = False
                        print('Куда базу сперли, ироды?!')
                        self.setup_error(self)
                        self.label.setText('Базу данных кто-то спизд*л, ищите жулика')
                        return

                # Установление соединения с БД
                self.connect = sqlite3.connect(database_path)
                self.cursor = self.connect.cursor()

                # Создание объекта "Пользователь", через который будет большая часть взаимодействия с БД
                self.user = db.user(self.connect, self.cursor)

                # Проверяем доступность приложения
                app_isEnabled = int(self.cursor.execute('SELECT value FROM options WHERE name = "app_isEnabled"').fetchone()[0])
                if not app_isEnabled:
                        self.styleSheet = styleSheet.styleSheet(colors)
                        print('Приложение не возможно запустить, такая возможность выключена в БД')
                        self.setup_error(self)
                        self.label.setText('Не получилось запустить приложение')
                        return
                
                modules_list = ("report_isEnabled", "users_isEnabled", "hiddenSoft_isEnabled", "workDay_isEnabled", "vacations_isEnabled")
                self.report_isEnabled, self.users_isEnabled, self.hiddenSoft_isEnabled, self.workDay_isEnabled, self.vacations_isEnabled = [
                        self.cursor.execute('SELECT value FROM options WHERE name = "{name}"'.format(name=x)).fetchone()[0] for x in modules_list
                ]

                if self.user.my_info:
                        # В переменной self.user.my_info хранятся данные, полученные с БД.
                        # Данное условие выполняется если при запросе было получено какое-нибудь значение с данными

                        # В таблице themes хранятся персональные цвета для сотрудников, которым они нужны
                        # Если в этой таблице есть запись для этого сотрудника, то будет активирована цветовая схема,
                        # использующая цвета в соответствующих колонках
                        color_theme = self.cursor.execute("""
                                SELECT text_color, background, rectangle, hover, hover_negative, non_active_color, indicator_border, text_color_inverse
                                FROM themes
                                WHERE id_user = {id_user}
                        """.format(
                                id_user = self.user.my_id
                        )).fetchone()

                        if color_theme:
                                # Установка цвета
                                colors.my_theme(
                                        text_color = color_theme[0],
                                        background = color_theme[1],
                                        rectangle = color_theme[2],
                                        hover = color_theme[3],
                                        hover_negative = color_theme[4],
                                        non_active_color = color_theme[5],
                                        indicator_border = color_theme[6],
                                        text_color_inverse = color_theme[7]
                                )

                        self.styleSheet = styleSheet.styleSheet(colors)

                        # Проверка версии приложения
                        db_version = self.cursor.execute("SELECT value FROM options WHERE name = 'app_version'").fetchone()[0]
                        if APP_VERSION <= db_version:
                                self.setup_error(self)
                                self.label.setText('Появилась новая версия приложения, необходимо обновить')
                                self.btn.setText('Обновить')

                                # Получаем настройку из БД, в которой говорится какую папку необходимо открыть, чтобы обновить
                                newapp_folder = self.cursor.execute("""
                                        SELECT value_text FROM options
                                        WHERE name = 'newapp_folder'
                                """).fetchone()
                                if newapp_folder:
                                        newapp_folder = newapp_folder[0]
                                        self.btn.clicked.connect(lambda x: self.open_update_folder(newapp_folder))
                                return
                        
                        if self.vacations_isEnabled:
                                # Проверяем и отправляем письма об отпусках
                                try:
                                        vacation = Vacation(self.cursor, self.connect)
                                        vacation.auto()
                                        vacation.close()
                                except Exception as e:
                                        self.user.error(str(e))
                                        self.user.insert_log(53, datetime.datetime.now(), 'Неудачная попытка отправить письма об отпусках', new_value=str(e))
                        
                        if self.user.my_root_report or self.user.my_root_admin or (self.user.my_root_startday and self.user.my_root_inReport) or (self.user.my_root_hidden_software_r or self.user.my_root_hidden_software_rw):
                                self.setupUi(self)

                                # Записываем логи о запуске приложения
                                if not self.user.testMode:
                                        self.cursor.execute("""
                                                INSERT INTO app_starting(id_user, hostname, start_time, app_version)
                                                VALUES 
                                                ({id_user}, '{hostname}', '{start_time}', '{app_version}')
                                        """.format(
                                                id_user = self.user.my_id,
                                                hostname = gethostname().upper(),
                                                start_time = report.date_datetime(datetime.datetime.now(), mode='class').format_db,
                                                app_version = APP_VERSION
                                        ))
                                        self.connect.commit()

                                if self.user.testMode:
                                        print('[TEST MODE]')
                                        self.label_errors.setText('Запущено в тестовом режиме')

                                self.combobox_username.currentTextChanged.connect(self.update_info)                             # Прослушка combobox (с пользователями) на изменение

                                self.btn_this_month.clicked.connect(self.btn_period_this_month)                                 # Прослушка кнопки "Этот месяц"

                                self.btn_generate_report.setEnabled(False)                                                      # Отключаем кнопку "Отчет за период", чтобы лишний раз не вызывать исключения
                                self.btn_generate_report.setStyleSheet(self.styleSheet.btn_off)
                                self.btn_generate_report.clicked.connect(self.generate_report)                                  # Прослушка кнопки "Отчет за период"
                                
                                self.btn_generate_addrecord.clicked.connect(self.add_record)                                    # Прослушка кнопки "Добавить запись"
                                self.btn_delete_record.setEnabled(False)                                                        # Отключение кнопки "Удалить запись". На случай мисклика
                                self.btn_delete_record.clicked.connect(self.delete_record)
                                self.lineEdit_delete_reason.textChanged.connect(self.deleteDate_changed)                        # Прослушка на изменение текста поля с вводом причины удаления
                                self.show_edit_panel( mode = 'clear' )                                                          # Очищаем панель редактирования записи
                                self.checkbox_timeoff.stateChanged.connect(self.timeoff_clicked)                                # Прослушка чекбокса с отгулом (будут автоматически проставлено стандартное время)
                                self.btn_save_edit.clicked.connect(self.save_report)                                            # Прослушка кнопки сохранить отчет
                                self.btn_cancel_edit.clicked.connect(lambda ch: self.show_edit_panel( mode = 'clear' ))         # Прослушка кнопки отмена отчета

                                self.page = 1                                                                                   # Счетчик текущей страницы
                                self.btn_report_up.clicked.connect(lambda ch: self.change_page( mode = 'up' ))                  # Прослушка кнопки листнуть вверх
                                self.btn_report_down.clicked.connect(lambda ch: self.change_page( mode = 'down' ))              # Прослушка кнопки листнуть вниз

                                self.temp_report_list = []                                                                      # Массив для хранения объектов (label и btn),
                                                                                                                                # которые показываются при вводе периода (или нажатии кнопки "Этот месяц")
                                                                                                                                # Все объекты из данного массива удаляются по вызову ф-ии clear_report()

                                self.temp_pc_list = []                                                                          # Массив в котором хранятся объекты с ПК, которые надо очищать

                                self.old_value = {                                                                              # Нужно чтобы при стирании значений в input, автоматически не подставлялась точка (или :)
                                        self.lineEdit_startdate: '',
                                        self.lineEdit_enddate: '',
                                        self.lineEdit_edit_date: '',
                                        self.lineEdit_edit_start_day: '',
                                        self.lineEdit_edit_end_day: '',
                                        self.lineEdit_edit_start_dinner: '',
                                        self.lineEdit_edit_end_dinner: ''
                                }

                                self.lineEdit_edit_date_isConnected = False                                                     # Статус прослушки редактирования даты в поле редактирования

                                self.btn_report_down.setEnabled(False)
                                self.btn_report_up.setEnabled(False)

                                # След 4 объекта прослушиваются для того, чтобы вручную не подставлять :
                                self.lineEdit_edit_start_day.textChanged.connect(lambda ch, obj = self.lineEdit_edit_start_day: self.edit_time_changed(obj))
                                self.lineEdit_edit_end_day.textChanged.connect(lambda ch, obj = self.lineEdit_edit_end_day: self.edit_time_changed(obj))
                                self.lineEdit_edit_start_dinner.textChanged.connect(lambda ch, obj = self.lineEdit_edit_start_dinner: self.edit_time_changed(obj))
                                self.lineEdit_edit_end_dinner.textChanged.connect(lambda ch, obj = self.lineEdit_edit_end_dinner: self.edit_time_changed(obj))

                                self.lineEdit_startdate.textChanged.connect(lambda ch, obj = self.lineEdit_startdate: self.date_edited(obj))          # Прослушка на изменение поля   "Начало периода"
                                self.lineEdit_enddate.textChanged.connect(lambda ch, obj = self.lineEdit_enddate: self.date_edited(obj))              #                               "Конец периода"

                                self.btn_save_status = None                                                             # В этой переменной хранится статус кнопки, в зависимости от которого будут выполняться разные действия:
                                                                                                                        # Возможные статусы:
                                                                                                                        # 1. None               - он является стандартным, при нем кнопка будет заблокирована
                                                                                                                        # 2. changing           - кнопка находится в статусе "Изменение записи" (в данный момент изменяется та или иная запись)
                                                                                                                        # 3. adding             - в данный момент добавляется новая запись

                                self.lineEdit_username.textChanged.connect(lambda ch, obj = self.lineEdit_username: self.addUser_changed(obj))
                                self.lineEdit_login.textChanged.connect(lambda ch, obj = self.lineEdit_login: self.addUser_changed(obj))
                                self.lineEdit_organization.textChanged.connect(lambda ch, obj = self.lineEdit_organization: self.addUser_changed(obj))
                                self.lineEdit_birthday.textChanged.connect(lambda ch, obj = self.lineEdit_birthday: self.addUser_changed(obj))

                                self.lineEdit_find.textChanged.connect(self.lineEdit_find_changed)
                                self.lineEdit_AddressPC.textChanged.connect(self.lineEdit_AddressPC_changed)
                                self.lineEdit_PCusername.textChanged.connect(self.lineEdit_PCusername_changed)
                                self.lineEdit_PCcase.textChanged.connect(self.lineEdit_PCcase_changed)
                                self.lineEdit_PCsoft.textChanged.connect(self.lineEdit_PCsoft_changed)
                                self.btn_cancelPC.clicked.connect(self.clear_fieldInfoAboutPC)
                                self.btn_savePC.clicked.connect(self.btn_savePC_clicked)
                                self.lineEdit_PCdelete.textChanged.connect(self.lineEdit_PCdelete_changed)
                                self.btn_deletePC.clicked.connect(self.btn_deletePC_clicked)
                                self.lineEdit_AddPC_namePC.textChanged.connect(self.lineEdit_AddPC_changed)
                                self.btn_generateReportHiddenSoft.clicked.connect(self.generateReportAboutHiddenSoftware)

                                self.btn_save_PC_status = None          # В этой переменной хранится статус кнопки, в зависимости от которого будут выполняться разные действия:
                                                                        # Возможные статусы:
                                                                        # 1. None       - стандарт, ничего делаться не будет
                                                                        # 2. changing   - изменение записей о ПК
                                                                        # 3. adding     - добавление записи о ПК

                                self.showedPC_id = 0    # ID ПК, который в данный момент отображается

                                if self.user.my_root_admin and not self.user.my_root_report:
                                        # Данное условие выполняется если у пользователя есть права Администратора, но при этом нету прав на Редактирование отчета

                                        self.btn_adduser_save.clicked.connect(self.add_user)                            # Прослушка кнопки сохранить пользователя на клик
                                        self.btn_adduser_cancel.clicked.connect(self.cancel_add_user)                   # Прослушка кнопки отменить при создании пользователя на клик
                                        self.btn_changeuser_save.clicked.connect(self.change_user)                      # Прослушка кнопки изменить пользователя
                                        self.btn_changeuser_cancel.clicked.connect(self.change_user_cancel)             # Прослушка кнопки отменить при изменении пользователя

                                        self.lineEdit_deluser_reason.textChanged.connect(self.delete_reason_edited)     # Прослушка поля с причиной удаления пользователя
                                        self.btn_deleteuser.clicked.connect(lambda: self.delete_user())                 # Прослушка кнопки "Удалить пользователя"
                                        self.btn_deleteuser.setEnabled(False)                                           # Отключаем кнопку "Удалить пользователя" на случай мисклика

                                        # Запрос в БД на добавление пользователей в checkkbox, после добавляем кажого найденного пользователя в checkbox
                                        user_list = self.cursor.execute(
                                                """
                                                        SELECT users.username, root.inReport, users.id FROM users, root
                                                        WHERE users.id = root.id_user AND users.deleted != 1 AND users.login != 'it_lunatic' AND users.id != {my_id}
                                                        ORDER BY root.inReport DESC, users.username
                                                """.format(
                                                        my_id = self.user.my_id
                                                )
                                        ).fetchall()
                                        for i in user_list:
                                                # Условия прописаны для того, чтобы простой смертный не мог видеть какие права есть у it_lunatic (id = 1)
                                                # Сделано для того, чтобы случайно никто не удалил меня (меня попросто не возможно будет выбрать, следовательно и изменить)
                                                if user_list[2] != 1 and self.user.my_id != 1:
                                                        self.combobox_username.addItem( i[0] )

                                                elif self.user.my_id == 1:
                                                        self.combobox_username.addItem( i[0] )

                                elif self.user.my_root_report and not self.user.my_root_admin:
                                        # Если есть права на Редактирование отчета и при этом не является Администратором

                                        # Прячем 2 вкладку (вкладка для добавления и редактирования пользователей) от тех, у кого нету права на её просмотр, ибо нефиг смотреть туда, куда не надо)
                                        # self.tabWidget.setTabVisible(self.tabWidget.indexOf(self.users), False)
                                        self.tabWidget.removeTab(self.tabWidget.indexOf(self.users))

                                        # Т.к. для редактирования отчета необходимы только определенные пользователи из БД выбираются только те,
                                        # у кого в таблице root значение inReport = 1 (означает что он должен отображаться в отчете).
                                        # Это сделано для того, чтобы не показывались лишние пользователи
                                        user_list = self.cursor.execute(
                                                """
                                                        SELECT users.username, root.inReport FROM users, root
                                                        WHERE users.id = root.id_user AND root.inReport = 1 AND users.deleted != 1
                                                        ORDER BY users.username
                                                """
                                        ).fetchall()
                                        for i in user_list:
                                                self.combobox_username.addItem( i[0] )

                                if self.user.my_root_startday:
                                        # Активация 3 вкладки "WorkDay"

                                        # Проверяем есть ли доступы к 1 и 2 вкладке, если нету, то отключаем их отображение
                                        if not self.user.my_root_report and not self.user.my_root_admin:
                                                # Если нету прав на работу с админкой и отчетами, отключаем вкладку с отчетами и добавляем только 1 пользователя (того, кто запустил)
                                                # self.tabWidget.setTabVisible(self.tabWidget.indexOf(self.reports), False)
                                                self.tabWidget.removeTab(self.tabWidget.indexOf(self.reports))
                                                self.combobox_username.addItem( self.user.my_username )
                                                self.combobox_username.setEnabled(False)

                                        if not self.user.my_root_admin:
                                                # Дополнительно, если нету прав администратора выключаем вкладку с управлением пользователями
                                                # self.tabWidget.setTabVisible(self.tabWidget.indexOf(self.users), False)
                                                self.tabWidget.removeTab(self.tabWidget.indexOf(self.users))

                                        self.btn_start.clicked.connect(self.start_day)
                                        self.btn_dinner.clicked.connect(self.dinner)
                                        self.btn_end.clicked.connect(self.end_day)

                                        # Проверяем закрыта ли последняя найденная запись
                                        self.check_last_record()
                   
                                        self.updater = Thread()                                 # Поток для автоматического обновления информации о времени работы / обеда
                                        self.updater.signal.connect(self.wd_update)

                                        # Загружаем пользователей, которые могут запускать WorkDay в список "Статусы"
                                        # после запускаем обновление данных о них
                                        self.users_status = {}
                                        users_startday = self.cursor.execute("""
                                                SELECT users.username FROM root, users
                                                WHERE users.id = root.id_user AND root.start_day = 1
                                        """).fetchall()
                                        y = 60
                                        for user in users_startday:
                                                user = user[0]
                                                self.status_username = QtWidgets.QLabel(self.workday)
                                                self.status_username.setGeometry(QtCore.QRect(370, y, 300, 15))
                                                self.status_username.setFont(self.font)
                                                self.status_username.setText(user)
                                                self.status_username.setObjectName(user)
                                                self.status_username.setStyleSheet(self.styleSheet.status_off)
                                                self.users_status[user] = self.status_username
                                                y += 25

                                        self.status_updater = Thread()                          # Поток для автоматического обновления статусов работы других сотрудников
                                        self.status_updater.signal.connect(self.status_update)
                                        self.status_updater.start()

                                        # флаг заканчивался ли обед. Если обед не закончился, то он не будет учитываться при:
                                        # 1 - автоматическом завершении
                                        self.isDinnerEnded = False

                                        # Получаем данные на сегодняшний день, есть ли запись за сегодня
                                        self.today = report.date_datetime('today')
                                        today_record = self.cursor.execute("""
                                                SELECT start_day, start_dinner, end_dinner, end_day, day_len, dinner_len, id
                                                FROM report
                                                WHERE   id_user = {id_user} AND
                                                        start_day >= '{day} 00:00' AND
                                                        start_day <= '{day} 23:59' AND
                                                        status IS NOT 'deleted'
                                        """.format(
                                                id_user = self.user.my_id,
                                                day = self.today.format_db
                                        )).fetchone()

                                        if not today_record:
                                                # Если записи нету, то активируем кнопку старта и устанавливаем режим WorkDay
                                                self.btn_start.setEnabled(True)
                                                self.btn_start.setStyleSheet(self.styleSheet.inverse_btn)
                                                self.wd_mode = 'not_started'
                                        
                                        else:
                                                self.restart_day(today_record)
                                
                                else:
                                        # Если прав нема:
                                        # self.tabWidget.setTabVisible(self.tabWidget.indexOf(self.workday), False)
                                        self.tabWidget.removeTab(self.tabWidget.indexOf(self.workday))

                                if self.user.my_root_hidden_software_r or self.user.my_root_hidden_software_rw:
                                        # Активация вкладки, где находится пиратское ПО

                                        # Проверяем есть ли доступы к 1 и 2 вкладке, если нету, то отключаем их отображение
                                        if not self.user.my_root_report and not self.user.my_root_admin:
                                                # Если нету прав на работу с админкой и отчетами, отключаем вкладку с отчетами и добавляем только 1 пользователя (того, кто запустил)
                                                # self.tabWidget.setTabVisible(self.tabWidget.indexOf(self.reports), False)
                                                self.tabWidget.removeTab(self.tabWidget.indexOf(self.reports))
                                                self.combobox_username.addItem( self.user.my_username )
                                                self.combobox_username.setEnabled(False)

                                        if not self.user.my_root_admin:
                                                # Дополнительно, если нету прав администратора выключаем вкладку с управлением пользователями
                                                # self.tabWidget.setTabVisible(self.tabWidget.indexOf(self.users), False)
                                                self.tabWidget.removeTab(self.tabWidget.indexOf(self.users))

                                        # Активируем кнопку добавления ПК и выгрузки отчета для тех, кому это разрешено
                                        if self.user.my_root_hidden_software_rw:
                                                self.btn_generateReportHiddenSoft.setEnabled(True)
                                                self.btn_generateReportHiddenSoft.setStyleSheet(self.styleSheet.btn)

                                                self.btn_addHiddenPC.setEnabled(True)
                                                self.btn_addHiddenPC.setStyleSheet(self.styleSheet.btn)

                                                self.btn_addHiddenPC.clicked.connect(self.btn_addHiddenPC_clicked)

                                else:
                                        # если нету прав на чтение/редактирование данных о пиратском софте
                                        # self.tabWidget.setTabVisible(self.tabWidget.indexOf(self.hidden_software), False)
                                        self.tabWidget.removeTab(self.tabWidget.indexOf(self.hidden_software))

                                # Отключаем вкладки, если в БД их функционал выключен

                                if not self.users_isEnabled: self.tabWidget.removeTab(self.tabWidget.indexOf(self.users))
                                if not self.report_isEnabled: self.tabWidget.removeTab(self.tabWidget.indexOf(self.reports))
                                if not self.workDay_isEnabled: self.tabWidget.removeTab(self.tabWidget.indexOf(self.workday))
                                if not self.hiddenSoft_isEnabled: self.tabWidget.removeTab(self.tabWidget.indexOf(self.hidden_software))

                        else:
                                self.setup_error(self)

                else:
                        self.setup_error(self)

        def generateReportAboutHiddenSoftware(self): # Генерация отчета по скрытому ПО
                """Генерация отчета по скрытому ПО"""
                path_to_save = QtWidgets.QFileDialog.getExistingDirectoryUrl().url()[8::]
                path_to_save = os.path.join(path_to_save, 'Отчет по скрытому ПО на ПК.xlsx')

                self.user.insert_log(
                        id_user = self.user.my_id,
                        time = self.user.time_to_db(datetime.datetime.now()),
                        param = 'Uploading the report about PC with non licensing software'
                )

                report = hiddenSoft_report.hiddenSoftReport(self.cursor)
                report.generate(path_to_save)

        def btn_addHiddenPC_clicked(self): # Отработка нажатия кнопки 'Добавить ПК' в Пиратском ПО
                self.clear_fieldInfoAboutPC()
                self.label_title_PCInfo.setText('Добавление ПК')

                self.label_AddPC_namePC.setHidden(False)
                self.lineEdit_AddPC_namePC.setHidden(False)
                self.lineEdit_AddPC_namePC.setText('')
                self.lineEdit_AddPC_namePC.setStyleSheet(self.styleSheet.input_text)

                self.label_AddressPC.setHidden(False)
                self.lineEdit_AddressPC.setHidden(False)
                self.lineEdit_AddressPC.setText('')
                self.lineEdit_AddressPC.setStyleSheet(self.styleSheet.input_text)
                
                self.label_PCusername.setHidden(False)
                self.lineEdit_PCusername.setHidden(False)
                self.lineEdit_PCusername.setText('')
                self.lineEdit_PCusername.setStyleSheet(self.styleSheet.input_text)

                self.label_PCcase.setHidden(False)
                self.lineEdit_PCcase.setHidden(False)
                self.lineEdit_PCcase.setText('')
                self.lineEdit_PCcase.setStyleSheet(self.styleSheet.input_text)

                self.label_PCsoft.setHidden(False)
                self.lineEdit_PCsoft.setHidden(False)
                self.lineEdit_PCsoft.setText('')
                self.lineEdit_PCsoft.setStyleSheet(self.styleSheet.input_text)

                self.btn_savePC.setHidden(False)
                self.btn_cancelPC.setHidden(False)

                self.label_PCdelete_bg.setHidden(True)
                self.lineEdit_PCdelete.setHidden(True)
                self.btn_deletePC.setHidden(True)

                self.btn_save_PC_status = 'adding'

        def lineEdit_AddPC_changed(self): # Изменено имя ПК
                
                self.label_errors.setText('')
                if self.lineEdit_AddPC_namePC.text():
                        self.lineEdit_AddPC_namePC.setStyleSheet(self.styleSheet.input_text_full)

                        if re.findall(r'[А-я]', self.lineEdit_AddPC_namePC.text()):
                                self.lineEdit_AddPC_namePC.setStyleSheet(self.styleSheet.input_text_full_error)
                                self.label_errors.setText('Имя ПК содержит русский язык')

                elif not self.lineEdit_AddPC_namePC.text():
                        self.lineEdit_AddPC_namePC.setStyleSheet(self.styleSheet.input_text)

        def btn_find_clicked(self): # Отработка нажатия кнопки 'Поиск' в Пиратском ПО
                """ Отработка нажатия кнопки 'Поиск' в Пиратском ПО """

                pc_list = self.cursor.execute("""
                        SELECT pc_name, id FROM hidden_software
                        WHERE LOWER(pc_name) LIKE '%{pc_name}%' AND NOT isDeleted
                        LIMIT 10
                """.format(
                        pc_name = self.lineEdit_find.text().lower()
                )).fetchall()

                # Очищаем имеющийся список
                self.clear_pcList()

                if not pc_list:
                        self.label_title_findResults.setText('Ничего не найдено')
                        return
                
                self.label_title_findResults.setText('Результаты поиска')
                start_y = 100

                for pc in pc_list:
                        self.btn_pc = QtWidgets.QPushButton(self.hidden_software)
                        self.btn_pc.setGeometry(QtCore.QRect(20, start_y, 130, 25))
                        self.btn_pc.setFont(self.font)
                        self.btn_pc.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
                        self.btn_pc.setObjectName(str(pc[1]))
                        self.btn_pc.setText(str(pc[0]))
                        self.btn_pc.setStyleSheet(self.styleSheet.inverse_btn)
                        self.btn_pc.clicked.connect(lambda ch, btn = self.btn_pc: self.show_PC_with_hidden_software(btn))
                        self.btn_pc.show()
                        self.temp_pc_list.append(self.btn_pc)
                        start_y += 30

        def clear_pcList(self): # Для очистки кнопок в поиске компов
                """ Для очистки кнопок в поиске компов """
                self.label_title_PCInfo.setText('Выберите ПК')
                self.label_title_findResults.setText('Введите запрос')
                self.clear_fieldInfoAboutPC()
                while self.temp_pc_list:
                        for i in self.temp_pc_list:
                                i.deleteLater()
                                self.temp_pc_list.remove(i)

        def clear_fieldInfoAboutPC(self): # Очистка поля с информацией об показанном ПК
                """ Очистка поля с информацией об показанном ПК """
                self.showedPC_id = 0
                self.label_title_PCInfo.setText('Выберите ПК')
                self.label_whenPCadd.setText('')
                self.label_whoAddPC.setText('')
                self.label_whoAddPC_username.setText('')
                self.label_whenPCadd_time.setText('')
                self.lineEdit_AddressPC.setHidden(True)
                self.lineEdit_AddressPC.setText('')
                self.label_AddressPC.setHidden(True)

                self.label_PCusername.setHidden(True)
                self.lineEdit_PCusername.setHidden(True)
                self.lineEdit_PCusername.setText('')

                self.label_PCcase.setHidden(True)
                self.lineEdit_PCcase.setHidden(True)
                self.lineEdit_PCcase.setText('')

                self.label_PCsoft.setHidden(True)
                self.lineEdit_PCsoft.setHidden(True)
                self.lineEdit_PCsoft.setText('')

                self.btn_savePC.setHidden(True)
                self.btn_cancelPC.setHidden(True)

                self.label_PCdelete_bg.setHidden(True)
                self.lineEdit_PCdelete.setHidden(True)
                self.lineEdit_PCdelete.setText('')
                self.btn_deletePC.setHidden(True)

                self.lineEdit_AddPC_namePC.setHidden(True)
                self.lineEdit_AddPC_namePC.setText('')
                self.label_AddPC_namePC.setHidden(True)
                
        def show_PC_with_hidden_software(self, pc): # Показать информацию по ПК, который был выбран
                """ Показать информацию по ПК, который был выбран """
                self.btn_save_PC_status = 'changing'
                self.clear_fieldInfoAboutPC()
                pc_id = pc.objectName()
                self.showedPC_id = pc_id
                pc_info = self.cursor.execute("""
                        SELECT users.username, h.pc_name, h.address, h.software, h.user_fullname, h.case_number, h.created FROM hidden_software h
                        JOIN users ON users.id = h.id_user
                        WHERE h.id = {pc_id}
                        LIMIT 1
                """.format(
                        pc_id = pc_id
                )).fetchone()

                if not self.user.testMode:
                        self.user.insert_log(
                                id_user = self.user.my_id,
                                time = self.user.time_to_db(datetime.datetime.now()),
                                param = 'Show PC info ' + pc_info[1]
                        )

                pc_AddDate = pc_info[6].split(' ')[0].split('-')[2] + '.' + pc_info[6].split(' ')[0].split('-')[1] + '.' + pc_info[6].split(' ')[0].split('-')[0]
                pc_AddTime = pc_info[6].split(' ')[1]

                self.label_title_PCInfo.setText('Информация об ' + pc_info[1])

                self.label_whenPCadd.setText('Время добавления:')
                self.label_whenPCadd_time.setText(' '.join([pc_AddDate, pc_AddTime]))

                self.label_whoAddPC.setText('Добавил:')
                self.label_whoAddPC_username.setText(pc_info[0])

                self.label_AddressPC.setHidden(False)
                self.lineEdit_AddressPC.setHidden(False)
                self.lineEdit_AddressPC.setText(pc_info[2])
                
                self.label_PCusername.setHidden(False)
                self.lineEdit_PCusername.setHidden(False)
                self.lineEdit_PCusername.setText(pc_info[4])

                self.label_PCcase.setHidden(False)
                self.lineEdit_PCcase.setHidden(False)
                self.lineEdit_PCcase.setText(pc_info[5])

                self.label_PCsoft.setHidden(False)
                self.lineEdit_PCsoft.setHidden(False)
                self.lineEdit_PCsoft.setText(pc_info[3])

                self.btn_savePC.setHidden(False)
                self.btn_savePC.setEnabled(True)
                self.btn_savePC.setStyleSheet(self.styleSheet.inverse_btn)
                self.btn_cancelPC.setHidden(False)
                self.btn_cancelPC.setEnabled(True)
                self.btn_cancelPC.setStyleSheet(self.styleSheet.inverse_btn)

                self.label_PCdelete_bg.setHidden(False)
                self.lineEdit_PCdelete.setHidden(False)
                self.btn_deletePC.setHidden(False)

                # Если у сотрудника имеются права только на чтение
                if self.user.my_root_hidden_software_r:
                        self.label_PCdelete_bg.setHidden(True)
                        self.lineEdit_PCdelete.setHidden(True)
                        self.btn_deletePC.setHidden(True)

                        self.btn_savePC.setEnabled(False)
                        self.btn_savePC.setStyleSheet(self.styleSheet.inverse_btn_off)

                        self.btn_cancelPC.setEnabled(False)
                        self.btn_cancelPC.setStyleSheet(self.styleSheet.inverse_btn_off)
        
        def btn_savePC_clicked(self): # Обработка нажатия на кнопку "сохранить ПК"
                address = self.lineEdit_AddressPC.text()
                username = self.lineEdit_PCusername.text()
                case_number = self.lineEdit_PCcase.text()
                software = self.lineEdit_PCsoft.text()
                pc_name = self.lineEdit_AddPC_namePC.text()

                if self.btn_save_PC_status == 'adding':

                        if not address: self.lineEdit_AddressPC.setStyleSheet(self.styleSheet.input_text_error)
                        if not username: self.lineEdit_PCusername.setStyleSheet(self.styleSheet.input_text_error)
                        if not case_number: self.lineEdit_PCcase.setStyleSheet(self.styleSheet.input_text_error)
                        if not software: self.lineEdit_PCsoft.setStyleSheet(self.styleSheet.input_text_error)
                        if not pc_name: self.lineEdit_AddPC_namePC.setStyleSheet(self.styleSheet.input_text_error)

                        # Нельзя добавить ПК в базу пока одно из полей не заполнено
                        if not address or not username or not case_number or not software or not pc_name: return

                        # Ищем ПК с таким же именем
                        isPCexists = self.cursor.execute(f'SELECT id FROM hidden_software WHERE pc_name = UPPER("{pc_name}") LIMIT 1').fetchone()
                        if isPCexists: 
                                self.lineEdit_AddPC_namePC.setStyleSheet(self.styleSheet.input_text_full_error)
                                self.label_errors.setText('ПК с таким именем уже существует')
                                return

                        self.cursor.execute(f"""
                                INSERT INTO hidden_software(id_user, pc_name, address, software, user_fullname, case_number) VALUES
                                ('{self.user.my_id}', UPPER('{pc_name}'), '{address}', '{software}', '{username}', '{case_number}')                        
                        """)
                        self.connect.commit()
                        record_id = self.cursor.execute(f'SELECT id FROM hidden_software WHERE pc_name = UPPER("{pc_name}") LIMIT 1').fetchone()[0]
                        self.user.insert_log(
                                id_user=self.user.my_id,
                                time=self.user.time_to_db(datetime.datetime.now()),
                                param='Add PC with crack software ' + str(record_id)
                        )
                        self.clear_fieldInfoAboutPC()
                        return

                old_data = self.cursor.execute(f'SELECT address, software, user_fullname, case_number FROM hidden_software WHERE id = {self.showedPC_id} LIMIT 1').fetchone()
                new_data = (address, software, username, case_number)

                self.user.insert_log(
                        id_user=self.user.my_id,
                        time=self.user.time_to_db(datetime.datetime.now()),
                        param='Changed PC info ' + str(self.showedPC_id),
                        last_value=str(old_data),
                        new_value=str(new_data)
                )

                self.cursor.execute("""
                        UPDATE hidden_software
                        SET address = '{address}', software = '{software}', user_fullname = '{user_fullname}', case_number = '{case_number}'
                        WHERE id = {pc_id}
                """.format(
                        address = address,
                        software = software,
                        user_fullname = username,
                        case_number = case_number,
                        pc_id = self.showedPC_id
                ))
                self.connect.commit()
                self.clear_fieldInfoAboutPC()

        def btn_deletePC_clicked(self): # Обработка удаления записи о скрытом ПО на ПК

                self.user.insert_log(
                        id_user=self.user.my_id,
                        time=self.user.time_to_db(datetime.datetime.now()),
                        param='Delete PC ' + str(self.showedPC_id)
                )

                delete_reason = self.lineEdit_PCdelete.text()
                self.cursor.execute(f"""
                        UPDATE hidden_software
                        SET isDeleted = 1, delete_reason = '{delete_reason}', delete_time = datetime('now', '+5 hours')
                        WHERE id = {self.showedPC_id}
                """)
                self.connect.commit()
                self.btn_find_clicked()
                self.clear_fieldInfoAboutPC()

        def lineEdit_PCdelete_changed(self): # Отработка события при измении поля с удалением ПК
                
                if self.lineEdit_PCdelete.text():
                        self.lineEdit_PCdelete.setStyleSheet(self.styleSheet.input_text_full)
                        self.btn_deletePC.setEnabled(True)
                        self.btn_deletePC.setStyleSheet(self.styleSheet.inverse_btn)
                elif not self.lineEdit_PCdelete.text():
                        self.lineEdit_PCdelete.setStyleSheet(self.styleSheet.input_text)
                        self.btn_deletePC.setEnabled(False)
                        self.btn_deletePC.setStyleSheet(self.styleSheet.inverse_btn_off)

        def lineEdit_PCcase_changed(self): # Отработка события при измении поля с кейсом
                
                if self.lineEdit_PCcase.text():
                        self.lineEdit_PCcase.setStyleSheet(self.styleSheet.input_text_full)
                elif not self.lineEdit_PCcase.text():
                        self.lineEdit_PCcase.setStyleSheet(self.styleSheet.input_text)

        def lineEdit_PCsoft_changed(self): # Отработка события при измении поля с ПО
                """ Отработка события при измении поля с ПО """

                if self.lineEdit_PCsoft.text():
                        self.lineEdit_PCsoft.setStyleSheet(self.styleSheet.input_text_full)
                elif not self.lineEdit_PCsoft.text():
                        self.lineEdit_PCsoft.setStyleSheet(self.styleSheet.input_text)

        def lineEdit_PCusername_changed(self): # Отработка события при измении поля с владельцем ПК
                
                if self.lineEdit_PCusername.text():
                        self.lineEdit_PCusername.setStyleSheet(self.styleSheet.input_text_full)
                elif not self.lineEdit_PCusername.text():
                        self.lineEdit_PCusername.setStyleSheet(self.styleSheet.input_text)

        def lineEdit_AddressPC_changed(self): # Отработка события при измении поля с адресом ПК
                
                if self.lineEdit_AddressPC.text():
                        self.lineEdit_AddressPC.setStyleSheet(self.styleSheet.input_text_full)
                elif not self.lineEdit_AddressPC.text():
                        self.lineEdit_AddressPC.setStyleSheet(self.styleSheet.input_text)

        def lineEdit_find_changed(self): # Отработка события при измении текста в поле поиск ПК
                """ Отработка события при измении текста в поле поиск ПК """
                
                self.clear_pcList()
                if self.lineEdit_find.text():
                        self.lineEdit_find.setStyleSheet(self.styleSheet.input_text_full)
                        self.btn_find_clicked()
                elif not self.lineEdit_find.text():
                        self.lineEdit_find.setStyleSheet(self.styleSheet.input_text)

        def check_last_record(self): # Проверка, была ли закрыта последняя запись в WorkDay
                last_record = self.cursor.execute("""
                        SELECT MAX(id), start_day, start_dinner, end_dinner, end_day FROM report
                        WHERE id_user = '{my_id}' AND start_day < '{day} 00:00' AND status IS NOT 'deleted'
                """.format(
                        my_id = self.user.my_id,
                        day = report.date_datetime('today').format_db
                )).fetchone()
                if last_record[0]:
                        id_record = last_record[0]
                        start_day = last_record[1]
                        start_dinner = last_record[2]
                        end_dinner = last_record[3]
                        end_day = last_record[4]
                        if not end_day:
                                # Если последняя запись не была закрыта, то необходимо ее закрыть и установить статус "auto"
                                date = report.date_datetime(start_day.split(' ')[0])
                                start_day = report.date_datetime(start_day, mode = 'time')
                                if start_dinner:
                                        start_dinner = report.date_datetime(start_dinner, mode = 'time')
                                        if end_dinner:
                                                end_dinner = report.date_datetime(end_dinner, mode = 'time')
                                                dinner_len = (end_dinner.date - start_dinner.date).seconds // 60

                                        elif not end_dinner:
                                                dinner_len = 0

                                elif not start_dinner:
                                        dinner_len = 0
                                
                                end_day = report.date_datetime(date.format_db + ' 18:10', mode = 'time')
                                day_len = (end_day.date - start_day.date).seconds // 60

                                self.cursor.execute("""
                                        UPDATE report
                                        SET     end_day = '{end_day}',
                                                day_len = {day_len},
                                                dinner_len = {dinner_len},
                                                status = 'auto'
                                        WHERE id = '{id_record}'
                                """.format(
                                        end_day = end_day.format_db,
                                        day_len = day_len,
                                        dinner_len = dinner_len,
                                        id_record = id_record
                                ))
                                self.connect.commit()
                                
        def status_update(self): # Обновление информации о статусе других пользователей
                for user in self.users_status:
                        status = self.cursor.execute("""
                                SELECT report.start_day, report.start_dinner, report.end_dinner, report.end_day FROM report, users
                                WHERE report.id_user = users.id AND users.username = '{username}' AND report.start_day >= '{day} 00:00' AND report.start_day <= '{day} 23:59' AND report.status IS NOT 'deleted'
                        """.format(
                                username = user,
                                day = report.date_datetime('today').format_db
                        )).fetchone()
                        
                        if status:
                                start_dinner = status[1]
                                end_dinner = status[2]
                                end_day = status[3]

                                style = self.styleSheet.status_onLine

                                if end_dinner and not end_day:
                                        style = self.styleSheet.status_onLine
                                
                                elif start_dinner and not (end_dinner or end_day):
                                        style = self.styleSheet.status_dinner
                                
                                elif end_day:
                                        style = self.styleSheet.status_disabled
                        
                        else:
                                style = self.styleSheet.status_off

                        self.users_status[user].setStyleSheet(style)

        def wd_update(self): # Обновление информации об отработанном времени
                # Устанавливаем время, после которого скрипт должен считаться автоматически завершенным
                time18 = datetime.datetime(
                        year = datetime.datetime.now().year,
                        month = datetime.datetime.now().month,
                        day = datetime.datetime.now().day,
                        hour = 18,
                        minute = 10,
                        second = 0
                )
                # Проверяем, если текущее время больше времени, после которого выключается скрипт с "Автоматичским завершением",
                # то ставим автоматическое завершение и др. вещи;
                # Если все таки время НЕ больше, то просто обновляем данные в заисимости от текущего режима работы скрипта
                if datetime.datetime.now() < time18:

                        # Если рабочий день был запущен,
                        # то попросту обновляем информацию в нужном Label (info_sum)
                        if self.wd_mode == 'started':
                                day_len = (datetime.datetime.now() - self.wd_start_day.date).seconds // 60
                                self.info_sum.setText( self.minute_to_format(day_len) )

                        # Если в данный момент мы обедаем, то необходимо обновять информацию в Label (info_dinner), который показывает сколько ты обедаешь
                        elif self.wd_mode == 'dinner_started':
                                dinner_len = (datetime.datetime.now() - self.wd_start_dinner.date).seconds // 60
                                self.info_dinner.setText( self.minute_to_format(dinner_len) )

                        # Если обед уже был завершен, то необходимо обновлять информацию в Label (info_sum) учитывая обеденное время (т.е. его просто надо вычитать)
                        elif self.wd_mode == 'dinner_ended':
                                dinner_len = (self.wd_end_dinner.date - self.wd_start_dinner.date).seconds // 60
                                day_len = ((datetime.datetime.now() - self.wd_start_day.date).seconds // 60) - dinner_len
                                self.info_sum.setText( self.minute_to_format(day_len) )
                
                else:
                        # Тут расписаны действия при автоматическом завершении

                        self.updater.running = False            # Оставливаем обновление

                        # Отключаем кнопки
                        self.btn_dinner.setEnabled(False)
                        self.btn_dinner.setStyleSheet(self.styleSheet.inverse_btn_off)

                        self.btn_end.setEnabled(False)
                        self.btn_end.setStyleSheet(self.styleSheet.inverse_btn_off)

                        # Говорим что было автоматическое завершение
                        self.label_errors.setText('Автоматическое завершение')
                        self.status_update()

                        self.wd_end_day = report.date_datetime(datetime.datetime.now(), 'class')
                        self.info_end.setText(self.wd_end_day.format_standart)
                        # Определяем сколько в итоге отработал сотрудник
                        self.dinner_len = 0
                        if self.wd_mode == 'dinner_ended':
                                self.dinner_len = (self.wd_end_dinner.date - self.wd_start_dinner.date).seconds // 60
                                self.day_len = (self.wd_end_day.date - self.wd_start_day.date).seconds // 60 - self.dinner_len
                        
                        elif self.wd_mode in ['started', 'dinner_started']:
                                self.day_len = (self.wd_end_day.date - self.wd_start_day.date).seconds // 60

                        if not self.user.testMode:
                                self.cursor.execute("""
                                        UPDATE report
                                        SET     end_day = '{end_day}',
                                                day_len = '{day_len}',
                                                dinner_len = '{dinner_len}',
                                                status = 'auto'
                                        WHERE id = {id_record}
                                """.format(
                                        id_record = self.wd_id_record,
                                        end_day = self.wd_end_day.format_db,
                                        day_len = self.day_len,
                                        dinner_len = self.dinner_len
                                ))
                                self.connect.commit()
                        
                        else:
                                print('[TEST MODE] Автоматическое завершение работы в ' + str(self.wd_end_day.format_db))

        def minute_to_format(self, minute: int): # Перевод минут в формат HH:MM
                minutes = minute % 60
                if minutes < 10:
                        minutes = '0' + str(minutes)
                
                hour = minute // 60
                if hour < 10:
                        hour = '0' + str(hour)
                
                return str(hour) + ':' + str(minutes)

        def restart_day(self, today_record): # Ф-я для проверки была ли ранее запись за сегодня
                start_day = today_record[0]
                start_dinner =  today_record[1]
                end_dinner =  today_record[2]
                end_day =  today_record[3]
                day_len =  today_record[4]
                dinner_len = today_record[5]
                self.wd_id_record = today_record[6]

                if day_len or day_len == 0:
                        # Если поле day_len не пустое, то значит что день был завершен
                        self.btn_start.setEnabled(False)
                        self.btn_start.setStyleSheet(self.styleSheet.inverse_btn_off)

                        self.btn_dinner.setEnabled(False)
                        self.btn_dinner.setStyleSheet(self.styleSheet.inverse_btn_off)

                        self.btn_end.setEnabled(False)
                        self.btn_end.setStyleSheet(self.styleSheet.inverse_btn_off)

                        day = report.date_datetime(start_day.split(' ')[0]).format_standart
                        self.info_start.setText(day + ' ' + start_day.split(' ')[1])

                        self.info_dinner.setText( self.minute_to_format(dinner_len) )

                        self.info_end.setText(day + ' ' + end_day.split(' ')[1])

                        self.info_sum.setText( self.minute_to_format(day_len) )
                        self.label_errors.setText('Вы уже работали.\nНе возможно запустить WorkDay еще раз')
                        self.wd_mode = 'ended'

                else:
                        if end_dinner:
                                # Если закончен обед
                                self.wd_mode = 'dinner_ended'

                                self.btn_start.setEnabled(False)
                                self.btn_start.setStyleSheet(self.styleSheet.inverse_btn_off)

                                self.btn_dinner.setEnabled(False)
                                self.btn_dinner.setStyleSheet(self.styleSheet.inverse_btn_off)
                                self.btn_dinner.setText('Пришел с обеда')

                                self.btn_end.setEnabled(True)
                                self.btn_end.setStyleSheet(self.styleSheet.inverse_btn)

                                self.isDinnerEnded = True

                                day = report.date_datetime(start_day.split(' ')[0]).format_standart
                                self.info_start.setText(day + ' ' + start_day.split(' ')[1])

                                self.wd_start_day = report.date_datetime(start_day, mode = 'time')
                                self.wd_end_dinner = report.date_datetime(end_dinner, mode = 'time')
                                self.wd_start_dinner = report.date_datetime(start_dinner, mode = 'time')

                                delta = (self.wd_end_dinner.date - self.wd_start_dinner.date).seconds // 60
                                self.info_dinner.setText( self.minute_to_format(delta) )
                        
                        elif start_dinner and not end_dinner:
                                # Если обед начался, но не закончен
                                self.wd_mode = 'dinner_started'
                                self.btn_start.setEnabled(False)
                                self.btn_start.setStyleSheet(self.styleSheet.inverse_btn_off)

                                self.btn_dinner.setEnabled(True)
                                self.btn_dinner.setStyleSheet(self.styleSheet.inverse_btn)
                                self.btn_dinner.setText('Пришел с обеда')

                                self.btn_end.setEnabled(False)
                                self.btn_end.setStyleSheet(self.styleSheet.inverse_btn_off)

                                self.isDinnerEnded = False

                                self.wd_start_day = report.date_datetime(start_day, mode = 'time')
                                self.wd_start_dinner = report.date_datetime(start_dinner, mode = 'time')

                                day_len = (datetime.datetime.now() - self.wd_start_day.date).seconds // 60
                                self.info_sum.setText( self.minute_to_format( day_len ) )
                                self.info_start.setText(self.wd_start_day.format_standart)

                        elif not start_dinner and not end_dinner:
                                # Если обед не начинался
                                self.wd_mode = 'started'
                                self.wd_start_day = report.date_datetime(start_day, mode = 'time')

                                self.info_start.setText(self.wd_start_day.format_standart)

                                self.btn_dinner.setEnabled(True)
                                self.btn_dinner.setStyleSheet(self.styleSheet.inverse_btn)

                                self.btn_end.setEnabled(True)
                                self.btn_end.setStyleSheet(self.styleSheet.inverse_btn)

                        self.updater.start()
                        print('Функции не продуманы =(')

        def start_day(self):
                self.wd_mode = 'started'
                self.btn_start.setEnabled(False)
                self.btn_start.setStyleSheet(self.styleSheet.inverse_btn_off)

                self.btn_dinner.setEnabled(True)
                self.btn_dinner.setStyleSheet(self.styleSheet.inverse_btn)

                self.btn_end.setEnabled(True)
                self.btn_end.setStyleSheet(self.styleSheet.inverse_btn)

                self.wd_start_day = report.date_datetime(datetime.datetime.now(), 'class')
                self.info_start.setText(self.wd_start_day.format_standart)

                self.updater.start()

                if not self.user.testMode:
                        print('Тестовый режим не был включен, выполнена запись в БД')
                        try:
                                self.cursor.execute("""
                                        INSERT INTO report(id_user, start_day)
                                        VALUES(
                                                {id_user}, '{start_day}'
                                        )
                                """.format(
                                        id_user = self.user.my_id,
                                        start_day = self.wd_start_day.format_db
                                ))
                                self.connect.commit()

                                self.wd_id_record = self.cursor.execute("""
                                        SELECT id FROM report
                                        WHERE   start_day >= '{day} 00:00' AND 
                                                start_day <= '{day} 23:59' AND 
                                                id_user = {id_user} AND
                                                status IS NOT 'deleted'
                                """.format(
                                        id_user = self.user.my_id,
                                        day = self.wd_start_day.format_db.split(' ')[0]
                                )).fetchone()[0]
                                self.status_update()

                        except Exception as error:
                                self.user.error( str(error) )

                                # Т.к. возникла ошибка, говорим пользователю что произошла ошибка, 
                                # и до кучи отключаем кнопки, чтобы пользователь не смог дальше работать с программой
                                self.label_errors.setText('Произошла ошибка при записи в БД')

                                self.btn_dinner.setEnabled(False)
                                self.btn_dinner.setStyleSheet(self.styleSheet.inverse_btn_off)

                                self.btn_end.setEnabled(False)
                                self.btn_end.setStyleSheet(self.styleSheet.inverse_btn_off)
                
                else:
                        print('[TEST MODE] Начат день: ' + self.wd_start_day.format_db)

        def dinner(self):
                if self.wd_mode == 'started':
                        self.btn_dinner.setText('Пришел с обеда')
                        self.wd_mode = 'dinner_started'
                        self.wd_start_dinner = report.date_datetime(datetime.datetime.now(), 'class')
                        self.btn_end.setEnabled(False)
                        self.btn_end.setStyleSheet(self.styleSheet.inverse_btn_off)
                        self.info_dinner.setText('00:00')

                        if not self.user.testMode:
                                print('Тестовый режим не был включен, выполнена запись в БД')
                                try:
                                        self.cursor.execute("""
                                                UPDATE report
                                                SET start_dinner = '{start_dinner}'
                                                WHERE id = {id_record}
                                        """.format(
                                                start_dinner = self.wd_start_dinner.format_db,
                                                id_record = self.wd_id_record
                                        ))
                                        self.connect.commit()
                                        self.status_update()

                                except Exception as error:
                                        self.user.error( str(error) )

                                        # Т.к. возникла ошибка, говорим пользователю что произошла ошибка, 
                                        # и до кучи отключаем кнопки, чтобы пользователь не смог дальше работать с программой
                                        self.label_errors.setText('Произошла ошибка при записи в БД')

                                        self.btn_dinner.setEnabled(False)
                                        self.btn_dinner.setStyleSheet(self.styleSheet.inverse_btn_off)

                                        self.btn_end.setEnabled(False)
                                        self.btn_end.setStyleSheet(self.styleSheet.inverse_btn_off)
                        
                        else:
                                print('[TEST MODE] Начат обед: ' + self.wd_start_dinner.format_db)

                elif self.wd_mode == 'dinner_started':
                        self.btn_dinner.setEnabled(False)
                        self.btn_dinner.setStyleSheet(self.styleSheet.inverse_btn_off)
                        self.wd_mode = 'dinner_ended'
                        self.wd_end_dinner = report.date_datetime(datetime.datetime.now(), 'class')
                        self.btn_end.setEnabled(True)
                        self.btn_end.setStyleSheet(self.styleSheet.inverse_btn)

                        if not self.user.testMode:
                                print('Тестовый режим не был включен, выполнена запись в БД')
                                try:
                                        self.cursor.execute("""
                                                UPDATE report
                                                SET end_dinner = '{end_dinner}'
                                                WHERE id = {id_record}
                                        """.format(
                                                end_dinner = self.wd_end_dinner.format_db,
                                                id_record = self.wd_id_record
                                        ))
                                        self.connect.commit()
                                        self.status_update()

                                except Exception as error:
                                        self.user.error( str(error) )

                                        # Т.к. возникла ошибка, говорим пользователю что произошла ошибка, 
                                        # и до кучи отключаем кнопки, чтобы пользователь не смог дальше работать с программой
                                        self.label_errors.setText('Произошла ошибка при записи в БД')

                                        self.btn_dinner.setEnabled(False)
                                        self.btn_dinner.setStyleSheet(self.styleSheet.inverse_btn_off)

                                        self.btn_end.setEnabled(False)
                                        self.btn_end.setStyleSheet(self.styleSheet.inverse_btn_off)
                        
                        else:
                                print('[TEST MODE] Обед закончен: ' + self.wd_end_dinner.format_db)

        def end_day(self):

                # Проверяем чтобы версия программы не изменилась при закрытии программы
                bd_version = self.cursor.execute("""
                        SELECT value FROM options
                        WHERE name = 'app_version'
                """).fetchone()

                if bd_version[0] != APP_VERSION:
                        self.label_errors.setText('Перед закрытием обнови WorkDay\nСмена не закрыта')
                        return

                self.wd_mode = 'ended'                  # Устанавливаем режим WorkDay
                self.updater.running = False            # Оставливаем обновление

                self.btn_dinner.setEnabled(False)
                self.btn_dinner.setStyleSheet(self.styleSheet.inverse_btn_off)

                self.btn_end.setEnabled(False)
                self.btn_end.setStyleSheet(self.styleSheet.inverse_btn_off)

                self.wd_end_day = report.date_datetime(datetime.datetime.now(), 'class')
                self.info_end.setText(self.wd_end_day.format_standart)

                if self.isDinnerEnded:
                        dinner_len = (self.wd_end_dinner.date - self.wd_start_dinner.date).seconds // 60
                
                else:
                        dinner_len = 0

                day_len = (self.wd_end_day.date - self.wd_start_day.date).seconds // 60 - dinner_len

                # Далее начинается костыль. 
                # К сожалению без него может быть ошибка в учете времени (обед может проставиться 0, даже если он был например минут 30)
                today = self.cursor.execute("""
                        SELECT start_day, start_dinner, end_dinner FROM report
                        WHERE id = {id_record}
                """.format(
                        id_record = self.wd_id_record
                )).fetchone()

                start_day = report.date_datetime(today[0], mode = 'time')

                if today[1] and today[2]:
                        start_dinner = report.date_datetime(today[1], mode = 'time')
                        end_dinner = report.date_datetime(today[2], mode = 'time')
                        dinner_len = (end_dinner.date - start_dinner.date).seconds // 60

                else:
                        start_dinner, end_dinner = 0, 0
                        dinner_len = 0

                end_day = self.wd_end_day

                day_len = (end_day.date - start_day.date).seconds // 60 - dinner_len
                # Окончание костыля

                if not self.user.testMode:
                        print('Тестовый режим не был включен, выполнена запись в БД')
                        try:
                                self.cursor.execute("""
                                        UPDATE report
                                        SET     end_day = '{end_day}',
                                                day_len = '{day_len}',
                                                dinner_len = '{dinner_len}'
                                        WHERE id = {id_record}
                                """.format(
                                        end_day = end_day.format_db,
                                        day_len = day_len,
                                        dinner_len = dinner_len,
                                        id_record = self.wd_id_record
                                ))
                                self.connect.commit()
                                self.status_update()

                        except Exception as error:
                                self.user.error( str(error) )

                                # Т.к. возникла ошибка, говорим пользователю что произошла ошибка, 
                                # и до кучи отключаем кнопки, чтобы пользователь не смог дальше работать с программой
                                self.label_errors.setText('Произошла ошибка при записи в БД')

                                self.btn_end.setEnabled(False)
                                self.btn_end.setStyleSheet(self.styleSheet.inverse_btn_off)
                        
                else:
                        print('[TEST MODE] Работа окончена: ' + self.wd_end_day.format_db)
                        print('[TEST MODE] Время работы: ' + self.minute_to_format(day_len))
                        print('[TEST MODE] Время обеда: ' + self.minute_to_format(dinner_len))

        def delete_record(self):
                reason = self.lineEdit_delete_reason.text()
                id_record = self.cursor.execute("""
                        SELECT id FROM report
                        WHERE start_day >= "{date} 00:00" AND start_day <= "{date} 23:59" AND id_user = {id_user}
                """.format(
                        date = report.date_datetime(self.lineEdit_edit_date.text()).format_db,
                        id_user = self.selected_user_id
                )).fetchone()[0]
                self.user.delete_report(id_record, reason)
                self.show_report(page = self.page)
                self.show_edit_panel('clear')
                self.lineEdit_delete_reason.setText('')

        def genDefaultReport(self, close: bool=False): # Генерация стандартногго отчета

                path_to_save = QtWidgets.QFileDialog.getExistingDirectoryUrl().url()[8::]
                if path_to_save:
                        report.generate(self.cursor, self.lineEdit_startdate.text(), self.lineEdit_enddate.text(), path_to_save)

                if close:
                        self.genReportWindow.close()
                
        def genSpecialReport(self): # Генерация специального отчета отчета
                ...

        def generate_report(self): # Генерация отчета по отработке

                date_start      = int(self.lineEdit_startdate.text()[3:5]), int(self.lineEdit_startdate.text()[6:])
                date_end        = int(self.lineEdit_enddate.text()[3:5]), int(self.lineEdit_startdate.text()[6:])

                isDateInOneMonth = date_start == date_end # Находятся ли дни в рамках одного месяца

                # Проверяем уровень доступа человека, который выгружает отчет. Если есть доступ до специального отчета, то выводим окно с выбором отчета
                if self.user.my_root_generalReport:
                        self.genReportWindow = Ui_genReportForm()
                        self.genReportWindow.show()
                        self.genReportWindow.btn_default_report.setStyleSheet(self.styleSheet.btn)
                        self.genReportWindow.btn_special_report.setStyleSheet(self.styleSheet.btn)
                        self.genReportWindow.label.setStyleSheet(self.styleSheet.label_inverse)

                        # Если период в разных месяцах, то блокируем генерацию отчета. Такой отчет может подаваться только в рамках одного месяца
                        if not isDateInOneMonth:
                                self.genReportWindow.label.setText('Период должен быть в одном месяце')
                                self.genReportWindow.btn_special_report.setEnabled(False)
                                self.genReportWindow.btn_special_report.setStyleSheet(self.styleSheet.btn_off)
                                self.genReportWindow.label.setStyleSheet(self.styleSheet.label_error)

                        self.genReportWindow.btn_default_report.clicked.connect(lambda ch: self.genDefaultReport(close = True))
                        self.genReportWindow.btn_special_report.clicked.connect(lambda ch: self.genSpecialReport())

                else:
                        self.genDefaultReport()

        def deleteDate_changed(self): # Изменен текст в причине удаления даты
                text = self.lineEdit_delete_reason.text()
                if text:
                        self.btn_delete_record.setEnabled(True)
                        self.lineEdit_delete_reason.setStyleSheet(self.styleSheet.input_text_full)
                else:
                        self.btn_delete_record.setEnabled(False)
                        self.lineEdit_delete_reason.setStyleSheet(self.styleSheet.input_text)

        def delete_reason_edited(self): # Изменен текст в причине удаления сотрудника
                text = self.lineEdit_deluser_reason.text()
                if text:
                        self.btn_deleteuser.setEnabled(True)
                        self.lineEdit_deluser_reason.setStyleSheet(self.styleSheet.input_text_full)
                else:
                        self.btn_deleteuser.setEnabled(False)
                        self.lineEdit_deluser_reason.setStyleSheet(self.styleSheet.input_text)

        def delete_user(self): # Если нажата кнопка "Удалить пользователя"
                # Ставим флаг "Удален" на пользователя
                self.cursor.execute("""
                        UPDATE users
                        SET     deleted = 1,
                                delete_reason = '{delete_reason}'
                        WHERE id = {id_user}
                """.format(
                        id_user = self.selected_user_id,
                        delete_reason = self.lineEdit_deluser_reason.text()
                ))
                self.connect.commit()

                # Сбрасываем права сотрудника
                self.cursor.execute("""
                        UPDATE root
                        SET     start_day = 0,
                                report = 0,
                                admin = 0,
                                inReport = 0,
                                generalReport = 0,
                                hidden_software_r = 0,
                                hidden_software_rw = 0
                        WHERE id_user = {id_user}
                """.format(
                        id_user = self.selected_user_id
                ))
                self.connect.commit()

                # Удаляем отпуска сотрудника из БД
                self.cursor.execute(f"""
                        DELETE FROM vacations
                        WHERE id_user = {self.selected_user_id}
                """)
                self.connect.commit()

                self.user.insert_log(self.user.my_id, self.user.time_to_db(datetime.datetime.now()), 'Deleted user ' + str(self.selected_user_id))
                self.lineEdit_delete_reason.setText('')
                index = self.combobox_username.currentIndex()
                self.combobox_username.removeItem(index)

        def add_record(self):
                self.show_edit_panel( mode = 'new' )

                # Прослушиваем поле с датой для того, чтобы не получилось записей с 2мя одинаковыми записями
                # + соблюдался формат даты
                self.lineEdit_edit_date.textChanged.connect(lambda ch, obj = self.lineEdit_edit_date: self.edit_date_changed(obj)) # Прослушка изменения даты в поле редактирования
                self.lineEdit_edit_date_isConnected = True

                self.lineEdit_edit_date.setEnabled(True)
                self.lineEdit_edit_date.setText('')

                self.lineEdit_edit_start_day.setText('')
                self.lineEdit_edit_end_day.setText('')
                self.lineEdit_edit_start_dinner.setText('')
                self.lineEdit_edit_end_dinner.setText('')

                self.checkbox_autostop.setEnabled(False)
                self.checkbox_autostop.setStyleSheet(self.styleSheet.checkbox_not_active)

        def timeoff_clicked(self): # Автоматическая установка стандартного времени, если стоит отгул
                if self.checkbox_timeoff.isChecked():
                        self.lineEdit_edit_start_day.setText('09:00')
                        self.lineEdit_edit_end_day.setText('18:00')
                        self.lineEdit_edit_start_dinner.setText('13:00')
                        self.lineEdit_edit_end_dinner.setText('14:00')

                        self.lineEdit_edit_start_day.setEnabled(False)
                        self.lineEdit_edit_end_day.setEnabled(False)
                        self.lineEdit_edit_start_dinner.setEnabled(False)
                        self.lineEdit_edit_end_dinner.setEnabled(False)

                elif not self.checkbox_timeoff.isChecked():
                        self.lineEdit_edit_start_day.setEnabled(True)
                        self.lineEdit_edit_end_day.setEnabled(True)
                        self.lineEdit_edit_start_dinner.setEnabled(True)
                        self.lineEdit_edit_end_dinner.setEnabled(True)
                        
        def change_page(self, mode: str):
                if mode == 'up':
                        self.page += 1
                elif mode == 'down':
                        self.page -= 1
                
                self.show_report(page = self.page)

        def edit_time_changed(self, obj):
                text = obj.text()
                if len(text) != 5:
                        if len(text) == 2 and re.match("(\d{2}):", self.old_value[obj]) is None:
                                obj.setText(text + ':')

                        self.old_value[obj] = obj.text()

                if text:
                        obj.setStyleSheet(self.styleSheet.input_datetime_full)

                else:
                        obj.setStyleSheet(self.styleSheet.input_datetime)

        def edit_date_changed(self, obj):
                text = obj.text()
                self.label_errors.setText('')

                if text:
                        # Проверка на наличия текста, для того чтобы значение, которое было введено после оставалось белым
                        # Если текст есть:
                        obj.setStyleSheet(self.styleSheet.input_datetime_full)
                
                else:
                        # Если в поле нету текста, то делаем его обратно серым
                        obj.setStyleSheet(self.styleSheet.input_datetime)

                if len(text) != 10:
                        if len(text) == 2 and re.match("(\d{2}).", self.old_value[obj]) is None:
                                obj.setText(text + '.')

                        elif len(text) == 5 and re.match("(\d{2}).(\d{2}).", self.old_value[obj]) is None:
                                obj.setText(text + '.')
                                
                        self.old_value[obj] = obj.text()

                elif len(text) == 10 and re.match("(\d{2}).(\d{2}).(\d{4})", text) is not None:
                        split = text.split('.')
                        date = split[2] + '-' + split[1] + '-' + split[0]
                        data = self.cursor.execute("""
                                SELECT id FROM report
                                WHERE start_day >= '{date} 00:00' and start_day <= '{date} 23:59' AND status IS NOT 'deleted' AND id_user = {id_user}
                        """.format(
                                date = date,
                                id_user = self.selected_user_id
                        )).fetchone()
                        if data:
                                self.label_errors.setText('Запись с данной датой уже имеется')
                                obj.setStyleSheet(self.styleSheet.input_datetime_full_error)

                                self.btn_save_edit.setEnabled(False)
                                self.btn_save_edit.setStyleSheet(self.styleSheet.inverse_btn_off)

                        else:
                                self.btn_save_edit.setEnabled(True)
                                self.btn_save_edit.setStyleSheet(self.styleSheet.inverse_btn)

        def show_edit_panel(self, mode: str): # Показать панель редактирования
                if mode in ['create', 'clear', 'new']:
                        if mode == 'create':
                                # Если была нажата кнопка "Добавить запись" или выбрана дата для редактирования

                                title = 'Редактирование записи'
                                status = True

                        elif mode == 'clear':
                                # Если необходимо очистить содержимое до стандартных значений
                                # Такое нужно при нажатии кнопок "Сохранить" или "Отмена", смене выбранного сотрудника

                                title = 'Выберите дату'
                                status = False

                        elif mode == 'new':
                                # Если нажата кнопка "Добавить запись"
                                # Устанавливается заголовок и убирается поле "Удалить запись", зачем она нам, если мы создаем запись?

                                title = 'Новая запись'
                                status = True 

                        self.label_errors.setText('')

                        self.label_edit_title.setText(title)  # Заголовок

                        self.label_edit_date.setVisible(status)                   # "Дата"
                        self.lineEdit_edit_date.setVisible(status)                # Input с датой
                        self.lineEdit_edit_date.setEnabled(status)

                        self.label_edit_worktime.setVisible(status)               # Подзаголовок "Рабочее время:"
                        self.label_edit_start_day.setVisible(status)              # Буква "с"
                        self.lineEdit_edit_start_day.setVisible(status)           # Input с началом времени
                        self.label_edit_end_day.setVisible(status)                # Буква "до"
                        self.lineEdit_edit_end_day.setVisible(status)             # Input с концом времени

                        self.label_edit_dinnertime.setVisible(status)             # Подзаголовок "Обед"
                        self.label_edit_start_dinner.setVisible(status)           # Буква "с"
                        self.lineEdit_edit_start_dinner.setVisible(status)        # Input с началом времени
                        self.label_edit_end_dinner.setVisible(status)             # Буква "до"
                        self.lineEdit_edit_end_dinner.setVisible(status)          # Input с концом времени

                        self.checkbox_autostop.setVisible(status)                 # Checkbox "Автоматическое завершение"
                        self.checkbox_timeoff.setVisible(status)                  # Checkbox "Отгул"
                        self.checkbox_timeoff.setChecked(False)

                        self.btn_save_edit.setVisible(status)                     # Кнопка "Сохранить"
                        self.btn_cancel_edit.setVisible(status)                   # Кнопка "Отменить"

                        if mode == 'new':
                                status = False
                        self.label_delete_bg.setVisible(status)                   # Фон удаления
                        self.lineEdit_delete_reason.setVisible(status)            # Input с причиной удаления
                        self.btn_delete_record.setVisible(status)                 # Кнопка "Удалить"

        def save_report(self):
                # Объвляем шаблону хранения данных, которые будут сохранены
                # Далее этот шаблон будет использоваться в регулярках для сравнения введенных данных
                time_format = "(\d{2}):(\d{2})"
                date_format = "(\d{2}).(\d{2}).(\d{4})"

                # Получаем текст, введенный в поле дату
                date = self.lineEdit_edit_date.text()
                if re.match(date_format, self.lineEdit_edit_date.text()) is not None:
                        # Если текст в поле дата соответствует шаблону time_format
                        date = date.split('.')[2] + '-' + date.split('.')[1] + '-' + date.split('.')[0]

                        day_start = self.lineEdit_edit_start_day.text()
                        day_end = self.lineEdit_edit_end_day.text()

                        dinner_start = self.lineEdit_edit_start_dinner.text()
                        dinner_end = self.lineEdit_edit_end_dinner.text()

                        errors = 0 # Количество ошибок. Если ошибок > 0, то не будет давать сохранить запись и будут выводиться ошибки форматирования

                        style_error = self.styleSheet.input_datetime_error
                        style_full_error = self.styleSheet.input_datetime_full_error

                        # След. 4 блока точно такие же, объясняю только на одном
                        # Провряем чтобы информация, введеная в поля для ввода времени была по шаблону
                        if re.match(time_format, day_start) is not None:
                                day_start = date + ' ' + day_start
                        elif day_start and re.match(time_format, day_start) is None: # Если информация не по шаблону, но при этом имеется какой-либо символ, то выдаем ошибку
                                errors += 1
                                self.lineEdit_edit_start_day.setStyleSheet(style_full_error)
                                self.lineEdit_edit_start_day.textChanged.connect(lambda ch, obj = self.lineEdit_edit_start_day: self.lineEdit_edit_clsRed(obj))
                        elif not day_start:
                                # Только для данного блока: не может быть такого, что в поле с началом рабочего времени нету ничего.
                                # В любом случае должно быть время начала рабочего дня
                                errors += 1
                                self.lineEdit_edit_start_day.setStyleSheet(style_error)

                        if re.match(time_format, day_end) is not None:
                                day_end = date + ' ' + day_end
                        elif day_end:
                                errors += 1
                                self.lineEdit_edit_end_day.setStyleSheet(style_full_error)
                                self.lineEdit_edit_end_day.textChanged.connect(lambda ch, obj = self.lineEdit_edit_end_day: self.lineEdit_edit_clsRed(obj))

                        if re.match(time_format, dinner_start) is not None:
                                dinner_start = date + ' ' + dinner_start
                        elif dinner_start:
                                errors += 1
                                self.lineEdit_edit_start_dinner.setStyleSheet(style_full_error)
                                self.lineEdit_edit_start_dinner.textChanged.connect(lambda ch, obj = self.lineEdit_edit_start_dinner: self.lineEdit_edit_clsRed(obj))

                        if re.match(time_format, dinner_end) is not None:
                                dinner_end = date + ' ' + dinner_end
                        elif dinner_end:
                                errors += 1
                                self.lineEdit_edit_end_dinner.setStyleSheet(style_full_error)
                                self.lineEdit_edit_end_dinner.textChanged.connect(lambda ch, obj = self.lineEdit_edit_end_dinner: self.lineEdit_edit_clsRed(obj))

                        time_off_status = self.checkbox_timeoff.isChecked()

                        if self.checkbox_autostop.isChecked():
                                # Вписать код для выделения
                                self.checkbox_autostop.setStyleSheet(self.styleSheet.checkbox_error)
                                self.label_errors.setText('С этой галочкой нельзя сохранять =)')
                                self.checkbox_autostop.clicked.connect(lambda ch, obj = self.checkbox_autostop: self.checkbox_edit_clsRed(obj))

                        else:
                                if errors:
                                        self.label_errors.setText('Неверное форматирование')

                                else:
                                        id_record = self.cursor.execute('SELECT id FROM report WHERE start_day >= "{date} 00:00" AND start_day <= "{date} 23:59" AND id_user = {id_user} AND status IS NOT "deleted"'.format(
                                                date = date,
                                                id_user = str(self.selected_user_id)
                                        )).fetchone()

                                        if id_record: # если запись есть, то это значит что было редактирование записи. Если ее нету, то значит что была создана новая)
                                                id_record = id_record[0]

                                                date_day_start = datetime.datetime(
                                                        year = int(day_start.split(' ')[0].split('-')[0]),
                                                        month = int(day_start.split(' ')[0].split('-')[1]),
                                                        day = int(day_start.split(' ')[0].split('-')[2]),
                                                        hour = int(day_start.split(' ')[1].split(':')[0]),
                                                        minute = int(day_start.split(' ')[1].split(':')[1])
                                                )

                                                if day_end:
                                                        date_day_end = datetime.datetime(
                                                                year = int(day_end.split(' ')[0].split('-')[0]),
                                                                month = int(day_end.split(' ')[0].split('-')[1]),
                                                                day = int(day_end.split(' ')[0].split('-')[2]),
                                                                hour = int(day_end.split(' ')[1].split(':')[0]),
                                                                minute = int(day_end.split(' ')[1].split(':')[1])
                                                        )

                                                        delta_day = date_day_end - date_day_start

                                                        if dinner_start and dinner_end:
                                                                date_dinner_start = datetime.datetime(
                                                                        year = int(dinner_start.split(' ')[0].split('-')[0]),
                                                                        month = int(dinner_start.split(' ')[0].split('-')[1]),
                                                                        day = int(dinner_start.split(' ')[0].split('-')[2]),
                                                                        hour = int(dinner_start.split(' ')[1].split(':')[0]),
                                                                        minute = int(dinner_start.split(' ')[1].split(':')[1])
                                                                )

                                                                date_dinner_end = datetime.datetime(
                                                                        year = int(dinner_end.split(' ')[0].split('-')[0]),
                                                                        month = int(dinner_end.split(' ')[0].split('-')[1]),
                                                                        day = int(dinner_end.split(' ')[0].split('-')[2]),
                                                                        hour = int(dinner_end.split(' ')[1].split(':')[0]),
                                                                        minute = int(dinner_end.split(' ')[1].split(':')[1])
                                                                )

                                                                delta_dinner = date_dinner_end - date_dinner_start
                                                                dinner_len = 1

                                                        else:
                                                                delta_dinner = datetime.timedelta(minutes = 0)
                                                                dinner_len = 0

                                                        day_len = (delta_day - delta_dinner).seconds / 60
                                                        if dinner_len:
                                                                dinner_len = delta_dinner.seconds / 60

                                                else:
                                                        day_len = 'Null'
                                                        dinner_len = 'Null'
                                                
                                                self.user.edit_report_time(id_record, day_start, dinner_start, dinner_end, day_end, day_len, dinner_len)
                                                print('Успешно сохранено')
                                                
                                                if re.match(date_format, self.lineEdit_startdate.text()) is not None and re.match(date_format, self.lineEdit_enddate.text()) is not None:
                                                        self.show_report(self.page)
                                                
                                                if time_off_status:
                                                        self.user.edit_report_status(id_record, 'time_off')
                                                else:
                                                        self.user.edit_report_status(id_record, 'changed')

                                                self.show_edit_panel(mode = 'clear')

                                        else:
                                                # Если запись не была найдена, то значит что ее не существовало ранее и она будет создана
                                                self.cursor.execute("""
                                                        INSERT INTO report(id_user, start_day)
                                                        VALUES(
                                                                {id_user}, "{start_day}"
                                                        )
                                                """.format(
                                                        id_user = self.selected_user_id,
                                                        start_day = day_start
                                                ))
                                                self.connect.commit()

                                                if self.lineEdit_edit_date_isConnected:
                                                        self.lineEdit_edit_date.disconnect()
                                                        self.lineEdit_edit_date_isConnected = False

                                                self.save_report()
                else:
                        # Вписать код для отображения ошибки форматирования даты
                        self.label_errors.setText('Неверный формат даты')
                        self.lineEdit_edit_date.setStyleSheet(self.styleSheet.input_datetime)
                        self.lineEdit_edit_date.textChanged.connect(lambda ch, obj = self.lineEdit_edit_date: self.lineEdit_edit_clsRed(obj))

        def checkbox_edit_clsRed(self, obj):
                self.label_errors.setText('')
                self.checkbox_autostop.setStyleSheet(self.styleSheet.checkbox)

        def lineEdit_edit_clsRed(self, obj):
                self.label_errors.setText('')
                obj.setStyleSheet(self.styleSheet.input_datetime)
                obj.disconnect()

        def date_edited(self, obj):
                field_text = obj.text()
                self.btn_generate_report.setEnabled(False)
                self.label_errors.setText('')
                self.label_page.setText('')

                if len(field_text) == 10:
                        template = "(\d{2}).(\d{2}).(\d{4})"

                        if re.match(template, self.lineEdit_startdate.text()) is not None and re.match(template, self.lineEdit_enddate.text()) is not None and report.date_datetime(self.lineEdit_startdate.text()).date <= report.date_datetime(self.lineEdit_enddate.text()).date:
                                self.btn_generate_report.setEnabled(True)
                                self.btn_generate_report.setStyleSheet(self.styleSheet.btn)
                                self.show_report()
                        else:
                                self.btn_generate_report.setEnabled(False)
                                self.btn_generate_report.setStyleSheet(self.styleSheet.btn_off)

                else:
                        if len(field_text) == 2 and re.match("(\d{2}).", self.old_value[obj]) is None:
                                obj.setText(field_text + '.')

                        elif len(field_text) == 5 and re.match("(\d{2}).(\d{2}).", self.old_value[obj]) is None:
                                obj.setText(field_text + '.')
                                
                        self.btn_generate_report.setEnabled(False)
                        self.btn_generate_report.setStyleSheet(self.styleSheet.btn_off)

                        self.old_value[obj] = obj.text()
                        self.clear_report()

                if field_text:
                        # Проверка на наличия текста, для того чтобы значение, которое было введено после оставалось белым
                        # Если текст есть:
                        obj.setStyleSheet(self.styleSheet.input_datetime_full)
                
                else:
                        # Если в поле нету текста, то делаем его обратно серым
                        obj.setStyleSheet(self.styleSheet.input_datetime)

                        if self.temp_report_list:
                                self.clear_report()

                self.show_edit_panel( mode = 'clear' )

        def show_report(self, page: int = 1): # Показать элементы отчета
                # Формат: DD.MM.YYYY
                self.clear_report()
                start_date = self.lineEdit_startdate.text()
                end_date = self.lineEdit_enddate.text()

                start_day = start_date.split('.')[0]
                start_month = start_date.split('.')[1]
                start_year = start_date.split('.')[2]

                end_day = end_date.split('.')[0]
                end_month = end_date.split('.')[1]
                end_year = end_date.split('.')[2]

                start_day = str(start_year) + '-' + str(start_month) + '-' + str(start_day)
                end_day =  str(end_year) + '-' + str(end_month) + '-' + str(end_day)

                data = self.cursor.execute("""
                        SELECT day_len, start_day, status FROM report
                        WHERE id_user = {id_user} AND start_day >= '{start_day}' AND start_day <= '{end_day}' AND status IS NOT 'deleted'
                        ORDER BY start_day DESC
                """.format(
                        id_user = self.selected_user_id,
                        start_day = start_day + ' 00:00',
                        end_day = end_day + ' 23:59'
                )).fetchall()
                if data:
                        # Устанавливаем заголовки
                        self.label_title_date.setText('Дата')
                        self.label_title_weekday.setText('День недели')
                        self.label_report_count.setText('Отработано')

                        # Устанавливаем счетчик страниц
                        data_len = len(data)
                        if not data_len % 10:
                                add = 0
                        else:
                                add = 1
                        pages = data_len // 10 + add
                        self.label_page.setText(str(page) + ' / ' + str(pages))
                        
                        # Далее будет управление кнопками (блокировка и разблокировка их в зависимости от текущей страницы)
                        if page == pages:
                                # Если достигнута максимальная страница, то блокируем кнопку вверх
                                self.btn_report_up.setEnabled(False)
                                self.btn_report_down.setEnabled(True)
                        
                        if page == 1:
                                # Если у нас в данный момент 1 страница, то мы не можем листатить вниз (блокируем эту кнопку)
                                self.btn_report_up.setEnabled(True)
                                self.btn_report_down.setEnabled(False)

                        if page != 1 and page != pages:
                                # Если у нас ни первая страница, ни последняя страницы
                                self.btn_report_up.setEnabled(True)
                                self.btn_report_down.setEnabled(True)

                        if pages == 1:
                                # Если у нас всего одна странциа
                                self.btn_report_up.setEnabled(False)
                                self.btn_report_down.setEnabled(False)

                        start_y = 100 # Позиция по Y с которой начинается расстановка объектов для отображения

                        count_hours = int() # Переменная, в которой будут считаться все часы и после отображаться внизу интерфейса

                        # Определяем какие записи будут выводиться (для того, чтобы можно было листать по стрелочкам)
                        min_record = 0
                        max_record = 11
                        if page > 1:
                                min_record = page * 10 - 10
                                max_record = page * 10 + 1

                        weekday_list = ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота', 'Воскресенье']
                        
                        # Подсчет всех часов в периоде, для отображения под списком
                        for i in data:
                                if not i[0]: # Не считаем те, у которых нету длины дня (не завершенный день)
                                        continue
                                count_hours += i[0]

                        for i in data[min_record:max_record]:
                                # Кортеж используется для того, чтобы выбрать определенный список записей (Например с 1 по 10 или с 11 по 20)
                                # i - запись, полученная в запросе
                                if not i[0]:
                                        # Такие записи чаще всего появляются после того, как день не был закончен. Скорее всего это за сегодняшний день
                                        # Просто устанавливаем текст для кнопки, которая будет отображаться
                                        day_len = '...'

                                elif i[0]:
                                        # Если день был закончен (i[0] имеет какую-то запись только в том случае, если в БД day_len имеет значение)

                                        # Переводим полученное значение из минутного вида (аля отработал 333 минуты) в часовой вид (333 минуты превратиться в 05:33)
                                        # В случае если минуты будут <10, то будет подставлен 0 для эстетического вида
                                        hours = i[0] // 60
                                        if hours < 10:
                                                hours = '0' + '' + str(hours)
                                        
                                        minutes = i[0] % 60
                                        if minutes < 10:
                                                minutes = '0' + '' + str(minutes)

                                        day_len = str(hours) + ':' + str(minutes)

                                date = i[1].split(' ')[0] # Формат YYYY-MM-DD HH:MM делим и оставляем YYYY-MM-DD

                                # Определяем день недели (получим значение от 0 до 6) и после можно будет понять с помощью массива weekday_list какое текстовое значения дня недели выводить
                                weekday_num = datetime.datetime.isoweekday( datetime.datetime( year = int(date.split('-')[0]), month = int(date.split('-')[1]), day = int(date.split('-')[2]) ) ) - 1

                                # Вывод кнопки с количеством часов
                                self.btn_count = QtWidgets.QPushButton(self.reports)
                                self.btn_count.setGeometry(QtCore.QRect(260, start_y, 130, 25))
                                self.btn_count.setFont(self.font)
                                self.btn_count.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
                                self.btn_count.setObjectName(date)
                                self.btn_count.setStyleSheet(self.styleSheet.btn)
                                if i[2] == 'auto':
                                        # Проверка на автоматическое закрытие
                                        self.btn_count.setStyleSheet(self.styleSheet.btn_red_text)
                                        
                                self.btn_count.setText(str( day_len ))
                                self.btn_count.show()
                                self.btn_count.clicked.connect(lambda ch, btn = self.btn_count: self.show_date(btn))
                                self.temp_report_list.append(self.btn_count)

                                # Вывод даты
                                self.label_report_date = QtWidgets.QLabel(self.reports)
                                self.label_report_date.setGeometry(QtCore.QRect(20, start_y, 110, 25))
                                self.label_report_date.setFont(self.font)
                                self.label_report_date.setStyleSheet(self.styleSheet.label_text)
                                self.label_report_date.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                                self.label_report_date.setObjectName("label_report_date")
                                self.label_report_date.setText(date.split('-')[2] + '.' + date.split('-')[1] + '.' + date.split('-')[0])
                                self.label_report_date.show()
                                self.temp_report_list.append(self.label_report_date)
                                
                                # Вывод текстового значения дня недели
                                self.label_report_weekday = QtWidgets.QLabel(self.reports)
                                self.label_report_weekday.setGeometry(QtCore.QRect(130, start_y, 130, 25))
                                self.label_report_weekday.setFont(self.font)
                                self.label_report_weekday.setStyleSheet(self.styleSheet.label_text)
                                self.label_report_weekday.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                                self.label_report_weekday.setObjectName("label_report_weekday")
                                self.label_report_weekday.setText(weekday_list[weekday_num])
                                self.label_report_weekday.show()
                                self.temp_report_list.append(self.label_report_weekday)

                                start_y += 25

                        # Так же как и в начале переводим минуты в понятный вид
                        hours = count_hours // 60
                        if hours < 10:
                                hours = '0' + str(hours)
                        
                        minutes = count_hours % 60
                        if minutes < 10:
                                minutes = '0' + str(minutes)

                        self.label_report_count_hours.setText( str(hours) + ':' + str(minutes) )

                else:
                        self.clear_report()

        def show_date(self, btn): # Отобразить дату
                self.show_edit_panel('create')
                date = btn.objectName()
                data = self.cursor.execute("""
                        SELECT start_day, start_dinner, end_dinner, end_day, status FROM report WHERE start_day >= '{date} 00:00' AND start_day <= '{date} 23:59' AND id_user = {id_user} AND status IS NOT 'deleted'
                """.format(
                        date = date,
                        id_user = self.selected_user_id
                )).fetchone()
                if data:
                        start_day = data[0].split(' ')[1]
                        if data[1]:
                                start_dinner = data[1].split(' ')[1]
                        else:
                                start_dinner = ''

                        if data[2]:
                                end_dinner = data[2].split(' ')[1]
                        else:
                                end_dinner = ''

                        if data[3]:
                                end_day = data[3].split(' ')[1]
                        else:
                                end_day = ''

                        status = data[4]

                        # Status list:
                        # day_off - отгул
                        # deleted - удалено (не будет отображаться в таблице)
                        # changed - изменено

                        self.lineEdit_edit_date.setEnabled(False)

                        if status != 'auto' and status in ['time_off', 'changed', None]:
                                self.checkbox_autostop.setEnabled(False)
                                self.checkbox_autostop.setChecked(False)
                                self.checkbox_autostop.setStyleSheet(self.styleSheet.checkbox_not_active)

                        elif status == 'auto':
                                self.checkbox_autostop.setEnabled(True)
                                self.checkbox_autostop.setChecked(True)
                                self.checkbox_autostop.setStyleSheet(self.styleSheet.checkbox)

                        if status == 'time_off':
                                self.checkbox_timeoff.setChecked(True)

                        self.lineEdit_edit_start_day.setText(start_day)
                        self.lineEdit_edit_start_dinner.setText(start_dinner)
                        self.lineEdit_edit_end_dinner.setText(end_dinner)
                        self.lineEdit_edit_end_day.setText(end_day)
                        self.lineEdit_edit_date.setText(date.split('-')[2] + '.' + date.split('-')[1] + '.' + date.split('-')[0])

        def clear_report(self): # Очистка всех объектов, которые есть на панели вывода основной информации
                while self.temp_report_list:
                        for i in self.temp_report_list:
                                i.deleteLater()
                                self.temp_report_list.remove(i)

                date_format = "(\d{2}).(\d{2}).(\d{4})"
                if re.match(date_format, self.lineEdit_startdate.text()) is None or re.match(date_format, self.lineEdit_enddate.text()) is None:
                        self.label_title_weekday.setText('Введите период')
                else:
                        self.label_title_weekday.setText('Нету записей')
                self.label_report_count_hours.setText('')
                self.label_title_date.setText('')
                self.label_report_count.setText('')

        def btn_period_this_month(self): # Вставка в input период в размере текущего месяца
                # Определяем текущий год
                year = int(datetime.datetime.now().year)

                # Определяем сколько дней в месяце в году (на случай если год високосный)
                if not year % 4:
                        month_len = [31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
                else:
                        month_len = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
                
                # Определяем месяц (и дописываем ему 0, для красоты и полноты)
                month = int(datetime.datetime.now().month)
                if month < 10:
                        month = '0' + str(month)
                month = str(month)
                first_date = '01.' + month + '.' + str(year)
                last_date = str( month_len[ int(month) - 1 ] ) + '.' + month + '.' + str(year)

                self.lineEdit_startdate.setText(first_date)
                self.lineEdit_enddate.setText(last_date)

        def change_user(self): # Функция, активирующаяся при изменении пользователя по кнопке сохранить
                start_day = self.checkbox_start_day.isChecked()
                report = self.checkbox_report.isChecked()
                admin = self.checkbox_admin.isChecked()
                inReport = self.checkbox_inreport.isChecked()
                hiddenSoft_R = self.checkbox_hiddenSoft_R.isChecked()
                hiddenSoft_RW = self.checkbox_hiddenSoft_RW.isChecked()
                specialReport = self.checkbox_specialReport.isChecked()

                start_day       = 1 if start_day else 0
                report          = 1 if report and not admin else 0
                admin           = 1 if admin else 0
                inReport        = 1 if inReport else 0
                hiddenSoft_R    = 1 if hiddenSoft_R and not hiddenSoft_RW else 0
                hiddenSoft_RW   = 1 if hiddenSoft_RW else 0
                specialReport   = 1 if specialReport else 0

                self.user.change_user(self.selected_user_id, 'start_day', new_value = start_day)
                self.user.change_user(self.selected_user_id, 'report', new_value = report)
                self.user.change_user(self.selected_user_id, 'admin', new_value = admin)
                self.user.change_user(self.selected_user_id, 'inReport', new_value = inReport)
                self.user.change_user(self.selected_user_id, 'generalReport', new_value = specialReport)
                self.user.change_user(self.selected_user_id, 'hidden_software_r', new_value = hiddenSoft_R)
                self.user.change_user(self.selected_user_id, 'hidden_software_rw', new_value = hiddenSoft_RW)
                self.change_user_cancel() # Обновляем чекбоксы, на тот случай, если имеются не совместимые права (report и admin не совместимы, может быть что-то одно)

        def change_user_cancel(self): # Ф-я для сброса выбранных чекбоксов, автоматически будут установлены значения из БД (p.s. внутри вызывается update_info)
                self.update_info( self.combobox_username.currentText() )

        def update_info(self, username): # При выборе пользователя автоматически обновляется информация о его доступах (изменяются чекбоксы на 2 вкладке)
                # Устанавливаем права на 2 вкладке для уже выбранного пользователя
                # Set roots at 2 widget for selected user
                root_list = self.cursor.execute(
                        """
                                SELECT root.start_day, root.report, root.admin, root.inReport, users.id, root.generalReport, root.hidden_software_r, root.hidden_software_rw FROM users, root
                                WHERE root.id_user = users.id AND users.username = "{username}"
                        """.format(
                                username = username
                        )
                ).fetchone()

                self.selected_user_id = root_list[4]

                self.checkbox_start_day.setChecked(True) if root_list[0] else self.checkbox_start_day.setChecked(False)                                 # Право на начало дня
                self.checkbox_report.setChecked(True) if root_list[1] and not root_list[2] else self.checkbox_report.setChecked(False)                  # Право на работу с отчетом
                self.checkbox_admin.setChecked(True) if root_list[2] else self.checkbox_admin.setChecked(False)                                         # Администратор
                self.checkbox_inreport.setChecked(True) if root_list[3] else self.checkbox_inreport.setChecked(False)                                   # Показ в отчете
                self.checkbox_specialReport.setChecked(True) if root_list[5] else self.checkbox_specialReport.setChecked(False)                              # Специальный отчет
                self.checkbox_hiddenSoft_R.setChecked(True) if root_list[6] and not root_list[7] else self.checkbox_hiddenSoft_R.setChecked(False)          # R  скрытого ПО
                self.checkbox_hiddenSoft_RW.setChecked(True) if root_list[7] else self.checkbox_hiddenSoft_RW.setChecked(False)                              # RW скрытого ПО

                self.clear_report()
                self.label_title_weekday.setText('Выберите период')
                self.label_title_date.setText('')
                self.label_report_count.setText('')
                
                self.lineEdit_startdate.setText('')
                self.lineEdit_enddate.setText('')
                self.label_page.setText('')
                self.lineEdit_deluser_reason.setText('')

        def add_user(self): # Активация при нажатии кнопки "Сохранить" пользователя на 2 вкладке
                username = self.lineEdit_username.text()
                login = self.lineEdit_login.text()
                organization = self.lineEdit_organization.text()
                birthday = self.lineEdit_birthday.text()
                        
                if not username: # Если ФИО не введено
                        self.lineEdit_username.setStyleSheet(self.styleSheet.input_text_error)

                if not birthday: # Если дата рождения не введена
                        self.lineEdit_birthday.setStyleSheet(self.styleSheet.input_text_error)

                if not login: # Если логин не введен
                        self.lineEdit_login.setStyleSheet(self.styleSheet.input_text_error)

                if not organization: # Если не введена организация
                        self.lineEdit_organization.setStyleSheet(self.styleSheet.input_text_error)

                if username and login and organization and birthday: # Если и ФИО и логин введены, то добавляем пользователя

                        if not re.match(r'^\d{2}\.\d{2}\.\d{4}$', self.lineEdit_birthday.text()):
                                self.lineEdit_birthday.setStyleSheet(self.styleSheet.input_text_full_error)
                                self.label_errors.setText('Формат даты DD.MM.YYYY')
                                return

                        # Для начала проверяем, есть ли пользователь с таким логином
                        _a = self.cursor.execute('SELECT id FROM users WHERE login = "{login}"'.format(
                                login = login
                        )).fetchone()

                        if not _a:
                                self.user.add_user(login, username, organization, birthday)
                                self.combobox_username.addItem( username )

                                self.lineEdit_username.setText('')
                                self.lineEdit_login.setText('')
                                self.lineEdit_organization.setText('')
                                self.lineEdit_birthday.setText('')
                        
                        elif _a:
                                self.lineEdit_login.setStyleSheet(self.styleSheet.input_text_full_error)
                                self.label_errors.setText('Пользователь с таким логином уже есть')

        def addUser_changed(self, obj): # Сброс красного обрамления в случае неправильно введенных данных в поле "ФИО" на 2 вкладке
                self.label_errors.setText('')
                if obj.text():
                        obj.setStyleSheet(self.styleSheet.input_text_full)
                else:
                        obj.setStyleSheet(self.styleSheet.input_text)

        def cancel_add_user(self): # При нажатии кнопки отмена создания пользователя на 2 странице сбрасываются поля "ФИО" и "Логин"
                self.lineEdit_username.setText('')
                self.lineEdit_username.setStyleSheet(self.styleSheet.input_text)
                self.lineEdit_login.setText('')
                self.lineEdit_login.setStyleSheet(self.styleSheet.input_text)
                self.lineEdit_organization.setText('')
                self.lineEdit_organization.setStyleSheet(self.styleSheet.input_text)
                self.lineEdit_birthday.setText('')
                self.lineEdit_birthday.setStyleSheet(self.styleSheet.input_text)

        def close(self):
                self.close()

class Thread(QThread):

        signal = QtCore.pyqtSignal(str)
        def __init__(self, parent = None):
                QtCore.QThread.__init__(self, parent)
                self.running = False
                self.count = 0

        def run(self):
                self.running = True
                while self.running:
                        self.count += 1
                        self.signal.emit('One more time ' + str( self.count ))
                        self.sleep(5)

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    app.setWindowIcon(QtGui.QIcon('icon.ico'))
    w = MainWindow()
    w.show()
    sys.exit(app.exec())