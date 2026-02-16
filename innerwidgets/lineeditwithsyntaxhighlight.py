from PySide6.QtWidgets import QLineEdit
from PySide6.QtGui import QTextLayout, QInputMethodEvent,QTextCharFormat, QColor
from PySide6.QtCore import QCoreApplication
import re

class LineEditWithSyntaxHighlight(QLineEdit):
    def __init__(self, parent):
        super().__init__(parent)

        highlight_color = QColor("#87cefa")
        self.syntax_highlight_format = QTextCharFormat()
        self.syntax_highlight_format.setBackground(highlight_color)

        self.is_env_var_set = False
        self.env_var_pattern = r"\{\{[ ]*[^ \{\}]+?[ ]*\}\}"

    def highlight_env_vars(self):
        url = self.text()
        if not self.is_env_var_set and re.search(self.env_var_pattern, url):
            self.is_env_var_set = True

        if self.is_env_var_set:
            attributes = []
            env_vars = re.finditer(self.env_var_pattern, url)
            env_var_indices = [(env_var.start(), env_var.end()) for env_var in env_vars]

            if not env_var_indices:
                self.is_env_var_set = False

            # s = start of hightlight section, e = end of highlight section
            for s, e in env_var_indices:
                type = QInputMethodEvent.AttributeType.TextFormat
                start = s - self.cursorPosition()
                length = e - s
                value = self.syntax_highlight_format
                attributes.append(QInputMethodEvent.Attribute(type, start, length, value))

            event = QInputMethodEvent("", attributes)
            QCoreApplication.sendEvent(self, event)