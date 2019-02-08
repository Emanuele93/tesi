import contextlib
import io
import re
from functools import partial

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtWidgets import QDialog, QWidget, QVBoxLayout, QLabel, QHBoxLayout, QScrollArea, QTextEdit, \
    QPlainTextEdit, QSplitter

from Data import DefaultColorStyles


class ClassExerciseComparisonWindow(QDialog):
    def __init__(self, title, class_solutions, exercise_limit, exercise_window, parent=None):
        QDialog.__init__(self, parent, flags=Qt.Dialog)
        self.setWindowTitle(title)
        self.setMinimumWidth(900)
        self.setFixedHeight(465)
        self.exercise_window = exercise_window
        self.parent = parent
        self.limits = exercise_limit
        self.color_styles = None
        self.code_widgets = []

        students_widgets = []
        for i in class_solutions:
            students_widgets.append(self.make_student_widget(i))

        box = QHBoxLayout(self)
        box.setAlignment(Qt.AlignLeft)
        for i in students_widgets:
            box.addWidget(i, alignment=Qt.AlignLeft)

        if len(class_solutions)==0:
            font = QFont()
            font.setPixelSize(20)
            title = QLabel("Nessuno ha ancora consegnato questo compito", self)
            title.setFont(font)
            box.addWidget(title, alignment=Qt.AlignCenter)

        widget = QWidget(self, flags=Qt.Widget)
        widget.setLayout(box)
        scroll = QScrollArea(self)
        scroll.setWidget(widget)
        scroll.setObjectName("scroll")
        scroll.setStyleSheet("QWidget#scroll {border: 0px solid grey}")
        box = QHBoxLayout(self)
        box.setContentsMargins(0,0,0,0)
        box.addWidget(scroll)

        for i in self.code_widgets:
            i.hide()

    def make_student_widget(self, solution):
        font = QFont()
        font.setPixelSize(20)

        title = QLabel(solution['username'], self)
        title.setFont(font)
        title.setFixedWidth(100)

        font.setPixelSize(15)

        pixmap = QPixmap('img/' + solution['current_image'])
        pixmap = pixmap.scaled(85, 85)
        img = QLabel(self)
        img.setPixmap(pixmap)
        img.setObjectName('img/' + solution['current_image'])

        box = QHBoxLayout(self)
        box.setSpacing(20)
        box.setContentsMargins(10, 1, 10, 1)
        box.setAlignment(Qt.AlignVCenter)
        box.addWidget(title, alignment=Qt.AlignLeft)
        box.addWidget(img, alignment=Qt.AlignRight)
        who = QWidget(self, flags=Qt.Widget)
        who.setLayout(box)
        who.setFixedHeight(90)

        date = solution['delivery_date'].split(' ')
        date_day = QLabel(date[0].split('-')[2] + '/' + date[0].split('-')[1] + '/' + date[0].split('-')[0], self)
        date_day.setFont(font)
        date_hour = QLabel(date[1].split(':')[0] + ':' + date[1].split(':')[1], self)
        date_hour.setFont(font)
        box = QHBoxLayout(self)
        box.setContentsMargins(25, 10, 40, 10)
        box.addWidget(date_day, alignment=Qt.AlignLeft)
        box.addWidget(date_hour, alignment=Qt.AlignRight)
        date = QWidget(self, flags=Qt.Widget)
        date.setLayout(box)
        date.setObjectName("date")
        date.setStyleSheet("QWidget#date {border: 0px solid grey; "
                           "border-bottom: 1px solid grey; border-top: 1px solid grey;}")

        resources = {
            'lines': int(solution['resources_used'].split(',')[0]),
            'if': int(solution['resources_used'].split(',')[1]),
            'elif': int(solution['resources_used'].split(',')[2]),
            'else': int(solution['resources_used'].split(',')[3]),
            'conditions': int(solution['resources_used'].split(',')[4]),
            'for': int(solution['resources_used'].split(',')[5]),
            'while': int(solution['resources_used'].split(',')[6]),
            'cycles': int(solution['resources_used'].split(',')[7]),
            'def': int(solution['resources_used'].split(',')[8]),
            'variables': int(solution['resources_used'].split(',')[9])
        }

        code_solution = solution['solution']

        color_styles = solution['color_styles'].split(',')
        cs = DefaultColorStyles()
        cs.code_background_color = color_styles[0]
        cs.code_text_color = color_styles[1]
        cs.results_background_color = color_styles[2]
        cs.results_text_color = color_styles[3]
        cs.error_results_background_color = color_styles[4]
        cs.error_results_text_color = color_styles[5]
        cs.string_color = color_styles[6]
        cs.comment_color = color_styles[7]
        cs.multi_line_comment_color = color_styles[8]
        cs.keyWords[0].color = color_styles[9]
        cs.keyWords[0].bold = True if color_styles[10] == 'T' else False
        cs.keyWords[1].bold = color_styles[11]
        cs.keyWords[1].bold = True if color_styles[12] == 'T' else False
        cs.keyWords[2].bold = color_styles[13]
        cs.keyWords[2].bold = True if color_styles[14] == 'T' else False
        cs.keyWords[3].bold = color_styles[15]
        cs.keyWords[3].bold = True if color_styles[16] == 'T' else False
        cs.keyWords[4].bold = color_styles[17]
        cs.keyWords[4].bold = True if color_styles[18] == 'T' else False
        cs.keyWords[5].bold = color_styles[19]
        cs.keyWords[5].bold = True if color_styles[20] == 'T' else False
        cs.keyWords[6].bold = color_styles[21]
        cs.keyWords[6].bold = True if color_styles[22] == 'T' else False
        cs.keyWords[7].bold = color_styles[23]
        cs.keyWords[7].bold = True if color_styles[24] == 'T' else False
        cs.keyWords[8].bold = color_styles[25]
        cs.keyWords[8].bold = True if color_styles[26] == 'T' else False
        cs.keyWords[9].bold = color_styles[27]
        cs.keyWords[9].bold = True if color_styles[28] == 'T' else False
        cs.keyWords[10].bold = color_styles[29]
        cs.keyWords[10].bold = True if color_styles[30] == 'T' else False
        cs.keyWords[11].bold = color_styles[31]
        cs.keyWords[11].bold = True if color_styles[32] == 'T' else False
        cs.keyWords[12].bold = color_styles[33]
        cs.keyWords[12].bold = True if color_styles[34] == 'T' else False
        cs.keyWords[13].bold = color_styles[35]
        cs.keyWords[13].bold = True if color_styles[36] == 'T' else False
        cs.keyWords[14].bold = color_styles[37]
        cs.keyWords[14].bold = True if color_styles[38] == 'T' else False
        self.color_styles = cs

        box = QVBoxLayout(self)
        box.setSpacing(0)
        box.setContentsMargins(10, 10, 10, 8)
        box.addWidget(self.h_box('Linee di codice:', resources['lines'], self.limits['lines'], True))
        box.addWidget(self.h_box('if utilizzati:', resources['if'], self.limits['if'], False))
        box.addWidget(self.h_box('elif utilizzati:', resources['elif'], self.limits['elif'], False))
        box.addWidget(self.h_box('else utilizzati:', resources['else'], self.limits['else'], False))
        box.addWidget(self.h_box('Condizioni:', resources['conditions'], self.limits['conditions'], True))
        box.addWidget(self.h_box('for utilizzati:', resources['for'], self.limits['for'], False))
        box.addWidget(self.h_box('while utilizzati:', resources['while'], self.limits['while'], False))
        box.addWidget(self.h_box('Cicli:', resources['cycles'], self.limits['cycles'], True))
        box.addWidget(self.h_box('Funzioni:', resources['def'], self.limits['def'], True))
        box.addWidget(self.h_box('Variabili:', resources['variables'], self.limits['variables'], False))
        counter = QWidget(self, flags=Qt.Widget)
        counter.setLayout(box)

        box = QVBoxLayout(self)
        box.setSpacing(0)
        box.setContentsMargins(0, 0, 0, 0)
        box.addWidget(who)
        box.addWidget(date)
        box.addWidget(counter)
        widget = QWidget(self, flags=Qt.Widget)
        widget.setLayout(box)
        widget.setObjectName("w")
        widget.setStyleSheet("QWidget#w {background-color: white; border: 1px solid grey}")

        code_widget = self.make_code_widget(code_solution)
        code_widget.setFixedWidth(400)
        widget.mousePressEvent = partial(self.show_code, code_widget)
        self.code_widgets.append(code_widget)

        box = QHBoxLayout(self)
        box.setSpacing(0)
        box.setContentsMargins(0, 0, 0, 0)
        box.addWidget(widget)
        box.addWidget(code_widget)
        widget_final = QWidget(self, flags=Qt.Widget)
        widget_final.setLayout(box)

        return widget_final

    def h_box(self, title, value, limit, border):
        font = QFont()
        font.setPixelSize(15)
        label_title = QLabel(title, self)
        label_title.setFixedWidth(100)
        label_title.setFont(font)
        label_value = QLabel(str(value), self)
        label_value.setFont(font)
        if limit is not None and value > limit:
            label_title.setStyleSheet('color: red')
            label_value.setStyleSheet('color: red')
        box = QHBoxLayout(self)
        box.setSpacing(15)
        box.setContentsMargins(5, 5, 5, 5)
        box.addWidget(label_title)
        box.addWidget(label_value)
        widget = QWidget(self, flags=Qt.Widget)
        widget.setLayout(box)
        if border:
            widget.setObjectName("widget")
            widget.setStyleSheet("QWidget#widget {border: 0px solid grey; border-bottom: 1px solid grey}")
        return widget

    def make_code_widget(self, code_solution):
        code_editor = QTextEdit(self)
        code_editor.setReadOnly(True)
        code_editor.setLineWrapMode(code_editor.NoWrap)
        code_editor.setObjectName("code_editor")
        code_editor.setStyleSheet("QWidget#code_editor {background-color: " + self.color_styles.code_background_color
                                  + "; color: " + self.color_styles.code_text_color + ";}")

        results = QPlainTextEdit(self)
        results.setReadOnly(True)
        results.setLineWrapMode(results.NoWrap)
        results.setObjectName("results")
        results.setStyleSheet("QWidget#results {background-color: " + self.color_styles.results_background_color
                              + "; color: " + self.color_styles.results_text_color + ";}")

        code_editor.setText(code_solution)
        self.format_text(code_editor)

        if not self.exercise_window.exercise.executable:
            results.hide()
        else:
            temp_vars = {}
            try:
                stream = io.StringIO()
                with contextlib.redirect_stdout(stream):
                    exec(code_editor.toPlainText(), globals(), temp_vars)
                result = stream.getvalue()
                code_compile = True
            except Exception as E:
                result = str(E)
                code_compile = False

                i = 0
                temp_result = ''
                texts = code_editor.toPlainText().split('\n')
                text = texts[i]
                while i < len(texts):
                    try:
                        stream = io.StringIO()
                        with contextlib.redirect_stdout(stream):
                            exec(text, globals(), temp_vars)
                        temp_result = stream.getvalue()
                    except Exception as E:
                        temp_result = temp_result
                    i += 1
                    if i < len(texts):
                        text += '\n' + texts[i]
                if temp_result != '':
                    result = temp_result + '\n' + result

            results.setPlainText(result)
            if code_compile:
                results.setStyleSheet(
                    "QWidget#results {background-color: " + self.color_styles.results_background_color
                    + "; color: " + self.color_styles.results_text_color + ";}")
            else:
                results.setStyleSheet("QWidget#results {background-color: "
                                      + self.color_styles.error_results_background_color + "; color: "
                                      + self.color_styles.error_results_text_color + ";}")

        font = QFont()
        font.setFamily(self.exercise_window.data.code_font_family)
        font.setPixelSize(self.exercise_window.data.code_font_size)
        code_editor.setFont(font)
        results.setFont(font)

        coding_widget = QSplitter()
        coding_widget.addWidget(code_editor)
        coding_widget.addWidget(results)
        coding_widget.setSizes([150, 100])
        coding_widget.setChildrenCollapsible(True)
        coding_widget.setObjectName("coding_widget")
        coding_widget.setStyleSheet("QWidget#coding_widget {background-color: white; border: 1px solid grey; "
                                    "border-left: 0px solid grey;}")
        coding_widget.setOrientation(Qt.Vertical)
        return coding_widget

    def color_strings(self, text):
        texts = []
        multi_line_comment, comment, string_start, i, start = False, False, None, 0, 0
        while i < len(text):
            if text[i] == '#' and string_start is None and not multi_line_comment and not comment:
                if i != start:
                    texts.append(text[start:i])
                    start = i
                text = text[0:i] + '<span style=\" color:' + self.color_styles.comment_color \
                       + ';\">' + text[i:len(text)]
                i += len('<span style=\" color:' + self.color_styles.comment_color + ';\">')
                comment = True
            elif (text[i] == '"' or text[i] == "'") and comment is False:
                if string_start is None:
                    if i + 2 < len(text) and text[i + 1] == text[i] and text[i + 2] == text[i]:
                        if i != start:
                            texts.append(text[start:i])
                            start = i
                        text = text[0:i] + '<span style=\" color:' + self.color_styles.multi_line_comment_color \
                               + ';\">' + text[i:len(text)]
                        i += len('<span style=\" color:' + self.color_styles.multi_line_comment_color + ';\">') + 2
                        multi_line_comment = True
                        string_start = text[i]
                    elif not multi_line_comment:
                        if i != start:
                            texts.append(text[start:i])
                            start = i
                        text = text[0:i] + '<span style=\" color:' + self.color_styles.string_color \
                               + ';\">' + text[i:len(text)]
                        i += len('<span style=\" color:' + self.color_styles.string_color + ';\">')
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

    @staticmethod
    def my_find_and_replace(text, word, new_word, replace):
        new_text = ""
        pos = re.search(r'\b(' + word + r')\b', text)
        while pos is not None:
            if replace:
                new_text += text[0: pos.start()] + new_word
                text = text[pos.start() + len(word): len(text)]
                pos = re.search(r'\b(' + word + r')\b', text)
        new_text += text
        return new_text

    def format_text(self, code_editor):
        text = code_editor.toPlainText()
        if text is '':
            return

        temp_text = text
        texts = self.color_strings(text)
        text = ''
        for i in range(0, len(texts)):
            if texts[i] != '' and texts[i][0] != '<':
                for word in self.color_styles.keyWords:
                    texts[i] = self.my_find_and_replace(texts[i], word.word, word.tagged_word(), True)
            text += texts[i]
        if self.exercise_window.exercise.white_paper_mode:
            text = temp_text
        if text[0] == '\n':
            text = ' ' + text
        if text[-1] == '\n':
            text = text + ' '
        text = '<pre>' + text + '</pre>'
    
        code_editor.setText(text)

    @staticmethod
    def show_code(code_widget, event):
        if code_widget.isVisible():
            code_widget.hide()
        else:
            code_widget.show()

