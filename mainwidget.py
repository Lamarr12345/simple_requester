from PySide6.QtWidgets import QMainWindow,QTabWidget

from requestwidgets.getwidget import GetWidget
from requestwidgets.generalrequestwidget import GeneralRequestWidget

class MainWidget(QMainWindow):
    def __init__(self, app):
        super().__init__()

        self.setWindowTitle("Simple Requester")
        self.app = app 

        self.tab_widget = QTabWidget(self)

        self.get_widget = GetWidget(self)
        self.post_widget = GeneralRequestWidget(self, "POST")
        self.put_widget = GeneralRequestWidget(self, "PUT")
        self.patch_widget = GeneralRequestWidget(self, "PATCH")
        self.delete_widget = GeneralRequestWidget(self, "DELETE")

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
