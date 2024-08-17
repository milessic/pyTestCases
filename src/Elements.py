import re
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QLabel, QLineEdit, QPushButton, QFrame, QFileDialog,
    QMessageBox, QVBoxLayout, QHBoxLayout, QTextEdit, QTableWidget, QTableWidgetItem, QHeaderView,
    QToolTip, QTableWidgetItem, QVBoxLayout, QGridLayout, QTableWidget, QTextEdit, QDialog
)
from PyQt5.QtCore import Qt, QTimer, QPoint
from PyQt5.QtGui import QFont, QColor

def myText(parent: QWidget, stylesheet, width, height, wrap=QTextEdit.WidgetWidth, **kwargs) -> QTextEdit:
    text_edit = QTextEdit(parent)
    text_edit.setStyleSheet(f"""
        background-color: {stylesheet.txt_bg};
        color: {stylesheet.txt_fg};
        border: 1px solid {stylesheet.bg};
    """)
    text_edit.setFixedWidth(width * 10)  # approximate width conversion
    text_edit.setFixedHeight(height * 20)  # approximate height conversion
    text_edit.setLineWrapMode(QTextEdit.WidgetWidth if wrap == QTextEdit.WidgetWidth else QTextEdit.NoWrap)
    return text_edit

def myEntry(parent: QWidget, stylesheet, width, **kwargs) -> QLineEdit:
    line_edit = QLineEdit(parent)
    line_edit.setStyleSheet(f"""
        background-color: {stylesheet.txt_bg};
        color: {stylesheet.txt_fg};
        border: 1px solid {stylesheet.bg};
    """)
    line_edit.setFixedWidth(width * 10)  # approximate width conversion
    return line_edit

