import sys

from src.PyTestCaseApp import PyTestCasesApp

if __name__ == "__main__":
    start_maximized = "-m" in sys.argv
    app = PyTestCasesApp(start_maximized=start_maximized)
    app.mainloop()
