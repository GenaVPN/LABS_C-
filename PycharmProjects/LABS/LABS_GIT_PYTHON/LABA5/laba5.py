from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLineEdit, QLabel, QVBoxLayout
from PyQt5.QtWidgets import QWidget



class MAIN(QMainWindow):
    def __init__(self):
        super().__init__()
        lay = QVBoxLayout()
        self.Label = QLabel()
        self.line = QLineEdit()
        self.button = QPushButton("Нажми")
        lay.addWidget(self.line)
        lay.addWidget(self.Label)
        lay.addWidget(self.button)
        self.Label.setFixedHeight(50)
        self.button.setFixedHeight(100)
        con = QWidget()
        con.setLayout(lay)
        self.setCentralWidget(con)
        self.button.clicked.connect(self.clickk)
        self.setGeometry(300, 300, 500, 400)
    def clickk(self):
        self.Label.setText(self.line.text())


app = QApplication([])
win = MAIN()
win.show()
win.hide()

app.exec()