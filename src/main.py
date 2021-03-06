import sys
sys.path.insert(0, '.')
from src.io import Sentence, Token
from src.reader import read_file
from src.writer import write_file
from src.metrics import evaluate
from src.state import State
from src.parser import ArcStandard
from src.parser_utils import getArcs
from src.feature_mapper import FeatureMap, FeatureItem
from src.model import Perceptron
from src.util import addHeads, convert_to_dict
from pathlib import Path
from typing import List, Tuple
from copy import copy
import pickle
import time
import numpy as np
import random
from sklearn.metrics import f1_score, accuracy_score
from tqdm import tqdm
import json


def test(data, model, fm, parser, path, debug=False):
    preds = []

    for i, sentence in enumerate(tqdm(data)):
        state = State(sentence)

        pred_arcs, pred_seq = parser.parse(state, sentence, fm, model, debug=debug)

        pred_sentence = addHeads(sentence, pred_arcs)
        preds.append(pred_sentence)
    
    if ".blind" in path:
        write_file(path.replace(".blind", ".preds"), preds)
    else:
        write_file(path+".preds", preds)

def main(path_train, path_dev, path_test, language, epochs=5, shuffle=True, debug=False, final=False):
    print("Reading files...")
    sentences_train = read_file(path_train, lang=language)
    if final:
        path_dev = path_dev.replace(".blind", ".gold")
    sentences_dev = read_file(path_dev, lang=language)
    sentences_test = read_file(path_test, lang=language)

    fm = FeatureMap()
    parser = ArcStandard()
    labels = {"LARC": 0, "RARC": 1, "SHIFT": 2}

    print("Extracting features...")

    train_data = []

    for i, sentence in enumerate(tqdm(sentences_train)):
        state = State(sentence)
        _, gold_seq = parser.oracleParse(state, sentence, fm, debug=debug)
        train_data += gold_seq

    if final:
        for i, sentence in enumerate(tqdm(sentences_dev)):
            state = State(sentence)
            _, gold_seq = parser.oracleParse(state, sentence, fm, debug=debug)
            train_data += gold_seq

    fm.freeze = True

    print("Done.")

    print("Training...")
    
    model = Perceptron(fm.feature_map, labels)
    model.train(train_data, epochs=epochs, shuffle=shuffle)

    print("Done.")

    print("Testing...")

    test(sentences_train, model, fm, parser, path_train, debug)
    test(sentences_dev, model, fm, parser, path_dev, debug)
    test(sentences_test, model, fm, parser, path_test, debug)

    print("Saving model...")

    model.save(f"lang_{language}_epochs_{str(epochs)}")

    print("Done.")

def eval(path_gold):
    if ".blind" in path_gold:
        sentences_gold = read_file(path_gold.replace(".blind", ".gold"))
        sentences_pred = read_file(path_gold.replace(".blind", ".preds"))
    else:
        sentences_gold = read_file(path_gold)
        sentences_pred = read_file(path_gold+".preds")

    gold_dict = convert_to_dict(sentences_gold)
    pred_dict = convert_to_dict(sentences_pred)

    return evaluate(gold_dict, pred_dict)


if __name__ == "__main__":
    first_k = False
    debug = False
    epochs = 50
    final = False
    name = ""
    if first_k:
        name = ".first-1k"

    path_train = f"/home/tony/Coding/MA/ws2021/sdp/data/english/train/wsj_train.only-projective{name}.conll06"
    path_dev = "/home/tony/Coding/MA/ws2021/sdp/data/english/dev/wsj_dev.conll06.blind"
    path_test = "/home/tony/Coding/MA/ws2021/sdp/data/english/test/wsj_test.conll06.blind"
    lang = "en"

    main(path_train, path_dev, path_test, lang, epochs=epochs, debug=debug, final=final)

    print("Train acc:", eval(path_train))
    print("Dev acc:", eval(path_dev))

    print("================")

    path_train = f"/home/tony/Coding/MA/ws2021/sdp/data/german/train/tiger-2.2.train.only-projective{name}.conll06"
    path_dev = "/home/tony/Coding/MA/ws2021/sdp/data/german/dev/tiger-2.2.dev.conll06.blind"
    path_test = "/home/tony/Coding/MA/ws2021/sdp/data/german/test/tiger-2.2.test.conll06.blind"
    lang = "de"

    main(path_train, path_dev, path_test, lang, epochs=epochs, debug=debug, final=final)

    print("Train acc:", eval(path_train))
    print("Dev acc:", eval(path_dev))
