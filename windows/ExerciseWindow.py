import datetime
import re
import contextlib
import io

from PyQt5.QtGui import QTextCursor, QFont
from PyQt5.QtWidgets import QWidget, QTextEdit, QPlainTextEdit, QPushButton, QSplitter, QHBoxLayout, QVBoxLayout, QLabel
from PyQt5.QtCore import *


class ExerciseWindow(QWidget):
    def __init__(self, exercise, data, closer_controller):
        super(ExerciseWindow, self).__init__(flags=Qt.Window)
        self.setMinimumSize(QSize(800, 650))
        self.setWindowTitle('Gamification - "' + exercise.title + '" by ' + exercise.creator)
        self.exercise = exercise
        self.data = data
        self.closer_controller = closer_controller
        self.text_changed = True
        self.more_options_is_visible = False

        play_option_widget = QWidget(self, flags=Qt.Widget)
        play_option_widget.setLayout(self.get_play_option_widget())
        play_option_widget.setFixedHeight(150)
        play_option_widget.setContentsMargins(0, 0, 0, 0)
        play_option_widget.setObjectName("play_option_widget")
        play_option_widget.setStyleSheet("QWidget#play_option_widget "
                                         "{border: 0px solid grey; border-bottom: 1px solid grey}")

        counter_functions_widget = QWidget(self, flags=Qt.Widget)
        counter_functions_widget.setLayout(self.get_counter_functions_layout())

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
        widget1.setFixedWidth(300)
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

        splitter2 = QSplitter(Qt.Vertical)
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
        box1.setAlignment(Qt.AlignHCenter)
        box1.setSpacing(20)
        box1.setContentsMargins(0, 0, 0, 0)
        box1.addWidget(play_button)
        box1.addWidget(self.save_button)
        box1.addWidget(more_button)

        box2 = QHBoxLayout(self)
        box2.setAlignment(Qt.AlignHCenter)
        box2.setSpacing(20)
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
        box.setAlignment(Qt.AlignVCenter)
        box.setSpacing(20)
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
        font = QFont()
        font.setPixelSize(15)
        label = QLabel(self)
        label.setText(text)
        label.setFont(font)
        return label

    def create_margin_label(self, text):
        label = self.create_label(text)
        label.setContentsMargins(10, 10, 10, 10)
        return label

    def create_margin_number_label(self, text):
        label = self.create_label(text)
        label.setContentsMargins(0, 10, 0, 10)
        label.setFixedWidth(50)
        label.setAlignment(Qt.AlignHCenter)
        return label

    @staticmethod
    def set_border_intro(label):
        label.setObjectName("label_intro")
        label.setStyleSheet("QWidget#label_intro {border: 1px solid grey; border-right: 0px solid grey}")
        return label

    @staticmethod
    def set_border_number(label, color='black'):
        label.setObjectName("label_number")
        label.setStyleSheet("QWidget#label_number "
                            "{border: 1px solid grey; border-right: 0px solid grey; border-left: 0px solid grey;"
                            + "color: " + color +"}")
        return label

    @staticmethod
    def set_border_limit(label, color='black'):
        label.setObjectName("label_limit")
        label.setStyleSheet("QWidget#label_limit {border: 1px solid grey; border-left: 0px solid grey; color: "
                            + color + ";}")
        return label

    def make_group_widget(self, elements, total):
        box = QVBoxLayout(self)
        box.setContentsMargins(15, 10, 15, 10)
        box.setSpacing(10)
        for i in elements:
            box.addWidget(i)
        widget = QWidget(self, flags=Qt.Widget)
        widget.setLayout(box)
        widget.setObjectName("widget")
        widget.setStyleSheet("QWidget#widget {border: 0px solid grey; border-bottom: 1px solid grey}")

        total.setContentsMargins(15, 10, 15, 10)
        box = QVBoxLayout(self)
        box.setContentsMargins(0, 0, 0, 0)
        box.setSpacing(0)
        box.addWidget(widget)
        box.addWidget(total)
        widget = QWidget(self, flags=Qt.Widget)
        widget.setLayout(box)
        return widget

    def make_group_number_widget(self, elements, total):
        box = QVBoxLayout(self)
        box.setContentsMargins(0, 10, 0, 10)
        box.setSpacing(10)
        for i in elements:
            i.setFixedWidth(50)
            i.setAlignment(Qt.AlignHCenter)
            box.addWidget(i)
        widget = QWidget(self, flags=Qt.Widget)
        widget.setLayout(box)
        widget.setObjectName("widget")
        widget.setStyleSheet("QWidget#widget {border: 0px solid grey; border-bottom: 1px solid grey}")

        total.setContentsMargins(0, 10, 0, 10)
        box = QVBoxLayout(self)
        box.setContentsMargins(0, 0, 0, 0)
        box.setSpacing(0)
        box.addWidget(widget)
        box.addWidget(total)
        widget = QWidget(self, flags=Qt.Widget)
        widget.setLayout(box)
        return widget

    def get_counter_functions_layout(self):
        font = QFont()
        font.setPixelSize(20)
        counters_title = QLabel(self)
        counters_title.setContentsMargins(5, 5, 5, 5)
        counters_title.setText("Contatori")
        counters_title.setFont(font)

        intro_title = self.create_label("   ")
        intro_lines = self.set_border_intro(self.create_margin_label("Linee di codice "))
        intro_variables = self.set_border_intro(self.create_margin_label("Variabili "))
        intro_if = self.create_label("if")
        intro_elif = self.create_label("elif")
        intro_else = self.create_label("else")
        intro_conditions = self.create_margin_label("Conditions ")
        intro_for = self.create_label("For ")
        intro_while = self.create_label("While ")
        intro_cycles = self.create_margin_label("Cicli ")
        intro_functions = self.set_border_intro(self.create_margin_label("Funzioni "))

        intro_used = self.create_label("Usati")
        self.lines_used_number = self.set_border_number(self.create_margin_number_label('0'))
        self.variables_used_number = self.set_border_number(self.create_margin_number_label('0'))
        self.if_used_number = self.create_label('0')
        self.elif_used_number = self.create_label('0')
        self.else_used_number = self.create_label('0')
        self.conditions_used_number = self.create_margin_number_label('0')
        self.for_used_number = self.create_label('0')
        self.while_used_number = self.create_label('0')
        self.cycles_used_number = self.create_margin_number_label('0')
        self.functions_used_number = self.set_border_number(self.create_margin_number_label('0'))

        intro_owned = self.create_label("Miei")
        self.lines_owned_number \
            = self.set_border_number(self.create_margin_number_label(str(self.data.owned_variables['lines'])))
        self.variables_owned_number \
            = self.set_border_number(self.create_margin_number_label(str(self.data.owned_variables['variables'])))
        self.if_owned_number = self.create_label(str(self.data.owned_variables['if']))
        self.elif_owned_number = self.create_label(str(self.data.owned_variables['elif']))
        self.else_owned_number = self.create_label(str(self.data.owned_variables['else']))
        self.conditions_owned_number \
            = self.create_margin_number_label(str(self.data.owned_variables['if']
                                                  + self.data.owned_variables['elif']
                                                  + self.data.owned_variables['else']))
        self.for_owned_number = self.create_label(str(self.data.owned_variables['for']))
        self.while_owned_number = self.create_label(str(self.data.owned_variables['while']))
        self.cycles_owned_number = self.create_margin_number_label(str(self.data.owned_variables['for']
                                                                       + self.data.owned_variables['while']))
        self.functions_owned_number \
            = self.set_border_number(self.create_margin_number_label(str(self.data.owned_variables['functions'])))

        intro_limit = self.create_label("Max")
        self.lines_limit_number = self.set_border_limit(self.create_margin_number_label(
            '/' if self.exercise.limits['lines'] is None else str(self.exercise.limits['lines'])))
        self.variables_limit_number = self.set_border_limit(self.create_margin_number_label(
            '/' if self.exercise.limits['variables'] is None else str(self.exercise.limits['variables'])))
        self.if_limit_number = self.create_label(
            '/' if self.exercise.limits['if'] is None else str(self.exercise.limits['if']))
        self.elif_limit_number = self.create_label(
            '/' if self.exercise.limits['elif'] is None else str(self.exercise.limits['elif']))
        self.else_limit_number = self.create_label(
            '/' if self.exercise.limits['else'] is None else str(self.exercise.limits['else']))
        self.conditions_limit_number = self.create_margin_number_label(
            '/' if self.exercise.limits['conditions'] is None else str(self.exercise.limits['conditions']))
        self.for_limit_number = self.create_label(
            '/' if self.exercise.limits['for'] is None else str(self.exercise.limits['for']))
        self.while_limit_number = self.create_label(
            '/' if self.exercise.limits['while'] is None else str(self.exercise.limits['while']))
        self.cycles_limit_number = self.create_margin_number_label(
            '/' if self.exercise.limits['cycles'] is None else str(self.exercise.limits['cycles']))
        self.functions_limit_number = self.set_border_limit(self.create_margin_number_label(
            '/' if self.exercise.limits['def'] is None else str(self.exercise.limits['def'])))

        intro_cond = self.set_border_intro(self.make_group_widget([intro_if, intro_elif, intro_else], intro_conditions))
        intro_cycles = self.set_border_intro(self.make_group_widget([intro_for, intro_while], intro_cycles))
        used_conditions = self.set_border_number(self.make_group_number_widget([self.if_used_number,
                                                                         self.elif_used_number, self.else_used_number],
                                                                        self.conditions_used_number))
        used_cycles = self.set_border_number(self.make_group_number_widget([self.for_used_number, self.while_used_number],
                                                                    self.cycles_used_number))
        owned_conditions = self.set_border_number(self.make_group_number_widget([self.if_owned_number, self.elif_owned_number,
                                                                          self.else_owned_number],
                                                                         self.conditions_owned_number))
        owned_cycles = self.set_border_number(self.make_group_number_widget([self.for_owned_number, self.while_owned_number],
                                                                     self.cycles_owned_number))
        limit_conditions = self.set_border_limit(self.make_group_number_widget([self.if_limit_number, self.elif_limit_number,
                                                                         self.else_limit_number],
                                                                        self.conditions_limit_number))
        limit_cycles = self.set_border_limit(self.make_group_number_widget([self.for_limit_number, self.while_limit_number],
                                                                    self.cycles_limit_number))

        box = QVBoxLayout(self)
        box.setContentsMargins(0, 5, 0, 5)
        box.addWidget(intro_title)
        box.addWidget(intro_lines)
        box.addWidget(intro_variables)
        box.addWidget(intro_cond)
        box.addWidget(intro_cycles)
        box.addWidget(intro_functions)
        widget_intro = QWidget(self, flags=Qt.Widget)
        widget_intro.setLayout(box)

        box = QVBoxLayout(self)
        box.setContentsMargins(0, 5, 0, 5)
        box.addWidget(intro_used, alignment=Qt.AlignHCenter)
        box.addWidget(self.lines_used_number)
        box.addWidget(self.variables_used_number)
        box.addWidget(used_conditions)
        box.addWidget(used_cycles)
        box.addWidget(self.functions_used_number)
        widget_used_number = QWidget(self, flags=Qt.Widget)
        widget_used_number.setLayout(box)
        widget_used_number.setObjectName("widget_used_number")
        widget_used_number.setStyleSheet("QWidget#widget_used_number {border: 1px solid grey; "
                                         "border-top: 0px solid grey; border-bottom: 0px solid grey;}")

        box = QVBoxLayout(self)
        box.setContentsMargins(0, 5, 0, 5)
        box.addWidget(intro_owned, alignment=Qt.AlignHCenter)
        box.addWidget(self.lines_owned_number)
        box.addWidget(self.variables_owned_number)
        box.addWidget(owned_conditions)
        box.addWidget(owned_cycles)
        box.addWidget(self.functions_owned_number)
        widget_owned_number = QWidget(self, flags=Qt.Widget)
        widget_owned_number.setLayout(box)

        box = QVBoxLayout(self)
        box.setContentsMargins(0, 5, 0, 5)
        box.addWidget(intro_limit, alignment=Qt.AlignHCenter)
        box.addWidget(self.lines_limit_number)
        box.addWidget(self.variables_limit_number)
        box.addWidget(limit_conditions)
        box.addWidget(limit_cycles)
        box.addWidget(self.functions_limit_number)
        widget_limit_number = QWidget(self, flags=Qt.Widget)
        widget_limit_number.setLayout(box)
        widget_limit_number.setObjectName("widget_limit_number")
        widget_limit_number.setStyleSheet("QWidget#widget_limit_number "
                                          "{border: 0px solid grey; border-left: 1px solid grey}")

        box = QHBoxLayout(self)
        box.setSpacing(0)
        box.addWidget(widget_intro)
        box.addWidget(widget_used_number)
        box.addWidget(widget_owned_number)
        box.addWidget(widget_limit_number)
        widget = QWidget(self, flags=Qt.Widget)
        widget.setLayout(box)

        box = QVBoxLayout(self)
        box.setSpacing(0)
        box.setContentsMargins(0, 0, 0, 0)
        box.setAlignment(Qt.AlignTop)
        box.addWidget(counters_title, alignment=Qt.AlignHCenter)
        box.addWidget(widget)
        return box

    '''
    
    def create_label(self, text):
        font = QFont()
        font.setPixelSize(15)
        label = QLabel(self)
        label.setText(text)
        label.setFont(font)
        return label
    
    def counter_widget(self, intro, number, margins):
        box = QHBoxLayout(self)
        box.setContentsMargins(margins[0], margins[1], margins[2], margins[3])
        box.addWidget(intro, alignment=Qt.AlignLeft)
        box.addWidget(number, alignment=Qt.AlignRight)
        widget = QWidget(self, flags=Qt.Widget)
        widget.setLayout(box)
        return widget

    def complex_widget(self, elements, margins, horizontal=True, h_spacing=10, v_spacing=0):
        if horizontal:
            box = QHBoxLayout(self)
            box.setSpacing(h_spacing)
        else:
            box = QVBoxLayout(self)
            box.setSpacing(v_spacing)
        box.setContentsMargins(margins[0], margins[1], margins[2], margins[3])
        for i in elements:
            box.addWidget(i)
        widget = QWidget(self, flags=Qt.Widget)
        widget.setLayout(box)
        return widget

    def get_counter_functions_layout(self):
        font = QFont()
        font.setPixelSize(20)
        counters_title = QLabel(self)
        counters_title.setContentsMargins(10, 10, 10, 10)
        counters_title.setText("Contatori")
        counters_title.setFont(font)

        intro_lines = self.create_label("Linee di codice ")
        intro_variables = self.create_label("Variabili ")
        intro_if = self.create_label("if")
        intro_elif = self.create_label("elif")
        intro_else = self.create_label("else")
        intro_conditions = self.create_label("Conditions ")
        intro_for = self.create_label("For ")
        intro_while = self.create_label("While ")
        intro_cycles = self.create_label("Cicli ")
        intro_functions = self.create_label("Funzioni ")
        self.lines_number = self.create_label('0')
        self.variables_number = self.create_label('0')
        self.if_number = self.create_label('0')
        self.elif_number = self.create_label('0')
        self.else_number = self.create_label('0')
        self.conditions_number = self.create_label('0')
        self.for_number = self.create_label('0')
        self.while_number = self.create_label('0')
        self.cycles_number = self.create_label('0')
        self.functions_number = self.create_label('0')

        lines_widget = self.counter_widget(intro_lines, self.lines_number, [10, 10, 10, 10])
        lines_widget.setObjectName("lines_widget")
        lines_widget.setStyleSheet("QWidget#lines_widget {border: 1px solid grey}")

        variables_widget = self.counter_widget(intro_variables, self.variables_number, [10, 10, 10, 10])
        variables_widget.setObjectName("variables_widget")
        variables_widget.setStyleSheet("QWidget#variables_widget {border: 1px solid grey}")

        if_widget = self.counter_widget(intro_if, self.if_number, [10, 10, 10, 0])
        elif_widget = self.counter_widget(intro_elif, self.elif_number, [10, 10, 10, 0])
        else_widget = self.counter_widget(intro_else, self.else_number, [10, 10, 10, 10])
        condition_widget = self.counter_widget(intro_conditions, self.conditions_number, [10, 10, 10, 10])

        if_elif_else_widget = self.complex_widget([if_widget, elif_widget, else_widget], [0, 0, 0, 0], horizontal=False)
        if_elif_else_widget.setObjectName("if_elif_else_widget")
        if_elif_else_widget.setStyleSheet("QWidget#if_elif_else_widget "
                                          "{border: 0px solid grey; border-bottom: 1px solid grey}")

        conditions_widget = self.complex_widget([if_elif_else_widget, condition_widget], [0, 0, 0, 0], horizontal=False)
        conditions_widget.setObjectName("conditions_widget")
        conditions_widget.setStyleSheet("QWidget#conditions_widget {border: 1px solid grey}")

        for_widget = self.counter_widget(intro_for, self.for_number, [10, 10, 10, 0])
        while_widget = self.counter_widget(intro_while, self.while_number, [10, 10, 10, 10])
        cycle_widget = self.counter_widget(intro_cycles, self.cycles_number, [10, 10, 10, 10])

        for_while_widget = self.complex_widget([for_widget, while_widget], [0, 0, 0, 0], horizontal=False)
        for_while_widget.setObjectName("for_while_widget")
        for_while_widget.setStyleSheet("QWidget#for_while_widget "
                                       "{border: 0px solid grey; border-bottom: 1px solid grey}")

        cycles_widget = self.complex_widget([for_while_widget, cycle_widget], [0, 0, 0, 0], horizontal=False)
        cycles_widget.setObjectName("cycles_widget")
        cycles_widget.setStyleSheet("QWidget#cycles_widget {border: 1px solid grey}")

        functions_widget = self.counter_widget(intro_functions, self.functions_number, [10, 10, 10, 10])
        functions_widget.setObjectName("functions_widget")
        functions_widget.setStyleSheet("QWidget#functions_widget {border: 1px solid grey}")

        box = QVBoxLayout(self)
        box.setAlignment(Qt.AlignTop)
        box.addWidget(counters_title, alignment=Qt.AlignHCenter)
        box.addWidget(lines_widget)
        box.addWidget(variables_widget)
        box.addWidget(conditions_widget)
        box.addWidget(cycles_widget)
        box.addWidget(functions_widget)

        return box
    '''

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

    def update_function_counters(self, functions):
        self.if_used_number.setText(str(functions['if']))
        if self.exercise.limits['if'] is not None and functions['if'] > self.exercise.limits['if']:
            color = 'red'
        elif functions['if'] > self.data.owned_variables['if']:
            color = '#ff5500'
        else:
            color = 'black'
        self.if_used_number.setStyleSheet("QWidget {color: " + color + "}")
        self.if_owned_number.setStyleSheet("QWidget {color: " + color + "}")
        self.if_limit_number.setStyleSheet("QWidget {color: " + color + "}")

        self.elif_used_number.setText(str(functions['elif']))
        if self.exercise.limits['elif'] is not None and functions['elif'] > self.exercise.limits['elif']:
            color = 'red'
        elif functions['elif'] > self.data.owned_variables['elif']:
            color = '#ff5500'
        else:
            color = 'black'
        self.elif_used_number.setStyleSheet("QWidget {color: " + color + "}")
        self.elif_owned_number.setStyleSheet("QWidget {color: " + color + "}")
        self.elif_limit_number.setStyleSheet("QWidget {color: " + color + "}")

        self.else_used_number.setText(str(functions['else']))
        if self.exercise.limits['else'] is not None and functions['else'] > self.exercise.limits['else']:
            color = 'red'
        elif functions['else'] > self.data.owned_variables['else']:
            color = '#ff5500'
        else:
            color = 'black'
        self.else_used_number.setStyleSheet("QWidget {color: " + color + "}")
        self.else_owned_number.setStyleSheet("QWidget {color: " + color + "}")
        self.else_limit_number.setStyleSheet("QWidget {color: " + color + "}")

        self.conditions_used_number.setText(str(functions['if'] + functions['elif'] + functions['else']))
        if self.exercise.limits['conditions'] is not None \
                and functions['if'] + functions['elif'] + functions['else'] > self.exercise.limits['conditions']:
            color = 'red'
        elif functions['if'] + functions['elif'] + functions['else'] > self.data.owned_variables['if'] \
                + self.data.owned_variables['elif'] + self.data.owned_variables['else']:
            color = '#ff5500'
        else:
            color = 'black'
        self.conditions_used_number.setStyleSheet("QWidget {color: " + color + "}")
        self.conditions_owned_number.setStyleSheet("QWidget {color: " + color + "}")
        self.conditions_limit_number.setStyleSheet("QWidget {color: " + color + "}")

        self.for_used_number.setText(str(functions['for']))
        if self.exercise.limits['for'] is not None and functions['for'] > self.exercise.limits['for']:
            color = 'red'
        elif functions['for'] > self.data.owned_variables['for']:
            color = '#ff5500'
        else:
            color = 'black'
        self.for_used_number.setStyleSheet("QWidget {color: " + color + "}")
        self.for_owned_number.setStyleSheet("QWidget {color: " + color + "}")
        self.for_limit_number.setStyleSheet("QWidget {color: " + color + "}")

        self.while_used_number.setText(str(functions['while']))
        if self.exercise.limits['while'] is not None and functions['while'] > self.exercise.limits['while']:
            color = 'red'
        elif functions['while'] > self.data.owned_variables['while']:
            color = '#ff5500'
        else:
            color = 'black'
        self.while_used_number.setStyleSheet("QWidget {color: " + color + "}")
        self.while_owned_number.setStyleSheet("QWidget {color: " + color + "}")
        self.while_limit_number.setStyleSheet("QWidget {color: " + color + "}")

        self.cycles_used_number.setText(str(functions['for'] + functions['while']))
        if self.exercise.limits['cycles'] is not None \
                and functions['for'] + functions['while'] > self.exercise.limits['cycles']:
            color = 'red'
        elif functions['for'] + functions['while'] \
                > self.data.owned_variables['for'] + self.data.owned_variables['while']:
            color = '#ff5500'
        else:
            color = 'black'
        self.cycles_used_number.setStyleSheet("QWidget {color: " + color + "}")
        self.cycles_owned_number.setStyleSheet("QWidget {color: " + color + "}")
        self.cycles_limit_number.setStyleSheet("QWidget {color: " + color + "}")

        self.functions_used_number.setText(str(functions['def']))
        if self.exercise.limits['def'] is not None and functions['def'] > self.exercise.limits['def']:
            color = 'red'
        elif functions['def'] > self.data.owned_variables['functions']:
            color = '#ff5500'
        else:
            color = 'black'
        self.set_border_number(self.functions_used_number, color)
        self.set_border_number(self.functions_owned_number, color)
        self.set_border_limit(self.functions_limit_number, color)

    def format_text(self):
        if self.text_changed:
            self.text_changed = False
            text = self.code_editor.toPlainText()
            functions = {
                'if': 0,
                'elif': 0,
                'else': 0,
                'for': 0,
                'while': 0,
                'def': 0
            }

            if text != self.exercise.solution:
                self.save_button.setStyleSheet('background-color:yellow')
            else:
                self.save_button.setStyleSheet('background-color:green')
            if text is '':
                self.update_rows_number()
                self.text_changed = True
                self.update_function_counters(functions)
                return
            if (self.exercise.limits['lines'] is not None) and len(text.split('\n')) > self.exercise.limits['lines']:
                self.code_editor.undo()
                self.text_changed = True
                return

            code_editor_cursor = self.code_editor.textCursor()
            x_cur, y_cur = code_editor_cursor.blockNumber(), code_editor_cursor.columnNumber()
            x_bar, y_bar = self.code_editor.verticalScrollBar().value(), self.code_editor.horizontalScrollBar().value()

            temp_text = text
            texts = self.color_strings(text)
            text = ''
            for i in range(0, len(texts)):
                if texts[i] != '' and texts[i][0] != '<':
                    for word in self.exercise.color_styles.keyWords:
                        texts[i], num = self.my_find_and_replace(texts[i], word.word, word.tagged_word(), True)
                        if functions.get(word.word, None) is not None:
                            functions[word.word] = functions[word.word] + num
                text += texts[i]
            if self.exercise.white_paper_mode:
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
            self.update_function_counters(functions)
        self.text_changed = True

    def update_rows_number(self):
        old_value = self.numbers.verticalScrollBar().value()
        rows = ''
        i = 0
        num = len(self.code_editor.toPlainText().split('\n'))
        for i in range(0, num):
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

        self.lines_used_number.setText(str(num))
        if self.exercise.limits['lines'] is not None and num > self.exercise.limits['lines']:
            color = 'red'
        elif num > self.data.owned_variables['lines']:
            color = '#ff5500'
        else:
            color = 'black'
        self.set_border_number(self.lines_used_number, color=color)
        self.set_border_number(self.lines_owned_number, color=color)
        self.set_border_limit(self.lines_limit_number, color=color)

    def scroll_numbers(self):
        self.numbers.verticalScrollBar().setValue(self.code_editor.verticalScrollBar().value())
