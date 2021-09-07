#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fileencoding=utf-8

from MonoX_FileOperation import FileOperation
from pathlib import Path
import sys
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import (QWidget, QPushButton, QLineEdit,
    QInputDialog, QApplication, QFileDialog, QMessageBox, QHBoxLayout, 
    QLabel)

class MainWindow(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):

        self.setAcceptDrops(True)
        self.btnOpnFile = QPushButton('Open File', self)
        self.btnOpnFile.move(60, 270)
        self.btnOpnFile.clicked.connect(self.openFile)

        self.btnInfo = QPushButton('Information', self)
        self.btnInfo.move(60, 300)
        self.btnInfo.clicked.connect(self.infoBox)

        lbl = QLabel(self)
        pixmap = QPixmap("MonoX_img.png")

        lbl.setPixmap(pixmap)
        lbl.move(10,10)
        
        self.setGeometry(300, 300, 200, 350)
        self.setWindowTitle('Fix Bottom Layers on MonoX')

        self.show()

    def showDialog(self):

        text, ok = QInputDialog.getText(self, 'Input Dialog', 'Здарова ебать!:')

        if ok:
            self.le.setText(str(text))

        self.infoBox()
    
    def openFile(self):
        fileDialog = QFileDialog()
        fileDialog.setDefaultSuffix(".pwmx")
        fileName = fileDialog.getOpenFileName(None, "Open Photon Workshop Mono X File", "", "Photon Mono X (*.pwmx)")[0]
        if not fileName:
            return

        print(fileName)
        try:
            doFile = FileOperation(fileName)
            newFilename = doFile.automaticWork()
        except Exception as e:
            errBox = QMessageBox()
            errBox.setWindowTitle('Error')
            errBox.setText('Error: ' + str(e))
            errBox.addButton(QMessageBox.Ok)
            errBox.exec()
            return
        else:
            errBox = QMessageBox()
            errBox.setWindowTitle('Complete')
            errBox.setText('File \'' + newFilename + '\' is writing')
            errBox.addButton(QMessageBox.Ok)
            errBox.exec()

    def infoBox(self):
        infBox = QMessageBox()
        infBox.setWindowTitle('Info')
        
        infBox.setText(' Push the \'Open File\' button and choose Photon Workshop MonoX file.' + \
                        '\r\n Then app generate new file with addition in name \'FixBL_\' '+ \
                        'in directory of original pwmx file with fixing of bottom layers. ' + \
                        '\r\n\n You can support the author on paypal n.s.shadrin@gmail.com or' +\
                        'on the bank card 5469 6800 8309 2725' + \

                        '\r\n\n\n Щелкните на кнопку \'Open File\' и выберете файл Photon Workshop MonoX.' +\
                        '\r\n Приложение сгенерирует новый файл с префиксом \'FixBL_\' в директории '+\
                        'оригинального файла pwmx с исправленными стартовыми слоями.'+\
                        '\r\n\n Вы можете поддержать автора на paypal n.s.shadrin@gmail.com или по ' +\
                        'банковской карте 5469 6800 8309 2725')
        infBox.addButton(QMessageBox.Ok)
        infBox.exec()

if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = MainWindow()
    sys.exit(app.exec_())
