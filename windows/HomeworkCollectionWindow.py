from functools import partial

from PyQt5.QtWidgets import QWidget, QPlainTextEdit, QPushButton, QHBoxLayout, QVBoxLayout
from PyQt5.QtCore import *

from windows.CreateHomeworkWindow import CreateHomeworkWindow
from windows.ExerciseWindow import ExerciseWindow


class HomeworkCollectionWindow(QWidget):
    def __init__(self, controller, data):
        super(HomeworkCollectionWindow, self).__init__(controller, flags=Qt.Widget)
        self.setMinimumSize(QSize(800, 400))
        self.setWindowTitle("Gamification")
        self.data = data
        self.controller = controller
        self.exercise_windows = []
        self.new_exercise = None

        self.bottom_box = QVBoxLayout(self)
        self.bottom_widget = QWidget(self, flags=Qt.Widget)
        self.top_box = QHBoxLayout(self)
        self.top_widget = QWidget(self, flags=Qt.Widget)
        self.home_button = QPushButton('HOME', self)

        self.make_top_widget()
        self.make_bottom_widget()

        window_layaut = QVBoxLayout(self)
        window_layaut.addWidget(self.top_widget)
        window_layaut.addWidget(self.bottom_widget)
        window_layaut.setContentsMargins(0, 0, 0, 0)
        window_layaut.setSpacing(0)

    def make_top_widget(self):
        self.home_button.setFixedSize(50, 50)
        self.home_button.clicked.connect(self.controller.open_MainWindow)

        title = QPlainTextEdit(self)
        title.setPlainText("COMPITI")
        title.setFixedSize(150, 50)
        title.setReadOnly(True)
        # TODO rendere bello il titolo

        button = QPushButton('AGGIUNGI COMPITO', self)
        button.clicked.connect(self.open_CreateHomeworkWindow)
        button.setFixedWidth(200)

        self.top_box.addWidget(self.home_button)
        self.top_box.addWidget(title)
        self.top_box.addWidget(button, alignment=Qt.AlignRight)
        self.top_box.setAlignment(Qt.AlignLeft)
        self.top_box.setSpacing(50)
        self.top_widget.setLayout(self.top_box)
        self.top_widget.setObjectName("topStyle")
        self.top_widget.setStyleSheet("QWidget#topStyle {border: 0px solid grey; border-bottom: 1px solid grey}")
        self.top_widget.setFixedHeight(70)

    def make_bottom_widget(self):
        exercises = []
        for i in self.data.exercises:
            exercises.append(i)
        while len(exercises) > 0:
            date_exercises = QPlainTextEdit(self)
            date_exercises.setFixedSize(100, 50)
            date = exercises[0].date
            date_exercises.setPlainText(date)
            date_exercises.setReadOnly(True)

            other_exercises_box = QHBoxLayout(self)
            other_exercises_box.setContentsMargins(0,0,0,0)
            other_exercises_box.setAlignment(Qt.AlignLeft)
            proff_exercises_box = QHBoxLayout(self)
            proff_exercises_box.setContentsMargins(0,0,0,0)
            proff_exercises_box.setAlignment(Qt.AlignLeft)

            proff_counter = other_counter = 0
            temp_exercises = []
            for i in exercises:
                if i.date == date:
                    temp_exercises.append(i)
                    button = QPushButton(i.title + "\nby " + i.creator)
                    button.setFixedSize(100, 50)
                    if (i.solution is None or i.solution == i.start_code) and i.delivery_date is None:
                        button.setStyleSheet('background-color:red')
                    elif i.solution is not None and i.delivery_date is None:
                        button.setStyleSheet('background-color:yellow')
                    else:
                        button.setStyleSheet('background-color:green')
                    button.clicked.connect(partial(self.open_ExerciseWindow, i))
                    if i.creator == self.data.my_proff:
                        proff_exercises_box.addWidget(button, alignment=Qt.AlignTop)
                        proff_counter += 1
                    else:
                        other_exercises_box.addWidget(button, alignment=Qt.AlignTop)
                        other_counter += 1
            for i in temp_exercises:
                exercises.remove(i)

            proff_exercises_widget = QWidget(self, flags=Qt.Widget)
            proff_exercises_widget.setLayout(proff_exercises_box)
            other_exercises_widget = QWidget(self, flags=Qt.Widget)
            other_exercises_widget.setLayout(other_exercises_box)
            both_exercises_box = QVBoxLayout(self)
            both_exercises_box.setContentsMargins(0,0,0,0)
            both_exercises_box.addWidget(proff_exercises_widget, alignment=Qt.AlignTop)
            both_exercises_box.addWidget(other_exercises_widget, alignment=Qt.AlignTop)
            both_exercises_widget = QWidget(self, flags=Qt.Widget)
            both_exercises_widget.setLayout(both_exercises_box)

            if proff_counter == 0:
                proff_exercises_widget.hide()
            if other_counter == 0:
                other_exercises_widget.hide()

            exercises_box = QHBoxLayout(self)
            exercises_box.setAlignment(Qt.AlignLeft)
            exercises_box.setSpacing(30)
            exercises_box.addWidget(date_exercises, alignment=Qt.AlignTop)
            exercises_box.addWidget(both_exercises_widget, alignment=Qt.AlignTop)
            exercises_widget = QWidget(self, flags=Qt.Widget)
            exercises_widget.setLayout(exercises_box)
            self.bottom_box.addWidget(exercises_widget)
        self.bottom_widget.setLayout(self.bottom_box)

    def open_ExerciseWindow(self, exercise):
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
        self.controller.open_HomeworkCollectionWindow()

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
        self.controller.open_HomeworkCollectionWindow()
