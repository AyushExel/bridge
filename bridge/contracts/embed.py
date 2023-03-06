import os
import glob
import logging
from typing import Dict
from PIL import Image
from argparse import Namespace
from sklearn.decomposition import PCA

import torch
import faiss
from img2vec_pytorch import Img2Vec

from bridge.contracts import Contract
from bridge.result import Result
from bridge.utils.globals import EXTENSIONS

class EmbeddingSimilarity(Contract):
    def __init__(self, args: Dict) -> None:
        super().__init__(args)
        self.args = self._build_contract_args() # dict
        self.args = Namespace(**self.args) # Temp
        # ------- #
        self.index = None
        self.is_initialized = None

    def params(self):
        args = {
            "path": None,
            "model": "resnet-18",
            "dim": 64,
            "sim": 60
        }

        return args

    def _get_embeddings(self):
        """
        Get image vectors. Supports image paths and folders.

        Returns:
            embeddings (Union[List, np.array]): Image(s) embeddings
        """
        # TODO: Improve memory management.
        path = self.args.path
        model = self.args.model
        dim = self.args.dim
        if os.path.isdir(path):
            img_paths = [file for i in [glob.glob(path + '/*.%s' % e) for e in EXTENSIONS] for file in i]
        else:
            img_paths = [path]
        imgs = [Image.open(f).convert('RGB') for f in img_paths]
        img2vec = Img2Vec(model=model, cuda=torch.cuda.is_available())

        logging.info(f"Getting {model} embeddings for {len(imgs)} images")
        vec = img2vec.get_vec(imgs)
        embs = PCA(n_components=dim).fit_transform(vec) # Use faiss here.

        return embs

    def _get_index(self, emb):
        if not self.is_initialized:
            # TODO:
            # build new index if not present
            # There should be a watcher mechanism to keep track of new entries added so
            # that we don't have to compute for existing data
            index = faiss.IndexFlatL2(emb.shape[1])
            index.add(emb)
            faiss.write_index(index, "emb_index") 
            # TODO: remove hardcoding
            # self.is_initialized = True
        else:
            index = faiss.read_index("emb_index")
            # Add new entries

        return index

    def enforce(self):
        # Contract enforcement logic
        failed_logs = []
        embs = self._get_embeddings()
        index = self._get_index(embs)
        img_paths = [file for i in [glob.glob(self.args.path + '/*.%s' % e) for e in EXTENSIONS] for file in i]

        for idx, emb in enumerate(embs[:len(embs)//2]):
                [d], [i] = index.search(emb.reshape(1,-1), 2)
                if d[1] < self.args.sim:
                    failed_logs.append(f" {img_paths[idx]} and {img_paths[i[1]]} are similar {d[1]}")
        
        return Result(name=self.__class__.__name__, success=len(failed_logs)==0, logs=failed_logs)

    

