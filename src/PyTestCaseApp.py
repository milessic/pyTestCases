import json
from pathlib import Path
from time import time
from tkinter import (
    END, Tk, StringVar, Label, Entry, Button, Frame, filedialog, messagebox, ttk, Misc, Text
)
from tkinter.constants import WORD

def myText(master:Misc, stylesheet, width,height, wrap) -> Text:
    return Text(
            master=master,
            bg=stylesheet.txt_bg,
            fg=stylesheet.txt_fg,
            highlightcolor=stylesheet.bg,
            highlightbackground=stylesheet.bg,
            width=width,
            wrap=wrap,
            height=height,
            border=1,
            )
def myEntry(master:Misc, stylesheet, width) -> Entry:
    return Entry(
            master=master,
            background=stylesheet.txt_bg,
            highlightcolor=stylesheet.bg,
            highlightbackground=stylesheet.bg,
            width=width,
            fg=stylesheet.txt_fg,
            border=0
            )

class Colors:
    black = "black"
    red = "#ffb3ba"
    green = "#baffc9"
    yellow = "#ffdfba"
    gray = "#ababab"


class LightGrayTheme:
    bg = "#f0f0f0"
    highlight = "#d9d9d9"
    fg = "#333333"
    txt_bg = "#ffffff"
    txt_fg = "#4f4f4f"
    btn_highlight = "#cccccc"
    status_bg = "#e6e6e6"

class BlackTheme:
    bg = "#000000"
    highlight = "#1a1a1a"
    fg = "#ffffff"
    txt_bg = "#2b2b2b"
    txt_fg = "#eaeaea"
    btn_highlight = "#4d4d4d"
    status_bg = "#151515"

class WhiteTheme:
    bg = "#ffffff"
    highlight = "#f2f2f2"
    fg = "#000000"
    txt_bg = "#e6e6e6"
    txt_fg = "#333333"
    btn_highlight = "#cccccc"
    status_bg = "#f7f7f7"

class BlueTheme:
    bg = "#007acc"
    highlight = "#005999"
    fg = "#ffffff"
    txt_bg = "#cce7ff"
    txt_fg = "#003366"
    btn_highlight = "#66b2ff"
    status_bg = "#004080"

class RedTheme:
    bg = "#b30000"
    highlight = "#800000"
    fg = "#ffffff"
    txt_bg = "#ffcccc"
    txt_fg = "#330000"
    btn_highlight = "#ff6666"
    status_bg = "#660000"

class DarkBlueTheme:
    bg = "#22303c"
    highlight = "#9DB2BF"
    fg = "#ffffff"
    txt_bg ="#FFFDFA" 
    txt_fg ="#15202b" 
    btn_highlight="#ffffff"
    status_bg = "#6b6967"

class PastelTheme:
    bg = "#ffd1dc"
    highlight = "#ffb3c1"
    fg = "#4b0082"
    txt_bg = "#fff0f5"
    txt_fg = "#800080"
    btn_highlight = "#ff69b4"
    status_bg = "#ff80bf"


selectedStyle = DarkBlueTheme
class Styles:
    def __init__(self, theme_name:str):
        default_theme = BlackTheme
        match theme_name.lower():
            case "darkblue":
                stylesheet = DarkBlueTheme
            case "lightgray":
                stylesheet = LightGrayTheme 
            case "black":
                stylesheet = BlackTheme
            case "white":
                stylesheet = WhiteTheme
            case "blue":
                stylesheet = BlueTheme
            case "red":
                stylesheet = RedTheme
            case "pastel":
                stylesheet = PastelTheme
            case "none":
                stylesheet = default_theme
            case _:
                print(f"Theme not supported - '{theme_name}'!")
                stylesheet = default_theme
        for k,v in stylesheet.__dict__.items():
            if k.startswith("__"):
                continue
            setattr(self, k,v)


class Table:
    def __init__(self, root: Misc, column_headers:list, column_width:int, stylesheet):
        r"""
        - column_width - in characters, e.g. "word" has 4 characters
        """
        self.s = stylesheet
        self.root = root
        self.table_width = column_width
        self.column_count = len(column_headers)
        self.column_headers = column_headers
        self.test_case_rows = 1
        self.previous_row_h = 0
        self.table = [[]]
        self.row_height = 1
        self.x = 0
        self.y = 0
        self.clear()
    
    def clear(self):
        self.previous_row_h = 0
        self.test_case_rows = 10
        for row in self.table:
            for cell in row:
                #cell.pack_forget()
                cell.grid_remove()
        self._create_row(self.column_headers)
        self.x = 1

    def insert(self, row:list):
        if len(row) != self.column_count:
            messagebox.showerror(f"Provided data contained {len(row)}, expected {self.column_count}")
            return
        self._create_row(row)

    def _create_row(self, row:list[str]):
        xx = 0 # just to keep previous_r_h calculation at end inactive
        misc_row = []
        # calculate row height
        max_lines = 1
        max_characters = 0
        for column in row:
            column_lines = column.count("\n") + 1
            column_rows = column.split("\n")
            for c_row in column_rows:
                row_len = len(c_row)
                if row_len > self.table_width:
                    column_lines += (row_len // self.table_width)
            max_characters = max(max_characters, len(column))
            max_lines = max(max_lines, column_lines)
        height = self.row_height * (max_lines)
        # Create text elements
        for column in row:
            cell = myText(
                        self.root,
                        stylesheet=self.s,
                        width=self.table_width,
                        height=height,
                        wrap=WORD
                        )
            cell.insert(END, column)
            cell.grid(row=self.x+self.test_case_rows, column=self.y, pady=(self.previous_row_h*xx))
            self.y += 1
            misc_row.append(cell)
        self.test_case_rows += self.previous_row_h
        self.table.append(misc_row)
        self.y = 0
        self.previous_row_h = height * 20  + (max_characters//self.table_width)
            


class PyTestCasesApp(Tk):
    def __init__(self, start_maximized: bool = False, table_width:int=60, theme:str | None = None):
        super().__init__()
        self.resizable(0, 0) 
        theme = str(theme)
        self.s = Styles(theme_name=theme)
        self.config(bg=self.s.bg)
        self.show_save_info = True
        self.test_cases = []
        self.column_width = int(table_width/2)
        self.current_test_index = 0
        self.test_execution_id = None
        #self.geometry("520x300")
        self.start_maximized = start_maximized
        self.initUI()
        self.style = ttk.Style(self)
        if self.start_maximized:
            print("Window maximized Not supported!")
            #self.attributes('-fullscreen', True)

    def initUI(self):
        # setup Window Title
        self.title("pyTestCases")

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



        # setup Test Case Table
        #self.test_case_table = ttk.Treeview(self, columns=("Description", "Expected Result"), show='headings')
        # TODO labels for Test Case Table
        self.table_test_case_frame = self.myFrame(self)
        self.test_table_column_step = self.myLabel(self.table_test_case_frame, text="Test Step", bold=True)
        self.test_table_column_expected = self.myLabel(self.table_test_case_frame, text="Expected Result", bold=True)
        self.test_case_table = Table(self.table_test_case_frame, column_headers=["Description", "Expected Result"], column_width=self.column_width, stylesheet=self.s)

        self.test_table_column_step.grid(row=0,column=0)
        self.test_table_column_expected.grid(row=0,column=1)
        self.table_test_case_frame.grid(row=5, column=0, columnspan=3, padx=5, pady=5)
        #self.test_case_table.heading("Description", text="Description")
        #self.test_case_table.heading("Expected Result", text="Expected Result")
        #self.test_case_table.column("Description", width=300)
        #self.test_case_table.grid(row=4, column=0, columnspan=3, padx=5, pady=5, sticky="nsew")

        # setup Buttons and their functions
        self.button_frame = self.myFrame(self)
        self.button_frame.grid(row=4, column=0, columnspan=3, padx=0, pady=5)

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

    def myLabel(self, master:Misc, text:str, bold:bool=False) -> Label:
        if bold:
            return Label(
                master=master,
                text=text,
                bg=self.s.bg,
                fg=self.s.fg,
                font="bold"
                )
        else:
            return Label(
                master=master,
                text=text,
                bg=self.s.bg,
                fg=self.s.fg,
                )

    def myCombobox(self, master:Misc, textvariable, width) -> ttk.Combobox:
        return ttk.Combobox(
                master=master,
                textvariable=textvariable,
                width=width,
                background=self.s.txt_bg,
                cursor="cross"

                
                )

    def myButton(self, master, text:str, command, fg=None, bg=None) -> Button:
        return Button(
                master=master,
                text=text,
                command=command,
                background=self.s.bg if bg is None else bg,
                fg=self.s.fg if fg is None else fg,
                highlightcolor=self.s.btn_highlight,
                highlightbackground=self.s.btn_highlight,
                activebackground=self.s.btn_highlight,
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

        self.test_case_table.clear()
        #for row in self.test_case_table.get_children():
        #    self.test_case_table.delete(row)

        for step in test_case["Test Steps"]:
            #lines_step = step[0].count("\n")
            #lines_expected = step[1].count("\n")
            #rowheight = max(lines_step, lines_expected) * 20
            #rowheight = rowheight if rowheight else 20
            #print(step[0],rowheight)
            self.test_case_table.insert(step)
        self.setTestStatus(test_case["Test Status"])

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
        try:
            from openpyxl import load_workbook
        except ImportError:
            err_msg = "Could not load openpyxl!\nInstall openpyxl or import json file!"
            messagebox.showerror(title="PyTestCases Error: Could not load Xlsx", message=err_msg)
            raise ImportError(err_msg)
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

