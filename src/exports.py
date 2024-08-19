class Formatting:
    formatting_dict = {
            "jira":{
                "bullet": "* ",
                "ordered": "# ",
                "h1": ".h1",
                "h2": ".h2"
                }
            }
    def __init__(self, format:str):
        self.format = format
        self.f = self.setup()

    def setup(self) -> dict:
        return self.formatting_dict[self.format]
        
