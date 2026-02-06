from PySide6.QtWidgets import QWidget, QScrollArea, QLineEdit, QVBoxLayout, QHBoxLayout, QLabel, QApplication
from PySide6.QtCore import Qt

class URLValueWidget(QScrollArea):

    def __init__(self, parent=None, max_height=200):
        super().__init__()

        self.parent_widget = parent

        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.setWidgetResizable(True)
        self.setMinimumHeight(150)
        self.setMaximumHeight(max_height)
        self.setFixedWidth(350)
        self.sizeHint()

        self.env_key_list: list[QLabel] = []
        self.env_value_list: list[QLineEdit] = []

        self.container_widget = QWidget()
        self.v_list_layout = QVBoxLayout()
        self.v_list_layout.setAlignment(Qt.AlignTop)
        self.container_widget.setLayout(self.v_list_layout)

        self.setWidget(self.container_widget)

    def set_env_variables_list(self, env_vars_list:list[str]):
        self.delete_all_env_variables()

        for key in env_vars_list:
            new_env_key = QLabel()
            new_env_key.setText(key)
            #new_env_key.setAlignment(Qt.AlignRight)
            self.env_key_list.append(new_env_key)

            new_env_value = QLineEdit()
            new_env_value.setPlaceholderText("Value")
            self.env_value_list.append(new_env_value)

            h_layout = QHBoxLayout()
            h_layout.addWidget(new_env_key, 1)
            h_layout.addWidget(new_env_value, 1)

            self.v_list_layout.addLayout(h_layout)

    def delete_all_env_variables(self):
        env_variables_count = self.v_list_layout.count()

        #state_before_deletion = self.get_complete_widget_state()

        for i in range(env_variables_count-1, -1, -1):

            self._remove_env_variable_at_index(i)

        #return state_before_deletion

    def get_env_variables_state(self):
        env_variables_count = self.v_list_layout.count()

        output_list = []

        for i in range(env_variables_count):

            if self.env_value_list[i].text():
                self.env_value_list[i].setText(self.env_value_list[i].text().strip())

            output_list.append((self.env_key_list[i].text(), self.env_value_list[i].text()))

        return output_list
    
    def set_env_variables_state(self, state_list: list[tuple]):
        self.delete_all_env_variables()

        for key, value in state_list:
            new_env_key = QLabel()
            new_env_key.setText(key)
            #new_env_key.setAlignment(Qt.AlignRight)
            self.env_key_list.append(new_env_key)

            new_env_value = QLineEdit()
            new_env_value.setPlaceholderText("Value")
            new_env_value.setText(value)
            self.env_value_list.append(new_env_value)

            h_layout = QHBoxLayout()
            h_layout.addWidget(new_env_key, 1)
            h_layout.addWidget(new_env_value, 1)

            self.v_list_layout.addLayout(h_layout)


    def _remove_env_variable_at_index(self, index):

        self.env_key_list[index].deleteLater()
        self.env_value_list[index].deleteLater()

        del self.env_key_list[index]
        del self.env_value_list[index]

        self.v_list_layout.takeAt(index)

def main():
    app = QApplication()
    main = URLValueWidget()

    #main.set_env_variables_list(["user_id", "blog_id", "comment_id"])
    main.set_env_variables_state([("user_id", "12"), ("blog_id", "13"), ("comment_id", "salat")])
    main.set_env_variables_list(["jim", "john", "dieter"])

    main.show()
    print(main.get_env_variables_state())

    app.exec()
if __name__ == '__main__':
    main()