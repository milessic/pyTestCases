import sys

from src.PyTestCaseApp import PyTestCasesApp

if __name__ == "__main__":
    start_maximized = False
    dont_keep_on_top = False
    theme_name = None
    table_width = 60
    # row_width
    for arg in sys.argv:
        print(arg)
        if arg.startswith("-m"):
            start_maximized = True
            continue
        if arg.startswith("--not-on-top") or arg.startswith("--notonstop"):
            dont_keep_on_top = True
            continue
        if arg.startswith("--table-width"):
            try:
                table_width = int(arg.split("-")[-1])
            except Exception as e:
                raise ValueError(f"Could not set column_width due to '{arg}'")
            finally:
                continue
        if arg.startswith("--theme"):
            try:
                theme_name = arg.split("-")[-1]
                print(theme_name)
            except Exception as e:
                raise ValueError(f"Could not set theme name due to '{arg}' {e}")
            finally:
                continue
        print("end")



    app = PyTestCasesApp(start_maximized=start_maximized, table_width=table_width, theme=theme_name)
    if not dont_keep_on_top:
        app.attributes("-topmost", True)
    app.update()
    app.mainloop()
