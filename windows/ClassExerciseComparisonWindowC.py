from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QWidget, QLabel, QHBoxLayout

from windows.ClassExerciseComparisonWindow import ClassExerciseComparisonWindow


class ClassExerciseComparisonWindowC(ClassExerciseComparisonWindow):

    def h_box(self, title, value, limit, border):
        font = QFont()
        font.setPixelSize(15)
        label_title = QLabel(title, self)
        label_title.setFixedWidth(100)
        label_title.setFont(font)
        if title=='Funzioni:' or title=='Variabili:':
            label_value = QLabel("?", self)
        else:
            label_value = QLabel(str(value), self)
        label_value.setFont(font)
        if limit is not None and value > limit:
            label_title.setStyleSheet('color: red')
            label_value.setStyleSheet('color: red')
        box = QHBoxLayout(self)
        box.setSpacing(15)
        box.setContentsMargins(5, 5, 5, 5)
        box.addWidget(label_title)
        box.addWidget(label_value)
        widget = QWidget(self, flags=Qt.Widget)
        widget.setLayout(box)
        if border:
            widget.setObjectName("widget")
            widget.setStyleSheet("QWidget#widget {border: 0px solid grey; border-bottom: 1px solid grey}")
        return widget

    def color_strings(self, text):
        texts = []
        multi_line_comment, comment, string_start, i, start = False, False, None, 0, 0
        while i < len(text):
            if ((i < len(text) - 1 and text[i] == '/' and text[i+1] == '/') or text[i] == '#') \
                    and string_start is None and not multi_line_comment and not comment:
                if i != start:
                    texts.append(text[start:i])
                    start = i
                text = text[0:i] + '<span style=\" color:' + self.color_styles.comment_color \
                       + ';\">' + text[i:len(text)]
                i += len('<span style=\" color:' + self.color_styles.comment_color + ';\">') + 1
                comment = True
            elif i < len(text) - 1 and text[i] == '/' and text[i+1] == '*' and string_start is None \
                    and not multi_line_comment and not comment:
                if i != start:
                    texts.append(text[start:i])
                    start = i
                text = text[0:i] + '<span style=\" color:' + self.color_styles.multi_line_comment_color \
                       + ';\">' + text[i:len(text)]
                i += len('<span style=\" color:' + self.color_styles.multi_line_comment_color + ';\">') + 1
                multi_line_comment = True
            elif i < len(text) - 1 and text[i] == '*' and text[i+1] == '/' and string_start is None \
                    and multi_line_comment and not comment:
                text = text[0:i + 2] + '</span>' + text[i + 2:len(text)]
                i += len('</span>') + 1
                texts.append(text[start:i + 1])
                start = i + 1
                multi_line_comment = False
            elif (text[i] == '"' or text[i] == "'") and comment is False:
                if string_start is None:
                    if not multi_line_comment:
                        if i != start:
                            texts.append(text[start:i])
                            start = i
                        text = text[0:i] + '<span style=\" color:' + self.color_styles.string_color \
                               + ';\">' + text[i:len(text)]
                        i += len('<span style=\" color:' + self.color_styles.string_color + ';\">')
                        string_start = text[i]
                elif text[i] == string_start:
                    if not multi_line_comment:
                        text = text[0:i + 1] + '</span>' + text[i + 1:len(text)]
                        i += len('</span>')
                        texts.append(text[start:i + 1])
                        start = i + 1
                        string_start = None
            elif text[i] == '\n' and not multi_line_comment:
                if comment:
                    text = text[0:i] + '</span>' + text[i:len(text)]
                    i += len('</span>')
                    texts.append(text[start:i + 1])
                    start = i + 1
                    comment = False
                elif string_start is not None:
                    text = text[0:i] + '</span>' + text[i:len(text)]
                    i += len('</span>')
                    texts.append(text[start:i + 1])
                    start = i + 1
                    string_start = None
            elif text[i] == '<':  # < da sostituire con &#60
                text = text[0:i] + '&#60;' + text[i + 1:len(text)]
                i += 4
            elif text[i] == '>':  # > da sostituire con &#62
                text = text[0:i] + '&#62;' + text[i + 1:len(text)]
                i += 4
            i += 1
        texts.append(text[start:i])
        return texts
