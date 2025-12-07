from PySide6.QtWidgets import QMainWindow,QTabWidget

from requestwidgets.getwidget import GetWidget
from requestwidgets.postwidget import PostWidget
# import requests
# import ast

# REQUEST_CHOISES = {
#     "GET": requests.get,
#     "POST": requests.post,
#     "PUT": requests.put,
#     "DELETE": requests.delete,
#     "PATCH": requests.patch,
#     "HEAD": requests.head,
#     "OPTIONS": requests.options,
# }

class MainWidget(QMainWindow):
    def __init__(self, app):
        super().__init__()

        self.setWindowTitle("Simple Requester")
        self.app = app 

        self.tab_widget = QTabWidget(self)

        self.get_widget = GetWidget(self)
        self.post_widget = PostWidget(self)

        self.tab_widget.addTab(self.get_widget,"GET request")
        self.tab_widget.addTab(self.post_widget,"POST request")

        self.response_widget = None

        self.setCentralWidget(self.tab_widget)
