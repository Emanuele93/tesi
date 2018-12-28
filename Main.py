import sys

from PyQt5 import QtWidgets
from windows.CodingWindow import CodingWindow

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    mainWin = CodingWindow()
    mainWin.show()
    sys.exit(app.exec_())


