import pickle
import re
from os import path
import numpy as np
from typing import List, Tuple
from .naive_identifier import NaiveIdentifier

DEFAULT_LABELS = ['de', 'fr', 'en', 'it', 'sg']


class Model:

    def __init__(self, model_name: str, description: str, labels=DEFAULT_LABELS, sanitizer=None):

        with open(path.join(path.dirname(path.realpath(__file__)), '_pickles', model_name), 'br') as f:
            self.pipe = pickle.load(f)

        self.description = description
        self.labels = labels
        self._sanitizer = sanitizer or (lambda s: s)

    # -- predictions

    def predict(self, sentences, min_words=0, return_raw=False) -> List[Tuple[str, int]]:
        tup = self._preprocess(sentences, min_words)
        if len(tup) > 0:
            predicted = self.pipe.predict([t[1] for t in tup])
            return list(zip(map(lambda t: t[not return_raw], tup), predicted))
        return []

    def predict_proba(self, sentences, min_words=0, return_raw=False) -> List[Tuple[str, int, List[np.float64]]]:
        tup = self._preprocess(sentences, min_words)
        if len(tup) > 0:
            proba = self.pipe.predict_proba([t[1] for t in tup])
            predicted = np.argmax(proba, axis=1).tolist()
            return list(zip(map(lambda t: t[not return_raw], tup), predicted, proba))
        return []

    # -- private methods

    def _preprocess(self, sentences, min_words=0) -> List[Tuple[str, str]]:
        tup = [(s, self._sanitizer(s)) for s in sentences]
        if min_words > 1:
            return [t for t in tup if len(re.split(r"\s+", t[1])) >= min_words]
        else:
            return tup
