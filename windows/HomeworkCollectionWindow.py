import threading
from functools import partial

from PyQt5.QtGui import QFont, QPixmap, QMovie
from PyQt5.QtWidgets import QWidget, QPlainTextEdit, QPushButton, QHBoxLayout, QVBoxLayout, QScrollArea, QLabel
from PyQt5.QtCore import *

from windows.CreateHomeworkWindow import CreateHomeworkWindow
from windows.ExerciseWindow import ExerciseWindow


class HomeworkCollectionWindow(QWidget):
    def __init__(self, controller, data, loading):
        super(HomeworkCollectionWindow, self).__init__(controller, flags=Qt.Widget)
        controller.setWindowTitle("Gamification - Compiti")
        self.data = data
        self.controller = controller
        self.exercise_windows = []
        self.new_exercise = None

        top_widget = self.make_top_widget()

        if loading:
            bottom_widget = QLabel()
            movie = QMovie("img/waiting.gif")
            bottom_widget.setMovie(movie)
            movie.start()
            self.change_button = QPushButton('PROVA', self)
            self.change_button.clicked.connect(partial(self.controller.open_HomeworkCollectionWindow, False))
            self.change_button.hide()
            box = QHBoxLayout(self)
            box.addWidget(bottom_widget)
            box.addWidget(self.change_button)
            box.setAlignment(Qt.AlignCenter)
            bottom_widget = QWidget(self, flags=Qt.Widget)
            bottom_widget.setLayout(box)
            self.add_homework_button.setEnabled(False)
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

        home_button = QPushButton('HOME', self)
        home_button.setFixedSize(100, 50)
        home_button.clicked.connect(self.controller.open_MainWindow)
        home_button.setFont(font)

        self.add_homework_button = QPushButton('AGGIUNGI COMPITO', self)
        self.add_homework_button.clicked.connect(self.open_CreateHomeworkWindow)
        self.add_homework_button.setFixedSize(250, 50)
        self.add_homework_button.setFont(font)
        if not self.data.make_homework_coin:
            self.add_homework_button.setEnabled(False)

        top_box = QHBoxLayout(self)
        top_box.setContentsMargins(20, 10, 20, 10)
        top_box.addWidget(home_button, alignment=Qt.AlignLeft)
        top_box.addWidget(self.add_homework_button, alignment=Qt.AlignRight)
        top_box.setSpacing(50)
        top_widget = QWidget(self, flags=Qt.Widget)
        top_widget.setLayout(top_box)
        top_widget.setObjectName("topStyle")
        top_widget.setStyleSheet("QWidget#topStyle {border: 0px solid grey; border-bottom: 1px solid grey}")
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
            other_exercises_box.setContentsMargins(0, 0, 0, 0)
            proff_exercises_box = QHBoxLayout(self)
            proff_exercises_box.setAlignment(Qt.AlignLeft)
            proff_exercises_box.setContentsMargins(0, 0, 0, 0)

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
                    by.mousePressEvent = partial(self.open_ExerciseWindow, i)
                    by.setTextFormat(Qt.RichText)

                    box = QVBoxLayout(self)
                    box.setAlignment(Qt.AlignTop)
                    box.setContentsMargins(0, 0, 0, 0)
                    box.setSpacing(0)
                    box.addWidget(title, alignment=Qt.AlignTop)
                    box.addWidget(by, alignment=Qt.AlignTop)
                    exercise = QWidget(self, flags=Qt.Widget)
                    exercise.setLayout(box)
                    exercise.mousePressEvent = partial(self.open_ExerciseWindow, i)

                    box = QHBoxLayout(self)
                    box.setAlignment(Qt.AlignTop)
                    box.setContentsMargins(0, 0, 0, 0)
                    box.setSpacing(0)
                    box.addWidget(exercise, alignment=Qt.AlignVCenter)
                    box.addWidget(difficulty, alignment=Qt.AlignLeft)
                    exercise = QWidget(self, flags=Qt.Widget)
                    exercise.setLayout(box)
                    exercise.setObjectName("exercise")

                    if (i.solution is None or i.solution == i.start_code) and i.delivery_date is None:
                        exercise.setStyleSheet('QWidget#exercise {background-color:red; border: 1px solid grey;}')
                    elif i.solution is not None and i.delivery_date is None:
                        exercise.setStyleSheet('QWidget#exercise {background-color:yellow; border: 1px solid grey};')
                    else:
                        exercise.setStyleSheet('QWidget#exercise {background-color:green; border: 1px solid grey;}')

                    if i.creator == self.data.my_proff:
                        proff_exercises_box.addWidget(exercise, alignment=Qt.AlignLeft)
                        proff_counter += 1
                    else:
                        other_exercises_box.addWidget(exercise, alignment=Qt.AlignLeft)
                        other_counter += 1
            for i in temp_exercises:
                exercises.remove(i)

            proff_exercises_widget = QWidget(self, flags=Qt.Widget)
            proff_exercises_widget.setLayout(proff_exercises_box)
            other_exercises_widget = QWidget(self, flags=Qt.Widget)
            other_exercises_widget.setLayout(other_exercises_box)
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
            exercises_box.setContentsMargins(20, 20, 20, 20)
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

        scroll = QScrollArea(self)
        scroll.setWidget(bottom_widget)
        scroll.setWidgetResizable(True)
        scroll.setObjectName("scroll")
        scroll.setStyleSheet("QWidget#scroll {border: 0px solid grey;}")
        return scroll

    def open_ExerciseWindow(self, exercise, event):
        for i in self.exercise_windows:
            if i[0] == exercise.id:
                i[1].hide()
                i[1].show()
                return
        cw = ExerciseWindow(exercise, self.data, self)
        self.exercise_windows.append([exercise.id, cw])
        cw.show()

    def close_ExerciseWindow(self, exercise):
        for i in self.exercise_windows:
            if i[0] == exercise.id:
                i[1].close()
                self.exercise_windows.remove(i)
                self.update()
                return

    def update(self):
        self.controller.open_HomeworkCollectionWindow(False)

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
        self.controller.open_HomeworkCollectionWindow(True)
