import json
from typing import List, Any
from pathlib import Path

import bridge.contracts as C
from bridge.contracts import Contract

class Executor:
    def __init__(self, config: Path, target: Any=None) -> None:
        self.contracts: List[Contract] = self.parse_config(config)
        self.target = target # TODO: this be used to enforce the same contract for different entities?
    
    def parse_config(self, config: Path):
        config = json.load(open(config))
        contracts = []
        for contract in config.keys():
            contracts.append(
                eval("C."+contract)(config[contract]) # WARN Unsafe eval
            )
        
        return contracts

    def enforce(self):
        results = []
        for contract in self.contracts:
            results.append(contract.enforce())
        
        # Log successes before failures
        results.sort(key=lambda x: len(x.logs), reverse=True)
        for result in results:
            print(result)
