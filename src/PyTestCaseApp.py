import json
from pathlib import Path
from time import time
from tkinter import (
    END, Tk, StringVar, Label, Entry, Button, Frame, filedialog, messagebox, ttk, Misc, Text, PhotoImage
)
from tkinter.constants import FIRST, LAST, WORD
from src.models import TestCaseModel
from src.styles import Styles, Colors
from src.Elements import myText, myEntry, Table


class PyTestCasesApp(Tk):
    def __init__(self,
                 theme:str | None = None,
                 actual_results_displayed=True,
                 always_on_top:bool=True,
                 column_width:int=30,
                 preconditions_displayed:bool=True,
                 default_exports_prefix:str="output_",
                 column_names_row:int=3,
                 test_case_data_starting_row:int=4,
                 xlsx_test_cases_sheet_name:str="TEST CASES"
                 ):
        super().__init__()
        self.app_name = "PyTestCases"
        self.xlsx_test_cases_sheet_name = xlsx_test_cases_sheet_name
        self.default_exports_prefix = default_exports_prefix
        self.editing_disabled = False
        self.column_names_row=column_names_row
        self.test_case_data_starting_row = test_case_data_starting_row
        self.actual_results_displayed = actual_results_displayed
        self.preconditions_displayed = preconditions_displayed
        self.entroll_actual_results = actual_results_displayed
        self.resizable(0, 0) 
        self.pixel = PhotoImage()
        theme = str(theme)
        self.s = Styles(theme_name=theme)
        self.config(bg=self.s.bg)
        self.show_save_info = True
        self.test_cases = []
        self.column_width = int(column_width)
        self.current_test_index = 0
        self.test_execution_id = None
        #self.geometry("520x300")
        self.initUI()
        self.style = ttk.Style(self)
        self.control_actual_result()
        if always_on_top:
            self.attributes("-topmost", True)

    def initUI(self):
        # setup Window Title
        self.title(self.app_name)

        # setup Top Panel
        self.execution_id_label = self.myLabel(self, text="Test Execution ID:")
        self.execution_id_label.grid(row=0, column=0, padx=5, pady=5, sticky="W")

        self.execution_id_input = myEntry(self, self.s, 30)
        self.execution_id_input.grid(row=0, column=1, columnspan=1,padx=10, pady=5)

        self.execution_id_button = self.myButton(self, text="Load Tests", command=self.loadTests)
        self.execution_id_button.grid(row=0, column=2, padx=0, pady=5, sticky="W")

        # setup Dropdown
        self.test_case_var = StringVar()
        self.test_case_dropdown = ttk.Combobox(self, textvariable=self.test_case_var, width=40)
        self.test_case_dropdown.grid(row=1, column=0, columnspan=2, padx=5,pady=5, sticky="W")
        self.test_case_dropdown.bind("<<ComboboxSelected>>", self.displayTestCase)

        # setup Test Case Title
        #self.test_case_title = self.myLabel(self, text="Select a test case")
        #self.test_case_title.grid(row=2, column=0, columnspan=3, padx=5, pady=5)

        # setup Test Case Status
        self.test_status_info_label = self.myLabel(self, text="Test Status:")
        self.test_status_info_label.grid(row=1, column=1,  padx=0, pady=5, sticky="E")
        self.test_status_label = self.myLabel(self, text="")
        self.test_status_label.grid(row=1, column=2,  padx=5, pady=5, sticky="we")

        # Setup Preconditions button and display
        self.preconditions_text_frame = self.myFrame(self)
        self.preconditions_label = self.myLabel(self.preconditions_text_frame, text="      Preconditions", bold=True)
        self.preconditions_text = Table(self.preconditions_text_frame, column_headers=[], column_width=50, stylesheet=self.s,) #fixed_grid=[2,0])
        #self.preconditions_text = myText(self, stylesheet=self.s, width=50, height=3, wrap=WORD)
        #self.preconditions_text.config(state="disabled")
        self.preconditions_control_btn = self.myButton(self, "-", command=lambda: self.control_preconditions(), image=True)

        self.preconditions_label.grid(row=2, column=0, sticky="W")
        self.preconditions_text_frame.grid(row=3, column=0, columnspan=3, sticky="W")
        self.preconditions_control_btn.place(x=5, y=132)

        # setup Test Case Table
        #self.test_case_table = ttk.Treeview(self, columns=("Description", "Expected Result"), show='headings')
        self.table_test_case_frame = self.myFrame(self)
        self.test_table_column_step = self.myLabel(self.table_test_case_frame, text="Test Step", bold=True)
        self.test_table_column_expected = self.myLabel(self.table_test_case_frame, text="Expected Results", bold=True)
        self.test_table_column_actual = self.myLabel(self.table_test_case_frame, text="Actual Results", bold=True)
        self.test_case_table = Table(self.table_test_case_frame, column_headers=["Description", "Expected Result", "Actual Result"], column_width=self.column_width, stylesheet=self.s)
        self.test_table_control_actual_btn = self.myButton(self.table_test_case_frame, "-", lambda: self.control_actual_result(), image=True)

        self.test_table_column_step.grid(row=0,column=0)
        self.test_table_column_expected.grid(row=0,column=1)
        self.test_table_column_actual.grid(row=0,column=2)
        self.test_table_control_actual_btn.place(x=self.column_width*15,y=1)
        self.table_test_case_frame.grid(row=5, column=0, columnspan=3, padx=5, pady=5)

        # setup Buttons and their functions
        self.button_frame = self.myFrame(self)
        self.button_frame.grid(row=2, column=0, columnspan=3, padx=0, pady=5)

        self.pass_button = self.myButton(self.button_frame, text="PASS", bg=Colors.green, fg="black",
                                  command=lambda: self.updateTestStatus("PASS"))
        self.pass_button.pack(side="left", padx=5, pady=5)

        self.fail_button = self.myButton(self.button_frame, text="FAIL", bg=Colors.red, fg="black",
                                  command=lambda: self.updateTestStatus("FAIL"))
        self.fail_button.pack(side="left", padx=5, pady=5)

        self.blocked_button = self.myButton(self.button_frame, text="BLOCKED", bg=Colors.yellow, fg="black",
                                     command=lambda: self.updateTestStatus("BLOCKED"))
        self.blocked_button.pack(side="left", padx=5, pady=5)

        self.not_tested_button = self.myButton(self.button_frame, text="NOT TESTED", bg=Colors.gray, fg="black",
                                        command=lambda: self.updateTestStatus("NOT TESTED"))
        self.not_tested_button.pack(side="left", padx=5, pady=5)

        self.prev_button = self.myButton(self.button_frame, text="Previous", command=self.previousTestCase)
        self.prev_button.pack(side="left", padx=5, pady=5)

        self.next_button = self.myButton(self.button_frame, text="Next", command=self.nextTestCase)
        self.next_button.pack(side="left", padx=5, pady=5)

    def control_preconditions(self):
        if self.preconditions_displayed:
            self.preconditions_text.hide_whole()
            self.preconditions_displayed = False
        else:
            self.preconditions_text.show_whole()
            self.preconditions_displayed = True


    def control_actual_result(self):
        if self.actual_results_displayed:
            self.hide_actual_result()
        else:
            self.show_actual_result()

    def hide_actual_result(self, change_status:bool=True):
        self.test_case_table.hide_actual()
        self.test_table_column_actual.grid_remove()
        if change_status:
            self.actual_results_displayed = False


    def show_actual_result(self, change_status:bool=True):
        #self.test_case_table.show_actual()
        self.test_table_column_actual.grid(row=0,column=2)
        self.displayTestCase(handle_actual_results=False)
        if change_status:
            self.actual_results_displayed = True

    def myLabel(self, master:Misc, text:str, bold:bool=False, **kwargs) -> Label:
        if bold:
            return Label(
                master=master,
                text=text,
                bg=self.s.bg,
                fg=self.s.fg,
                font="bold",
                **kwargs
                )
        else:
            return Label(
                master=master,
                text=text,
                bg=self.s.bg,
                fg=self.s.fg,
                **kwargs,
                )

    def myCombobox(self, master:Misc, textvariable, width) -> ttk.Combobox:
        return ttk.Combobox(
                master=master,
                textvariable=textvariable,
                width=width,
                background=self.s.txt_bg,
                cursor="cross"

                
                )

    def myButton(self, master, text:str, command, fg=None, bg=None, image:bool=False,**kwargs) -> Button:
        if image:
            btn_image = self.pixel
            width = 10
            height = 10
        else:
            btn_image = None
            width = None
            height = None
        return Button(
                image=btn_image,#self.pixel,
                master=master,
                text=text,
                command=command,
                background=self.s.bg if bg is None else bg,
                fg=self.s.fg if fg is None else fg,
                highlightcolor=self.s.btn_highlight,
                highlightbackground=self.s.btn_highlight,
                activebackground=self.s.btn_highlight,
                width=width,
                height=height,
                **kwargs
                )
    def myFrame(self, master) -> Frame:
        return Frame(
                master=master,
                bg=self.s.bg,
                )


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
        self.test_status_label.config(text=status, fg=color, bg=self.s.status_bg)
        return f"""<b style="color: {color};">{status}</b>"""


    def loadTests(self):
        file_path = filedialog.askopenfilename()
        self.file_name = Path(file_path).name

        if file_path.endswith("xlsx"):
            raw_data = self.loadXlsx(file_path)
        elif file_path.endswith("json"):
            raw_data = self.loadJson(file_path)
        else:
            messagebox.showerror("Error", "File format not supported")
            return
        self.loadTestsFromRawData(raw_data)

        if raw_data[0] == "from_output":
            execution_id = self.file_name.removeprefix(self.default_exports_prefix).removesuffix(".json")
            self.execution_id_input.delete(0, END)
            self.execution_id_input.insert(0, execution_id)
            self._update_test_execution_id()
            self.file_loaded_from_output = True
            self.execution_id_input.config(state="disabled")
            #self.test_cases.remove("from_output")
        else:
            self.file_loaded_from_output = False
            current_text_execution = self.execution_id_input.get()
            if current_text_execution == "":
                self.test_execution_id = str(int(time()))
                self.execution_id_input.insert(0, self.test_execution_id)

        self.test_case_dropdown['values'] = [
            test_case for test_case in self.test_cases
        ]

        self.current_test_index = 0
        self.test_case_dropdown.current(self.current_test_index)
        self.displayTestCase()

    def displayTestCase(self, event=None, handle_actual_results:bool=True):
        self.current_test_index = self.test_case_dropdown.current()
        if self.current_test_index == -1:
            return

        test_case = self.test_cases[self.current_test_index].dict()
        #self.test_case_title.config(text=f"{test_case['Test Case ID']} - {test_case['Test Case Name']}")
        self.setTestStatus(test_case["Test Status"])

        self.test_case_table.clear()
        #for row in self.test_case_table.get_children():
        #    self.test_case_table.delete(row)

        for step, expected, actual, note in zip(
                test_case["Test Steps"][0],
                test_case["Test Steps"][1],
                test_case["Test Steps"][2],
                test_case["Test Steps"][3],
                ):
            #lines_step = step[0].count("\n")
            #lines_expected = step[1].count("\n")
            #rowheight = max(lines_step, lines_expected) * 20
            #rowheight = rowheight if rowheight else 20
            #print(step[0],rowheight)
            test_row = [step, expected, actual, note]
            self.test_case_table.insert(test_row)
        self.setTestStatus(test_case["Test Status"])
        if not handle_actual_results:
            return
        preconditions = test_case["Preconditions"] if test_case["Preconditions"] is not None else ""
        self.preconditions_text.clear()
        self.preconditions_text.insert([preconditions])

        #if not self.actual_results_displayed:
        #    self.show_actual_result(change_status=False)
        #    print(0)
        if not self.actual_results_displayed:
            self.hide_actual_result(change_status=False)

    def updateTestStatus(self, status):
        self.test_cases[self.current_test_index].set_status(status)
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

    def _update_test_execution_id(self):
        self.test_execution_id = self.execution_id_input.get()


    def saveResults(self):
        self._update_test_execution_id()
        self.test_execution_id = self.execution_id_input.get().strip()

        if not self.file_loaded_from_output and not self.test_execution_id:
            messagebox.showwarning("Error", "Test Execution ID is required!")
            return

        if self.file_loaded_from_output:
            output_file_name = self.file_name
        else:
            output_file_name = f"{self.default_exports_prefix}{self.test_execution_id}.json"

        # read data from tables
        if not self.editing_disabled:
            data_from_table = self.test_case_table.return_test_steps()
            self.test_cases[self.current_test_index].set_test_steps(data_from_table)
        #if isinstance(self.test_cases, str):
        #    test_case_data_to_save.insert(0, self.test_cases[0])
        test_case_data_to_save = [tc.dict_to_save() for tc in self.test_cases if isinstance(tc, TestCaseModel)]
        test_case_data_to_save.insert(0, "from_output")
        with open(output_file_name, "w") as file:
            json.dump(test_case_data_to_save, file, indent=4)

        if self.show_save_info:
            messagebox.showinfo("Info", f"This pop-up is shown once per session!\nResults saved to {output_file_name}")
            self.show_save_info = False
        #self.test_cases.remove("from_output")

    def loadTestsFromRawData(self, raw_data: list[dict]):
        for i, test_case in enumerate(raw_data):
            if isinstance(test_case, str):
                if test_case == "from_output":
                    continue
            try:
                tc = TestCaseModel(
                        test_case_id=test_case["Test Case Id"],
                        test_case_name=test_case["Test Case Name"],
                        area=test_case["Area"],
                        level=test_case["Level"],
                        test_steps=test_case["Test Steps"],
                        #expected_results=test_case["Test Steps"][1],
                        #actual_results=test_case["Test Steps"][2] if len(test_case["Test Steps"]) > 2 else None,
                        #notes=test_case["Test Steps"][3] if len(test_case["Test Steps"]) > 3 else None,
                        test_status=test_case.get("Test Status"),
                        preconditions=test_case.get("Preconditions"), 
                        assignee=test_case.get("Assignee"),
                        gsheet_document_id=test_case.get("Gsheet Document Id")
                        )
                self.test_cases.append(tc)
            except TypeError as e:
                print(test_case)
                messagebox.showwarning(title=self.app_name, message=f"Could not convert '{test_case}' to Test Case due to TypeError: {e}")
            except KeyError as e:
                print(test_case)
                messagebox.showerror(title=self.app_name, message=f"Could not load test case with index {i} due to KeyError: {e}!")

    def loadJson(self, file_path: str) -> list[dict]:
        with open(file_path, "r") as file:
            data = json.load(file)
        return data 

    def loadXlsx(self, file_path: str) -> list:
        try:
            from openpyxl import load_workbook
        except ImportError:
            err_msg = "Could not load openpyxl!\nInstall openpyxl or import json file!"
            messagebox.showerror(title="PyTestCases Error: Could not load Xlsx", message=err_msg)
            raise ImportError(err_msg)
        wb = load_workbook(file_path)
        try:
            ws = wb[self.xlsx_test_cases_sheet_name]
        except KeyError:
            messagebox.showerror(title=self.app_name, message=f"Did not detect sheet with name '{self.xlsx_test_cases_sheet_name}'!")
            return

        column_names = [cell.value for cell in ws[self.column_names_row]]

        raw_data = []
        current_test_case = None
        current_test_steps = []
        current_test_preconditions = ""

        for row in ws.iter_rows(min_row=self.test_case_data_starting_row, values_only=True):
            row_data = dict(zip(column_names, row))

            if current_test_case and row_data["Test Case Id"] != current_test_case["Test Case Id"]:
                tc = {
                    "Test Case Id": current_test_case["Test Case Id"],
                    "Test Case Name": current_test_case["Test Case Name"],
                    "Area": current_test_case["Area"],
                    "Level": current_test_case["Level"],
                    "Preconditions": current_test_preconditions,
                    "Test Steps": current_test_steps,
                    "Test Execution Id": current_test_case.get("Test Execution Id"),
                    "Test Status": current_test_case.get("Test Status"),
                    "Assignee": current_test_case.get("Assignee"),
                    "Gsheet Document Id": current_test_case.get("Gsheet Document Id")
                }
                raw_data.append(tc)
                current_test_steps = []
                current_test_preconditions = ""

            current_test_case = row_data
            current_test_steps.append([row_data["Test Step Description"], row_data["Expected Result"]])
            current_test_preconditions += (str(row_data["Preconditions"]) + "\n") if row_data.get("Preconditions") is not None else ""
            print("===", current_test_case, "----")
            print(current_test_case.get("Preconditions"))


        if current_test_case:
            tc = {
                    "Test Case Id": current_test_case["Test Case Id"],
                    "Test Case Name": current_test_case["Test Case Name"],
                    "Area": current_test_case["Area"],
                    "Level": current_test_case["Level"],
                    "Preconditions": current_test_preconditions,
                    "Test Steps": current_test_steps,
                    "Test Execution Id": current_test_case.get("Test Execution Id"),
                    "Test Status": current_test_case.get("Test Status"),
                    "Assignee": current_test_case.get("Assignee"),
                    "Gsheet Document Id": current_test_case.get("Gsheet Document Id")
                }
            raw_data.append(tc)

        while raw_data[-1] is None:
            self.test_cases.pop()
        return raw_data
        self.test_cases += raw_data

        #while self.test_cases[-1]["Test Case ID"] is None:
        #    self.test_cases.pop()



        


if __name__ == "__main__":
    app = PyTestCasesApp()
    app.mainloop()

