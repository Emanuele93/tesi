import functools
import re
import contextlib
import io
from functools import partial
from threading import Thread

import requests
from PyQt5.QtGui import QTextCursor, QFont, QFontMetricsF, QIcon
from PyQt5.QtWidgets import QWidget, QTextEdit, QPlainTextEdit, QPushButton, QSplitter, QHBoxLayout, QVBoxLayout, \
    QLineEdit, QCheckBox, QCalendarWidget, QLabel, QScrollArea, QDialog, QComboBox
from PyQt5.QtCore import *

from windows.ConfirmWindow import ConfirmWindow


class CreateHomeworkWindow(QWidget):
    def __init__(self, data, closer_controller, exercise=None):
        super(CreateHomeworkWindow, self).__init__(flags=Qt.Window)
        self.setMinimumSize(QSize(800, 800))
        self.setWindowTitle("Creazione di un nuovo esercizio")
        self.setWindowIcon(QIcon("img/logo.png"))
        self.data = data
        self.text_changed = True
        self.temp_vars = {}
        self.resources_correct = True
        self.text_exercise_ready = False
        self.exercise = exercise
        self.functions = {
            'if': 0,
            'elif': 0,
            'else': 0,
            'for': 0,
            'while': 0,
            'def': 0
        }

        self.closer_controller = closer_controller
        self.white_paper_mode = False
        self.difficulty = "Facile"

        self.text_exercise = QPlainTextEdit(self)
        self.text_exercise.setPlaceholderText("  Inserire qui il testo dell'esercizio")
        self.text_exercise.setStyleSheet("QWidget {color: red}")
        self.text_exercise.textChanged.connect(self.text_exercise_changed)

        self.numbers = QTextEdit(self)
        self.numbers.setReadOnly(True)
        self.numbers.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.numbers.setFixedWidth(50)

        self.code_editor = QTextEdit(self)
        self.code_editor.setLineWrapMode(self.code_editor.NoWrap)
        self.code_editor.textChanged.connect(self.format_text)
        self.code_editor.verticalScrollBar().valueChanged.connect(self.scroll_numbers)
        self.code_editor.setPlaceholderText("Inserire il codice di partenza\n(Non obbligatorio)")
        self.code_editor.setTabStopDistance(QFontMetricsF(self.code_editor.font()).width(' ') * 12)

        self.results = QPlainTextEdit(self)
        self.results.setReadOnly(True)
        self.results.setLineWrapMode(self.results.NoWrap)

        settings_widget = QWidget(self, flags=Qt.Widget)
        settings_widget.setLayout(self.get_settings_layout())
        settings_widget.setFixedWidth(400)
        settings_widget.setObjectName("settings_widget")
        settings_widget.setStyleSheet("QWidget#settings_widget {border: 0px solid grey; "
                                      "border-right: 1px solid grey}")

        if self.exercise is not None:
            self.text_exercise.setPlainText(self.exercise.text)
        self.code_editor.setText('' if self.exercise is None else self.exercise.start_code)
        self.set_text_font_size(self.data.code_font_size)

        box = QHBoxLayout(self)
        box.setSpacing(0)
        box.setContentsMargins(0, 0, 0, 0)
        box.addWidget(self.numbers)
        box.addWidget(self.code_editor)
        widget2 = QWidget(self, flags=Qt.Widget)
        widget2.setLayout(box)

        self.coding_widget = QSplitter()
        self.coding_widget.setOrientation(Qt.Horizontal if data.code_result_horizontal_orientation else Qt.Vertical)
        self.coding_widget.addWidget(widget2)
        self.coding_widget.addWidget(self.results)
        self.coding_widget.setSizes([150, 100])
        self.coding_widget.setChildrenCollapsible(False)

        splitter2 = QSplitter(Qt.Vertical)
        splitter2.addWidget(self.text_exercise)
        splitter2.addWidget(self.coding_widget)
        splitter2.setSizes([100, 500])
        splitter2.setChildrenCollapsible(False)
        splitter2.setContentsMargins(10, 10, 10, 10)

        box = QHBoxLayout(self)
        box.setContentsMargins(0, 0, 0, 0)
        box.addWidget(settings_widget)
        box.addWidget(splitter2)

    def get_settings_layout(self):
        self.play_button = QPushButton('Prova codice', self)
        self.play_button.setFixedSize(100, 50)
        self.play_button.clicked.connect(self.play_button_on_click)

        font = QFont()
        font.setPixelSize(20)
        self.title_widget = QLineEdit(self)
        self.title_widget.setPlaceholderText(" Inserire Titolo (20 caratteri max)")
        self.title_widget.setContentsMargins(20, 20, 20, 10)
        self.title_widget.textChanged.connect(self.title_form_changed)
        self.title_widget.setStyleSheet("QWidget {color: red}")
        self.title_widget.setFont(font)
        self.title_ready = False

        calendar_intro = QLabel("Data di consegna del compito:", self)
        calendar_intro.setContentsMargins(0, 20, 0, 0)

        self.calendar_widget = MyCalendar(self)
        self.calendar_widget.setVerticalHeaderFormat(QCalendarWidget.NoVerticalHeader)
        self.calendar_widget.setMinimumDate(QDate.currentDate())
        self.calendar_widget.setContentsMargins(0, 0, 0, 20)
        self.calendar_widget.setFixedHeight(300)
        self.calendar_widget.setGridVisible(True)
        self.calendar_widget.clicked.connect(self.title_form_changed)

        executable_intro = QLabel(self)
        executable_intro.setStyleSheet("border: 0px solid grey; border-bottom: 1px solid grey")
        executable_intro.setText("Codice eseguibile: ")

        self.executable_check = QCheckBox(self)
        self.executable_check.setChecked(True)
        self.executable_check.clicked.connect(self.executable_check_on_click)

        white_paper_mode_intro = QLabel(self)
        white_paper_mode_intro.setStyleSheet("border: 0px solid grey; border-bottom: 1px solid grey")
        white_paper_mode_intro.setText("Modalità carta e penna: ")

        white_paper_mode_check = QCheckBox(self)
        white_paper_mode_check.setChecked(False)
        white_paper_mode_check.clicked.connect(partial(self.white_paper_mode_check_on_click, white_paper_mode_check))

        line_limit_intro = QLabel(self)
        line_limit_intro.setStyleSheet("border: 0px solid grey; border-bottom: 1px solid grey")
        line_limit_intro.setText("Limite numero linee codice: ")

        self.line_limit_form = QLineEdit(self)
        self.line_limit_form.setPlaceholderText(" (Non Obbligatorio)")
        self.line_limit_form.textChanged.connect(self.update_function_counters)
        self.line_limit_form.setFixedWidth(150)

        variables_limit_intro = QLabel(self)
        variables_limit_intro.setStyleSheet("border: 0px solid grey; border-bottom: 1px solid grey")
        variables_limit_intro.setText("Limite variabili utilizzabili: ")

        self.variables_limit_form = QLineEdit(self)
        self.variables_limit_form.setPlaceholderText(" (Non Obbligatorio)")
        self.variables_limit_form.textChanged.connect(self.update_function_counters)
        self.variables_limit_form.setFixedWidth(150)

        conditions_limit_intro = QLabel(self)
        conditions_limit_intro.setStyleSheet("border: 0px solid grey; border-bottom: 1px solid grey")
        conditions_limit_intro.setText("Limite condizioni utilizzabili: ")

        self.conditions_limit_form = QLineEdit(self)
        self.conditions_limit_form.setPlaceholderText(" (Non Obbligatorio)")
        self.conditions_limit_form.textChanged.connect(self.update_function_counters)
        self.conditions_limit_form.setFixedWidth(150)

        if_limit_intro = QLabel(self)
        if_limit_intro.setStyleSheet("border: 0px solid grey; border-bottom: 1px solid grey")
        if_limit_intro.setText("Limite di if: ")

        self.if_limit_form = QLineEdit(self)
        self.if_limit_form.setPlaceholderText(" (Non Obbligatorio)")
        self.if_limit_form.setFixedWidth(150)
        self.if_limit_form.textChanged.connect(self.update_function_counters)

        elif_limit_intro = QLabel(self)
        elif_limit_intro.setStyleSheet("border: 0px solid grey; border-bottom: 1px solid grey")
        elif_limit_intro.setText("Limite di elif: ")

        self.elif_limit_form = QLineEdit(self)
        self.elif_limit_form.setPlaceholderText(" (Non Obbligatorio)")
        self.elif_limit_form.setFixedWidth(150)
        self.elif_limit_form.textChanged.connect(self.update_function_counters)

        else_limit_intro = QLabel(self)
        else_limit_intro.setStyleSheet("border: 0px solid grey; border-bottom: 1px solid grey")
        else_limit_intro.setText("Limite di elif: ")

        self.else_limit_form = QLineEdit(self)
        self.else_limit_form.setPlaceholderText(" (Non Obbligatorio)")
        self.else_limit_form.setFixedWidth(150)
        self.else_limit_form.textChanged.connect(self.update_function_counters)

        cycles_limit_intro = QLabel(self)
        cycles_limit_intro.setStyleSheet("border: 0px solid grey; border-bottom: 1px solid grey")
        cycles_limit_intro.setText("Limite cicli utilizzabili: ")

        self.cycles_limit_form = QLineEdit(self)
        self.cycles_limit_form.setPlaceholderText(" (Non Obbligatorio)")
        self.cycles_limit_form.textChanged.connect(self.update_function_counters)
        self.cycles_limit_form.setFixedWidth(150)

        for_limit_intro = QLabel(self)
        for_limit_intro.setStyleSheet("border: 0px solid grey; border-bottom: 1px solid grey")
        for_limit_intro.setText("Limite di for: ")

        self.for_limit_form = QLineEdit(self)
        self.for_limit_form.setPlaceholderText(" (Non Obbligatorio)")
        self.for_limit_form.setFixedWidth(150)
        self.for_limit_form.textChanged.connect(self.update_function_counters)

        while_limit_intro = QLabel(self)
        while_limit_intro.setStyleSheet("border: 0px solid grey; border-bottom: 1px solid grey")
        while_limit_intro.setText("Limite di while: ")

        self.while_limit_form = QLineEdit(self)
        self.while_limit_form.setPlaceholderText(" (Non Obbligatorio)")
        self.while_limit_form.setFixedWidth(150)
        self.while_limit_form.textChanged.connect(self.update_function_counters)

        functions_limit_intro = QLabel(self)
        functions_limit_intro.setStyleSheet("border: 0px solid grey; border-bottom: 1px solid grey")
        functions_limit_intro.setText("Limite fuzioni utilizzabili: ")

        self.functions_limit_form = QLineEdit(self)
        self.functions_limit_form.setPlaceholderText(" (Non Obbligatorio)")
        self.functions_limit_form.textChanged.connect(self.update_function_counters)
        self.functions_limit_form.setFixedWidth(150)

        level_intro = QLabel(self)
        level_intro.setText("Difficoltà: ")
        level_intro.setStyleSheet("border: 0px solid grey; border-bottom: 1px solid grey")

        easy_button = QPushButton('Facile', self)
        easy_button.setFixedWidth(50)
        medium_button = QPushButton('Medio', self)
        medium_button.setFixedWidth(50)
        hard_button = QPushButton('Difficile', self)
        hard_button.setFixedWidth(50)
        easy_button.setStyleSheet('background-color:green')
        easy_button.clicked.connect(partial(self.set_difficulty_on_click, easy_button, medium_button, hard_button,
                                            "Facile"))
        medium_button.clicked.connect(partial(self.set_difficulty_on_click, medium_button, easy_button, hard_button,
                                              "Medio"))
        hard_button.clicked.connect(partial(self.set_difficulty_on_click, hard_button, easy_button, medium_button,
                                            "Difficile"))

        self.order_by = QComboBox(self)
        self.order_by.addItem("Ordina per data di consegna")
        self.order_by.addItem("Classifica per linee di codice")
        self.order_by.addItem("Classifica per numero di variabili")
        self.order_by.addItem("Classifica per numero di condizioni")
        self.order_by.addItem("Classifica per numero di cicli")

        lookable_intro = QLabel(self)
        lookable_intro.setStyleSheet("border: 0px solid grey; border-bottom: 1px solid grey")
        lookable_intro.setText("Esercizio sbirciabile: ")

        self.lookable_check = QCheckBox(self)
        self.lookable_check.setChecked(True)

        self.send_button = QPushButton('Fine', self)
        self.send_button.setFixedSize(100, 50)
        self.send_button.setEnabled(False)
        self.send_button.clicked.connect(self.send_button_on_click)

        if self.exercise is not None:
            self.title_widget.setText(self.exercise.title)
            if not self.exercise.executable:
                self.executable_check.click()
            if self.exercise.white_paper_mode:
                white_paper_mode_check.click()
            if self.exercise.limits['lines'] is not None:
                self.line_limit_form.setText(str(self.exercise.limits['lines']))
            if self.exercise.limits['variables'] is not None:
                self.variables_limit_form.setText(str(self.exercise.limits['variables']))
            if self.exercise.limits['conditions'] is not None:
                self.conditions_limit_form.setText(str(self.exercise.limits['conditions']))
            if self.exercise.limits['if'] is not None:
                self.if_limit_form.setText(str(self.exercise.limits['if']))
            if self.exercise.limits['elif'] is not None:
                self.elif_limit_form.setText(str(self.exercise.limits['elif']))
            if self.exercise.limits['else'] is not None:
                self.else_limit_form.setText(str(self.exercise.limits['else']))
            if self.exercise.limits['cycles'] is not None:
                self.cycles_limit_form.setText(str(self.exercise.limits['cycles']))
            if self.exercise.limits['for'] is not None:
                self.for_limit_form.setText(str(self.exercise.limits['for']))
            if self.exercise.limits['while'] is not None:
                self.while_limit_form.setText(str(self.exercise.limits['while']))
            if self.exercise.limits['def'] is not None:
                self.functions_limit_form.setText(str(self.exercise.limits['def']))
            if self.exercise.level == 'Facile':
                easy_button.click()
            elif self.exercise.level == 'Medio':
                medium_button.click()
            else:
                hard_button.click()

        font.setPixelSize(25)
        tit = QLabel(self)
        tit.setFont(font)
        tit.setText('Creazione Compito')

        box = QHBoxLayout(self)
        box.setAlignment(Qt.AlignCenter)
        box.setSpacing(50)
        box.addWidget(tit)
        box.addWidget(self.send_button)
        widget0 = QWidget(self, flags=Qt.Widget)
        widget0.setLayout(box)
        widget0.setFixedHeight(100)

        box = QHBoxLayout(self)
        box.addWidget(executable_intro)
        box.addWidget(self.executable_check)
        widget2 = QWidget(self, flags=Qt.Widget)
        widget2.setLayout(box)

        box = QHBoxLayout(self)
        box.addWidget(white_paper_mode_intro)
        box.addWidget(white_paper_mode_check)
        widget3 = QWidget(self, flags=Qt.Widget)
        widget3.setLayout(box)

        box = QHBoxLayout(self)
        box.addWidget(if_limit_intro)
        box.addWidget(self.if_limit_form)
        box.setContentsMargins(0, 0, 0, 0)
        if_limit_widget = QWidget(self, flags=Qt.Widget)
        if_limit_widget.setLayout(box)

        box = QHBoxLayout(self)
        box.addWidget(elif_limit_intro)
        box.addWidget(self.elif_limit_form)
        box.setContentsMargins(0, 0, 0, 0)
        elif_limit_widget = QWidget(self, flags=Qt.Widget)
        elif_limit_widget.setLayout(box)

        box = QHBoxLayout(self)
        box.addWidget(else_limit_intro)
        box.addWidget(self.else_limit_form)
        box.setContentsMargins(0, 0, 0, 0)
        else_limit_widget = QWidget(self, flags=Qt.Widget)
        else_limit_widget.setLayout(box)

        box = QVBoxLayout(self)
        box.setContentsMargins(20, 0, 50, 0)
        box.addWidget(if_limit_widget)
        box.addWidget(elif_limit_widget)
        box.addWidget(else_limit_widget)
        if_elif_else_widget = QWidget(self, flags=Qt.Widget)
        if_elif_else_widget.setLayout(box)

        box = QHBoxLayout(self)
        box.addWidget(conditions_limit_intro)
        box.addWidget(self.conditions_limit_form)
        box.setContentsMargins(0, 0, 0, 0)
        conditions_limit_widget = QWidget(self, flags=Qt.Widget)
        conditions_limit_widget.setLayout(box)

        box = QVBoxLayout(self)
        box.addWidget(conditions_limit_widget)
        box.addWidget(if_elif_else_widget)
        if_elif_else_widget = QWidget(self, flags=Qt.Widget)
        if_elif_else_widget.setLayout(box)

        box = QHBoxLayout(self)
        box.addWidget(for_limit_intro)
        box.addWidget(self.for_limit_form)
        box.setContentsMargins(0, 0, 0, 0)
        for_limit_widget = QWidget(self, flags=Qt.Widget)
        for_limit_widget.setLayout(box)

        box = QHBoxLayout(self)
        box.addWidget(while_limit_intro)
        box.addWidget(self.while_limit_form)
        box.setContentsMargins(0, 0, 0, 0)
        while_limit_widget = QWidget(self, flags=Qt.Widget)
        while_limit_widget.setLayout(box)

        box = QVBoxLayout(self)
        box.setContentsMargins(20, 0, 50, 0)
        box.addWidget(for_limit_widget)
        box.addWidget(while_limit_widget)
        for_while_widget = QWidget(self, flags=Qt.Widget)
        for_while_widget.setLayout(box)

        box = QHBoxLayout(self)
        box.addWidget(cycles_limit_intro)
        box.addWidget(self.cycles_limit_form)
        box.setContentsMargins(0, 0, 0, 0)
        cycles_limit_widget = QWidget(self, flags=Qt.Widget)
        cycles_limit_widget.setLayout(box)

        box = QVBoxLayout(self)
        box.addWidget(cycles_limit_widget)
        box.addWidget(for_while_widget)
        for_while_widget = QWidget(self, flags=Qt.Widget)
        for_while_widget.setLayout(box)

        box = QHBoxLayout(self)
        box.setContentsMargins(0, 0, 0, 0)
        box.addWidget(easy_button)
        box.addWidget(medium_button)
        box.addWidget(hard_button)
        box.setSpacing(0)
        widget3_4 = QWidget(self, flags=Qt.Widget)
        widget3_4.setLayout(box)

        box = QHBoxLayout(self)
        box.addWidget(level_intro)
        box.addWidget(widget3_4)
        widget4 = QWidget(self, flags=Qt.Widget)
        widget4.setLayout(box)

        box = QHBoxLayout(self)
        box.addWidget(line_limit_intro)
        box.addWidget(self.line_limit_form)
        box.setContentsMargins(10, 10, 10, 10)
        line_limit_widget = QWidget(self, flags=Qt.Widget)
        line_limit_widget.setLayout(box)

        box = QHBoxLayout(self)
        box.addWidget(variables_limit_intro)
        box.addWidget(self.variables_limit_form)
        box.setContentsMargins(10, 10, 10, 10)
        variables_limit_widget = QWidget(self, flags=Qt.Widget)
        variables_limit_widget.setLayout(box)

        box = QHBoxLayout(self)
        box.addWidget(functions_limit_intro)
        box.addWidget(self.functions_limit_form)
        box.setContentsMargins(10, 10, 10, 10)
        functions_limit_widget = QWidget(self, flags=Qt.Widget)
        functions_limit_widget.setLayout(box)

        box = QHBoxLayout(self)
        box.addWidget(self.order_by)
        box.setContentsMargins(10, 10, 100, 10)
        order_by_widget = QWidget(self, flags=Qt.Widget)
        order_by_widget.setLayout(box)

        box = QHBoxLayout(self)
        box.addWidget(lookable_intro)
        box.addWidget(self.lookable_check)
        widget_look = QWidget(self, flags=Qt.Widget)
        widget_look.setLayout(box)

        settings_box = QVBoxLayout(self)
        settings_box.setAlignment(Qt.AlignTop)
        settings_box.addWidget(self.title_widget)
        settings_box.addWidget(calendar_intro)
        settings_box.addWidget(self.calendar_widget)
        settings_box.addWidget(widget2)
        settings_box.addWidget(widget3)
        settings_box.addWidget(line_limit_widget)
        settings_box.addWidget(variables_limit_widget)
        settings_box.addWidget(if_elif_else_widget)
        settings_box.addWidget(for_while_widget)
        settings_box.addWidget(functions_limit_widget)
        settings_box.addWidget(widget4)
        settings_box.addWidget(widget_look)
        settings_box.addWidget(order_by_widget)
        settings = QWidget(self)
        settings.setLayout(settings_box)

        box = QHBoxLayout(self)
        box.setContentsMargins(20, 20, 20, 20)
        box.addWidget(self.play_button, alignment=Qt.AlignLeft)
        send_button = QWidget(self, flags=Qt.Widget)
        send_button.setLayout(box)

        box = QVBoxLayout(self)
        box.setSpacing(0)
        box.setContentsMargins(0, 0, 0, 0)
        box.addWidget(settings)
        box.addWidget(send_button)
        options_widget = QWidget(self, flags=Qt.Widget)
        options_widget.setLayout(box)

        scroll_area = QScrollArea()
        scroll_area.setWidget(options_widget)
        scroll_area.setWidgetResizable(True)

        box = QVBoxLayout(self)
        box.setSpacing(0)
        box.setContentsMargins(0, 0, 0, 0)
        box.addWidget(widget0)
        box.addWidget(scroll_area)
        return box

    @staticmethod
    def timeout(timeout):
        def deco(func):
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                res = [Exception('function [%s] timeout [%s seconds] exceeded!' % (func.__name__, timeout))]

                def newFunc():
                    try:
                        res[0] = func(*args, **kwargs)
                    except Exception as e:
                        res[0] = e

                t = Thread(target=newFunc)
                t.daemon = True
                try:
                    t.start()
                    t.join(timeout)
                except Exception as je:
                    print('error starting thread')
                    raise je
                ret = res[0]
                if isinstance(ret, BaseException):
                    raise ret
                return ret

            return wrapper

        return deco

    def execution(self):
        try:
            stream = io.StringIO()
            with contextlib.redirect_stdout(stream):
                exec(self.code_editor.toPlainText(), globals(), self.temp_vars)
            self.execution_result = stream.getvalue()
            self.execution_errors = False
        except Exception as E:
            self.execution_result = str(E)
            self.execution_errors = True

            i = 0
            self.execution_temp_result = ''
            texts = self.code_editor.toPlainText().split('\n')
            text = texts[i]
            while i < len(texts):
                try:
                    stream = io.StringIO()
                    with contextlib.redirect_stdout(stream):
                        exec(text, globals(), self.temp_vars)
                    self.execution_temp_result = stream.getvalue()
                except Exception as E:
                    self.execution_temp_result = self.execution_temp_result
                i += 1
                if i < len(texts):
                    text += '\n' + texts[i]

    def play_button_on_click(self):
        self.temp_vars = {}
        self.execution_result = ''
        self.execution_temp_result = ''

        func = self.timeout(timeout=5)(self.execution)
        try:
            func()
        except Exception as E:
            self.execution_result = E
        if self.execution_temp_result != '':
            self.execution_result = self.execution_temp_result + '\n' + self.execution_result

        self.results.setPlainText(self.execution_result)
        if self.execution_errors:
            self.results.setStyleSheet('color: red')
        else:
            self.results.setStyleSheet('color: black')
        self.update_function_counters()
        return self.execution_errors

    def text_exercise_changed(self):
        if self.text_exercise.toPlainText().strip() == '':
            self.text_exercise.setStyleSheet("QWidget {color: red}")
            self.text_exercise_ready = False
        else:
            self.text_exercise.setStyleSheet("QWidget {color: black}")
            self.text_exercise_ready = True
        self.check_send_button_ready()

    def get_selected_day(self):
        selected_day = self.calendar_widget.selectedDate()
        s_day = ("0" + str(selected_day.day()) if selected_day.day() < 10 else str(selected_day.day())) + "/"
        s_day += ("0" + str(selected_day.month()) if selected_day.month() < 10 else str(selected_day.month())) + "/"
        s_day += str(selected_day.year())
        return s_day

    def title_form_changed(self):
        if self.title_widget.text().strip() == '' or len(self.title_widget.text()) > 20:
            self.title_widget.setStyleSheet("QWidget {color: red}")
            self.title_ready = False
        else:
            s_day = self.get_selected_day()
            for i in self.data.exercises:
                if i.date == s_day and i.title == self.title_widget.text():
                    self.title_widget.setStyleSheet("QWidget {color: red}")
                    self.title_ready = False
                    self.check_send_button_ready()
                    return
            self.title_widget.setStyleSheet("QWidget {color: black}")
            self.title_ready = True
        self.check_send_button_ready()

    def executable_check_on_click(self):
        if self.executable_check.isChecked():
            self.play_button.setEnabled(True)
            self.results.show()
        else:
            self.results.hide()
            self.play_button.setEnabled(False)

    def white_paper_mode_check_on_click(self, check):
        self.white_paper_mode = check.isChecked()
        self.code_editor.setText(self.code_editor.toPlainText())

    def set_difficulty_on_click(self, b1, b2, b3, difficulty):
        b1.setStyleSheet('background-color:green')
        b2.setStyleSheet('')
        b3.setStyleSheet('')
        self.difficulty = difficulty

    def check_send_button_ready(self):
        if self.title_ready and self.text_exercise_ready:
            self.send_button.setEnabled(True)
        else:
            self.send_button.setEnabled(False)

    def send_button_on_click(self):
        errors = self.play_button_on_click()

        confermation_text = "Sei sicuro di voler inviare l'esercizio?<br>" \
                            "La tua traccia non potrà più essere modificata!"

        if not self.resources_correct:
            confermation_text += "<br><br><span style=\" color: red;\">" \
                                 "Attenzione, il codice che hai scritto richiede più risorse " \
                                 "di quelle che hai segnato come limite massimo!</span>"

        if errors:
            confermation_text += "<br><br><span style=\" color: red;\">" \
                                 "Attenzione, il tuo codice ha degli errori e non viene eseguito interamente!</span>"

        ok_text = 'Invia comunque' if errors or not self.resources_correct else 'Invia'
        confirm = ConfirmWindow("Creazione di un nuovo esercizio", confermation_text, parent=self,
                                ok=ok_text, cancel='Annulla')

        if confirm.exec_() == QDialog.Accepted:
            date = self.get_selected_day().split('/')[2] + "-" + self.get_selected_day().split('/')[1] + "-" \
                   + self.get_selected_day().split('/')[0]
            title = self.title_widget.text().strip()
            text = self.text_exercise.toPlainText().strip()
            if self.order_by.currentIndex() == 1:
                text += "\n\n\n(Classifica per numero di righe utilizzate)"
            elif self.order_by.currentIndex() == 2:
                text += "\n\n\n(Classifica per numero di variabili utilizzate)"
            elif self.order_by.currentIndex() == 3:
                text += "\n\n\n(Classifica per numero di condizioni utilizzate)"
            elif self.order_by.currentIndex() == 4:
                text += "\n\n\n(Classifica per numero di cicli utilizzati)"
            level = '1' if self.difficulty == 'Facile' else ('2' if self.difficulty == 'Medio' else '3')
            white_paper_mode = '1' if self.white_paper_mode else '0'
            start_code = self.code_editor.toPlainText()
            try:
                line_limit = int(self.line_limit_form.text())
            except ValueError:
                line_limit = None
            try:
                variables_limit = int(self.variables_limit_form.text())
            except ValueError:
                variables_limit = None
            try:
                if_limit = int(self.if_limit_form.text())
            except ValueError:
                if_limit = None
            try:
                elif_limit = int(self.elif_limit_form.text())
            except ValueError:
                elif_limit = None
            try:
                else_limit = int(self.else_limit_form.text())
            except ValueError:
                else_limit = None
            try:
                conditions_limit = int(self.conditions_limit_form.text())
            except ValueError:
                conditions_limit = None
            try:
                for_limit = int(self.for_limit_form.text())
            except ValueError:
                for_limit = None
            try:
                while_limit = int(self.while_limit_form.text())
            except ValueError:
                while_limit = None
            try:
                cycles_limit = int(self.cycles_limit_form.text())
            except ValueError:
                cycles_limit = None
            try:
                functions_limit = int(self.functions_limit_form.text())
            except ValueError:
                functions_limit = None
            limits = str(line_limit) + ',' + str(variables_limit) + ',' + str(if_limit) + ',' + str(elif_limit) + ',' \
                     + str(else_limit) + ',' + str(conditions_limit) + ',' + str(for_limit) + ',' + str(while_limit) \
                     + ',' + str(cycles_limit) + ',' + str(functions_limit)
            executable = '1' if self.executable_check.isChecked() else '0'
            lookable = '1' if self.lookable_check.isChecked() else '0'

            try:
                r = requests.post("http://programmingisagame.netsons.org/add_exercise.php",
                                  data={'username': self.data.my_name, 'password': self.data.my_psw,
                                        'class': self.data.my_class, 'date': date, 'title': title, 'text': text,
                                        'level': level, 'white_paper_mode': white_paper_mode, 'start_code': start_code,
                                        'limits': limits, 'executable': executable,
                                        'order': self.order_by.currentIndex(), 'lookable': lookable})
                if r.text != "":
                    self.closer_controller.close_CreateHomeworkWindow()
            except requests.exceptions.RequestException as e:
                confirm2 = ConfirmWindow('Errore di connessione',
                                        "<span style=\" color: red;\"> Attenzione, si sono verificati problemi di "
                                        "connessione<br>Controllare la propria connessione internet e riprovare</span>",
                                        ok="Ok", cancel=None)
                if confirm2.exec_() == QDialog.Accepted:
                    print('ok')
                confirm2.deleteLater()
        confirm.deleteLater()

    def set_text_font_size(self, num):
        font = QFont()
        font.setPixelSize(num)
        self.code_editor.setFont(font)
        self.results.setFont(font)
        self.numbers.setFont(font)
        self.text_exercise.setFont(font)

    @staticmethod
    def my_find_and_replace(text, word, new_word, replace):
        new_text = ""
        count = 0
        pos = re.search(r'\b(' + word + r')\b', text)
        while pos is not None:
            count += 1
            if replace:
                new_text += text[0: pos.start()] + new_word
                text = text[pos.start() + len(word): len(text)]
                pos = re.search(r'\b(' + word + r')\b', text)
        new_text += text
        return new_text, count

    def color_strings(self, text):
        texts = []
        multi_line_comment, comment, string_start, i, start = False, False, None, 0, 0
        while i < len(text):
            if text[i] == '#' and string_start is None and not multi_line_comment and not comment:
                if i != start:
                    texts.append(text[start:i])
                    start = i

                text = text[0:i] + '<span style=\" color:' + self.data.color_styles.comment_color \
                       + ';\">' + text[i:len(text)]
                i += len('<span style=\" color:' + self.data.color_styles.comment_color + ';\">')
                comment = True
            elif (text[i] == '"' or text[i] == "'") and comment is False:
                if string_start is None:
                    if i + 2 < len(text) and text[i + 1] == text[i] and text[i + 2] == text[i]:
                        if i != start:
                            texts.append(text[start:i])
                            start = i
                        text = text[0:i] + '<span style=\" color:' + self.data.color_styles.multi_line_comment_color \
                               + ';\">' + text[i:len(text)]
                        i += len('<span style=\" color:' + self.data.color_styles.multi_line_comment_color + ';\">') + 2
                        multi_line_comment = True
                        string_start = text[i]
                    elif not multi_line_comment:
                        if i != start:
                            texts.append(text[start:i])
                            start = i
                        text = text[0:i] + '<span style=\" color:' + self.data.color_styles.string_color \
                               + ';\">' + text[i:len(text)]
                        i += len('<span style=\" color:' + self.data.color_styles.string_color + ';\">')
                        string_start = text[i]
                elif text[i] == string_start:
                    if multi_line_comment and i + 2 < len(text) and text[i + 1] == text[i] and text[i + 2] == text[i]:
                        text = text[0:i + 3] + '</span>' + text[i + 3:len(text)]
                        i += len('</span>') + 2
                        texts.append(text[start:i + 1])
                        start = i + 1
                        multi_line_comment = False
                        string_start = None
                    elif not multi_line_comment:
                        text = text[0:i + 1] + '</span>' + text[i + 1:len(text)]
                        i += len('</span>')
                        texts.append(text[start:i + 1])
                        start = i + 1
                        string_start = None
            elif text[i] == '\n' and not multi_line_comment:
                if comment:
                    text = text[0:i] + '</span>' + text[i:len(text)]
                    i += len('</span>')
                    texts.append(text[start:i + 1])
                    start = i + 1
                    comment = False
                elif string_start is not None:
                    text = text[0:i] + '</span>' + text[i:len(text)]
                    i += len('</span>')
                    texts.append(text[start:i + 1])
                    start = i + 1
                    string_start = None
            elif text[i] == '<':
                text = text[0:i] + '&#60;' + text[i + 1:len(text)]
                i += 4
            elif text[i] == '>':
                text = text[0:i] + '&#62;' + text[i + 1:len(text)]
                i += 4
            i += 1
        texts.append(text[start:i])
        return texts

    def update_function_counters(self):
        self.resources_correct = True
        text = self.line_limit_form.text()
        if text != '':
            try:
                if int(text) > 500:
                    self.line_limit_form.setText('500')
                    text = '500'
                if int(text) < len(self.numbers.toPlainText().split('\n')):
                    self.line_limit_form.setStyleSheet("QWidget {color: red}")
                    self.resources_correct = False
                else:
                    self.line_limit_form.setStyleSheet("QWidget {color: black}")
            except ValueError:
                self.line_limit_form.setStyleSheet("QWidget {color: red}")
                self.resources_correct = False
        else:
            self.line_limit_form.setStyleSheet("QWidget {color: black}")

        text = self.variables_limit_form.text()
        if text != '':
            try:
                if int(text) > 100:
                    self.variables_limit_form.setText('100')
                    text = '100'
                if int(text) < len(self.temp_vars):
                    self.variables_limit_form.setStyleSheet("QWidget {color: red}")
                    self.resources_correct = False
                else:
                    self.variables_limit_form.setStyleSheet("QWidget {color: black}")
            except ValueError:
                self.variables_limit_form.setStyleSheet("QWidget {color: red}")
                self.resources_correct = False
        else:
            self.variables_limit_form.setStyleSheet("QWidget {color: black}")

        conditions_limit = None
        try:
            self.conditions_limit_form.setText(str(int(self.if_limit_form.text()) + int(self.elif_limit_form.text())
                                                   + int(self.else_limit_form.text())))
            self.conditions_limit_form.setEnabled(False)
        except ValueError:
            if not self.conditions_limit_form.isEnabled():
                self.conditions_limit_form.setEnabled(True)
                self.conditions_limit_form.setText('')
            text = self.conditions_limit_form.text()
            if text != '':
                try:
                    if int(text) > 300:
                        self.conditions_limit_form.setText('300')
                        text = '300'
                    conditions_limit = int(text)
                    if int(text) < self.functions['if'] + self.functions['elif'] + self.functions['else']:
                        self.conditions_limit_form.setStyleSheet("QWidget {color: red}")
                        self.resources_correct = False
                    else:
                        self.conditions_limit_form.setStyleSheet("QWidget {color: black}")
                except ValueError:
                    self.conditions_limit_form.setStyleSheet("QWidget {color: red}")
                    self.resources_correct = False
            else:
                self.conditions_limit_form.setStyleSheet("QWidget {color: black}")

        if_limit = None
        text = self.if_limit_form.text()
        if text != '':
            try:
                if int(text) > 100:
                    self.if_limit_form.setText('100')
                    text = '100'
                if_limit = int(text)
                if int(text) < self.functions['if']:
                    self.if_limit_form.setStyleSheet("QWidget {color: red}")
                    self.resources_correct = False
                else:
                    self.if_limit_form.setStyleSheet("QWidget {color: black}")
            except ValueError:
                self.if_limit_form.setStyleSheet("QWidget {color: red}")
                self.resources_correct = False
        else:
            self.if_limit_form.setStyleSheet("QWidget {color: black}")

        elif_limit = None
        text = self.elif_limit_form.text()
        if text != '':
            try:
                if int(text) > 100:
                    self.elif_limit_form.setText('100')
                    text = '100'
                elif_limit = int(text)
                if int(text) < self.functions['elif']:
                    self.elif_limit_form.setStyleSheet("QWidget {color: red}")
                    self.resources_correct = False
                else:
                    self.elif_limit_form.setStyleSheet("QWidget {color: black}")
            except ValueError:
                self.elif_limit_form.setStyleSheet("QWidget {color: red}")
                self.resources_correct = False
        else:
            self.elif_limit_form.setStyleSheet("QWidget {color: black}")

        else_limit = None
        text = self.else_limit_form.text()
        if text != '':
            try:
                if int(text) > 100:
                    self.else_limit_form.setText('100')
                    text = '100'
                else_limit = int(text)
                if int(text) < self.functions['else']:
                    self.else_limit_form.setStyleSheet("QWidget {color: red}")
                    self.resources_correct = False
                else:
                    self.else_limit_form.setStyleSheet("QWidget {color: black}")
            except ValueError:
                self.else_limit_form.setStyleSheet("QWidget {color: red}")
                self.resources_correct = False
        else:
            self.else_limit_form.setStyleSheet("QWidget {color: black}")

        sum = 0
        if if_limit is not None:
            sum += if_limit
        if elif_limit is not None:
            sum += elif_limit
        if else_limit is not None:
            sum += else_limit
        if conditions_limit is not None and sum > conditions_limit:
            if if_limit is not None:
                self.if_limit_form.setStyleSheet("QWidget {color: red}")
                self.resources_correct = False
            if elif_limit is not None:
                self.elif_limit_form.setStyleSheet("QWidget {color: red}")
                self.resources_correct = False
            if else_limit is not None:
                self.else_limit_form.setStyleSheet("QWidget {color: red}")
                self.resources_correct = False

        cycles_limit = None
        try:
            self.cycles_limit_form.setText(str(int(self.for_limit_form.text()) + int(self.while_limit_form.text())))
            self.cycles_limit_form.setEnabled(False)
        except ValueError:
            if not self.cycles_limit_form.isEnabled():
                self.cycles_limit_form.setEnabled(True)
                self.cycles_limit_form.setText('')
            text = self.cycles_limit_form.text()
            if text != '':
                try:
                    if int(text) > 200:
                        self.cycles_limit_form.setText('200')
                        text = '200'
                    cycles_limit = int(text)
                    if int(text) < self.functions['for'] + self.functions['while']:
                        self.cycles_limit_form.setStyleSheet("QWidget {color: red}")
                        self.resources_correct = False
                    else:
                        self.cycles_limit_form.setStyleSheet("QWidget {color: black}")
                except ValueError:
                    self.cycles_limit_form.setStyleSheet("QWidget {color: red}")
                    self.resources_correct = False
            else:
                self.cycles_limit_form.setStyleSheet("QWidget {color: black}")

        for_limit = None
        text = self.for_limit_form.text()
        if text != '':
            try:
                if int(text) > 100:
                    self.for_limit_form.setText('100')
                    text = '100'
                for_limit = int(text)
                if int(text) < self.functions['for']:
                    self.for_limit_form.setStyleSheet("QWidget {color: red}")
                    self.resources_correct = False
                else:
                    self.for_limit_form.setStyleSheet("QWidget {color: black}")
            except ValueError:
                self.for_limit_form.setStyleSheet("QWidget {color: red}")
                self.resources_correct = False
        else:
            self.for_limit_form.setStyleSheet("QWidget {color: black}")

        while_limit = None
        text = self.while_limit_form.text()
        if text != '':
            try:
                if int(text) > 100:
                    self.while_limit_form.setText('100')
                    text = '100'
                while_limit = int(text)
                if int(text) < self.functions['while']:
                    self.while_limit_form.setStyleSheet("QWidget {color: red}")
                    self.resources_correct = False
                else:
                    self.while_limit_form.setStyleSheet("QWidget {color: black}")
            except ValueError:
                self.while_limit_form.setStyleSheet("QWidget {color: red}")
                self.resources_correct = False
        else:
            self.while_limit_form.setStyleSheet("QWidget {color: black}")

        sum = 0
        if for_limit is not None:
            sum += for_limit
        if while_limit is not None:
            sum += while_limit
        if cycles_limit is not None and sum > cycles_limit:
            if for_limit is not None:
                self.for_limit_form.setStyleSheet("QWidget {color: red}")
                self.resources_correct = False
            if while_limit is not None:
                self.while_limit_form.setStyleSheet("QWidget {color: red}")
                self.resources_correct = False

        text = self.functions_limit_form.text()
        if text != '':
            try:
                if int(text) > 100:
                    self.functions_limit_form.setText('100')
                    text = '100'
                if int(text) < self.functions['def']:
                    self.functions_limit_form.setStyleSheet("QWidget {color: red}")
                    self.resources_correct = False
                else:
                    self.functions_limit_form.setStyleSheet("QWidget {color: black}")
            except ValueError:
                self.functions_limit_form.setStyleSheet("QWidget {color: red}")
                self.resources_correct = False
        else:
            self.functions_limit_form.setStyleSheet("QWidget {color: black}")

    def format_text(self):
        if self.text_changed:
            self.text_changed = False
            text = self.code_editor.toPlainText()
            self.functions = {
                'if': 0,
                'elif': 0,
                'else': 0,
                'for': 0,
                'while': 0,
                'def': 0
            }

            if text is '':
                self.update_rows_number()
                self.text_changed = True
                self.update_function_counters()
                return

            code_editor_cursor = self.code_editor.textCursor()
            x_cur, y_cur = code_editor_cursor.blockNumber(), code_editor_cursor.columnNumber()
            x_bar, y_bar = self.code_editor.verticalScrollBar().value(), self.code_editor.horizontalScrollBar().value()

            temp_text = text
            texts = self.color_strings(text)
            text = ''
            for i in range(0, len(texts)):
                if texts[i] != '' and texts[i][0] != '<':
                    for word in self.data.color_styles.keyWords:
                        texts[i], num = self.my_find_and_replace(texts[i], word.word, word.tagged_word(), True)
                        if self.functions.get(word.word, None) is not None:
                            self.functions[word.word] = self.functions[word.word] + num
                text += texts[i]
            if self.white_paper_mode:
                text = temp_text
            if text[0] == '\n':
                text = ' ' + text
            if text[-1] == '\n':
                text = text + ' '
            text = '<pre>' + text + '</pre>'
            self.code_editor.setText(text)

            code_editor_cursor.movePosition(QTextCursor.Start)
            while code_editor_cursor.blockNumber() < x_cur:
                code_editor_cursor.movePosition(QTextCursor.Down)
            while code_editor_cursor.columnNumber() < y_cur:
                code_editor_cursor.movePosition(QTextCursor.Right)
            self.code_editor.setTextCursor(code_editor_cursor)
            self.code_editor.verticalScrollBar().setValue(x_bar)
            self.code_editor.horizontalScrollBar().setValue(y_bar)

            self.update_rows_number()
            self.update_function_counters()
        self.text_changed = True

    def update_rows_number(self):
        old_value = self.numbers.verticalScrollBar().value()
        rows = ''
        i = 0
        for i in range(0, len(self.code_editor.toPlainText().split('\n'))):
            rows += str(i + 1) + '\n'
        rows = rows[0: -1]
        i += 1
        c = 1
        while i / 10 >= 1:
            c += 1
            i = i / 10
        self.numbers.setText('<pre>' + rows + '</pre>')
        self.numbers.verticalScrollBar().setValue(old_value)
        self.numbers.setFixedWidth(c * self.data.code_font_size * 2 / 3 + 10)

    def scroll_numbers(self):
        self.numbers.verticalScrollBar().setValue(self.code_editor.verticalScrollBar().value())


class MyCalendar(QCalendarWidget):
    def __init__(self, parent=None):
        QCalendarWidget.__init__(self, parent)

    def paintCell(self, painter, rect, date, **kwargs):
        QCalendarWidget.paintCell(self, painter, rect, date)
        if date == self.selectedDate():
            painter.drawText(rect.bottomLeft(), "   ------")
