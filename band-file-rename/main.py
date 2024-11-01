import os
import sys

from PyQt6.QtWidgets import QApplication
from PyQt6 import QtWidgets, QtCore, QtGui
from views.main_window import MainWindow


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    path = "images/US_Air_Force_Logo_Solid_Colour.svg"
    if getattr(sys, "frozen", False):
        resolved_path = os.path.abspath(os.path.join(sys._MEIPASS, path))
    else:
        resolved_path = os.path.abspath(os.path.join(os.getcwd(), path))
    app.setWindowIcon(QtGui.QIcon(resolved_path))

    window = MainWindow()
    window.show()
    sys.exit(app.exec())
