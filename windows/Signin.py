from functools import partial
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtWidgets import QWidget, QLineEdit, QPushButton, QVBoxLayout, QLabel, QCheckBox, QButtonGroup, QHBoxLayout
from PyQt5.QtCore import *
import Server_call_master


class Signin(QWidget):
    def __init__(self, login):
        super(Signin, self).__init__(flags=Qt.Window)
        self.setWindowTitle("Signin")
        self.setWindowIcon(QIcon("img/logo.png"))
        self.setFixedSize(QSize(500, 650))
        self.login = login
        font = QFont()
        font.setPixelSize(20)

        title = QLabel('THE GAME OF PROGRAMMING', self)
        title.setFont(font)
        title.setStyleSheet('background-color: #5994d3; border: 1px solid grey; '
                            'border-left: 0px solid grey; border-right: 0px solid grey')
        title.setFixedSize(500, 60)
        title.setAlignment(Qt.AlignCenter)

        font.setPixelSize(20)
        subtitle = QLabel('Inserire i dati di registrazione:', self)
        subtitle.setFont(font)
        subtitle.setAlignment(Qt.AlignCenter)

        name = QLineEdit(self)
        name.setPlaceholderText("Nome")
        name.setFixedWidth(400)
        name.setFont(font)
        name.setTextMargins(10, 2, 10, 2)
        self.name = False

        surname = QLineEdit(self)
        surname.setPlaceholderText("Cognome")
        surname.setFixedWidth(400)
        surname.setFont(font)
        surname.setTextMargins(10, 2, 10, 2)
        self.surname = False

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

        check_1 = QCheckBox("Studente")
        check_1.setFont(font)
        check_1.setChecked(True)
        check_2 = QCheckBox("Docente")
        check_2.setFont(font)
        check_2.setChecked(False)

        box = QHBoxLayout(self)
        box.setContentsMargins(0, 0, 0, 0)
        box.setSpacing(50)
        box.addWidget(check_1, alignment=Qt.AlignVCenter)
        box.addWidget(check_2, alignment=Qt.AlignVCenter)
        user_type = QWidget(self, flags=Qt.Widget)
        user_type.setLayout(box)

        self.bg = QButtonGroup()
        self.bg.addButton(check_1, 1)
        self.bg.addButton(check_2, 2)

        check_1 = QCheckBox("Python")
        check_1.setFont(font)
        check_1.setChecked(True)
        check_2 = QCheckBox("C/C++")
        check_2.setFont(font)
        check_2.setChecked(False)

        box = QHBoxLayout(self)
        box.setContentsMargins(0, 0, 0, 0)
        box.setSpacing(50)
        box.addWidget(check_1, alignment=Qt.AlignVCenter)
        box.addWidget(check_2, alignment=Qt.AlignVCenter)
        language = QWidget(self, flags=Qt.Widget)
        language.setLayout(box)
        language.hide()

        self.bg2 = QButtonGroup()
        self.bg2.addButton(check_1, 1)
        self.bg2.addButton(check_2, 2)

        box = QVBoxLayout(self)
        box.setSpacing(15)
        box.setContentsMargins(0, 0, 0, 0)
        box.addWidget(user_type, alignment=Qt.AlignVCenter)
        box.addWidget(language, alignment=Qt.AlignVCenter)
        user_type = QWidget(self, flags=Qt.Widget)
        user_type.setLayout(box)

        button = QPushButton('Registra', self)
        button.setFont(font)
        button.setFixedSize(100, 50)
        button.setEnabled(False)

        message = QLabel("Registrazione effettuata!\n\nPer accedere devi attendere la conferma del docente.")
        message.setFont(font)
        message.setWordWrap(True)
        message.hide()
        message.setFixedHeight(480)
        message.setAlignment(Qt.AlignHCenter)
        message.setContentsMargins(0, 50, 0, 0)

        name.textChanged.connect(partial(self.name_changed, name, button))
        surname.textChanged.connect(partial(self.surname_changed, surname, button))
        user.textChanged.connect(partial(self.user_changed, user, button))
        password.textChanged.connect(partial(self.password_changed, password, button))
        classe.textChanged.connect(partial(self.classe_changed, classe, button))
        button.clicked.connect(partial(self.button_on_click, user, password, classe, name, surname, user_type, button,
                                       message, subtitle))

        font.setPixelSize(15)
        font.setUnderline(True)
        login_widget = QLabel('Accedi', self)
        login_widget.setFont(font)
        login_widget.setStyleSheet("color: blue")
        login_widget.setContentsMargins(5, 5, 25, 5)
        login_widget.mousePressEvent = self.open_login

        box = QVBoxLayout(self)
        box.setSpacing(30)
        box.setContentsMargins(10, 20, 10, 0)
        box.addWidget(subtitle, alignment=Qt.AlignHCenter)
        box.addWidget(name, alignment=Qt.AlignHCenter)
        box.addWidget(surname, alignment=Qt.AlignHCenter)
        box.addWidget(user, alignment=Qt.AlignHCenter)
        box.addWidget(password, alignment=Qt.AlignHCenter)
        box.addWidget(classe, alignment=Qt.AlignHCenter)
        box.addWidget(user_type, alignment=Qt.AlignHCenter)
        box.addWidget(button, alignment=Qt.AlignHCenter)
        box.addWidget(message, alignment=Qt.AlignHCenter)
        form = QWidget(self, flags=Qt.Widget)
        form.setLayout(box)

        box = QVBoxLayout(self)
        box.setContentsMargins(0, 0, 0, 0)
        box.setAlignment(Qt.AlignTop)
        box.setSpacing(25)
        box.addWidget(title, alignment=Qt.AlignHCenter)
        box.addWidget(form, alignment=Qt.AlignHCenter)
        box.addWidget(login_widget, alignment=Qt.AlignRight)
        self.bg.buttonClicked.connect(partial(self.change_user_type, language, box))

    def change_user_type(self, language, box):
        if self.bg.checkedId() == 2:
            language.show()
            box.setSpacing(0)
        else:
            language.hide()
            box.setSpacing(25)

    def name_changed(self, name, button):
        if name.text().strip() != '':
            if len(name.text().strip()) > 20 or '"' in name.text() or "'" in name.text() or "\\" in name.text() \
                    or "," in name.text():
                name.setStyleSheet('color: red')
            else:
                name.setStyleSheet('color: black')
                self.name = True
                if self.name and self.surname and self.user and self.password and self.classe:
                    button.setEnabled(True)
                return
        else:
            name.setStyleSheet('color: black')
        self.name = False
        button.setEnabled(False)

    def surname_changed(self, surname, button):
        if surname.text().strip() != '':
            if len(surname.text().strip()) > 20 or '"' in surname.text() or "'" in surname.text() \
                    or "\\" in surname.text() or "," in surname.text():
                surname.setStyleSheet('color: red')
            else:
                surname.setStyleSheet('color: black')
                self.surname = True
                if self.name and self.surname and self.user and self.password and self.classe:
                    button.setEnabled(True)
                return
        else:
            surname.setStyleSheet('color: black')
        self.surname = False
        button.setEnabled(False)

    def user_changed(self, user, button):
        if user.text().strip() != '':
            if len(user.text().strip()) > 20 or '"' in user.text() or "'" in user.text() \
                    or "\\" in user.text() or "," in user.text():
                user.setStyleSheet('color: red')
            else:
                user.setStyleSheet('color: black')
                self.user = True
                if self.name and self.surname and self.user and self.password and self.classe:
                    button.setEnabled(True)
                return
        else:
            user.setStyleSheet('color: black')
        self.user = False
        button.setEnabled(False)

    def password_changed(self, password, button):
        if password.text().strip() != '':
            if len(password.text().strip()) > 20 or '"' in password.text() or "'" in password.text() \
                    or "\\" in password.text() or "," in password.text():
                password.setStyleSheet('color: red')
            else:
                password.setStyleSheet('color: black')
                self.password = True
                if self.name and self.surname and self.user and self.password and self.classe:
                    button.setEnabled(True)
                return
        else:
            password.setStyleSheet('color: black')
        self.password = False
        button.setEnabled(False)

    def classe_changed(self, classe, button):
        if classe.text().strip() != '':
            if len(classe.text().strip()) > 20 or '"' in classe.text() or "'" in classe.text() \
                    or "\\" in classe.text() or "," in classe.text():
                classe.setStyleSheet('color: red')
            else:
                classe.setStyleSheet('color: black')
                self.classe = True
                if self.name and self.surname and self.user and self.password and self.classe:
                    button.setEnabled(True)
                return
        else:
            classe.setStyleSheet('color: black')
        self.classe = False
        button.setEnabled(False)

    def button_on_click(self, user, password, classe, name, surname, check, button, message, subtitle):
        r = Server_call_master.access("/singin.php", ['ok', 'ready', 'username', 'class'],
                                      {'username': user.text().strip(), 'password': password.text().strip(),
                                       'class': classe.text().strip(), 'name': name.text().strip(),
                                       'surname': surname.text().strip(), 'type': (self.bg.checkedId() - 1),
                                       'language': self.bg2.checkedId()})
        if r == 'ok':
            name.hide()
            subtitle.hide()
            surname.hide()
            user.hide()
            password.hide()
            classe.hide()
            check.hide()
            button.hide()
            message.show()
            f = open('user_info.txt', "w")
            f.write("\n\n\nTrue\n20\n3")
            f.close()
        elif r == 'ready':
            self.close()
            self.login.button_on_click(user, password, classe)
        elif r == 'username':
            user.setStyleSheet('color: red')
            password.setStyleSheet('color: black')
            classe.setStyleSheet('color: black')
        elif r == 'class':
            user.setStyleSheet('color: black')
            password.setStyleSheet('color: black')
            classe.setStyleSheet('color: red')

    def open_login(self, event):
        self.close()
        self.login.show()
