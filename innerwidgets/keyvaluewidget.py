from PySide6.QtWidgets import QWidget, QScrollArea, QLineEdit, QCheckBox, QVBoxLayout, QHBoxLayout, QPushButton, QMessageBox, QApplication
from PySide6.QtCore import Qt

class KeyValueWidget(QScrollArea):

    def __init__(self, parent=None, height=150):
        super().__init__()

        self.parent_widget = parent

        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.setWidgetResizable(True)
        self.setMinimumHeight(1)
        self.setFixedHeight(height)
        self.setFixedWidth(350)
        self.sizeHint()

        self.checkbox_list: list[QCheckBox] = []
        self.key_list: list[QLineEdit] = []
        self.value_list: list[QLineEdit] = []
        self.delete_button_list: list[QPushButton] = []

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
        new_valuebox.text()
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


    def delete_kv_pair(self):
        del_index = self.delete_button_list.index(self.sender())

        self._remove_kv_pair_at_index(del_index)

    def delete_all_kv_pair(self):
        kv_pair_count = self.v_list_layout.count()

        #state_before_deletion = self.get_complete_widget_state()

        for i in range(kv_pair_count-1, -1, -1):

            self._remove_kv_pair_at_index(i)

        #return state_before_deletion

    def get_valid_kv_list(self):
        kv_pair_count = self.v_list_layout.count()

        output_list = []

        for i in range(kv_pair_count):

            self._strip_kv_pair_at_index(i)

            if self.checkbox_list[i].isChecked() and self.key_list[i].text():
                output_list.append((self.key_list[i].text(), self.value_list[i].text()))

        return output_list
    
    def get_complete_widget_state(self):
        kv_pair_count = self.v_list_layout.count()

        output_list = []

        for i in range(kv_pair_count):
            
            self._strip_kv_pair_at_index(i)
            
            output_list.append(
                {
                    "is_checked": self.checkbox_list[i].isChecked(),
                    "key": self.key_list[i].text(),
                    "value": self.value_list[i].text()
                }
            )

        return output_list

    def set_complete_widget_state(self, state_list:list[dict]):
        self.delete_all_kv_pair()

        for i in range(len(state_list)):
            self.add_kv_pair()

            self.checkbox_list[i].setChecked(state_list[i].get("is_checked"))
            self.key_list[i].setText(state_list[i].get("key"))
            self.value_list[i].setText(state_list[i].get("value"))


    def _remove_kv_pair_at_index(self, index):

        self.checkbox_list[index].deleteLater()
        self.key_list[index].deleteLater()
        self.value_list[index].deleteLater()
        self.delete_button_list[index].deleteLater()

        del self.checkbox_list[index]
        del self.key_list[index]
        del self.value_list[index]
        del self.delete_button_list[index]

        self.v_list_layout.takeAt(index)

    def _strip_kv_pair_at_index(self, index):

        if self.key_list[index].text():
            self.key_list[index].setText(self.key_list[index].text().strip())
        if self.value_list[index].text():
            self.value_list[index].setText(self.value_list[index].text().strip())