from PySide6.QtWidgets import QApplication
import sys 
from mainwidgets.mainwidget import MainWidget
from mainwidgets.responsewidget import ResponseWidget

def main():
    app = QApplication(sys.argv)

    window = MainWidget(app)
    window.show()

    app.exec()

if __name__ == "__main__":
    main()