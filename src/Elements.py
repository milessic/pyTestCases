import re
from tkinter import (
    END, Tk, StringVar, Label, Entry, Button, Frame, filedialog, messagebox, ttk, Misc, Text, Toplevel
)
from tkinter.constants import WORD

def myText(master:Misc, stylesheet, width,height, wrap, **kwargs) -> Text:
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
            **kwargs
            )
def myEntry(master:Misc, stylesheet, width, **kwargs) -> Entry:
    return Entry(
            master=master,
            background=stylesheet.txt_bg,
            highlightcolor=stylesheet.bg,
            highlightbackground=stylesheet.bg,
            width=width,
            fg=stylesheet.txt_fg,
            border=0,
            **kwargs
            )
class Table:
    def __init__(self, root: Misc, column_headers:list, column_width:int, stylesheet, fixed_grid:bool|list=False):
        r"""
        - column_width - in characters, e.g. "word" has 4 characters
        """
        self.tooltips = []
        self.fixed_grid = fixed_grid
        self.s = stylesheet
        self.root = root
        self.table_width = column_width
        self.column_count = len(column_headers)
        self.column_headers = column_headers
        self.test_case_rows = 0
        self.test_step_i = 0
        self.previous_row_h = 0
        self.table = [[]]
        self.row_height = 1
        self.x = 0
        self.y = 0
        self.clear()
    
    def clear(self):
        # destory tooltips
        for t in self.tooltips:
            del t
        self.tooltips=[]
        self.previous_row_h = 0
        self.test_case_rows = 10
        for row in self.table:
            for cell in row:
                #cell.pack_forget()
                #cell.grid_remove() # it is little more smooth, but creates a lot of elements
                cell.destroy()
        self._create_row(self.column_headers)
        self.x = 1
        self.test_step_i = 0

    def hide_actual(self):
        for row in self.table:
            for i, cell in enumerate(row):
                if i == 2:
                    try:
                        cell.grid_remove()
                    except Exception:
                        continue
                        #raise

    def hide_whole(self):
        for row in self.table:
            for cell in row:
                try:
                    cell.grid_remove()
                except Exception as e:
                    print(cell)
                    print(e)
                    continue

    def show_whole(self):
        row_pos, column_pos = 0,0
        for row in self.table:
            for cell in row:
                try:
                    cell.grid(row=row_pos, column=column_pos)
                except Exception:
                    continue
                finally:
                    column_pos += 1
            row_pos += 1
            column_pos = 0

    def return_test_steps(self) -> list[list]:
        test_steps = [[],[],[],[]]
        children = self.root.winfo_children()
        row_i, column_i = 0, 0
        for c in children:
            locator = str(c)
            if "cell_" not in locator:
                continue
            cell_text = c.get("1.0", END)
            while cell_text.endswith("\n"):
                cell_text = cell_text.removesuffix("\n")
            if f"cell_{row_i}_" in locator:
                column_from_locator = int(re.sub(r"[\s\S]*_","",locator))
                test_steps[column_from_locator].append(cell_text)
            elif f"cell_{row_i+1}_" in locator:
                column_from_locator = int(re.sub(r"[\s\S]*_","",locator))
                test_steps[column_from_locator].append(cell_text)
                row_i += 1
        return test_steps
                
        for i, c in enumerate(children):
            locator = str(c)
            if "cell_" not in locator:
                continue
            if f"cell_{row_i}" in locator:
                test_steps

            print("---",c.get("1.0", END),"--")


    def insert(self, row:list):
        if len(row) != self.column_count + 1:
            messagebox.showerror(title="PyTestCases", message=f"Provided data contained {len(row)}, expected {self.column_count}")
            return
        self._create_row(row)
        self.test_step_i += 1

    def _create_row(self, row:list[str]):
        expected_cell = None
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
        for i, column in enumerate(row):
            cell_x = self.x+self.test_case_rows
            cell_y = self.y
            cell = myText(
                        self.root,
                        stylesheet=self.s,
                        width=self.table_width,
                        height=height,
                        wrap=WORD,
                        name=f"tc_cell_{self.test_step_i}_{cell_y}"
                        )
            cell.insert(END, column)
            #cell.grid(row=self.x+self.test_case_rows, column=self.y, pady=(self.previous_row_h*xx))
            if i != 3: # Notes
                # TODO why?
                if isinstance(self.fixed_grid, bool) and not self.fixed_grid:
                    cell.grid(row=cell_x, column=cell_y, pady=(self.previous_row_h*xx))
                else:
                    cell.grid(row=self.fixed_grid[0], column=self.fixed_grid[1])
            if i == 3:
                if column == "" or column is None:
                    continue
                print(expected_cell)
                self.tooltips.append(
                        CreateToolTip(
                        expected_cell,
                        text=column
                        )
                )
                expected_cell.config(
                        highlightcolor="blue",
                        highlightbackground="blue",
                        )

                #tooltip.grid(row=cell_x, column=cell_y)
            self.y += 1
            misc_row.append(cell)
            if i == 1:
                expected_cell = cell
        self.test_case_rows += self.previous_row_h
        self.table.append(misc_row)
        self.y = 0
        self.previous_row_h = height * 20  + (max_characters//self.table_width)
            

class CreateToolTip(object):
    """
    create a tooltip for a given widget
    """
    def __init__(self, widget, text='widget info'):
        self.waittime = 50     #miliseconds
        self.wraplength = 180   #pixels
        self.widget = widget
        self.text = text
        self.widget.bind("<Enter>", self.enter)
        self.widget.bind("<Leave>", self.leave)
        self.widget.bind("<ButtonPress>", self.leave)
        self.id = None
        self.tw = None

    def enter(self, event=None):
        self.schedule()

    def leave(self, event=None):
        self.unschedule()
        self.hidetip()

    def schedule(self):
        self.unschedule()
        self.id = self.widget.after(self.waittime, self.showtip)

    def unschedule(self):
        id = self.id
        self.id = None
        if id:
            self.widget.after_cancel(id)

    def showtip(self, event=None):
        x = y = 0
        x, y, cx, cy = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 20
        # creates a toplevel window
        self.tw = Toplevel(self.widget)
        # Leaves only the label and removes the app window
        self.tw.wm_overrideredirect(True)
        self.tw.wm_geometry("+%d+%d" % (x, y))
        label = Label(
                self.tw,
                text=self.text,
                justify='left',
                    background="#ffffff", relief='solid', borderwidth=1,
                       wraplength = self.wraplength)
        label.pack(ipadx=1)

    def hidetip(self):
        tw = self.tw
        self.tw= None
        if tw:
            tw.destroy()
