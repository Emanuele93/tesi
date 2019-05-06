from functools import partial
import re
from os import path
from PyQt5.QtGui import QTextCursor, QFont, QPixmap, QFontMetricsF, QIcon
from PyQt5.QtWidgets import QWidget, QTextEdit, QPlainTextEdit, QSplitter, QHBoxLayout, QVBoxLayout, QLabel, QDialog
from PyQt5.QtCore import *
from windows.ConfirmWindow import ConfirmWindow
from windows.ExerciseWindow import MyThread, MyTimer
from windows.SettingsWindow import SettingsWindow


class BookExerciseWindow(QWidget):
    def __init__(self, exercise, data, exercise_widget):
        super(BookExerciseWindow, self).__init__(flags=Qt.Window)
        self.setMinimumSize(QSize(1000, 650))
        self.setWindowTitle('Eserciziario - "' + exercise.title + '"')
        self.setWindowIcon(QIcon("img/logo.png"))
        self.exercise = exercise
        self.data = data
        self.exercise_widget = exercise_widget

        self.text_changed = True
        self.more_options_is_visible = False
        self.code_compile = True
        self.resources_used = {'lines': 0, 'variables': 0, 'if': 0, 'elif': 0, 'else': 0, 'conditions': 0,
                               'for': 0, 'while': 0, 'cycles': 0, 'def': 0}

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
        self.numbers.setObjectName("code_editor")
        self.numbers.setStyleSheet("QWidget#code_editor {background-color: "
                                   + self.data.color_styles.code_background_color
                                   + "; color: " + self.data.color_styles.code_text_color + ";}")

        self.code_editor = QTextEdit(self)
        self.code_editor.setLineWrapMode(self.code_editor.NoWrap)
        self.code_editor.textChanged.connect(self.format_text)
        self.code_editor.verticalScrollBar().valueChanged.connect(self.scroll_numbers)
        self.code_editor.setText(self.exercise.start_code if self.exercise.solution is None else self.exercise.solution)
        self.code_editor.setTabStopDistance(QFontMetricsF(self.code_editor.font()).width(' ') * 12)
        self.code_editor.setObjectName("code_editor")
        self.code_editor.setStyleSheet("QWidget#code_editor {background-color: "
                                       + self.data.color_styles.code_background_color + "; color: "
                                       + self.data.color_styles.code_text_color + ";}")
        if self.exercise.delivery_date is not None:
            self.code_editor.setReadOnly(True)

        self.results = QPlainTextEdit(self)
        self.results.setReadOnly(True)
        self.results.setLineWrapMode(self.results.NoWrap)
        self.results.setObjectName("results")
        self.results.setStyleSheet("QWidget#results {background-color: "
                                   + self.data.color_styles.results_background_color
                                   + "; color: " + self.data.color_styles.results_text_color + ";}")
        if not self.exercise.executable:
            self.results.hide()

        self.set_text_font_size(self.data.code_font_size, self.data.code_font_family)

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
        self.coding_widget.addWidget(widget2)
        self.coding_widget.addWidget(self.results)
        self.coding_widget.setSizes([150, 100])
        self.coding_widget.setChildrenCollapsible(False)
        self.update_text_result_orientation()

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

        self.info = QLabel('', self)
        self.info.setStyleSheet("border: 1px solid grey; background-color: #ffdd99}")
        self.info.setAlignment(Qt.AlignCenter)
        self.info.hide()

    def show_text(self, text, dim, rif, event):
        self.info.setText(text)
        self.info.show()
        self.info.setFixedWidth(dim)
        self.info.move(rif.pos().x() + rif.width() / 5 * 1, rif.pos().y() + rif.height())

    def hide_text(self, event):
        self.info.hide()

    def resize_window(self, widget, event):
        widget.move(self.width()-80, 10)

    def update_text_result_orientation(self):
        self.coding_widget.setOrientation(
            Qt.Horizontal if self.data.code_result_horizontal_orientation else Qt.Vertical)

    def get_play_option_widget(self):
        pixmap = QPixmap('img/play.png')
        pixmap = pixmap.scaled(50, 50)
        play_button = QLabel(self)
        play_button.setPixmap(pixmap)
        play_button.setObjectName('img/play.png')
        play_button.mousePressEvent = self.play_button_on_click
        play_button.enterEvent = partial(self.show_text, 'Play', 40, play_button)
        play_button.leaveEvent = self.hide_text
        if not self.exercise.executable:
            play_button.setEnabled(False)

        pixmap = QPixmap('img/saved.png')
        pixmap = pixmap.scaled(50, 50)
        self.save_button = QLabel(self)
        self.save_button.setPixmap(pixmap)
        self.save_button.setObjectName('img/save.png')
        self.save_button.mousePressEvent = self.save_button_on_click
        self.save_button.enterEvent = partial(self.show_text, 'Salva', 45, self.save_button)
        self.save_button.leaveEvent = self.hide_text
        if self.exercise.text is None:
            self.save_button.hide()

        pixmap = QPixmap('img/settings.png')
        pixmap = pixmap.scaled(50, 50)
        settings_button = QLabel(self)
        settings_button.setPixmap(pixmap)
        settings_button.setObjectName('img/settings.png')
        settings_button.mousePressEvent = self.swap_button_on_click
        settings_button.enterEvent = partial(self.show_text, 'Impostazioni', 85, settings_button)
        settings_button.leaveEvent = self.hide_text

        pixmap = QPixmap('img/reset.png')
        pixmap = pixmap.scaled(50, 50)
        restart_button = QLabel(self)
        restart_button.setPixmap(pixmap)
        restart_button.setObjectName('img/reset.png')
        restart_button.mousePressEvent = self.restart_button_on_click
        restart_button.enterEvent = partial(self.show_text, 'Ricomincia', 75, restart_button)
        restart_button.leaveEvent = self.hide_text
        if self.exercise.text is None:
            restart_button.hide()

        box = QHBoxLayout(self)
        box.setAlignment(Qt.AlignCenter)
        if self.exercise.text is None:
            box.setSpacing(60)
        else:
            box.setSpacing(20)
        box.setContentsMargins(20, 0, 20, 0)
        box.addWidget(play_button)
        box.addWidget(self.save_button)
        box.addWidget(restart_button)
        box.addWidget(settings_button)
        return box

    def play_button_on_click(self, event):
        execution_temp_vars = {}

        t1 = MyThread('Thread 1', self.code_editor, execution_temp_vars)
        t2 = MyTimer(t1)
        t1.start()
        t2.start()
        t1.join()

        execution_result = t1.execution_result
        self.code_compile = t1.code_compile
        execution_temp_result = t1.execution_temp_result

        if execution_temp_result != '':
            execution_result = execution_temp_result + '\n' + execution_result

        self.results.setPlainText(execution_result)
        if self.code_compile:
            self.results.setStyleSheet(
                "QWidget#results {background-color: " + self.data.color_styles.results_background_color
                + "; color: " + self.data.color_styles.results_text_color + ";}")
        else:
            self.results.setStyleSheet("QWidget#results {background-color: "
                                       + self.data.color_styles.error_results_background_color + "; color: "
                                       + self.data.color_styles.error_results_text_color + ";}")

        self.variables_used_number.setText(str(len(execution_temp_vars)))
        self.resources_used['variables'] = len(execution_temp_vars)
        if self.exercise.limits['variables'] is not None and len(execution_temp_vars) > self.exercise.limits[
            'variables']:
            color = 'red'
        elif self.data.owned_variables['variables'] is not None \
                and len(execution_temp_vars) > self.data.owned_variables['variables']:
            color = '#ff5500'
        else:
            color = 'black'
        self.set_border_number(self.variables_used_number, color=color)
        self.set_border_number(self.variables_owned_number, color=color)
        self.set_border_limit(self.variables_limit_number, color=color)

    def save_button_on_click(self, event):
        pixmap = QPixmap('img/saved.png')
        pixmap = pixmap.scaled(50, 50)
        self.save_button.setPixmap(pixmap)
        self.exercise.solution = self.code_editor.toPlainText()

        file = self.exercise.title
        file_name = 'saves/' + self.exercise.title + '.txt'

        if file.__contains__('"') or file.__contains__("'") or file.__contains__('?') or file.__contains__('\\') \
                or file.__contains__('/') or file.__contains__(":") or file.__contains__("*") \
                or file.__contains__("<") or file.__contains__(">") or file.__contains__("|"):
            not_find = True
            file_name = '0'
            if path.isfile('saves/_lib.txt'):
                f = open('saves/_lib.txt', 'r')
                for i in f:
                    if not_find:
                        if i[len(i.split(':')[0]) + 1:-1] == file:
                            not_find = False
                            file_name = i.split(':')[0]
                        else:
                            file_name = str(int(i.split(':')[0]) + 1)
                f.close()
            if not_find:
                f = open('saves/_lib.txt', 'a')
                f.write(file_name + ':' + file + '\n')
                f.close()
            file_name = 'saves/' + file_name + '.txt'

        f = open(file_name, "w")
        f.write(self.exercise.solution)
        f.close()

        self.exercise_widget.setStyleSheet('background-color: #99dd99')

    def more_button_on_click(self, event):
        if self.more_options_is_visible:
            self.more_options.hide()
        else:
            self.more_options.show()
        self.more_options_is_visible = not self.more_options_is_visible
        return

    def swap_button_on_click(self, event):
        self.exercise.color_styles = None
        confirm = SettingsWindow('Settings - "' + self.exercise.title + '"',
                                 self.data, self, parent=self)
        if confirm.exec_() == QDialog.Accepted:
            print('ok')
        confirm.deleteLater()

    def restart_button_on_click(self, event):
        confirm = ConfirmWindow("Ricominciare l'esercizio",
                                "<span style=\" color: red;\"> Attenzione, confermi di voler ricominciare "
                                "l'esercizio?<br>Tutto ciò che non e stato salvato non sarà più recuperabile</span>",
                                ok="Conferma", cancel="Annulla")
        if confirm.exec_() == QDialog.Accepted:
            self.code_editor.setText(self.exercise.start_code)
            self.results.setPlainText('')
        confirm.deleteLater()

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
                            + "color: " + color + "}")
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

    def make_separator(self):
        separator = QLabel(self)
        separator.setFixedHeight(5)
        separator.setObjectName("separator")
        separator.setStyleSheet("QWidget#separator {border: 0px solid grey; border-bottom: 1px solid grey; "
                                "border-top: 1px solid grey}")
        return separator

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
        intro_conditions = self.create_margin_label("Selezioni ")
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
        self.lines_owned_number = self.set_border_number(self.create_margin_number_label(
            '/' if self.data.owned_variables['lines'] is None else str(self.data.owned_variables['lines'])))
        self.variables_owned_number = self.set_border_number(self.create_margin_number_label(
            '/' if self.data.owned_variables['variables'] is None else str(self.data.owned_variables['variables'])))
        self.if_owned_number = self.create_label(
            '/' if self.data.owned_variables['if'] is None else str(self.data.owned_variables['if']))
        self.elif_owned_number = self.create_label('/' if self.data.owned_variables['elif'] is None
                                                   else str(self.data.owned_variables['elif']))
        self.else_owned_number = self.create_label('/' if self.data.owned_variables['else'] is None
                                                   else str(self.data.owned_variables['else']))
        self.conditions_owned_number = self.create_margin_number_label(
            '/' if self.data.owned_variables['elif'] is None or self.data.owned_variables['if'] is None
                   or self.data.owned_variables['else'] is None
            else str(self.data.owned_variables['if'] + self.data.owned_variables['elif']
                     + self.data.owned_variables['else']))
        self.for_owned_number = self.create_label('/' if self.data.owned_variables['for'] is None
                                                  else str(self.data.owned_variables['for']))
        self.while_owned_number = self.create_label('/' if self.data.owned_variables['while'] is None
                                                    else str(self.data.owned_variables['while']))
        self.cycles_owned_number = self.create_margin_number_label(
            '/' if self.data.owned_variables['for'] is None or self.data.owned_variables['while'] is None
            else str(self.data.owned_variables['for'] + self.data.owned_variables['while']))
        self.functions_owned_number = self.set_border_number(self.create_margin_number_label(
            '/' if self.data.owned_variables['functions'] is None else str(self.data.owned_variables['functions'])))

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
                                                                                self.elif_used_number,
                                                                                self.else_used_number],
                                                                               self.conditions_used_number))
        used_cycles = self.set_border_number(
            self.make_group_number_widget([self.for_used_number, self.while_used_number],
                                          self.cycles_used_number))
        owned_conditions = self.set_border_number(
            self.make_group_number_widget([self.if_owned_number, self.elif_owned_number,
                                           self.else_owned_number],
                                          self.conditions_owned_number))
        owned_cycles = self.set_border_number(
            self.make_group_number_widget([self.for_owned_number, self.while_owned_number],
                                          self.cycles_owned_number))
        limit_conditions = self.set_border_limit(
            self.make_group_number_widget([self.if_limit_number, self.elif_limit_number,
                                           self.else_limit_number],
                                          self.conditions_limit_number))
        limit_cycles = self.set_border_limit(
            self.make_group_number_widget([self.for_limit_number, self.while_limit_number],
                                          self.cycles_limit_number))

        separator1 = self.make_separator()
        separator2 = self.make_separator()
        separator3 = self.make_separator()
        separator4 = self.make_separator()

        box = QVBoxLayout(self)
        box.setContentsMargins(0, 5, 0, 5)
        box.addWidget(intro_title)
        box.addWidget(intro_lines)
        box.addWidget(intro_cond)
        box.addWidget(intro_cycles)
        box.addWidget(intro_functions)
        box.addWidget(separator1)
        box.addWidget(intro_variables)
        widget_intro = QWidget(self, flags=Qt.Widget)
        widget_intro.setLayout(box)

        box = QVBoxLayout(self)
        box.setContentsMargins(0, 5, 0, 5)
        box.addWidget(intro_used, alignment=Qt.AlignHCenter)
        box.addWidget(self.lines_used_number)
        box.addWidget(used_conditions)
        box.addWidget(used_cycles)
        box.addWidget(self.functions_used_number)
        box.addWidget(separator2)
        box.addWidget(self.variables_used_number)
        widget_used_number = QWidget(self, flags=Qt.Widget)
        widget_used_number.setLayout(box)
        widget_used_number.setObjectName("widget_used_number")
        widget_used_number.setStyleSheet("QWidget#widget_used_number {border: 1px solid grey; "
                                         "border-top: 0px solid grey; border-bottom: 0px solid grey;}")

        box = QVBoxLayout(self)
        box.setContentsMargins(0, 5, 0, 5)
        box.addWidget(intro_owned, alignment=Qt.AlignHCenter)
        box.addWidget(self.lines_owned_number)
        box.addWidget(owned_conditions)
        box.addWidget(owned_cycles)
        box.addWidget(self.functions_owned_number)
        box.addWidget(separator3)
        box.addWidget(self.variables_owned_number)
        widget_owned_number = QWidget(self, flags=Qt.Widget)
        widget_owned_number.setLayout(box)

        box = QVBoxLayout(self)
        box.setContentsMargins(0, 5, 0, 5)
        box.addWidget(intro_limit, alignment=Qt.AlignHCenter)
        box.addWidget(self.lines_limit_number)
        box.addWidget(limit_conditions)
        box.addWidget(limit_cycles)
        box.addWidget(self.functions_limit_number)
        box.addWidget(separator4)
        box.addWidget(self.variables_limit_number)
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

    def set_text_font_size(self, num=None, family=None):
        font = QFont()
        if family is not None:
            font.setFamily(family)
        if num is not None:
            font.setPixelSize(num)
        self.code_editor.setFont(font)
        self.results.setFont(font)
        self.numbers.setFont(font)
        self.text_exercise.setFont(font)

    def update_text_font_size(self):
        font = QFont()
        font.setFamily(self.data.code_font_family)
        font.setPixelSize(self.data.code_font_size)
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
            elif text[i] == '<':  # < da sostituire con &#60
                text = text[0:i] + '&#60;' + text[i + 1:len(text)]
                i += 4
            elif text[i] == '>':  # > da sostituire con &#62
                text = text[0:i] + '&#62;' + text[i + 1:len(text)]
                i += 4
            i += 1
        texts.append(text[start:i])
        return texts

    def update_function_counters(self):
        self.if_used_number.setText(str(self.resources_used['if']))
        if self.exercise.limits['if'] is not None and self.resources_used['if'] > self.exercise.limits['if']:
            color = 'red'
        elif self.data.owned_variables['if'] is not None \
                and self.resources_used['if'] > self.data.owned_variables['if']:
            color = '#ff5500'
        else:
            color = 'black'
        self.if_used_number.setStyleSheet("QWidget {color: " + color + "}")
        self.if_owned_number.setStyleSheet("QWidget {color: " + color + "}")
        self.if_limit_number.setStyleSheet("QWidget {color: " + color + "}")

        self.elif_used_number.setText(str(self.resources_used['elif']))
        if self.exercise.limits['elif'] is not None and self.resources_used['elif'] > self.exercise.limits['elif']:
            color = 'red'
        elif self.data.owned_variables['elif'] is not None \
                and self.resources_used['elif'] > self.data.owned_variables['elif']:
            color = '#ff5500'
        else:
            color = 'black'
        self.elif_used_number.setStyleSheet("QWidget {color: " + color + "}")
        self.elif_owned_number.setStyleSheet("QWidget {color: " + color + "}")
        self.elif_limit_number.setStyleSheet("QWidget {color: " + color + "}")

        self.else_used_number.setText(str(self.resources_used['else']))
        if self.exercise.limits['else'] is not None and self.resources_used['else'] > self.exercise.limits['else']:
            color = 'red'
        elif self.data.owned_variables['else'] is not None \
                and self.resources_used['else'] > self.data.owned_variables['else']:
            color = '#ff5500'
        else:
            color = 'black'
        self.else_used_number.setStyleSheet("QWidget {color: " + color + "}")
        self.else_owned_number.setStyleSheet("QWidget {color: " + color + "}")
        self.else_limit_number.setStyleSheet("QWidget {color: " + color + "}")

        self.conditions_used_number.setText(str(self.resources_used['if'] + self.resources_used['elif']
                                                + self.resources_used['else']))
        if self.exercise.limits['conditions'] is not None \
                and self.resources_used['if'] + self.resources_used['elif'] \
                + self.resources_used['else'] > self.exercise.limits['conditions']:
            color = 'red'
        elif self.data.owned_variables['if'] is not None and self.data.owned_variables['elif'] is not None \
                and self.data.owned_variables['else'] is not None \
                and self.resources_used['if'] + self.resources_used['elif'] + self.resources_used['else'] > \
                self.data.owned_variables['if'] + self.data.owned_variables['elif'] + self.data.owned_variables['else']:
            color = '#ff5500'
        else:
            color = 'black'
        self.conditions_used_number.setStyleSheet("QWidget {color: " + color + "}")
        self.conditions_owned_number.setStyleSheet("QWidget {color: " + color + "}")
        self.conditions_limit_number.setStyleSheet("QWidget {color: " + color + "}")

        self.for_used_number.setText(str(self.resources_used['for']))
        if self.exercise.limits['for'] is not None and self.resources_used['for'] > self.exercise.limits['for']:
            color = 'red'
        elif self.data.owned_variables['for'] is not None \
                and self.resources_used['for'] > self.data.owned_variables['for']:
            color = '#ff5500'
        else:
            color = 'black'
        self.for_used_number.setStyleSheet("QWidget {color: " + color + "}")
        self.for_owned_number.setStyleSheet("QWidget {color: " + color + "}")
        self.for_limit_number.setStyleSheet("QWidget {color: " + color + "}")

        self.while_used_number.setText(str(self.resources_used['while']))
        if self.exercise.limits['while'] is not None and self.resources_used['while'] > self.exercise.limits['while']:
            color = 'red'
        elif self.data.owned_variables['while'] is not None \
                and self.resources_used['while'] > self.data.owned_variables['while']:
            color = '#ff5500'
        else:
            color = 'black'
        self.while_used_number.setStyleSheet("QWidget {color: " + color + "}")
        self.while_owned_number.setStyleSheet("QWidget {color: " + color + "}")
        self.while_limit_number.setStyleSheet("QWidget {color: " + color + "}")

        self.cycles_used_number.setText(str(self.resources_used['for'] + self.resources_used['while']))
        if self.exercise.limits['cycles'] is not None \
                and self.resources_used['for'] + self.resources_used['while'] > self.exercise.limits['cycles']:
            color = 'red'
        elif self.data.owned_variables['for'] is not None and self.data.owned_variables['while'] is not None \
                and self.resources_used['for'] + self.resources_used['while'] \
                > self.data.owned_variables['for'] + self.data.owned_variables['while']:
            color = '#ff5500'
        else:
            color = 'black'
        self.cycles_used_number.setStyleSheet("QWidget {color: " + color + "}")
        self.cycles_owned_number.setStyleSheet("QWidget {color: " + color + "}")
        self.cycles_limit_number.setStyleSheet("QWidget {color: " + color + "}")

        self.functions_used_number.setText(str(self.resources_used['def']))
        if self.exercise.limits['def'] is not None and self.resources_used['def'] > self.exercise.limits['def']:
            color = 'red'
        elif self.data.owned_variables['functions'] is not None \
                and self.resources_used['def'] > self.data.owned_variables['functions']:
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
            self.resources_used['if'] = 0
            self.resources_used['elif'] = 0
            self.resources_used['else'] = 0
            self.resources_used['for'] = 0
            self.resources_used['while'] = 0
            self.resources_used['def'] = 0

            if text != self.exercise.solution:
                pixmap = QPixmap('img/unsaved.png')
                pixmap = pixmap.scaled(50, 50)
                self.save_button.setPixmap(pixmap)
            else:
                pixmap = QPixmap('img/saved.png')
                pixmap = pixmap.scaled(50, 50)
                self.save_button.setPixmap(pixmap)
            if text is '':
                self.update_rows_number()
                self.text_changed = True
                self.update_function_counters()
                return
            '''
            if (self.exercise.limits['lines'] is not None) and len(text.split('\n')) > self.exercise.limits['lines']:
                self.code_editor.undo()
                self.text_changed = True
                return
            '''

            code_editor_cursor = self.code_editor.textCursor()
            x_cur, y_cur = code_editor_cursor.blockNumber(), code_editor_cursor.columnNumber()
            x_bar, y_bar = self.code_editor.verticalScrollBar().value(), self.code_editor.horizontalScrollBar().value()

            temp_text = text
            texts = self.color_strings(text)
            text = ''
            for i in range(0, len(texts)):
                if texts[i] != '' and texts[i][0] != '<':
                    for word in self.data.color_styles.keyWords.keys():
                        for w in word.split(', '):
                            tagged = '<span style=\" color: ' + self.data.color_styles.keyWords[word][0] \
                                     + ';\">' + w + '</span>'
                            if self.data.color_styles.keyWords[word][1]:
                                tagged = '<b>' + tagged + '</b>'
                            texts[i], num = self.my_find_and_replace(texts[i], w, tagged, True)
                            if self.resources_used.get(w, None) is not None:
                                self.resources_used[w] = self.resources_used[w] + num
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
            self.update_function_counters()
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
        self.resources_used['lines'] = num
        if self.exercise.limits['lines'] is not None and num > self.exercise.limits['lines']:
            color = 'red'
        elif self.data.owned_variables['lines'] is not None and num > self.data.owned_variables['lines']:
            color = '#ff5500'
        else:
            color = 'black'
        self.set_border_number(self.lines_used_number, color=color)
        self.set_border_number(self.lines_owned_number, color=color)
        self.set_border_limit(self.lines_limit_number, color=color)

    def scroll_numbers(self):
        self.numbers.verticalScrollBar().setValue(self.code_editor.verticalScrollBar().value())

    def set_color_styles(self, color_styles):
        self.exercise.color_styles = color_styles
        self.data.color_styles = self.data.color_styles if self.exercise.color_styles is None else self.exercise.color_styles
        # Todo da segnare su file

        self.code_editor.setStyleSheet("QWidget#code_editor {background-color: "
                                       + self.data.color_styles.code_background_color
                                       + "; color: " + self.data.color_styles.code_text_color + ";}")
        self.numbers.setStyleSheet("QWidget#code_editor {background-color: " + self.data.color_styles.code_background_color
                                   + "; color: " + self.data.color_styles.code_text_color + ";}")
        if self.code_compile:
            self.results.setStyleSheet("QWidget#results {background-color: "
                                       + self.data.color_styles.results_background_color
                                       + "; color: " + self.data.color_styles.results_text_color + ";}")
        else:
            self.results.setStyleSheet("QWidget#results {background-color: "
                                       + self.data.color_styles.error_results_background_color + "; color: "
                                       + self.data.color_styles.error_results_text_color + ";}")
        self.format_text()

    def show(self):
        super(BookExerciseWindow, self).show()
        self.update_text_result_orientation()
        self.update_text_font_size()
        self.data.color_styles = self.data.color_styles
        self.numbers.setStyleSheet("QWidget#code_editor {background-color: " + self.data.color_styles.code_background_color
                                   + "; color: " + self.data.color_styles.code_text_color + ";}")
        self.code_editor.setStyleSheet("QWidget#code_editor {background-color: "
                                       + self.data.color_styles.code_background_color + "; color: "
                                       + self.data.color_styles.code_text_color + ";}")
        self.results.setStyleSheet("QWidget#results {background-color: " + self.data.color_styles.results_background_color
                                   + "; color: " + self.data.color_styles.results_text_color + ";}")
        self.format_text()
