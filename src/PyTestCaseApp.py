import json
from pathlib import Path
from time import time
from tkinter import (
    Tk, StringVar, Label, Entry, Button, Frame, filedialog, messagebox, ttk
)
from openpyxl import load_workbook

class Colors:
    black = "black"
    red = "#ffb3ba"
    green = "#baffc9"
    yellow = "#ffdfba"
    gray = "#ababab"
    status_bg = "#6b6967"


class PyTestCasesApp(Tk):
    def __init__(self, start_maximized: bool = False):
        super().__init__()
        self.show_save_info = True
        self.test_cases = []
        self.current_test_index = 0
        self.test_execution_id = None
        self.start_maximized = start_maximized
        self.initUI()
        if self.start_maximized:
            print("Window maximized Not supported!")
            #self.attributes('-fullscreen', True)

    def initUI(self):
        # setup Window Title
        self.title("pyTestCases")

        # setup Top Panel
        self.execution_id_label = Label(self, text="Test Execution ID:")
        self.execution_id_label.grid(row=0, column=0, padx=5, pady=5)

        self.execution_id_input = Entry(self)
        self.execution_id_input.grid(row=0, column=1, padx=5, pady=5)

        self.execution_id_button = Button(self, text="Load Tests", command=self.loadTests)
        self.execution_id_button.grid(row=0, column=2, padx=5, pady=5)

        # setup Dropdown
        self.test_case_var = StringVar()
        self.test_case_dropdown = ttk.Combobox(self, textvariable=self.test_case_var)
        self.test_case_dropdown.grid(row=1, column=0, columnspan=3, padx=5, pady=5, sticky="ew")
        self.test_case_dropdown.bind("<<ComboboxSelected>>", self.displayTestCase)

        # setup Test Case Title
        #self.test_case_title = Label(self, text="Select a test case")
        #self.test_case_title.grid(row=2, column=0, columnspan=3, padx=5, pady=5)

        # setup Test Case Status
        self.test_status_info_label = Label(self, text="Test Status:")
        self.test_status_info_label.grid(row=3, column=0, columnspan=3, padx=0, pady=5, sticky="W")
        self.test_status_label = Label(self, text="")
        self.test_status_label.grid(row=3, column=1, columnspan=3, padx=0, pady=5, sticky="W")

        # setup Test Case Table
        self.test_case_table = ttk.Treeview(self, columns=("Description", "Expected Result"), show='headings')
        self.test_case_table.heading("Description", text="Description")
        self.test_case_table.heading("Expected Result", text="Expected Result")
        self.test_case_table.column("Description", width=300)
        self.test_case_table.grid(row=4, column=0, columnspan=3, padx=5, pady=5, sticky="nsew")

        # setup Buttons and their functions
        self.button_frame = Frame(self)
        self.button_frame.grid(row=5, column=0, columnspan=3, padx=5, pady=5)

        self.pass_button = Button(self.button_frame, text="PASS", bg=Colors.green, fg="black",
                                  command=lambda: self.updateTestStatus("PASS"))
        self.pass_button.pack(side="left", padx=5, pady=5)

        self.fail_button = Button(self.button_frame, text="FAIL", bg=Colors.red, fg="black",
                                  command=lambda: self.updateTestStatus("FAIL"))
        self.fail_button.pack(side="left", padx=5, pady=5)

        self.blocked_button = Button(self.button_frame, text="BLOCKED", bg=Colors.yellow, fg="black",
                                     command=lambda: self.updateTestStatus("BLOCKED"))
        self.blocked_button.pack(side="left", padx=5, pady=5)

        self.not_tested_button = Button(self.button_frame, text="NOT TESTED", bg=Colors.gray, fg="black",
                                        command=lambda: self.updateTestStatus("NOT TESTED"))
        self.not_tested_button.pack(side="left", padx=5, pady=5)

        self.prev_button = Button(self.button_frame, text="Previous", command=self.previousTestCase)
        self.prev_button.pack(side="left", padx=5, pady=5)

        self.next_button = Button(self.button_frame, text="Next", command=self.nextTestCase)
        self.next_button.pack(side="left", padx=5, pady=5)

    def setTestStatus(self, test_status: str):
        status = str(test_status).upper()
        match status:
            case "PASS":
                color = Colors.green
            case "FAIL":
                color = Colors.red
            case "BLOCKED":
                color = Colors.yellow
            case _:
                color = Colors.gray
        self.test_status_label.config(text=test_status, fg=color, bg=Colors.status_bg)
        return f"""<b style="color: {color};">{status}</b>"""
        print(test_status)


    def loadTests(self):
        file_path = filedialog.askopenfilename()
        self.file_name = Path(file_path).name

        if file_path.endswith("xlsx"):
            self.loadFromXlsx(file_path)
        elif file_path.endswith("json"):
            self.loadFromJson(file_path)
        else:
            messagebox.showerror("Error", "File format not supported")
            return

        if self.test_cases[0] == "from_output":
            self.file_loaded_from_output = True
            self.execution_id_input.config(state="disabled")
            self.test_cases.remove("from_output")
        else:
            self.file_loaded_from_output = False
            current_text_execution = self.execution_id_input.get()
            if current_text_execution == "":
                self.test_execution_id = str(int(time()))
                self.execution_id_input.insert(0, self.test_execution_id)

        self.test_case_dropdown['values'] = [
            f"{test_case['Test Case ID']} - {test_case['Test Case Name']}" for test_case in self.test_cases
        ]

        self.current_test_index = 0
        self.test_case_dropdown.current(self.current_test_index)
        self.displayTestCase()

    def displayTestCase(self, event=None):
        self.current_test_index = self.test_case_dropdown.current()
        if self.current_test_index == -1:
            return

        test_case = self.test_cases[self.current_test_index]
        #self.test_case_title.config(text=f"{test_case['Test Case ID']} - {test_case['Test Case Name']}")
        self.setTestStatus(test_case["Test Status"])

        for row in self.test_case_table.get_children():
            self.test_case_table.delete(row)

        for step in test_case["Test Steps"]:
            self.test_case_table.insert("", "end", values=step)

    def updateTestStatus(self, status):
        self.test_cases[self.current_test_index]["Test Status"] = status
        self.setTestStatus(status)
        self.saveResults()

    def previousTestCase(self):
        if self.current_test_index > 0:
            self.current_test_index -= 1
            self.test_case_dropdown.current(self.current_test_index)
            self.displayTestCase()

    def nextTestCase(self):
        if self.current_test_index < len(self.test_cases) - 1:
            self.current_test_index += 1
            self.test_case_dropdown.current(self.current_test_index)
            self.displayTestCase()

    def saveResults(self):
        self.test_execution_id = self.execution_id_input.get().strip()

        if not self.file_loaded_from_output and not self.test_execution_id:
            messagebox.showwarning("Error", "Test Execution ID is required!")
            return

        if self.file_loaded_from_output:
            output_file_name = self.file_name
        else:
            output_file_name = f"output_{self.test_execution_id}.json"

        self.test_cases.insert(0, "from_output")
        with open(output_file_name, "w") as file:
            json.dump(self.test_cases, file, indent=4)

        if self.show_save_info:
            messagebox.showinfo("Info", f"This pop-up is shown once per session!\nResults saved to {output_file_name}")
            self.show_save_info = False
        self.test_cases.remove("from_output")

    def loadFromJson(self, file_path: str):
        with open(file_path, "r") as file:
            self.test_cases = json.load(file)

    def loadFromXlsx(self, file_path: str):
        wb = load_workbook(file_path)
        ws = wb.active

        column_names = [cell.value for cell in ws[3]]

        raw_data = []
        current_test_case = None
        current_test_steps = []

        for row in ws.iter_rows(min_row=4, values_only=True):
            row_data = dict(zip(column_names, row))

            if current_test_case and row_data["Test Case Id"] != current_test_case["Test Case Id"]:
                raw_data.append({
                    "Test Case ID": current_test_case["Test Case Id"],
                    "Test Case Name": current_test_case["Test Case Name"],
                    "Area": current_test_case["Feature"],
                    "Level": current_test_case["Level"],
                    "Test Steps": current_test_steps,
                    "Test Execution Id": None,
                    "Test Status": None,
                })
                current_test_steps = []

            current_test_case = row_data
            current_test_steps.append([row_data["Test Step Description"], row_data["Expected Results"]])

        if current_test_case:
            raw_data.append({
                "Test Case ID": current_test_case["Test Case Id"],
                "Test Case Name": current_test_case["Test Case Name"],
                "Area": current_test_case["Feature"],
                "Level": current_test_case["Level"],
                "Test Steps": current_test_steps,
                "Test Execution Id": None,
                "Test Status": None,
            })

        self.test_cases += raw_data

        while self.test_cases[-1]["Test Case ID"] is None:
            self.test_cases.pop()


if __name__ == "__main__":
    app = PyTestCasesApp()
    app.mainloop()

