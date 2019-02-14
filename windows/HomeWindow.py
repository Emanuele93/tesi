from functools import partial

from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtWidgets import QWidget, QPushButton, QHBoxLayout, QVBoxLayout, QFrame, QLabel
from PyQt5.QtCore import *

from windows.LoginWindow import LoginWindow
from windows.SettingsWindow import SettingsWindow


class HomeWindow(QWidget):
    def __init__(self, controller, data):
        super(HomeWindow, self).__init__(controller, flags=Qt.Widget)
        controller.setWindowTitle("Gamification")
        font = QFont()
        font.setPixelSize(15)
        self.data = data
        self.controller = controller

        self.image = QLabel(self)
        pixmap = QPixmap('img/'+data.current_image)
        pixmap = pixmap.scaled(130, 130)
        self.image.setPixmap(pixmap)
        self.image.setObjectName(data.current_image)
        self.image.mousePressEvent = partial(controller.open_Abilities_Window, 3)
        self.image.setStyleSheet('border: 1px solid grey')

        pixmap = QPixmap('img/settings.png')
        pixmap = pixmap.scaled(50, 50)
        settings_button = QLabel(self)
        settings_button.setPixmap(pixmap)
        settings_button.setObjectName('img/settings.png')
        settings_button.mousePressEvent = self.settings_button_on_click

        l = 1
        old = 0
        for i in self.data.level_progression:
            if self.data.level >= i:
                l += 1
                old = i

        level_number = QLabel('Liv. ' + str(l), self)
        level_number.setFont(font)
        level_number.setStyleSheet('background-color: #9999FF; border: 1px solid grey')
        level_number.setFixedSize(85, 42)
        level_number.setContentsMargins(20, 10, 20, 10)

        level_bar = QLabel(self)
        level_bar.setStyleSheet('background-color: #4040FF')
        level_bar.setFixedSize(int(85*(self.data.level-old)/(self.data.level_progression[l-1]-old)), 8)

        box = QVBoxLayout(self)
        box.setSpacing(0)
        box.setContentsMargins(0, 0, 0, 0)
        box.addWidget(level_number)
        box.addWidget(level_bar)
        level = QWidget(self, flags=Qt.Widget)
        level.setLayout(box)
        level.setFixedHeight(50)
        level.setObjectName("level")
        level.setStyleSheet("QWidget#level {border: 1px solid grey; background-color: #BBBBFF}")

        soldi = QLabel(str(self.data.money) + ' soldi', self)
        soldi.setFont(font)
        soldi.setStyleSheet('background-color: #ffea00; border: 1px solid grey;')
        soldi.setFixedHeight(50)
        soldi.setContentsMargins(20, 10, 20, 10)

        box = QHBoxLayout(self)
        box.setAlignment(Qt.AlignTop)
        box.addWidget(level)
        box.addWidget(soldi)
        box.setContentsMargins(0, 0, 0, 0)
        soldi_widget = QWidget(self, flags=Qt.Widget)
        soldi_widget.setLayout(box)

        box = QHBoxLayout(self)
        box.setAlignment(Qt.AlignTop)
        box.addWidget(settings_button)
        box.setSpacing(50)
        settings_widget = QWidget(self, flags=Qt.Widget)
        settings_widget.setLayout(box)

        box = QHBoxLayout(self)
        box.setAlignment(Qt.AlignVCenter)
        box.addWidget(self.image, alignment=Qt.AlignLeft)
        box.addWidget(soldi_widget, alignment=Qt.AlignLeft)
        box.addWidget(settings_widget, alignment=Qt.AlignRight)
        frame = QWidget(self, flags=Qt.Widget)
        frame.setFixedHeight(150)
        frame.setLayout(box)
        frame.setObjectName("frame")
        frame.setStyleSheet("QWidget#frame {border: 0px solid grey; border-top: 1px solid grey; "
                            "border-bottom: 1px solid grey; background-color: #ffdd55}")

        pixmap = QPixmap('img/esercizi.png')
        box1 = QLabel(self)
        box1.setPixmap(pixmap)
        box1.setObjectName('img/esercizi.png')
        #box1.mousePressEvent = self.my_open_HomeworkCollectionWindow
        box1.setStyleSheet("border: 1px solid grey")

        pixmap = QPixmap('img/compiti.png')
        box2 = QLabel(self)
        box2.setPixmap(pixmap)
        box2.setObjectName('img/compiti.png')
        box2.mousePressEvent = self.my_open_HomeworkCollectionWindow
        box2.setStyleSheet("border: 1px solid grey")

        pixmap = QPixmap('img/obiettivi.png')
        box3 = QLabel(self)
        box3.setPixmap(pixmap)
        box3.setObjectName('img/obiettivi.png')
        box3.mousePressEvent = self.my_open_AchievementsWindow
        box3.setStyleSheet("border: 1px solid grey")

        pixmap = QPixmap('img/negozio.png')
        box4 = QLabel(self)
        box4.setPixmap(pixmap)
        box4.setObjectName('img/negozio.png')
        box4.mousePressEvent = self.my_open_Abilities_Window
        box4.setStyleSheet("border: 1px solid grey")

        box = QWidget(self, flags=Qt.Widget)
        internal_layout = QHBoxLayout(self)
        internal_layout.setContentsMargins(10, 5, 10, 15)
        internal_layout.setSpacing(10)
        internal_layout.addWidget(box1)
        internal_layout.addWidget(box2)
        internal_layout.addWidget(box3)
        internal_layout.addWidget(box4)
        box.setLayout(internal_layout)

        layout = QVBoxLayout(self)
        layout.setSpacing(10)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(frame)
        layout.addWidget(box)

    def settings_button_on_click(self, event):
        confirm = SettingsWindow('Gamification - settings', self.data, None, parent=self)
        confirm.exec_()
        confirm.deleteLater()

    def set_image(self, name):
        pixmap = QPixmap('img/' + name)
        pixmap = pixmap.scaled(130,130)
        self.image.setPixmap(pixmap)

    def my_open_HomeworkCollectionWindow(self, event):
        self.controller.open_HomeworkCollectionWindow(True, 0)

    def my_open_AchievementsWindow(self, event):
        self.controller.open_AchievementsWindow(0)

    def my_open_Abilities_Window(self, event):
        self.controller.open_Abilities_Window(1, None)

    def open_LoginWindow(self):
        self.controller.login.show()
        self.controller.hide()
