"""
Module Name: main_window
Author: Josh Voyles
Created: 28 Oct 24

Description:

This module tries the front end gui to backend for virin xmp toolkit.

"""

from PyQt6.QtWidgets import QFileDialog, QMainWindow, QMessageBox
from PyQt6 import QtGui
from PyQt6.QtGui import QRegularExpressionValidator
from PyQt6.QtCore import QRegularExpression, QThread, pyqtSignal
from models.file_rename import FileRenamer
from models.meta_edit import MetaTool
from models.ai_backend import VIRINAI
from views.main_window_ui import Ui_MainWindow
import os

SOFTWARE_VERSION = "0.3.0"
APPLICATION_TITLE = "VIRIN XMP Toolkit"
FILENAME_PAGE_INDEX = 0
METADATA_PAGE_INDEX = 1
AI_CAPTION_PAGE_INDEX = 2
EMPTY_STRING = ""
DEFAULT_CREATOR = "USAF Band Production"
DEFAULT_KEYWORD = "USAFBand"
PUBLIC_DOMAIN_COPYRIGHT = "Public Domain"


class FileRenameWorker(QThread):
    """Worker thread for file rename operations"""

    finished = pyqtSignal(str)

    def __init__(
        self,
        renamer,
        file_path=None,
        ext=None,
        date=None,
        shot=None,
        seq=None,
        operation="rename",
    ) -> None:
        super().__init__()
        self.fr = renamer
        self.file_path = file_path
        self.ext = ext
        self.date = date
        self.shot = shot
        self.seq = seq
        self.operation = operation

    def run(self):
        try:
            if self.operation == "rename":
                result = self.fr.rename_all_files(
                    self.file_path, self.ext, self.date, self.shot, self.seq
                )
            else:  # undo
                result = self.fr.undo_rename()
            self.finished.emit(result)
        except Exception as e:
            self.finished.emit(f"Error: {str(e)}")


class MetadataWorker(QThread):
    """Worker thread for metadata operations"""

    finished = pyqtSignal(dict)  # For load operations
    message = pyqtSignal(str)  # For write operations

    def __init__(self, meta_tool, file_path, file_format, operation, metadata=None):
        super().__init__()
        self.meta = meta_tool
        self.file_path = file_path
        self.file_format = file_format
        self.operation = operation  # 'load' or 'write'
        self.metadata = metadata

    def run(self):
        try:
            if self.operation == "load":
                result = self.meta.retreive_metadata(self.file_path, self.file_format)
                self.finished.emit(result)
            else:  # write
                result = self.meta.write_metadata(
                    self.file_path, self.file_format, self.metadata
                )
                self.message.emit(result)
        except Exception as e:
            self.message.emit(f"Error: {str(e)}")


class AICaptionWorker(QThread):
    """Worker thread to update AI caption"""

    text_update = pyqtSignal(str)

    def __init__(self, ai_instance, input_text):
        super().__init__()
        self.ai = ai_instance
        self.input_text = input_text

    def run(self) -> None:
        try:
            stream = self.ai.get_caption(self.input_text)
            text = ""
            for chunk in stream:
                text += chunk["message"]["content"]
                self.text_update.emit(text)
        except Exception as e:
            self.text_update.emit(f"Error generating caption: {str(e)}")


class MainWindow(QMainWindow):
    """
    MainWindow class that manages the user interface for renaming files and editing metadata.
    """

    def __init__(self, resolved_app_path):
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
        self.ai = VIRINAI(resolved_app_path)

        self.setWindowTitle(APPLICATION_TITLE + " " + SOFTWARE_VERSION)
        # must reset logo to gui for pyinstaller executables
        self.ui.logoLabel.setPixmap(
            QtGui.QPixmap(
                os.path.join(
                    resolved_app_path,
                    "resources/images/US_Air_Force_Logo_Solid_Colour.svg",
                )
            )
        )
        self.rename_thread = None
        self.metadata_thread = None

        self._setup_validators()
        self._connect_buttons()

    def _setup_validators(self):
        """Set up input validators"""
        date_regex = QRegularExpression(
            r"(20|19)\d{2}(0[1-9]|1[012])(0[1-9]|[12][0-9]|3[01])$"
        )
        shot_regex = QRegularExpression(r"\d$")
        seq_regex = QRegularExpression(r"\d{3}$")

        self.ui.dateEdit.setValidator(QRegularExpressionValidator(date_regex))
        self.ui.shotEdit.setValidator(QRegularExpressionValidator(shot_regex))
        self.ui.seqEdit.setValidator(QRegularExpressionValidator(seq_regex))

    def _connect_buttons(self):
        """Connect all buttons to their slots"""
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

    def _show_message_box(self, title, message, message_type):
        """Slot for displaying actual message box"""
        if message_type == "warning":
            QMessageBox.warning(self, title, message)
        else:
            QMessageBox.information(self, title, message)

    def _display_empty_shot_seq_warning(self):
        """Displays a warning message if shot or sequence numbers are not provided."""
        message = "Please enter a shot and sequence number"
        self._show_message_box("Number Error", message, "warning")

    def _display_empty_path_warning(self):
        """Displays a warning message if no file path is selected."""
        if not self.file_path:
            message = "Please choose a file path"
            self._show_message_box("Path Error", message, "warning")

    def _get_file_format(self):
        """Retrieves the current file format based on the selected page."""
        if self.current_window_index == FILENAME_PAGE_INDEX:
            return self.ui.fileFormatComboBox.currentText()
        return self.ui.metaFileFormatComboBox.currentText()

    def _update_metadata_fields(self, metadata):
        """Updates UI with loaded metadata"""
        self.ui.creatorEdit.setText(metadata["Creator"])
        self.ui.writerEdit.setText(metadata["Writer"])
        self.ui.descriptionEdit.setPlainText(metadata["Description"])
        self.ui.titleEdit.setText(metadata["Title"])
        self.ui.keywordEdit.setText(metadata["Keywords"])
        self.ui.cityEdit.setText(metadata["City"])
        self.ui.countryEdit.setText(metadata["Country"])
        self.ui.stateEdit.setText(metadata["State"])
        self.ui.copyrightEdit.setText(metadata["Copyright"])

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
                self.rename_thread = FileRenameWorker(
                    self.fr, self.file_path, ext, date, shot, seq
                )
                self.rename_thread.finished.connect(
                    lambda msg: self._show_message_box(
                        "Notification", msg, "notification"
                    )
                )
                self.rename_thread.start()
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
        self.rename_thread = FileRenameWorker(self.fr, operation="undo")
        self.rename_thread.finished.connect(
            lambda msg: self._show_message_box("Notification", msg, "information")
        )
        self.rename_thread.start()

    def load_metadata(self):
        """Loads existing metadata from the files in the selected path into the input fields."""
        self.metadata_thread = MetadataWorker(
            self.meta, self.file_path, self._get_file_format(), "load"
        )
        self.metadata_thread.finished.connect(self._update_metadata_fields)
        self.metadata_thread.message.connect(
            lambda msg: self._show_message_box("Notification", msg, "information")
        )
        self.metadata_thread.start()

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
        self.metadata_thread = MetadataWorker(
            self.meta, self.file_path, self._get_file_format(), "write", metadata
        )
        self.metadata_thread.message.connect(
            lambda: self._show_message_box(
                "Notification", "Metadata updated succussfully!", "notification"
            )
        )
        self.metadata_thread.start()

    def prompt_ai(self):
        """
        Prompts the AI to generate a caption based on the input text and displays
        the generated caption in the AI output box.
        """
        self.ui.aiOutputBox.setPlainText("")
        input_text = self.ui.aiInputBoxEdit.toPlainText()
        self.ai_thread = AICaptionWorker(self.ai, input_text)
        self.ai_thread.text_update.connect(self.ui.aiOutputBox.setPlainText)
        self.ai_thread.start()

    def clear_ai_fields(self):
        """Clears the AI output and input fields."""
        self.ui.aiOutputBox.setPlainText(EMPTY_STRING)
        self.ui.aiInputBoxEdit.setPlainText(EMPTY_STRING)
