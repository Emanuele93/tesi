import json
import random

import requests
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtWidgets import QDialog, QWidget, QVBoxLayout, QLabel, QHBoxLayout, QScrollArea
from windows.ConfirmWindow import ConfirmWindow


class ClassAchievementsComparisonWindow(QDialog):
    def __init__(self, data, achievements_titles, parent=None):
        QDialog.__init__(self, parent, flags=Qt.Dialog)
        self.setWindowTitle("Gamification - Classifica")
        self.setMinimumWidth(600)
        self.setMinimumHeight(500)
        self.achievements_titles = achievements_titles
        self.data = data

        try:
            r = requests.post("http://programmingisagame.netsons.org/get_class_achievement_progress.php",
                              data={'username': data.my_name, 'password': data.my_psw, 'class': data.my_class})
            if r.text != "":
                students_widgets = []
                not_visible_students_widget = []
                #my_widget = None
                mates = json.loads(r.text)
                pos = 0
                for i in range(0, len(mates)):
                    if i > 0 and mates[i]['exp'] != mates[i-1]['exp']:
                        pos += 1
                    if mates[i]['visible'] == '1' or self.data.my_name in self.data.my_proff:
                        students_widgets.append(self.make_student_widget(mates[i], pos, mates[i]['visible'] == '1'))
                    else:
                        not_visible_students_widget.append(self.make_student_widget(mates[i], None, False))
                    '''
                    if mates[i]['username'] == data.my_name:
                        my_widget = self.make_student_widget(mates[i], i)
                    else:
                        students_widgets.append(self.make_student_widget(mates[i], i))
                    '''

                box = QHBoxLayout(self)
                box.setAlignment(Qt.AlignLeft)
                random.shuffle(not_visible_students_widget)
                #box.addWidget(my_widget, alignment=Qt.AlignLeft)
                for i in students_widgets:
                    box.addWidget(i, alignment=Qt.AlignLeft)
                for i in not_visible_students_widget:
                    box.addWidget(i, alignment=Qt.AlignLeft)
                widget = QWidget(self, flags=Qt.Widget)
                widget.setLayout(box)
                scroll = QScrollArea(self)
                scroll.setWidget(widget)
                scroll.setObjectName("scroll")
                scroll.setStyleSheet("QWidget#scroll {border: 0px solid grey}")
                box = QHBoxLayout(self)
                box.setContentsMargins(0,0,0,0)
                box.addWidget(scroll)

        except requests.exceptions.RequestException as e:
            c = ConfirmWindow('Gamification - Errore di connessione',
                                "<span style=\" color: red;\"> Attenzione, si sono verificati problemi di "
                                "connessione<br>Controllare la connessione internet e riprovare</span>",
                                ok="Ok", cancel=None)
            if c.exec_() == QDialog.Accepted:
                print('ok')
            c.deleteLater()

    def make_student_widget(self, user, position, visible):
        font = QFont()
        font.setPixelSize(20)

        pos_str = "?" if position is None else ((str(position+1)+"°") if visible else ("? (" + str(position+1)+"°)"))
        pos = QLabel(pos_str, self)
        pos.setFont(font)
        pos.setFixedWidth(50)

        title = QLabel(user['username'], self)
        title.setFont(font)
        title.setFixedWidth(150)

        font.setPixelSize(15)

        pixmap = QPixmap('img/' + user['current_image'])
        pixmap = pixmap.scaled(100, 100)
        img = QLabel(self)
        img.setPixmap(pixmap)
        img.setObjectName('img/' + user['current_image'])

        l = 1
        old = 0
        for i in self.data.level_progression:
            if int(user['exp']) >= i:
                l += 1
                old = i

        level_number_str = '???' if position is None else('Liv. ' + str(l))
        level_number = QLabel(level_number_str, self)
        level_number.setFont(font)
        level_number.setAlignment(Qt.AlignRight)
        level_number.setStyleSheet('background-color: #9999FF; border: 1px solid grey')
        level_number.setFixedSize(100, 35)
        level_number.setContentsMargins(0, 10, 10, 0)

        level_bar = QLabel(self)
        level_bar.setStyleSheet('background-color: #4040FF')
        level_bar.setFixedSize(int(100*(int(user['exp'])-old)/(self.data.level_progression[l-1]-old)), 5)
        if position is None:
            level_bar.hide()
            level_number.setFixedHeight(40)

        box = QVBoxLayout(self)
        box.setSpacing(0)
        box.setContentsMargins(0, 0, 0, 0)
        box.addWidget(level_number)
        box.addWidget(level_bar)
        lev = QWidget(self, flags=Qt.Widget)
        lev.setLayout(box)
        lev.setObjectName("level")
        lev.setStyleSheet("QWidget#level {border: 1px solid grey; background-color: #BBBBFF}")
        lev.setFixedHeight(40)

        money_str = '???' if position is None else(user['money'] + " Soldi")
        money = QLabel(money_str, self)
        money.setFont(font)
        money.setFixedSize(100, 40)
        money.setAlignment(Qt.AlignRight)
        money.setContentsMargins(0, 10, 10, 0)
        money.setStyleSheet("background-color: yellow; border: 1px solid grey")

        box = QHBoxLayout(self)
        box.addWidget(pos)
        box.addWidget(title)
        who = QWidget(self, flags=Qt.Widget)
        who.setLayout(box)

        box = QVBoxLayout(self)
        box.setContentsMargins(0, 0, 0, 0)
        box.setSpacing(0)
        box.addWidget(lev)
        box.addWidget(money)
        lev_mon = QWidget(self, flags=Qt.Widget)
        lev_mon.setLayout(box)

        box = QHBoxLayout(self)
        box.setContentsMargins(0,0,0,0)
        box.addWidget(img)
        box.addWidget(lev_mon, alignment=Qt.AlignRight)
        what = QWidget(self, flags=Qt.Widget)
        what.setLayout(box)

        progress = user['progress'].split(',')

        box = QVBoxLayout(self)
        box.addWidget(who)
        box.addWidget(what)
        for i in range(0, len(progress)):
            box.addWidget(
                self.make_achievement_widget(self.achievements_titles[i], progress[i], (position is not None)))
        widget = QWidget(self, flags=Qt.Widget)
        widget.setLayout(box)
        widget.setObjectName("w")
        widget.setStyleSheet("QWidget#w {background-color: white; border: 1px solid grey}")

        return widget

    def make_achievement_widget(self, title, progress, visible):
        font = QFont()
        font.setPixelSize(15)

        name = QLabel(title, self)
        name.setFont(font)
        name.setFixedWidth(220)
        name.setContentsMargins(10, 0, 0, 0)

        box = QVBoxLayout(self)
        box.setSpacing(0)
        box.setContentsMargins(0, 0, 0, 0)
        box.addWidget(name)

        widget = QWidget(self, flags=Qt.Widget)
        widget.setFixedHeight(50)
        widget.setObjectName("widget")

        if progress != 'ok' and visible:
            prog = QLabel(progress+"%", self)
            prog.setAlignment(Qt.AlignCenter)
            prog.setFixedSize(max(int(progress)*2.4, 45), 20)
            prog.setStyleSheet("border: 1px solid grey; background-color: #99FF99")
            box.addWidget(prog)
            widget.setStyleSheet("QWidget#widget {border: 1px solid grey; background-color: #9999FF}")
        elif visible:
            widget.setStyleSheet("QWidget#widget {border: 1px solid grey; background-color: #99FF99}")
        else:
            widget.setStyleSheet("QWidget#widget {border: 1px solid grey; background-color: #9999FF}")


        widget.setLayout(box)
        return widget
