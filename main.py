import sys

from PyQt5.QtWidgets import QApplication

from src.PyTestCaseApp import PyTestCasesApp

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = PyTestCasesApp()
    ex.show()
    sys.exit(app.exec_())
