from src.io import Sentence
from typing import List, Tuple


def getArcs(sentence: Sentence) -> List[Tuple]:
    arcs = []

    for token in sentence.tokens:
        l = "L" if token.head > token.id else "R"
        arcs.append((token.head, l, token.id))

    return arcs
