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
import argparse


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

def main(path_train, path_dev=None, path_test=None, epochs=5, shuffle=True, debug=False):
    print("Reading files...")
    sentences_train = read_file(path_train)
    if path_dev:
        sentences_dev = read_file(path_dev)
    if path_test:
        sentences_test = read_file(path_test)

    fm = FeatureMap()
    parser = ArcStandard()
    labels = {"LARC": 0, "RARC": 1, "SHIFT": 2}

    print("Extracting features...")

    train_data = []

    for i, sentence in enumerate(tqdm(sentences_train)):
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
    if path_dev:
        test(sentences_dev, model, fm, parser, path_dev, debug)
    if path_test:
        test(sentences_test, model, fm, parser, path_test, debug)

    print("Saving model...")

    model.save(f"file_{Path(path_train).name}_epochs_{str(epochs)}")

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
    parser = argparse.ArgumentParser()
    parser.add_argument('--train', required=True, help='Path to training conll06 file.')
    parser.add_argument('--dev', required=False, help='Path to development conll06 file.')
    parser.add_argument('--test', required=False, help='Path to testing conll06 file.')
    parser.add_argument('--shuffle', default=True, required=False, help='Shuffle training data each epoch.')
    parser.add_argument('--epochs', default=5, required=False, help='Number of epochs.')
    parser.add_argument('--debug', default=False, required=False, help='Print debug messages.')

    args = parser.parse_args()

    path_train = args.train if args.train else None
    path_dev = args.dev if args.dev else None
    path_test = args.test if args.test else None
    shuffle = args.shuffle
    epochs = args.epochs
    debug = args.debug

    print(path_train, path_dev, path_test, shuffle, epochs, debug)

    main(path_train, path_dev, path_test, epochs=epochs, shuffle=shuffle, debug=debug)
    print("Train UAS score:", eval(path_train))
    if path_dev:
        print("Development UAS score:", eval(path_dev))
