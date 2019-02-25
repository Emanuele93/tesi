import json
from functools import partial

import requests
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QWidget, QPushButton, QHBoxLayout, QVBoxLayout, QScrollArea, QLabel, QDialog
from PyQt5.QtCore import *

from windows.ClassAchievementsComparisonWindow import ClassAchievementsComparisonWindow
from windows.ConfirmWindow import ConfirmWindow


class AchievementsWindow(QWidget):
    def __init__(self, home, data, pos):
        super(AchievementsWindow, self).__init__(home, flags=Qt.Widget)
        home.setWindowTitle("Gamification - Obiettivi")
        self.data = data
        self.controller = home
        self.achievements = []
        self.titles = []

        self.update_data()

        top_widget = self.make_top_widget()
        bottom_widget = self.make_bottom_widget(pos)

        window_layaut = QVBoxLayout(self)
        window_layaut.addWidget(top_widget)
        window_layaut.addWidget(bottom_widget)
        window_layaut.setContentsMargins(0, 0, 0, 0)
        window_layaut.setSpacing(0)

    def update_data(self):
        try:
            r = requests.post("http://programmingisagame.netsons.org/update_achievements.php",
                              data={'username': self.data.my_name, 'password': self.data.my_psw})
            j = json.loads(r.text.split("-")[0])
            k = r.text.split("-")[1][1:-1].split(',')
            for i in range(0, len(j)):
                achievement = {
                    'title': j[i]['title'],
                    'description': j[i]['description'],
                    'value': int(j[i]['value']),
                    'level': k[i]
                }
                self.achievements.append(achievement)
                self.titles.append(j[i]['title'])
        except requests.exceptions.RequestException as e:
            confirm = ConfirmWindow('Gamification - Errore di connessione',
                                    "<span style=\" color: red;\"> Attenzione, si sono verificati problemi di "
                                    "connessione<br>Controllare la connessione internet</span>",
                                    ok="Riprova", cancel="Chiudi il programma")
            if confirm.exec_() == QDialog.Accepted:
                self.update_data()
                confirm.deleteLater()
            else:
                confirm.deleteLater()
                exit()

    def make_top_widget(self):
        font = QFont()
        font.setPixelSize(15)

        home_button = QPushButton('HOME', self)
        home_button.setFixedSize(100, 50)
        home_button.clicked.connect(self.controller.open_MainWindow)
        home_button.setFont(font)
        home_button.setStyleSheet("background-color: #ffdd55")

        open_leaderboard_button = QPushButton('CLASSIFICA', self)
        open_leaderboard_button.clicked.connect(self.open_leaderboard_window)
        open_leaderboard_button.setFixedSize(250, 50)
        open_leaderboard_button.setFont(font)
        open_leaderboard_button.setStyleSheet("background-color: #ffdd55")
        open_leaderboard_button.setEnabled(self.data.visible)

        l = 1
        old = 0
        for i in self.data.level_progression:
            if self.data.level >= i:
                l += 1
                old = i

        self.level_number = QLabel('Liv. ' + str(l), self)
        self.level_number.setFont(font)
        self.level_number.setStyleSheet('background-color: #9999FF; border: 1px solid grey')
        self.level_number.setFixedSize(85, 40)
        self.level_number.setContentsMargins(20, 10, 20, 10)

        self.level_bar = QLabel(self)
        self.level_bar.setStyleSheet('background-color: #4040FF')
        self.level_bar.setFixedSize(int(85*(self.data.level-old)/(self.data.level_progression[l-1]-old)), 5)

        box = QVBoxLayout(self)
        box.setSpacing(0)
        box.setContentsMargins(0, 0, 0, 0)
        box.addWidget(self.level_number)
        box.addWidget(self.level_bar)
        level = QWidget(self, flags=Qt.Widget)
        level.setLayout(box)
        level.setObjectName("level")
        level.setStyleSheet("QWidget#level {border: 1px solid grey; background-color: #BBBBFF}")

        self.soldi = QLabel(str(self.data.money) + ' soldi', self)
        self.soldi.setFont(font)
        self.soldi.setStyleSheet('background-color: #ffea00; border: 1px solid grey')
        self.soldi.setFixedHeight(45)
        self.soldi.setContentsMargins(20, 5, 20, 5)

        box = QHBoxLayout(self)
        box.setAlignment(Qt.AlignCenter)
        box.addWidget(level)
        box.addWidget(self.soldi)
        box.setSpacing(5)
        box.setContentsMargins(0, 0, 0, 0)
        soldi_widget = QWidget(self, flags=Qt.Widget)
        soldi_widget.setLayout(box)

        font.setPixelSize(25)
        font.setBold(True)
        title = QLabel("Obiettivi", self)
        title.setFont(font)
        title.setStyleSheet("color: #ffffff")

        top_box = QHBoxLayout(self)
        top_box.setContentsMargins(20, 0, 20, 0)
        top_box.addWidget(home_button)
        top_box.addWidget(title)
        top_box.addWidget(open_leaderboard_button, alignment=Qt.AlignRight)
        top_box.setSpacing(60)
        top_widget = QWidget(self, flags=Qt.Widget)
        top_widget.setLayout(top_box)
        top_widget.setObjectName("topStyle")
        top_widget.setStyleSheet("QWidget#topStyle {border: 0px solid grey; border-bottom: 1px solid grey; "
                                 "border-top: 1px solid grey; background-color: #88aaff}")
        top_widget.setFixedHeight(80)

        font.setPixelSize(17)
        font.setBold(False)
        log_line = QLabel('Sblocca tutti gli obiettivi per avanzare nella classifica', self)
        log_line.setFont(font)
        box = QHBoxLayout(self)
        box.addWidget(log_line)
        box.addWidget(soldi_widget, alignment=Qt.AlignRight)
        box.setContentsMargins(75, 0, 5, 0)
        log_line = QWidget(self, flags=Qt.Widget)
        log_line.setLayout(box)
        log_line.setObjectName("log_line")
        log_line.setStyleSheet("QWidget#log_line {border: 0px solid grey; border-bottom: 1px solid grey; "
                               "background-color: #88c5ff}")
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

    def make_bottom_widget(self, pos):
        font = QFont()
        font.setPixelSize(15)
        font.setBold(True)

        v_box = QVBoxLayout(self)
        h_box = QHBoxLayout(self)
        h_box.setContentsMargins(10, 10, 0, 10)
        h_box.setSpacing(25)
        for i in range(0, len(self.achievements)):
            if i % 3 == 0 and i > 0:
                row = QWidget(self, flags=Qt.Widget)
                row.setLayout(h_box)
                v_box.addWidget(row)
                h_box = QHBoxLayout(self)
                h_box.setContentsMargins(10, 10, 0, 10)
                h_box.setSpacing(25)

            title = QLabel(self.achievements[i]['title'], self)
            title.setFont(font)
            title.setContentsMargins(10, 10, 10, 0)
            title.setWordWrap(True)
            description = QLabel(self.achievements[i]['description'], self)
            description.setWordWrap(True)
            description.setContentsMargins(10, 0, 10, 2)
            if self.achievements[i]['level'] == '100':
                box = QVBoxLayout(self)
            else:
                box = QHBoxLayout(self)
                box.setSpacing(20)
                box.setContentsMargins(20, 0, 20, 0)
            money = QLabel(str(self.achievements[i]['value'] * 10) + " soldi", self)
            money.setAlignment(Qt.AlignCenter)
            money.setObjectName("money")
            money.setStyleSheet("QWidget#money {border: 1px solid grey; background-color: #ffea00}")
            money.setContentsMargins(0,5,0,5)
            box.addWidget(money)
            exp = QLabel(str(self.achievements[i]['value'] * 3) + " exp", self)
            exp.setAlignment(Qt.AlignCenter)
            exp.setObjectName("exp")
            exp.setStyleSheet("QWidget#exp {border: 1px solid grey; background-color: #9999FF}")
            exp.setContentsMargins(0,5,0,5)
            box.addWidget(exp)
            value = QWidget(self, flags=Qt.Widget)
            value.setLayout(box)

            if self.achievements[i]['level'] == '100':
                level = QPushButton('Riscatta\nil premio')
                level.setFixedSize(85,45)
                level.setObjectName("level")
                level.setStyleSheet("QWidget#level {background-color: #99FF99}")
                level.clicked.connect(partial(self.get_award, i))
                box = QHBoxLayout(self)
                box.setContentsMargins(15, 0, 5, 5)
                box.addWidget(level)
                box.addWidget(value)
                level_value = QWidget(self, flags=Qt.Widget)
                level_value.setLayout(box)
            else:
                level = QLabel(' ' + self.achievements[i]['level'] + '%', self)
                if self.achievements[i]['level'] != 'ok':
                    level.setFixedWidth(max(45.0, int(self.achievements[i]['level']) / 100 * 230))
                    level.setAlignment(Qt.AlignCenter)
                level.setObjectName("level")
                level.setStyleSheet("QWidget#level {border: 1px solid grey; background-color: #99FF99}")

            box = QVBoxLayout(self)
            box.setContentsMargins(0, 0, 0, 0)
            box.addWidget(title)
            box.addWidget(description)
            if self.achievements[i]['level'] == '100':
                box.addWidget(level_value)
            else:
                box.addWidget(value)
                box.addWidget(level)
            achievement = QWidget(self, flags=Qt.Widget)
            achievement.setLayout(box)
            achievement.setFixedWidth(230)
            achievement.setObjectName("achievement")
            if self.achievements[i]['level'] == 'ok':
                value.hide()
                level.hide()
                box.setAlignment(Qt.AlignVCenter)
                box.setContentsMargins(5, 0, 5, 20)
                achievement.setStyleSheet("QWidget#achievement {border: 1px solid grey; background-color: #99FF99}")
            else:
                achievement.setStyleSheet("QWidget#achievement {border: 1px solid grey; background-color: #bbbbff}")

            h_box.addWidget(achievement)

        row = QWidget(self, flags=Qt.Widget)
        row.setLayout(h_box)
        v_box.addWidget(row)

        bottom_widget = QWidget(self, flags=Qt.Widget)
        bottom_widget.setLayout(v_box)
        self.scroll = QScrollArea(self)
        self.scroll.setWidget(bottom_widget)
        self.scroll.setObjectName("scroll")
        self.scroll.setStyleSheet("QWidget#scroll {border: 0px solid grey}")
        self.scroll.verticalScrollBar().setValue(pos)
        return self.scroll

    def get_award(self, index):
        try:
            r = requests.post("http://programmingisagame.netsons.org/get_aword_achievement.php",
                      data={'username': self.data.my_name, 'password': self.data.my_psw, 'index': index})
            if r.text != "":
                self.data.get_user_data()
                self.soldi.setText(str(self.data.money) + " Soldi")

                l = 1
                old = 0
                for i in self.data.level_progression:
                    if self.data.level >= i:
                        l += 1
                        old = i

                self.level_number.setText('Liv. ' + str(l))
                self.level_bar.setFixedSize(int(85*(self.data.level-old)/(self.data.level_progression[l-1]-old)), 5)
                self.controller.open_AchievementsWindow(self.scroll.verticalScrollBar().value())
        except requests.exceptions.RequestException as e:
            confirm = ConfirmWindow('Gamification - Errore di connessione',
                                    "<span style=\" color: red;\"> Attenzione, si sono verificati problemi di "
                                    "connessione<br>Controllare la connessione internet e riprovare</span>",
                                    ok="Ok", cancel=None)
            if confirm.exec_() == QDialog.Accepted:
                print('ok')
            confirm.deleteLater()

    def open_leaderboard_window(self):
        confirm = ClassAchievementsComparisonWindow(self.data, self.titles, parent=self)
        if confirm.exec_() == QDialog.Accepted:
            print('ok')
        confirm.deleteLater()
