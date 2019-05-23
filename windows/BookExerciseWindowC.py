import os
from signal import CTRL_BREAK_EVENT
from subprocess import run, Popen, PIPE, DEVNULL
from PyQt5.QtGui import QTextCursor, QFont, QPixmap
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLabel
from PyQt5.QtCore import *

from windows.BookExerciseWindow import BookExerciseWindow


class BookExerciseWindowC(BookExerciseWindow):

    def exec_code(self):
        compiler = "C:\Program Files (x86)\Dev-Cpp\MinGW64\\bin\g++.exe"

        if not os.path.isfile(compiler):
            compiler = self.data.get_path() + "\MinGW64\\bin\g++"

        path = self.data.get_path() + "\\temp\code.cpp"
        exe_path = self.data.get_path() + "\\temp\\ris.exe"

        f = open(path, "w")
        f.write(self.code_editor.toPlainText())
        f.close()
        result = run(compiler + " -o " + exe_path + " " + path, stdout=PIPE, stderr=PIPE, stdin=DEVNULL)
        if result.returncode == 0:
            result = Popen(exe_path, stdout=PIPE, stderr=PIPE, stdin=DEVNULL)
            try:
                result.wait(self.data.execution_waitng_time)
                out = result.stdout.read().decode('ascii')
                err = result.stderr.read().decode('ascii')
                if err == '':
                    execution_result = out
                    code_compile = True
                else:
                    execution_result = err
                    code_compile = False
            except Exception:
                result.send_signal(CTRL_BREAK_EVENT)
                #result.kill()
                execution_result = "Errore nell'esecuzione del codice.\n" \
                                   "Ciclo infinito / Esecuzione lenta\n" \
                                   "Al prossimo play l'applicativo crasherà"
                code_compile = False
        else:
            execution_result = result.stderr.decode('ascii').replace(path + ":", "")
            code_compile = False
        return execution_result, code_compile

    def play_button_on_click(self, event):
        execution_temp_vars = {}
        execution_result, self.code_compile = self.exec_code()

        self.results.setPlainText(execution_result)
        if self.code_compile:
            self.results.setStyleSheet(
                "QWidget#results {background-color: " + self.data.color_styles.results_background_color
                + "; color: " + self.data.color_styles.results_text_color + ";}")
        else:
            self.results.setStyleSheet("QWidget#results {background-color: "
                                       + self.data.color_styles.error_results_background_color + "; color: "
                                       + self.data.color_styles.error_results_text_color + ";}")

        self.variables_used_number.setText('?')
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
        self.show()

    def get_counter_functions_layout(self):
        font = QFont()
        font.setPixelSize(20)
        counters_title = QLabel(self)
        counters_title.setContentsMargins(5, 5, 5, 5)
        counters_title.setText("Contatori")
        counters_title.setFont(font)

        intro_title = self.create_label("   ")
        intro_lines = self.set_border_intro(self.create_margin_label("Linee di codice "))
        intro_variables = self.set_border_intro(self.create_margin_label("Variabili"))
        intro_if = self.create_label("if")
        intro_elif = self.create_label("else if")
        intro_else = self.create_label("else")
        intro_conditions = self.create_margin_label("Selezioni ")
        intro_for = self.create_label("For ")
        intro_while = self.create_label("While ")
        intro_cycles = self.create_margin_label("Cicli ")
        intro_functions = self.set_border_intro(self.create_margin_label("Funzioni "))

        intro_used = self.create_label("Usati")
        self.lines_used_number = self.set_border_number(self.create_margin_number_label('0'))
        self.variables_used_number = self.set_border_number(self.create_margin_number_label('?'))
        self.if_used_number = self.create_label('0')
        self.elif_used_number = self.create_label('0')
        self.else_used_number = self.create_label('0')
        self.conditions_used_number = self.create_margin_number_label('0')
        self.for_used_number = self.create_label('0')
        self.while_used_number = self.create_label('0')
        self.cycles_used_number = self.create_margin_number_label('0')
        self.functions_used_number = self.set_border_number(self.create_margin_number_label('?'))

        intro_owned = self.create_label("Miei")
        self.lines_owned_number = self.set_border_number(self.create_margin_number_label(
            '/' if self.data.owned_variables['lines'] is None else str(self.data.owned_variables['lines'])))
        self.variables_owned_number = self.set_border_number(self.create_margin_number_label('?'))
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
        self.functions_owned_number = self.set_border_number(self.create_margin_number_label('?'))

        intro_limit = self.create_label("Max")
        self.lines_limit_number = self.set_border_limit(self.create_margin_number_label(
            '/' if self.exercise.limits['lines'] is None else str(self.exercise.limits['lines'])))
        self.variables_limit_number = self.set_border_limit(self.create_margin_number_label('?'))
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
        self.functions_limit_number = self.set_border_limit(self.create_margin_number_label('?'))

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

    def color_strings(self, text):
        texts = []
        multi_line_comment, comment, string_start, i, start = False, False, None, 0, 0
        while i < len(text):
            if ((i < len(text) - 1 and text[i] == '/' and text[i+1] == '/') or text[i] == '#') \
                    and string_start is None and not multi_line_comment and not comment:
                if i != start:
                    texts.append(text[start:i])
                    start = i
                text = text[0:i] + '<span style=\" color:' + self.data.color_styles.comment_color \
                       + ';\">' + text[i:len(text)]
                i += len('<span style=\" color:' + self.data.color_styles.comment_color + ';\">')
                comment = True
            elif i < len(text) - 1 and text[i] == '/' and text[i+1] == '*' and string_start is None \
                    and not multi_line_comment and not comment:
                if i != start:
                    texts.append(text[start:i])
                    start = i
                text = text[0:i] + '<span style=\" color:' + self.data.color_styles.multi_line_comment_color \
                       + ';\">' + text[i:len(text)]
                i += len('<span style=\" color:' + self.data.color_styles.multi_line_comment_color + ';\">') + 1
                multi_line_comment = True
            elif i < len(text) - 1 and text[i] == '*' and text[i+1] == '/' and string_start is None \
                    and multi_line_comment and not comment:
                text = text[0:i + 2] + '</span>' + text[i + 2:len(text)]
                i += len('</span>') + 1
                texts.append(text[start:i + 1])
                start = i + 1
                multi_line_comment = False
            elif (text[i] == '"' or text[i] == "'") and comment is False:
                if string_start is None:
                    if not multi_line_comment:
                        if i != start:
                            texts.append(text[start:i])
                            start = i
                        text = text[0:i] + '<span style=\" color:' + self.data.color_styles.string_color \
                               + ';\">' + text[i:len(text)]
                        i += len('<span style=\" color:' + self.data.color_styles.string_color + ';\">')
                        string_start = text[i]
                elif text[i] == string_start:
                    if not multi_line_comment:
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

        self.functions_used_number.setText('?')
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
                            if w == 'else if':
                                self.resources_used['elif'] = self.resources_used['elif'] + num
                            if self.resources_used.get(w, None) is not None:
                                self.resources_used[w] = self.resources_used[w] + num
                text += texts[i]
            self.resources_used['if'] -= self.resources_used['elif']
            self.resources_used['else'] -= self.resources_used['elif']
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
