from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QDialog, QPushButton, QWidget, QVBoxLayout, QLabel, QHBoxLayout


class ConfirmWindow(QDialog):
    def __init__(self,title, text, ok='Ok', cancel='Cancel', parent=None):
        QDialog.__init__(self, parent)
        self.setWindowTitle(title)

        font = QFont()
        font.setPixelSize(15)
        text_widget = QLabel(self)
        text_widget.setText(text)
        text_widget.setFont(font)
        text_widget.setTextFormat(Qt.RichText)
        buttonOk = QPushButton(ok, self)
        buttonOk.clicked.connect(self.accept)
        buttonOk.setFixedWidth(len(ok)*10 + 20)
        buttonOk.setFont(font)
        buttonCancel = QPushButton(cancel, self)
        buttonCancel.clicked.connect(self.reject)
        buttonCancel.setFixedWidth(len(cancel)*10 + 20)
        buttonCancel.setFont(font)

        box = QHBoxLayout(self)
        box.setContentsMargins(0, 0, 0, 0)
        box.addWidget(buttonOk)
        box.addWidget(buttonCancel)
        widget = QWidget(self, flags=Qt.Widget)
        widget.setLayout(box)

        box = QVBoxLayout(self)
        box.setContentsMargins(20, 20, 20, 20)
        box.setSpacing(20)
        box.addWidget(text_widget)
        box.addWidget(widget)
