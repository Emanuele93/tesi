from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtWidgets import QDialog, QPushButton, QWidget, QVBoxLayout, QLabel, QHBoxLayout


class ConfirmWindow(QDialog):
    def __init__(self, title, text, ok='Ok', cancel='Cancel', parent=None):
        QDialog.__init__(self, parent)
        self.setWindowTitle(title)
        self.setWindowIcon(QIcon("img/logo.png"))

        font = QFont()
        font.setPixelSize(15)
        text_widget = QLabel(self)
        text_widget.setText(text)
        text_widget.setFont(font)
        text_widget.setTextFormat(Qt.RichText)
        button_ok = QPushButton(ok, self)
        button_ok.clicked.connect(self.accept)
        button_ok.setFixedWidth(len(ok)*10 + 20)
        button_ok.setFont(font)
        button_cancel = QPushButton(cancel, self)
        button_cancel.clicked.connect(self.reject)
        button_cancel.setFont(font)
        if cancel is None:
            button_cancel.hide()
        else:
            button_cancel.setFixedWidth(len(cancel)*10 + 20)

        box = QHBoxLayout(self)
        box.setContentsMargins(0, 0, 0, 0)
        box.addWidget(button_ok)
        box.addWidget(button_cancel)
        widget = QWidget(self, flags=Qt.Widget)
        widget.setLayout(box)

        box = QVBoxLayout(self)
        box.setContentsMargins(20, 20, 20, 20)
        box.setSpacing(20)
        box.addWidget(text_widget)
        box.addWidget(widget)
