import sys
import configparser

from src.PyTestCaseApp import PyTestCasesApp

if __name__ == "__main__":
    config = configparser.ConfigParser()
    config.read(".config.ini")
    try:
        column_names_row = config["XLSX"]["ColumnNamesRow"]
    except KeyError:
        column_names_row = 3
    try:
        test_cases_data_starting_row = config["XLSX"]["TestCasesDataStartingRow"]
    except KeyError:
        test_cases_data_starting_row = 4
    try:
        test_case_data_worksheet_name = config["XLSX"]["TestCaseDataWorksheetName"]
    except KeyError:
        test_case_data_worksheet_name = "TEST CASES"
    try:
        theme = config["APPEARANCE"]["VisualTheme"]
    except KeyError:
        theme = "black"
    try:
        actual_results_enrolled = config["APPEARANCE"]["ActualResultsEnrolled"]
    except KeyError:
        actual_results_enrolled = True
    try:
        always_on_top = config["APPEARANCE"]["AlwaysOnTop"]
    except KeyError:
        always_on_top = True
    try:
        table_column_width = config["APPEARANCE"]["TableColumnWidth"]
    except KeyError:
        table_column_width = 30
    try:
        preconditions_enrolled = config["APPEARANCE"]["PreconditionsEnrolled"]
    except KeyError:
        preconditions_enrolled = True
    try:
        default_export_prefix = config["EXPORTS"]["DefaultExportPrefix"]
    except KeyError:
        default_export_prefix = "output_"

    # row_width
    for arg in sys.argv:
        print(arg)
        if arg.startswith("--not-on-top") or arg.startswith("--notonstop"):
            always_on_top = False
            continue
        if arg.startswith("--column-width"):
            try:
                table_column_width = int(arg.split("-")[-1])
            except Exception as e:
                raise ValueError(f"Could not set column_width due to '{arg}'")
            finally:
                continue
        if arg.startswith("--theme"):
            try:
                theme = arg.split("-")[-1]
            except Exception as e:
                raise ValueError(f"Could not set theme name due to '{arg}' {e}")
            finally:
                continue
        print("end")



    app = PyTestCasesApp(
            theme=theme,
            actual_results_displayed=actual_results_enrolled,
            always_on_top=always_on_top,
            column_width=table_column_width,
            preconditions_displayed=preconditions_enrolled,
            default_exports_prefix=default_export_prefix,
            column_names_row=column_names_row,
            test_case_data_starting_row=test_cases_data_starting_row,
            xlsx_test_cases_sheet_name=test_case_data_worksheet_name
            )
    app.update()
    app.mainloop()
