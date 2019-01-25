import sys

from PyQt5.QtWidgets import QWidget, QHBoxLayout, QApplication, QDialog
from PyQt5.QtCore import *

from Data import Data
from windows.AbilitiesWindow import AbilitiesWindow
from windows.HomeWindow import HomeWindow
from windows.HomeworkCollectionWindow import HomeworkCollectionWindow


class WindowsController(QWidget):
    def __init__(self):
        super(WindowsController, self).__init__(flags=Qt.Window)
        self.setFixedSize(QSize(800, 600))
        self.setWindowTitle("Gamification")

        self.data = Data()
        self.box = QHBoxLayout(self)
        self.box.setContentsMargins(0, 0, 0, 0)
        self.mainWin = HomeWindow(self, self.data)
        self.box.addWidget(self.mainWin)

        self.mainWin.show()

    def open_window(self, window):
        self.mainWin.setParent(None)
        self.mainWin = window
        self.box.addWidget(self.mainWin)
        self.mainWin.show()

    def open_MainWindow(self):
        self.open_window(HomeWindow(self, self.data))

    def open_HomeworkCollectionWindow(self):
        self.open_window(HomeworkCollectionWindow(self, self.data))

    def open_Abilities_Window(self, page, event):
        self.open_window(AbilitiesWindow(self, self.data, page))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = WindowsController()
    win.show()
    sys.exit(app.exec_())
