from PyQt5.QtWidgets import QWidget, QPushButton, QHBoxLayout, QVBoxLayout, QFrame
from PyQt5.QtCore import *


class HomeWindow(QWidget):
    def __init__(self, controller):
        super(HomeWindow, self).__init__(controller, flags=Qt.Widget)
        controller.setWindowTitle("Gamification")

        frame = QFrame(flags=Qt.Widget)
        frame.setFrameShape(QFrame.StyledPanel)
        frame.setFixedHeight(100)

        frame1 = QFrame(flags=Qt.Widget)
        frame1.setFrameShape(QFrame.StyledPanel)

        box2 = QWidget(self, flags=Qt.Widget)
        box2.setObjectName("box2")
        box2.setStyleSheet("QWidget#box2 {border: 1px solid grey}")
        internal_layout = QVBoxLayout(self)
        internal_layout.setContentsMargins(10, 10, 10, 10)
        internal_layout.setSpacing(10)
        button = QPushButton('COMPITI', self)
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
        button.clicked.connect(controller.open_Abilities_Window)
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

