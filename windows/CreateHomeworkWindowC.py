import os
from signal import CTRL_BREAK_EVENT
from subprocess import run, Popen, PIPE, DEVNULL
from functools import partial
from PyQt5.QtGui import QTextCursor, QFont
from PyQt5.QtWidgets import QWidget, QPushButton, QHBoxLayout, QVBoxLayout, QLineEdit, QCheckBox, QCalendarWidget, \
    QLabel, QScrollArea, QComboBox
from PyQt5.QtCore import *
from windows.CreateHomeworkWindow import CreateHomeworkWindow, MyCalendar


class CreateHomeworkWindowC(CreateHomeworkWindow):

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
        self.variables_limit_form.setPlaceholderText(" Non implementato")
        self.variables_limit_form.textChanged.connect(self.update_function_counters)
        self.variables_limit_form.setFixedWidth(150)
        self.variables_limit_form.setEnabled(False)

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
        elif_limit_intro.setText("Limite di else if: ")

        self.elif_limit_form = QLineEdit(self)
        self.elif_limit_form.setPlaceholderText(" (Non Obbligatorio)")
        self.elif_limit_form.setFixedWidth(150)
        self.elif_limit_form.textChanged.connect(self.update_function_counters)

        else_limit_intro = QLabel(self)
        else_limit_intro.setStyleSheet("border: 0px solid grey; border-bottom: 1px solid grey")
        else_limit_intro.setText("Limite di else: ")

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
        self.functions_limit_form.setPlaceholderText(" Non implementato")
        self.functions_limit_form.textChanged.connect(self.update_function_counters)
        self.functions_limit_form.setFixedWidth(150)
        self.functions_limit_form.setEnabled(False)

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

        self.validation_type = QComboBox(self)
        self.validation_type.addItem("Nessuna correzione  (ricompensa automatica)")
        self.validation_type.addItem("Correzione binaria  (valido o non valido)")
        self.validation_type.addItem("Correzione graduata (valutazione da 0 a 10)")

        validation_information = QLabel("(Attenzione, sarai responsabile delle valutzioni)", self)
        if self.data.correction_type == 0:
            validation_information.hide()
            self.validation_type.setEnabled(False)
        elif self.data.correction_type == 2 and self.data.my_name not in self.data.my_proff:
            if self.data.approving_type == 0:
                validation_information.setText("(La correzione è a carico del docente)")
                self.validation_type.setCurrentIndex(2)
                self.validation_type.setEnabled(False)
            else:
                validation_information.hide()
                self.validation_type.addItem("La correzione è a carico del docente")
                self.validation_type.setCurrentIndex(3)
                self.validation_type.setEnabled(False)

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
            # if self.exercise.limits['variables'] is not None:
            #    self.variables_limit_form.setText(str(self.exercise.limits['variables']))
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
            # if self.exercise.limits['def'] is not None:
            #    self.functions_limit_form.setText(str(self.exercise.limits['def']))
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

        w = tit.sizeHint().width() + 40
        if self.data.approving_type == 1 and self.data.my_name not in self.data.my_proff:
            font.setPixelSize(12)
            warning = QLabel("Attenzione, il compito dovrà essere approvato per poter fornire la ricompensa"
                             if self.data.student_exercises_visible else
                             "Attenzione, il compito dovrà essere approvato per essere visibile dagli studenti", self)
            self.send_button.setFixedHeight(40)
            warning.setWordWrap(True)
            warning.setFixedHeight(30)
            warning.setFont(font)

            box = QVBoxLayout(self)
            box.setSpacing(5)
            box.setContentsMargins(0, 0, 0, 0)
            box.addWidget(tit)
            box.addWidget(warning)
            tit = QWidget(self, flags=Qt.Widget)
            tit.setLayout(box)
        tit.setFixedWidth(w)

        box = QHBoxLayout(self)
        box.setAlignment(Qt.AlignCenter)
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

        box = QVBoxLayout(self)
        box.setSpacing(5)
        box.addWidget(self.validation_type)
        box.addWidget(validation_information)
        box.setContentsMargins(10, 10, 50, 10)
        validation_type_widget = QWidget(self, flags=Qt.Widget)
        validation_type_widget.setLayout(box)

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
        settings_box.addWidget(validation_type_widget)
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
                result.wait(self.waiting_time)
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
                if self.waiting_time < 5:
                    self.waiting_time = 10
                else:
                    self.waiting_time = 3
                execution_result = "Errore nell'esecuzione del codice.\n" \
                                   "Ciclo infinito / Esecuzione lenta\n" \
                                   "Al prossimo play l'applicativo crasherà"
                code_compile = False
        else:
            execution_result = result.stderr.decode('ascii').replace(path + ":", "")
            code_compile = False
        return execution_result, code_compile

    def play_button_on_click(self):
        self.temp_vars = {}
        execution_result, code_compile = self.exec_code()

        self.results.setPlainText(execution_result)
        if code_compile:
            self.results.setStyleSheet('color: black')
        else:
            self.results.setStyleSheet('color: red')
        self.update_function_counters()
        self.show()
        return not code_compile

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
            elif text[i] == '<':
                text = text[0:i] + '&#60;' + text[i + 1:len(text)]
                i += 4
            elif text[i] == '>':
                text = text[0:i] + '&#62;' + text[i + 1:len(text)]
                i += 4
            i += 1
        texts.append(text[start:i])
        return texts

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
                    for word in self.data.color_styles.keyWords.keys():
                        for w in word.split(', '):
                            tagged = '<span style=\" color: ' + self.data.color_styles.keyWords[word][0] \
                                     + ';\">' + w + '</span>'
                            if self.data.color_styles.keyWords[word][1]:
                                tagged = '<b>' + tagged + '</b>'
                            texts[i], num = self.my_find_and_replace(texts[i], w, tagged, True)
                            if w == 'else if':
                                self.functions['elif'] = self.functions['elif'] + num
                            if self.functions.get(w, None) is not None:
                                self.functions[w] = self.functions[w] + num
                text += texts[i]
            self.functions['if'] -= self.functions['elif']
            self.functions['else'] -= self.functions['elif']
            if self.white_paper_mode:
                temp_text = temp_text.replace('<', '&#60;')
                temp_text = temp_text.replace('>', '&#62;')
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
