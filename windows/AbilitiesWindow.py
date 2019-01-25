from functools import partial

from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtWidgets import QWidget, QPushButton, QHBoxLayout, QVBoxLayout, QLabel, QDialog, QLineEdit
from PyQt5.QtCore import *


class AbilitiesWindow(QWidget):
    def __init__(self, home, data):
        super(AbilitiesWindow, self).__init__(home, flags=Qt.Widget)
        home.setWindowTitle("Gamification - Negozio")
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
        home_button.setFixedSize(100, 50)
        home_button.clicked.connect(self.home.open_MainWindow)
        home_button.setFont(font)

        button1 = QPushButton('CONTATORI', self)
        button1.setFixedHeight(50)
        button1.setFont(font)
        button2 = QPushButton('COLORI', self)
        button2.setFixedHeight(50)
        button2.setFont(font)
        button3 = QPushButton('SKIN', self)
        button3.setFixedHeight(50)
        button3.setFont(font)
        button4 = QPushButton('GETTONI', self)
        button4.setFixedHeight(50)
        button4.setFont(font)

        page1 = self.make_page1()
        page2 = self.make_page2()
        page3 = self.make_page3()
        page4 = self.make_page4()

        button1.clicked.connect(partial(self.open_subpage,button1,page1,button2,page2,button3,page3,button4,page4))
        button2.clicked.connect(partial(self.open_subpage,button2,page2,button1,page1,button3,page3,button4,page4))
        button3.clicked.connect(partial(self.open_subpage,button3,page3,button2,page2,button1,page1,button4,page4))
        button4.clicked.connect(partial(self.open_subpage,button4,page4,button2,page2,button3,page3,button1,page1))

        self.open_subpage(button1,page1,button2,page2,button3,page3,button4,page4)

        self.soldi = QLabel(str(self.data.money) + ' soldi', self)
        self.soldi.setFont(font)

        empty = QWidget(self, flags=Qt.Widget)
        empty.setFixedWidth(20)

        home_box = QHBoxLayout(self)
        home_box.addWidget(home_button)
        home_box.setContentsMargins(0,0,40,0)
        home_widget = QWidget(self, flags=Qt.Widget)
        home_widget.setLayout(home_box)
        home_widget.setFixedWidth(180)

        top_box = QHBoxLayout(self)
        top_box.addWidget(home_widget)
        top_box.addWidget(button1)
        top_box.addWidget(button2)
        top_box.addWidget(button3)
        top_box.addWidget(button4)
        top_box.setContentsMargins(20, 10, 20, 10)
        top_box.setSpacing(0)
        top_widget = QWidget(self, flags=Qt.Widget)
        top_widget.setLayout(top_box)
        top_widget.setFixedHeight(90)
        top_widget.setObjectName("topStyle")
        top_widget.setStyleSheet("QWidget#topStyle {border: 0px solid grey; border-bottom: 1px solid grey}")

        box = QHBoxLayout(self)
        box.addWidget(self.soldi)
        box.setContentsMargins(20,10,20,10)
        box.setAlignment(Qt.AlignRight)
        bottom_widget = QWidget(self, flags=Qt.Widget)
        bottom_widget.setLayout(box)
        bottom_widget.setObjectName("soldi")
        bottom_widget.setStyleSheet("QWidget#soldi {border: 1px solid grey; border-top: 0px solid grey; "
                                    "background-color:yellow;}")
        bottom_widget.setFixedHeight(50)

        window_layaut = QVBoxLayout(self)
        window_layaut.setContentsMargins(0,0,0,0)
        window_layaut.addWidget(top_widget)
        window_layaut.addWidget(bottom_widget, alignment=Qt.AlignRight)
        window_layaut.addWidget(page1)
        window_layaut.addWidget(page2)
        window_layaut.addWidget(page3)
        window_layaut.addWidget(page4)
        window_layaut.setSpacing(0)

    def open_subpage(self,b1,p1,b2,p2,b3,p3,b4,p4):
        p1.setVisible(True)
        p2.setVisible(False)
        p3.setVisible(False)
        p4.setVisible(False)
        b1.setStyleSheet('background-color: grey')
        b2.setStyleSheet('background-color: #c9c9c9')
        b3.setStyleSheet('background-color: #c9c9c9')
        b4.setStyleSheet('background-color: #c9c9c9')

    def make_page1(self):
        box = QHBoxLayout(self)
        box.setContentsMargins(0,0,0,0)
        box.addWidget(self.counter_upgrade_widget('Righe di codice'))
        box.setAlignment(Qt.AlignLeft)
        widget_lines = QWidget(self, flags=Qt.Widget)
        widget_lines.setLayout(box)

        box = QHBoxLayout(self)
        box.setContentsMargins(0,0,0,0)
        box.addWidget(self.counter_upgrade_widget('Variabili'))
        box.setAlignment(Qt.AlignLeft)
        widget_variables = QWidget(self, flags=Qt.Widget)
        widget_variables.setLayout(box)

        box = QHBoxLayout(self)
        box.setContentsMargins(0,0,0,0)
        box.addWidget(self.counter_upgrade_widget('if'))
        box.addWidget(self.counter_upgrade_widget('elif'))
        box.addWidget(self.counter_upgrade_widget('else'))
        box.setAlignment(Qt.AlignLeft)
        widget_conditions = QWidget(self, flags=Qt.Widget)
        widget_conditions.setLayout(box)

        box = QHBoxLayout(self)
        box.setContentsMargins(0,0,0,0)
        box.addWidget(self.counter_upgrade_widget('for'))
        box.addWidget(self.counter_upgrade_widget('while'))
        box.setAlignment(Qt.AlignLeft)
        widget_cycles = QWidget(self, flags=Qt.Widget)
        widget_cycles.setLayout(box)

        box = QHBoxLayout(self)
        box.setContentsMargins(0,0,0,0)
        box.addWidget(self.counter_upgrade_widget('def'))
        box.setAlignment(Qt.AlignLeft)
        widget_functions = QWidget(self, flags=Qt.Widget)
        widget_functions.setLayout(box)

        box = QVBoxLayout(self)
        box.setSpacing(25)
        box.setContentsMargins(0,0,0,0)
        box.addWidget(widget_lines)
        box.addWidget(widget_variables)
        box.setAlignment(Qt.AlignTop)
        widget1 = QWidget(self, flags=Qt.Widget)
        widget1.setLayout(box)

        box = QVBoxLayout(self)
        box.setContentsMargins(0,0,0,0)
        box.setSpacing(25)
        box.addWidget(widget_conditions)
        box.addWidget(widget_cycles)
        box.addWidget(widget_functions)
        box.setAlignment(Qt.AlignTop)
        widget2 = QWidget(self, flags=Qt.Widget)
        widget2.setLayout(box)

        box = QHBoxLayout(self)
        box.setContentsMargins(0,50,0,0)
        box.setSpacing(50)
        box.addWidget(widget1)
        box.addWidget(widget2)
        box.setAlignment(Qt.AlignHCenter)
        widget = QWidget(self, flags=Qt.Widget)
        widget.setLayout(box)
        return widget

    def counter_upgrade_widget(self, name):
        font = QFont()
        font.setPixelSize(15)

        name_label = QLabel(self)
        name_label.setText(name)
        name_label.setContentsMargins(10,0,10,0)
        name_label.setFont(font)

        if name == 'Righe di codice':
            name = 'lines'
        elif name == 'Variabili':
            name = 'variables'
        elif name == 'def':
            name = 'functions'

        lev = self.data.level_variables[name]
        numbers_upgrade = QLabel(self)
        if lev < len(self.data.variables_numbers[name])-1:
            numbers_upgrade.setText(str(self.data.variables_numbers[name][lev]) + ' &#8594; '
                                    + str(self.data.variables_numbers[name][lev + 1]))
        elif lev < len(self.data.variables_numbers[name]):
            numbers_upgrade.setText(str(self.data.variables_numbers[name][lev]) + ' &#8594; No Limit ')
        else:
            numbers_upgrade.setText(' ')
        numbers_upgrade.setTextFormat(Qt.RichText)
        numbers_upgrade.setContentsMargins(10,0,10,0)
        numbers_upgrade.setFont(font)

        cost = QPushButton(self)
        cost.clicked.connect(partial(self.upgrade_counter, name, cost, numbers_upgrade))
        cost.setFont(font)
        self.buttons[name] = cost

        if lev < len(self.data.variables_numbers[name]):
            cost.setText(str(self.data.variables_cost[name][lev]) + ' soldi')
            if self.data.variables_cost[name][lev] > self.data.money:
                cost.setEnabled(False)
        else:
            cost.setText(' No limit ')
            cost.setEnabled(False)
            self.buttons.pop(name)

        box = QVBoxLayout(self)
        box.addWidget(name_label)
        box.addWidget(numbers_upgrade)
        box.addWidget(cost)
        box.setAlignment(Qt.AlignTop)
        box.setContentsMargins(0,10,0,0)

        widget = QWidget(self, flags=Qt.Widget)
        widget.setLayout(box)
        widget.setObjectName("counter")
        widget.setStyleSheet("QWidget#counter {border: 1px solid grey;}")
        return widget

    def upgrade_counter(self, name, button, numbers):
        lev = self.data.level_variables[name]
        self.data.money -= self.data.variables_cost[name][lev]
        self.soldi.setText(str(self.data.money) + ' soldi')
        self.data.level_variables[name] += 1
        self.data.owned_variables = self.data.get_owned_variables_numbers()
        lev = self.data.level_variables[name]
        if lev < len(self.data.variables_numbers[name])-1:
            numbers.setText(str(self.data.variables_numbers[name][lev]) + ' &#8594; '
                            + str(self.data.variables_numbers[name][lev + 1]))
        elif lev < len(self.data.variables_numbers[name]):
            numbers.setText(str(self.data.variables_numbers[name][lev]) + ' &#8594; No Limit ')
        else:
            numbers.setText(' ')

        if lev < len(self.data.variables_numbers[name]):
            button.setText(str(self.data.variables_cost[name][lev]) + ' soldi')
        else:
            button.setText(' No limit ')
            button.setEnabled(False)
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
        if 500 > self.data.money:
            self.watch_homework_coin.setEnabled(False)



    def make_page2(self):
        v_box = QVBoxLayout(self)
        v_box.setSpacing(15)
        v_box.setAlignment(Qt.AlignTop)
        h_box = QHBoxLayout(self)
        h_box.setSpacing(15)
        h_box.setContentsMargins(0,0,0,0)
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
                h_box.setContentsMargins(0,0,0,0)
                h_box.setAlignment(Qt.AlignCenter)

        v_widget = QWidget(self, flags=Qt.Widget)
        v_widget.setLayout(v_box)
        return v_widget

    def make_color_widget(self, color):
        change = QPushButton('Cambia colore', self)
        change.setFixedSize(120,30)
        change.setStyleSheet('background-color: #dddddd')
        change.hide()

        label = QLabel(self)
        label.setFixedSize(120, 90)
        label.setObjectName("color")
        label.setStyleSheet("QWidget#color {border: 1px solid grey; border-bottom: 0px solid grey; "
                            "background-color: " + color + ";}")

        price = QPushButton('100 soldi', self)
        price.setFixedSize(120,30)
        price.setStyleSheet('background-color: #dddddd')

        price.clicked.connect(partial(self.buy_color_on_click,label,price,color))
        change.clicked.connect(partial(self.change_color_on_click,label))

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
        box.setContentsMargins(0,0,0,0)
        box.addWidget(label)
        box.addWidget(price)
        box.addWidget(change)

        widget = QWidget(self, flags=Qt.Widget)
        widget.setLayout(box)
        return widget

    def buy_color_on_click(self, label, button, color):
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
                i.setStyleSheet("QWidget#color {border: 1px solid grey; "
                                "border-bottom: 0px solid grey; background-color: " + self.color_label[i] + ";}")

    def change_color_on_click(self, label):
        color = self.color_label[label]
        confirm = ColorWindow(color, parent=self)

        if confirm.exec_() == QDialog.Accepted:
            self.data.money -= 200
            self.soldi.setText(str(self.data.money) + ' soldi')
            self.update_buttons_price()

            self.color_label[label] = confirm.color
            self.data.owned_colors.remove(color)
            self.data.all_colors.remove(color)
            self.data.owned_colors.append(confirm.color)
            self.data.all_colors.append(confirm.color)
            label.setStyleSheet("QWidget#color {border: 1px solid grey; border-bottom: 0px solid grey; "
                                "background-color: " + confirm.color + ";}")
        confirm.deleteLater()

    def make_page3(self):
        v_box = QVBoxLayout(self)
        v_box.setSpacing(5)
        v_box.setAlignment(Qt.AlignTop)
        h_box = QHBoxLayout(self)
        h_box.setSpacing(5)
        h_box.setContentsMargins(0,0,0,0)
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
                h_box.setContentsMargins(0,0,0,0)
                h_box.setAlignment(Qt.AlignCenter)

        v_widget = QWidget(self, flags=Qt.Widget)
        v_widget.setLayout(v_box)
        return v_widget

    def make_image_widget(self, key):
        label = QLabel(self)
        pixmap = QPixmap(key)
        pixmap = pixmap.scaled(120,120)
        label.setPixmap(pixmap)
        label.setObjectName(key)

        price = QPushButton(str(self.data.all_images[key]) + ' soldi', self)
        price.setFixedSize(120,30)
        price.setStyleSheet('background-color: #dddddd')
        price.clicked.connect(partial(self.buy_image_on_click,price,key))
        self.images_buttons[price] = self.data.all_images[key]

        if self.data.owned_images.__contains__(key):
            price.hide()

        if 100 > self.data.money:
            price.setEnabled(False)

        box = QVBoxLayout(self)
        box.setContentsMargins(5,5,5,5)
        box.setSpacing(0)
        box.addWidget(label)
        box.addWidget(price)
        widget = QWidget(self, flags=Qt.Widget)
        widget.setLayout(box)
        widget.setFixedSize(130,130)

        if self.data.current_image == key:
            widget.setStyleSheet('background-color: #8888dd')
            self.current_image = widget

        label.mousePressEvent = partial(self.image_on_click, key, widget)
        return widget

    def image_on_click(self, key, widget, event):
        if self.data.owned_images.__contains__(key):
            widget.setStyleSheet('background-color: #8888dd')
            self.current_image.setStyleSheet(' ')
            self.current_image = widget
            self.data.current_image = key

    def buy_image_on_click(self, button, key):
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

        self.make_homework_coin = QPushButton('200 soldi', self)
        self.make_homework_coin.setFixedSize(150,40)
        self.make_homework_coin.setFont(font)
        self.make_homework_coin.clicked.connect(self.buy_make_homework_coin)

        label2 = QLabel('Gettone sbircia compito', self)
        label2.setFont(font)

        self.watch_homework_coin = QPushButton('500 soldi', self)
        self.watch_homework_coin.setFixedSize(150,40)
        self.watch_homework_coin.setFont(font)
        self.watch_homework_coin.clicked.connect(self.buy_watch_homework_coin)

        if 200 > self.data.money:
            self.make_homework_coin.setEnabled(False)
        if self.data.make_homework_coin:
            self.make_homework_coin.setEnabled(False)
            self.make_homework_coin.setText('Acquistato')

        if 500 > self.data.money:
            self.watch_homework_coin.setEnabled(False)
        if self.data.watch_homework_coin:
            self.watch_homework_coin.setEnabled(False)
            self.watch_homework_coin.setText('Acquistato')

        box = QHBoxLayout(self)
        box.setAlignment(Qt.AlignCenter)
        box.addWidget(label1)
        box.addWidget(self.make_homework_coin)
        widget1 = QWidget(self, flags=Qt.Widget)
        widget1.setLayout(box)

        box = QHBoxLayout(self)
        box.setAlignment(Qt.AlignCenter)
        box.addWidget(label2)
        box.addWidget(self.watch_homework_coin)
        widget2 = QWidget(self, flags=Qt.Widget)
        widget2.setLayout(box)

        box = QVBoxLayout(self)
        box.setContentsMargins(0,50,0,0)
        box.setAlignment(Qt.AlignTop)
        box.addWidget(widget1)
        box.addWidget(widget2)
        widget = QWidget(self, flags=Qt.Widget)
        widget.setLayout(box)
        return widget

    def buy_make_homework_coin(self):
        self.make_homework_coin.setEnabled(False)
        self.make_homework_coin.setText('Acquistato')
        self.data.make_homework_coin = True
        self.data.money -= 200
        self.soldi.setText(str(self.data.money) + ' soldi')
        self.update_buttons_price()

    def buy_watch_homework_coin(self):
        self.watch_homework_coin.setEnabled(False)
        self.watch_homework_coin.setText('Acquistato')
        self.data.watch_homework_coin = True
        self.data.money -= 500
        self.soldi.setText(str(self.data.money) + ' soldi')
        self.update_buttons_price()


class ColorWindow(QDialog):
    def __init__(self,color, parent=None):
        QDialog.__init__(self, parent)
        self.setWindowTitle('Gamification - Cambia colore')
        self.setFixedSize(QSize(600, 300))

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
        red_form.setTextMargins(10,5,10,5)
        red_form.setText(str(int(color[1:3], 16)))

        green_form = QLineEdit(self)
        green_form.setPlaceholderText("(0 - 255)")
        green_form.setFixedWidth(100)
        green_form.setFont(font)
        green_form.setTextMargins(10,5,10,5)
        green_form.setText(str(int(color[3:5], 16)))

        blu_form = QLineEdit(self)
        blu_form.setPlaceholderText("(0 - 255)")
        blu_form.setFixedWidth(100)
        blu_form.setFont(font)
        blu_form.setTextMargins(10,5,10,5)
        blu_form.setText(str(int(color[5:7], 16)))

        label = QLabel(self)
        label.setFixedSize(200,200)
        label.setObjectName("color_change")
        label.setStyleSheet("QWidget#color_change {border: 1px solid grey; background-color: " + color + ";}")

        ok = QPushButton('Cambia colore\n200 soldi', self)
        ok.clicked.connect(self.accept)
        ok.setEnabled(False)
        ok.setFont(font)
        ok.setFixedSize(120,60)

        annulla = QPushButton('Annulla', self)
        annulla.clicked.connect(self.reject)
        annulla.setFont(font)
        annulla.setFixedSize(120,30)

        red_form.textChanged.connect(partial(self.changed_color, label, red_form, green_form, blu_form,ok))
        green_form.textChanged.connect(partial(self.changed_color, label, red_form, green_form, blu_form,ok))
        blu_form.textChanged.connect(partial(self.changed_color, label, red_form, green_form, blu_form,ok))

        check_box = QVBoxLayout(self)
        check_box.setContentsMargins(40,0,0,0)
        check_box.addWidget(ok)
        check_box.addWidget(annulla)
        check_widget = QWidget(self, Qt.Widget)
        check_widget.setLayout(check_box)

        rgb_box = QVBoxLayout(self)
        rgb_box.setContentsMargins(0,0,0,0)
        rgb_box.addWidget(red_form)
        rgb_box.addWidget(green_form)
        rgb_box.addWidget(blu_form)
        rgb_widget = QWidget(self, Qt.Widget)
        rgb_widget.setLayout(rgb_box)

        rgb_box = QVBoxLayout(self)
        rgb_box.setContentsMargins(0,0,0,0)
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
            if c != self.original:
                self.color = c
                ok.setEnabled(True)
            else:
                ok.setEnabled(False)
        else:
            ok.setEnabled(False)
