from PySide6.QtWidgets import QDialog, QTextEdit, QVBoxLayout
from PySide6.QtCore import Qt

class JSONWidget(QDialog):
    def __init__(self, parent):
        super().__init__(parent)

        self.parent_widget = parent
        self.setWindowTitle("JSON Data")
        self.setWindowModality(Qt.WindowModal)

        self.json_data = QTextEdit()

        v_main_layout = QVBoxLayout()
        v_main_layout.addWidget(self.json_data)

        self.setLayout(v_main_layout)

    def get_json_data(self):
        return self.json_data.toPlainText()
    
    def set_json_data(self, json_text: str):
        self.json_data.setPlainText(json_text)
    
    def delete_json_data(self):
        self.json_data.clear()


