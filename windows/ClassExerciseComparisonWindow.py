import re
from functools import partial
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QPixmap, QIcon
from PyQt5.QtWidgets import QDialog, QWidget, QVBoxLayout, QLabel, QHBoxLayout, QScrollArea, QTextEdit, \
    QPlainTextEdit, QSplitter, QCheckBox, QButtonGroup, QPushButton, QLineEdit, QAbstractButton
from Data import DefaultColorStyles
import Server_call_master


class ClassExerciseComparisonWindow(QDialog):
    def __init__(self, title, class_solutions, order_by, exercise_limit, exercise_window, parent=None):
        QDialog.__init__(self, parent, flags=Qt.Dialog)
        self.setWindowTitle(title)
        self.setWindowIcon(QIcon("img/logo.png"))
        self.setMinimumWidth(1200)
        self.exercise_window = exercise_window
        self.parent = parent
        self.limits = exercise_limit
        self.color_styles = None
        self.code_widgets = []
        self.evaluation_buttons = []
        self.comments_text = {}

        if self.exercise_window.data.my_name not in self.exercise_window.data.my_proff:
            for i in class_solutions:
                if i['visible'] == '0':
                    class_solutions.remove(i)

        order_by = int(order_by)
        if order_by == 1 or order_by == 2:
            order_by -= 1
            for i in range(0, len(class_solutions) - 1):
                for j in range(i + 1, len(class_solutions)):
                    if int(class_solutions[j]['resources_used'].split(',')[order_by]) < \
                            int(class_solutions[i]['resources_used'].split(',')[order_by]):
                        t = class_solutions[i].copy()
                        class_solutions[i] = class_solutions[j].copy()
                        class_solutions[j] = t.copy()
            order_by += 1
        elif order_by == 3:
            for i in range(0, len(class_solutions) - 1):
                for j in range(i + 1, len(class_solutions)):
                    if int(class_solutions[j]['resources_used'].split(',')[2]) + \
                            int(class_solutions[j]['resources_used'].split(',')[3]) + \
                            int(class_solutions[j]['resources_used'].split(',')[4]) < \
                            int(class_solutions[i]['resources_used'].split(',')[2]) + \
                            int(class_solutions[i]['resources_used'].split(',')[3]) + \
                            int(class_solutions[i]['resources_used'].split(',')[4]):
                        t = class_solutions[i].copy()
                        class_solutions[i] = class_solutions[j].copy()
                        class_solutions[j] = t.copy()
        elif order_by == 4:
            for i in range(0, len(class_solutions) - 1):
                for j in range(i + 1, len(class_solutions)):
                    if int(class_solutions[j]['resources_used'].split(',')[5]) + \
                            int(class_solutions[j]['resources_used'].split(',')[6]) < \
                            int(class_solutions[i]['resources_used'].split(',')[5]) + \
                            int(class_solutions[i]['resources_used'].split(',')[6]):
                        t = class_solutions[i].copy()
                        class_solutions[i] = class_solutions[j].copy()
                        class_solutions[j] = t.copy()
        if order_by > 0:
            for j in range(1, 3):
                pos = 0
                for i in range(0, len(class_solutions)):
                    if int(class_solutions[pos]['impurity']) == j or int(class_solutions[pos]['impurity']) - 3 == j:
                        temp = class_solutions[pos]
                        class_solutions.pop(pos)
                        class_solutions.append(temp)
                    else:
                        pos += 1
            for j in range(0, 10):
                pos = 0
                for i in range(0, len(class_solutions)):
                    if class_solutions[pos]['evaluation'] is not None and \
                            int(class_solutions[pos]['evaluation']) == 10 - j:
                        temp = class_solutions[pos]
                        class_solutions.pop(pos)
                        class_solutions.append(temp)
                    else:
                        pos += 1
            pos = 0
            for i in range(0, len(class_solutions)):
                if class_solutions[pos]['evaluation'] is None:
                    temp = class_solutions[pos]
                    class_solutions.pop(pos)
                    class_solutions.append(temp)
                else:
                    pos += 1

        students_widgets = []
        pos = 1
        for i in class_solutions:
            students_widgets.append(self.make_student_widget(i, pos, order_by == 0))
            pos += 1

        box = QHBoxLayout(self)
        box.setAlignment(Qt.AlignLeft)
        for i in students_widgets:
            box.addWidget(i, alignment=Qt.AlignLeft)

        if len(class_solutions) == 0:
            font = QFont()
            font.setPixelSize(20)
            title = QLabel("Nessuno ha ancora consegnato questo compito", self)
            title.setFont(font)
            box.addWidget(title, alignment=Qt.AlignCenter)
        widget = QWidget(self, flags=Qt.Widget)
        widget.setLayout(box)

        font = QFont()
        font.setPixelSize(20)
        validator = "" if self.exercise_window.exercise.validation_type == 0 \
            else (", corretto da " + self.exercise_window.exercise.creator
                  if self.exercise_window.exercise.self_validation else " corretto dal prof")
        log_line = QLabel('Soluzioni della classe "' + self.exercise_window.data.my_class + '" all' + "'" +
                          'esercizio "' + self.exercise_window.exercise.title + '"' + validator)

        log_line.setFont(font)
        box = QHBoxLayout(self)
        box.addWidget(log_line)
        box.setContentsMargins(75, 0, 0, 0)
        log_line = QWidget(self, flags=Qt.Widget)
        log_line.setLayout(box)
        log_line.setObjectName("log_line")
        log_line.setStyleSheet("QWidget#log_line {border: 1px solid grey; border-right: 0px solid grey; "
                               "border-left: 0px solid grey; background-color: #ffff55}")
        log_line.setFixedHeight(50)

        scroll = QScrollArea(self)
        scroll.setWidget(widget)
        scroll.setObjectName("scroll")
        scroll.setStyleSheet("QWidget#scroll {border: 0px solid grey}")
        box = QVBoxLayout(self)
        box.setContentsMargins(0, 0, 0, 0)
        box.addWidget(log_line)
        box.addWidget(scroll)

        for i in self.code_widgets:
            i.hide()

        self.setMinimumHeight(scroll.sizeHint().height() +
                              (180 if self.exercise_window.exercise.validation_type == 0 else 235))

    def make_student_widget(self, solution, pos, order):
        font = QFont()
        font.setPixelSize(20)

        pos = QLabel(str(pos) + "°" if solution['visible'] == '1' else "(" + str(pos) + "°", self)
        pos.setFont(font)
        pos.setFixedWidth(30)

        if order:
            pos.hide()

        title_str = solution['username'] if solution['visible'] == '1' else ("(" + solution['username'] + ")" if order
                                                                             else solution['username'] + ")")
        title = QLabel(title_str, self)
        title.setFont(font)
        title.setFixedWidth(130)
        title.setWordWrap(True)

        font.setPixelSize(15)

        pixmap = QPixmap('img/' + solution['current_image'])
        pixmap = pixmap.scaled(85, 85)
        img = QLabel(self)
        img.setPixmap(pixmap)
        img.setObjectName('img/' + solution['current_image'])

        box = QHBoxLayout(self)
        box.setContentsMargins(0, 0, 0, 0)
        box.addWidget(pos)
        box.addWidget(title)
        who = QWidget(self, flags=Qt.Widget)
        who.setLayout(box)
        if solution['visible'] == '1':
            box = QHBoxLayout(self)
            box.setSpacing(0)
            box.setContentsMargins(15, 0, 15, 0)
            box.setAlignment(Qt.AlignLeft)
            box.addWidget(who)
            box.addWidget(img, alignment=Qt.AlignRight)
            who = QWidget(self, flags=Qt.Widget)
            who.setLayout(box)
            who.setFixedHeight(90)
        else:
            description = QLabel('Modalità riservata')
            description.setFont(font)
            box = QVBoxLayout(self)
            box.setAlignment(Qt.AlignVCenter)
            box.setContentsMargins(0, 0, 0, 0)
            box.setSpacing(5)
            box.addWidget(who)
            box.addWidget(description)
            who = QWidget(self, flags=Qt.Widget)
            who.setLayout(box)
            box = QHBoxLayout(self)
            box.setSpacing(0)
            box.setContentsMargins(15, 0, 15, 0)
            box.addWidget(who)
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

        evaluation_txet = "In attesa di valutazione" if solution['evaluation'] is None else \
            ("Soluzione convalidata" if self.exercise_window.exercise.validation_type in [1, 3]
                                        and int(solution['evaluation']) >= 6 else
             ("Soluzione non valida" if self.exercise_window.exercise.validation_type in [1, 3]
              else "Valutazione:  " + str(int(float(solution['evaluation'])) if float(solution['evaluation']) % 1 == 0
                                          else round(float(solution['evaluation']), 2)) + "/10"))

        evaluation_txet = QLabel(evaluation_txet, self)
        font.setBold(True)
        evaluation_txet.setFont(font)
        font.setBold(False)
        pixmap = QPixmap('img/notify.png')
        pixmap = pixmap.scaled(25, 25)
        notify = QLabel(self)
        notify.setPixmap(pixmap)
        notify.setObjectName('img/notify.png')
        if solution['evaluation'] is not None:
            notify.hide()
            if float(solution['evaluation']) >= 6:
                evaluation_txet.setStyleSheet('color: #44bb55')
            else:
                evaluation_txet.setStyleSheet('color: #bb4455')
        else:
            if (self.exercise_window.exercise.self_validation
                and self.exercise_window.exercise.creator == self.exercise_window.data.my_name) \
                    or (not self.exercise_window.exercise.self_validation
                        and self.exercise_window.data.my_name in self.exercise_window.data.my_proff):
                evaluation_txet.setStyleSheet('color: #bb4455')
            else:
                notify.hide()

        box = QHBoxLayout(self)
        box.setAlignment(Qt.AlignLeft)
        box.setContentsMargins(25, 10, 25, 10)
        box.addWidget(notify)
        box.addWidget(evaluation_txet)
        evaluation = QWidget(self, flags=Qt.Widget)
        evaluation.setLayout(box)
        evaluation.setObjectName("evaluation")
        evaluation.setStyleSheet("QWidget#evaluation {border: 0px solid grey; border-bottom: 1px solid grey}")

        if self.exercise_window.exercise.validation_type == 0:
            evaluation.hide()

        resources = {
            'lines': int(solution['resources_used'].split(',')[0]),
            'if': int(solution['resources_used'].split(',')[2]),
            'elif': int(solution['resources_used'].split(',')[3]),
            'else': int(solution['resources_used'].split(',')[4]),
            'conditions': int(solution['resources_used'].split(',')[2]) +
                          int(solution['resources_used'].split(',')[3]) +
                          int(solution['resources_used'].split(',')[4]),
            'for': int(solution['resources_used'].split(',')[5]),
            'while': int(solution['resources_used'].split(',')[6]),
            'cycles': int(solution['resources_used'].split(',')[5]) + int(solution['resources_used'].split(',')[6]),
            'def': int(solution['resources_used'].split(',')[7]),
            'variables': int(solution['resources_used'].split(',')[1])
        }

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
        box.addWidget(self.h_box('Selezioni:', resources['conditions'], self.limits['conditions'], True))
        box.addWidget(self.h_box('for utilizzati:', resources['for'], self.limits['for'], False))
        box.addWidget(self.h_box('while utilizzati:', resources['while'], self.limits['while'], False))
        box.addWidget(self.h_box('Cicli:', resources['cycles'], self.limits['cycles'], True))
        box.addWidget(self.h_box('Funzioni:', resources['def'], self.limits['def'], True))
        box.addWidget(self.h_box('Variabili:', resources['variables'], self.limits['variables'], False))
        counter = QWidget(self, flags=Qt.Widget)
        counter.setLayout(box)

        if self.exercise_window.data.comments_visible:
            pixmap = QPixmap('img/like.png')
            pixmap = pixmap.scaled(18, 18)
            like = QLabel(self)
            like.setPixmap(pixmap)
            like.setObjectName('img/like.png')

            pixmap = QPixmap('img/user_like.png')
            pixmap = pixmap.scaled(18, 18)
            user_like = QLabel(self)
            user_like.setPixmap(pixmap)
            user_like.setObjectName('img/user_like.png')

            like_number = QLabel("0", self)
            like_number.setFont(font)
            if solution['users_like'] is not None:
                like_number.setText(str(len(solution['users_like'].split(","))))
                if solution['users_like'] == self.exercise_window.data.my_name or \
                        solution['users_like'].__contains__(self.exercise_window.data.my_name + ",") or \
                        solution['users_like'].__contains__("," + self.exercise_window.data.my_name):
                    like.hide()
                else:
                    user_like.hide()
            else:
                user_like.hide()

            box = QHBoxLayout(self)
            box.setAlignment(Qt.AlignLeft)
            box.setContentsMargins(0, 0, 0, 0)
            box.addWidget(like)
            box.addWidget(user_like)
            box.addWidget(like_number)
            like_w = QWidget(self, flags=Qt.Widget)
            like_w.setLayout(box)

            pixmap = QPixmap('img/dislike.png')
            pixmap = pixmap.scaled(18, 18)
            dislike = QLabel(self)
            dislike.setPixmap(pixmap)
            dislike.setObjectName('img/dislike.png')

            pixmap = QPixmap('img/user_dislike.png')
            pixmap = pixmap.scaled(18, 18)
            user_dislike = QLabel(self)
            user_dislike.setPixmap(pixmap)
            user_dislike.setObjectName('img/user_dislike.png')

            dislike_number = QLabel("0", self)
            dislike_number.setFont(font)
            if solution['users_dislike'] is not None:
                dislike_number.setText(str(len(solution['users_dislike'].split(","))))
                if solution['users_dislike'] == self.exercise_window.data.my_name or \
                        solution['users_dislike'].__contains__(self.exercise_window.data.my_name + ",") or \
                        solution['users_dislike'].__contains__("," + self.exercise_window.data.my_name):
                    dislike.hide()
                else:
                    user_dislike.hide()
            else:
                user_dislike.hide()

            box = QHBoxLayout(self)
            box.setAlignment(Qt.AlignLeft)
            box.setContentsMargins(0, 0, 0, 0)
            box.addWidget(dislike)
            box.addWidget(user_dislike)
            box.addWidget(dislike_number)
            dislike_w = QWidget(self, flags=Qt.Widget)
            dislike_w.setLayout(box)

            if solution['username'] == self.exercise_window.data.my_name:
                like.setEnabled(False)
                dislike.setEnabled(False)
            else:
                like_w.mousePressEvent = partial(self.like_on_click, like, user_like, like_number, dislike,
                                                 user_dislike,
                                                 dislike_number, solution)
                dislike_w.mousePressEvent = partial(self.dislike_on_click, like, user_like, like_number, dislike,
                                                    user_dislike, dislike_number, solution)

            pixmap = QPixmap('img/comments.png')
            pixmap = pixmap.scaled(18, 18)
            comments = QLabel(self)
            comments.setPixmap(pixmap)
            comments.setObjectName('img/comments.png')

            pixmap = QPixmap('img/user_comments.png')
            pixmap = pixmap.scaled(18, 18)
            user_comments = QLabel(self)
            user_comments.setPixmap(pixmap)
            user_comments.setObjectName('img/user_comments.png')

            comments_number = QLabel("0", self)
            comments_number.setFont(font)
            if solution['users_comments'] is not None:
                comments_number.setText(str(len(solution['users_comments'].split("<b>")) - 1))
                self.comments_text[solution['username']] = solution['users_comments']
                if solution['users_comments'].__contains__("<b>" + self.exercise_window.data.my_name + "</b>"):
                    comments.hide()
                else:
                    user_comments.hide()
            else:
                user_comments.hide()
                self.comments_text[solution['username']] = ""

            box = QHBoxLayout(self)
            box.setAlignment(Qt.AlignLeft)
            box.setContentsMargins(0, 0, 0, 0)
            box.addWidget(comments)
            box.addWidget(user_comments)
            box.addWidget(comments_number)
            comments_w = QWidget(self, flags=Qt.Widget)
            comments_w.setLayout(box)

            box = QHBoxLayout(self)
            box.setContentsMargins(35, 10, 35, 10)
            box.addWidget(like_w)
            box.addWidget(dislike_w)
            box.addWidget(comments_w)
            social = QWidget(self, flags=Qt.Widget)
            social.setLayout(box)
            social.setObjectName("social")
            social.setStyleSheet("QWidget#social {border: 0px solid grey; border-top: 1px solid grey}")

        box = QVBoxLayout(self)
        box.setSpacing(0)
        box.setContentsMargins(0, 0, 0, 0)
        box.addWidget(who)
        box.addWidget(date)
        if self.exercise_window.exercise.validation_type > 0:
            box.addWidget(evaluation)
        box.addWidget(counter)
        if self.exercise_window.data.comments_visible:
            box.addWidget(social)
        widget = QWidget(self, flags=Qt.Widget)
        widget.setLayout(box)
        widget.setObjectName("w")
        widget.setStyleSheet("QWidget#w {background-color: white; border: 1px solid grey}")

        if self.exercise_window.data.comments_visible:
            comment_text = QTextEdit(self)
            comment_text.setReadOnly(True)
            comment_text.setFont(font)
            comment_text.setText(self.comments_text[solution['username']])
            comment_editor = QTextEdit(self)
            comment_editor.setFixedHeight(100)
            comment_editor.setFont(font)
            comment_send_button = QPushButton("Invia", self)
            comment_send_button.setFixedHeight(40)
            comment_send_button.setEnabled(False)
            comment_send_button.setFont(font)
            comment_editor.textChanged.connect(partial(self.comment_edit, comment_editor, comment_send_button))
            comment_send_button.clicked.connect(
                partial(self.comment_send, comment_text, self.exercise_window.data.my_name,
                        comment_editor, comments_number, comments, user_comments,
                        solution['username']))
            box = QVBoxLayout(self)
            box.setContentsMargins(0, 1, 0, 1)
            box.setSpacing(0)
            box.addWidget(comment_text)
            box.addWidget(comment_editor)
            box.addWidget(comment_send_button)
            comments_area = QWidget(self, flags=Qt.Widget)
            comments_area.setLayout(box)
            comments_area.setFixedWidth(250)
            comments_area.setObjectName("comments_area")
            comments_area.setStyleSheet("QWidget#comments_area {border: 1px solid grey}")
            self.code_widgets.append(comments_area)

            comments_w.mousePressEvent = partial(self.comments_on_click, comments_area)

        code_widget = self.make_code_widget(solution['solution'], solution['result'], solution['code_compile'] == '1',
                                            solution['evaluation'] is None, notify, evaluation_txet,
                                            solution['username'])
        code_widget.setFixedWidth(400)
        widget.mousePressEvent = partial(self.show_code, code_widget)
        self.code_widgets.append(code_widget)

        box = QHBoxLayout(self)
        box.setSpacing(0)
        box.setContentsMargins(0, 0, 0, 0)
        box.addWidget(widget)
        if self.exercise_window.data.comments_visible:
            box.addWidget(comments_area)
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

    def make_code_widget(self, code_solution, result, code_compile, evaluation, correction_img, correction_text, user):
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
        coding_widget.setOrientation(Qt.Vertical)

        if evaluation and ((self.exercise_window.exercise.self_validation
                            and self.exercise_window.exercise.creator == self.exercise_window.data.my_name)
                           or (not self.exercise_window.exercise.self_validation
                               and self.exercise_window.data.my_name in self.exercise_window.data.my_proff)):
            font = QFont()
            font.setPixelSize(15)
            intro = QLabel("Valuta la soluzione:", self)
            intro.setContentsMargins(20, 0, 0, 0)
            intro.setFont(font)

            send_button = QPushButton("Invia", self)
            send_button.setFixedSize(80, 50)
            send_button.setEnabled(False)

            temp_form = None
            temp_bg = None

            if self.exercise_window.exercise.validation_type in [1, 3]:
                check_1 = QCheckBox("Valida")
                check_1.setFont(font)
                check_2 = QCheckBox("Non valida")
                check_2.setFont(font)

                bg = QButtonGroup()
                bg.addButton(check_1, 1)
                bg.addButton(check_2, 2)
                bg.buttonClicked[QAbstractButton].connect(partial(self.correction_check_changed, send_button))
                temp_bg = bg
                self.evaluation_buttons.append(bg)

                box = QHBoxLayout(self)
                box.setAlignment(Qt.AlignLeft)
                box.setSpacing(20)
                box.addWidget(check_1)
                box.addWidget(check_2)
                correction = QWidget(self, flags=Qt.Widget)
                correction.setLayout(box)
            else:
                correction = QLineEdit(self)
                correction.setPlaceholderText(" Valore compreso tra 0 e 10 ")
                correction.textChanged.connect(partial(self.correction_form_changed, correction, send_button))
                correction.setFont(font)
                correction.setFixedWidth(225)
                correction.setContentsMargins(10, 5, 0, 5)
                temp_form = correction

            box = QVBoxLayout(self)
            box.addWidget(intro)
            box.addWidget(correction)
            correction = QWidget(self, flags=Qt.Widget)
            correction.setLayout(box)

            box = QHBoxLayout(self)
            box.setContentsMargins(0, 0, 40, 0)
            box.addWidget(correction)
            box.addWidget(send_button, alignment=Qt.AlignRight)
            correction = QWidget(self, flags=Qt.Widget)
            correction.setLayout(box)
            correction.setObjectName("correction")
            correction.setStyleSheet("QWidget#correction {background-color: white; border: 1px solid grey}")

            send_button.clicked.connect(partial(self.send_button_onclick, correction, correction_img, correction_text,
                                                temp_form, temp_bg, user))

            if self.exercise_window.exercise.validation_type == 0:
                correction.hide()

            box = QVBoxLayout(self)
            box.setContentsMargins(0, 0, 0, 0)
            box.addWidget(coding_widget)
            box.addWidget(correction)
            coding_widget = QWidget(self, flags=Qt.Widget)
            coding_widget.setLayout(box)

        coding_widget.setObjectName("coding_widget")
        coding_widget.setStyleSheet("QWidget#coding_widget {border: 1px solid grey; border-right: 0px solid grey;"
                                    "border-left: 0px solid grey}")
        return coding_widget

    @staticmethod
    def correction_check_changed(button, btn):
        button.setEnabled(True)

    @staticmethod
    def correction_form_changed(input_form, button):
        try:
            if 0 <= float(input_form.text()) <= 10:
                input_form.setStyleSheet('color: black')
                button.setEnabled(True)
            else:
                input_form.setStyleSheet('color: #bb4455')
                button.setEnabled(False)
        except ValueError:
            input_form.setStyleSheet('color: #bb4455')
            button.setEnabled(False)

    def send_button_onclick(self, widget, img, text, form, bg, user):
        if form is None:
            ris = 10 if bg.checkedId() == 1 else 0
        else:
            ris = round(float(form.text()), 2)

        if Server_call_master.set_variable("/evaluate_exercise.php", {'username': self.exercise_window.data.my_name,
                                                                      'password': self.exercise_window.data.my_psw,
                                                                      'class': self.exercise_window.data.my_class,
                                                                      'id': self.exercise_window.exercise.id,
                                                                      'vote': ris, 'username2': user}):
            if ris % 1 == 0:
                ris = int(ris)
            widget.hide()
            img.hide()
            if form is None:
                if ris >= 6:
                    text.setText("Soluzione convalidata")
                else:
                    text.setText("Soluzione non valida")
            else:
                text.setText("Valutazione:  " + str(ris) + "/10")
            if ris >= 6:
                text.setStyleSheet('color: #44bb55')
            else:
                text.setStyleSheet('color: #bb4455')
            if user == self.exercise_window.data.my_name:
                self.exercise_window.new_evaluation(ris)
            else:
                self.exercise_window.new_evaluation()

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
            temp_text = temp_text.replace('<', '&#60;')
            temp_text = temp_text.replace('>', '&#62;')
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

    def like_on_click(self, like, user_like, like_number, dislike, user_dislike, dislike_number, solution, event):
        if Server_call_master.set_variable("/exercise_add_like.php", {'username': self.exercise_window.data.my_name,
                                                                      'password': self.exercise_window.data.my_psw,
                                                                      'class': self.exercise_window.data.my_class,
                                                                      'id': self.exercise_window.exercise.id,
                                                                      'username2': solution['username']}):
            if solution['users_like'] is None:
                solution['users_like'] = self.exercise_window.data.my_name
                like_number.setText("1")
                like.hide()
                user_like.show()
            elif solution['users_like'] == self.exercise_window.data.my_name:
                solution['users_like'] = None
                like_number.setText("0")
                like.show()
                user_like.hide()
            elif solution['users_like'].__contains__(self.exercise_window.data.my_name + ",") or \
                    solution['users_like'].__contains__("," + self.exercise_window.data.my_name):
                solution['users_like'] = solution['users_like'].replace(self.exercise_window.data.my_name + ",", "")
                solution['users_like'] = solution['users_like'].replace("," + self.exercise_window.data.my_name, "")
                like_number.setText(str(int(like_number.text()) - 1))
                like.show()
                user_like.hide()
            else:
                solution['users_like'] = solution['users_like'] + ',' + self.exercise_window.data.my_name
                like_number.setText(str(int(like_number.text()) + 1))
                like.hide()
                user_like.show()

            if solution['users_dislike'] == self.exercise_window.data.my_name:
                solution['users_dislike'] = None
                dislike.show()
                user_dislike.hide()
                dislike_number.setText(str(int(dislike_number.text()) - 1))
            elif solution['users_dislike'] is not None and \
                    (solution['users_dislike'].__contains__(self.exercise_window.data.my_name + ",") or
                     solution['users_dislike'].__contains__("," + self.exercise_window.data.my_name)):
                solution['users_dislike'] = \
                    solution['users_dislike'].replace(self.exercise_window.data.my_name + ",", "")
                solution['users_dislike'] = \
                    solution['users_dislike'].replace("," + self.exercise_window.data.my_name, "")
                dislike.show()
                user_dislike.hide()
                dislike_number.setText(str(int(dislike_number.text()) - 1))

    def dislike_on_click(self, like, user_like, like_number, dislike, user_dislike, dislike_number, solution, event):
        if Server_call_master.set_variable("/exercise_add_dislike.php", {'username': self.exercise_window.data.my_name,
                                                                         'password': self.exercise_window.data.my_psw,
                                                                         'class': self.exercise_window.data.my_class,
                                                                         'id': self.exercise_window.exercise.id,
                                                                         'username2': solution['username']}):
            if solution['users_dislike'] is None:
                solution['users_dislike'] = self.exercise_window.data.my_name
                dislike_number.setText("1")
                dislike.hide()
                user_dislike.show()
            elif solution['users_dislike'] == self.exercise_window.data.my_name:
                solution['users_dislike'] = None
                dislike_number.setText("0")
                dislike.show()
                user_dislike.hide()
            elif solution['users_dislike'].__contains__(self.exercise_window.data.my_name + ",") or \
                    solution['users_dislike'].__contains__("," + self.exercise_window.data.my_name):
                solution['users_dislike'] = \
                    solution['users_dislike'].replace(self.exercise_window.data.my_name + ",", "")
                solution['users_dislike'] = \
                    solution['users_dislike'].replace("," + self.exercise_window.data.my_name, "")
                dislike_number.setText(str(int(dislike_number.text()) - 1))
                dislike.show()
                user_dislike.hide()
            else:
                solution['users_dislike'] = solution['users_dislike'] + ',' + self.exercise_window.data.my_name
                dislike_number.setText(str(int(dislike_number.text()) + 1))
                dislike.hide()
                user_dislike.show()

            if solution['users_like'] == self.exercise_window.data.my_name:
                solution['users_like'] = None
                like.show()
                user_like.hide()
                like_number.setText(str(int(like_number.text()) - 1))
            elif solution['users_like'] is not None and \
                    (solution['users_like'].__contains__(self.exercise_window.data.my_name + ",") or
                     solution['users_like'].__contains__("," + self.exercise_window.data.my_name)):
                solution['users_like'] = solution['users_like'].replace(self.exercise_window.data.my_name + ",", "")
                solution['users_like'] = solution['users_like'].replace("," + self.exercise_window.data.my_name, "")
                like.show()
                user_like.hide()
                like_number.setText(str(int(like_number.text()) - 1))

    @staticmethod
    def comments_on_click(comments_area, event):
        if comments_area.isVisible():
            comments_area.hide()
        else:
            comments_area.show()

    @staticmethod
    def comment_edit(text, button):
        if text.toPlainText() != "":
            button.setEnabled(True)
        else:
            button.setEnabled(False)

    def comment_send(self, area, name, text, number, comments, user_comments, user):
        s = text.toPlainText().strip()
        s = s.replace("<", "&#60;")
        s = s.replace("<", "&#62;")
        s = s.replace("\n", "<br>")

        r = Server_call_master.exercise_add_comment({'username': self.exercise_window.data.my_name,
                                                     'password': self.exercise_window.data.my_psw,
                                                     'class': self.exercise_window.data.my_class,
                                                     'id': self.exercise_window.exercise.id, 'username2': user,
                                                     'comment': ("<b>" + name + "</b><br>" + s + "<br><br>")})
        if r != "":
            self.comments_text[user] = r
            area.setText(self.comments_text[user])
            text.setText("")
            number.setText(str(int(number.text()) + 1))
            comments.hide()
            user_comments.show()
