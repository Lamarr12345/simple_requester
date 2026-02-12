from PySide6.QtWidgets import QWidget, QLabel, QLineEdit, QListWidget, QPushButton, QHBoxLayout, QVBoxLayout,QMessageBox
from PySide6.QtCore import Qt
import requests
import re

from mainwidgets.responsewidget import ResponseWidget
from innerwidgets.keyvaluewidget import KeyValueWidget
from datawidgets.urlenviromentvariableswidget import URLEnviromentVariablesWidget
from innerwidgets.lineeditwithsyntaxhighlight import LineEditWithSyntaxHighlight

class GetWidget(QWidget):
    """
    A specialized widget for configuring and executing HTTP GET requests with a graphical interface.
    
    This widget provides a user interface to configure and send HTTP  GET requests with support for
    parameters, headers and request persistence.
    
    Features:
    - URL input with validation
    - Key-value parameter management
    - Custom header configuration
    - JSON data editor
    - Request history and persistence
    - Response display integration
    
    Attributes:
        main_widget (QWidget): Parent widget that contains this component.
        recent_valid_request_data (dict or None): Cached data from the most recent successful request.
        saved_request_data (dict): Dictionary storing saved request configurations keyed by name.
        le_url (QLineEdit): Input field for the target URL.
        kv_params (KeyValueWidget): Widget for managing query parameters.
        kv_headers (KeyValueWidget): Widget for managing HTTP headers.
        le_savename (QLineEdit): Input field for naming saved requests.
        lw_saved_requests (QListWidget): List displaying saved request names.
    
    Args:
        parent (QWidget): The parent widget that contains this request widget.
        method (str): The HTTP method this widget will use for requests.
    """
    def __init__(self, parent):
        """
        Initialize the GetWidget.
        
        Args:
            parent (QWidget): The parent widget that contains this request widget.
        """
        super().__init__()

        self.main_widget = parent
        self.recent_valid_request_data = None
        self.saved_request_data = {}
        self.url_var_env_widget = URLEnviromentVariablesWidget(self, self.main_widget)

        # URL Section
        label_url = QLabel("URL:")
        self.le_url = LineEditWithSyntaxHighlight(self)
        self.le_url.textEdited.connect(self.highlight_env_vars)
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
        """
        Execute an HTTP request with the configured parameters.
        
        This method:
        1. Validates and trims the URL input
        3. Sends the HTTP request with configured parameters and headers
        4. Displays any validation or network errors in message boxes
        5. Creates a ResponseWidget to display the response
        6. Caches the successful request configuration for potential saving
        
        Raises:
            Shows QMessageBox for:
                - Network request errors (timeout, connection issues, etc.)
                - Invalid URLs or malformed request configurations
        """
        self.le_url.setText(self.le_url.text().strip())
        url = self.le_url.text()

        if not self.url_var_env_widget.is_var_env_valid(self.le_url):
            QMessageBox.critical(self, "Var Env Error","The current variable enviroment is not matching the URL anymore.", QMessageBox.Ok)
            return
        
        if self.url_var_env_widget.is_env_set():
            try:
                url = self.url_var_env_widget.get_modified_url(self.le_url)
            except Exception as e:
                QMessageBox.critical(self, type(e).__name__, str(e), QMessageBox.Ok)
                return

        
        try:
            response = requests.get(url=url,
                                    params=self.kv_params.get_valid_kv_list(),
                                    headers=self.kv_headers.get_valid_kv_dict(),
                                    timeout=self.main_widget.response_timeout)
        except Exception as e:
            QMessageBox.critical(self,type(e).__name__, str(e), QMessageBox.Ok)
            return

        self.main_widget.response_widget = ResponseWidget(response)
        self._cache_recent_valid_request_data()

    def _cache_recent_valid_request_data(self):
        """
        Cache the current request configuration after a successful request.
        
        Stores the complete state of the request widget including:
            - URL
            - Parameters widget state
            - Headers widget state
        
        This cached data can be later saved using the save_request() method.
        """
        self.recent_valid_request_data = {
            "url": self.le_url.text(),
            "url_env_state": self.url_var_env_widget.get_env_state(),
            "params_state": self.kv_params.get_complete_widget_state(),
            "headers_state": self.kv_headers.get_complete_widget_state(),
        }

    def clear_data(self):
        """
        Reset all input fields and configurations to their default empty state.
        
        Clears:
            - URL input field
            - All parameter key-value pairs
            - All header key-value pairs
        """
        self.le_url.clear()
        self.kv_params.delete_all_kv_pair()
        self.kv_headers.delete_all_kv_pair()
        self.url_var_env_widget.clear_env_vars()

    def clear_save_data(self):
        save_count = self.lw_saved_requests.count()

        for i in range(save_count-1, -1, -1):
            entry_name = self.lw_saved_requests.item(i).text()
            del self.saved_request_data[entry_name]
            self.lw_saved_requests.takeItem(i)

        self.le_savename.clear()
            

    def save_request(self):
        """
        Save the most recent successful request configuration.
        
        This method:
        1. Validates that there is recent valid request data to save
        2. Validates and trims the save name input
        3. Ensures the save name is not empty
        4. Checks for duplicate save names
        5. Stores the request configuration in saved_request_data dictionary
        6. Adds the save name to the saved requests list widget
        7. Clears the recent valid request data cache and save name input
        
        Raises:
            Shows QMessageBox for:
                - No recent valid request data
                - Empty save name
                - Duplicate save name
        """
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
        """
        Load a previously saved request configuration.
        
        This method:
        1. Checks if a saved request is selected in the list widget
        2. Retrieves the saved configuration from saved_request_data
        3. Populates all input fields with the saved configuration
        4. Restores the url, parameters, and headers to their saved state
        
        If no request is selected, the method returns without making any changes.
        """
        selected_items = self.lw_saved_requests.selectedItems()
        
        if not selected_items:
            return
        
        selected_item_text = selected_items[0].text()

        saved_entry =  self.saved_request_data.get(selected_item_text)

        self.le_url.setText(saved_entry.get("url"))
        self.url_var_env_widget.set_env_state(saved_entry.get("url_env_state"))
        self.kv_params.set_complete_widget_state(saved_entry.get("params_state"))
        self.kv_headers.set_complete_widget_state(saved_entry.get("headers_state"))

    def delete_request(self):
        """
        Delete a saved request configuration.
        
        This method:
        1. Checks if a saved request is selected in the list widget
        2. Removes the configuration from the saved_request_data dictionary
        3. Removes the item from the saved requests list widget
        
        If no request is selected, the method returns without making any changes.
        
        Note: This action cannot be undone.
        """
        selected_items = self.lw_saved_requests.selectedItems()
        
        if not selected_items:
            return

        selected_item = selected_items[0]

        del self.saved_request_data[selected_item.text()]
        self.lw_saved_requests.takeItem(self.lw_saved_requests.row(selected_item))

    def set_env_vars_and_show_widget(self):
        try:
            self.url_var_env_widget.set_env_vars(self.le_url)
        except Exception as e:
            QMessageBox.warning(self,type(e).__name__, str(e), QMessageBox.Ok)
            return
        
        self.url_var_env_widget.show()

    def get_widget_state(self):

        return self.saved_request_data
    
    def set_widget_state(self, widget_state: dict):
        self.clear_data()
        self.clear_save_data()

        self.saved_request_data = widget_state

        for key in widget_state.keys():
            self.lw_saved_requests.addItem(key)

    def highlight_env_vars(self):
        url = self.le_url.text()

        pattern = r"(?![^\{])\{\{[ ]*[^ \{\}]+?[ ]*\}\}"
        env_vars = re.finditer(pattern, url)

        if env_vars:
            env_var_indices = [(env_var.start(), env_var.end()) for env_var in env_vars]
            self.le_url.highlight_text_by_index_span(env_var_indices)
        

