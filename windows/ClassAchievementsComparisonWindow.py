import random
import Server_call_master
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QPixmap, QIcon
from PyQt5.QtWidgets import QDialog, QWidget, QVBoxLayout, QLabel, QHBoxLayout, QScrollArea


class ClassAchievementsComparisonWindow(QDialog):
    def __init__(self, data, achievements_titles, parent=None):
        QDialog.__init__(self, parent, flags=Qt.Dialog)
        self.setWindowTitle("Classifica")
        self.setWindowIcon(QIcon("img/logo.png"))
        self.setMinimumSize(1200, 550)
        self.achievements_titles = achievements_titles
        self.data = data

        mates = Server_call_master.get_class_achievement_progress({'username': data.my_name, 'password': data.my_psw,
                                                                   'class': data.my_class})
        if mates != "":
            students_widgets = []
            not_visible_students_widget = []
            pos = 0
            for i in range(0, len(mates)):
                if i == 0 or (mates[i]['exp'] != mates[i-1]['exp'] and
                              (mates[i]['visible'] == '1' or self.data.my_name in self.data.my_proff)):
                    pos += 1
                if mates[i]['visible'] == '1' or self.data.my_name in self.data.my_proff:
                    students_widgets.append(self.make_student_widget(mates[i], pos, mates[i]['visible'] == '1'))
                else:
                    not_visible_students_widget.append(self.make_student_widget(mates[i], None, False))
            font = QFont()
            font.setPixelSize(20)
            log_line = QLabel('Classifica della classe: "' + self.data.my_class + '" per esperieza raccolta', self)
            log_line.setFont(font)
            box = QHBoxLayout(self)
            box.addWidget(log_line)
            box.setContentsMargins(75, 0, 0, 0)
            log_line = QWidget(self, flags=Qt.Widget)
            log_line.setLayout(box)
            log_line.setObjectName("log_line")
            log_line.setStyleSheet("QWidget#log_line {border: 1px solid grey; border-right: 0px solid grey; "
                                   "border-left: 0px solid grey; background-color: #88c5ff}")
            log_line.setFixedHeight(50)

            box = QHBoxLayout(self)
            box.setAlignment(Qt.AlignLeft)
            random.shuffle(not_visible_students_widget)
            for i in students_widgets:
                box.addWidget(i, alignment=Qt.AlignLeft)
            for i in not_visible_students_widget:
                box.addWidget(i, alignment=Qt.AlignLeft)
            widget = QWidget(self, flags=Qt.Widget)
            widget.setLayout(box)
            scroll = QScrollArea(self)
            scroll.setWidget(widget)
            scroll.setObjectName("scroll")
            scroll.setStyleSheet("QWidget#scroll {border: 0px solid grey}")
            box = QVBoxLayout(self)
            box.setContentsMargins(0,0,0,0)
            box.addWidget(log_line)
            box.addWidget(scroll)

    def make_student_widget(self, user, position, visible):
        font = QFont()
        font.setPixelSize(20)

        pos_str = "?" if position is None else ((str(position)+"°") if visible else ("(" + str(position)+"°"))
        pos = QLabel(pos_str, self)
        pos.setFont(font)
        pos.setFixedWidth(50)

        title = QLabel(user['username'] if visible or self.data.my_name not in self.data.my_proff else
                       user['username'] + ')', self)
        title.setFont(font)

        font.setPixelSize(15)

        pixmap = QPixmap('img/' + user['current_image'])
        pixmap = pixmap.scaled(100, 100)
        img = QLabel(self)
        img.setPixmap(pixmap)
        img.setObjectName('img/' + user['current_image'])

        l = 1
        old = 0
        for i in self.data.level_progression:
            if int(user['exp']) >= i:
                l += 1
                old = i

        level_number_str = '???' if position is None else('Liv. ' + str(l))
        level_number = QLabel(level_number_str, self)
        level_number.setFont(font)
        level_number.setAlignment(Qt.AlignRight)
        level_number.setStyleSheet('background-color: #9999FF; border: 1px solid grey')
        level_number.setFixedSize(100, 35)
        level_number.setContentsMargins(0, 10, 10, 0)

        level_bar = QLabel(self)
        level_bar.setStyleSheet('background-color: #4040FF')
        level_bar.setFixedSize(int(100*(int(user['exp'])-old)/(self.data.level_progression[l-1]-old)), 5)
        if position is None:
            level_bar.hide()
            level_number.setFixedHeight(40)

        box = QVBoxLayout(self)
        box.setSpacing(0)
        box.setContentsMargins(0, 0, 0, 0)
        box.addWidget(level_number)
        box.addWidget(level_bar)
        lev = QWidget(self, flags=Qt.Widget)
        lev.setLayout(box)
        lev.setObjectName("level")
        lev.setStyleSheet("QWidget#level {border: 1px solid grey; background-color: #BBBBFF}")
        lev.setFixedHeight(40)

        money_str = '???' if position is None else(user['money'] + " Soldi")
        money = QLabel(money_str, self)
        money.setFont(font)
        money.setFixedSize(100, 40)
        money.setAlignment(Qt.AlignRight)
        money.setContentsMargins(0, 10, 10, 0)
        money.setStyleSheet("background-color: yellow; border: 1px solid grey")

        if not visible and self.data.my_name in self.data.my_proff:
            description = QLabel('Utente in modalità riservata')
            description.setFont(font)
            box = QHBoxLayout(self)
            box.setContentsMargins(0, 0, 0, 0)
            box.setSpacing(5)
            box.addWidget(pos)
            box.addWidget(title)
            who = QWidget(self, flags=Qt.Widget)
            who.setLayout(box)
            box = QVBoxLayout(self)
            box.setContentsMargins(10, 5, 10, 0)
            box.setSpacing(5)
            box.addWidget(who)
            box.addWidget(description)
            who = QWidget(self, flags=Qt.Widget)
            who.setLayout(box)
        else:
            box = QHBoxLayout(self)
            box.setSpacing(5)
            box.addWidget(pos)
            box.addWidget(title)
            who = QWidget(self, flags=Qt.Widget)
            who.setLayout(box)

        box = QVBoxLayout(self)
        box.setContentsMargins(0, 0, 0, 0)
        box.setSpacing(0)
        box.addWidget(lev)
        box.addWidget(money)
        lev_mon = QWidget(self, flags=Qt.Widget)
        lev_mon.setLayout(box)

        box = QHBoxLayout(self)
        box.setContentsMargins(0,0,0,0)
        box.addWidget(img)
        box.addWidget(lev_mon, alignment=Qt.AlignRight)
        what = QWidget(self, flags=Qt.Widget)
        what.setLayout(box)

        progress = user['progress'].split(',')

        box = QVBoxLayout(self)
        box.addWidget(who)
        box.addWidget(what)
        for i in range(0, len(progress)):
            box.addWidget(
                self.make_achievement_widget(self.achievements_titles[i], progress[i], (position is not None)))
        widget = QWidget(self, flags=Qt.Widget)
        widget.setLayout(box)
        widget.setObjectName("w")
        widget.setStyleSheet("QWidget#w {background-color: white; border: 1px solid grey}")

        return widget

    def make_achievement_widget(self, title, progress, visible):
        font = QFont()
        font.setPixelSize(15)

        name = QLabel(title, self)
        name.setFont(font)
        name.setFixedWidth(220)
        name.setContentsMargins(10, 0, 0, 0)

        box = QVBoxLayout(self)
        box.setSpacing(0)
        box.setContentsMargins(0, 0, 0, 0)
        box.addWidget(name)

        widget = QWidget(self, flags=Qt.Widget)
        widget.setFixedHeight(50)
        widget.setObjectName("widget")

        if progress != 'ok' and visible:
            prog = QLabel(progress+"%", self)
            prog.setAlignment(Qt.AlignCenter)
            prog.setFixedSize(max(int(progress)*2.4, 45), 20)
            prog.setStyleSheet("border: 1px solid grey; background-color: #99FF99")
            box.addWidget(prog)
            widget.setStyleSheet("QWidget#widget {border: 1px solid grey; background-color: #9999FF}")
        elif visible:
            widget.setStyleSheet("QWidget#widget {border: 1px solid grey; background-color: #99FF99}")
        else:
            widget.setStyleSheet("QWidget#widget {border: 1px solid grey; background-color: #9999FF}")


        widget.setLayout(box)
        return widget
