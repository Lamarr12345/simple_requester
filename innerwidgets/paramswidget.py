from PySide6.QtWidgets import QScrollArea, QLineEdit, QCheckBox, QVBoxLayout, QHBoxLayout, QPushButton,QApplication
from PySide6.QtCore import Qt

class KeyValueWidget(QScrollArea):

    def __init__(self, parent=None, kv_pairs=10):
        super().__init__(parent=parent)

        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.setWidgetResizable(True)
        self.setMaximumHeight(200)

        self.checkbox_list = []
        self.key_list = []
        self.value_list = []
        self.delete_button_list = []

        self.v_layout = QVBoxLayout()
        for i in range(kv_pairs):
            self.checkbox_list.append(QCheckBox())
            self.checkbox_list[i].setChecked(False)
            #self.checkbox_list[i].stateChanged.connect()

            self.key_list.append(QLineEdit())
            self.key_list[i].setPlaceholderText("Key")

            self.value_list.append(QLineEdit())
            self.value_list[i].setPlaceholderText("Value")

            self.delete_button_list.append(QPushButton("Del"))
            self.delete_button_list[i].clicked.connect(self.delete_kv_pair)

            h_layout = QHBoxLayout()
            h_layout.addWidget(self.checkbox_list[i])
            h_layout.addWidget(self.key_list[i])
            h_layout.addWidget(self.value_list[i])
            h_layout.addWidget(self.delete_button_list[i])

            self.v_layout.addLayout(h_layout)
        
        self.setLayout(self.v_layout)

    def add_kv_pair(self):
        new_checkbox = QCheckBox()
        self.checkbox_list.append(new_checkbox)
        new_checkbox.setChecked(False)
        #self.checkbox_list[i].stateChanged.connect()

        new_keybox = QLineEdit()
        self.key_list.append(new_keybox)
        new_keybox.setPlaceholderText("Key")

        new_valuebox = QLineEdit()
        self.value_list.append(new_valuebox)
        new_valuebox.setPlaceholderText("Value")

        new_delete_button = QPushButton("Del")
        self.delete_button_list.append(new_delete_button)
        new_delete_button.clicked.connect(self.delete_kv_pair)

        h_layout = QHBoxLayout()
        h_layout.addWidget(new_checkbox)
        h_layout.addWidget(new_keybox)
        h_layout.addWidget(new_valuebox)
        h_layout.addWidget(new_delete_button)

        self.v_layout.addLayout(h_layout)
        print(self.v_layout.count())

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

        self.v_layout.takeAt(del_index)






def main():
    app = QApplication()
    main = KeyValueWidget(kv_pairs=10)
    main.show()
    main.add_kv_pair()
    app.exec()
if __name__ == '__main__':
    main()


