from PySide6.QtWidgets import QMainWindow,QTabWidget

from requestwidgets.getwidget import GetWidget
from requestwidgets.postwidget import PostWidget
from requestwidgets.putwidget import PutWidget
from requestwidgets.patchwidget import PatchWidget
from requestwidgets.deletewidget import DeleteWidget
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
        self.put_widget = PutWidget(self)
        self.patch_widget = PatchWidget(self)
        self.delete_widget = DeleteWidget(self)

        self.tab_widget.addTab(self.get_widget,"GET request")
        self.tab_widget.addTab(self.post_widget,"POST request")
        self.tab_widget.addTab(self.put_widget,"PUT request")
        self.tab_widget.addTab(self.patch_widget,"PATCH request")
        self.tab_widget.addTab(self.delete_widget,"DELETE request")

        self.json_data_widget = None
        self.response_widget = None
        self.response_timeout = 5

        self.setCentralWidget(self.tab_widget)

        # window dimensions fixed
        self.resize(self.minimumSizeHint())
        self.setFixedSize(self.frameGeometry().width(), self.frameGeometry().height())
