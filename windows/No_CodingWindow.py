import re
import contextlib
import io
from functools import partial

from PyQt5.QtGui import QTextCursor, QFont
from PyQt5.QtWidgets import QWidget, QMainWindow, QTextEdit, QPlainTextEdit, QPushButton, QSplitter, QHBoxLayout, QVBoxLayout, \
    QFrame
from PyQt5.QtCore import *


# Schermata si pogrammazione
class CodingWindow(QWidget):
    '''
    editor_mode = False
    text_font_size = 10
    fixed_line_number = None
    horizontal_code_result_position = True
    '''

    def __init__(self, exercise):
        super(CodingWindow, self).__init__(flags=Qt.Window)
        self.setMinimumSize(QSize(800, 400))
        self.setWindowTitle("Gamification")
        self.exercise = exercise

        box = QHBoxLayout(self)
        self.make_main_widget()
        box.addWidget(self.exercise_code_box)

        #self.text_changed = True
        #self.set_text_font_size(20)

    '''
    def make_top_widget(self):
        self.home_button = QPushButton('HOME', self)
        self.home_button.setFixedSize(50, 50)
        self.home_button.clicked.connect(self.controller.open_MainWindow)

        self.pos_code_result_button = QPushButton('Swap', self)
        self.pos_code_result_button.setFixedSize(50, 50)
        self.pos_code_result_button.clicked.connect(self.change_code_result_orientation)

        self.exercises_widget = QWidget(self, flags=Qt.Widget)
        self.exercises_box = QHBoxLayout(self)
        self.exercises_box.setAlignment(Qt.AlignHCenter)
        self.exercises_box.setContentsMargins(10, 10, 10, 10)
        self.exercise_buttons = []
        for i in self.data.exercises:
            button = button_exercise_area()
            button.make(i, self)
            self.exercises_box.addWidget(button.get_widget())
            self.exercise_buttons.append(button)
        self.exercises_widget.setLayout(self.exercises_box)

        self.top_widget = QWidget(self, flags=Qt.Widget)
        self.top_box = QHBoxLayout(self)
        self.top_box.addWidget(self.home_button)
        self.top_box.addWidget(self.pos_code_result_button)
        self.top_box.addWidget(self.exercises_widget)
        self.top_widget.setLayout(self.top_box)
        self.top_widget.setObjectName("topStyle")
        self.top_widget.setStyleSheet("QWidget#topStyle {border: 0px solid grey; border-bottom: 1px solid grey}")
        #self.top_widget.setFixedHeight(70)
    '''

    def make_main_widget(self):
        self.numbers = QTextEdit(self)
        self.numbers.setReadOnly(True)
        self.numbers.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.code_editor = QTextEdit(self)
        self.code_editor.setLineWrapMode(self.code_editor.NoWrap)
        self.code_editor.textChanged.connect(self.format_text)
        self.code_editor.verticalScrollBar().valueChanged.connect(self.scroll_numbers)
        self.code_editor.setText(self.exercise.start_code if self.exercise.solution is None else self.exercise.solution)

        self.code_text_box_widget = QWidget(self, flags=Qt.Widget)
        self.code_text_box = QHBoxLayout(self)
        self.code_text_box.setSpacing(0)
        self.code_text_box.setContentsMargins(0, 0, 0, 0)
        self.code_text_box.addWidget(self.numbers, alignment=Qt.AlignLeft)
        self.code_text_box.addWidget(self.code_editor, alignment=Qt.AlignLeading)
        self.code_text_box_widget.setLayout(self.code_text_box)

        self.results = QPlainTextEdit(self)
        self.results.setReadOnly(True)
        self.results.setLineWrapMode(self.results.NoWrap)

        self.code_box_widget = QSplitter()
        if self.horizontal_code_result_position:
            self.code_box_widget.setOrientation(Qt.Horizontal)
        else:
            self.code_box_widget.setOrientation(Qt.Vertical)
        self.code_box_widget.addWidget(self.code_text_box_widget)
        self.code_box_widget.addWidget(self.results)
        self.code_box_widget.setSizes([100, 100])
        self.code_box_widget.setChildrenCollapsible(False)

        self.text_exercise = QPlainTextEdit(self)
        self.text_exercise.setReadOnly(True)

        frame = QFrame()
        frame.setFrameShape(QFrame.StyledPanel)
        frame.setFixedWidth(250)

        self.text_exercise_box = QWidget(self, flags=Qt.Widget)
        text_exercise_layout = QHBoxLayout(self)
        text_exercise_layout.addWidget(frame)
        text_exercise_layout.addWidget(self.text_exercise)
        text_exercise_layout.setContentsMargins(10,10,10,0)
        self.text_exercise_box.setLayout(text_exercise_layout)

        frame = QFrame()
        frame.setFrameShape(QFrame.StyledPanel)
        frame.setFixedWidth(150)

        bottom_widget = QWidget(self, flags=Qt.Widget)
        bottom_box = QHBoxLayout(self)
        bottom_box.addWidget(frame)
        bottom_box.addWidget(self.code_box_widget)
        bottom_box.setContentsMargins(10,5,10,10)
        bottom_widget.setLayout(bottom_box)

        self.exercise_code_box = QSplitter(Qt.Vertical)
        self.exercise_code_box.addWidget(self.text_exercise_box)
        self.exercise_code_box.addWidget(bottom_widget)
        self.exercise_code_box.setSizes([100, 200])
        self.exercise_code_box.setChildrenCollapsible(False)
        self.text_exercise_box.hide()

    def execute_code_button_on_click(self):
        temp_vars = {}
        try:
            stream = io.StringIO()
            with contextlib.redirect_stdout(stream):
                exec(self.code_editor.toPlainText(), globals(), temp_vars)
            result = stream.getvalue()
        except Exception as E:
            result = str(E)
        self.results.setPlainText(result)

    # funzione "migliorata" del raplace (se parola da modificare è ciao, non si modifica ciaone)
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
                text = text[0:i] + self.data.comment_tag_start + text[i:len(text)]
                i += len(self.data.comment_tag_start)
                comment = True
            elif (text[i] == '"' or text[i] == "'") and comment is False:
                if string_start is None:
                    if i + 2 < len(text) and text[i + 1] == text[i] and text[i + 2] == text[i]:
                        if i != start:
                            texts.append(text[start:i])
                            start = i
                        text = text[0:i] + self.data.multi_line_comment_tag_start + text[i:len(text)]
                        i += len(self.data.multi_line_comment_tag_start) + 2
                        multi_line_comment = True
                        string_start = text[i]
                    elif not multi_line_comment:
                        if i != start:
                            texts.append(text[start:i])
                            start = i
                        text = text[0:i] + self.data.string_tag_start + text[i:len(text)]
                        i += len(self.data.string_tag_start)
                        string_start = text[i]
                elif text[i] == string_start:
                    if multi_line_comment and i + 2 < len(text) and text[i + 1] == text[i] and text[i + 2] == text[i]:
                        text = text[0:i + 3] + self.data.multi_line_comment_tag_end + text[i + 3:len(text)]
                        i += len(self.data.multi_line_comment_tag_end) + 2
                        texts.append(text[start:i + 1])
                        start = i + 1
                        multi_line_comment = False
                        string_start = None
                    elif not multi_line_comment:
                        text = text[0:i + 1] + self.data.string_tag_end + text[i + 1:len(text)]
                        i += len(self.data.string_tag_end)
                        texts.append(text[start:i + 1])
                        start = i + 1
                        string_start = None
            elif text[i] == '\n' and not multi_line_comment:
                if comment:
                    text = text[0:i] + self.data.comment_tag_end + text[i:len(text)]
                    i += len(self.data.comment_tag_end)
                    texts.append(text[start:i + 1])
                    start = i + 1
                    comment = False
                elif string_start is not None:
                    text = text[0:i] + self.data.string_tag_end + text[i:len(text)]
                    i += len(self.data.string_tag_end)
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

    # Funzione che aggiunge i tag al testo chiamata e rieseguita ad ogni sua modifica
    def format_text(self):
        if self.text_changed:
            # check così che l'aggiunta dei tag venga fatta una sola volta ad ogni modifica e non all'infinito
            self.text_changed = False

            # Salvo i valori iniziali di cursore e scrollbar
            text = self.code_editor.toPlainText()
            if text is '':
                self.text_changed = True
                return
            if (self.fixed_line_number is not None) and len(text.split('\n')) > self.fixed_line_number:
                self.code_editor.undo()
                self.text_changed = True
                return
            code_editor_cursor = self.code_editor.textCursor()
            x_cur, y_cur = code_editor_cursor.blockNumber(), code_editor_cursor.columnNumber()
            x_bar, y_bar = self.code_editor.verticalScrollBar().value(), self.code_editor.horizontalScrollBar().value()

            # Aggiungo al testo i tag per colore delle funzioni e salvo il nuovo testo
            if self.editor_mode:
                texts = self.color_strings(text)
                text = ''
                for i in range(0, len(texts)):
                    if texts[i] != '' and texts[i][0] != '<':
                        for word in self.data.keyWords:
                            texts[i] = self.my_replace(texts[i], word.word, word.tagged_word())
                    text += texts[i]
            if text[0] == '\n':
                text = ' ' + text
            if text[-1] == '\n':
                text = text + ' '
            text = '<pre>' + text + '</pre>'
            self.code_editor.setText(text)

            # Riporto il cursore e le scrollbar alla posizione originale
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

    # Aggiorno numero righe
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
        self.numbers.setFixedWidth(c * self.text_font_size * 2 / 3 + 10)

    # Aggiorno numero righe
    def scroll_numbers(self):
        self.numbers.verticalScrollBar().setValue(self.code_editor.verticalScrollBar().value())

    def set_text_font_size(self, num):
        self.text_font_size = num
        font = QFont()
        font.setPixelSize(num)
        self.code_editor.setFont(font)
        self.results.setFont(font)
        self.numbers.setFont(font)
        self.text_exercise.setFont(font)

    def change_code_result_orientation(self):
        self.horizontal_code_result_position = not self.horizontal_code_result_position
        if self.horizontal_code_result_position:
            self.code_box_widget.setOrientation(Qt.Horizontal)
        else:
            self.code_box_widget.setOrientation(Qt.Vertical)

    def set_exercise(self, exercise):
        for i in self.exercise_buttons:
            if exercise.id == i.get_id():
                i.activate()
            else:
                i.disable()

        self.text_exercise_box.show()
        self.fixed_line_number = exercise.line_limit
        self.editor_mode = not exercise.white_paper_mode
        self.code_editor.setEnabled(True)
        self.code_editor.setText('<pre><span style=\" color: #000000;\">' + exercise.start_code + '</span></pre>')
        self.results.setPlainText('')
        self.text_exercise.setPlainText(exercise.text)
        if exercise.executable:
            self.results.show()
        else:
            self.results.hide()

    def restart_exercise(self, exercise):
        self.code_editor.setText('<pre><span style=\" color: #000000;\">' + exercise.start_code + '</span></pre>')
        self.results.setPlainText('')

    def deliver_exercise(self, exercise):
        for i in self.exercise_buttons:
            if exercise.id == i.get_id():
                self.data.deliver(exercise.id)
                i.deliver()
        exercise.set_solution(self.code_editor.toPlainText())
        self.code_editor.setText(' Seleziona un esercizio ')
        self.code_editor.setEnabled(False)
        self.text_exercise_box.hide()
        self.results.setPlainText('')


class button_exercise_area:
    widget = None
    exercise = None

    def make(self, exercise, windows):
        self.widget = QWidget(windows, flags=Qt.Widget)
        self.exercise = exercise
        self.top_button = QPushButton(exercise.title)
        self.top_button.setFixedSize(100, 50)
        self.top_button.clicked.connect(partial(windows.set_exercise, exercise))

        self.left_button = QPushButton('Consegna')
        self.left_button.setFixedSize(70, 40)
        self.left_button.clicked.connect(partial(windows.deliver_exercise, exercise))
        self.left_button.setStyleSheet('background-color:yellow')

        self.right_button = QPushButton('Ricomincia')
        self.right_button.setFixedSize(70, 40)
        self.right_button.clicked.connect(partial(windows.restart_exercise, exercise))
        self.right_button.setStyleSheet('background-color:yellow')

        self.widget.setContentsMargins(0, 0, 0, 0)
        self.external_box = QHBoxLayout(windows)
        self.widget.setObjectName("exerciseAreaStyle")
        self.widget.setStyleSheet('QWidget#exerciseAreaStyle {border: 0px solid grey}')
        self.external_box.setContentsMargins(0, 0, 0, 0)
        self.external_box.setAlignment(Qt.AlignLeft)
        self.external_box.addWidget(self.top_button)
        if exercise.executable:
            self.execute_code_button = QPushButton('Play')
            self.execute_code_button.setFixedSize(50, 40)
            self.execute_code_button.clicked.connect(windows.execute_code_button_on_click)
            self.execute_code_button.setStyleSheet('background-color:green')
            self.external_box.addWidget(self.execute_code_button)
        self.external_box.addWidget(self.left_button)
        self.external_box.addWidget(self.right_button)
        self.widget.setLayout(self.external_box)
        self.disable()

    def disable(self):
        self.left_button.hide()
        self.right_button.hide()
        if self.exercise.executable:
            self.execute_code_button.hide()
        self.external_box.setContentsMargins(0,0,0,0)
        self.widget.setStyleSheet('QWidget#exerciseAreaStyle {border: 0px solid grey}')
        self.top_button.setStyleSheet("background-color: red")

    def activate(self):
        self.left_button.show()
        self.right_button.show()
        if self.exercise.executable:
            self.execute_code_button.show()
        self.external_box.setContentsMargins(0,0,7,0)
        self.widget.setStyleSheet('QWidget#exerciseAreaStyle {border: 1px solid grey}')
        self.top_button.setStyleSheet("background-color: red")

    def get_id(self):
        return self.exercise.id

    def get_widget(self):
        return self.widget

    def deliver(self):
        self.widget.hide()

