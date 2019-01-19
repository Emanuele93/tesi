import sys

from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QWidget, QApplication, QLabel


class Window(QWidget):
    def __init__(self):
        super(Window, self).__init__(flags=Qt.Window)
        self.setMinimumSize(QSize(600, 600))
        self.setWindowTitle("Prova")

        label = QLabel(self)
        pixmap = QPixmap('1.png')
        #pixmap = pixmap.scaled(50,50)
        label.setPixmap(pixmap)
        label.mousePressEvent = self.link_handler

    def link_handler(self, event):
        print('qui')

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = Window()
    win.show()
    sys.exit(app.exec_())
