from functools import partial

from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QFont, QPixmap, QColor
from PyQt5.QtWidgets import QDialog, QPushButton, QWidget, QVBoxLayout, QLabel, QHBoxLayout, QScrollArea, QCheckBox, \
    QButtonGroup, QAbstractButton
from django.dispatch import Signal


class SettingsWindow(QDialog):
    def __init__(self, title, data, exercise_window, parent=None):
        QDialog.__init__(self, parent)
        self.setWindowTitle(title)
        self.setMinimumSize(QSize(450, 600))
        self.exercise_window = exercise_window
        self.data = data
        self.current_button = None
        self.current_key = None
        self.color_styles = \
            data.color_styles.__copy__() if exercise_window is None or exercise_window.exercise.color_styles is None \
                else exercise_window.exercise.color_styles
        self.lib = {
            'Colore sfondo (codice): ': self.color_styles.code_background_color,
            'Colore sfondo (risultati): ': self.color_styles.results_background_color,
            'Colore sfondo (risultati sbagliati): ': self.color_styles.error_results_background_color,
            'Colore texto (codice): ': self.color_styles.code_text_color,
            'Colore texto (risultati): ': self.color_styles.results_text_color,
            'Colore texto (risultati sbagliati): ': self.color_styles.error_results_text_color,
            'Colore commenti (# linea unica): ': self.color_styles.comment_color,
            "Colore commenti (''' più linee): ": self.color_styles.multi_line_comment_color,
            'Colore stringhe: ': self.color_styles.string_color

        }

        font = QFont()
        font.setPixelSize(15)
        self.personal_settings_button = QPushButton('Impostazioni personali', self)
        self.personal_settings_button.clicked.connect(self.personal_settings_button_on_click)
        self.personal_settings_button.setFixedHeight(50)
        self.personal_settings_button.setFont(font)

        self.exercise_settings_button = QPushButton("Impostazioni dell'esercizio", self)
        self.exercise_settings_button.clicked.connect(self.exercise_settings_button_on_click)
        self.exercise_settings_button.setFixedHeight(50)
        self.exercise_settings_button.setFont(font)

        self.personal_settings_widget = QScrollArea(self)
        self.personal_settings_widget.setWidget(self.get_personal_settings_widget())
        self.exercise_settings_widget = QScrollArea(self)
        self.exercise_settings_widget.setWidget(self.get_exercise_settings_widget())

        self.selection_color_widget = self.get_selection_color_widget()
        self.selection_image_widget = self.get_selection_image_widget()

        box = QHBoxLayout(self)
        box.setContentsMargins(0, 0, 0, 0)
        box.setSpacing(0)
        box.addWidget(self.personal_settings_button, alignment=Qt.AlignTop)
        box.addWidget(self.exercise_settings_button)
        widget = QWidget(self, flags=Qt.Widget)
        widget.setLayout(box)

        box = QVBoxLayout(self)
        box.setContentsMargins(0, 0, 0, 0)
        box.setSpacing(0)
        box.addWidget(widget)
        box.addWidget(self.personal_settings_widget)
        box.addWidget(self.exercise_settings_widget)
        box.addWidget(self.selection_color_widget)
        box.addWidget(self.selection_image_widget)

        if exercise_window is None:
            self.personal_settings_button_on_click()
        else:
            self.exercise_settings_button_on_click()

    def personal_settings_button_on_click(self):
        self.personal_settings_widget.show()
        self.exercise_settings_widget.hide()
        self.selection_color_widget.hide()
        self.selection_image_widget.hide()
        self.personal_settings_button.setStyleSheet('background-color: grey')
        self.exercise_settings_button.setStyleSheet('background-color: #c9c9c9')

    def exercise_settings_button_on_click(self):
        self.personal_settings_widget.hide()
        self.exercise_settings_widget.show()
        self.selection_color_widget.hide()
        self.selection_image_widget.hide()
        self.personal_settings_button.setStyleSheet('background-color: #c9c9c9')
        self.exercise_settings_button.setStyleSheet('background-color: grey')

    def show_selection_color_widget(self, text, button):
        if self.current_button == button and self.selection_color_widget.isVisible():
            self.selection_color_widget.hide()
        else:
            self.current_key = text
            self.current_button = button
            self.selection_color_title.setText(text)
            self.selection_color_widget.show()

    def get_personal_settings_widget(self):
        font = QFont()
        font.setPixelSize(13)
        label = QLabel(self)
        label.setText('Immagine utente: ')
        label.setFont(font)

        self.current_img = QLabel(self)
        pixmap = QPixmap(self.data.current_image)
        pixmap = pixmap.scaled(100, 100)
        self.current_img.setPixmap(pixmap)
        self.current_img.setObjectName(self.data.current_image)
        self.current_img.mousePressEvent = self.selection_image_on_click

        box = QHBoxLayout(self)
        box.addWidget(label)
        box.addWidget(self.current_img)
        image_widget = QWidget(self, flags=Qt.Widget)
        image_widget.setLayout(box)


        intro_font_dimesion = QLabel(self)
        intro_font_dimesion.setText('Dimensione del testo: ')
        check_15 = QCheckBox("15px")
        if self.data.code_font_size == 15: check_15.setChecked(True)
        check_20 = QCheckBox("20px")
        if self.data.code_font_size == 20: check_20.setChecked(True)
        check_25 = QCheckBox("25px")
        if self.data.code_font_size == 25: check_25.setChecked(True)
        check_30 = QCheckBox("30px")
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

        intro_code_orientation = QLabel(self)
        intro_code_orientation.setText('Disposizione codice e risultati: ')
        check_h = QCheckBox("Orizzontale")
        check_h.setChecked(self.data.code_result_horizontal_orientation)
        check_v = QCheckBox("Vericale")
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

        box = QVBoxLayout(self)
        box.setSpacing(0)
        box.addWidget(image_widget)
        box.addWidget(code_result_orientation)
        box.addWidget(font_dimesion)
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

        button = QPushButton('Salva come impostazioni preferite', self)
        button.clicked.connect(self.set_preferences)

        box = QVBoxLayout(self)
        box.addWidget(widget)
        box.addWidget(button)
        widget = QWidget(self, flags=Qt.Widget)
        widget.setLayout(box)
        return widget

    def color_selector(self, text, color):
        font = QFont()
        font.setPixelSize(13)
        label = QLabel(self)
        label.setText(text)
        label.setFont(font)

        button = QPushButton('', self)
        button.clicked.connect(partial(self.show_selection_color_widget, text, button))
        button.setStyleSheet('background-color: ' + color)
        button.setFixedSize(50, 30)

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
        font.setPixelSize(13)
        label = QLabel(self)
        label.setText('Colore della funzione <b>' + word + '</b>')
        label.setTextFormat(Qt.RichText)
        label.setFont(font)

        button = QPushButton('', self)
        button.clicked.connect(partial(self.show_selection_color_widget, 'Colore della funzione ' + word, button))
        button.setStyleSheet('background-color: ' + color)
        button.setFixedSize(50, 30)

        check = QCheckBox("Grassetto")
        check.setChecked(bold)
        check.stateChanged.connect(partial(self.set_bold, word, check))
        check.setFixedWidth(100)

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

        box = QHBoxLayout(self)
        box.setContentsMargins(0,0,0,0)

        for i in self.data.owned_colors:
            button = QPushButton('', self)
            button.clicked.connect(partial(self.set_lib_element, i))
            button.setStyleSheet('background-color: ' + i)
            button.setFixedSize(50, 50)
            box.addWidget(button)

        widget = QWidget(self, flags=Qt.Widget)
        widget.setLayout(box)

        box = QVBoxLayout(self)
        box.setContentsMargins(20,20,20,20)
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
        selection_image_title.setText('Immagini:')
        selection_image_title.setFont(font)
        selection_image_title.setContentsMargins(20,0,0,0)

        box = QHBoxLayout(self)
        box.setSpacing(20)
        box.setContentsMargins(20,0,20,0)

        for i in self.data.owned_images:
            label = QLabel(self)
            pixmap = QPixmap(i)
            pixmap = pixmap.scaled(100,100)
            label.setPixmap(pixmap)
            label.setObjectName(i)
            label.mousePressEvent = partial(self.image_on_click, i)
            box.addWidget(label)

        widget = QWidget(self, flags=Qt.Widget)
        widget.setLayout(box)
        scroll = QScrollArea(self)
        scroll.setWidget(widget)
        scroll.setStyleSheet('border: 0px solid grey')

        box = QVBoxLayout(self)
        box.setContentsMargins(0,20,0,0)
        box.setSpacing(20)
        box.addWidget(selection_image_title)
        box.addWidget(scroll)
        widget = QWidget(self, flags=Qt.Widget)
        widget.setLayout(box)
        widget.hide()
        widget.setStyleSheet('background-color: #c9c9c9')
        widget.setFixedHeight(190)

        return widget

    def set_lib_element(self, color):
        if self.current_key in self.lib.keys():
            self.lib[self.current_key] = color

            self.color_styles.code_background_color = self.lib['Colore sfondo (codice): ']
            self.color_styles.code_text_color = self.lib['Colore texto (codice): ']
            self.color_styles.results_background_color = self.lib['Colore sfondo (risultati): ']
            self.color_styles.results_text_color = self.lib['Colore texto (risultati): ']
            self.color_styles.error_results_background_color = self.lib['Colore sfondo (risultati sbagliati): ']
            self.color_styles.error_results_text_color = self.lib['Colore texto (risultati sbagliati): ']
            self.color_styles.string_color = self.lib['Colore stringhe: ']
            self.color_styles.comment_color = self.lib['Colore commenti (# linea unica): ']
            self.color_styles.multi_line_comment_color = self.lib["Colore commenti (''' più linee): "]

        else:
            for i in self.color_styles.keyWords:
                if i.word == self.current_key[22:len(self.current_key)]:
                    i.color = color

        self.current_button.setStyleSheet('background-color: ' + color)

        self.exercise_window.set_color_styles(self.color_styles)

    def set_bold(self, word, check):
        for i in self.color_styles.keyWords:
            if i.word == word:
                i.bold = check.isChecked()

        self.exercise_window.set_color_styles(self.color_styles)

    def set_text_dimesion(self, btn):
        self.data.code_font_size = int(btn.text()[0:-2])
        self.exercise_window.set_text_font_size(int(btn.text()[0:-2]))

    def set_code_result_orientation(self, btn):
        self.data.code_result_horizontal_orientation = True if btn.text() == 'Orizzontale' else False
        self.exercise_window.update_text_result_orientation()

    def selection_image_on_click(self, event):
        if self.selection_image_widget.isVisible():
            self.selection_image_widget.hide()
        else:
            self.selection_image_widget.show()

    def image_on_click(self, name, event):
        pixmap = QPixmap(name)
        pixmap = pixmap.scaled(100,100)
        self.current_img.setPixmap(pixmap)
        self.data.current_image = name

    def set_preferences(self):
        self.data.color_styles = self.color_styles
