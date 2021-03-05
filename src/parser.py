from src.io import Sentence
from src.model import scoreTransitions, Perceptron
from src.feature_mapper import FeatureMap, FeatureItem
from src.state import State
from src.parser_utils import getArcs
from typing import List, Tuple
from abc import ABC, abstractmethod
import time
from copy import deepcopy, copy


class TransitionParser(ABC):
    @abstractmethod
    def apply_transition(self):
        pass

    @abstractmethod
    def oracleParse(self):
        pass

    @abstractmethod
    def parse(self):
        pass

    def notTerminal(self, c: State) -> bool:
        if c.buffer != []:
            return True
        else:
            return False


class ArcStandard(TransitionParser):
    def __init__(self):
        super()

    def leftArc(self, c) -> State:
        if c.stack == [] or c.buffer == []:
            return

        front_buffer = c.buffer[0]
        top_stack = c.stack[-1]

        if top_stack != 0:
            c.stack = c.stack[:-1]
            c.arcs.append((front_buffer, "L", top_stack))

            return c

    def rightArc(self, c) -> State:
        if c.stack == [] or c.buffer == []:
            return

        front_buffer = c.buffer[0]
        top_stack = c.stack[-1]

        c.stack = c.stack[:-1]
        c.buffer = c.buffer[1:]
        c.buffer = [top_stack] + c.buffer
        c.arcs.append((top_stack, "R", front_buffer))

        return c

    def shift(self, c) -> State:
        if len(c.buffer) > 1 or c.stack == []:

            front_buffer = c.buffer[0]
            c.stack.append(front_buffer)
            c.buffer = c.buffer[1:]

            return c

    def can_leftArc(self, c) -> bool:
        if c.stack ==[] or c.buffer == []:
            return False
        else:
            top_stack = c.stack[-1]

            if top_stack != 0:
                return True
            else:
                return False

    def can_rightArc(self, c) -> bool:
        if c.stack == [] or c.buffer ==[]:
            return False
        else:
            return True

    def can_shift(self, c) -> bool:
        if len(c.buffer) > 1 or c.stack == []:
            return True
        else:
            return False

    def shouldLeftArc(self, c: State, gold_arcs: List[Tuple]) -> bool:
        if c.stack == []:
            return False

        front_buffer = c.buffer[0]
        top_stack = c.stack[-1]

        if (front_buffer, "L", top_stack) in gold_arcs and top_stack != 0:
            return True
        else:
            return False

    def shouldRightArc(self, c: State, gold_arcs: List[Tuple]) -> bool:
        if c.stack == []:
            return False

        front_buffer = c.buffer[0]
        top_stack = c.stack[-1]

        if (top_stack, "R", front_buffer) in gold_arcs and self.hasAllChildren(front_buffer, c.arcs, gold_arcs):
            return True
        else:
            return False

    def hasAllChildren(self, front_buffer: int, arcs_current: List[Tuple], arcs_gold: List[Tuple]) -> bool:
        b = front_buffer
        for t in arcs_gold:
            if (b == t[0] and t not in arcs_current and "R" == t[1]) or (b == t[2] and t not in arcs_current and "L" == t[1]):
                return False
        return True

    def findFirstValid(self, scores: dict, c: State) -> str:
        for (t, score) in scores:
            if t == "LARC":
                if self.can_leftArc(c):
                    return (t, score)
            elif t == "RARC":
                if self.can_rightArc(c):
                    return (t, score)
            elif t == "SHIFT":
                if self.can_shift(c):
                    return (t, score)
            else:
                print(f"Invalid transition: {t}")

    def apply_transition(self, c: State, t: str) -> None:    
        if t == "LARC":
            try:
                self.leftArc(c)
            except:
                print("Could not execute transition: LARC")
        elif t == "RARC":
            try:
                self.rightArc(c)
            except:
                print("Could not execute transition: RARC")
        elif t == "SHIFT":
            try:
                self.shift(c)
            except:
                print("Could not execute transition: RARC")
        else:
            print(f"Invalid transition: {t}")
    
    def oracleParse(self, s: State, sentence: Sentence, fm: FeatureMap, debug: bool = False) -> List[FeatureItem]:
        seq = []
        c = deepcopy(s)

        gold_arcs = getArcs(sentence)

        if debug:
            print("Starting state:")
            print("Stack:", c.stack)
            print("Buffer:", c.buffer)
            print("Arcs:", c.arcs)
            print("Gold arcs:", gold_arcs)
            print("======================")
            print("\n")

        while self.notTerminal(c):
            features = fm.get_features(c, sentence, debug=debug)
            if self.shouldLeftArc(c, gold_arcs):
                t = "LARC"
            elif self.shouldRightArc(c, gold_arcs):
                t = "RARC"
            else:
                t = "SHIFT"
            
            self.apply_transition(c, t)

            item = FeatureItem(t, features)
            seq.append(item)

            if debug:
                print("Transition:", t)
                print("Stack:", c.stack)
                print("Buffer:", c.buffer)
                print("Arcs:", c.arcs)
                print("Seq:", [t.transition for t in seq])
                print("\n")

        if debug:
            print("\n")
            print("======================")
            print("\n")
            print("Ending state:")
            print("Stack:", c.stack)
            print("Buffer:", c.buffer)
            print("Arcs:", c.arcs)
            print("Seq:", [t.transition for t in seq])

        return (c.arcs, gold_arcs), seq

    def parse(self, s: State, sentence: Sentence, fm: FeatureMap, model: Perceptron, debug: bool = False) -> List[FeatureItem]:
        seq = []
        c = deepcopy(s)

        if debug:
            print("Starting state:")
            print("Stack:", c.stack)
            print("Buffer:", c.buffer)
            print("Arcs:", c.arcs)
            print("======================")
            print("\n")

        while self.notTerminal(c):
            features = fm.get_features(c, sentence, debug=debug)

            scores = scoreTransitions(c, features, model, ["LARC", "RARC", "SHIFT"])
            t,_ = self.findFirstValid(scores, c)
            self.apply_transition(c, t)

            item = FeatureItem(t, features)
            seq.append(item)

            if debug:
                print("Scores:", scores)
                print("First valid:", t)
                print("Stack:", c.stack)
                print("Buffer:", c.buffer)
                print("Arcs:", c.arcs)
                print("Seq:", [t.transition for t in seq])
                print("\n")

        if debug:
            print("\n")
            print("======================")
            print("\n")
            print("Ending state:")
            print("Stack:", c.stack)
            print("Buffer:", c.buffer)
            print("Arcs:", c.arcs)
            print("Seq:", [t.transition for t in seq])

        return c.arcs, seq


# class ArcEager(TransitionParser):
#     def __init__(self):
#         super()

#     def apply_transition(self, c: State, t: str) -> None:      
#         if t == "LARC":
#             front_buffer = c.buffer[0]
#             top_stack = c.stack[-1]
#             if not self.hasHead(top_stack, c.arcs) and top_stack != 0:
#                 c.stack = c.stack[:-1]
#                 c.arcs.append((front_buffer, "L", top_stack))
#             else:
#                 print(f"Precondition not met for transition: {t}")
#         elif t == "RARC":
#             front_buffer = c.buffer[0]
#             top_stack = c.stack[-1]
#             c.stack.append(front_buffer)
#             c.buffer = c.buffer[1:]
#             c.arcs.append((top_stack, "R", front_buffer))
#         elif t == "REDUCE":
#             top_stack = c.stack[-1]
#             if self.hasHead(top_stack, c.arcs):
#                 c.stack = c.stack[:-1]
#             else:
#                 print(f"Precondition not met for transition: {t}")
#         elif t == "SHIFT":
#             front_buffer = c.buffer[0]
#             c.stack.append(front_buffer)
#             c.buffer = c.buffer[1:]
#         else:
#             print(f"Invalid transition: {t}")

#     def hasHead(self, top_stack: int, arcs_current: List[Tuple]) -> bool:
#         for (a,l,b) in arcs_current:
#             if a == top_stack and l == "L" or b == top_stack and l == "R":  # TODO check validity
#                 return True
#         return False

#     def hasAllChildren(self, top_stack: int, arcs_current: List[Tuple], arcs_gold: List[Tuple]) -> bool:
#         b = top_stack
#         for t in arcs_gold:
#             if (b == t[0] and t not in arcs_current and "R" == t[1]) or (b == t[2] and t not in arcs_current and "L" == t[1]):
#                 return False
#         return True

#     def shouldLeftArc(self, c: State, gold_arcs: List[Tuple]) -> bool:
#         if c.stack == []:
#             return False

#         front_buffer = c.buffer[0]
#         top_stack = c.stack[-1]

#         if (front_buffer, "L",  top_stack) in gold_arcs and top_stack != 0:
#             return True
#         else:
#             return False

#     def shouldRightArc(self, c: State, gold_arcs: List[Tuple]) -> bool:
#         if c.stack == []:
#             return False

#         front_buffer = c.buffer[0]
#         top_stack = c.stack[-1]

#         if (top_stack, "R", front_buffer) in gold_arcs:
#             return True
#         else:
#             return False

#     def shouldReduce(self, c: State, gold_arcs: List[Tuple]) -> bool:
#         if c.stack == []:
#             return False
        
#         top_stack = c.stack[-1]

#         if self.hasHead(top_stack, c.arcs) and self.hasAllChildren(top_stack, c.arcs, gold_arcs):
#             return True
#         else:
#             return False

#     def oracleParse(self, s: State, sentence: Sentence, fm: FeatureMap) -> List[FeatureItem]:
#         seq = []
#         c = deepcopy(s)

#         gold_arcs = getArcs(sentence)

#         while self.notTerminal(c):
#             if self.shouldLeftArc(c, gold_arcs):
#                 t = "LARC"
#             elif self.shouldRightArc(c, gold_arcs):
#                 t = "RARC"
#             elif self.shouldReduce(c, gold_arcs):
#                 t = "REDUCE"
#             else:
#                 t = "SHIFT"
            
#             self.apply_transition(c, t)
#             seq.append(t)

#             time.sleep(0.25)
#         return seq

#     def parse(self):
#         pass
