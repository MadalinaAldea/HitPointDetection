"""Docstring"""

import sys

from PyQt5.QtWidgets import QApplication, QMainWindow

from dialog.MainWindow import UiMainWindow

def run():
    app = QApplication(sys.argv)
    window = QMainWindow()
    ui = UiMainWindow(window)
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    run()
