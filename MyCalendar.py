from PyQt5.QtWidgets import QCalendarWidget


class MyCalendar(QCalendarWidget):
    def __init__(self, parent=None):
        QCalendarWidget.__init__(self, parent)

    def paintCell(self, painter, rect, date, **kwargs):
        QCalendarWidget.paintCell(self, painter, rect, date)
        if date == self.selectedDate():
            painter.drawText(rect.bottomLeft(), "   ------")
