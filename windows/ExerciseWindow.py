import datetime
import re
import contextlib
import io
from functools import partial

from PyQt5.QtGui import QTextCursor, QFont
from PyQt5.QtWidgets import QWidget, QTextEdit, QPlainTextEdit, QPushButton, QSplitter, QHBoxLayout, QVBoxLayout, \
    QFrame, QLabel
from PyQt5.QtCore import *


class ExerciseWindow(QWidget):
    def __init__(self, exercise, data, closer_controller):
        super(ExerciseWindow, self).__init__(flags=Qt.Window)
        self.setMinimumSize(QSize(800, 400))
        self.setWindowTitle('Gamification - "' + exercise.title + '" by ' + exercise.creator)
        self.exercise = exercise
        self.data = data
        self.closer_controller = closer_controller
        self.text_changed = True
        self.more_options_is_visible = False

        play_option_widget = QWidget(self, flags=Qt.Widget)
        play_option_widget.setLayout(self.get_play_option_widget())
        play_option_widget.setFixedHeight(130)
        play_option_widget.setContentsMargins(0, 0, 0, 0)
        play_option_widget.setObjectName("play_option_widget")
        play_option_widget.setStyleSheet("QWidget#play_option_widget "
                                         "{border: 0px solid grey; border-bottom: 1px solid grey}")

        counter_functions_widget = QWidget(self, flags=Qt.Widget)
        counter_functions_widget.setLayout(self.get_counter_functions_layout())
        #counter_functions_widget.setObjectName("widget1")
        #counter_functions_widget.setStyleSheet("QWidget#widget1 {border: 1px solid grey}")

        self.text_exercise = QPlainTextEdit(self)
        self.text_exercise.setReadOnly(True)
        self.text_exercise.hide() if exercise.text is None else self.text_exercise.setPlainText(exercise.text)

        self.numbers = QTextEdit(self)
        self.numbers.setReadOnly(True)
        self.numbers.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.numbers.setFixedWidth(50)

        self.code_editor = QTextEdit(self)
        self.code_editor.setLineWrapMode(self.code_editor.NoWrap)
        self.code_editor.textChanged.connect(self.format_text)
        self.code_editor.verticalScrollBar().valueChanged.connect(self.scroll_numbers)
        self.code_editor.setText(self.exercise.start_code if self.exercise.solution is None else self.exercise.solution)
        if self.exercise.delivery_date is not None:
            self.code_editor.setReadOnly(True)

        self.results = QPlainTextEdit(self)
        self.results.setReadOnly(True)
        self.results.setLineWrapMode(self.results.NoWrap)
        if not self.exercise.executable:
            self.results.hide()

        self.set_text_font_size(self.data.code_font_size)

        box = QVBoxLayout(self)
        box.addWidget(play_option_widget)
        box.addWidget(counter_functions_widget)
        box.setContentsMargins(0, 0, 0, 0)
        widget1 = QWidget(self, flags=Qt.Widget)
        widget1.setLayout(box)
        widget1.setFixedWidth(250)
        widget1.setContentsMargins(0, 0, 0, 0)
        widget1.setObjectName("play_option_counter_functions_widgets")
        widget1.setStyleSheet("QWidget#play_option_counter_functions_widgets "
                              "{border: 0px solid grey; border-right: 1px solid grey}")

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

        splitter2 =QSplitter(Qt.Vertical)
        splitter2.addWidget(self.text_exercise)
        splitter2.addWidget(self.coding_widget)
        splitter2.setSizes([100, 500])
        splitter2.setChildrenCollapsible(False)
        splitter2.setContentsMargins(0, 10, 10, 10)

        box = QHBoxLayout(self)
        box.addWidget(widget1)
        box.addWidget(splitter2)
        box.setContentsMargins(0, 0, 0, 0)

    def get_play_option_widget(self):
        play_button = QPushButton('PLAY', self)
        play_button.setFixedSize(50, 50)
        play_button.clicked.connect(self.play_button_on_click)
        if not self.exercise.executable:
            play_button.setEnabled(False)
        else:
            play_button.setStyleSheet('background-color:green')

        self.save_button = QPushButton('Save', self)
        self.save_button.setFixedSize(50, 50)
        self.save_button.clicked.connect(self.save_button_on_click)
        self.save_button.setStyleSheet('background-color:green')

        more_button = QPushButton(' ... ', self)
        more_button.setFixedSize(50, 50)
        more_button.clicked.connect(self.more_button_on_click)

        if self.exercise.delivery_date is not None:
            self.save_button.hide()
            more_button.hide()

        swap_button = QPushButton('Swap', self)
        swap_button.setFixedSize(50, 50)
        swap_button.clicked.connect(self.swap_button_on_click)

        send_button = QPushButton('Send', self)
        send_button.setFixedSize(50, 50)
        send_button.clicked.connect(self.send_button_on_click)

        restart_button = QPushButton('Restart', self)
        restart_button.setFixedSize(50, 50)
        restart_button.clicked.connect(self.restart_button_on_click)

        box1 = QHBoxLayout(self)
        box1.setContentsMargins(0, 0, 0, 0)
        box1.addWidget(play_button)
        box1.addWidget(self.save_button)
        box1.addWidget(more_button)

        box2 = QHBoxLayout(self)
        box2.setContentsMargins(0, 0, 0, 0)
        box2.addWidget(swap_button)
        box2.addWidget(send_button)
        box2.addWidget(restart_button)

        widget1 = QWidget(self, flags=Qt.Widget)
        widget1.setLayout(box1)
        self.more_options = QWidget(self, flags=Qt.Widget)
        self.more_options.setLayout(box2)
        self.more_options.hide()
        box = QVBoxLayout(self)
        box.setContentsMargins(0, 0, 0, 0)
        box.addWidget(widget1)
        box.addWidget(self.more_options)
        return box

    def play_button_on_click(self):
        temp_vars = {}
        try:
            stream = io.StringIO()
            with contextlib.redirect_stdout(stream):
                exec(self.code_editor.toPlainText(), globals(), temp_vars)
            result = stream.getvalue()
        except Exception as E:
            result = str(E)
        self.results.setPlainText(result)

    def save_button_on_click(self):
        self.exercise.solution = self.code_editor.toPlainText()
        self.data.save_exercise(self.exercise)
        self.save_button.setStyleSheet('background-color:green')
        self.closer_controller.update()

    def more_button_on_click(self):
        if self.more_options_is_visible:
            self.more_options.hide()
        else:
            self.more_options.show()
        self.more_options_is_visible = not self.more_options_is_visible
        return

    def swap_button_on_click(self):
        # ToDo
        return

    def send_button_on_click(self):
        self.exercise.solution = self.code_editor.toPlainText()
        self.exercise.delivery_date = datetime.datetime.now()
        self.data.send_exercise(self.exercise)
        self.closer_controller.close_ExerciseWindow(self.exercise)

    def restart_button_on_click(self):
        self.code_editor.setText(self.exercise.start_code)
        self.results.setPlainText('')

    def create_label(self, text):
        label = QLabel(self)
        label.setText(text)
        label.setMargin(10)
        return label

    def get_counter_functions_layout(self):
        intro_variables = self.create_label("Variabili ")
        intro_if = self.create_label("if")
        intro_elif = self.create_label("elif")
        intro_else = self.create_label("else")
        intro_conditions = self.create_label("Conditions ")
        self.variables_number = self.create_label('20')
        self.if_number = self.create_label('5')
        self.elif_number = self.create_label('0')
        self.else_number = self.create_label('0')
        self.conditions_number = self.create_label('5')

        box = QHBoxLayout(self)
        box.setContentsMargins(0, 0, 0, 0)
        box.addWidget(intro_variables)
        box.addWidget(self.variables_number)
        variables_widget = QWidget(self, flags=Qt.Widget)
        variables_widget.setLayout(box)
        variables_widget.setObjectName("variables_widget")
        variables_widget.setStyleSheet("QWidget#variables_widget {border: 1px solid grey}")

        box = QHBoxLayout(self)
        box.addWidget(intro_if)
        box.addWidget(self.if_number)
        box.setContentsMargins(0, 0, 0, 0)
        if_widget = QWidget(self, flags=Qt.Widget)
        if_widget.setLayout(box)

        box = QHBoxLayout(self)
        box.addWidget(intro_elif)
        box.addWidget(self.elif_number)
        box.setContentsMargins(0, 0, 0, 0)
        elif_widget = QWidget(self, flags=Qt.Widget)
        elif_widget.setLayout(box)

        box = QHBoxLayout(self)
        box.addWidget(intro_else)
        box.addWidget(self.else_number)
        box.setContentsMargins(0, 0, 0, 0)
        else_widget = QWidget(self, flags=Qt.Widget)
        else_widget.setLayout(box)

        box = QHBoxLayout(self)
        box.addWidget(intro_else)
        box.addWidget(self.else_number)
        box.setContentsMargins(0, 0, 0, 0)
        else_widget = QWidget(self, flags=Qt.Widget)
        else_widget.setLayout(box)

        box = QHBoxLayout(self)
        box.setContentsMargins(0, 0, 0, 0)
        box.addWidget(intro_conditions)
        box.addWidget(self.conditions_number)
        conditions_widget = QWidget(self, flags=Qt.Widget)
        conditions_widget.setLayout(box)

        box = QVBoxLayout(self)
        box.setSpacing(0)
        box.setContentsMargins(0, 0, 0, 0)
        box.addWidget(if_widget)
        box.addWidget(elif_widget)
        box.addWidget(else_widget)
        box.addWidget(conditions_widget)
        conditions_widget = QWidget(self, flags=Qt.Widget)
        conditions_widget.setLayout(box)
        conditions_widget.setObjectName("conditions_widget")
        conditions_widget.setStyleSheet("QWidget#conditions_widget {border: 1px solid grey}")

        box = QVBoxLayout(self)
        box.setAlignment(Qt.AlignTop)
        box.addWidget(variables_widget)
        box.addWidget(conditions_widget)

        return box

    def set_text_font_size(self, num):
        font = QFont()
        font.setPixelSize(num)
        self.code_editor.setFont(font)
        self.results.setFont(font)
        self.numbers.setFont(font)
        self.text_exercise.setFont(font)

    @staticmethod
    def my_replace(text, word, new_word):
        new_text = ""
        pos = re.search(r'\b(' + word + r')\b', text)
        while pos is not None:
            new_text += text[0: pos.start()] + new_word
            text = text[pos.start() + len(word): len(text)]
            pos = re.search(r'\b(' + word + r')\b', text)
        new_text += text
        return new_text

    def color_strings(self, text):
        texts = []
        multi_line_comment, comment, string_start, i, start = False, False, None, 0, 0
        while i < len(text):
            if text[i] == '#' and string_start is None and not multi_line_comment and not comment:
                if i != start:
                    texts.append(text[start:i])
                    start = i
                text = text[0:i] + self.exercise.color_styles.comment_tag_start + text[i:len(text)]
                i += len(self.exercise.color_styles.comment_tag_start)
                comment = True
            elif (text[i] == '"' or text[i] == "'") and comment is False:
                if string_start is None:
                    if i + 2 < len(text) and text[i + 1] == text[i] and text[i + 2] == text[i]:
                        if i != start:
                            texts.append(text[start:i])
                            start = i
                        text = text[0:i] + self.exercise.color_styles.multi_line_comment_tag_start + text[i:len(text)]
                        i += len(self.exercise.color_styles.multi_line_comment_tag_start) + 2
                        multi_line_comment = True
                        string_start = text[i]
                    elif not multi_line_comment:
                        if i != start:
                            texts.append(text[start:i])
                            start = i
                        text = text[0:i] + self.exercise.color_styles.string_tag_start + text[i:len(text)]
                        i += len(self.exercise.color_styles.string_tag_start)
                        string_start = text[i]
                elif text[i] == string_start:
                    if multi_line_comment and i + 2 < len(text) and text[i + 1] == text[i] and text[i + 2] == text[i]:
                        text = text[0:i + 3] + self.exercise.color_styles.multi_line_comment_tag_end \
                               + text[i + 3:len(text)]
                        i += len(self.exercise.color_styles.multi_line_comment_tag_end) + 2
                        texts.append(text[start:i + 1])
                        start = i + 1
                        multi_line_comment = False
                        string_start = None
                    elif not multi_line_comment:
                        text = text[0:i + 1] + self.exercise.color_styles.string_tag_end + text[i + 1:len(text)]
                        i += len(self.exercise.color_styles.string_tag_end)
                        texts.append(text[start:i + 1])
                        start = i + 1
                        string_start = None
            elif text[i] == '\n' and not multi_line_comment:
                if comment:
                    text = text[0:i] + self.exercise.color_styles.comment_tag_end + text[i:len(text)]
                    i += len(self.exercise.color_styles.comment_tag_end)
                    texts.append(text[start:i + 1])
                    start = i + 1
                    comment = False
                elif string_start is not None:
                    text = text[0:i] + self.exercise.color_styles.string_tag_end + text[i:len(text)]
                    i += len(self.exercise.color_styles.string_tag_end)
                    texts.append(text[start:i + 1])
                    start = i + 1
                    string_start = None
            elif text[i] == '<':  # < da sostituire con &#60
                text = text[0:i] + '&#60;' + text[i + 1:len(text)]
                i += 4
            elif text[i] == '>':  # > da sostituire con &#62
                text = text[0:i] + '&#62;' + text[i + 1:len(text)]
                i += 4
            i += 1
        texts.append(text[start:i])
        return texts

    def format_text(self):
        if self.text_changed:
            self.text_changed = False

            text = self.code_editor.toPlainText()
            if text != self.exercise.solution:
                self.save_button.setStyleSheet('background-color:yellow')
            else:
                self.save_button.setStyleSheet('background-color:green')
            if text is '':
                self.update_rows_number()
                self.text_changed = True
                return
            if (self.exercise.line_limit is not None) and len(text.split('\n')) > self.exercise.line_limit:
                self.code_editor.undo()
                self.text_changed = True
                return

            code_editor_cursor = self.code_editor.textCursor()
            x_cur, y_cur = code_editor_cursor.blockNumber(), code_editor_cursor.columnNumber()
            x_bar, y_bar = self.code_editor.verticalScrollBar().value(), self.code_editor.horizontalScrollBar().value()

            if not self.exercise.white_paper_mode:
                texts = self.color_strings(text)
                text = ''
                for i in range(0, len(texts)):
                    if texts[i] != '' and texts[i][0] != '<':
                        for word in self.exercise.color_styles.keyWords:
                            texts[i] = self.my_replace(texts[i], word.word, word.tagged_word())
                    text += texts[i]
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
