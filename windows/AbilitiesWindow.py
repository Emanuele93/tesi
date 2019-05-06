from functools import partial
from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtWidgets import QWidget, QPushButton, QHBoxLayout, QVBoxLayout, QLabel, QDialog, QLineEdit
from PyQt5.QtCore import *
import Server_call_master


class AbilitiesWindow(QWidget):
    def __init__(self, home, data, page=1):
        super(AbilitiesWindow, self).__init__(home, flags=Qt.Widget)
        home.setWindowTitle("Negozio")
        self.data = data
        self.home = home
        self.buttons = {}
        self.color_buttons = []
        self.color_label = {}
        self.color_change_buttons = []
        self.current_image = None
        self.images_buttons = {}

        font = QFont()
        font.setPixelSize(15)

        home_button = QPushButton('HOME', self)
        home_button.setFixedSize(115, 50)
        home_button.clicked.connect(self.home.open_MainWindow)
        home_button.setFont(font)
        home_button.setStyleSheet("background-color: #ffdd55")

        button1 = QPushButton('CONTATORI', self)
        button1.setFixedSize(115, 50)
        button1.setFont(font)
        button2 = QPushButton('COLORI', self)
        button2.setFixedSize(115, 50)
        button2.setFont(font)
        button3 = QPushButton('SKIN', self)
        button3.setFixedSize(115, 50)
        button3.setFont(font)
        button4 = QPushButton('GETTONI', self)
        button4.setFixedSize(115, 50)
        button4.setFont(font)

        page1 = self.make_page1()
        page2 = self.make_page2()
        page3 = self.make_page3()
        page4 = self.make_page4()

        font_log = QFont()
        font_log.setPixelSize(17)
        self.logLine = QLabel(self)
        self.logLine.setFont(font_log)

        button1.clicked.connect(
            partial(self.open_subpage, button1, page1, button2, page2, button3, page3, button4, page4,
                    "Aumenta i tuoi contatori per riuscire a completare ogni esercizio"))
        button2.clicked.connect(
            partial(self.open_subpage, button2, page2, button1, page1, button3, page3, button4, page4,
                    "Acquista nuovi colori per personalizzare il tuo codice"))
        button3.clicked.connect(
            partial(self.open_subpage, button3, page3, button2, page2, button1, page1, button4, page4,
                    "Cambia la tua immagine profilo"))
        button4.clicked.connect(
            partial(self.open_subpage, button4, page4, button2, page2, button3, page3, button1, page1,
                    "Compra un gettone per ampliare le tue possibilità"))

        if page == 1:
            self.open_subpage(button1, page1, button2, page2, button3, page3, button4, page4,
                              "Aumenta i tuoi contatori per riuscire a completare ogni esercizio")
        elif page == 2:
            self.open_subpage(button2, page2, button1, page1, button3, page3, button4, page4,
                              "Acquista nuovi colori per personalizzare il tuo codice")
        elif page == 3:
            self.open_subpage(button3, page3, button1, page1, button2, page2, button4, page4,
                              "Cambia la tua immagine profilo")
        elif page == 4:
            self.open_subpage(button4, page4, button1, page1, button2, page2, button3, page3,
                              "Compra un gettone per ampliare le tue possibilità")

        l = 1
        old = 0
        for i in self.data.level_progression:
            if self.data.level >= i:
                l += 1
                old = i

        level_number = QLabel('Liv. ' + str(l), self)
        level_number.setFont(font)
        level_number.setStyleSheet('background-color: #9999FF; border: 1px solid grey')
        level_number.setFixedSize(90, 40)
        level_number.setContentsMargins(20, 10, 20, 10)

        level_bar = QLabel(self)
        level_bar.setStyleSheet('background-color: #4040FF')
        level_bar.setFixedSize(int(90*(self.data.level-old)/(self.data.level_progression[l-1]-old)), 5)

        box = QVBoxLayout(self)
        box.setSpacing(0)
        box.setContentsMargins(0, 0, 0, 0)
        box.addWidget(level_number)
        box.addWidget(level_bar)
        level = QWidget(self, flags=Qt.Widget)
        level.setLayout(box)
        level.setObjectName("level")
        level.setStyleSheet("QWidget#level {border: 1px solid grey; background-color: #BBBBFF}")

        self.soldi = QLabel(str(self.data.money) + ' soldi', self)
        self.soldi.setFont(font)
        self.soldi.setStyleSheet("QWidget#soldi {border: 1px solid grey; background-color: #ffea00}")
        self.soldi.setContentsMargins(20, 5, 20, 5)
        self.soldi.setObjectName("soldi")
        self.soldi.setFixedHeight(45)

        box = QHBoxLayout(self)
        box.setAlignment(Qt.AlignCenter)
        box.setSpacing(5)
        box.addWidget(level)
        box.addWidget(self.soldi)
        box.setContentsMargins(0, 0, 0, 0)
        soldi_widget = QWidget(self, flags=Qt.Widget)
        soldi_widget.setLayout(box)

        empty = QWidget(self, flags=Qt.Widget)
        empty.setFixedWidth(20)

        buttons_box = QHBoxLayout(self)
        buttons_box.addWidget(button1)
        buttons_box.addWidget(button2)
        buttons_box.addWidget(button3)
        buttons_box.addWidget(button4)
        buttons_box.setContentsMargins(0, 0, 0, 0)
        buttons_box.setSpacing(0)
        buttons_box.setAlignment(Qt.AlignCenter)
        buttons_widget = QWidget(self, flags=Qt.Widget)
        buttons_widget.setLayout(buttons_box)

        font.setPixelSize(25)
        font.setBold(True)
        title = QLabel("Negozio", self)
        title.setFont(font)
        title.setStyleSheet("color: #ffffff")

        top_box = QHBoxLayout(self)
        top_box.addWidget(home_button)
        top_box.addWidget(title)
        top_box.addWidget(buttons_widget)
        top_box.setContentsMargins(20, 0, 20, 0)
        top_box.setSpacing(40)
        top_widget = QWidget(self, flags=Qt.Widget)
        top_widget.setLayout(top_box)
        top_widget.setFixedHeight(80)
        top_widget.setObjectName("topStyle")
        top_widget.setStyleSheet("QWidget#topStyle {border: 0px solid grey; border-bottom: 1px solid grey; "
                                 "border-top: 1px solid grey; background-color: #47d271}")

        box = QHBoxLayout(self)
        box.addWidget(self.logLine)
        box.addWidget(soldi_widget, alignment=Qt.AlignRight)
        box.setContentsMargins(50, 0, 5, 0)
        bottom_widget = QWidget(self, flags=Qt.Widget)
        bottom_widget.setLayout(box)
        bottom_widget.setObjectName("bw")
        bottom_widget.setStyleSheet("QWidget#bw {border: 0px solid grey; border-bottom: 1px solid grey; "
                                    "background-color: #99cc99}")
        bottom_widget.setFixedHeight(55)

        window_layaut = QVBoxLayout(self)
        window_layaut.setContentsMargins(0, 0, 0, 0)
        window_layaut.addWidget(top_widget)
        window_layaut.addWidget(bottom_widget)
        window_layaut.addWidget(page1)
        window_layaut.addWidget(page2)
        window_layaut.addWidget(page3)
        window_layaut.addWidget(page4)
        window_layaut.setSpacing(0)

    def open_subpage(self, b1, p1, b2, p2, b3, p3, b4, p4, logline):
        p1.setVisible(True)
        p2.setVisible(False)
        p3.setVisible(False)
        p4.setVisible(False)
        b1.setStyleSheet('background-color: #dd9933')
        b2.setStyleSheet('background-color: #ffdd55')
        b3.setStyleSheet('background-color: #ffdd55')
        b4.setStyleSheet('background-color: #ffdd55')
        self.logLine.setText(logline)

    def make_page1(self):
        box = QHBoxLayout(self)
        box.setContentsMargins(0, 0, 0, 0)
        box.addWidget(self.counter_upgrade_widget('Righe di codice correnti'))
        box.setAlignment(Qt.AlignLeft)
        widget_lines = QWidget(self, flags=Qt.Widget)
        widget_lines.setLayout(box)

        box = QHBoxLayout(self)
        box.setContentsMargins(0, 0, 0, 0)
        box.addWidget(self.counter_upgrade_widget('Variabili correnti'))
        box.setAlignment(Qt.AlignLeft)
        widget_variables = QWidget(self, flags=Qt.Widget)
        widget_variables.setLayout(box)

        font = QFont()
        font.setPixelSize(15)

        box = QHBoxLayout(self)
        box.setSpacing(20)
        box.addWidget(self.counter_upgrade_widget('if'))
        box.addWidget(self.counter_upgrade_widget('elif' if self.data.language == 1 else 'else if'))
        box.addWidget(self.counter_upgrade_widget('else'))
        box.setAlignment(Qt.AlignLeft)
        widget_conditions = QWidget(self, flags=Qt.Widget)
        widget_conditions.setLayout(box)

        title = QLabel('Selezioni correnti', self)
        title.setFont(font)
        title.setAlignment(Qt.AlignHCenter)
        title.setStyleSheet("border: 1px solid grey; background-color: #ccccff")
        title.setContentsMargins(5, 3, 5, 3)

        width = widget_conditions.sizeHint().width()

        box = QVBoxLayout(self)
        box.addWidget(title)
        box.addWidget(widget_conditions)
        box.setContentsMargins(0, 0, 0, 0)
        box.setSpacing(0)
        box.setAlignment(Qt.AlignLeft)
        widget_conditions = QWidget(self, flags=Qt.Widget)
        widget_conditions.setLayout(box)
        widget_conditions.setObjectName("widget_cycles")
        widget_conditions.setStyleSheet("QWidget#widget_cycles {border: 1px solid grey; background-color: #aaaaff}")
        widget_conditions.setFixedWidth(width)

        box = QHBoxLayout(self)
        box.setSpacing(20)
        box.addWidget(self.counter_upgrade_widget('for'))
        box.addWidget(self.counter_upgrade_widget('while'))
        box.setAlignment(Qt.AlignLeft)
        widget_cycles = QWidget(self, flags=Qt.Widget)
        widget_cycles.setLayout(box)

        title = QLabel('Cicli correnti', self)
        title.setFont(font)
        title.setAlignment(Qt.AlignHCenter)
        title.setStyleSheet("border: 1px solid grey; background-color: #ccccff")
        title.setContentsMargins(5, 3, 5, 3)

        width = widget_cycles.sizeHint().width()

        box = QVBoxLayout(self)
        box.addWidget(title)
        box.addWidget(widget_cycles)
        box.setContentsMargins(0, 0, 0, 0)
        box.setSpacing(0)
        box.setAlignment(Qt.AlignLeft)
        widget_cycles = QWidget(self, flags=Qt.Widget)
        widget_cycles.setLayout(box)
        widget_cycles.setObjectName("widget_cycles")
        widget_cycles.setStyleSheet("QWidget#widget_cycles {border: 1px solid grey; background-color: #aaaaff}")
        widget_cycles.setFixedWidth(width)

        box = QHBoxLayout(self)
        box.setContentsMargins(0, 0, 0, 0)
        box.addWidget(self.counter_upgrade_widget('Funzioni correnti' + (' (def)' if self.data.language == 1 else '')))
        box.setAlignment(Qt.AlignLeft)
        widget_functions = QWidget(self, flags=Qt.Widget)
        widget_functions.setLayout(box)

        box = QVBoxLayout(self)
        box.setSpacing(12)
        box.setContentsMargins(100, 15, 0, 0)
        box.addWidget(widget_lines)
        box.addWidget(widget_variables)
        box.addWidget(widget_conditions)
        box.addWidget(widget_cycles)
        box.addWidget(widget_functions)
        box.setAlignment(Qt.AlignTop)
        widget = QWidget(self, flags=Qt.Widget)
        widget.setLayout(box)
        return widget

    def counter_upgrade_widget(self, name):
        font = QFont()
        font.setPixelSize(17)

        name_label = QLabel(self)
        name_label.setText(name)
        name_label.setContentsMargins(10, 0, 10, 0)
        name_label.setFont(font)

        if name == 'Righe di codice correnti':
            name = 'lines'
        elif name == 'Variabili correnti':
            name = 'variables'
        elif name == 'Funzioni correnti (def)' or name == 'Funzioni correnti':
            name = 'functions'
        elif name == 'else if':
            name = 'elif'

        lev = self.data.level_variables[name]
        numbers_upgrade = QLabel(self)
        if lev < len(self.data.variables_numbers[name]):
            numbers_upgrade.setText(str(self.data.variables_numbers[name][lev]))
        else:
            numbers_upgrade.setText(' &#8734; ')
        numbers_upgrade.setTextFormat(Qt.RichText)
        numbers_upgrade.setContentsMargins(10, 0, 10, 0)
        numbers_upgrade.setFont(font)

        font.setPixelSize(15)
        upgrade_value = QLabel(self)
        cost = QPushButton(self)
        cost.clicked.connect(partial(self.upgrade_counter, name, cost, numbers_upgrade, upgrade_value))
        cost.setFont(font)
        cost.setStyleSheet('background-color: #ffff55')
        cost.setEnabled(not((name == 'variables' or name == 'functions') and self.data.language != 1))
        self.buttons[name] = cost

        if lev < len(self.data.variables_numbers[name]):
            cost.setText(str(self.data.variables_cost[name][lev]) + ' soldi')
            if self.data.variables_cost[name][lev] > self.data.money:
                cost.setEnabled(False)
        else:
            self.buttons.pop(name)

        lev = self.data.level_variables[name]
        if lev < len(self.data.variables_numbers[name])-1:
            upgrade_value.setText('+ ' + str(self.data.variables_numbers[name][lev + 1] -
                                             self.data.variables_numbers[name][lev]))
        else:
            upgrade_value.setText(' + &#8734; ')
        upgrade_value.setTextFormat(Qt.RichText)
        upgrade_value.setFont(font)

        box = QVBoxLayout(self)
        box.setAlignment(Qt.AlignCenter)
        box.setSpacing(3)
        box.addWidget(upgrade_value, alignment=Qt.AlignHCenter)
        box.addWidget(cost)
        box.setAlignment(Qt.AlignLeft)
        box.setContentsMargins(0, 0, 0, 0)
        cost = QWidget(self, flags=Qt.Widget)
        cost.setLayout(box)

        if lev >= len(self.data.variables_numbers[name]):
            cost.hide()

        box = QHBoxLayout(self)
        box.setAlignment(Qt.AlignLeft)
        box.addWidget(name_label)
        box.addWidget(numbers_upgrade)
        box.addWidget(cost)
        box.setAlignment(Qt.AlignLeft)
        box.setContentsMargins(5, 5, 5, 5)

        widget = QWidget(self, flags=Qt.Widget)
        widget.setLayout(box)
        widget.setObjectName("counter")
        widget.setStyleSheet("QWidget#counter {border: 1px solid grey; background-color: #ccccff}")
        widget.setMinimumHeight(55)
        return widget

    def upgrade_counter(self, name, button, numbers, upgrade_value):
        if Server_call_master.set_variable("/add_level.php?name="+name, {'username': self.data.my_name,
                                                                         'password': self.data.my_psw}):
            lev = self.data.level_variables[name]
            self.data.money -= self.data.variables_cost[name][lev]
            self.soldi.setText(str(self.data.money) + ' soldi')
            self.data.level_variables[name] += 1
            self.data.owned_variables = self.data.get_owned_variables_numbers()
            lev = self.data.level_variables[name]
            if lev < len(self.data.variables_numbers[name]):
                numbers.setText(str(self.data.variables_numbers[name][lev]))
            else:
                numbers.setText(' &#8734; ')

            if lev < len(self.data.variables_numbers[name])-1:
                upgrade_value.setText('+ ' + str(self.data.variables_numbers[name][lev + 1] -
                                                 self.data.variables_numbers[name][lev]))
            else:
                upgrade_value.setText(' + &#8734; ')

            if lev < len(self.data.variables_numbers[name]):
                button.setText(str(self.data.variables_cost[name][lev]) + ' soldi')
            else:
                button.hide()
                upgrade_value.hide()
                self.buttons.pop(name)

            self.update_buttons_price()

    def update_buttons_price(self):
        for i in self.buttons.keys():
            if self.data.variables_cost[i][self.data.level_variables[i]] > self.data.money:
                self.buttons[i].setEnabled(False)
        for i in self.color_buttons:
            if 100 > self.data.money:
                i.setEnabled(False)
        for i in self.color_change_buttons:
            if 200 > self.data.money:
                i.setEnabled(False)
        for i in self.images_buttons.keys():
            if self.images_buttons[i] > self.data.money:
                i.setEnabled(False)
        if 200 > self.data.money:
            self.make_homework_coin.setEnabled(False)
        if 350 > self.data.money:
            self.watch_homework_coin.setEnabled(False)

    def make_page2(self):
        v_box = QVBoxLayout(self)
        v_box.setSpacing(15)
        v_box.setAlignment(Qt.AlignCenter)
        h_box = QHBoxLayout(self)
        h_box.setSpacing(15)
        h_box.setContentsMargins(0, 0, 0, 0)
        h_box.setAlignment(Qt.AlignCenter)
        widgets = []
        n = 0
        for i in self.data.all_colors:
            widgets.append(self.make_color_widget(i))

            n += 1
            if n % 5 == 0:
                for i in widgets:
                    h_box.addWidget(i)
                widgets = []
                h_widget = QWidget(self, flags=Qt.Widget)
                h_widget.setLayout(h_box)
                v_box.addWidget(h_widget)
                h_box = QHBoxLayout(self)
                h_box.setSpacing(15)
                h_box.setContentsMargins(0, 0, 0, 0)
                h_box.setAlignment(Qt.AlignCenter)

        v_widget = QWidget(self, flags=Qt.Widget)
        v_widget.setLayout(v_box)
        return v_widget

    def make_color_widget(self, color):
        change = QPushButton('Cambia colore', self)
        change.setFixedSize(120, 30)
        change.setStyleSheet('background-color: #ffff55')
        change.hide()

        label = QLabel(self)
        label.setFixedSize(120, 90)
        label.setObjectName("color")
        label.setStyleSheet("QWidget#color {border: 1px solid grey; border-bottom: 0px solid grey; "
                            "background-color: " + color + ";}")

        price = QPushButton('100 soldi', self)
        price.setFixedSize(120, 30)
        price.setStyleSheet('background-color: #ffff55')

        price.clicked.connect(partial(self.buy_color_on_click, label, price, color))
        change.clicked.connect(partial(self.change_color_on_click, label))

        if self.data.owned_colors.__contains__(color):
            price.hide()
            label.setStyleSheet("QWidget#color {border: 1px solid grey; background-color: " + color + ";}")
            label.setFixedSize(120, 120)

        if 100 > self.data.money:
            price.setEnabled(False)

        if len(self.data.owned_colors) == len(self.data.all_colors):
            price.hide()
            change.show()
            label.setFixedSize(120, 90)
            label.setStyleSheet("QWidget#color {border: 1px solid grey; border-bottom: 0px solid grey; "
                                "background-color: " + color + ";}")

        self.color_buttons.append(price)
        self.color_label[label] = color
        self.color_change_buttons.append(change)

        box = QVBoxLayout(self)
        box.setSpacing(0)
        box.setContentsMargins(0, 0, 0, 0)
        box.addWidget(label)
        box.addWidget(price)
        box.addWidget(change)

        widget = QWidget(self, flags=Qt.Widget)
        widget.setLayout(box)
        return widget

    def buy_color_on_click (self, label, button, color):
        if Server_call_master.set_variable("/add_color.php", {'username': self.data.my_name,
                                                              'password': self.data.my_psw, 'color': color}):
            self.data.owned_colors.append(color)
            button.setVisible(False)
            label.setStyleSheet("QWidget#color {border: 1px solid grey; background-color: " + color + ";}")
            label.setFixedSize(120, 120)

            self.data.money -= 100
            self.soldi.setText(str(self.data.money) + ' soldi')
            self.update_buttons_price()

            if len(self.data.owned_colors) == len(self.data.all_colors):
                for i in self.color_change_buttons:
                    i.show()
                for i in self.color_label.keys():
                    i.setFixedSize(120, 90)
                    i.setStyleSheet("QWidget#color {border: 1px solid grey; border-bottom: 0px solid grey; "
                                    "background-color: " + self.color_label[i] + ";}")

    def change_color_on_click(self, label):
        color = self.color_label[label]
        confirm = ColorWindow(color, self.data, parent=self)

        if confirm.exec_() == QDialog.Accepted:
            if Server_call_master.set_variable("/change_color.php", {'username': self.data.my_name,
                                                                     'password': self.data.my_psw,
                                                                     'color1': color, 'color2': confirm.color}):
                self.data.money -= 200
                self.soldi.setText(str(self.data.money) + ' soldi')
                self.update_buttons_price()

                self.color_label[label] = confirm.color
                for i in range(0,len(self.data.owned_colors)):
                    if self.data.owned_colors[i] == color: self.data.owned_colors[i] = confirm.color
                self.data.all_colors = self.data.owned_colors.copy()
                label.setStyleSheet("QWidget#color {border: 1px solid grey; border-bottom: 0px solid grey; "
                                    "background-color: " + confirm.color + ";}")
        confirm.deleteLater()

    def make_page3(self):
        v_box = QVBoxLayout(self)
        v_box.setSpacing(5)
        v_box.setAlignment(Qt.AlignCenter)
        h_box = QHBoxLayout(self)
        h_box.setSpacing(5)
        h_box.setContentsMargins(0, 0, 0, 0)
        h_box.setAlignment(Qt.AlignCenter)
        widgets = []
        n = 0
        for i in self.data.all_images.keys():
            widgets.append(self.make_image_widget(i))

            n += 1
            if n % 5 == 0:
                for i in widgets:
                    h_box.addWidget(i)
                widgets = []
                h_widget = QWidget(self, flags=Qt.Widget)
                h_widget.setLayout(h_box)
                v_box.addWidget(h_widget)
                h_box = QHBoxLayout(self)
                h_box.setSpacing(5)
                h_box.setContentsMargins(0, 0, 0, 0)
                h_box.setAlignment(Qt.AlignCenter)

        v_widget = QWidget(self, flags=Qt.Widget)
        v_widget.setLayout(v_box)
        return v_widget

    def make_image_widget(self, key):
        label = QLabel(self)
        pixmap = QPixmap('img/' + key)
        pixmap = pixmap.scaled(120, 120)
        label.setPixmap(pixmap)
        label.setObjectName(key)

        price = QPushButton(str(self.data.all_images[key]) + ' soldi', self)
        price.setFixedSize(120, 30)
        price.setStyleSheet('background-color: #ffff55')
        price.clicked.connect(partial(self.buy_image_on_click, price, key))
        self.images_buttons[price] = self.data.all_images[key]

        if self.data.owned_images.__contains__(key):
            price.hide()

        if self.data.all_images[key] > self.data.money:
            price.setEnabled(False)

        box = QVBoxLayout(self)
        box.setContentsMargins(5, 5, 5, 5)
        box.setSpacing(0)
        box.addWidget(label)
        box.addWidget(price)
        widget = QWidget(self, flags=Qt.Widget)
        widget.setLayout(box)
        widget.setFixedSize(130, 130)

        if self.data.current_image == key:
            widget.setStyleSheet('background-color: #8888dd')
            self.current_image = widget

        label.mousePressEvent = partial(self.image_on_click, key, widget)
        return widget

    def image_on_click(self, key, widget, event):
        if Server_call_master.set_variable("/select_user_image.php", {'username': self.data.my_name,
                                                                      'password': self.data.my_psw, 'img': key}):
            widget.setStyleSheet('background-color: #8888dd')
            if self.current_image is not None:
                self.current_image.setStyleSheet(' ')
            self.current_image = widget
            self.data.current_image = key

    def buy_image_on_click(self, button, key):
        if Server_call_master.set_variable("/add_user_image.php", {'username': self.data.my_name,
                                                                   'password': self.data.my_psw, 'img': key}):
            self.data.owned_images.append(key)
            button.hide()

            self.data.money -= self.data.all_images[key]
            self.soldi.setText(str(self.data.money) + ' soldi')
            self.update_buttons_price()

    def make_page4(self):
        font = QFont()
        font.setPixelSize(20)

        label1 = QLabel('Gettone crea compito', self)
        label1.setFont(font)

        label1_description1 = QLabel('Questo gettone consente di creare un compito da consegnare alla classe.', self)
        label1_description1.setFixedSize(350, 33)
        label1_description1.setWordWrap(True)
        label1_description2 = QLabel('Sarà visibile solo dal prof finchè non verrà approvato.', self)
        label1_description2.setFixedSize(350, 33)
        label1_description2.setWordWrap(True)
        if self.data.student_exercises_visible:
            label1_description2.hide()

        self.make_homework_coin = QPushButton('200 soldi', self)
        self.make_homework_coin.setFixedWidth(150)
        self.make_homework_coin.setFont(font)
        self.make_homework_coin.clicked.connect(self.buy_make_homework_coin)
        self.make_homework_coin.setStyleSheet('background-color: #ffff55')

        label2 = QLabel('Gettone sbircia compito', self)
        label2.setFont(font)

        label2_description1 = QLabel("Questo gettone consente di guardare le soluzioni degli alti utenti "
                                     "prima ancora di aver consegnato.", self)
        label2_description1.setWordWrap(True)
        label2_description1.setFixedSize(350, 33)
        label2_description2 = QLabel("Il gettone non viene consumato se al momento dell'utilizzo nessuno ha inviato la "
                                     "propria soluzione.", self)
        label2_description2.setWordWrap(True)
        label2_description2.setFixedSize(350, 33)
        label2_description3 = QLabel("Utilizzabile solo in alcuni esercizi.", self)
        label2_description3.setWordWrap(True)

        self.watch_homework_coin = QPushButton('350 soldi', self)
        self.watch_homework_coin.setFixedWidth(150)
        self.watch_homework_coin.setFont(font)
        self.watch_homework_coin.clicked.connect(self.buy_watch_homework_coin)
        self.watch_homework_coin.setStyleSheet('background-color: #ffff55')

        if 200 > self.data.money:
            self.make_homework_coin.setEnabled(False)
        if self.data.make_homework_coin:
            self.make_homework_coin.setEnabled(False)
            self.make_homework_coin.setText('Acquistato')

        if 350 > self.data.money:
            self.watch_homework_coin.setEnabled(False)
        if self.data.watch_homework_coin:
            self.watch_homework_coin.setEnabled(False)
            self.watch_homework_coin.setText('Acquistato')

        box = QVBoxLayout(self)
        box.addWidget(label1)
        box.addWidget(label1_description1)
        box.addWidget(label1_description2)
        widget1 = QWidget(self, flags=Qt.Widget)
        widget1.setLayout(box)

        box = QHBoxLayout(self)
        box.setAlignment(Qt.AlignCenter)
        box.addWidget(widget1)
        box.addWidget(self.make_homework_coin)
        widget1 = QWidget(self, flags=Qt.Widget)
        widget1.setLayout(box)

        box = QVBoxLayout(self)
        box.addWidget(label2)
        box.addWidget(label2_description1)
        box.addWidget(label2_description2)
        box.addWidget(label2_description3)
        widget2 = QWidget(self, flags=Qt.Widget)
        widget2.setLayout(box)

        box = QHBoxLayout(self)
        box.setAlignment(Qt.AlignCenter)
        box.addWidget(widget2)
        box.addWidget(self.watch_homework_coin)
        widget2 = QWidget(self, flags=Qt.Widget)
        widget2.setLayout(box)

        box = QVBoxLayout(self)
        box.setContentsMargins(0, 50, 0, 0)
        box.setAlignment(Qt.AlignTop)
        box.addWidget(widget1)
        box.addWidget(widget2)
        widget = QWidget(self, flags=Qt.Widget)
        widget.setLayout(box)
        return widget

    def buy_make_homework_coin(self):
        if Server_call_master.set_variable("/add_make_homework_coin.php", {'username': self.data.my_name,
                                                                           'password': self.data.my_psw}):
            self.make_homework_coin.setEnabled(False)
            self.make_homework_coin.setText('Acquistato')
            self.data.make_homework_coin = True
            self.data.money -= 200
            self.soldi.setText(str(self.data.money) + ' soldi')
            self.update_buttons_price()

    def buy_watch_homework_coin(self):
        if Server_call_master.set_variable("/add_watch_homework_coin.php", {'username': self.data.my_name,
                                                                            'password': self.data.my_psw}):
            self.watch_homework_coin.setEnabled(False)
            self.watch_homework_coin.setText('Acquistato')
            self.data.watch_homework_coin = True
            self.data.money -= 350
            self.soldi.setText(str(self.data.money) + ' soldi')
            self.update_buttons_price()


class ColorWindow(QDialog):
    def __init__(self, color, data, parent=None):
        QDialog.__init__(self, parent)
        self.setWindowTitle('Cambia colore')
        self.setFixedSize(QSize(600, 350))

        self.data = data
        self.original = color
        self.color = color

        font = QFont()
        font.setPixelSize(15)

        red_label = QLabel('Rosso: ', self)
        red_label.setFont(font)
        red_label.setFixedHeight(30)
        green_label = QLabel('Verde: ', self)
        green_label.setFont(font)
        green_label.setFixedHeight(30)
        blu_label = QLabel('Blu: ', self)
        blu_label.setFont(font)
        blu_label.setFixedHeight(30)

        red_form = QLineEdit(self)
        red_form.setPlaceholderText("(0 - 255)")
        red_form.setFixedWidth(100)
        red_form.setFont(font)
        red_form.setTextMargins(10, 5, 10, 5)
        red_form.setText(str(int(color[1:3], 16)))

        green_form = QLineEdit(self)
        green_form.setPlaceholderText("(0 - 255)")
        green_form.setFixedWidth(100)
        green_form.setFont(font)
        green_form.setTextMargins(10, 5, 10, 5)
        green_form.setText(str(int(color[3:5], 16)))

        blu_form = QLineEdit(self)
        blu_form.setPlaceholderText("(0 - 255)")
        blu_form.setFixedWidth(100)
        blu_form.setFont(font)
        blu_form.setTextMargins(10, 5, 10, 5)
        blu_form.setText(str(int(color[5:7], 16)))

        label = QLabel(self)
        label.setFixedSize(200, 200)
        label.setObjectName("color_change")
        label.setStyleSheet("QWidget#color_change {border: 1px solid grey; background-color: " + color + ";}")

        ok = QPushButton('Cambia colore\n200 soldi', self)
        ok.clicked.connect(self.accept)
        ok.setEnabled(False)
        ok.setFont(font)
        ok.setFixedSize(120, 60)

        annulla = QPushButton('Annulla', self)
        annulla.clicked.connect(self.reject)
        annulla.setFont(font)
        annulla.setFixedSize(120, 30)

        red_form.textChanged.connect(partial(self.changed_color, label, red_form, green_form, blu_form, ok))
        green_form.textChanged.connect(partial(self.changed_color, label, red_form, green_form, blu_form, ok))
        blu_form.textChanged.connect(partial(self.changed_color, label, red_form, green_form, blu_form, ok))

        check_box = QVBoxLayout(self)
        check_box.setContentsMargins(40, 0, 0, 0)
        check_box.addWidget(ok)
        check_box.addWidget(annulla)
        check_widget = QWidget(self, Qt.Widget)
        check_widget.setLayout(check_box)

        rgb_box = QVBoxLayout(self)
        rgb_box.setContentsMargins(0, 0, 0, 0)
        rgb_box.addWidget(red_form)
        rgb_box.addWidget(green_form)
        rgb_box.addWidget(blu_form)
        rgb_widget = QWidget(self, Qt.Widget)
        rgb_widget.setLayout(rgb_box)

        rgb_box = QVBoxLayout(self)
        rgb_box.setContentsMargins(0, 0, 0, 0)
        rgb_box.addWidget(red_label)
        rgb_box.addWidget(green_label)
        rgb_box.addWidget(blu_label)
        rgb_intro_widget = QWidget(self, Qt.Widget)
        rgb_intro_widget.setLayout(rgb_box)

        box = QHBoxLayout(self)
        box.setAlignment(Qt.AlignLeft)
        box.addWidget(rgb_intro_widget)
        box.addWidget(rgb_widget)
        box.addWidget(label)
        box.addWidget(check_widget)

    def changed_color(self, label, red_form, green_form, blu_form, ok):
        r = False
        try:
            if 0 <= int(red_form.text()) <= 255:
                red_form.setStyleSheet('color: black')
                r = True
            else:
                red_form.setStyleSheet('color: red')
        except ValueError:
            red_form.setStyleSheet('color: red')

        g = False
        try:
            if 0 <= int(green_form.text()) <= 255:
                green_form.setStyleSheet('color: black')
                g = True
            else:
                green_form.setStyleSheet('color: red')
        except ValueError:
            green_form.setStyleSheet('color: red')

        b = False
        try:
            if 0 <= int(blu_form.text()) <= 255:
                blu_form.setStyleSheet('color: black')
                b = True
            else:
                blu_form.setStyleSheet('color: red')
        except ValueError:
            blu_form.setStyleSheet('color: red')

        if r and g and b:
            c = '#%02x%02x%02x' % (int(red_form.text()), int(green_form.text()), int(blu_form.text()))
            label.setStyleSheet("QWidget#color_change {border: 1px solid grey; background-color: " + c + ";}")
            if self.data.owned_colors.__contains__(c):
                ok.setEnabled(False)
            else:
                self.color = c
                ok.setEnabled(True)
        else:
            ok.setEnabled(False)
