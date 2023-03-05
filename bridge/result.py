from typing import List

class Result:
    def __init__(self, name:str, success: bool, logs: List[str]) -> None:
        self.name = name
        self.success = success
        self.logs = logs
        
    
    def __str__(self) -> str:
        return f" {self.name} " + f"{'success' if self.success else 'fail'} \n {self.logs} \n"

    def write(self, name: str):
        # TODO:
        raise NotImplementedError
