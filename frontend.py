import sys
from PyQt6.QtWidgets import (
    QApplication,    
    QVBoxLayout,
    QSlider,
    QSpinBox,
    QWidget,
    QMainWindow,
)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self = AuthorizeWindow() 


class AuthorizeWindow(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        layout.addWidget(QSlider())
        layout.addWidget(QSpinBox())
        self.setLayout(layout)


app = QApplication([])
window = AuthorizeWindow()
window.show()

app.exec()
