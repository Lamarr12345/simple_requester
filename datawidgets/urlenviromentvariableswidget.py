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
        self.button_help.clicked.connect(self.show_help)

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
        pattern = r"(?<=(?![^\{])\{\{)[ ]*[^\{\}]+?[ ]*(?=\}\})"
        var_list = re.findall(pattern, url)
        var_list = [var.strip() for var in var_list]
        var_list = list(dict.fromkeys(var_list))

        if var_list == self.url_value_widget.get_env_variable_key_list():
            return
        
        vars_with_empty_space = [var for var in var_list if " " in var]
        if vars_with_empty_space:
            raise ValueError("Enviroment variable(s) include empty space.")

        self.url_value_widget.set_env_variables_list(var_list)

        if var_list:
            self.stack_url_env.setCurrentIndex(1)
        else:
            self.stack_url_env.setCurrentIndex(0)


    def clear_env_vars(self):
        self.url_value_widget.delete_all_env_variables()
        self.stack_url_env.setCurrentIndex(0)

    def is_var_env_valid(self, url_widget: QTextEdit):
        url = url_widget.text()

        pattern = r"(?<=(?![^\{])\{\{)[ ]*[^ \{\}]+?[ ]*(?=\}\})"
        var_list = re.findall(pattern, url)
        var_list = [var.strip() for var in var_list]
        var_list = list(dict.fromkeys(var_list))

        return var_list == self.url_value_widget.get_env_variable_key_list()
    
    def get_modified_url(self, url_widget: QTextEdit):
        env_state = self.url_value_widget.get_env_variables_state()

        url:str = url_widget.text()
        
        error_list = []
        for key, value in env_state:
            if not value:
                error_list.append(f"Value for the variable '{key}' is empty.")
            if " " in value:
                error_list.append(f"Value for the variable '{key}' contains empty space.")
        if error_list:
            raise ValueError("\n".join(error_list))
        
        pattern = r"(?![^\{])\{\{[ ]*[^ \{\}]+?[ ]*\}\}"
        replacement_sections = re.findall(pattern, url)

        for section in replacement_sections:
            cleaned_section = section.replace(" ","")
            url = url.replace(section, cleaned_section)

        for key, value in env_state:
            url = url.replace(r"{{"+key+r"}}", value)
        
        return url
    
    def get_env_state(self):
        env_state = self.url_value_widget.get_env_variables_state()
        if env_state:
            self.stack_url_env.setCurrentIndex(1)
        else:
            self.stack_url_env.setCurrentIndex(0)
        return env_state
    
    def set_env_state(self, env_state):
        if env_state:
            self.stack_url_env.setCurrentIndex(1)
        else:
            self.stack_url_env.setCurrentIndex(0)
        self.url_value_widget.set_env_variables_state(env_state)

    def show_help(self):
        help_text = """Some Helpfull text about how it works."""
        QMessageBox.about(self, "Help", help_text)

    def is_env_set(self):
        return len(self.url_value_widget.get_env_variable_key_list()) != 0

