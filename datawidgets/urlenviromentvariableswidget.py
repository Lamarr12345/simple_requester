from PySide6.QtWidgets import QDialog, QPushButton, QVBoxLayout, QHBoxLayout, QStackedWidget, QLabel, QMessageBox ,QApplication
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

        self.button_update_env = QPushButton("Set Enviroment")
        self.button_update_env.clicked.connect(self.grab_and_set_enviroment_variables)
        self.button_help = QPushButton("Help")

        h_button_layout = QHBoxLayout()
        h_button_layout.addWidget(self.button_update_env)
        h_button_layout.addWidget(self.button_help)

        v_main_layout = QVBoxLayout()
        v_main_layout.addWidget(self.stack_url_env)
        v_main_layout.addLayout(h_button_layout)

        self.setLayout(v_main_layout)

        self.stack_url_env.setCurrentIndex(0)

        new_size = self.sizeHint()
        self.setFixedSize(new_size)

    def grab_and_set_enviroment_variables(self):
        url = self.parent_widget.le_url.text()

        if re.search(r"\{{3}|\}{3}", url):
            missing_error = "Variables can not be empty."
            QMessageBox.warning(self,"{}}}", missing_error, QMessageBox.Ok)
            return

        var_list = re.findall(r"(?<=\{\{).*?(?=\}\})", url)
        
        for i in range(len(var_list)):
            var_list[i] = var_list[i].strip()
            if not var_list[i]:
                missing_error = "Variables can not be empty."
                QMessageBox.warning(self,"Missing Variable Name", missing_error, QMessageBox.Ok)
                return
            
            if not re.fullmatch(r"[a-zA-Z0-9_-]+", var_list[i]):
                name_error = "Variables can only contain a-z, A-Z, 0-9, -, _ and no empty spaces."
                QMessageBox.warning(self,"Invalid Variable Name", name_error, QMessageBox.Ok)
                return
        
        if len(var_list) != len(set(var_list)):
                duplicate_error = "Variables have to be unique."
                QMessageBox.warning(self,"Duplicate Variable Name", duplicate_error, QMessageBox.Ok)
                return

        self.url_value_widget.set_env_variables_list(var_list)

        if var_list:
            self.stack_url_env.setCurrentIndex(1)
            self.button_update_env.setText("Update Enviroment")
        else:
            self.stack_url_env.setCurrentIndex(0)
            self.button_update_env.setText("Set Enviroment")

