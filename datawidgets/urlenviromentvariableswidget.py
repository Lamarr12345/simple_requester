from PySide6.QtWidgets import QDialog, QPushButton, QVBoxLayout, QHBoxLayout, QStackedWidget, QLabel, QMessageBox, QTextEdit ,QApplication
from PySide6.QtCore import Qt
import re

from innerwidgets.urlvaluewidget import URLValueWidget

class URLEnviromentVariablesWidget(QDialog):
    def __init__(self, parent, main_widget):
        super().__init__(parent=main_widget)

        self.parent_widget = parent
        self.setWindowTitle("URL Enviroment Variables")
        self.setWindowModality(Qt.WindowModal)

        empty_hint_label = QLabel("Currently no enviroment variables set up.")
        empty_hint_label.setAlignment(Qt.AlignCenter)

        self.url_value_widget = URLValueWidget()

        self.stack_url_env = QStackedWidget()
        self.stack_url_env.addWidget(empty_hint_label)
        self.stack_url_env.addWidget(self.url_value_widget)

        self.button_help = QPushButton("Help")

        v_main_layout = QVBoxLayout()
        v_main_layout.addWidget(self.stack_url_env)
        v_main_layout.addWidget(self.button_help)

        self.setLayout(v_main_layout)

        self.stack_url_env.setCurrentIndex(0)

        new_size = self.sizeHint()
        self.setFixedSize(new_size)

    def set_env_vars(self, url_widget: QTextEdit):
        
        url = url_widget.text()

        # #(?![^\{])\{\{[ ]*[^ \{\}]+?[ ]*\}\} that is one word
        # #(?<=(?![^\{])\{\{)[ ]*[^ \{\}]+?[ ]*(?=\}\}) content of brackeds (including empty spaces)
        pattern = r"(?<=(?![^\{])\{\{)[ ]*[^ \{\}]+?[ ]*(?=\}\})"
        var_list = re.findall(pattern, url)
        var_list = [var.strip() for var in var_list]
        var_list = list(dict.fromkeys(var_list))

        if var_list == self.url_value_widget.get_env_variable_key_list():
            self.parent_widget.le_url.setModified(False)
            return

        self.url_value_widget.set_env_variables_list(var_list)

        if var_list:
            self.stack_url_env.setCurrentIndex(1)
        else:
            self.stack_url_env.setCurrentIndex(0)

        url_widget.setModified(False)


    def is_var_env_valid(self, url_widget: QTextEdit):
        url = self.parent_widget.le_url.text()

        pattern = r"(?<=(?![^\{])\{\{)[ ]*[^ \{\}]+?[ ]*(?=\}\})"
        var_list = re.findall(pattern, url)
        var_list = [var.strip() for var in var_list]
        var_list = list(dict.fromkeys(var_list))

        return var_list == self.url_value_widget.get_env_variable_key_list()
    
    def get_modified_url(self, url_widget: QTextEdit):
        env_state = self.url_value_widget.get_env_variables_state()

        url:str = url_widget.text()

        pattern = r"(?![^\{])\{\{[ ]*[^ \{\}]+?[ ]*\}\}"
        replacement_list = re.findall(pattern, url)
        
        error_list = []
        for key, value in env_state:
            if not value:
                error_list.append(f"Value for the variable '{key}' is empty.")
            if " " in value:
                error_list.append(f"Value for the variable '{key}' contains empty space.")

            for replacement in replacement_list:
                print(replacement, key, value)
                if key in replacement:
                    url.replace(replacement, value)

        if error_list:
            raise ValueError("\n".join(error_list))
        
        return url


