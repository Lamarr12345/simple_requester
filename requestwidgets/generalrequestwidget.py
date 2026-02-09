from PySide6.QtWidgets import QWidget, QLabel, QLineEdit, QListWidget, QPushButton, QHBoxLayout, QVBoxLayout,QMessageBox
from PySide6.QtCore import Qt
from requests import request

from responsewidget import ResponseWidget
from innerwidgets.keyvaluewidget import KeyValueWidget
from datawidgets.jsonwidget import JSONWidget
from datawidgets.urlenviromentvariableswidget import URLEnviromentVariablesWidget
from utils.helper import valid_json_to_py_object

class GeneralRequestWidget(QWidget):
    
    def __init__(self, parent, method):
       
        super().__init__()

        self.main_widget = parent
        self.method = method
        self.recent_valid_request_data = None
        self.saved_request_data = {}
        self.url_var_env_widget = URLEnviromentVariablesWidget(self, self.main_widget)
        self.json_data_widget = JSONWidget(self.main_widget)

        # URL Section
        label_url = QLabel("URL:")
        self.le_url = QLineEdit(self)
        self.le_url.setPlaceholderText("URL here")
        self.le_url.setFixedWidth(400)
        v_url_layout = QVBoxLayout()
        v_url_layout.addWidget(label_url)
        v_url_layout.addWidget(self.le_url)

        # Parameters Section
        label_params = QLabel("Params:")
        self.kv_params = KeyValueWidget(parent=self)
        b_add_param = QPushButton("Add Param")
        b_add_param.clicked.connect(self.kv_params.add_kv_pair)
        v_params_layout = QVBoxLayout()
        v_params_layout.addWidget(label_params)
        v_params_layout.addWidget(self.kv_params)
        v_params_layout.addWidget(b_add_param)

        # Headers Section
        label_headers = QLabel("Headers:")
        self.kv_headers = KeyValueWidget(parent=self)
        b_add_header = QPushButton("Add Header")
        b_add_header.clicked.connect(self.kv_headers.add_kv_pair)
        v_headers_layout = QVBoxLayout()
        v_headers_layout.addWidget(label_headers)
        v_headers_layout.addWidget(self.kv_headers)
        v_headers_layout.addWidget(b_add_header)

        # Main Action Buttons
        b_send_request = QPushButton("Send Request")
        b_send_request.clicked.connect(self.send_request)
        b_url_var_env = QPushButton("Var Enviroment")
        b_url_var_env.clicked.connect(self.set_env_vars_and_show_widget)
        b_clear_data = QPushButton("Clear Data")
        b_clear_data.clicked.connect(self.clear_data)
        h_main_buttons_layout = QHBoxLayout()
        h_main_buttons_layout.addWidget(b_send_request, 1)
        h_main_buttons_layout.addWidget(b_url_var_env, 1)
        h_main_buttons_layout.addWidget(b_clear_data, 1)

        # JSON Data Section
        label_data = QLabel("Data:")
        b_edit_json_data = QPushButton("Edit JSON")
        b_edit_json_data.clicked.connect(self.edit_json_data)
        v_data_layout = QVBoxLayout()
        v_data_layout.addWidget(label_data)
        v_data_layout.addWidget(b_edit_json_data)

        # Saved Requests Section
        label_saved_requests = QLabel("Saved Requests:")
        self.le_savename = QLineEdit(self)
        self.le_savename.setPlaceholderText("Savename here")
        self.lw_saved_requests = QListWidget(self)
        v_save_requests_layout = QVBoxLayout()
        v_save_requests_layout.addWidget(self.le_savename)
        v_save_requests_layout.addWidget(self.lw_saved_requests)

        # Saved Requests Action Buttons
        b_save_request = QPushButton("Save")
        b_save_request.clicked.connect(self.save_request)
        b_load_request = QPushButton("Load")
        b_load_request.clicked.connect(self.load_request)
        b_delete_request = QPushButton("Delete")
        b_delete_request.clicked.connect(self.delete_request)
        v_save_requests_buttons_layout = QVBoxLayout()
        v_save_requests_buttons_layout.setAlignment(Qt.AlignTop)
        v_save_requests_buttons_layout.addWidget(b_save_request)
        v_save_requests_buttons_layout.addWidget(b_load_request)
        v_save_requests_buttons_layout.addWidget(b_delete_request)

        h_save_requests_layout = QHBoxLayout()
        h_save_requests_layout.addLayout(v_save_requests_layout)
        h_save_requests_layout.addLayout(v_save_requests_buttons_layout)

        # Main Layout Organization
        v_main_layout_1 = QVBoxLayout()
        v_main_layout_1.addLayout(v_url_layout)
        v_main_layout_1.addLayout(h_main_buttons_layout)
        v_main_layout_1.addLayout(v_data_layout)
        v_main_layout_1.addWidget(label_saved_requests)
        v_main_layout_1.addLayout(h_save_requests_layout)

        v_main_layout_2 = QVBoxLayout()
        v_main_layout_2.addLayout(v_params_layout)
        v_main_layout_2.addLayout(v_headers_layout)

        h_main_layout = QHBoxLayout()
        h_main_layout.addLayout(v_main_layout_1)
        h_main_layout.addLayout(v_main_layout_2)

        self.setLayout(h_main_layout)
       

    def send_request(self):
       
        self.le_url.setText(self.le_url.text().strip())
        url = self.le_url.text()

        try:
            json = valid_json_to_py_object(self.json_data_widget.get_json_data())
        except Exception as e:
            QMessageBox.critical(self,type(e).__name__, str(e), QMessageBox.Ok)
            return
        
        if not self.url_var_env_widget.is_var_env_valid(self.le_url):
            QMessageBox.critical(self, "Var Env Error","The current variable enviroment is not matching the URL anymore.", QMessageBox.Ok)
            return
        
        if self.url_var_env_widget.url_value_widget.get_env_variable_key_list():
            try:
                url = self.url_var_env_widget.get_modified_url(self.le_url)
            except Exception as e:
                QMessageBox.critical(self,type(e).__name__, str(e), QMessageBox.Ok)
                return

        try:
            response = request(method=self.method,
                               url=url,
                               params=self.kv_params.get_valid_kv_list(),
                               headers=self.kv_headers.get_valid_kv_dict(),
                               json=json,
                               timeout=self.main_widget.response_timeout)
        except Exception as e:
            QMessageBox.critical(self,type(e).__name__, str(e), QMessageBox.Ok)
            return

        self.main_widget.response_widget = ResponseWidget(response)
        self._cache_recent_valid_request_data()

    def _cache_recent_valid_request_data(self):
      
        self.recent_valid_request_data = {
            "url": self.le_url.text(),
            "url_env_state": self.url_var_env_widget.get_env_state(),
            "json": self.json_data_widget.get_json_data(),
            "params_state": self.kv_params.get_complete_widget_state(),
            "headers_state": self.kv_headers.get_complete_widget_state(),
        }


    def clear_data(self):
    
        self.le_url.clear()
        self.json_data_widget.delete_json_data()
        self.kv_params.delete_all_kv_pair()
        self.kv_headers.delete_all_kv_pair()
        self.url_var_env_widget.clear_env_vars()

    def save_request(self):
       
        if not self.recent_valid_request_data:
            QMessageBox.warning(self,"No recent data", "No recent valid unsaved data.", QMessageBox.Ok)
            return

        self.le_savename.setText(self.le_savename.text().strip())
        request_savename = self.le_savename.text()

        if not request_savename:
            QMessageBox.warning(self,"Savename missing", "The savename cannot be empty.", QMessageBox.Ok)
            return
    
        if request_savename in self.saved_request_data.keys():
            QMessageBox.warning(self,"Request savename used", "The exact savename was already used.", QMessageBox.Ok)
            return
        
        self.lw_saved_requests.addItem(request_savename)
        
        self.saved_request_data[request_savename] = self.recent_valid_request_data
        self.recent_valid_request_data = None
        self.le_savename.setText("")


    def load_request(self):
    
        selected_items = self.lw_saved_requests.selectedItems()
        
        if not selected_items:
            return
        
        selected_item_text = selected_items[0].text()

        saved_entry =  self.saved_request_data.get(selected_item_text)

        self.le_url.setText(saved_entry.get("url"))
        self.url_var_env_widget.set_env_state(saved_entry.get("url_env_state"))
        self.json_data_widget.set_json_data(saved_entry.get("json"))
        self.kv_params.set_complete_widget_state(saved_entry.get("params_state"))
        self.kv_headers.set_complete_widget_state(saved_entry.get("headers_state"))

    def delete_request(self):
       
        selected_items = self.lw_saved_requests.selectedItems()
        
        if not selected_items:
            return

        selected_item = selected_items[0]

        del self.saved_request_data[selected_item.text()]
        self.lw_saved_requests.takeItem(self.lw_saved_requests.row(selected_item))


    def edit_json_data(self):
     
        self.json_data_widget.show()

    def set_env_vars_and_show_widget(self):
        try:
            self.url_var_env_widget.set_env_vars(self.le_url)
        except Exception as e:
            QMessageBox.warning(self,type(e).__name__, str(e), QMessageBox.Ok)
            return
        
        self.url_var_env_widget.show()