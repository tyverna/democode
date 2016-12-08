#!/usr/bin/env python3

# Copyright (c) 2010-2011, 2013 Algis Kabaila. All rights reserved.
# This work is made available under  the terms of the 
# Creative Commons Attribution-ShareAlike 3.0 license,
# http://creativecommons.org/licenses/by-sa/3.0/. 

# combine.py - combination of ShowGPL, About, Close scripts   
# The purpose of this version of program is to show implementation
# of most code in one file - all_in_1!. The Ui_MainWindow is eliminated
# and does not appear in the program.
     
import sys
import time
import platform
     
import PySide
     
from PySide.QtCore import QRect
from PySide.QtGui import (QApplication, QMainWindow, QMessageBox,
                          QIcon, QAction, QWidget, QGridLayout,
                          QTextEdit, QMenuBar, QMenu, QStatusBar, 
                          QLabel, QStackedWidget)

     
__version__ = '3.1.5'

    
class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.resize(800, 480)
        self.setWindowTitle('PySide GUI')
        #self.setWindowFlags(PySide.QtCore.Qt.FramelessWindowHint)

         
        self.wgHome, self.dcHome = self.createHomePage()


        '''# home page
        self.wgHome = QWidget(self)
        gridLayout = QGridLayout(self.wgHome)
        gridLayout.addWidget(QLabel('Home'), 0, 0, 1, 0)

        gridLayout.addWidget(QLabel('Tx'), 1, 0)
        self.lbtx = QLabel('tx data')
        self.lbtx.setMinimumWidth(400)
        gridLayout.addWidget(self.lbtx, 1, 1)

        gridLayout.addWidget(QLabel('Rx'), 2, 0)
        self.lbrx = QLabel('rx data')
        gridLayout.addWidget(self.lbrx, 2, 1)'''

        
        # serial page
        self.wgSerial = QWidget(self)
        gridLayout = QGridLayout(self.wgSerial)
        self.lb1 = QLabel('serial page')
        self.lb2 = QLabel('label 2')
        self.lb3 = QLabel('label 3')
        
        gridLayout.addWidget(self.lb1, 0, 0)
        gridLayout.addWidget(self.lb2, 1, 0)
        gridLayout.addWidget(self.lb3, 2, 0)
        

        self.sw = QStackedWidget(self)
        self.sw.addWidget(self.wgHome)
        self.sw.addWidget(self.wgSerial)
        self.setCentralWidget(self.sw)
        
        
        menubar = QMenuBar(self)
        menubar.setGeometry(QRect(0, 0, 731, 29))
        menu_File = QMenu(menubar)
        self.setMenuBar(menubar)
        statusbar = QStatusBar(self)
        self.setStatusBar(statusbar)
        

        actionHome = QAction(self)
        actionHome.setIcon(QIcon("icon/Home-50.png"))
        actionHome.setStatusTip("Home content")
        actionHome.triggered.connect(
            lambda: self.sw.setCurrentWidget(self.wgHome))

        actionSerial = QAction(self)
        actionSerial.setIcon(QIcon("icon/Unicast-50.png"))
        actionSerial.setStatusTip("Serial polling task status")
        actionSerial.triggered.connect(
            lambda: self.sw.setCurrentWidget(self.wgSerial))

        actionLogging = QAction(self)
        actionLogging.setIcon(QIcon("icon/Database-50.png"))
        actionLogging.setStatusTip("Logging task status")
        actionLogging.triggered.connect(
            lambda: self.sw.setCurrentWidget(self.wgLogging))  

        actionUpload = QAction(self)
        actionUpload.setIcon(QIcon("icon/Upload to Cloud-50.png"))
        actionUpload.setStatusTip("Uploading task status")
        actionUpload.triggered.connect(
            lambda: self.sw.setCurrentWidget(self.wgLogging))  

        actionDebug = QAction(self)
        actionDebug.setIcon(QIcon("icon/Bug-50.png"))
        actionDebug.setStatusTip("debug")
        actionDebug.triggered.connect(self.debug)  


        actionAbout = QAction(self)
        actionAbout.triggered.connect(self.about)
        actionAbout.setIcon(QIcon("icon/Info-50.png"))
        actionAbout.setStatusTip("Pop up the About dialog.")

        actionSetting = QAction(self)
        actionSetting.setCheckable(False)
        actionSetting.setObjectName('action_clear')
        actionSetting.setIcon(QIcon("icon/Settings-50.png"))
        

        actionLeft = QAction(self)
        actionLeft.setIcon(QIcon("icon/Left-50.png"))
        actionLeft.setStatusTip("Left page")
        actionLeft.triggered.connect(self.switchLeftWidget)

        actionRight = QAction(self)
        actionRight.setIcon(QIcon("icon/Right-50.png"))
        actionRight.setStatusTip("Right page")
        actionRight.triggered.connect(self.switchRightWidget)
        

        actionClose = QAction(self)
        actionClose.setCheckable(False)
        actionClose.setObjectName("action_Close")        
        actionClose.setIcon(QIcon("icon/Delete-50.png"))
        actionClose.setStatusTip("Close the program.")
        actionClose.triggered.connect(self.close)        

#------------------------------------------------------
        menu_File.addAction(actionHome)
        menu_File.addAction(actionAbout)
        menu_File.addAction(actionClose)
        menu_File.addAction(actionSetting)
        menubar.addAction(menu_File.menuAction())


        iconToolBar = self.addToolBar("iconBar.png")
        iconToolBar.addAction(actionHome)
        
        iconToolBar.addAction(actionSerial)
        iconToolBar.addAction(actionLogging)
        iconToolBar.addAction(actionUpload)

        iconToolBar.addAction(actionDebug)
        
        iconToolBar.addAction(actionAbout)
        iconToolBar.addAction(actionSetting)
        iconToolBar.addAction(actionLeft)
        iconToolBar.addAction(actionRight)
        iconToolBar.addAction(actionClose)


    def createHomePage(self):
        dc = dict()
        wgHome = QWidget(self)
        gridLayout = QGridLayout(wgHome)
        gridLayout.addWidget(QLabel('Home'), 0, 0, 1, 0)

        gridLayout.addWidget(QLabel('Tx'), 1, 0)
        lbtx = QLabel('tx data')
        lbtx.setMinimumWidth(400)
        dc['pvtx'] = lbtx
        gridLayout.addWidget(lbtx, 1, 1)

        gridLayout.addWidget(QLabel('Rx'), 2, 0)
        lbrx = QLabel('rx data')
        dc['pvrx'] = lbrx
        gridLayout.addWidget(lbrx, 2, 1)

        return wgHome, dc


    def debug(self):
        self.dcHome['pvtx'].setText(str(time.time()))
        

    def switchLeftWidget(self):
        i = self.sw.currentIndex() - 1
        if i < 0: i = 0
        self.sw.setCurrentIndex(i)
        #print('{}, {}'.format(self.sw.currentIndex(), self.sw.count()))

    def switchRightWidget(self):
        i = self.sw.currentIndex() + 1
        if i > self.sw.count(): i = self.sw.count() 
        self.sw.setCurrentIndex(i)
        #print('{}, {}'.format(self.sw.currentIndex(), self.sw.count()))
        


           
    def about(self):
        '''Popup a box with about message.'''
        QMessageBox.about(self, "About PySide, Platform and version.",
                """<b> about.py version %s </b> 
                <p>Copyright &copy; 2013 by Algis Kabaila. 
                This work is made available under  the terms of
                Creative Commons Attribution-ShareAlike 3.0 license,
                http://creativecommons.org/licenses/by-sa/3.0/.
                <p>This application is useful for displaying  
                Qt version and other details.
                <p>Python %s -  PySide version %s - Qt version %s on %s""" %
                (__version__, platform.python_version(), PySide.__version__,
                 PySide.QtCore.__version__, platform.system()))                        
           
if __name__ == '__main__':
    app = QApplication(sys.argv)
    frame = MainWindow()
    frame.show()
    sys.exit(app.exec_())
