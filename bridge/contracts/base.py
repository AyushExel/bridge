from typing import Dict

class Contract:
    """
    Abstract base class for contracts.
    """
    def __init__(self, args: Dict) -> None:
        self.args = args
    
    @property
    def params(self):
        """
        Get deafult values for all args required in json format. An arg is set to None if user input is mandatory

        Returns
            defaults (Dict[str]): default arguments
        """
        raise NotImplementedError

    def enforce(self):
        """
        To enforce the contract.

        Returns:
            result (Report)
        """
        raise NotImplementedError
    
    def _build_contract_args(self):
        """
        Merge the default args with user inputs. Check all args have a non-null value

        Returns:
           args (Dict[srt]): Final contract args
        """
        defaults = self.params()
        defaults.update(self.args)
        for k in defaults.keys():
            if not k:
                raise Exception("Configuration missing mandatory argument.")
        
        return defaults

    
