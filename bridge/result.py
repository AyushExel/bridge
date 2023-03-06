from typing import List

class Result:
    def __init__(self, name:str, success: bool, logs: List[str]) -> None:
        self.name = name
        self.success = success
        self.logs = logs
        
    
    def __str__(self) -> str:
        return f" {self.name} " + f"{'success' if self.success else 'fail'} \n" + ''.join([log+'\n' for log in self.logs])


    def write(self, name: str):
        # TODO:
        raise NotImplementedError
