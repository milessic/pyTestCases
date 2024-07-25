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
```
<column 3>| Test Case Id | Feature | Level | Test Case Name | Test Steps | Preconditions | Test Step Description | Expected Results |
<column 4+> {Test Cases Data}
```

# Saving and loading sessions
Sessinos are saved after clicking one of ``Status button`` at the bottom.

All generated ``output files`` have first item set as ``"from_output"``, which changes the way the program saves such file.

It is possible to open already saved ``output file``, but then there is no possibility to change ``Test Execution ID``.

# Roadmap
- [ ] Add Preconditions
- [ ] Make xlsx importing more flexible
- [ ] Add Test Case Creation
- [ ] Add Test Case Edidtion
- [ ] Add Test Case filtering
- [ ] Add Test Report functionaltiy
- [ ] Add Support for light mode ( currently pastel colors are to pastel and barely visible on light mode )

