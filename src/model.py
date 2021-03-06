from src.state import State
import random
import numpy as np
from typing import List, Tuple
import time
import json
import pickle
from sklearn.metrics import f1_score, accuracy_score
from tqdm import tqdm


class Perceptron:
    def __init__(self, feature_map, labels):
        self.fm = feature_map
        self.w = np.zeros((len(labels), len(feature_map)), dtype=np.float32)
        self.labels = labels

    def save(self, language):
        if not Path('./models').is_dir():
            Path('./models').mkdir()
        timestr = time.strftime("%Y%m%d-%H%M%S")
        model_path = f"./models/{language}_model_{timestr}.pkl"
        with open(model_path, "wb") as f:
            pickle.dump(self.w, f, -1)

        with open(f"./models/{language}_featuremap_{timestr}.json", "w") as f:
            json.dump(self.fm, f)

        print(f"Saved model to {model_path}")

    def load(self, path):
        try:
            self.fm = []  # TODO
            self.w = np.load(path)
        except:
            raise Exception(f"Could not load {path} into numpy array.")
    
    def train(self, data, epochs=5, shuffle=False):
        """
        - Shuffle training data at each iteration
        - Save model weights and pick best model at the end
        - Start training on 1k files
        - Early-stopping
        - Save feature_map and weights
        """
        q = 0
        # u = np.zeros(self.w.shape, dtype=np.float32)

        for e in tqdm(range(epochs)):
            correct = 0
            n = 0

            if shuffle:
                random.shuffle(data)

            for i,item in enumerate(data):
                q += 1
                n += 1

                scores = np.zeros((len(self.labels),))

                for idx in item.features:
                    for r in range(self.w.shape[0]):
                        scores[r] += self.w[r][idx-1]

                y_pred = np.argmax(scores)

                if y_pred != self.labels[item.transition]:
                    for idx in item.features:
                        self.w[self.labels[item.transition]][idx-1] += 1
                        self.w[y_pred][idx-1] -= 1
                        # diff = np.dot(y, self.phi(item))
                        # self.w += diff
                        # self.u += (q * diff)
                        # u[self.labels[item.transition]][idx-1] += q
                        # u[y_pred][idx-1] -= q
                else:
                    correct += 1

            print(f"Accuracy for epoch {e+1}: {correct/n}")

            # self.w -= u * (1/q)  # averaged perceptron

    def evaluate(self, data, average="micro"):

        gold = [self.labels[d.transition] for d in data]
        pred = []
        
        for i,item in enumerate(data):
            scores = np.zeros((len(self.labels)))

            for idx in item.features:
                for r in range(self.w.shape[0]):
                    scores[r] += self.w[r][idx-1]

            y_pred = np.argmax(scores)
            pred.append(y_pred)
        
        f1 = f1_score(gold, pred, labels=list(self.labels.values()), average=average)
        acc = accuracy_score(gold, pred)

        print(f"Accuracy: {acc}\nF1: {f1}")


def scoreTransitions(c: State, features: List, model: Perceptron, transitions: List[str], debug: bool = False, random: bool = False) -> List[Tuple]:
        scores = {}
        idxs = []
        
        if random:
            for t in transitions:
                scores[t] = random.random()
        else:
            scores = np.zeros((len(transitions)))
            for idx in features:
                for r in range(model.w.shape[0]):
                    scores[r] += model.w[r][idx-1]
                    idxs.append(idx-1)

        if debug:
            print("IDs:", idxs)
        
        scores = {t:scores[i] for i,t in enumerate(transitions)}
        sorted_scores = sorted(scores.items(), key=lambda item: item[1], reverse=True)

        return sorted_scores
