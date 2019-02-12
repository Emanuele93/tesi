from functools import partial

import requests
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QWidget, QPushButton, QVBoxLayout, QLineEdit, QDialog, QHBoxLayout
from PyQt5.QtCore import *

from Data import Data
from windows.ConfirmWindow import ConfirmWindow


class LoginWindow(QWidget):
    def __init__(self, home):
        super(LoginWindow, self).__init__(home, flags=Qt.Widget)
        home.setWindowTitle("Gamification - Login")
        home.setFixedSize(QSize(500, 400))
        font = QFont()
        font.setPixelSize(20)
        self.home = home

        user = QLineEdit(self)
        user.setPlaceholderText("Username")
        user.setFixedWidth(400)
        user.setFont(font)
        user.setTextMargins(10, 2, 10, 2)
        self.user = False

        password = QLineEdit(self)
        password.setPlaceholderText("Password")
        password.setFixedWidth(400)
        password.setFont(font)
        password.setTextMargins(10, 2, 10, 2)
        self.password = False

        classe = QLineEdit(self)
        classe.setPlaceholderText("Classe")
        classe.setFixedWidth(400)
        classe.setFont(font)
        classe.setTextMargins(10, 2, 10, 2)
        self.classe = False

        button1 = QPushButton('Login', self)
        button1.setFont(font)
        button1.setFixedSize(100, 50)
        button1.setEnabled(False)

        button2 = QPushButton('Registrati', self)
        button2.setFont(font)
        button2.setFixedSize(150, 50)
        button2.setEnabled(False)

        box = QHBoxLayout(self)
        box.setContentsMargins(0, 0, 0, 0)
        box.addWidget(button1, alignment=Qt.AlignHCenter)
        box.addWidget(button2, alignment=Qt.AlignHCenter)
        button = QWidget(self, flags=Qt.Widget)
        button.setLayout(box)
        button.setFixedHeight(50)

        user.textChanged.connect(partial(self.user_changed, user, button1, button2))
        password.textChanged.connect(partial(self.password_changed, password, button1, button2))
        classe.textChanged.connect(partial(self.classe_changed, classe, button1, button2))
        button1.clicked.connect(partial(self.button1_on_click, user, password, classe))
        button2.clicked.connect(partial(self.button2_on_click, user, password, classe))

        box = QVBoxLayout(self)
        box.addWidget(user, alignment=Qt.AlignHCenter)
        box.addWidget(password, alignment=Qt.AlignHCenter)
        box.addWidget(classe, alignment=Qt.AlignHCenter)
        box.addWidget(button, alignment=Qt.AlignHCenter)

    def user_changed(self, user, button1, button2):
        if user.text().strip() != '':
            if len(user.text().strip()) > 20:
                user.setStyleSheet('color: red')
            else:
                user.setStyleSheet('color: black')
                self.user = True
                if self.user and self.password and self.classe:
                    button1.setEnabled(True)
                    button2.setEnabled(True)
                return
        self.user = False
        button1.setEnabled(False)
        button2.setEnabled(False)

    def password_changed(self, password, button1, button2):
        if password.text().strip() != '':
            if len(password.text().strip()) > 20:
                password.setStyleSheet('color: red')
            else:
                password.setStyleSheet('color: black')
                self.password = True
                if self.user and self.password and self.classe:
                    button1.setEnabled(True)
                    button2.setEnabled(True)
                return
        self.password = False
        button1.setEnabled(False)
        button2.setEnabled(False)

    def classe_changed(self, classe, button1, button2):
        if classe.text().strip() != '':
            if len(classe.text().strip()) > 20:
                classe.setStyleSheet('color: red')
            else:
                classe.setStyleSheet('color: black')
                self.classe = True
                if self.user and self.password and self.classe:
                    button1.setEnabled(True)
                    button2.setEnabled(True)
                return
        self.classe = False
        button1.setEnabled(False)
        button2.setEnabled(False)

    def button1_on_click(self, user, password, classe):
        try:
            r = requests.post("http://programmingisagame.netsons.org/login.php",
                              data={'username': user.text().strip(), 'password': password.text().strip(),
                                    'class': classe.text().strip()})
            if r.text == 'ok':
                f = open('user_info.txt', "w")
                f.write(
                    user.text().strip() + "\n" + password.text().strip() + "\n" + classe.text().strip() + "\nTrue\n20")
                f.close()
                self.home.setFixedSize(QSize(800, 600))
                self.home.data = Data()
                self.home.open_MainWindow()
            elif r.text == 'username':
                user.setStyleSheet('color: red')
                password.setStyleSheet('color: black')
                classe.setStyleSheet('color: black')
            elif r.text == 'password':
                user.setStyleSheet('color: black')
                password.setStyleSheet('color: red')
                classe.setStyleSheet('color: black')
            elif r.text == 'classe':
                user.setStyleSheet('color: black')
                password.setStyleSheet('color: black')
                classe.setStyleSheet('color: red')
        except requests.exceptions.RequestException:
            confirm = ConfirmWindow('Gamification - Errore di connessione',
                                    "<span style=\" color: red;\"> Attenzione, si sono verificati problemi di "
                                    "connessione<br>Controllare la propria connessione internet</span>",
                                    ok="Chiudi il programma", cancel=None)
            if confirm.exec_() == QDialog.Accepted:
                print('ok')
            confirm.deleteLater()
            exit()

    def button2_on_click(self, user, password, classe):
        try:
            r = requests.post("http://programmingisagame.netsons.org/singin.php",
                              data={'username': user.text().strip(), 'password': password.text().strip(),
                                    'class': classe.text().strip()})
            if r.text == 'ok':
                f = open('user_info.txt', "w")
                f.write(
                    user.text().strip() + "\n" + password.text().strip() + "\n" + classe.text().strip() + "\nTrue\n20")
                f.close()
                self.home.setFixedSize(QSize(800, 600))
                self.home.data = Data()
                self.home.open_MainWindow()
            elif r.text == 'username':
                user.setStyleSheet('color: red')
                password.setStyleSheet('color: black')
                classe.setStyleSheet('color: black')
            elif r.text == 'class':
                user.setStyleSheet('color: black')
                password.setStyleSheet('color: black')
                classe.setStyleSheet('color: red')
        except requests.exceptions.RequestException:
            confirm = ConfirmWindow('Gamification - Errore di connessione',
                                    "<span style=\" color: red;\"> Attenzione, si sono verificati problemi di "
                                    "connessione<br>Controllare la propria connessione internet</span>",
                                    ok="Chiudi il programma", cancel=None)
            if confirm.exec_() == QDialog.Accepted:
                print('ok')
            confirm.deleteLater()
            exit()
