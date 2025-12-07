from PySide6.QtWidgets import QWidget, QLabel, QLineEdit, QListWidget, QPushButton, QHBoxLayout, QVBoxLayout,QMessageBox
import requests

from responsewidget import ResponseWidget
from utils.helper import str_to_valid_dict

class GetWidget(QWidget):
    def __init__(self, parent):
        super().__init__()

        self.main_widget = parent
        self.recent_valid_request_data = None
        self.saved_request_data = {}

        label_url = QLabel("URL:")
        self.le_url = QLineEdit(self)

        label_params = QLabel("Params (dictionary format):")
        self.le_params = QLineEdit(self)

        label_headers = QLabel("Headers (dictionary format):")
        self.le_headers = QLineEdit(self)

        b_send_request = QPushButton("Send Request")
        b_send_request.clicked.connect(self.send_request)

        b_clear_data = QPushButton("Clear Data")
        b_clear_data.clicked.connect(self.clear_data)

        label_saved_requests = QLabel("Saved Requests:")
        
        self.lw_saved_requests = QListWidget(self)

        b_save_request = QPushButton("Save")
        b_save_request.clicked.connect(self.save_request)

        b_load_request = QPushButton("Load")
        b_load_request.clicked.connect(self.load_request)

        v_url_layout = QVBoxLayout()
        v_url_layout.addWidget(label_url)
        v_url_layout.addWidget(self.le_url)

        v_params_layout = QVBoxLayout()
        v_params_layout.addWidget(label_params)
        v_params_layout.addWidget(self.le_params)

        v_headers_layout = QVBoxLayout()
        v_headers_layout.addWidget(label_headers)
        v_headers_layout.addWidget(self.le_headers)

        h_b_main_layout = QHBoxLayout()
        h_b_main_layout.addWidget(b_send_request)
        h_b_main_layout.addWidget(b_clear_data)

        v_b_saved_requests_layout = QVBoxLayout()
        v_b_saved_requests_layout.addWidget(b_save_request)
        v_b_saved_requests_layout.addWidget(b_load_request)
        v_b_saved_requests_layout.addStretch()

        h_saved_requests_layout = QHBoxLayout()
        h_saved_requests_layout.addWidget(self.lw_saved_requests)
        h_saved_requests_layout.addLayout(v_b_saved_requests_layout)

        v_saved_requests_layout = QVBoxLayout()
        v_saved_requests_layout.addWidget(label_saved_requests)
        v_saved_requests_layout.addLayout(h_saved_requests_layout)

        v_base_layout = QVBoxLayout()
        v_base_layout.addLayout(v_url_layout)
        v_base_layout.addLayout(v_params_layout)
        v_base_layout.addLayout(v_headers_layout)
        v_base_layout.addLayout(h_b_main_layout)
        v_base_layout.addLayout(v_saved_requests_layout)
        
        self.setLayout(v_base_layout)

    def send_request(self):
        url = self.le_url.text()
        try:
            params = str_to_valid_dict(self.le_params.text(), "params")
        except Exception as e:
            QMessageBox.critical(self,type(e).__name__, "\n".join(e.args), QMessageBox.Ok)
            return
        try:
            headers = str_to_valid_dict(self.le_headers.text(), "headers")
        except Exception as e:
            QMessageBox.critical(self,type(e).__name__, "\n".join(e.args), QMessageBox.Ok)
            return
        try:
            response = requests.get(url=url, params=params, headers=headers)
        except Exception as e:
            QMessageBox.critical(self,type(e).__name__, "\n".join(e.args), QMessageBox.Ok)
            return

        self.main_widget.response_widget = ResponseWidget(response)
        self.cache_recent_valid_request_data()

    def cache_recent_valid_request_data(self):
        self.recent_valid_request_data = {
            "url": self.le_url.text(),
            "params": self.le_params.text(),
            "headers": self.le_headers.text(),
        }

    def clear_data(self):
        self.le_url.clear(),
        self.le_params.clear(),
        self.le_headers.clear(),

    def save_request(self):
        if not self.recent_valid_request_data:
            QMessageBox.warning(self,"No recent data", "No recent valid unsaved data.", QMessageBox.Ok)
            return

        new_key = self.recent_valid_request_data.get("url")
        params = self.recent_valid_request_data.get("params")
        if params:
            new_key += f"++p:{params}"
        headers = self.recent_valid_request_data.get("headers")
        if headers:
            new_key += f"++h:{headers}"

        if new_key in self.saved_request_data.keys():
            QMessageBox.warning(self,"Request not new", "The exact request was saved before.\nTry sending a new request.", QMessageBox.Ok)
            return
        
        self.lw_saved_requests.addItem(new_key)
        
        self.saved_request_data[new_key] = self.recent_valid_request_data
        self.recent_valid_request_data = None

    def load_request(self):
        selected_item = self.lw_saved_requests.selectedItems()[0].text()

        saved_entry =  self.saved_request_data.get(selected_item)

        self.le_url.setText(saved_entry.get("url"))
        self.le_params.setText(saved_entry.get("params"))
        self.le_headers.setText(saved_entry.get("headers"))


