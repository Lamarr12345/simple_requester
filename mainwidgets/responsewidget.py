from PySide6.QtWidgets import QWidget,QLineEdit,QTextEdit, QLabel, QVBoxLayout, QHBoxLayout, QSplitter, QTabWidget
from PySide6.QtCore import Qt
from requests import Response
from bs4 import BeautifulSoup

class ResponseWidget(QWidget):
    def __init__(self, response: Response):
        super().__init__()

        self.response = response

        self.setWindowTitle("Response Details")

        label_status = QLabel("Status")
        self.le_status = QLineEdit(self)
        self.le_status.setReadOnly(True)
        
        label_headers = QLabel("Headers")
        self.te_headers = QTextEdit(self)
        self.te_headers.setReadOnly(True)

        self.te_html_content = QTextEdit(self)
        self.te_html_content.setReadOnly(True)

        self.te_raw_content = QTextEdit(self)
        self.te_raw_content.setReadOnly(True)
        self.te_raw_content.setAutoFormatting(QTextEdit.AutoNone)

        v_status_headers_layout = QVBoxLayout()
        v_status_headers_layout.addWidget(label_status)
        v_status_headers_layout.addWidget(self.le_status)
        v_status_headers_layout.addWidget(label_headers)
        v_status_headers_layout.addWidget(self.te_headers)
        status_header_widget = QWidget()
        status_header_widget.setLayout(v_status_headers_layout)

        v_raw_content_layout = QVBoxLayout()
        v_raw_content_layout.addWidget(self.te_raw_content)
        raw_content_widget = QWidget()
        raw_content_widget.setLayout(v_raw_content_layout)
        v_html_content_layout = QVBoxLayout()
        v_html_content_layout.addWidget(self.te_html_content)
        html_content_widget = QWidget()
        html_content_widget.setLayout(v_html_content_layout)

        tab_content = QTabWidget(self)
        tab_content.addTab(raw_content_widget, "raw")
        tab_content.addTab(html_content_widget, "HTML")

        splitter = QSplitter(Qt.Orientation.Horizontal)
        splitter.addWidget(status_header_widget)
        splitter.addWidget(tab_content)

        h_base_layout = QHBoxLayout()
        h_base_layout.addWidget(splitter)

        self.setLayout(h_base_layout)

        self.load_response_data()

        self.show()

    def load_response_data(self):
        soup = BeautifulSoup(self.response.content, "html.parser")
        html_text_string = soup.prettify()
        
        status_text = f"{self.response.status_code} : {self.response.reason}"
        self.le_status.setText(status_text)

        header_text = ""
        for key, value in self.response.headers.items():
            header_text += f"{key} : {value}\n\n"
        self.te_headers.setPlainText(header_text)

        self.te_html_content.setHtml(html_text_string)
        self.te_raw_content.setPlainText(html_text_string)

