import sys
sys.path.insert(0, '.')
from src.io import Sentence, Token
from typing import List, Tuple
from copy import deepcopy


def convert_to_dict(sentences: List[Sentence]):
    res = {"HEAD": [], "REL": []}

    for sent in sentences:
        for tok in sent.tokens:
            res['HEAD'].append(tok.head)
            res['REL'].append(tok.rel)
    
    return res


def addHeads(s: Sentence, pred_arcs: List[Tuple]) -> Sentence:
    sentence = deepcopy(s)

    for (head,l,dep) in pred_arcs:
        # if l == "R":
        #     head = x
        #     dep = y
        # elif l == "L":
        #     head = y
        #     dep = x
        # else:
        #     print(f"Invalid relation: {l}")
        #     return

        sentence.tokens[dep-1].head = head
        # sentence.tokens[dep].head = head

    return sentence
