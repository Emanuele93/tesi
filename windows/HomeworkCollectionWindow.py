import threading
from functools import partial

from PyQt5.QtGui import QFont, QPixmap, QMovie
from PyQt5.QtWidgets import QWidget, QPlainTextEdit, QPushButton, QHBoxLayout, QVBoxLayout, QScrollArea, QLabel
from PyQt5.QtCore import *

from windows.CreateHomeworkWindow import CreateHomeworkWindow
from windows.ExerciseWindow import ExerciseWindow


class HomeworkCollectionWindow(QWidget):
    def __init__(self, controller, data, loading, pos):
        super(HomeworkCollectionWindow, self).__init__(controller, flags=Qt.Widget)
        controller.setWindowTitle("Gamification - Compiti")
        self.data = data
        self.controller = controller
        self.exercise_windows = []
        self.new_exercise = None
        self.pos = pos

        top_widget = self.make_top_widget()

        if loading:
            bottom_widget = QLabel()
            movie = QMovie("img/waiting.gif")
            bottom_widget.setMovie(movie)
            movie.start()
            self.change_button = QPushButton('PROVA', self)
            self.change_button.clicked.connect(partial(self.controller.open_HomeworkCollectionWindow, False, 0))
            self.change_button.hide()
            box = QHBoxLayout(self)
            box.addWidget(bottom_widget)
            box.addWidget(self.change_button)
            box.setAlignment(Qt.AlignCenter)
            bottom_widget = QWidget(self, flags=Qt.Widget)
            bottom_widget.setLayout(box)
            self.add_homework_button.setEnabled(False)
            self.home_button.setEnabled(False)
        else:
            bottom_widget = self.make_bottom_widget()

        window_layaut = QVBoxLayout(self)
        window_layaut.addWidget(top_widget)
        window_layaut.addWidget(bottom_widget)
        window_layaut.setContentsMargins(0, 0, 0, 0)
        window_layaut.setSpacing(0)

    def make_top_widget(self):
        font = QFont()
        font.setPixelSize(15)

        self.home_button = QPushButton('HOME', self)
        self.home_button.setFixedSize(100, 50)
        self.home_button.clicked.connect(self.controller.open_MainWindow)
        self.home_button.setFont(font)
        self.home_button.setStyleSheet('background-color: #ffdd55')

        l = 1
        old = 0
        for i in self.data.level_progression:
            if self.data.level >= i:
                l += 1
                old = i

        level_number = QLabel('Liv. ' + str(l), self)
        level_number.setFont(font)
        level_number.setStyleSheet('background-color: #9999FF; border: 1px solid grey')
        level_number.setFixedSize(85, 40)
        level_number.setContentsMargins(20, 10, 20, 10)

        level_bar = QLabel(self)
        level_bar.setStyleSheet('background-color: #4040FF')
        level_bar.setFixedSize(int(85*(self.data.level-old)/(self.data.level_progression[l-1]-old)), 5)

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
        box.addWidget(level)
        box.addWidget(soldi)
        box.setContentsMargins(10, 10, 10, 10)
        soldi_widget = QWidget(self, flags=Qt.Widget)
        soldi_widget.setLayout(box)

        self.add_homework_button = QPushButton('AGGIUNGI COMPITO', self)
        self.add_homework_button.clicked.connect(self.open_CreateHomeworkWindow)
        self.add_homework_button.setFixedSize(250, 50)
        self.add_homework_button.setFont(font)
        self.add_homework_button.setStyleSheet("background-color: #ffdd55")
        if not self.data.make_homework_coin:
            self.add_homework_button.setEnabled(False)

        top_box = QHBoxLayout(self)
        top_box.setContentsMargins(20, 0, 20, 0)
        top_box.addWidget(self.home_button)
        top_box.addWidget(soldi_widget, alignment=Qt.AlignTop)
        top_box.addWidget(self.add_homework_button, alignment=Qt.AlignRight)
        top_box.setSpacing(80)
        top_widget = QWidget(self, flags=Qt.Widget)
        top_widget.setLayout(top_box)
        top_widget.setObjectName("topStyle")
        top_widget.setStyleSheet("QWidget#topStyle {border: 0px solid grey; border-bottom: 1px solid grey; "
                                 "border-top: 1px solid grey; background-color: #ffbd49}")
        top_widget.setFixedHeight(90)
        return top_widget

    def make_bottom_widget(self):
        font = QFont()
        font.setPixelSize(15)
        f = QFont()
        f.setPixelSize(10)

        bottom_box = QVBoxLayout(self)
        exercises = []
        for i in self.data.exercises:
            exercises.append(i)
        while len(exercises) > 0:
            date = exercises[0].date
            date_exercises = QLabel(date, self)
            date_exercises.setFixedSize(100, 50)
            date_exercises.setFont(font)

            other_exercises_box = QHBoxLayout(self)
            other_exercises_box.setAlignment(Qt.AlignLeft)
            other_exercises_box.setContentsMargins(0, 0, 0, 0)
            other_exercises_box_v = QVBoxLayout(self)
            other_exercises_box_v.setContentsMargins(0, 0, 0, 0)
            width_students = 0

            proff_exercises_box = QHBoxLayout(self)
            proff_exercises_box.setAlignment(Qt.AlignLeft)
            proff_exercises_box.setContentsMargins(0, 0, 0, 0)
            width = 0
            proff_exercises_box_v = QVBoxLayout(self)
            proff_exercises_box_v.setContentsMargins(0, 0, 0, 0)

            proff_counter = other_counter = 0
            temp_exercises = []
            for i in exercises:
                if i.date == date:
                    temp_exercises.append(i)
                    title = QLabel(i.title, self)
                    title.setFont(font)
                    title.setContentsMargins(20, 10, 5, 0)

                    s = '&#x25EF;' if i.level == 'Facile' \
                        else ('&#x25EF;<br>&#x25EF;' if i.level == 'Medio' else '&#x25EF;<br>&#x25EF;<br>&#x25EF;')
                    difficulty = QLabel(s, self)
                    difficulty.setContentsMargins(10, 2, 10, 2)
                    difficulty.setTextFormat(Qt.RichText)
                    difficulty.setFont(f)

                    by = QLabel("<i>by " + i.creator + "</i>", self)
                    by.setContentsMargins(20, 0, 5, 10)
                    by.setTextFormat(Qt.RichText)

                    box = QVBoxLayout(self)
                    box.setAlignment(Qt.AlignTop)
                    box.setContentsMargins(0, 0, 0, 0)
                    box.setSpacing(0)
                    box.addWidget(title, alignment=Qt.AlignTop)
                    box.addWidget(by, alignment=Qt.AlignTop)
                    exercise = QWidget(self, flags=Qt.Widget)
                    exercise.setLayout(box)

                    box = QHBoxLayout(self)
                    box.setAlignment(Qt.AlignTop)
                    box.setContentsMargins(0, 0, 0, 0)
                    box.setSpacing(0)
                    box.addWidget(exercise, alignment=Qt.AlignVCenter)
                    box.addWidget(difficulty, alignment=Qt.AlignLeft)
                    exercise = QWidget(self, flags=Qt.Widget)
                    exercise.setLayout(box)
                    exercise.setObjectName("exercise")
                    exercise.mousePressEvent = partial(self.open_ExerciseWindow, i, False)

                    if (i.solution is None or i.solution == i.start_code) and i.delivery_date is None:
                        exercise.setStyleSheet('QWidget#exercise {background-color: #dd6666; border: 1px solid grey;}')
                    elif i.solution is not None and i.delivery_date is None:
                        exercise.setStyleSheet('QWidget#exercise {background-color: #ffff33; border: 1px solid grey};')
                    else:
                        exercise.setStyleSheet('QWidget#exercise {background-color: #66ee66; border: 1px solid grey;}')

                    if i.creator in self.data.my_proff:
                        width += exercise.sizeHint().width()
                        if width > 580:
                            width = exercise.sizeHint().width()
                            proff_exercises_widget = QWidget(self, flags=Qt.Widget)
                            proff_exercises_widget.setLayout(proff_exercises_box)
                            proff_exercises_box_v.addWidget(proff_exercises_widget)
                            proff_exercises_box = QHBoxLayout(self)
                            proff_exercises_box.setAlignment(Qt.AlignLeft)
                            proff_exercises_box.setContentsMargins(0, 0, 0, 0)
                        proff_exercises_box.addWidget(exercise)
                        proff_counter += 1
                    else:
                        width_students += exercise.sizeHint().width()
                        if width_students > 580:
                            width_students = exercise.sizeHint().width()
                            other_exercises_widget = QWidget(self, flags=Qt.Widget)
                            other_exercises_widget.setLayout(other_exercises_box)
                            other_exercises_box_v.addWidget(other_exercises_widget)
                            other_exercises_box = QHBoxLayout(self)
                            other_exercises_box.setAlignment(Qt.AlignLeft)
                            other_exercises_box.setContentsMargins(0, 0, 0, 0)
                        other_exercises_box.addWidget(exercise, alignment=Qt.AlignLeft)
                        other_counter += 1
            for i in temp_exercises:
                exercises.remove(i)


            other_exercises_widget = QWidget(self, flags=Qt.Widget)
            other_exercises_widget.setLayout(other_exercises_box)
            other_exercises_box_v.addWidget(other_exercises_widget)

            proff_exercises_widget = QWidget(self, flags=Qt.Widget)
            proff_exercises_widget.setLayout(proff_exercises_box)
            proff_exercises_box_v.addWidget(proff_exercises_widget)

            proff_exercises_widget = QWidget(self, flags=Qt.Widget)
            proff_exercises_widget.setLayout(proff_exercises_box_v)
            other_exercises_widget = QWidget(self, flags=Qt.Widget)
            other_exercises_widget.setLayout(other_exercises_box_v)
            both_exercises_box = QVBoxLayout(self)
            both_exercises_box.setContentsMargins(0, 0, 0, 0)
            both_exercises_box.addWidget(proff_exercises_widget, alignment=Qt.AlignTop)
            both_exercises_box.addWidget(other_exercises_widget, alignment=Qt.AlignTop)
            both_exercises_widget = QWidget(self, flags=Qt.Widget)
            both_exercises_widget.setLayout(both_exercises_box)

            if proff_counter == 0:
                proff_exercises_widget.hide()
            if other_counter == 0:
                other_exercises_widget.hide()

            exercises_box = QHBoxLayout(self)
            exercises_box.setContentsMargins(20, 20, 0, 20)
            exercises_box.addWidget(date_exercises, alignment=Qt.AlignTop)
            exercises_box.addWidget(both_exercises_widget, alignment=Qt.AlignLeft)
            exercises_widget = QWidget(self, flags=Qt.Widget)
            exercises_widget.setLayout(exercises_box)
            exercises_widget.setObjectName("exercises_widget")
            exercises_widget.setStyleSheet("QWidget#exercises_widget {border: 0px solid grey; "
                                           "border-bottom: 1px solid grey;}")
            bottom_box.addWidget(exercises_widget, alignment=Qt.AlignTop)
        bottom_box.setAlignment(Qt.AlignTop)
        bottom_box.setContentsMargins(20,20,20,20)
        bottom_box.setSpacing(20)
        bottom_widget = QWidget(self, flags=Qt.Widget)
        bottom_widget.setLayout(bottom_box)

        self.scroll = QScrollArea(self)
        self.scroll.setWidget(bottom_widget)
        self.scroll.setWidgetResizable(True)
        self.scroll.setObjectName("scroll")
        self.scroll.setStyleSheet("QWidget#scroll {border: 0px solid grey;}")
        self.scroll.verticalScrollBar().setValue(self.pos)
        return self.scroll

    def open_ExerciseWindow(self, exercise, show_results, event):
        for i in self.exercise_windows:
            if i[0] == exercise.id:
                i[1].hide()
                i[1].show()
                return
        cw = ExerciseWindow(exercise, self.data, self)
        self.exercise_windows.append([exercise.id, cw])
        cw.show()
        if show_results:
            cw.watch_button_on_click(None, None)

    def close_ExerciseWindow(self, exercise):
        for i in self.exercise_windows:
            if i[0] == exercise.id:
                self.exercise_windows.remove(i)
                self.update()
                return

    def update(self):
        self.controller.open_HomeworkCollectionWindow(False, self.scroll.verticalScrollBar().value())
        # self.open_ExerciseWindow(ex, self.data.visible, None) con questa riga di codice si riapre sulle soluzioni

    def open_CreateHomeworkWindow(self):
        if self.new_exercise is None:
            self.new_exercise = CreateHomeworkWindow(self.data, self)
            self.new_exercise.show()
        else:
            self.new_exercise.hide()
            self.new_exercise.show()

    def close_CreateHomeworkWindow(self):
        self.new_exercise.close()
        self.new_exercise = None
        self.controller.open_HomeworkCollectionWindow(True, 0)
