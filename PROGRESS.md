# Versions
## v 0.1
### General
- [x] - Make app resizable
- [x] - Make Test Case Details section scrollable in better way
- [x] - Resize Test Case name to be fully shown
- [x] - Move Test Execution Id input to be aksed when saving

### Appearance
- [x] - Style status buttons
    - [x] All contents must fit
    - [x] colors
- [x] Make Test Section scrollable
    - [x] Scrollable if table.height > ``.config.max_test_section_height``
- [ ] Improve widget spacing
- [x] Create Test Status layout
    - [x] - Move Assignee here
    - [x] - move Test Status labels here

### Imports
- [ ] - Xlsx
    - [x] - Don't ask for sheet name, give dropdown with options instead
    - [ ] - Make sheet name window on top

### Exports
- [ ] - Xlsx
    - [ ] - Move export path to details


## v 0.
### General
- [ ] -

### Appearance
- [ ] - 

### Imports
- [ ] - 

### Exports
- [ ] - 

# Tasks
- [ ] Create .config file and it's handling
    - [x] config support
    - [x] Xlsx settings
        - [x] Xlsx Field Names row ``3``
        - [x] Xlsx import starting row ``4``
        - [x] Xlsx Test Cases worksheet name ``TEST CASES``
    - [x] Default UI
        - [x] App Theme ``BlackTheme``
        - [x] ``Actual Result`` Enrolled ``True``
        - [x] Always-on-top ``True``
        - [x] Table column width ``30``
        - [x] Max Test Section height ``??``
    - [x] Export settings
        - [x] Default prefix ``output_``
- [ ] Import from file improvements 
    - [x] Change the import to import all ``Supported Fields``
    - [ ] Make field importing case-sensitivity-proof (always use Title Case)
    - [ ] Make importing asynchronous
- [ ] Import from gSheet
    - [ ] ??
- [x] Add Preconditions
    - [x] As a ``Text`` above Test Table, enrollable
    - [x] Make a label that will indicate that there is some precondition if it is collapsed
- [x] Add Notes
    - [x] Add a highlight if there are some notes
- [ ] Enhance Notes
    - [ ] As a Custom blue "N" Element, in the top right corner of the ``Expected Result``
    - [ ] If opened, text from here can be copied
    - [ ] Can be closed by clicking on the "x" button, or anywhere else in the applicaiton
- [x] Add assignee field
    - [x] show it if it is not ``null``
- [ ] Make xlsx importing more flexible
    - [x] open workbook with name ``<TEST CASES SHEET NAME>``
    - [x] make it possible to change the starting row
    - [ ] import xlsx values not formulas
- [ ] Add Test Case Edidtion
    - [x] Gather input from ``Test Step``, ``Expected Result``, ``Actual Result``
    - [ ] Add possibility to edit ``source file``
- [ ] Add Test Case filtering
    - [ ] Filtering by ``Area``
    - [ ] Filtering by ``Level``
- [ ] Create custom Frame
    - [ ] ``Minimize``, ``Close``, ``Title``
    - [ ] Enable drag-and-drop via all background
- [ ] Focus modes
    - [ ] Make top panel enrollable horizontally
    - [x] Make Expected Result enrollable vertically
- [ ] Recognition that there were changes in ``Test Step`` or ``Expected Result``
    - [ ] Add `` - [!e]`` to the ``Test Case Name``, but do not save it with it
    - [ ] Make a green ``!`` to top-left conrer of edited ``Test Step`` / ``Expected Result``
    - [ ] Make a green ``!`` next to Exports (``Xlsx``, ``Csv``, ``gSheet``)
    - [ ] If exporting as (``Xlsx``, ``Csv``, ``gSheet``), ask if export with new data
- [ ] Exports
    - [x] Create a template for ``text`` Exports
    - [ ] MD support
    - [x] Jira Markdown support
    - [ ] HTML support
    - [x] Xlsx support
        - [ ] import xlsx values and formulas, (for xlsx importsave)
    - [ ] Csv support
    - [ ] gSheet support
        - [ ] gSheet connection
        - [ ] ``Gsheet Document Id`` value handling
        - [ ] ``Gsheet Document Id`` pop-up
        - [ ] Gsheet Document Name validation
- [x] Add Support for light mode ( currently pastel colors are to pastel and barely visible on light mode )
- [x] Add support of openpyxl optional
- [ ] Add Test Case Creation

