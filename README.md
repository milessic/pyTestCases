# PyTestCases
Simple Application to run and manage test cases written in PyQt5

# About app
Test Case app that loads test cases from ``Json`` or ``xlsx`` file and enables test execution.
test data from file format:

> [!WARNING]
> Xlsx supports only 1 very specific format of files!

Example input data:
## Json format
```json
[
	{
		"Test Case ID": 1,
		"Test Case Name": "Verify user can use filters",
		"Area": "Dashboard",
		"Test Steps": [
			["Open Dashboard", "Dashboard is opened"],
			["Use Filter and run search", "Filters are applied and serach results are properly displayed"]
		]
		"Test Exection Id": null,
		"Test Status": null
	}
]
```

## Excel format
Tool will use ``TEST CASES`` worksheet by default

```
<column 3>| Test Case Id | Feature | Level | Test Case Name | Test Steps | Preconditions | Test Step Description | Expected Results |
<column 4+> {Test Cases Data}
```

Both ``Json`` or ``Excel`` files will be reffered as ``Database`` further.

## Supported fields:
| __Field__ | __Desciption__ | __Display__ |
| ---- | --- | --- |
| ``Test Case Id``* | ``int``, must be unique | Displayed in the title and Test Dropdown |
| ``Test Case Name``* | ``str`` | Displayed in the title and Test Dropdown |
| ``Area`` | ``str`` | Displayed in the dropdown, Tests may be filtered by ``Area`` |
| ``Level`` | ``str``  | eg. ``Smoke``, ``Regression`` |
| ``Test Step Description``* | ``str`` | Displayed under ``Test Step`` column |
| ``Expected Result``*  | ``str`` | Displayed under ``Expected Result`` column |
| ``Actual Result`` | ``str`` | Displayed under ``Actual Result`` column |
| ``Notes`` | ``str`` | Notes, displayed as small, blue "N" button, if clicked, it is opened |
| ``Test Execution Id`` | ``str`` or ``null`` | Displayed under ``Test Execution Id`` field | 
| ``Test Status`` | ``str`` or ``null`` that can be converted to Status (``PASS``, ``FAIL``, ``BLOCKED``, ``NOT TESTED``, ``null``)  | Displayed under ``Test Status`` element |
| ``Assignee`` | ``str`` or ``null`` | Displayed in the Assignee section, but only if there is at least 1 non-null value in the database |
| ``Gsheet Document Id``| ``str`` | Used in ``gSheet Export``, can be in all cells, can be in some, can be in one, but it will work only if there is one of them |

All fields marked with ``*`` are mandatory

``Test Step Description``, ``Expected Result`` and ``Actual Result`` will be merged to ``Test Steps`` as list of lists ``[[description], [expected], [actual]]``.

## UX and modulity
Application supports various focus modes.

Top section can be collapsed (from ``Test Execution Id`` to ``Test Dropdown`` and ``Test Status``)

``Actual Result`` column can be colapsed or enrolled
# Saving and loading sessions
Sessinos are saved after clicking one of ``Status button`` at the bottom.

All generated ``output files`` have first item set as ``"output_"``, which changes the way the program saves such file.

It is possible to open already saved ``output file``, but then there is no possibility to change ``Test Execution ID``.

## Exports
### Report MD
After clicking clicking ``Export`` Menu and selecting ``Report MD``, the Markdown report will be generated out of current execution.

### Report Jira
After clicking clicking ``Export`` Menu and selecting ``Report Jira``, the Jira Markdown report will be generated out of current execution.

### Report HTML
After clicking clicking ``Export`` Menu and selecting ``Report HTML``, the HTML report will be generated out of current execution.

### Xlsx
After clicking clicking ``Export`` Menu and selecting ``Xlsx``, the Xlsx file will be generated, with no formatting, just data

### Csv
After clicking clicking ``Export`` Menu and selecting ``Csv``, the Xlsx file will be generated, with no formatting, just data

### gSheet
After clicking clicking ``Export`` Menu and selecting ``gSheet``, the Xlsx file will create a new Sheet in Gsheet Document
> [!WARNING]
> If there is no unique entry for ``Gsheet Document Id`` field, it will ask the user for gSheet Docuemnt Id
Before it will populate gSheet with new worksheet, it will ask for confirmation with gSheet Document Name

