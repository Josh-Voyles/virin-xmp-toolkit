"""
Description
    
"""

import re, os, sys
from PyQt6.QtWidgets import QFileDialog, QMainWindow, QMessageBox
from PyQt6.QtGui import QRegularExpressionValidator
from PyQt6.QtCore import Q_RETURN_ARG, QRegularExpression
from models.file_rename import FileRenamer
from models.meta_edit import MetaTool
from views.main_window_ui import Ui_MainWindow

FILENAME_PAGE_INDEX = 0
METADATA_PAGE_INDEX = 1
AI_CAPTION_PAGE_INDEX = 2


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.retranslateUi(self)
        self.current_window_index = 0
        self.file_path = ""
        self.fr = FileRenamer()
        self.meta = MetaTool()

        self.setWindowTitle("virin exiftool")

        # filename rename input validation
        date_regex = QRegularExpression(
            r"(20|19)\d{2}(0[1-9]|1[012])(0[1-9]|[12][0-9]|3[01])$"
        )
        shot_regex = QRegularExpression(r"\d$")
        seq_regex = QRegularExpression(r"\d\d\d$")
        date_validator = QRegularExpressionValidator(date_regex)
        shot_validator = QRegularExpressionValidator(shot_regex)
        seq_validator = QRegularExpressionValidator(seq_regex)
        self.ui.dateEdit.setValidator(date_validator)
        self.ui.shotEdit.setValidator(shot_validator)
        self.ui.seqEdit.setValidator(seq_validator)

        self.ui.pushButton.clicked.connect(self.display_filename_page)
        self.ui.metaButton.clicked.connect(self.display_metadata_page)
        self.ui.aiButton.clicked.connect(self.display_ai_page)
        self.ui.openButton.clicked.connect(self.open_folder_chooser)
        self.ui.dateOverrideCheckBox.clicked.connect(self.clear_date)
        self.ui.renameButton.clicked.connect(self.rename_files)
        self.ui.undoButton.clicked.connect(self.undo_rename)
        self.ui.resetButton.clicked.connect(self.clear_all_filename_data)

    # Functions listed in priority top down
    def open_folder_chooser(self):
        # TODO fix large dialog size
        # TODO Confirm slash will never be added
        folder_chooser = QFileDialog(self)
        path = folder_chooser.getExistingDirectory(None, "Select a Folder", "")
        self.file_path = path
        self.ui.pathLabel.setText(path)
        # self.meta.retreive_metadata(path, "png")  # temp fixed entension

    def display_filename_page(self):
        """Displays filename edit page"""
        self.ui.stackedWidget.setCurrentIndex(FILENAME_PAGE_INDEX)
        self.current_window_index = FILENAME_PAGE_INDEX

    def display_metadata_page(self):
        """Displays metadata edit page"""
        self.ui.stackedWidget.setCurrentIndex(METADATA_PAGE_INDEX)
        self.current_window_index = METADATA_PAGE_INDEX

    def display_ai_page(self):
        """Displays ai edit page"""
        self.ui.stackedWidget.setCurrentIndex(AI_CAPTION_PAGE_INDEX)
        self.current_window_index = AI_CAPTION_PAGE_INDEX

    def display_current_metadata(self):
        pass

    def get_file_format(self):
        if self.current_window_index == FILENAME_PAGE_INDEX:
            return self.ui.fileFormatComboBox.currentText()
        return self.ui.metaFileFormatComboBox.currentText()

    def clear_date(self):
        self.ui.dateEdit.setText("")

    def clear_all_filename_data(self):
        if self.ui.dateEdit.text() != "":
            self.ui.dateOverrideCheckBox.toggle()
            self.clear_date()
        self.ui.shotEdit.setText("")
        self.ui.seqEdit.setText("")

    def rename_files(self):
        if self.file_path:
            date = self.ui.dateEdit.text()
            shot = int(self.ui.shotEdit.text())
            seq = int(self.ui.seqEdit.text())
            ext = self.ui.fileFormatComboBox.currentText()
            QMessageBox.warning(
                self,
                "Notification",
                self.fr.rename_all_files(self.file_path, ext, date, shot, seq),
            )
        else:
            self.display_empty_path_warning()

    def undo_rename(self):
        QMessageBox.warning(self, "Notification", self.fr.undo_rename())

    def display_empty_path_warning(self):
        if not self.file_path:
            message = "Please choose a file path"
            QMessageBox.warning(self, "Path Error", message)
