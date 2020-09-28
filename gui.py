from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QPushButton, QVBoxLayout, QMessageBox, QFileDialog
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import *
import main_area

app = QApplication([])
window = QWidget()
layout = QVBoxLayout()
button = QPushButton('Open CSV file')
cpbut = QPushButton('Copy to clipboard')



def openfile():
    dlg = QFileDialog()
    dlg.setFileMode(QFileDialog.AnyFile)
    dlg.setNameFilter("CSV files *.csv")
    if dlg.exec_():
        filename = dlg.selectedFiles()[0]
    else:
        return None
    return filename



def run():
    filename = openfile()
    if filename:
        results = main_area.results(filename)
        label2.setText(results)
        label2.setTextInteractionFlags(Qt.TextSelectableByMouse)
        main_area.get_plot(filename)




button.clicked.connect(run)

label1 = QLabel()
label2 = QLabel()
label2.setText('Made by Maciej Pawelski\n@ Wroclaw University of Technology')
layout.addWidget(label1)
layout.addWidget(label2)
layout.addWidget(button)
pixmap = QPixmap('title.png')
label1.setPixmap(pixmap)
label1.setAlignment(Qt.AlignCenter)
label2.setAlignment(Qt.AlignCenter)
window.setFixedSize(310,260)
window.setLayout(layout)
window.setWindowTitle('Raman Analysis Automizer')

window.show()
app.exec_()

