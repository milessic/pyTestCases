from os import walk
from tkinter.messagebox import askretrycancel

import json

class TestCaseModel:
    def __init__(
            self,
            test_case_id:int,
            test_case_name:str,
            area:str,
            level:str,
            test_steps:list[list[str]],
            #expected_results:list[str],
            #actual_results:list[str]|None,
            #notes:list[str]|None,
            preconditions:str|None,
            test_status:str|None,
            assignee:str|None,
            gsheet_document_id:str|None,
            ):
        self.test_case_id = test_case_id
        self.test_case_name = test_case_name
        self.area = area
        self.level = level
        # Test Step Description, Expected Result, Actual Result, Notes
        self.test_steps = [[], [],[], []]
        self.insert_test_steps(test_steps)
        self.insert_expected_results(test_steps)
        self.insert_actual_results(test_steps)
        self.insert_notes(test_steps)
        # back to normal fields
        self.preconditions = preconditions
        self.test_status = test_status
        self.assignee = assignee
        self.gsheet_document_id = gsheet_document_id

    def __str__(self):
        return f"{self.test_case_id} - [{self.test_status[0] if self.test_status is not None else 'N'}] - {self.test_case_name}"
    
    def dict(self) -> dict:
        as_dict = {}
        for field in self.__dir__():
            if field.startswith("__"):
                continue
            value = getattr(self, field) 
            if type(value).__name__ =="method":
                continue
            # change names to human
            field_human = field.replace("_", " ").title()
            as_dict[field_human] = value
        return as_dict
    
    def dict_to_save(self) -> dict:
        # load as dict
        as_dict = self.dict()
        # merge test_steps
        try:
            reconfigured_steps = [(s,e,a,n) for s,e,a,n in zip(
            self.test_steps[0],
            self.test_steps[1],
            self.test_steps[2],
            self.test_steps[3],
            )]
            del as_dict["Test Steps"]
            as_dict["Test Steps"] = reconfigured_steps
        except:
            print("ERRROERORERE!")
            print(self.test_steps)
            raise
        # return
        return as_dict

    def set_status(self, status):
        self.test_status = status

    def set_test_steps(self, test_steps:list):
        r"Sets Description, Exptected and Actual"
        self.test_steps[0] = test_steps[0]
        self.test_steps[1] = test_steps[1]
        self.test_steps[2] = test_steps[2]

    def insert_test_steps(self, test_steps:list[str]):
        for step in test_steps:
            self.test_steps[0].append(step[0])

    def insert_expected_results(self, test_steps:list[str]):
        for step in test_steps:
            self.test_steps[1].append(step[1])

    def insert_actual_results(self, test_steps:list[str]):
        if len(test_steps[0]) > 2:
            for step in test_steps:
                self.test_steps[2].append(step[2])
            return
        for _ in test_steps[0]:
            self.test_steps[2].append("")

    def insert_notes(self, test_steps:list[str]):
        if len(test_steps[0]) > 3:
            for step in test_steps:
                self.test_steps[3].append(step[3])
            return
        for _ in test_steps[0]:
            self.test_steps[3].append("")




