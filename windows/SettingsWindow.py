import json
from functools import partial

import requests
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QFont, QPixmap, QIcon
from PyQt5.QtWidgets import QDialog, QPushButton, QWidget, QVBoxLayout, QLabel, QHBoxLayout, QScrollArea, QCheckBox, \
    QButtonGroup, QAbstractButton

from Data import DefaultColorStyles
from windows.ConfirmWindow import ConfirmWindow


class SettingsWindow(QDialog):
    def __init__(self, title, data, exercise_window, parent=None):
        QDialog.__init__(self, parent)
        self.setWindowTitle(title)
        self.setWindowIcon(QIcon("img/logo.png"))
        self.setFixedSize(QSize(465, 600))
        self.exercise_window = exercise_window
        self.parent = parent
        self.data = data
        self.current_image_label = None
        self.current_button = None
        self.current_key = None
        self.color_buttons = {}
        self.color_keys = {}
        self.check_keys = {}
        self.color_styles = \
            data.color_styles.__copy__() if exercise_window is None or exercise_window.exercise.color_styles is None \
                else exercise_window.exercise.color_styles
        self.lib = {
            'Colore sfondo (codice): ': self.color_styles.code_background_color,
            'Colore sfondo (risultati): ': self.color_styles.results_background_color,
            'Colore sfondo (risultati sbagliati): ': self.color_styles.error_results_background_color,
            'Colore testo (codice): ': self.color_styles.code_text_color,
            'Colore testo (risultati): ': self.color_styles.results_text_color,
            'Colore testo (risultati sbagliati): ': self.color_styles.error_results_text_color,
            'Colore commenti (# linea unica): ': self.color_styles.comment_color,
            "Colore commenti (''' più linee): ": self.color_styles.multi_line_comment_color,
            'Colore stringhe: ': self.color_styles.string_color
        }

        font = QFont()
        font.setPixelSize(17)
        self.data.get_class_components()

        self.personal_settings_button = QPushButton("Impostazioni personali", self)
        self.personal_settings_button.clicked.connect(self.personal_settings_button_on_click)
        self.personal_settings_button.setFixedHeight(55)
        self.personal_settings_button.setFont(font)

        text_temp = "Colorazione preferita\ndegli esercizi" \
            if exercise_window is None or self.exercise_window.exercise.id is None else "Colorazione dell'esercizio"
        self.exercise_settings_button = QPushButton(text_temp, self)
        self.exercise_settings_button.clicked.connect(self.exercise_settings_button_on_click)
        self.exercise_settings_button.setFixedHeight(55)
        self.exercise_settings_button.setFont(font)
        self.exercise_settings_button.setMinimumWidth(190)

        if self.data.my_name in self.data.my_proff:
            self.class_management_settings_widget = QScrollArea(self)
            self.class_management_settings_widget.setWidget(self.get_users_widget())
            self.class_management_settings_widget.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

            self.advanced_settings_widget = QScrollArea(self)
            self.advanced_settings_widget.setWidget(self.get_advanced_settings_widget())
            self.advanced_settings_widget.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.personal_settings_widget = QScrollArea(self)
        self.personal_settings_widget.setWidget(self.get_personal_settings_widget())
        self.personal_settings_widget.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.exercise_settings_widget = QScrollArea(self)
        self.exercise_settings_widget.setWidget(self.get_exercise_settings_widget())
        self.exercise_settings_widget.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.selection_color_widget = self.get_selection_color_widget()
        self.selection_image_widget = self.get_selection_image_widget()

        box = QHBoxLayout(self)
        box.setContentsMargins(0, 0, 0, 0)
        box.setSpacing(0)
        box.addWidget(self.personal_settings_button)
        box.addWidget(self.exercise_settings_button)
        widget = QWidget(self, flags=Qt.Widget)
        widget.setLayout(box)

        box = QVBoxLayout(self)
        box.setContentsMargins(0, 0, 0, 0)
        box.setSpacing(0)
        box.addWidget(widget)
        if self.data.my_name in self.data.my_proff:
            box.addWidget(self.class_management_settings_widget)
            box.addWidget(self.advanced_settings_widget)
        box.addWidget(self.personal_settings_widget)
        box.addWidget(self.exercise_settings_widget)
        box.addWidget(self.selection_color_widget)
        box.addWidget(self.selection_image_widget)

        if exercise_window is None:
            self.personal_settings_button_on_click()
        else:
            self.exercise_settings_button_on_click()

    def class_management_on_click(self):
        self.advanced_settings_widget.hide()
        self.class_management_settings_widget.show()

    def advanced_settings_button_on_click(self):
        self.class_management_settings_widget.hide()
        self.advanced_settings_widget.show()
        self.personal_settings_widget.hide()
        self.exercise_settings_widget.hide()
        self.selection_color_widget.hide()
        self.selection_image_widget.hide()
        self.personal_settings_button.setStyleSheet('background-color: #ffdd55')
        self.exercise_settings_button.setStyleSheet('background-color: #ffdd55')

    def personal_settings_button_on_click(self):
        if self.data.my_name in self.data.my_proff:
            self.class_management_settings_widget.hide()
            self.advanced_settings_widget.hide()
        self.personal_settings_widget.show()
        self.exercise_settings_widget.hide()
        self.selection_color_widget.hide()
        self.selection_image_widget.hide()
        self.personal_settings_button.setStyleSheet('background-color: #dd9933')
        self.exercise_settings_button.setStyleSheet('background-color: #ffdd55')

    def exercise_settings_button_on_click(self):
        if self.data.my_name in self.data.my_proff:
            self.class_management_settings_widget.hide()
            self.advanced_settings_widget.hide()
        self.personal_settings_widget.hide()
        self.exercise_settings_widget.show()
        self.selection_color_widget.hide()
        self.selection_image_widget.hide()
        self.personal_settings_button.setStyleSheet('background-color: #ffdd55')
        self.exercise_settings_button.setStyleSheet('background-color: #dd9933')

    def show_selection_color_widget(self, text, button):
        if self.current_button == button and self.selection_color_widget.isVisible():
            self.selection_color_widget.hide()
        else:
            self.current_key = text
            self.current_button = button
            self.selection_color_title.setText(text)
            self.selection_color_widget.show()

    def get_users_widget(self):
        box = QVBoxLayout(self)
        box.setAlignment(Qt.AlignTop)
        try:
            r = requests.post("http://programmingisagame.netsons.org/get_class_users.php",
                              data={'username': self.data.my_name, 'password': self.data.my_psw,
                                    'class': self.data.my_class})
            users = json.loads(r.text)

            for i in users:
                box.addWidget(self.make_user_wait_widget(i['username'], i['name'], i['surname'],
                                                         True if i['student_type'] == '1' else False,
                                                         True if i['approved'] == '1' else False))
        except requests.exceptions.RequestException as e:
            confirm = ConfirmWindow('Errore di connessione',
                                    "<span style=\" color: red;\"> Attenzione, si sono verificati problemi di "
                                    "connessione<br>Controllare la connessione internet e riprovare</span>",
                                    ok="Ok", cancel=None)
            if confirm.exec_() == QDialog.Accepted:
                print('ok')
            confirm.deleteLater()
        users = QWidget(self, flags=Qt.Widget)
        users.setLayout(box)

        font = QFont()
        font.setPixelSize(17)
        intro = QLabel("Componenti della classe " + self.data.my_class , self)
        intro.setFont(font)
        intro.setFixedHeight(20)
        box = QVBoxLayout(self)
        box.setContentsMargins(0, 20, 0, 0)
        box.addWidget(intro, alignment=Qt.AlignHCenter)
        box.addWidget(users)
        users = QWidget(self, flags=Qt.Widget)
        users.setLayout(box)

        users.setFixedWidth(440)
        return users

    def get_advanced_settings_widget(self):
        font = QFont()
        font.setPixelSize(15)

        intro_correction_type = QLabel("Soggetto incaricato della correzione dei compiti:", self)
        intro_correction_type.setFont(font)
        font.setPixelSize(14)
        check_1 = QCheckBox("Nessuno, ricompensa fornita automaticamente")
        check_1.setFont(font)
        check_1.setChecked(self.data.correction_type == 0)
        check_2 = QCheckBox("Il creatore dell'esercizio")
        check_2.setFont(font)
        check_2.setChecked(self.data.correction_type == 1)
        check_3 = QCheckBox("Il docente")
        check_3.setFont(font)
        check_3.setChecked(self.data.correction_type == 2)

        self.bg6 = QButtonGroup()
        self.bg6.addButton(check_1, 1)
        self.bg6.addButton(check_2, 2)
        self.bg6.addButton(check_3, 3)
        self.bg6.buttonClicked[QAbstractButton].connect(self.set_correction_type)

        box = QVBoxLayout(self)
        box.setAlignment(Qt.AlignLeft)
        box.setContentsMargins(50, 0, 0, 0)
        box.addWidget(check_1)
        box.addWidget(check_2)
        box.addWidget(check_3)
        correction_type = QWidget(self, flags=Qt.Widget)
        correction_type.setLayout(box)

        box = QVBoxLayout(self)
        box.setAlignment(Qt.AlignLeft)
        box.setSpacing(15)
        box.addWidget(intro_correction_type)
        box.addWidget(correction_type)
        correction_type = QWidget(self, flags=Qt.Widget)
        correction_type.setLayout(box)

        font.setPixelSize(15)
        intro_approving_type = QLabel("Approvazione degli esercizi: ", self)
        intro_approving_type.setFont(font)
        check_1 = QCheckBox("Automatica")
        check_1.setFont(font)
        check_1.setChecked(self.data.approving_type == 0)
        check_2 = QCheckBox("Manuale")
        check_2.setFont(font)
        check_2.setChecked(self.data.approving_type == 1)

        self.bg5 = QButtonGroup()
        self.bg5.addButton(check_1, 1)
        self.bg5.addButton(check_2, 2)
        self.bg5.buttonClicked[QAbstractButton].connect(self.set_approving_type)

        box = QHBoxLayout(self)
        box.setContentsMargins(50, 0, 0, 0)
        box.setAlignment(Qt.AlignLeft)
        box.setSpacing(35)
        box.addWidget(check_1)
        box.addWidget(check_2)
        approving_type = QWidget(self, flags=Qt.Widget)
        approving_type.setLayout(box)

        box = QVBoxLayout(self)
        box.setAlignment(Qt.AlignLeft)
        box.addWidget(intro_approving_type)
        box.addWidget(approving_type)
        box.setSpacing(15)
        approving_type = QWidget(self, flags=Qt.Widget)
        approving_type.setLayout(box)

        intro_student_exercises_visible = QLabel("Compiti non approvati: ", self)
        intro_student_exercises_visible.setFont(font)
        check_1 = QCheckBox("Visibili")
        check_1.setFont(font)
        check_1.setChecked(self.data.student_exercises_visible)
        check_2 = QCheckBox("Non visibili")
        check_2.setFont(font)
        check_2.setChecked(not self.data.student_exercises_visible)

        self.bg4 = QButtonGroup()
        self.bg4.addButton(check_1, 1)
        self.bg4.addButton(check_2, 2)
        self.bg4.buttonClicked[QAbstractButton].connect(self.set_student_exercises_visible)

        box = QHBoxLayout(self)
        box.setContentsMargins(50, 0, 0, 0)
        box.setAlignment(Qt.AlignLeft)
        box.setSpacing(35)
        box.addWidget(check_1)
        box.addWidget(check_2)
        student_exercises_visible = QWidget(self, flags=Qt.Widget)
        student_exercises_visible.setLayout(box)

        box = QVBoxLayout(self)
        box.setAlignment(Qt.AlignLeft)
        box.setSpacing(15)
        box.addWidget(intro_student_exercises_visible)
        box.addWidget(student_exercises_visible)
        student_exercises_visible = QWidget(self, flags=Qt.Widget)
        student_exercises_visible.setLayout(box)

        intro_comments_visible = QLabel("Commenti alle soluzioni degli esercizi: ", self)
        intro_comments_visible.setFont(font)
        check_1 = QCheckBox("Abilitati")
        check_1.setFont(font)
        check_1.setChecked(self.data.comments_visible)
        check_2 = QCheckBox("Disabilitati")
        check_2.setFont(font)
        check_2.setChecked(not self.data.comments_visible)

        self.bg7 = QButtonGroup()
        self.bg7.addButton(check_1, 1)
        self.bg7.addButton(check_2, 2)
        self.bg7.buttonClicked[QAbstractButton].connect(self.set_comments_visible)

        box = QHBoxLayout(self)
        box.setContentsMargins(50, 0, 0, 0)
        box.setAlignment(Qt.AlignLeft)
        box.setSpacing(15)
        box.addWidget(check_1)
        box.addWidget(check_2)
        comments_visible = QWidget(self, flags=Qt.Widget)
        comments_visible.setLayout(box)

        box = QVBoxLayout(self)
        box.setAlignment(Qt.AlignLeft)
        box.setSpacing(15)
        box.addWidget(intro_comments_visible)
        box.addWidget(comments_visible)
        comments_visible = QWidget(self, flags=Qt.Widget)
        comments_visible.setLayout(box)

        class_management = QPushButton('Gestione classe', self)
        class_management.setFont(font)
        class_management.setFixedSize(120, 40)
        class_management.clicked.connect(self.class_management_on_click)

        box = QVBoxLayout(self)
        box.setContentsMargins(10, 10, 0, 20)
        box.addWidget(class_management, alignment=Qt.AlignRight)
        class_management_w = QWidget(self, flags=Qt.Widget)
        class_management_w.setLayout(box)

        box = QVBoxLayout(self)
        box.setSpacing(20)
        box.setContentsMargins(10, 20, 10, 10)
        box.addWidget(approving_type)
        box.addWidget(student_exercises_visible)
        box.addWidget(correction_type)
        box.addWidget(comments_visible)
        box.addWidget(class_management_w, alignment=Qt.AlignRight)
        widget = QWidget(self, flags=Qt.Widget)
        widget.setLayout(box)

        widget.setFixedWidth(420)
        return widget

    def get_personal_settings_widget(self):
        font = QFont()
        font.setPixelSize(15)
        label = QLabel(self)
        label.setText('Immagine utente: ')
        label.setFont(font)

        self.current_img = QLabel(self)
        pixmap = QPixmap('img/' + self.data.current_image)
        pixmap = pixmap.scaled(100, 100)
        self.current_img.setPixmap(pixmap)
        self.current_img.setObjectName(self.data.current_image)
        self.current_img.mousePressEvent = self.selection_image_on_click
        self.current_img.setStyleSheet('border: 1px solid grey')

        box = QHBoxLayout(self)
        box.setAlignment(Qt.AlignLeft)
        box.setSpacing(20)
        box.addWidget(label)
        box.addWidget(self.current_img)
        image_widget = QWidget(self, flags=Qt.Widget)
        image_widget.setLayout(box)

        intro_font_dimesion = QLabel('Dimensione del testo: ', self)
        intro_font_dimesion.setFont(font)
        check_15 = QCheckBox("15px")
        check_15.setFont(font)
        if self.data.code_font_size == 15: check_15.setChecked(True)
        check_20 = QCheckBox("20px")
        check_20.setFont(font)
        if self.data.code_font_size == 20: check_20.setChecked(True)
        check_25 = QCheckBox("25px")
        check_25.setFont(font)
        if self.data.code_font_size == 25: check_25.setChecked(True)
        check_30 = QCheckBox("30px")
        check_30.setFont(font)
        if self.data.code_font_size == 30: check_30.setChecked(True)

        self.bg1 = QButtonGroup()
        self.bg1.addButton(check_15, 1)
        self.bg1.addButton(check_20, 2)
        self.bg1.addButton(check_25, 3)
        self.bg1.addButton(check_30, 4)
        self.bg1.buttonClicked[QAbstractButton].connect(self.set_text_dimesion)

        box = QHBoxLayout(self)
        box.addWidget(intro_font_dimesion)
        box.addWidget(check_15)
        box.addWidget(check_20)
        box.addWidget(check_25)
        box.addWidget(check_30)
        font_dimesion = QWidget(self, flags=Qt.Widget)
        font_dimesion.setLayout(box)

        intro_code_orientation = QLabel('Disposizione codice e risultati: ', self)
        intro_code_orientation.setFont(font)
        check_h = QCheckBox("Orizzontale")
        check_h.setFont(font)
        check_h.setChecked(self.data.code_result_horizontal_orientation)
        check_v = QCheckBox("Verticale")
        check_v.setFont(font)
        check_v.setChecked(not self.data.code_result_horizontal_orientation)

        self.bg2 = QButtonGroup()
        self.bg2.addButton(check_h, 1)
        self.bg2.addButton(check_v, 2)
        self.bg2.buttonClicked[QAbstractButton].connect(self.set_code_result_orientation)

        box = QHBoxLayout(self)
        box.addWidget(intro_code_orientation)
        box.addWidget(check_h)
        box.addWidget(check_v)
        code_result_orientation = QWidget(self, flags=Qt.Widget)
        code_result_orientation.setLayout(box)

        intro_visible = QLabel("Modalità riservata: ", self)
        intro_visible.setFont(font)
        check_1 = QCheckBox("Si")
        check_1.setFont(font)
        check_1.setChecked(not self.data.visible)
        check_2 = QCheckBox("No")
        check_2.setFont(font)
        check_2.setChecked(self.data.visible)

        self.bg3 = QButtonGroup()
        self.bg3.addButton(check_1, 1)
        self.bg3.addButton(check_2, 2)
        self.bg3.buttonClicked[QAbstractButton].connect(self.set_visible)

        box = QHBoxLayout(self)
        box.setAlignment(Qt.AlignLeft)
        box.setSpacing(15)
        box.setContentsMargins(0, 0, 0, 0)
        box.addWidget(intro_visible)
        box.addWidget(check_1)
        box.addWidget(check_2)
        visible = QWidget(self, flags=Qt.Widget)
        visible.setLayout(box)

        font.setPixelSize(13)
        intro_visible = QLabel("I tuoi compiti e progressi non saranno visibili dagli studenti", self)
        intro_visible.setFont(font)
        intro_visible.setWordWrap(True)
        font.setPixelSize(15)

        box = QVBoxLayout(self)
        box.setSpacing(0)
        box.addWidget(visible)
        box.addWidget(intro_visible)
        visible = QWidget(self, flags=Qt.Widget)
        visible.setLayout(box)

        pixmap = QPixmap('img/logout.png')
        pixmap = pixmap.scaled(50, 50)
        logout = QLabel(self)
        logout.setPixmap(pixmap)
        logout.setObjectName('img/logout.png')
        logout.mousePressEvent = self.log_out_on_click
        if self.exercise_window is not None:
            logout.hide()

        box = QHBoxLayout(self)
        box. setContentsMargins(20, 90, 20, 0)
        if self.data.my_name in self.data.my_proff:
            advanced_settings_button = QPushButton('Impostazioni\navanzate', self)
            advanced_settings_button.clicked.connect(self.advanced_settings_button_on_click)
            advanced_settings_button.setFixedHeight(55)
            advanced_settings_button.setFont(font)
            box.addWidget(advanced_settings_button)
        box.addWidget(logout, alignment=Qt.AlignRight)
        logout = QWidget(self, flags=Qt.Widget)
        logout.setLayout(box)

        box = QVBoxLayout(self)
        box.setSpacing(20)
        box.addWidget(image_widget)
        box.addWidget(code_result_orientation)
        box.addWidget(font_dimesion)
        box.addWidget(visible)
        box.addWidget(logout)
        widget = QWidget(self, flags=Qt.Widget)
        widget.setLayout(box)
        return widget

    def get_exercise_settings_widget(self):
        box = QVBoxLayout(self)
        box.setContentsMargins(0, 0, 0, 0)
        box.setSpacing(0)
        for i in self.lib.keys():
            box.addWidget(self.color_selector(i, self.lib[i]))
        for i in self.color_styles.keyWords:
            box.addWidget(self.color_selector_key_word(i.word, i.color, i.bold))
        widget = QWidget(self, flags=Qt.Widget)
        widget.setLayout(box)

        font = QFont()
        font.setPixelSize(15)
        button1 = QPushButton('Ritorna alle impostazioni preferite', self)
        button1.clicked.connect(self.set_style_preferred)
        button1.setFont(font)

        button2 = QPushButton('Ritorna alle impostazioni di default', self)
        button2.clicked.connect(self.set_style_default)
        button2.setFont(font)

        button3 = QPushButton('Salva come impostazioni preferite', self)
        button3.clicked.connect(self.set_preferences)
        button3.setFont(font)

        if self.exercise_window is None or self.exercise_window.exercise.id is None:
            button3.hide()
            button1.hide()

        box = QVBoxLayout(self)
        box.addWidget(widget)
        box.addWidget(button1)
        box.addWidget(button2)
        box.addWidget(button3)
        widget = QWidget(self, flags=Qt.Widget)
        widget.setLayout(box)
        return widget

    def color_selector(self, text, color):
        font = QFont()
        font.setPixelSize(15)
        label = QLabel(self)
        label.setText(text)
        label.setFont(font)

        button = QPushButton('', self)
        button.clicked.connect(partial(self.show_selection_color_widget, text, button))
        button.setStyleSheet('background-color: ' + color)
        button.setFixedSize(50, 30)

        self.color_buttons[text] = button

        space=QWidget(self, flags=Qt.Widget)
        space.setFixedWidth(100)

        box = QHBoxLayout(self)
        box.addWidget(label)
        box.addWidget(button)
        box.addWidget(space)
        widget = QWidget(self, flags=Qt.Widget)
        widget.setLayout(box)
        return widget

    def color_selector_key_word(self, word, color, bold):
        font = QFont()
        font.setPixelSize(15)
        label = QLabel(self)
        label.setText('Colore della funzione <b>' + word + '</b>')
        label.setTextFormat(Qt.RichText)
        label.setFont(font)

        button = QPushButton('', self)
        button.clicked.connect(partial(self.show_selection_color_widget, 'Colore della funzione ' + word, button))
        button.setStyleSheet('background-color: ' + color)
        button.setFixedSize(50, 30)

        self.color_keys[word] = button

        check = QCheckBox("Grassetto")
        check.setChecked(bold)
        check.stateChanged.connect(partial(self.set_bold, word, check))
        check.setFixedWidth(100)
        check.setFont(font)

        self.check_keys[word] = check

        box = QHBoxLayout(self)
        box.addWidget(label)
        box.addWidget(button)
        box.addWidget(check)
        widget = QWidget(self, flags=Qt.Widget)
        widget.setLayout(box)
        return widget

    def get_selection_color_widget(self):
        font = QFont()
        font.setPixelSize(15)
        self.selection_color_title = QLabel(self)
        self.selection_color_title.setText('colori:')
        self.selection_color_title.setFont(font)
        self.selection_color_title.setContentsMargins(15, 0, 15, 0)

        box = QHBoxLayout(self)
        box.setContentsMargins(0,0,0,0)

        for i in self.data.owned_colors:
            button = QPushButton('', self)
            button.clicked.connect(partial(self.set_lib_element, i))
            button.setStyleSheet('background-color: ' + i)
            button.setFixedSize(70, 70)
            box.addWidget(button)

        widget = QWidget(self, flags=Qt.Widget)
        widget.setLayout(box)

        box = QVBoxLayout(self)
        box.setContentsMargins(20,15,20,20)
        box.setSpacing(20)
        box.addWidget(self.selection_color_title)
        box.addWidget(widget)
        widget = QWidget(self, flags=Qt.Widget)
        widget.setLayout(box)
        widget.hide()
        widget.setStyleSheet('background-color: #c9c9c9')

        return widget

    def get_selection_image_widget(self):
        font = QFont()
        font.setPixelSize(15)
        selection_image_title = QLabel(self)
        selection_image_title.setText("Seleziona l'immagine che preferisci:")
        selection_image_title.setFont(font)
        selection_image_title.setContentsMargins(20,0,0,0)

        box = QHBoxLayout(self)
        box.setSpacing(20)
        box.setContentsMargins(20, 0, 20, 0)

        for i in self.data.owned_images:
            label = QLabel(self)
            pixmap = QPixmap('img/' + i)
            pixmap = pixmap.scaled(100, 100)
            label.setPixmap(pixmap)
            label.setObjectName(i)
            label.mousePressEvent = partial(self.image_on_click, i, label)
            label.setStyleSheet('border: 1px solid grey')
            if self.data.current_image == i:
                label.setStyleSheet('border: 3px solid #5555ee')
                self.current_image_label = label
            box.addWidget(label, alignment=Qt.AlignCenter)

        widget = QWidget(self, flags=Qt.Widget)
        widget.setLayout(box)
        scroll = QScrollArea(self)
        scroll.setWidget(widget)
        scroll.setStyleSheet('border: 0px solid grey')

        box = QVBoxLayout(self)
        box.setContentsMargins(0, 20, 0, 0)
        box.setSpacing(20)
        box.addWidget(selection_image_title)
        box.addWidget(scroll)
        widget = QWidget(self, flags=Qt.Widget)
        widget.setLayout(box)
        widget.hide()
        widget.setStyleSheet('background-color: #c9c9c9')
        widget.setFixedHeight(200)

        return widget

    def set_lib_element(self, color):
        if self.current_key in self.lib.keys():
            self.lib[self.current_key] = color

            self.color_styles.code_background_color = self.lib['Colore sfondo (codice): ']
            self.color_styles.code_text_color = self.lib['Colore testo (codice): ']
            self.color_styles.results_background_color = self.lib['Colore sfondo (risultati): ']
            self.color_styles.results_text_color = self.lib['Colore testo (risultati): ']
            self.color_styles.error_results_background_color = self.lib['Colore sfondo (risultati sbagliati): ']
            self.color_styles.error_results_text_color = self.lib['Colore testo (risultati sbagliati): ']
            self.color_styles.string_color = self.lib['Colore stringhe: ']
            self.color_styles.comment_color = self.lib['Colore commenti (# linea unica): ']
            self.color_styles.multi_line_comment_color = self.lib["Colore commenti (''' più linee): "]

        else:
            for i in self.color_styles.keyWords:
                if i.word == self.current_key[22:len(self.current_key)]:
                    i.color = color

        self.current_button.setStyleSheet('background-color: ' + color)

        if self.exercise_window is None:
            self.data.color_styles = self.color_styles.__copy__()
            self.data.write_file_color_styles('favorite_style.txt', self.data.color_styles)
        elif self.exercise_window.exercise.id is None:
            self.data.color_styles = self.color_styles.__copy__()
            self.data.write_file_color_styles('favorite_style.txt', self.data.color_styles)
            self.exercise_window.set_color_styles(self.color_styles)
        else:
            self.exercise_window.set_color_styles(self.color_styles)
            self.data.write_file_color_styles('styles/' + self.exercise_window.exercise.id + '.txt', self.color_styles)

    def set_bold(self, word, check):
        for i in self.color_styles.keyWords:
            if i.word == word:
                i.bold = check.isChecked()

        if self.exercise_window is None:
            self.data.color_styles = self.color_styles.__copy__()
            self.data.write_file_color_styles('favorite_style.txt', self.data.color_styles)
        elif self.exercise_window.exercise.id is None:
            self.data.color_styles = self.color_styles.__copy__()
            self.data.write_file_color_styles('favorite_style.txt', self.data.color_styles)
            self.exercise_window.set_color_styles(self.color_styles)
        else:
            self.exercise_window.set_color_styles(self.color_styles)
            self.data.write_file_color_styles('styles/' + self.exercise_window.exercise.id + '.txt', self.color_styles)

    def set_text_dimesion(self, btn):
        self.data.code_font_size = int(btn.text()[0:-2])
        text = self.data.my_name + "\n"
        text += self.data.my_psw + "\n"
        text += self.data.my_class + "\n"
        text += str(self.data.code_result_horizontal_orientation) + "\n"
        text += str(self.data.code_font_size)
        f = open('user_info.txt', "w")
        f.write(text)
        f.close()
        if self.exercise_window is not None:
            self.exercise_window.set_text_font_size(int(btn.text()[0:-2]))

    def set_code_result_orientation(self, btn):
        self.data.code_result_horizontal_orientation = True if btn.text() == 'Orizzontale' else False
        text = self.data.my_name + "\n"
        text += self.data.my_psw + "\n"
        text += self.data.my_class + "\n"
        text += str(self.data.code_result_horizontal_orientation) + "\n"
        text += str(self.data.code_font_size)
        f = open('user_info.txt', "w")
        f.write(text)
        f.close()
        if self.exercise_window is not None:
            self.exercise_window.update_text_result_orientation()

    def set_visible(self, btn):
        try:
            visible = 1 if btn.text() == "No" else 0
            r = requests.post("http://programmingisagame.netsons.org/set_user_visible.php",
                              data={'username': self.data.my_name, 'password': self.data.my_psw, 'visible': visible})
            if r.text != "":
                self.data.visible = True if btn.text() == "No" else False
                if self.exercise_window is not None and self.exercise_window.exercise.id is not None:
                    self.exercise_window.watch_button.setEnabled(self.data.visible
                                                                 or self.data.my_name in self.data.my_proff)
        except requests.exceptions.RequestException as e:
            confirm = ConfirmWindow('Errore di connessione',
                                    "<span style=\" color: red;\"> Attenzione, si sono verificati problemi di "
                                    "connessione<br>Controllare la connessione internet e riprovare</span>",
                                    ok="Ok", cancel=None)
            if confirm.exec_() == QDialog.Accepted:
                print('ok')
            confirm.deleteLater()

    def set_correction_type(self, btn):
        try:
            mode = 1 if btn.text() == "Il creatore dell'esercizio" else (2 if btn.text() == "Il docente" else 0)
            r = requests.post("http://programmingisagame.netsons.org/set_correction_type.php",
                              data={'username': self.data.my_name, 'password': self.data.my_psw,
                                    'class': self.data.my_class, 'mode': mode})
            if r.text != "":
                self.data.correction_type = mode
        except requests.exceptions.RequestException as e:
            confirm = ConfirmWindow('Errore di connessione',
                                    "<span style=\" color: red;\"> Attenzione, si sono verificati problemi di "
                                    "connessione<br>Controllare la connessione internet e riprovare</span>",
                                    ok="Ok", cancel=None)
            if confirm.exec_() == QDialog.Accepted:
                print('ok')
            confirm.deleteLater()

    def set_approving_type(self, btn):
        try:
            mode = 0 if btn.text() == "Automatica" else 1
            r = requests.post("http://programmingisagame.netsons.org/set_approving_type.php",
                              data={'username': self.data.my_name, 'password': self.data.my_psw,
                                    'class': self.data.my_class, 'mode': mode})
            if r.text != "":
                self.data.approving_type = mode
        except requests.exceptions.RequestException as e:
            confirm = ConfirmWindow('Errore di connessione',
                                    "<span style=\" color: red;\"> Attenzione, si sono verificati problemi di "
                                    "connessione<br>Controllare la connessione internet e riprovare</span>",
                                    ok="Ok", cancel=None)
            if confirm.exec_() == QDialog.Accepted:
                print('ok')
            confirm.deleteLater()

    def set_student_exercises_visible(self, btn):
        try:
            visible = 1 if btn.text() == "Visibili" else 0
            r = requests.post("http://programmingisagame.netsons.org/set_student_exercises_visible.php",
                              data={'username': self.data.my_name, 'password': self.data.my_psw,
                                    'class': self.data.my_class, 'visible': visible})
            if r.text != "":
                self.data.student_exercises_visible = True if btn.text() == "Visibili" else False
        except requests.exceptions.RequestException as e:
            confirm = ConfirmWindow('Errore di connessione',
                                    "<span style=\" color: red;\"> Attenzione, si sono verificati problemi di "
                                    "connessione<br>Controllare la connessione internet e riprovare</span>",
                                    ok="Ok", cancel=None)
            if confirm.exec_() == QDialog.Accepted:
                print('ok')
            confirm.deleteLater()

    def set_comments_visible(self, btn):
        try:
            visible = 1 if btn.text() == "Abilitati" else 0
            r = requests.post("http://programmingisagame.netsons.org/set_comments_visible.php",
                              data={'username': self.data.my_name, 'password': self.data.my_psw,
                                    'class': self.data.my_class, 'visible': visible})
            if r.text != "":
                self.data.comments_visible = btn.text() == "Abilitati"
        except requests.exceptions.RequestException as e:
            confirm = ConfirmWindow('Errore di connessione',
                                    "<span style=\" color: red;\"> Attenzione, si sono verificati problemi di "
                                    "connessione<br>Controllare la connessione internet e riprovare</span>",
                                    ok="Ok", cancel=None)
            if confirm.exec_() == QDialog.Accepted:
                print('ok')
            confirm.deleteLater()

    def selection_image_on_click(self, event):
        if self.selection_image_widget.isVisible():
            self.selection_image_widget.hide()
        else:
            self.selection_image_widget.show()

    def log_out_on_click(self, event):
        text = "\n\n" + self.data.my_class + "\n" + str(self.data.code_result_horizontal_orientation) + "\n" \
               + str(self.data.code_font_size)
        f = open('user_info.txt', "w")
        f.write(text)
        f.close()

        self.close()
        self.parent.open_LoginWindow()

    def image_on_click(self, name, label, event):
        try:
            r = requests.post("http://programmingisagame.netsons.org/select_user_image.php",
                              data={'username': self.data.my_name, 'password': self.data.my_psw, 'img': name})
            if r.text != "":
                pixmap = QPixmap('img/' + name)
                pixmap = pixmap.scaled(100,100)
                self.current_img.setPixmap(pixmap)
                self.data.current_image = name
                if self.exercise_window is None:
                    self.parent.set_image(name)
                label.setStyleSheet('border: 3px solid #5555ee')
                self.current_image_label.setStyleSheet('border: 0px solid #000000')
                self.current_image_label = label
        except requests.exceptions.RequestException as e:
            confirm = ConfirmWindow('Errore di connessione',
                                    "<span style=\" color: red;\"> Attenzione, si sono verificati problemi di "
                                    "connessione<br>Controllare la propria connessione internet e riprovare</span>",
                                    ok="Ok", cancel=None)
            if confirm.exec_() == QDialog.Accepted:
                print('ok')
            confirm.deleteLater()

    def set_preferences(self):
        self.data.color_styles = self.color_styles.__copy__()
        self.data.write_file_color_styles('favorite_style.txt', self.data.color_styles)

    def set_style_preferred(self):
        self.color_styles = self.data.color_styles.__copy__()
        self.color_style_changed(None)

    def set_style_default(self):
        self.color_styles = DefaultColorStyles()
        self.color_style_changed(self.color_styles)

    def color_style_changed(self, cs):
        self.color_buttons['Colore sfondo (codice): ']\
            .setStyleSheet('background-color: ' + self.color_styles.code_background_color)
        self.color_buttons['Colore sfondo (risultati): ']\
            .setStyleSheet('background-color: ' + self.color_styles.results_background_color)
        self.color_buttons['Colore sfondo (risultati sbagliati): ']\
            .setStyleSheet('background-color: ' + self.color_styles.error_results_background_color)
        self.color_buttons['Colore testo (codice): ']\
            .setStyleSheet('background-color: ' + self.color_styles.code_text_color)
        self.color_buttons['Colore testo (risultati): ']\
            .setStyleSheet('background-color: ' + self.color_styles.results_text_color)
        self.color_buttons['Colore testo (risultati sbagliati): ']\
            .setStyleSheet('background-color: ' + self.color_styles.error_results_text_color)
        self.color_buttons['Colore commenti (# linea unica): ']\
            .setStyleSheet('background-color: ' + self.color_styles.comment_color)
        self.color_buttons["Colore commenti (''' più linee): "]\
            .setStyleSheet('background-color: ' + self.color_styles.multi_line_comment_color)
        self.color_buttons['Colore stringhe: ']\
            .setStyleSheet('background-color: ' + self.color_styles.string_color)

        for i in self.color_styles.keyWords:
            self.color_keys[i.word].setStyleSheet('background-color: ' + i.color)
            self.check_keys[i.word].setChecked(i.bold)

        if self.exercise_window is None:
            self.data.color_styles = self.color_styles.__copy__()
            self.data.write_file_color_styles('favorite_style.txt', self.data.color_styles)
        elif self.exercise_window.exercise.id is None:
            self.data.color_styles = self.color_styles.__copy__()
            self.data.write_file_color_styles('favorite_style.txt', self.data.color_styles)
            self.exercise_window.set_color_styles(cs)
        else:
            self.exercise_window.set_color_styles(cs)
            self.data.write_file_color_styles('styles/' + self.exercise_window.exercise.id + '.txt', self.color_styles)

    def make_user_wait_widget(self, username, name, surname, student_type, approved):
        font = QFont()
        font.setPixelSize(15)
        w1 = QLabel(('Studente "' if student_type else 'Docente "') + username + '"', self)
        w2 = QLabel("Nome: " + name + " " + surname, self)
        w1.setFont(font)
        w2.setFont(font)

        box = QVBoxLayout(self)
        box.addWidget(w1)
        box.addWidget(w2)
        user = QWidget(self, flags=Qt.Widget)
        user.setLayout(box)

        remove = QPushButton('Rimuovi', self)
        remove.setFont(font)
        w5 = QPushButton('Accetta', self)
        w6 = QPushButton('Rifiuta', self)
        w5.setFont(font)
        w6.setFont(font)
        box = QVBoxLayout(self)
        box.setContentsMargins(0, 0, 0, 0)
        box.addWidget(w5)
        box.addWidget(w6)
        accept_w = QWidget(self, flags=Qt.Widget)
        accept_w.setLayout(box)

        box = QHBoxLayout(self)
        box.setContentsMargins(0, 0, 0, 0)
        box.setSpacing(0)
        box.addWidget(remove)
        box.addWidget(accept_w)
        accept = QWidget(self, flags=Qt.Widget)
        accept.setLayout(box)

        if username == self.data.my_name:
            remove.hide()
        if approved:
            accept_w.hide()
        else:
            remove.hide()
        accept.setFixedWidth(100)

        box = QHBoxLayout(self)
        box.setContentsMargins(10, 20, 10, 10)
        box.addWidget(user)
        box.addWidget(accept)
        widget = QWidget(self, flags=Qt.Widget)
        widget.setLayout(box)
        widget.setObjectName("widget")
        widget.setStyleSheet("QWidget#widget {border: 0px solid grey; border-top: 1px solid grey}")

        w5.clicked.connect(partial(self.accept_user, True, remove, accept_w, username))
        w6.clicked.connect(partial(self.accept_user, False, remove, widget, username))
        remove.clicked.connect(partial(self.remove_user, widget, username))
        return widget

    def accept_user(self, accepted, w1, widget, username):
        try:
            r = requests.post("http://programmingisagame.netsons.org/solve_request_signin.php",
                              data={'username': self.data.my_name, 'password': self.data.my_psw,
                                    'class': self.data.my_class, 'user': username, 'type': 1 if accepted else 2})
            if r.text == "ok":
                if accepted:
                    w1.show()
                widget.hide()
        except requests.exceptions.RequestException as e:
            confirm = ConfirmWindow('Errore di connessione',
                                    "<span style=\" color: red;\"> Attenzione, si sono verificati problemi di "
                                    "connessione<br>Controllare la connessione internet e riprovare</span>",
                                    ok="Ok", cancel=None)
            if confirm.exec_() == QDialog.Accepted:
                print('ok')
            confirm.deleteLater()

    def remove_user(self, widget, username):
        try:
            r = requests.post("http://programmingisagame.netsons.org/remove_user.php",
                              data={'username': self.data.my_name, 'password': self.data.my_psw,
                                    'class': self.data.my_class, 'user': username})
            if r.text == "ok":
                widget.hide()
        except requests.exceptions.RequestException as e:
            confirm = ConfirmWindow('Errore di connessione',
                                    "<span style=\" color: red;\"> Attenzione, si sono verificati problemi di "
                                    "connessione<br>Controllare la connessione internet e riprovare</span>",
                                    ok="Ok", cancel=None)
            if confirm.exec_() == QDialog.Accepted:
                print('ok')
            confirm.deleteLater()
