from PyQt5.QtWidgets import QLabel, QAction, QWidget, QMainWindow, QPushButton, QVBoxLayout, QMessageBox, QFileDialog
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import *
from datetime import datetime
from fbs_runtime.application_context.PyQt5 import ApplicationContext
import main_area
import sys
import os
import configparser





# def run(filename):
#     msg = QMessageBox()
#     msg.setWindowTitle("Finished!")
#     if len(filename)==1:
#         results = main_area.results(filename[0])
#         msg.setText(results)
#         msg.setTextInteractionFlags(Qt.TextSelectableByMouse)
#         msg.exec_()
#         main_area.get_plot(filename[0])
#
#     elif len(filename)>1:
#         now = datetime.now()
#         window.config.read('{}/ramanizator.conf'.format(window.ramandir))
#         savepath = window.config['main']['savepath']
#
#         res = '{}\\results_{}.csv'.format(savepath, now.strftime('%m_%d_%Y'))
#         with open(res,'w') as f:
#             for elem in filename:
#                 results = main_area.results(elem)
#                 file = elem.split('/')[-1]
#                 f.write('Results for {}\n'.format(file))
#                 splitted = results.split('\n')[1:]
#                 for spl in splitted:
#                     f.write(spl.replace(':',',')+'\n')
#
#
#         f.close()
#         msg.setText('Results saved in {}'.format(res))
#         msg.exec_()
#     return 0

def openfile():
    dlg = QFileDialog()
    dlg.setFileMode(QFileDialog.ExistingFile)
    dlg.setNameFilter("CSV files *.csv")

    if dlg.exec_():
        filename = dlg.selectedFiles()

    if filename:
        msg = QMessageBox()
        msg.setWindowTitle("Finished!")
        results = main_area.results(filename[0])
        msg.setText(results)
        msg.setTextInteractionFlags(Qt.TextSelectableByMouse)
        msg.exec_()
        main_area.get_plot(filename[0])

def multiplefiles():
    msg = QMessageBox()
    dlg = QFileDialog()
    dlg.setFileMode(QFileDialog.ExistingFiles)
    dlg.setNameFilter("CSV files *.csv")

    if dlg.exec_():
        filename = dlg.selectedFiles()

    if filename:
        now = datetime.now()
        try:
            window.config.read('{}/ramanizator.conf'.format(window.ramandir))
        except:
            msg.setWindowTitle("Error!")
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Can't find save path!\nRamanizator config file not found!")
            msg.exec_()

        savepath = window.config['main']['savepath']

        res = '{}\\results_{}.csv'.format(savepath, now.strftime('%m_%d_%Y'))
        with open(res, 'w') as f:
            for elem in filename:
                results = main_area.results(elem)
                file = elem.split('/')[-1]
                f.write('Results for {}\n'.format(file))
                splitted = results.split('\n')[1:]
                for spl in splitted:
                    f.write(spl.replace(':', ',') + '\n')

    msg.setText('Results saved in {}'.format(res))
    msg.exec_()


class MainWindow(QMainWindow):


    def __init__(self):
        self.config = configparser.ConfigParser()
        super(MainWindow, self).__init__()
        self.settings = QSettings('Wroclaw University of Science and Technology', 'Raman Automizer')
        self.setWindowTitle('Raman Automizer')
        self.setFixedSize(350, 300)
        self.widget = MainWidget()
        self.setCentralWidget(self.widget)
        menubar = self.menuBar()
        setmenu = menubar.addMenu('Settings')
        self.ramandir = os.path.dirname(os.path.realpath(__file__))
        if not os.path.isfile('{}/ramanizator.conf'.format(self.ramandir)):
            with open('{}/ramanizator.conf'.format(self.ramandir), 'w') as conf:
                self.config['main'] = {'savepath':self.ramandir}
                self.config.write(conf)
                conf.close()

        path = QAction('Set save path', self, triggered=self.change_savepath)
        setmenu.addAction(path)
        self.settings.setValue('path', path)


    def change_savepath(self):
        path = QFileDialog.getExistingDirectory()
        if len(path)>1:
            with open('{}/ramanizator.conf'.format(self.ramandir), 'w') as conf:
                self.config['main'] = {'savepath': path}
                self.config.write(conf)
                conf.close()





class MainWidget(QWidget):


    def __init__(self):
        super(MainWidget, self).__init__()
        self.pixmap = QPixmap(appctxt.get_resource('title.png'))
        self.label = QLabel()
        self.label.setPixmap(self.pixmap)
        self.label.setAlignment(Qt.AlignCenter)
        self.label2 = QLabel()
        self.label2.setText('Made by Maciej Pawelski\n@ Wroclaw University of Technology')
        self.label2.setAlignment(Qt.AlignCenter)
        self.layout = QVBoxLayout(self)
        self.button = QPushButton('Single analysis')
        self.button2 = QPushButton('Multiple analysis')
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.label2)
        self.layout.addWidget(self.button)
        self.layout.addWidget(self.button2)
        self.button.clicked.connect(openfile)
        self.button2.clicked.connect(multiplefiles)



if __name__=='__main__':
    appctxt = ApplicationContext()
    window = MainWindow()
    window.show()
    sys.exit(appctxt.app.exec_())

