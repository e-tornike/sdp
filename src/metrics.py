import sys
sys.path.insert(0, '.')
from src.io import Sentence, Token
from typing import List, Dict
import numpy as np


def evaluate(gold: Dict, pred: Dict) -> Dict:
    gold_head = np.asarray(gold['HEAD'])
    # gold_rel = np.asarray(gold['REL'])
    pred_head = np.asarray(pred['HEAD'])
    # pred_rel = np.asarray(pred['REL'])

    print(gold_head)
    print(pred_head)

    # assert gold_head.shape == gold_rel.shape

    true_head = gold_head == pred_head
    uas = true_head.sum() / gold_head.shape[0]

    # true_rel = gold_rel == pred_rel
    # las = np.logical_and(true_head, true_rel).sum() / gold_head.shape[0]

    # return {"UAS": uas, "LAS": las}
    return {"UAS": uas}
