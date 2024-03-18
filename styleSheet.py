class styleSheet:
    """
    # Данный класс содержит стили, которые используются в работе приложения WorkDay - Admin
    # Создан для более удобного редактирования и использования стилей

    label_bg
    label_text
    label_error
    label_inverse

    btn
    btn_off
    btn_red_text
    inverse_btn
    inverse_btn_off

    input_datetime
    input_datetime_full
    input_datetime_error
    input_datetime_full_error

    input_text
    input_text_full
    input_text_error
    input_text_full_error

    tab_widget

    checkbox
    checkbox_error
    checkbox_not_active

    combobox

    status_off
    status_onLine
    status_dinner
    status_disabled
    """

    
    def __init__(self, colors):

        # Label
        self.label_bg = """
            QLabel {{
                background-color: {rectangle};
                border-radius: 10px;
                color: white;
            }}
        """.format(
            rectangle = colors.rectangle
        )

        self.label_text = """
            QLabel {{
                background: transparent;
                color: {text_color}
            }}
        """.format(
            text_color = colors.text_color
        )

        self.label_inverse = """
            QLabel {{
                background: transparent;
                color: {text_color_inverse}
            }}
        """.format(
            text_color_inverse = colors.text_color_inverse
        )

        self.label_error = """
            QLabel {{
                background: transparent;
                color: {hover_negative};
            }}
        """.format(
            hover_negative = colors.hover_negative
        )

        # Btn
        self.btn = """
            QPushButton {{
                background-color: {rectangle};
                border-radius: 10px;
                color: {text_color};
                outline: 0;
            }}

            QPushButton:hover {{
                background-color: {hover};
                color: {text_color_inverse};
            }}
        """.format(
            text_color_inverse = colors.text_color_inverse,
            text_color = colors.text_color,
            hover = colors.hover,
            rectangle = colors.rectangle
        )

        self.btn_off = """
            QPushButton {{
                background-color: {rectangle};
                border-radius: 10px;
                color: {non_active_color};
                outline: 0;
            }}
        """.format(
            rectangle = colors.rectangle,
            non_active_color = colors.non_active_color
        )

        self.btn_red_text = """
            QPushButton {{
                background-color: {rectangle};
                border-radius: 10px;
                color: {hover_negative};
                outline: 0;
            }}

            QPushButton:hover {{
                background-color: {hover};
            }}
        """.format(
            rectangle = colors.rectangle,
            hover = colors.hover,
            hover_negative = colors.hover_negative
        )

        self.inverse_btn = """
            QPushButton {{
                background-color: {background};
                border-radius: 10px;
                color: {text_color_inverse};
                outline: 0;
            }}

            QPushButton:hover {{
                background-color: {hover};
                color: {text_color_inverse};
            }}
        """.format(
            background = colors.background,
            hover = colors.hover,
            text_color_inverse = colors.text_color_inverse
        )

        self.inverse_btn_off = """
            QPushButton {{
                background-color: {background};
                border-radius: 10px;
                outline: 0;
                color: {non_active_color};
            }}

            QPushButton:hover {{
                background-color: {hover};
                color: {non_active_color};
            }}
        """.format(
            background = colors.background,
            hover = colors.hover,
            non_active_color = colors.non_active_color
        )

        # Input datetime
        self.input_datetime = """
            QLineEdit {{
                color: {non_active_color};
                background-color: {background};
                border: none;
                border-radius: 10px;
            }}

            QLineEdit:focus {{
                color: {text_color_inverse};
            }}
        """.format(
            non_active_color = colors.non_active_color,
            background = colors.background,
            text_color_inverse = colors.text_color_inverse
        )

        self.input_datetime_full = """
            QLineEdit {{
                color: {text_color_inverse};
                background-color: {background};
                border: none;
                border-radius: 10px;
            }}

            QLineEdit:focus {{
                color: {text_color_inverse};
            }}
        """.format(
            background = colors.background,
            text_color_inverse = colors.text_color_inverse
        )

        self.input_datetime_error = """
            QLineEdit {{
                color: {non_active_color};
                background-color: {background};
                border: 2px solid {hover_negative};
                border-radius: 10px;
            }}

            QLineEdit:focus {{
                color: {text_color_inverse};
            }}
        """.format(
            background = colors.background,
            text_color_inverse = colors.text_color_inverse,
            hover_negative = colors.hover_negative,
            non_active_color = colors.non_active_color
        )

        self.input_datetime_full_error = """
            QLineEdit {{
                color: {text_color_inverse};
                background-color: {background};
                border: 2px solid {hover_negative};
                border-radius: 10px;
            }}

            QLineEdit:focus {{
                color: {text_color_inverse};
            }}
        """.format(
            background = colors.background,
            text_color_inverse = colors.text_color_inverse,
            hover_negative = colors.hover_negative
        )

        # Input text
        self.input_text = """
                QLineEdit {{
                        color: {non_active_color};
                        background-color: {background};
                        border: none;
                        border-radius: 10px;
                        padding-left: 5px;
                }}

                QLineEdit:focus {{
                        color: {text_color_inverse};
                }}
        """.format(
                non_active_color = colors.non_active_color,
                background = colors.background,
                text_color_inverse = colors.text_color_inverse
        )

        self.input_text_full = """
                QLineEdit {{
                        color: {text_color_inverse};
                        background-color: {background};
                        border: none;
                        border-radius: 10px;
                        padding-left: 5px;
                }}

                QLineEdit:focus {{
                        color: {text_color_inverse};
                }}
        """.format(
                background = colors.background,
                text_color_inverse = colors.text_color_inverse
        )

        self.input_text_error = """
                QLineEdit {{
                        color: {non_active_color};
                        background-color: {background};
                        border: 2px solid {hover_negative};
                        border-radius: 10px;
                        padding-left: 5px;
                }}

                QLineEdit:focus {{
                        color: {text_color_inverse};
                }}
        """.format(
                non_active_color = colors.non_active_color,
                background = colors.background,
                text_color_inverse = colors.text_color_inverse,
                hover_negative = colors.hover_negative
        )

        self.input_text_full_error = """
                QLineEdit {{
                        color: {text_color_inverse};
                        background-color: {background};
                        border: 2px solid {hover_negative};
                        border-radius: 10px;
                        padding-left: 5px;
                }}

                QLineEdit:focus {{
                        color: {text_color_inverse};
                }}
        """.format(
                non_active_color = colors.non_active_color,
                background = colors.background,
                text_color_inverse = colors.text_color_inverse,
                hover_negative = colors.hover_negative
        )
        
        # Tab widget
        self.tab_widget = """
            QTabWidget::pane {{
                border: none;
                background: transparent;
            }}

            QTabBar::tab {{
                background: {rectangle};
                border: none;
                border-radius: 10px;
                padding: 0 10px;
                height: 30px;
                color: {text_color};
                margin: 0 10px;
            }}

            QTabBar::tab:hover, QTabBar::tab:selected {{
                background: {hover};
            }}
        """.format(
            rectangle = colors.rectangle,
            text_color = colors.text_color,
            hover = colors.hover
        )

        # Checkbox
        self.checkbox = """
            QCheckBox {{
                color: {text_color};
                background-color: transparent;
                outline: 0;
            }}

            QCheckBox::indicator {{
                border: 2px solid {indicator_border};
                width: 10px;
                height: 10px;
                border-radius: 2px;
                margin-top: 2px;
            }}

            QCheckBox::indicator:checked {{
                background-color: {hover};
                border-radius: 2px;
            }}
        """.format(
                text_color = colors.text_color,
                indicator_border = colors.indicator_border,
                hover = colors.hover
        )

        self.checkbox_error = """
            QCheckBox {{
                color: {hover_negative};
                background-color: transparent;
                outline: 0;
            }}

            QCheckBox::indicator {{
                border: 2px solid {indicator_border};
                width: 10px;
                height: 10px;
                border-radius: 2px;
                margin-top: 2px;
            }}

            QCheckBox::indicator:checked {{
                background-color: {hover};
                border-radius: 2px;
            }}
        """.format(
                hover_negative = colors.hover_negative,
                indicator_border = colors.indicator_border,
                hover = colors.hover
        )

        self.checkbox_not_active = """
                QCheckBox {{
                        color: {non_active_color};
                        background-color: transparent;
                        outline: 0;
                }}

                QCheckBox::indicator {{
                        border: 2px solid {non_active_color};
                        width: 10px;
                        height: 10px;
                        border-radius: 2px;
                        margin-top: 2px;
                }}
        """.format(
                non_active_color = colors.non_active_color
        )

        # Combobox
        self.combobox = """
            QComboBox {{
                background-color: {rectangle};
                border-radius: 10px;
                color: {text_color};
                padding: 10px;
                outline: 0;
            }}

            QComboBox:hover {{
                background-color: {hover};
            }}

            QComboBox::drop-down {{
                width: 0;
                border-radius: 10px;
            }}

            QComboBox:editable {{
                background: {background};
                border-radius: 10px;
            }}

            QComboBox QAbstractItemView {{
                margin-top: 5px;
                color: #1C1D22;
                padding: 10px 5px;
                background-color: white;
                outline: none;
                border-radius: 10px;
            }}
        """.format(
            rectangle = colors.rectangle,
            text_color = colors.text_color,
            hover = colors.hover,
            background = colors.background
        )

        # status
        self.status_off = """
            QLabel {{
                background: transparent;
                color: {non_active_color}
            }}
        """.format(
            non_active_color = colors.non_active_color
        )
        
        self.status_onLine = """
            QLabel {
                background: transparent;
                color: #5ddf8b
            }
        """

        self.status_dinner = """
            QLabel {
                background: transparent;
                color: #dddf5d
            }
        """

        self.status_disabled = """
            QLabel {{
                background: transparent;
                color: {hover_negative}
            }}
        """.format(
            hover_negative = colors.hover_negative
        )