from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton,  QLabel, QVBoxLayout
from PyQt5.QtWidgets import QWidget, QMessageBox



class MAIN(QMainWindow):
    def _Mesblock(self):
        mess = QMessageBox(self)
        mess.addButton("100%", QMessageBox.AcceptRole)
        mess.addButton("Конечно, нет", QMessageBox.RejectRole)
        mess.setText("Хотите закрыть диалоговое окно?")
        mess.setWindowTitle("Диалог")
        mess.exec()
        self.label.setText(mess.clickedButton().text())


    def __init__(self):
        super().__init__()
        self.label = QLabel()
        self.button = QPushButton("Нажми")
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.button)
        self.button.setFixedHeight(100)
        con = QWidget()
        con.setLayout(layout)
        self.setCentralWidget(con)
        self.button.clicked.connect(self._Mesblock)
        self.setGeometry(300, 300, 500, 400)


app = QApplication([])
win = MAIN()
win.show()

app.exec()