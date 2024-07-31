import json
from pathlib import Path
from time import time

from openpyxl import load_workbook
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFontMetrics
from PyQt5.QtWidgets import (
    QComboBox,
    QFileDialog,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)


class Colors:
    black = "black"
    red = "#ffb3ba"
    green = "#baffc9"
    yellow = "#ffdfba"
    gray = "#ababab"


class PyTestCasesApp(QWidget):
    r"""QWidget to load and execute Test Cases"""

    def __init__(self, start_maximized: bool = False):
        super().__init__()
        self.show_save_popup = True
        self.test_cases = []
        self.current_test_index = 0
        self.test_execution_id = None
        self.start_maximized = start_maximized
        self.initUI()
        if self.start_maximized:
            self.showMaximized()

    def initUI(self):
        # setup Window Title
        self.setWindowTitle("pyTestCases")

        # setup Layout
        self.layout = QVBoxLayout()

        # setup Top Panel
        self.execution_id_label = QLabel("Test Execution ID:")
        self.execution_id_input = QLineEdit()
        self.execution_id_button = QPushButton("Load Tests")
        self.execution_id_button.clicked.connect(self.loadTests)

        self.execution_layout = QHBoxLayout()
        self.execution_layout.addWidget(self.execution_id_label)
        self.execution_layout.addWidget(self.execution_id_input)
        self.execution_layout.addWidget(self.execution_id_button)

        self.layout.addLayout(self.execution_layout)

        # setup Dropdown
        self.test_case_dropdown = QComboBox()
        self.test_case_dropdown.currentIndexChanged.connect(self.displayTestCase)
        self.layout.addWidget(self.test_case_dropdown)

        # setup Test Case Title
        self.test_case_title = QLabel("Select a test case")
        self.test_status_label = QLabel("Test Status:")
        self.layout.addWidget(self.test_case_title)
        self.layout.addWidget(self.test_status_label)

        # setup Test Case Table
        self.test_case_table = QTableWidget()
        self.test_case_table.setColumnCount(2)
        self.test_case_table.setHorizontalHeaderLabels(
            ["Description", "Expected Result"]
        )
        self.test_case_table.setColumnWidth(0, 300)

        self.test_case_table.horizontalHeader().setStretchLastSection(True)

        self.test_case_table.setWordWrap(True)
        self.layout.addWidget(self.test_case_table)

        # setup Buttons and their functions
        self.button_layout = QHBoxLayout()

        self.pass_button = QPushButton("PASS")
        self.pass_button.setStyleSheet(f"background-color: {Colors.green};color: black")
        self.pass_button.clicked.connect(lambda: self.updateTestStatus("PASS"))
        self.fail_button = QPushButton("FAIL")
        self.fail_button.setStyleSheet(f"background-color: {Colors.red};color: black")
        self.fail_button.clicked.connect(lambda: self.updateTestStatus("FAIL"))
        self.blocked_button = QPushButton("BLOCKED")
        self.blocked_button.setStyleSheet(
            f"background-color: {Colors.yellow};color: black"
        )
        self.blocked_button.clicked.connect(lambda: self.updateTestStatus("BLOCKED"))
        self.not_tested_button = QPushButton("NOT TESTED")
        self.not_tested_button.setStyleSheet(
            "background-color: {Colors.gray};color: black"
        )
        self.not_tested_button.clicked.connect(
            lambda: self.updateTestStatus("NOT TESTED")
        )

        self.prev_button = QPushButton("Previous")
        self.prev_button.clicked.connect(self.previousTestCase)
        self.next_button = QPushButton("Next")
        self.next_button.clicked.connect(self.nextTestCase)

        self.button_layout.addWidget(self.pass_button)
        self.button_layout.addWidget(self.fail_button)
        self.button_layout.addWidget(self.blocked_button)
        self.button_layout.addWidget(self.not_tested_button)
        self.button_layout.addWidget(self.prev_button)
        self.button_layout.addWidget(self.next_button)

        self.layout.addLayout(self.button_layout)

        # set Layout
        self.setLayout(self.layout)

    def setTestStatus(self, test_status: str):
        # sets Test Status in the Application Window
        self.test_status_label.setText(
            f"Test Status: {self.returnTestStatus(test_status)}"
        )

    def returnTestStatus(self, status: str | None) -> str:
        # return formatted Test Status as string
        status = str(status).upper()
        match status:
            case "PASS":
                color = Colors.green
            case "FAIL":
                color = Colors.red
            case "BLOCKED":
                color = Colors.yellow
            case _:
                color = Colors.gray
        return f"""<b style="color: {color};">{status}</b>"""

    def loadTests(self):
        r"Loads tests from file"
        # use OpenFileName to opne file from the system
        file_path = QFileDialog.getOpenFileName(self)[0]
        self.file_name = Path(file_path).name

        # open file or
        if file_path.endswith("xlsx"):
            self.loadFromXlsx(file_path)
        elif file_path.endswith("json"):
            self.loadFromJson(file_path)
        else:
            # TODO add popup that file is not supported
            pass

        # if file origin is from pyTestCasses, then set the file_loaded_from_output flag and remove `from_output` entry from data
        # also disable execution_id_input to prevent saveAs functionlity
        if self.test_cases[0] == "from_output":
            self.file_loaded_from_output = True
            self.execution_id_input.setDisabled(True)
            self.test_cases.remove("from_output")
        else:
            self.file_loaded_from_output = False
            current_text_execution = self.execution_id_input.text()
            if current_text_execution == "":
                self.test_execution_id = str(int(time()))
                self.execution_id_input.setText(self.test_execution_id)

        # set up test_case_dropdown
        self.test_case_dropdown.clear()
        for test_case in self.test_cases:
            self.test_case_dropdown.addItem(
                f"{test_case['Test Case ID']} - {test_case['Test Case Name']}"
            )

        # display tes case
        self.displayTestCase()

    def displayTestCase(self):
        r"Displays test case from current_test_index"
        # get the index from test_case_dropdown
        self.current_test_index = self.test_case_dropdown.currentIndex()
        if self.current_test_index == -1:
            return

        # load test case from test_cases
        test_case = self.test_cases[self.current_test_index]
        self.test_case_title.setText(
            f"{test_case['Test Case ID']} - {test_case['Test Case Name']}"
        )
        self.setTestStatus(test_case["Test Status"])

        # populate test_case_table with test_case data
        self.test_case_table.setRowCount(len(test_case["Test Steps"]))
        for row, step in enumerate(test_case["Test Steps"]):
            item_description = QTableWidgetItem(str(step[0]))
            item_description.setTextAlignment(Qt.AlignLeft | Qt.AlignTop)
            item_expected = QTableWidgetItem(str(step[1]))
            item_expected.setTextAlignment(Qt.AlignLeft | Qt.AlignTop)
            self.test_case_table.setItem(row, 0, item_description)
            self.test_case_table.setItem(row, 1, item_expected)
            self.test_case_table.resizeRowsToContents()
            self.resizeRowsToFitContents()
        self.test_case_table.resizeRowsToContents()

    def resizeRowsToFitContents(self):
        """Resize all row heights to fit contents."""
        for row in range(self.test_case_table.rowCount()):
            self.resizeRowToContents(row)

    def resizeRowToContents(self, row):
        """Resize certain row height to fit contents."""
        font_metrics = QFontMetrics(self.test_case_table.font())
        row_height = 0

        # iterate through items in the row
        for column in range(self.test_case_table.columnCount()):
            item = self.test_case_table.item(row, column)
            if item:
                # calculate height of the text
                text_height = font_metrics.boundingRect(item.text()).height()
                row_height = max(row_height, text_height)

        # add padding
        padding = 10
        row_height += padding

        # set row height
        self.test_case_table.setRowHeight(row, row_height)

    def updateTestStatus(self, status):
        r"Updates Test Status both in data and UI"
        self.test_cases[self.current_test_index]["Test Status"] = status
        self.setTestStatus(status)
        self.saveResults()

    def previousTestCase(self):
        r"Loads previous test_case"
        if self.current_test_index > 0:
            self.current_test_index -= 1
            self.test_case_dropdown.setCurrentIndex(self.current_test_index)

    def nextTestCase(self):
        r"Loads next test case"
        if self.current_test_index < len(self.test_cases) - 1:
            self.current_test_index += 1
            self.test_case_dropdown.setCurrentIndex(self.current_test_index)

    def saveResults(self):
        r"Saves results to the file"
        # TODO error handling
        # format test_execution_id
        self.test_execution_id = self.execution_id_input.text().strip()

        # raise alert if test_execution_id is empty, skip for outputs
        if not self.file_loaded_from_output and not self.test_execution_id:
            QMessageBox.warning(self, "Error", "Test Execution ID is required!")
            return

        # set output name
        if self.file_loaded_from_output:
            output_file_name = self.file_name
        else:
            output_file_name = f"output_{self.test_execution_id}.json"

        # inject "from_output" to the data
        self.test_cases.insert(0, "from_output")
        with open(output_file_name, "w") as file:
            json.dump(self.test_cases, file, indent=4)

        # inform user that it worked
        if self.show_save_popup:
            QMessageBox.information(self, "Info", f"<b>This pop-up is shown once per session!</b><br>Results saved to {output_file_name}")
            self.show_save_popup = False
        self.test_cases.remove("from_output")

    def loadFromJson(self, file_path: str):
        r"Loads file from Json via path/filename"
        with open(file_path, "r") as file:
            self.test_cases = json.load(file)

    def loadFromXlsx(self, file_path: str):
        r"Loads file from Xlsx via path/filename"
        # TODO xlsx load more customizable
        # Open Workbook
        wb = load_workbook(file_path)
        ws = wb.active

        # fetch column names
        column_names = []
        for cell in ws[3]:
            try:
                column_names.append(cell.value.title())
            except AttributeError:
                break

        # initialize variables
        raw_data = []
        current_test_case = None
        current_test_steps = []

        # iterate through rows
        for row in ws.iter_rows(min_row=4, values_only=True):
            row_data = dict(zip(column_names, row))

            # check if it's a new test case
            if (
                current_test_case
                and row_data["Test Case Id"] != current_test_case["Test Case Id"]
            ):
                # save the previous test case before starting data collection for new one
                raw_data.append(
                    {
                        "Test Case ID": current_test_case["Test Case Id"],
                        "Test Case Name": current_test_case["Test Case Name"],
                        "Area": current_test_case["Feature"],
                        "Level": current_test_case["Level"],
                        "Test Steps": current_test_steps,
                        "Test Execution Id": None,
                        "Test Status": None,
                    }
                )
                # reset current_test_steps
                current_test_steps = []

            # Update the current test case and add the step
            current_test_case = row_data
            current_test_steps.append(
                [row_data["Test Step Description"], row_data["Expected Results"]]
            )

        # add the last test case to the raw_data
        if current_test_case:
            raw_data.append(
                {
                    "Test Case ID": current_test_case["Test Case Id"],
                    "Test Case Name": current_test_case["Test Case Name"],
                    "Area": current_test_case["Feature"],
                    "Level": current_test_case["Level"],
                    "Test Steps": current_test_steps,
                    "Test Execution Id": None,
                    "Test Status": None,
                }
            )

        # set test_cases
        self.test_cases += raw_data
        
        # remove empty results from end of the file
        while self.test_cases[-1]["Test Case ID"] is None:
            self.test_cases.pop()
