import json
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

        try:
            r = requests.post("http://programmingisagame.netsons.org/get_class_achievement_progress.php",
                              data={'username': data.my_name, 'password': data.my_psw, 'class': data.my_class})
            if r.text != "":
                students_widgets = []
                #my_widget = None
                mates = json.loads(r.text)
                for i in range(0, len(mates)):
                    students_widgets.append(self.make_student_widget(mates[i], i))
                    '''
                    if mates[i]['username'] == data.my_name:
                        my_widget = self.make_student_widget(mates[i], i)
                    else:
                        students_widgets.append(self.make_student_widget(mates[i], i))
                    '''

                box = QHBoxLayout(self)
                box.setAlignment(Qt.AlignLeft)
                #box.addWidget(my_widget, alignment=Qt.AlignLeft)
                for i in students_widgets:
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

    def make_student_widget(self, user, position):
        font = QFont()
        font.setPixelSize(20)

        pos = QLabel(str(position+1)+"°", self)
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

        lev = QLabel("Liv: " + user['exp'], self)
        lev.setFont(font)
        lev.setFixedSize(100, 40)
        lev.setAlignment(Qt.AlignRight)
        lev.setContentsMargins(0, 10, 10, 0)
        lev.setStyleSheet("background-color: #9999FF; border: 1px solid grey")

        money = QLabel(user['money'] + " Soldi", self)
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
        box.addWidget(img)
        box.addWidget(lev_mon, alignment=Qt.AlignRight)
        what = QWidget(self, flags=Qt.Widget)
        what.setLayout(box)

        progress = user['progress'].split(',')

        box = QVBoxLayout(self)
        box.addWidget(who)
        box.addWidget(what)
        for i in range(0, len(progress)):
            box.addWidget(self.make_achievement_widget(self.achievements_titles[i], progress[i]))
        widget = QWidget(self, flags=Qt.Widget)
        widget.setLayout(box)
        widget.setObjectName("w")
        widget.setStyleSheet("QWidget#w {background-color: white; border: 1px solid grey}")

        return widget

    def make_achievement_widget(self, title, progress):
        font = QFont()
        font.setPixelSize(15)

        name = QLabel(title, self)
        name.setFont(font)
        name.setFixedWidth(200)
        name.setContentsMargins(10, 0, 10, 0)

        box = QVBoxLayout(self)
        box.setSpacing(0)
        box.setContentsMargins(0, 0, 0, 0)
        box.addWidget(name)

        widget = QWidget(self, flags=Qt.Widget)
        widget.setFixedHeight(50)
        widget.setObjectName("widget")

        if progress != 'ok':
            prog = QLabel(progress+"%", self)
            prog.setAlignment(Qt.AlignCenter)
            prog.setFixedSize(max(int(progress)*2.4, 45), 20)
            prog.setStyleSheet("border: 1px solid grey; background-color: #99FF99")
            box.addWidget(prog)
            widget.setStyleSheet("QWidget#widget {border: 1px solid grey; background-color: #9999FF}")
        else:
            widget.setStyleSheet("QWidget#widget {border: 1px solid grey; background-color: #99FF99}")

        widget.setLayout(box)
        return widget
