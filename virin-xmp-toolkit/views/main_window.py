"""
Module Name: main_window
Author: Josh Voyles
Created: 28 Oct 24

Description:

This module tries the front end gui to backend for virin xmp toolkit.

"""

from PyQt6.QtWidgets import QFileDialog, QMainWindow, QMessageBox
from PyQt6.QtGui import QRegularExpressionValidator
from PyQt6.QtCore import QCoreApplication, QRegularExpression
from models.file_rename import FileRenamer
from models.meta_edit import MetaTool
from models.ai_backend import VIRINAI
from views.main_window_ui import Ui_MainWindow


FILENAME_PAGE_INDEX = 0
METADATA_PAGE_INDEX = 1
AI_CAPTION_PAGE_INDEX = 2
EMPTY_STRING = ""
DEFAULT_CREATOR = "USAF Band Production"
DEFAULT_KEYWORD = "USAFBand"
PUBLIC_DOMAIN_COPYRIGHT = "Public Domain"


class MainWindow(QMainWindow):
    """
    MainWindow class that manages the user interface for renaming files and editing metadata.
    """

    def __init__(self):
        """
        Initializes the main window and sets up the user interface components,
        validators, and signals for various buttons.
        """
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.retranslateUi(self)
        self.current_window_index = 0
        self.file_path = EMPTY_STRING
        # dependencies
        self.fr = FileRenamer()
        self.meta = MetaTool()
        self.ai = VIRINAI()

        self.setWindowTitle("VIRIN XMP Toolkit")

        # filename rename input validation
        date_regex = QRegularExpression(
            r"(20|19)\d{2}(0[1-9]|1[012])(0[1-9]|[12][0-9]|3[01])$"
        )
        shot_regex = QRegularExpression(r"\d$")
        seq_regex = QRegularExpression(r"\d{3}$")
        date_validator = QRegularExpressionValidator(date_regex)
        shot_validator = QRegularExpressionValidator(shot_regex)
        seq_validator = QRegularExpressionValidator(seq_regex)
        self.ui.dateEdit.setValidator(date_validator)
        self.ui.shotEdit.setValidator(shot_validator)
        self.ui.seqEdit.setValidator(seq_validator)

        # connect buttons to functions
        self.ui.pushButton.clicked.connect(self.display_filename_page)
        self.ui.metaButton.clicked.connect(self.display_metadata_page)
        self.ui.aiButton.clicked.connect(self.display_ai_page)
        self.ui.openButton.clicked.connect(self.open_folder_chooser)
        self.ui.dateOverrideCheckBox.clicked.connect(self.clear_date)
        self.ui.renameButton.clicked.connect(self.rename_files)
        self.ui.undoButton.clicked.connect(self.undo_rename)
        self.ui.resetButton.clicked.connect(self.clear_all_filename_data)
        self.ui.loadButton.clicked.connect(self.load_metadata)
        self.ui.clearButton.clicked.connect(self.clear_metadata_fields)
        self.ui.writeButton.clicked.connect(self.write_metadata_to_files)
        self.ui.aiSubmitButton.clicked.connect(self.prompt_ai)
        self.ui.aiResetButton.clicked.connect(self.clear_ai_fields)

    def _display_empty_shot_seq_warning(self):
        """Displays a warning message if shot or sequence numbers are not provided."""
        message = "Please enter a shot and sequence number"
        QMessageBox.warning(self, "Number Error", message)

    def _display_empty_path_warning(self):
        """Displays a warning message if no file path is selected."""
        if not self.file_path:
            message = "Please choose a file path"
            QMessageBox.warning(self, "Path Error", message)

    def _get_file_format(self):
        """Retrieves the current file format based on the selected page."""
        if self.current_window_index == FILENAME_PAGE_INDEX:
            return self.ui.fileFormatComboBox.currentText()
        return self.ui.metaFileFormatComboBox.currentText()

    # Functions listed in priority top down
    def open_folder_chooser(self):
        """Opens a dialog to choose a folder and sets the selected folder path."""
        # TODO fix large dialog size
        folder_chooser = QFileDialog(self)
        path = folder_chooser.getExistingDirectory(
            None, "Select a Folder", EMPTY_STRING
        )
        self.file_path = path
        self.ui.pathLabel.setText(path)

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

    def rename_files(self):
        """Renames all files in the selected path based on the provided inputs (path, format, date, shot, sequence)."""
        if self.file_path:
            if self.ui.shotEdit.text() and self.ui.seqEdit.text():
                date = self.ui.dateEdit.text()
                shot = int(self.ui.shotEdit.text())
                seq = int(self.ui.seqEdit.text())
                ext = self.ui.fileFormatComboBox.currentText()
                QMessageBox.information(
                    self,
                    "Notification",
                    self.fr.rename_all_files(self.file_path, ext, date, shot, seq),
                )
            else:
                self._display_empty_shot_seq_warning()
        else:
            self._display_empty_path_warning()

    def clear_date(self):
        """Clears the date input field."""
        self.ui.dateEdit.setText(EMPTY_STRING)

    def clear_all_filename_data(self):
        """Clears all filename-related input fields."""
        if self.ui.dateEdit.text() != EMPTY_STRING:
            self.ui.dateOverrideCheckBox.toggle()
            self.clear_date()
        self.ui.shotEdit.setText(EMPTY_STRING)
        self.ui.seqEdit.setText(EMPTY_STRING)

    def undo_rename(self):
        """Undoes the last renaming operation."""
        QMessageBox.information(self, "Notification", self.fr.undo_rename())

    def load_metadata(self):
        """Loads existing metadata from the files in the selected path into the input fields."""
        metadata = self.meta.retreive_metadata(self.file_path, self._get_file_format())
        self.ui.creatorEdit.setText(metadata["Creator"])
        self.ui.writerEdit.setText(metadata["Writer"])
        self.ui.descriptionEdit.setPlainText(metadata["Description"])
        self.ui.titleEdit.setText(metadata["Title"])
        self.ui.keywordEdit.setText(metadata["Keywords"])
        self.ui.cityEdit.setText(metadata["City"])
        self.ui.countryEdit.setText(metadata["Country"])
        self.ui.stateEdit.setText(metadata["State"])
        self.ui.copyrightEdit.setText(metadata["Copyright"])

    def clear_metadata_fields(self):
        """Clears all metadata input fields to their default values."""
        self.ui.creatorEdit.setText(DEFAULT_CREATOR)
        self.ui.writerEdit.setText(EMPTY_STRING)
        self.ui.descriptionEdit.setPlainText(EMPTY_STRING)
        self.ui.titleEdit.setText(EMPTY_STRING)
        self.ui.keywordEdit.setText(DEFAULT_KEYWORD)
        self.ui.cityEdit.setText(EMPTY_STRING)
        self.ui.countryEdit.setText(EMPTY_STRING)
        self.ui.stateEdit.setText(EMPTY_STRING)
        self.ui.copyrightEdit.setText(PUBLIC_DOMAIN_COPYRIGHT)

    def write_metadata_to_files(self):
        """Writes metadata to the files in the selected path based on the input fields."""
        # standardizes keyword format
        clean_keywords = self.ui.keywordEdit.text().replace(",", " ").split(" ")
        clean_keywords = [
            keyword for keyword in clean_keywords if keyword != EMPTY_STRING
        ]
        joined_keywords = ", ".join(clean_keywords)
        metadata = {
            "creator": self.ui.creatorEdit.text(),
            "writer": self.ui.writerEdit.text(),
            "title": self.ui.titleEdit.text(),
            "description": self.ui.descriptionEdit.toPlainText(),
            "keywords": joined_keywords,
            "headline": self.ui.titleEdit.text(),
            "city": self.ui.cityEdit.text(),
            "country": self.ui.countryEdit.text(),
            "state": self.ui.stateEdit.text(),
            "copyright": self.ui.copyrightEdit.text(),
            "rights": self.ui.copyrightEdit.text(),
        }
        QMessageBox.information(
            self,
            "Notification",
            self.meta.write_metadata(self.file_path, self._get_file_format(), metadata),
        )

    def prompt_ai(self):
        """
        Prompts the AI to generate a caption based on the input text and displays
        the generated caption in the AI output box.
        """
        stream = self.ai.get_caption(self.ui.aiInputBoxEdit.toPlainText())
        text = ""
        for chunk in stream:
            text += chunk["message"]["content"]
            self.ui.aiOutputBox.setPlainText(text)
            QCoreApplication.processEvents()  # to get word by word stream of text

    def clear_ai_fields(self):
        """Clears the AI output and input fields."""
        self.ui.aiOutputBox.setPlainText(EMPTY_STRING)
        self.ui.aiInputBoxEdit.setPlainText(EMPTY_STRING)
