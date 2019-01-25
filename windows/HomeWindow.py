from functools import partial

from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtWidgets import QWidget, QPushButton, QHBoxLayout, QVBoxLayout, QFrame, QLabel
from PyQt5.QtCore import *

from windows.SettingsWindow import SettingsWindow


class HomeWindow(QWidget):
    def __init__(self, controller, data):
        super(HomeWindow, self).__init__(controller, flags=Qt.Widget)
        controller.setWindowTitle("Gamification")
        font = QFont()
        font.setPixelSize(15)
        self.data = data

        self.image = QLabel(self)
        pixmap = QPixmap(data.current_image)
        pixmap = pixmap.scaled(130, 130)
        self.image.setPixmap(pixmap)
        self.image.setObjectName(data.current_image)
        self.image.mousePressEvent = partial(controller.open_Abilities_Window, 3)

        box = QHBoxLayout(self)
        box.addWidget(self.image, alignment=Qt.AlignCenter)
        box.setContentsMargins(0, 0, 0, 0)
        label = QWidget(self, flags=Qt.Widget)
        label.setFixedSize(150, 150)
        label.setLayout(box)
        label.setObjectName("frame")
        label.setStyleSheet("QWidget#frame {border: 1px solid grey; background-color: #8888dd}")

        pixmap = QPixmap('img/settings.png')
        pixmap = pixmap.scaled(50, 50)
        settings_button = QLabel(self)
        settings_button.setPixmap(pixmap)
        settings_button.setObjectName('img/settings.png')
        settings_button.mousePressEvent = self.settings_button_on_click

        soldi = QLabel(str(self.data.money) + ' soldi', self)
        soldi.setFont(font)
        soldi.setStyleSheet('background-color: yellow; border-top: 1px solid grey;')
        soldi.setFixedHeight(50)
        soldi.setContentsMargins(20, 10, 20, 10)

        box = QHBoxLayout(self)
        box.setAlignment(Qt.AlignTop)
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
        box.addWidget(label, alignment=Qt.AlignLeft)
        box.addWidget(soldi_widget, alignment=Qt.AlignLeft)
        box.addWidget(settings_widget, alignment=Qt.AlignRight)
        box.setContentsMargins(0, 0, 0, 0)
        frame = QWidget(self, flags=Qt.Widget)
        frame.setFixedHeight(150)
        frame.setLayout(box)
        frame.setObjectName("frame")
        frame.setStyleSheet("QWidget#frame {border: 1px solid grey}")

        frame1 = QFrame(flags=Qt.Widget)
        frame1.setFrameShape(QFrame.StyledPanel)

        box2 = QWidget(self, flags=Qt.Widget)
        box2.setObjectName("box2")
        box2.setStyleSheet("QWidget#box2 {border: 1px solid grey}")
        internal_layout = QVBoxLayout(self)
        internal_layout.setContentsMargins(10, 10, 10, 10)
        internal_layout.setSpacing(10)
        button = QPushButton('COMPITI', self)
        button.setFont(font)
        button.clicked.connect(controller.open_HomeworkCollectionWindow)
        internal_layout.addWidget(button, alignment=Qt.AlignVCenter)
        box2.setLayout(internal_layout)

        frame3 = QFrame(flags=Qt.Widget)
        frame3.setFrameShape(QFrame.StyledPanel)

        box4 = QWidget(self, flags=Qt.Widget)
        box4.setObjectName("box4")
        box4.setStyleSheet("QWidget#box4 {border: 1px solid grey}")
        internal_layout = QVBoxLayout(self)
        internal_layout.setContentsMargins(10, 10, 10, 10)
        internal_layout.setSpacing(10)
        button = QPushButton('NEGOZIO', self)
        button.setFont(font)
        button.clicked.connect(partial(controller.open_Abilities_Window, 1))
        internal_layout.addWidget(button, alignment=Qt.AlignVCenter)
        box4.setLayout(internal_layout)

        box = QWidget(self, flags=Qt.Widget)
        internal_layout = QHBoxLayout(self)
        internal_layout.setContentsMargins(0,0,0,0)
        internal_layout.setSpacing(10)
        internal_layout.addWidget(frame1)
        internal_layout.addWidget(box2)
        internal_layout.addWidget(frame3)
        internal_layout.addWidget(box4)
        box.setLayout(internal_layout)

        layout = QVBoxLayout(self)
        layout.setSpacing(10)
        layout.setContentsMargins(10,10,10,10)
        layout.addWidget(frame)
        layout.addWidget(box)

    def settings_button_on_click(self, event):
        confirm = SettingsWindow('Gamification - settings', self.data, None, parent=self)
        confirm.exec_()
        confirm.deleteLater()

    def set_image(self, name):
        pixmap = QPixmap(name)
        pixmap = pixmap.scaled(130,130)
        self.image.setPixmap(pixmap)
