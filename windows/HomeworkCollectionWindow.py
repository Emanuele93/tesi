from functools import partial
from PyQt5.QtGui import QFont, QPixmap, QMovie
from PyQt5.QtWidgets import QWidget, QPushButton, QHBoxLayout, QVBoxLayout, QScrollArea, QLabel
from PyQt5.QtCore import *
from windows.CreateHomeworkWindow import CreateHomeworkWindow
from windows.ExerciseWindow import ExerciseWindow
from windows.ExerciseWindowC import ExerciseWindowC


class HomeworkCollectionWindow(QWidget):
    def __init__(self, controller, data, loading, pos):
        super(HomeworkCollectionWindow, self).__init__(controller, flags=Qt.Widget)
        controller.setWindowTitle("Compiti")
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

        self.home_button = QPushButton('HOME', self)
        self.home_button.setFixedSize(100, 50)
        self.home_button.clicked.connect(self.controller.open_MainWindow)
        self.home_button.setFont(font)
        self.home_button.setStyleSheet('background-color: #ffdd55')

        self.add_homework_button = QPushButton('AGGIUNGI COMPITO', self)
        self.add_homework_button.clicked.connect(self.open_CreateHomeworkWindow)
        self.add_homework_button.setFixedSize(250, 50)
        self.add_homework_button.setFont(font)
        self.add_homework_button.setStyleSheet("background-color: #ffdd55")
        if not self.data.make_homework_coin:
            self.add_homework_button.setEnabled(False)

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
        title = QLabel("Compiti di " + self.data.my_name, self)
        title.setFont(font)
        title.setAlignment(Qt.AlignHCenter)
        title.setStyleSheet("color: #ffffff")

        '''
        box = QVBoxLayout(self)
        box.setAlignment(Qt.AlignCenter)
        box.setContentsMargins(7, 7, 7, 7)
        box.setSpacing(5)
        box.addWidget(title)
        box.addWidget(soldi_widget)
        box.setAlignment(Qt.AlignLeft)
        soldi_widget = QWidget(self, flags=Qt.Widget)
        soldi_widget.setLayout(box)
        '''

        top_box = QHBoxLayout(self)
        top_box.setContentsMargins(20, 0, 20, 0)
        top_box.setSpacing(40)
        top_box.addWidget(self.home_button)
        top_box.addWidget(title, alignment=Qt.AlignCenter)
        top_box.addWidget(self.add_homework_button, alignment=Qt.AlignRight)
        #top_box.addWidget(soldi_widget, alignment=Qt.AlignRight)
        top_widget = QWidget(self, flags=Qt.Widget)
        top_widget.setLayout(top_box)
        top_widget.setObjectName("topStyle")
        top_widget.setStyleSheet("QWidget#topStyle {border: 0px solid grey; border-bottom: 1px solid grey; "
                                 "border-top: 1px solid grey; background-color: #ffbd49}")
        top_widget.setFixedHeight(80)

        font.setPixelSize(17)
        font.setBold(False)
        log_line = QLabel('Risolvi, consegna, confronta e guadagna.', self)
        log_line.setFont(font)
        box = QHBoxLayout(self)
        box.addWidget(log_line)
        box.addWidget(soldi_widget, alignment=Qt.AlignRight)
        box.setContentsMargins(75, 0, 5, 0)
        log_line = QWidget(self, flags=Qt.Widget)
        log_line.setLayout(box)
        log_line.setObjectName("log_line")
        log_line.setStyleSheet("QWidget#log_line {border: 0px solid grey; border-bottom: 1px solid grey; "
                               "background-color: #ffff55}")
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
            date_exercises = QLabel("Esercizi per il\n" + date, self)
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

                    pixmap = QPixmap('img/approved.png')
                    pixmap = pixmap.scaled(30, 30)
                    approved_icon = QLabel(self)
                    approved_icon.setPixmap(pixmap)
                    approved_icon.setObjectName('img/approved.png')
                    approved_icon.setFixedWidth(35)
                    approved_icon.setContentsMargins(5, 0, 0, 10)
                    if not i.approved:
                        approved_icon.hide()

                    title = QLabel(i.title, self)
                    title.setFont(font)
                    title.setContentsMargins(0, 10, 5, 0)

                    s = '&#x25EF;' if i.level == 'Facile' \
                        else ('&#x25EF;<br>&#x25EF;' if i.level == 'Medio' else '&#x25EF;<br>&#x25EF;<br>&#x25EF;')
                    difficulty = QLabel(s, self)
                    difficulty.setContentsMargins(10, 2, 10, 2)
                    difficulty.setTextFormat(Qt.RichText)
                    difficulty.setFont(f)
                    difficulty.enterEvent = partial(self.show_text, i.level, 60, difficulty)
                    difficulty.leaveEvent = self.hide_text

                    by = QLabel("<i>by " + i.creator + "</i>", self)
                    by.setContentsMargins(0, 0, 5, 10)
                    by.setTextFormat(Qt.RichText)

                    box = QVBoxLayout(self)
                    box.setAlignment(Qt.AlignTop)
                    if i.approved:
                        box.setContentsMargins(5, 0, 0, 0)
                    else:
                        box.setContentsMargins(15, 0, 0, 0)
                    box.setSpacing(0)
                    box.addWidget(title, alignment=Qt.AlignTop)
                    box.addWidget(by, alignment=Qt.AlignTop)
                    exercise = QWidget(self, flags=Qt.Widget)
                    exercise.setLayout(box)

                    f.setPixelSize(12)
                    vote_intro = QLabel("voto", self)
                    vote_intro.setFont(f)
                    f.setPixelSize(18)
                    vote_value = QLabel('?' if i.vote is None else(str(i.vote) if i.validation_type in [2, 4] else
                                                                   ('ok' if float(i.vote) >= 6 else ' no ')), self)
                    vote_value.setFont(f)
                    f.setPixelSize(10)

                    box = QVBoxLayout(self)
                    box.setAlignment(Qt.AlignTop)
                    box.setSpacing(3)
                    box.setContentsMargins(10, 7, 10, 5)
                    box.addWidget(vote_intro, alignment=Qt.AlignHCenter)
                    box.addWidget(vote_value, alignment=Qt.AlignHCenter)
                    vote = QWidget(self, flags=Qt.Widget)
                    vote.setLayout(box)
                    vote.setObjectName("vote")
                    vote.setStyleSheet("QWidget#vote {background-color: #dfe366; border: 1px solid grey}")

                    s = "Un compito da correggere" if i.missing_votes == 1 else \
                        str(i.missing_votes) + " compiti da correggere"
                    pixmap = QPixmap('img/notify.png')
                    pixmap = pixmap.scaled(35, 35)
                    notify = QLabel(self)
                    notify.setPixmap(pixmap)
                    notify.setObjectName('img/notify.png')
                    notify.enterEvent = partial(self.show_text, s, 165, notify)
                    notify.leaveEvent = self.hide_text
                    box = QHBoxLayout(self)
                    box.setContentsMargins(5, 0, 5, 0)
                    box.addWidget(notify, alignment=Qt.AlignVCenter)
                    notify_w = QWidget(self, flags=Qt.Widget)
                    notify_w.setLayout(box)
                    notify_w.setObjectName("vote")
                    notify_w.setStyleSheet("QWidget#vote {background-color: #dfe366; border: 1px solid grey}")

                    if i.missing_votes == 0:
                        notify_w.hide()
                    else:
                        vote.hide()

                    box = QHBoxLayout(self)
                    box.setContentsMargins(0, 0, 0, 0)
                    box.setSpacing(0)
                    box.addWidget(approved_icon)
                    box.addWidget(exercise)
                    box.addWidget(difficulty)
                    box.addWidget(vote)
                    box.addWidget(notify_w)
                    exercise = QWidget(self, flags=Qt.Widget)
                    exercise.setLayout(box)
                    exercise.setObjectName("exercise")
                    exercise.mousePressEvent = partial(self.open_ExerciseWindow, i, False)

                    if (i.solution is None or i.solution == i.start_code) and i.delivery_date is None:
                        exercise.setStyleSheet('QWidget#exercise {background-color: #dd6666; border: 1px solid grey;}')
                        vote.hide()
                    elif i.solution is not None and i.delivery_date is None:
                        exercise.setStyleSheet('QWidget#exercise {background-color: #ffff33; border: 1px solid grey};')
                        vote.hide()
                    else:
                        exercise.setStyleSheet('QWidget#exercise {background-color: #66ee66; border: 1px solid grey;}')
                        if i.validation_type == 0:
                            vote.hide()

                    if i.creator in self.data.my_proff:
                        width += exercise.sizeHint().width()
                        if width > 600:
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
                        if width_students > 600:
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
        cw = ExerciseWindow(exercise, self.data, self) if self.data.language == 1 else \
            ExerciseWindowC(exercise, self.data, self)
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

    def open_CreateHomeworkWindow(self):
        self.data.get_class_components()
        #  TODO rimetti le 6 righe sotto al posto di queste 2 ma aggiorna le impostazioni di valutazione
        self.new_exercise = CreateHomeworkWindow(self.data, self)
        self.new_exercise.show()
        '''
        if self.new_exercise is None:
            self.new_exercise = CreateHomeworkWindow(self.data, self)
            self.new_exercise.show()
        else:
            self.new_exercise.hide()
            self.new_exercise.show()
        '''

    def close_CreateHomeworkWindow(self):
        self.new_exercise.close()
        self.new_exercise = None
        self.controller.open_HomeworkCollectionWindow(True, 0)
