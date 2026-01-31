from PySide6.QtWidgets import (QWidget, QSlider, QLineEdit, QLabel, QPushButton, QScrollArea,QApplication,
                             QHBoxLayout, QVBoxLayout, QMainWindow, QFrame, QCheckBox)
from PySide6.QtCore import Qt, QSize, Signal, Slot
pyqtSignal = Signal
pyqtSlot = Slot
import sys
class ListContainer(QScrollArea):
    changeItem=pyqtSignal(list)
    def __init__(self,items=None, parent=None):
        super().__init__(parent)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.setWidgetResizable(True)
        self.listItem=items
        if self.listItem==None:
            self.listItem=[0]*20
        self.listState=[False]*len(self.listItem)
        self.itemChk=[]
        self.initUI()
        
    def initUI(self):
        container=QWidget()
        self.setWidget(container)
        layout = QVBoxLayout(container)
        
        for i,s in enumerate(self.listItem):
            self.itemChk.append(QCheckBox(f"Object {i}"))
            self.itemChk[i].setChecked(False)
            self.itemChk[i].stateChanged.connect(self.changeChk)
           
            layout.addWidget(self.itemChk[i])
    
    def changeChk(self,state):
        print("{} : {}".format(self.sender().text(),True if state else False))
        for i,s in enumerate(self.itemChk):
            if s.text() == self.sender().text():
                self.listState[i]=True if state else False
        self.changeItem.emit(self.listState)
                
def main():
    app = QApplication(sys.argv)
    main = ListContainer()
    main.show()
    sys.exit(app.exec())
if __name__ == '__main__':
    main()