import json
from functools import partial
from os import path, listdir

from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtWidgets import QWidget, QPushButton, QHBoxLayout, QVBoxLayout, QScrollArea, QLabel, QDialog
from PyQt5.QtCore import *

from Data import Exercise
from windows.BookExerciseWindow import BookExerciseWindow
from windows.CreateHomeworkWindow import CreateHomeworkWindow


class ExercisesCollectionWindow(QWidget):
    def __init__(self, home, data):
        super(ExercisesCollectionWindow, self).__init__(home, flags=Qt.Widget)
        home.setWindowTitle("Eserciziario")
        self.data = data
        self.home = home
        self.pages = {'0': None}
        self.new_exercise = None

        if self.data.my_name in self.data.my_proff:
            self.data.get_homework()

        top_widget = self.make_top_widget()
        bottom_widget = self.make_bottom_widget()

        window_layaut = QVBoxLayout(self)
        window_layaut.addWidget(top_widget)
        window_layaut.addWidget(bottom_widget)
        window_layaut.setContentsMargins(0, 0, 0, 0)
        window_layaut.setSpacing(0)

        self.info = QLabel('', self)
        self.info.setStyleSheet("border: 1px solid grey; background-color: #ffdd99}")
        self.info.setAlignment(Qt.AlignCenter)
        self.info.hide()

    def show_text(self, text, dim, rif, event):
        self.info.setText(text)
        self.info.show()
        self.info.setFixedWidth(dim)
        pos_x, pos_y = rif.pos().x(), rif.pos().y()
        parent = rif.parent()
        while parent and parent is not self:
            pos_x += parent.pos().x()
            pos_y += parent.pos().y()
            parent = parent.parent()
        self.info.move(pos_x + rif.width() / 5, pos_y + rif.height() / 5 * 4)

    def hide_text(self, event):
        self.info.hide()

    def make_top_widget(self):
        font = QFont()
        font.setPixelSize(15)

        home_button = QPushButton('HOME', self)
        home_button.setFixedSize(100, 50)
        home_button.clicked.connect(self.home.open_MainWindow)
        home_button.setFont(font)
        home_button.setStyleSheet('background-color: #ffdd55')

        free_editor = QPushButton('PAGINA VUOTA', self)
        free_editor.clicked.connect(self.open_void_page)
        free_editor.setFixedSize(250, 50)
        free_editor.setFont(font)
        free_editor.setStyleSheet("background-color: #ffdd55")

        l = 1
        old = 0
        for i in self.data.level_progression:
            if self.data.level >= i:
                l += 1
                old = i

        level_number = QLabel('Liv. ' + str(l), self)
        level_number.setFont(font)
        level_number.setStyleSheet('background-color: #9999FF; border: 1px solid grey')
        level_number.setFixedSize(90, 40)
        level_number.setContentsMargins(20, 10, 20, 10)

        level_bar = QLabel(self)
        level_bar.setStyleSheet('background-color: #4040FF')
        level_bar.setFixedSize(int(90*(self.data.level-old)/(self.data.level_progression[l-1]-old)), 5)

        box = QVBoxLayout(self)
        box.setSpacing(0)
        box.setContentsMargins(0, 0, 0, 0)
        box.addWidget(level_number)
        box.addWidget(level_bar)
        level = QWidget(self, flags=Qt.Widget)
        level.setLayout(box)
        level.setObjectName("level")
        level.setStyleSheet("QWidget#level {border: 1px solid grey; background-color: #BBBBFF}")

        soldi = QLabel(str(self.data.money) + ' soldi', self)
        soldi.setFont(font)
        soldi.setStyleSheet('background-color: #ffea00; border: 1px solid grey')
        soldi.setFixedHeight(45)
        soldi.setContentsMargins(20, 5, 20, 5)

        box = QHBoxLayout(self)
        box.setAlignment(Qt.AlignCenter)
        box.setSpacing(5)
        box.addWidget(level)
        box.addWidget(soldi)
        box.setContentsMargins(0, 0, 0, 0)
        soldi_widget = QWidget(self, flags=Qt.Widget)
        soldi_widget.setLayout(box)

        font.setPixelSize(25)
        font.setBold(True)
        title = QLabel("Esercizi", self)
        title.setFont(font)
        title.setStyleSheet("color: #ffffff")

        top_box = QHBoxLayout(self)
        top_box.setContentsMargins(20, 0, 20, 0)
        top_box.addWidget(home_button)
        top_box.addWidget(title)
        top_box.addWidget(free_editor, alignment=Qt.AlignRight)
        top_box.setSpacing(60)
        top_widget = QWidget(self, flags=Qt.Widget)
        top_widget.setLayout(top_box)
        top_widget.setObjectName("topStyle")
        top_widget.setStyleSheet("QWidget#topStyle {border: 0px solid grey; border-bottom: 1px solid grey; "
                                 "border-top: 1px solid grey; background-color: #ee6353}")
        top_widget.setFixedHeight(80)

        font.setPixelSize(17)
        font.setBold(False)
        log_line = QLabel('Fai pratica e guadagna esperienza.', self)
        log_line.setFont(font)
        box = QHBoxLayout(self)
        box.addWidget(log_line)
        box.addWidget(soldi_widget, alignment=Qt.AlignRight)
        box.setContentsMargins(75, 0, 5, 0)
        log_line = QWidget(self, flags=Qt.Widget)
        log_line.setLayout(box)
        log_line.setObjectName("log_line")
        log_line.setStyleSheet("QWidget#log_line {border: 0px solid grey; border-bottom: 1px solid grey; "
                               "background-color: #eda3a3}")
        log_line.setFixedHeight(55)

        top_box = QVBoxLayout(self)
        top_box.setAlignment(Qt.AlignTop)
        top_box.setContentsMargins(0, 0, 0, 0)
        top_box.setSpacing(0)
        top_box.addWidget(top_widget)
        top_box.addWidget(log_line)
        top_widget = QWidget(self, flags=Qt.Widget)
        top_widget.setLayout(top_box)
        return top_widget

    def make_bottom_widget(self):
        box = QVBoxLayout(self)
        box.setContentsMargins(20, 10, 20, 10)
        for f in listdir("exercises"):
            ex = []
            i = open("exercises/" + f, "r")
            for x in i:
                y = json.loads(x)
                ex. append(Exercise(None, None, None, y["title"], y["text"], y["level"], y["white_paper_mode"],
                                    y["start_code"], y["limits"], y["executable"], True, True, 0, False))
            box.addWidget(self.make_group_of_exercises(f.title()[2:-4], ex))
        bottom_widget = QWidget(self, flags=Qt.Widget)
        bottom_widget.setLayout(box)

        scroll = QScrollArea(self)
        scroll.setWidget(bottom_widget)
        scroll.setWidgetResizable(True)
        scroll.setObjectName("scroll")
        scroll.setStyleSheet("QWidget#scroll {border: 0px solid grey;}")
        return scroll

    def make_group_of_exercises(self, title, exercises):
        font = QFont()
        font.setPixelSize(20)
        font2 = QFont()
        font2.setPixelSize(10)
        box = QVBoxLayout(self)
        box.setSpacing(0)
        intro = QLabel(title, self)
        intro.setFont(font)
        intro.setFixedSize(700, 45)
        intro.setContentsMargins(50, 0, 50, 0)
        intro.setStyleSheet('background-color: #75a0e9')
        box.addWidget(intro)

        font.setPixelSize(17)
        internal_box = QVBoxLayout(self)
        internal_box.setAlignment(Qt.AlignTop)
        internal_box.setContentsMargins(20, 10, 20, 10)
        for i in exercises:
            ex = QLabel(str(len(self.pages)) + " - " + i.title, self)
            ex.setFont(font)
            ex.setContentsMargins(20, 10, 20, 10)
            ex.setTextFormat(Qt.RichText)
            self.pages[str(len(self.pages))] = None
            dif = QLabel('&#x25EF;' if i.level == 'Facile' else ('&#x25EF;<br>&#x25EF;' if i.level == 'Medio'
                                                                        else '&#x25EF;<br>&#x25EF;<br>&#x25EF;'), self)
            dif.setContentsMargins(0, 5, 10, 5)
            dif.setTextFormat(Qt.RichText)
            dif.setFont(font2)
            dif.enterEvent = partial(self.show_text, i.level, 60, dif)
            dif.leaveEvent = self.hide_text
            ex_box = QHBoxLayout(self)
            ex_box.setAlignment(Qt.AlignLeft)
            ex_box.addWidget(ex)
            ex_box.addWidget(dif)
            ex_box.setContentsMargins(0, 0, 0, 0)
            ex_box.setSpacing(0)
            ex = QWidget(self, flags=Qt.Widget)
            ex.setLayout(ex_box)
            solution_file = 'saves/' + i.title + '.txt'
            if (i.title.__contains__('"') or i.title.__contains__("'") or i.title.__contains__('?')
                    or i.title.__contains__('\\') or i.title.__contains__('/') or i.title.__contains__(":")
                    or i.title.__contains__("*") or i.title.__contains__("<") or i.title.__contains__(">")
                    or i.title.__contains__("|")) and path.isfile('saves/_lib.txt'):
                f = open('saves/_lib.txt', 'r')
                for j in f:
                    if j[len(j.split(':')[0])+1:-1] == i.title:
                        solution_file = 'saves/' + j.split(':')[0] + '.txt'
                f.close()

            if self.data.my_name in self.data.my_proff:
                pixmap = QPixmap('img/upload.png')
                pixmap = pixmap.scaled(50, 50)
                send_button = QLabel(self)
                send_button.setPixmap(pixmap)
                send_button.setObjectName('img/upload.png')
                send_button.mousePressEvent = partial(self.send_button_on_click, i)
                send_button.enterEvent = partial(self.show_text, "Consegna alla classe", 150, send_button)
                send_button.leaveEvent = self.hide_text
                prof_box = QHBoxLayout(self)
                prof_box.setContentsMargins(0, 0, 0, 0)
                prof_box.setSpacing(30)
                prof_box.addWidget(ex)
                prof_box.addWidget(send_button)
                ex = QWidget(self, flags=Qt.Widget)
                ex.setLayout(prof_box)

            ex.mousePressEvent = partial(self.open_exercise, i, str(len(self.pages)), ex)
            if path.isfile(solution_file):
                f = open(solution_file, "r")
                i.solution = f.read()
                ex.setStyleSheet('background-color: #99dd99')
                f.close()
            else:
                ex.setStyleSheet('background-color: #dd6666')

            internal_box.addWidget(ex, alignment=Qt.AlignLeft)
        group_widget = QWidget(self, flags=Qt.Widget)
        group_widget.setLayout(internal_box)

        box.addWidget(group_widget)
        group_widget = QWidget(self, flags=Qt.Widget)
        group_widget.setLayout(box)
        return group_widget

    def open_exercise(self, exercise, pos, widget, event):
        if self.pages[pos] is None:
            self.pages[pos] = BookExerciseWindow(exercise, self.data, widget)
            self.pages[pos].show()
        else:
            self.pages[pos].hide()
            self.pages[pos].show()

    def open_void_page(self):
        if self.pages['0'] is None:
            self.pages['0'] = BookExerciseWindow(Exercise(None, None, None, "Pagina vuota", None, 'Facile', False, "", {'lines': None, 'variables': None, 'if': None, 'elif': None, 'else': None, 'conditions': None, 'for': None, 'while': None, 'cycles': None, 'def': None}, True, False, False, 0, False), self.data, None)
            self.pages['0'].show()
        else:
            self.pages['0'].show()

    def send_button_on_click(self, exercise, event):
        if self.new_exercise is None or self.new_exercise.exercise.title != exercise.title:
            self.new_exercise = CreateHomeworkWindow(self.data, self, exercise=exercise)
            self.new_exercise.show()
        else:
            self.new_exercise.hide()
            self.new_exercise.show()

    def close_CreateHomeworkWindow(self):
        self.new_exercise.close()
        self.new_exercise = None
