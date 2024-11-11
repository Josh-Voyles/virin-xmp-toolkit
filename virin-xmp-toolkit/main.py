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


if __name__ == "__main__":
    app = QApplication(sys.argv)
    AIR_FORCE_LOGO = "resources/images/US_Air_Force_Logo_Solid_Colour.svg"
    if getattr(sys, "frozen", False):
        resolved_AIR_FORCE_LOGO = os.path.abspath(
            os.path.join(sys._MEIPASS, AIR_FORCE_LOGO)
        )
    else:
        resolved_AIR_FORCE_LOGO = os.path.abspath(
            os.path.join(os.getcwd(), AIR_FORCE_LOGO)
        )
    app.setWindowIcon(QtGui.QIcon(resolved_AIR_FORCE_LOGO))

    window = MainWindow()
    window.show()
    sys.exit(app.exec())
