"""
Description
    
"""

import re, os, sys
from PyQt6.QtWidgets import QMainWindow, QMessageBox
from PyQt6.QtGui import QRegularExpressionValidator
from PyQt6.QtCore import QRegularExpression
from models.file_rename import FileRenamer as fr
from views.main_window_ui import Ui_MainWindow


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.retranslateUi(self)

        # any regex validation
        #
        self.setWindowTitle("virin exiftool")
