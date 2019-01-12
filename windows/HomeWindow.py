from PyQt5.QtWidgets import QWidget, QPushButton, QHBoxLayout, QVBoxLayout, QFrame
from PyQt5.QtCore import *


class HomeWindow(QWidget):
    def __init__(self, controller):
        super(HomeWindow, self).__init__(controller, flags=Qt.Widget)
        self.setMinimumSize(QSize(800, 400))
        self.setWindowTitle("Gamification")

        frame = QFrame(flags=Qt.Widget)
        frame.setFrameShape(QFrame.StyledPanel)
        frame.setFixedHeight(100)

        frame1 = QFrame(flags=Qt.Widget)
        frame1.setFrameShape(QFrame.StyledPanel)

        box2 = QWidget(self, flags=Qt.Widget)
        box2.setObjectName("box2")
        box2.setStyleSheet("QWidget#box2 {border: 1px solid grey}")
        internal_layout2 = QVBoxLayout(self)
        internal_layout2.setContentsMargins(10, 10, 10, 10)
        internal_layout2.setSpacing(10)
        button = QPushButton('COMPITI', self)
        button.clicked.connect(controller.open_HomeworkCollectionWindow)
        internal_layout2.addWidget(button, alignment=Qt.AlignVCenter)
        box2.setLayout(internal_layout2)

        frame3 = QFrame(flags=Qt.Widget)
        frame3.setFrameShape(QFrame.StyledPanel)

        frame4 = QFrame(flags=Qt.Widget)
        frame4.setFrameShape(QFrame.StyledPanel)

        box = QWidget(self, flags=Qt.Widget)
        internal_layout = QHBoxLayout(self)
        internal_layout.setContentsMargins(0,0,0,0)
        internal_layout.setSpacing(10)
        internal_layout.addWidget(frame1)
        internal_layout.addWidget(box2)
        internal_layout.addWidget(frame3)
        internal_layout.addWidget(frame4)
        box.setLayout(internal_layout)

        layout = QVBoxLayout(self)
        layout.setSpacing(10)
        layout.setContentsMargins(10,10,10,10)
        layout.addWidget(frame)
        layout.addWidget(box)

