from typing import List
from src.io import Sentence
from src.state import State


class FeatureItem:
    def __init__(self, transition: str, features: List):
        self.transition = transition
        self.features = features


class FeatureMap:
    def __init__(self):
        self.feature_map = {"__NULL__": 0}
        self.feature_map_reverse = {0: "__NULL__"}
        self.freeze = False
        self.id = 1

    def get_features(self, c: State, s: Sentence, debug=False) -> List:
        features = []
        # stack = c.stack
        # buffer = c.buffer
        # arcs = c.arcs
        # ld = c.ld
        # rd = c.rd
        form = ["ROOT"]+[t.form for t in s.tokens]
        lemma = ["ROOT"]+[t.lemma for t in s.tokens]
        pos = ["ROOT"]+[t.pos for t in s.tokens]
        xpos = ["ROOT"]+[t.xpos for t in s.tokens]
        morph = ["ROOT"]+[t.morph for t in s.tokens]

        idx = 0  # root is not in tokens

        if c.buffer != []:
            # Features for B[0]
            b0 = c.buffer[0]-idx
            features.append(self.get_feature(f"B[0]-form:{form[b0]}"))
            features.append(self.get_feature(f"B[0]-lemma:{lemma[b0]}"))
            features.append(self.get_feature(f"B[0]-cpos:{pos[b0]}"))
            # features.append(self.get_feature(f"B[0]:fpos:{xpos[b0]}"))
            # features.append(self.get_feature(f"B[0]:feat:{morph[b0]}"))

            # Extended
            features.append(self.get_feature(f"B[0]-form:{form[b0]}+cpos:{pos[b0]}"))

            # Features for B[1]
            if len(c.buffer) > 1:
                b1 = c.buffer[1]-idx
                features.append(self.get_feature(f"B[1]-form:{form[b1]}"))
                # features.append(self.get_feature(f"B[1]:fpos:{xpos[b1]}"))
                features.append(self.get_feature(f"B[1]-cpos:{pos[b1]}"))

                # Extended
                features.append(self.get_feature(f"B[1]-form:{form[b1]}+cpos:{pos[b1]}"))
            
            # Features for B[2]
            if len(c.buffer) > 2:
                b2 = c.buffer[2]-idx
                # features.append(self.get_feature(f"B[2]:fpos:{xpos[b2]}"))
                features.append(self.get_feature(f"B[2]-cpos:{pos[b2]}"))

                # Extended
                features.append(self.get_feature(f"B[2]-form:{form[b2]}"))
                features.append(self.get_feature(f"B[2]-form:{form[b2]}+cpos:{pos[b2]}"))
            
            # Features for B[3]
            if len(c.buffer) > 3:
                b3 = c.buffer[3]-idx
                # features.append(self.get_feature(f"B[3]:fpos:{xpos[b3]}"))
                features.append(self.get_feature(f"B[3]-cpos:{pos[b3]}"))

            # # Features for ld(B[0])
            # if c.ld[b0] >= 0:
            #     features.append(self.get_feature(f"ld(B[0]):dep:{c.ld[b0]}"))
            
            # # Features for rd(B[0])
            # if c.ld[b0] >= 0:
            #     features.append(self.get_feature(f"rd(B[0]):dep:{c.rd[b0]}"))  # TODO Only S

        if c.stack != []:
            # Features for S[0]
            s0 = c.stack[-1]-idx
            features.append(self.get_feature(f"S[0]-form:{form[s0]}"))
            features.append(self.get_feature(f"S[0]-lemma:{lemma[s0]}"))
            features.append(self.get_feature(f"S[0]-cpos:{pos[s0]}"))
            # features.append(self.get_feature(f"S[0]:fpos:{xpos[s0]}"))
            # features.append(self.get_feature(f"S[0]:feat:{morph[s0]}"))
            # features.append(self.get_feature(f"S[0]:dep:{}"))  # TODO Only E

            # Extended
            features.append(self.get_feature(f"S[0]-form:{form[s0]}+cpos:{pos[s0]}"))

            # Features for S[1]
            if len(c.stack) > 1:
                s1 = c.stack[-2]-idx
                # features.append(self.get_feature(f"S[1]:fpos:{xpos[s1]}"))
                features.append(self.get_feature(f"S[1]-cpos:{pos[s1]}"))

            # Extended
            if c.buffer != []:
                b0 = c.buffer[0]-idx
                features.append(self.get_feature(f"S[0]-form:{form[s0]}+cpos:{pos[s0]}&B[0]-form:{form[b0]}+cpos:{pos[b0]}"))
                features.append(self.get_feature(f"S[0]-form:{form[s0]}+cpos:{pos[s0]}&B[0]-form:{form[b0]}"))
                features.append(self.get_feature(f"S[0]-form:{form[s0]}+cpos:{pos[s0]}&B[0]-cpos:{pos[b0]}"))
                features.append(self.get_feature(f"S[0]-form:{form[s0]}&B[0]-form:{form[b0]}+cpos:{pos[b0]}"))
                features.append(self.get_feature(f"S[0]-cpos:{pos[s0]}&B[0]-form:{form[b0]}+cpos:{pos[b0]}"))
                features.append(self.get_feature(f"S[0]-form:{form[s0]}&B[0]-form:{form[b0]}"))
                features.append(self.get_feature(f"S[0]-cpos:{pos[s0]}&B[0]-cpos:{pos[b0]}"))

                if len(c.buffer) > 1:
                    b1 = c.buffer[1]-idx
                    features.append(self.get_feature(f"B[0]-cpos:{pos[b0]}&B[1]-cpos:{pos[b1]}"))
            
            # Features for hd(S[0]) TODO Only E

            # # Features for ld(S[0])
            # if c.ld[s0] >= 0:
            #     features.append(self.get_feature(f"ld(S[0]):dep:{c.ld[s0]}"))
            
            # # Features for rd(S[0])
            # if c.rd[s0] >= 0:
            #     features.append(self.get_feature(f"rd(S[0]):dep:{c.rd[s0]}"))
        # if c.stack != []:
        #     if c.stack[-1] == 0:
        #         print("\n===")
        #         print(f"Sentence:", [(t.id, t.form, t.lemma, t.pos, t.xpos, t.morph) for t in s.tokens])
        #         print(f"Stack:", c.stack)
        #         print(f"Buffer:", c.buffer)
        #         print("=")
        #         print(f"Features:", features)
        #         print(f"Features length:", len(self.feature_map_reverse))
        #         print(f"Features:", [self.feature_map_reverse[f] for f in features])
        #         print("===\n")
        # if c.buffer != []:
        #     if c.buffer[0] == 0:
        #         print("\n===")
        #         print(f"Sentence:", [(t.id, t.form, t.lemma, t.pos, t.xpos, t.morph) for t in s.tokens])
        #         print(f"Stack:", c.stack)
        #         print(f"Buffer:", c.buffer)
        #         print("=")
        #         print(f"Features:", features)
        #         print(f"Features length:", len(self.feature_map_reverse))
        #         print(f"Features:", [self.feature_map_reverse[f] for f in features])
        #         print("===\n")

        if debug:
            # self.feature_map_reverse = {v:k for k,v in self.feature_map.items()}
            print("\n===")
            print(f"Sentence:", [(t.id, t.form, t.lemma, t.pos, t.xpos, t.morph) for t in s.tokens])
            print(f"Stack:", c.stack)
            print(f"Buffer:", c.buffer)
            print("=")
            print(f"Features:", features)
            print(f"Features length:", len(self.feature_map_reverse))
            print(f"Features:", [self.feature_map_reverse[f] for f in features])
            print("===\n")

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
                self.feature_map_reverse[self.id] = feature
                self.id += 1
            return self.feature_map[feature]
