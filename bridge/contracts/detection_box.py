import os
import glob
from typing import Dict
from multiprocessing.pool import ThreadPool
from itertools import repeat
from argparse import Namespace

import numpy as np

from bridge.contracts import Contract
from bridge.result import Result


class DetectionBoxBounds(Contract):
    """
    Detection bounding box contracts. Ensures
        * The box bounds is normalized and within the frame
        * The number of co-ordinated per label satisfies the format
        * Class index is within bounds
        * There are no negative co-ordinates
        
    """
    def __init__(self, args: Dict) -> None:
        super().__init__(args)
        self.args = self._build_contract_args() # dict
        self.args = Namespace(**self.args) # Temp

    def params(self):
        args = {
            "path": None,
            "format": "yolo", # TODO: auto-detector
            "num_classes": 80
        }

        return args
  
    def enforce(self):
        # Contract enforcement logic
        failed_logs = []
        label_files = glob.glob(self.args.path + '/*.txt')
        with ThreadPool(4) as pool:
            results = pool.map(verify_txt_label, zip(label_files, repeat(self.args.num_classes)))

        for idx,  r in enumerate(results):
            failed_logs.append(f"{label_files[idx]} : " + r) if r else None

        return Result(name=self.__class__.__name__, success=len(failed_logs)==0, logs=failed_logs)


def verify_txt_label(args):
    lb_file, num_cls = args
    failed_log = ''
    # verify labels
    if os.path.isfile(lb_file):
        nf = 1  # label found
        with open(lb_file) as f:
            lb = [x.split() for x in f.read().strip().splitlines() if len(x)]
            lb = np.array(lb, dtype=np.float32)
        nl = len(lb)
        if nl:
            if lb.shape[1] != 5:
                failed_log += f'labels require 5 columns, {lb.shape[1]} columns detected \n'

            if not (lb[:, 1:] <= 1).all():
                failed_log += f'non-normalized or out of bounds coordinates {lb[:, 1:][lb[:, 1:] > 1]} \n'
    
            # All labels
            max_cls = int(lb[:, 0].max())  # max label count
            if max_cls > num_cls:
                failed_log += f'Label class {max_cls} exceeds dataset class count {num_cls}. \n'
                
            if not (lb >= 0).all():
                failed_log += f'negative label values {lb[lb < 0]} \n'
                
    return failed_log
