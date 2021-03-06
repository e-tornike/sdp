from typing import List, Dict


class Token():
    def __init__(self, t: Dict):
        self.id = t['ID']
        self.form = t['FORM']
        self.lemma = t['LEMMA']
        self.pos = t['POS']
        self.xpos = t['XPOS']
        self.morph = t['MORPH']
        self.head = t['HEAD']
        self.rel = t['REL']
        self.x1 = t['X1']
        self.x2 = t['X2']


class Sentence():
    def __init__(self, sentence: List[Dict]):
        self.tokens = self.convert2tokens(sentence)

    def convert2tokens(self, sentence: List[Dict]):
        tokens = []

        for i, d in enumerate(sentence):
            token = Token(d)
            tokens.append(token)
        
        return tokens
