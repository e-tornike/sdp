import sys
sys.path.insert(0, '.')
from pathlib import Path
from typing import List
from src.io import Sentence, Token
import pandas as pd


def read_file(filename: str) -> List[Sentence]:
    path = Path(filename)
    assert path.is_file()

    df = pd.read_csv(path, sep='\t', names=["ID", "FORM", "LEMMA", "POS", "XPOS", "MORPH", "HEAD", "REL", "X1", "X2"])

    sentences = []
    tokens = []

    for row in df.itertuples():
        if row.ID == 1 and row.Index > 0:
            sentences.append(Sentence(tokens))
            tokens = []

        dic = {
            'ID': row.ID, 
            'FORM': row.FORM, 
            'LEMMA': row.LEMMA, 
            'POS': row.POS, 
            'XPOS': row.XPOS, 
            'MORPH': row.MORPH, 
            'HEAD': row.HEAD, 
            'REL': row.REL,
            'X1': row.X1, 
            'X2': row.X2
            }
        tokens.append(dic)

        if row.Index == df.shape[0]-1:
            sentences.append(Sentence(tokens))
    
    return sentences
