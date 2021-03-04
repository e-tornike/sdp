from typing import List
from src.io import Sentence
from src.state import State


class FeatureItem:
    def __init__(self, transition: str, features: List):
        self.transition = transition
        self.features = features


class FeatureMap:
    def __init__(self):
        self.feature_map = {}
        self.freeze = False
        self.id = 1

    def get_features(self, c: State, s: Sentence) -> List:
        features = []
        # stack = c.stack
        # buffer = c.buffer
        # arcs = c.arcs
        # ld = c.ld
        # rd = c.rd
        form = [t.form for t in s.tokens]
        lemma = [t.lemma for t in s.tokens]
        pos = [t.pos for t in s.tokens]
        xpos = [t.xpos for t in s.tokens]
        morph = [t.morph for t in s.tokens]

        # print(len(form), "Form:", form)
        # print(len(lemma), "Lemma:", lemma)
        # print(len(pos), "POS:", pos)
        # print(len(xpos), "XPOS:", xpos)
        # print(len(morph), "Morph:", morph)

        if c.buffer != []:
            # Features for B[0]
            b0 = c.buffer[0]-1
            features.append(self.get_feature(f"B[0]:form:{form[b0]}"))
            features.append(self.get_feature(f"B[0]:lemma:{lemma[b0]}"))
            features.append(self.get_feature(f"B[0]:cpos:{pos[b0]}"))
            features.append(self.get_feature(f"B[0]:fpos:{xpos[b0]}"))
            features.append(self.get_feature(f"B[0]:feat:{morph[b0]}"))

            # Features for B[1]
            if len(c.buffer) > 1:
                b1 = c.buffer[1]-1
                features.append(self.get_feature(f"B[1]:form:{form[b1]}"))
                features.append(self.get_feature(f"B[2]:fpos:{xpos[b1]}"))
            
            # Features for B[2]
            if len(c.buffer) > 2:
                b2 = c.buffer[2]-1
                features.append(self.get_feature(f"B[2]:fpos:{xpos[b2]}"))
            
            # Features for B[3]
            if len(c.buffer) > 3:
                b3 = c.buffer[3]-1
                features.append(self.get_feature(f"B[3]:fpos:{xpos[b3]}"))

            # # Features for ld(B[0])
            # if c.ld[b0] >= 0:
            #     features.append(self.get_feature(f"ld(B[0]):dep:{c.ld[b0]}"))
            
            # # Features for rd(B[0])
            # if c.ld[b0] >= 0:
            #     features.append(self.get_feature(f"rd(B[0]):dep:{c.rd[b0]}"))  # TODO Only S

        if c.stack != []:
            # Features for S[0]
            s0 = c.stack[-1]-1
            features.append(self.get_feature(f"S[0]:form:{form[s0]}"))
            features.append(self.get_feature(f"S[0]:lemma:{lemma[s0]}"))
            features.append(self.get_feature(f"S[0]:cpos:{pos[s0]}"))
            features.append(self.get_feature(f"S[0]:fpos:{xpos[s0]}"))
            features.append(self.get_feature(f"S[0]:feat:{morph[s0]}"))
            # features.append(self.get_feature(f"S[0]:dep:{}"))  # TODO Only E

            # Features for S[1]
            if len(c.stack) > 1:
                s1 = c.stack[-2]-1
                features.append(self.get_feature(f"S[1]:fpos:{xpos[s1]}"))
            
            # Features for hd(S[0]) TODO Only E

            # # Features for ld(S[0])
            # if c.ld[s0] >= 0:
            #     features.append(self.get_feature(f"ld(S[0]):dep:{c.ld[s0]}"))
            
            # # Features for rd(S[0])
            # if c.rd[s0] >= 0:
            #     features.append(self.get_feature(f"rd(S[0]):dep:{c.rd[s0]}"))

        return features

    def get_feature(self, feature):
        if self.freeze:
            if feature in self.feature_map:
                return self.feature_map[feature]
            else:
                return 0
        else:
            if feature not in self.feature_map:
                self.feature_map[feature] = self.id
                self.id += 1
            return self.feature_map[feature]

            
