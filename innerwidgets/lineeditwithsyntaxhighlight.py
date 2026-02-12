from PySide6.QtWidgets import QLineEdit
from PySide6.QtGui import QTextLayout, QInputMethodEvent,QTextCharFormat, QColor
from PySide6.QtCore import QCoreApplication

class LineEditWithSyntaxHighlight(QLineEdit):
    def __init__(self, parent):
        super().__init__(parent)

        highlight_color = QColor("#87cefa")
        self.syntax_highlight_format = QTextCharFormat()
        self.syntax_highlight_format.setBackground(highlight_color)

    def highlight_text_by_index_span(self, index_spans: list[tuple[int, int]]):
        attributes = []

        # s = start of hightlight section, e = end of highlight section
        for s, e in index_spans:
            type = QInputMethodEvent.AttributeType.TextFormat
            start = s - self.cursorPosition()
            length = e - s
            value = self.syntax_highlight_format
            attributes.append(QInputMethodEvent.Attribute(type, start, length, value))

        event = QInputMethodEvent("", attributes)
        QCoreApplication.sendEvent(self, event)