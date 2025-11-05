from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QRadioButton, QSlider, \
    QHBoxLayout
from PyQt5.QtWidgets import QWidget, QCheckBox

from PyQt5.QtCore import Qt

class MAIN(QMainWindow):
    def __init__(self):
        super().__init__()

        self.checkbox = QCheckBox("check")
        self.radio = QRadioButton("radio1")
        self.radio2 = QRadioButton("radio2")
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setRange(1,5)

        self.label_slider= QLabel("1")

        self.label_slider.setMaximumHeight(50)
        layout = QVBoxLayout()
        layout2 = QHBoxLayout()
        layout2.addWidget(self.slider)
        layout2.addWidget(self.label_slider)

        layout.addWidget(self.checkbox)
        layout.addWidget(self.radio)
        layout.addWidget(self.radio2)
        layout.addLayout(layout2)
        con = QWidget()
        con.setLayout(layout)
        self.setCentralWidget(con)
        self.setGeometry(300, 300, 500, 400)
        self.checkbox.clicked.connect(self._cb)
        self.radio.clicked.connect(self._rad)
        self.radio2.clicked.connect(self._rad)
        self.slider.valueChanged.connect(self._pp)


    def _cb(self):
        print(f"CheckBox is {self.checkbox.isChecked()}")
    def _rad(self):
        sen = self.sender()
        print(f"Radio({sen.text()}) is {sen.isChecked()}")
    def _pp(self,value):
        print(f"Position is {value}")
        self.label_slider.setText(str(value))






app = QApplication([])
win = MAIN()
win.show()

app.exec()