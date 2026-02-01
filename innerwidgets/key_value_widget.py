from PySide6.QtWidgets import QWidget, QScrollArea, QLineEdit, QCheckBox, QVBoxLayout, QHBoxLayout, QPushButton,QApplication
from PySide6.QtCore import Qt

class KeyValueWidget(QScrollArea):

    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.setWidgetResizable(True)
        self.setMinimumHeight(120)

        self.checkbox_list = []
        self.key_list = []
        self.value_list = []
        self.delete_button_list = []

        button_add_vk_pair = QPushButton("Add New")
        button_add_vk_pair.clicked.connect(self.add_kv_pair)

        self.container_widget = QWidget()
        self.v_list_layout = QVBoxLayout()
        self.v_list_layout.setAlignment(Qt.AlignTop)
        self.container_widget.setLayout(self.v_list_layout)

        v_main_layout = QVBoxLayout()
        v_main_layout.addWidget(self.container_widget)
        v_main_layout.addWidget(button_add_vk_pair)

        self.setWidget(self.container_widget)

    def add_kv_pair(self):
        new_checkbox = QCheckBox()
        new_checkbox.setChecked(False)
        #self.checkbox_list[i].stateChanged.connect()
        self.checkbox_list.append(new_checkbox)

        new_keybox = QLineEdit()
        new_keybox.setPlaceholderText("Key")
        self.key_list.append(new_keybox)

        new_valuebox = QLineEdit()
        new_valuebox.setPlaceholderText("Value")
        self.value_list.append(new_valuebox)

        new_delete_button = QPushButton("Del")
        new_delete_button.clicked.connect(self.delete_kv_pair)
        self.delete_button_list.append(new_delete_button)

        h_layout = QHBoxLayout()
        h_layout.addWidget(new_checkbox)
        h_layout.addWidget(new_keybox)
        h_layout.addWidget(new_valuebox)
        h_layout.addWidget(new_delete_button)

        self.v_list_layout.addLayout(h_layout)

        print(self.v_list_layout.count())

    def delete_kv_pair(self):
        del_index = self.delete_button_list.index(self.sender())

        self.checkbox_list[del_index].deleteLater()
        self.key_list[del_index].deleteLater()
        self.value_list[del_index].deleteLater()
        self.delete_button_list[del_index].deleteLater()

        del self.checkbox_list[del_index]
        del self.key_list[del_index]
        del self.value_list[del_index]
        del self.delete_button_list[del_index]

        self.v_list_layout.takeAt(del_index)






def main():
    app = QApplication()
    main = KeyValueWidget()
    main.show()
    app.exec()
  
if __name__ == '__main__':
    main()


