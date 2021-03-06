import sys
sys.path.insert(0, '.')
from pathlib import Path
from typing import List
from src.io import Sentence, Token
from reader import read


class TestReader:

    def test_contents(self):
        file1 = "/home/tony/Coding/MA/ws2021/sdp/data/english/train/wsj_train.conll06"
        sentences1 = read(file1)
        assert isinstance(sentences1, List)
        assert isinstance(sentences1[0], Sentence)
        assert isinstance(sentences1[0].tokens, List)
        assert isinstance(sentences1[0].tokens[0], Token)

        assert len(sentences1[0].tokens) == 49
        assert len(sentences1[4].tokens) == 29
        assert len(sentences1[-1].tokens) == 45
        assert len(sentences1[-2].tokens) == 23
        assert sentences1[1].tokens[1].form == "Haag"
        assert sentences1[1].tokens[1].pos == "NNP"
        assert sentences1[1].tokens[1].head == 3
        assert sentences1[-2].tokens[10].form == "million"
        assert sentences1[-2].tokens[10].pos == "CD"
        assert sentences1[-2].tokens[10].head == 10

        file2 = "/home/tony/Coding/MA/ws2021/sdp/data/german/dev/tiger-2.2.dev.conll06.gold"
        sentences2 = read(file2)
        assert isinstance(sentences2, List)
        assert isinstance(sentences2[0], Sentence)
        assert isinstance(sentences2[0].tokens, List)
        assert isinstance(sentences2[0].tokens[0], Token)

        assert len(sentences2[0].tokens) == 26
        assert len(sentences2[4].tokens) == 16
        assert len(sentences2[-1].tokens) == 24
        assert len(sentences2[-2].tokens) == 18
        assert sentences2[1].tokens[20].form == "Abkehr"
        assert sentences2[1].tokens[20].pos == "NN"
        assert sentences2[1].tokens[20].head == 19
        assert sentences2[-2].tokens[15].form == "aufbringen"
        assert sentences2[-2].tokens[15].pos == "VVFIN"
        assert sentences2[-2].tokens[15].head == 1

        file3 = "/home/tony/Coding/MA/ws2021/sdp/data/german/test/tiger-2.2.test.conll06.blind"
        sentences3 = read(file3)
        assert isinstance(sentences3, List)
        assert isinstance(sentences3[0], Sentence)
        assert isinstance(sentences3[0].tokens, List)
        assert isinstance(sentences3[0].tokens[0], Token)

        assert len(sentences3[0].tokens) == 26
        assert len(sentences3[4].tokens) == 9
        assert len(sentences3[-1].tokens) == 11
        assert len(sentences3[-2].tokens) == 8
        assert sentences3[1].tokens[1].form == "Ministerium"
        assert sentences3[1].tokens[1].pos == "NN"
        assert sentences3[1].tokens[1].head == "_"
        assert sentences3[-2].tokens[5].form == "der"
        assert sentences3[-2].tokens[5].pos == "ART"
        assert sentences3[-2].tokens[5].head == "_"
