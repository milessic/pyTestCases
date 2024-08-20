class Formatting:
    formatting_dict = {
            "jira":{
                "bullet": "* ",
                "ordered": "# ",
                "h1": ".h1 ",
                "h2": ".h2 ",
                "h3": ".h3 ",
                "h4": ".h4 ",
                "h5": ".h5 ",
                "line_divider": "----"
                }
            }
    def __init__(self, format:str):
        self.format = format
        self.f = self.setup()

    def setup(self) -> dict:
        return self.formatting_dict[self.format]
        
