from src.io import Sentence


class State:
    def __init__(self, sentence: Sentence):
        self.stack = [0]
        self.buffer = []
        self.arcs = []
        self.ld = []  # TODO
        self.rd = []  # TODO

        self.init_config(sentence)

    def init_config(self, sentence: Sentence):
        self.buffer = [t.id for t in sentence.tokens]
