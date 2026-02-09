from PySide6.QtWidgets import QMainWindow,QTabWidget

from requestwidgets.getwidget import GetWidget
from requestwidgets.generalrequestwidget import GeneralRequestWidget
from managementwidgets.saveloadwidget import SaveLoadWidget

class MainWidget(QMainWindow):
    def __init__(self, app):
        super().__init__()

        self.setWindowTitle("Simple Requester")
        self.app = app 

        tab_widget = QTabWidget(self)

        get_widget = GetWidget(self)
        post_widget = GeneralRequestWidget(self, "POST")
        put_widget = GeneralRequestWidget(self, "PUT")
        patch_widget = GeneralRequestWidget(self, "PATCH")
        delete_widget = GeneralRequestWidget(self, "DELETE")
        save_load_widget = SaveLoadWidget(self,
                                          get_widget,
                                          post_widget,
                                          put_widget,
                                          patch_widget,
                                          delete_widget)

        tab_widget.addTab(get_widget,"GET request")
        tab_widget.addTab(post_widget,"POST request")
        tab_widget.addTab(put_widget,"PUT request")
        tab_widget.addTab(patch_widget,"PATCH request")
        tab_widget.addTab(delete_widget,"DELETE request")
        tab_widget.addTab(save_load_widget, "Save/Load State")

        self.json_data_widget = None
        self.response_widget = None
        self.response_timeout = 5

        self.setCentralWidget(tab_widget)

        # window dimensions fixed
        self.resize(self.minimumSizeHint())
        self.setFixedSize(self.frameGeometry().width(), self.frameGeometry().height())
