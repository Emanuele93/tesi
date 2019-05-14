from functools import partial
from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtWidgets import QWidget, QPushButton, QHBoxLayout, QVBoxLayout, QLabel, QDialog, QLineEdit
from PyQt5.QtCore import *
import Server_call_master
from windows.AbilitiesWindow import AbilitiesWindow


class AbilitiesWindowC(AbilitiesWindow):
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
        box.addWidget(self.counter_upgrade_widget('else if'))
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
        box.addWidget(self.counter_upgrade_widget('Funzioni correnti'))
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
        elif name == 'Funzioni correnti':
            name = 'functions'
        elif name == 'else if':
            name = 'elif'

        lev = self.data.level_variables[name]
        numbers_upgrade = QLabel(self)
        if lev < len(self.data.variables_numbers[name]):
            if name == 'variables' or name == 'functions':
                numbers_upgrade.setText("?")
            else:
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
        cost.setEnabled(not(name == 'variables' or name == 'functions'))
        self.buttons[name] = cost

        if lev < len(self.data.variables_numbers[name]):
            if name == 'variables' or name == 'functions':
                cost.setText("?")
            else:
                cost.setText(str(self.data.variables_cost[name][lev]) + ' soldi')
            if self.data.variables_cost[name][lev] > self.data.money:
                cost.setEnabled(False)
        else:
            self.buttons.pop(name)

        lev = self.data.level_variables[name]
        if lev < len(self.data.variables_numbers[name])-1:
            if name == 'variables' or name == 'functions':
                upgrade_value.setText("   Non implementato   ")
            else:
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
