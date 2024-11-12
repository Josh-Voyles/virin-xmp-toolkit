"""
Author: Josh Voyles
Created: 28 Oct 24

Description:

virin-xmp-toolkit is desgined to batch process video and image files.
It allows for file-renaming and metadata writing with ai help.

"""

import os
import sys

from PyQt6.QtWidgets import QApplication
from PyQt6 import QtGui
from views.main_window import MainWindow


def get_application_path() -> str:
    """Function to resolve application path when pyinstaller used"""
    if getattr(sys, "frozen", False):
        return os.path.abspath(sys._MEIPASS)
    return os.getcwd()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    AIR_FORCE_LOGO = "resources/images/US_Air_Force_Logo_Solid_Colour.svg"
    resolved_app_path = get_application_path()
    app.setWindowIcon(QtGui.QIcon(os.path.join(resolved_app_path, AIR_FORCE_LOGO)))

    window = MainWindow(resolved_app_path)
    window.show()
    sys.exit(app.exec())
