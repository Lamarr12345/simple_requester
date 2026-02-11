from PySide6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QFileDialog, QPushButton, QLabel, QMessageBox
from PySide6.QtCore import Qt
from pathlib import Path
import json

from requestwidgets.generalrequestwidget import GeneralRequestWidget
from requestwidgets.getwidget import GetWidget

SAVE_FILE_EXTENSION = ".srsf"

class SaveLoadWidget(QWidget):
    def __init__(self,
                 parent,
                 getwidget: GetWidget,
                 postwidget: GeneralRequestWidget,
                 putwidget: GeneralRequestWidget,
                 patchwidget: GeneralRequestWidget,
                 deletewidget: GeneralRequestWidget):
        super().__init__(parent=parent)

        self.getwidget = getwidget
        self.postwidget = postwidget
        self.putwidget = putwidget
        self.patchwidget = patchwidget
        self.deletewidget = deletewidget

        label_test = QLabel("This is for testing save and load functionallity")
        button_save = QPushButton("Save Requests")
        button_save.clicked.connect(self.save_requests)
        button_load = QPushButton("Load Requests")
        button_load.clicked.connect(self.load_requests)

        h_sl_buttons_layout = QHBoxLayout()
        h_sl_buttons_layout.addWidget(button_save)
        h_sl_buttons_layout.addWidget(button_load)

        v_sl_layout = QVBoxLayout()
        v_sl_layout.setAlignment(Qt.AlignTop|Qt.AlignLeft)
        v_sl_layout.addWidget(label_test)
        v_sl_layout.addLayout(h_sl_buttons_layout)

        self.setLayout(v_sl_layout)

    def save_requests(self):
        file_dialog = QFileDialog(self)
        file_dialog.setDefaultSuffix(SAVE_FILE_EXTENSION)
        file_dialog.setWindowTitle("Save File")
        file_dialog.setAcceptMode(QFileDialog.AcceptMode.AcceptSave)
        file_dialog.setNameFilter(f"Save Files (*{SAVE_FILE_EXTENSION})")
        file_dialog.setViewMode(QFileDialog.ViewMode.Detail)

        selected_files = None
        if file_dialog.exec():
            selected_files = file_dialog.selectedFiles()
        
        if not selected_files:
            return

        # if not selected_files:
        #     QMessageBox.warning(self, "File Error", "No file has been selected.", QMessageBox.Ok)
        #     return

        # if len(selected_files) > 1:
        #     QMessageBox.warning(self, "File Error", "Please only select 1 file.", QMessageBox.Ok)
        #     return
        
        selected_file = selected_files[0]

        if not selected_file.endswith(SAVE_FILE_EXTENSION):
            selected_file = selected_file + SAVE_FILE_EXTENSION

        save_data = {}
        save_data["getrequests"] = self.getwidget.get_widget_state()
        save_data["postrequests"] = self.postwidget.get_widget_state()
        save_data["putrequests"] = self.putwidget.get_widget_state()
        save_data["patchrequests"] = self.patchwidget.get_widget_state()
        save_data["deleterequests"] = self.deletewidget.get_widget_state()

        with open(selected_file, 'w') as save_file:
            json.dump(save_data, save_file)
    

    def load_requests(self):
        file_dialog = QFileDialog(self)
        file_dialog.setWindowTitle("Load File")
        file_dialog.setFileMode(QFileDialog.FileMode.ExistingFile)
        file_dialog.setNameFilter(f"Save Files (*{SAVE_FILE_EXTENSION})")
        file_dialog.setViewMode(QFileDialog.ViewMode.Detail)

        selected_files = None
        if file_dialog.exec():
            selected_files = file_dialog.selectedFiles()
        
        if not selected_files:
            return
        
        selected_file = selected_files[0]

        with open(selected_file, 'r') as save_file:
            save_data = json.load(save_file)

        getwidget_cache = self.getwidget.get_widget_state()
        postwidget_cache = self.postwidget.get_widget_state()
        putwidget_cache = self.putwidget.get_widget_state()
        patchwidget_cache = self.patchwidget.get_widget_state()
        deletewidget_cache = self.deletewidget.get_widget_state()

        try:
            self.getwidget.set_widget_state(save_data["getrequests"])
            self.postwidget.set_widget_state(save_data["postrequests"])
            self.putwidget.set_widget_state(save_data["putrequests"])
            self.patchwidget.set_widget_state(save_data["patchrequests"])
            self.deletewidget.set_widget_state(save_data["deleterequests"])
        except:
            self.getwidget.set_widget_state(getwidget_cache)
            self.postwidget.set_widget_state(postwidget_cache)
            self.putwidget.set_widget_state(putwidget_cache)
            self.patchwidget.set_widget_state(patchwidget_cache)
            self.deletewidget.set_widget_state(deletewidget_cache)

            QMessageBox.warning(self, "File Error", "File could not be loaded.", QMessageBox.Ok)
            return

