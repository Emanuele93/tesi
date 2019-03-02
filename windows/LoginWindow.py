from functools import partial

import requests
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QWidget, QPushButton, QVBoxLayout, QLineEdit, QDialog, QLabel
from PyQt5.QtCore import *
from Data import Data
from windows.ConfirmWindow import ConfirmWindow


class LoginWindow(QWidget):
    def __init__(self, home):
        super(LoginWindow, self).__init__(flags=Qt.Window)
        self.setWindowTitle("Gamification - Login")
        self.setFixedSize(QSize(500, 400))
        font = QFont()
        font.setPixelSize(25)
        self.home = home

        title = QLabel('THE GAME OF PROGRAMMING', self)
        title.setFont(font)
        title.setStyleSheet('background-color: #59d394; border: 1px solid grey; '
                            'border-left: 0px solid grey; border-right: 0px solid grey')
        title.setFixedSize(500, 60)
        title.setAlignment(Qt.AlignCenter)

        font.setPixelSize(20)
        subtitle = QLabel('Inserire i dati di accesso:', self)
        subtitle.setFont(font)
        subtitle.setAlignment(Qt.AlignCenter)

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
        password.setEchoMode(QLineEdit.Password)
        self.password = False

        classe = QLineEdit(self)
        classe.setPlaceholderText("Classe")
        classe.setFixedWidth(400)
        classe.setFont(font)
        classe.setTextMargins(10, 2, 10, 2)
        self.classe = False

        button = QPushButton('Login', self)
        button.setFont(font)
        button.setFixedSize(100, 50)
        button.setEnabled(False)

        user.textChanged.connect(partial(self.user_changed, user, button))
        password.textChanged.connect(partial(self.password_changed, password, button))
        classe.textChanged.connect(partial(self.classe_changed, classe, button))
        button.clicked.connect(partial(self.button_on_click, user, password, classe))

        box = QVBoxLayout(self)
        box.setAlignment(Qt.AlignTop)
        box.setSpacing(30)
        box.addWidget(subtitle, alignment=Qt.AlignHCenter)
        box.addWidget(user, alignment=Qt.AlignHCenter)
        box.addWidget(password, alignment=Qt.AlignHCenter)
        box.addWidget(classe, alignment=Qt.AlignHCenter)
        box.addWidget(button, alignment=Qt.AlignHCenter)
        form = QWidget(self, flags=Qt.Widget)
        form.setLayout(box)

        box = QVBoxLayout(self)
        box.setContentsMargins(0, 0, 0, 0)
        box.setAlignment(Qt.AlignTop)
        box.setSpacing(7)
        box.addWidget(title, alignment=Qt.AlignHCenter)
        box.addWidget(form, alignment=Qt.AlignHCenter)

    def user_changed(self, user, button):
        if user.text().strip() != '':
            if len(user.text().strip()) > 20:
                user.setStyleSheet('color: red')
            else:
                user.setStyleSheet('color: black')
                self.user = True
                if self.user and self.password and self.classe:
                    button.setEnabled(True)
                return
        self.user = False
        button.setEnabled(False)

    def password_changed(self, password, button):
        if password.text().strip() != '':
            if len(password.text().strip()) > 20:
                password.setStyleSheet('color: red')
            else:
                password.setStyleSheet('color: black')
                self.password = True
                if self.user and self.password and self.classe:
                    button.setEnabled(True)
                return
        self.password = False
        button.setEnabled(False)

    def classe_changed(self, classe, button):
        if classe.text().strip() != '':
            if len(classe.text().strip()) > 20:
                classe.setStyleSheet('color: red')
            else:
                classe.setStyleSheet('color: black')
                self.classe = True
                if self.user and self.password and self.classe:
                    button.setEnabled(True)
                return
        self.classe = False
        button.setEnabled(False)

    def button_on_click(self, user, password, classe):
        try:
            r = requests.post("http://programmingisagame.netsons.org/login.php",
                              data={'username': user.text().strip(), 'password': password.text().strip(),
                                    'class': classe.text().strip()})
            if r.text == 'ok':
                f = open('user_info.txt', "w")
                f.write(
                    user.text().strip() + "\n" + password.text().strip() + "\n" + classe.text().strip() + "\nTrue\n20")
                f.close()
                self.home.data = Data()
                self.home.open_MainWindow()
                self.home.show()
                self.close()
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
