import pickle
import re
from os import path
import numpy as np
from typing import List, Tuple

DEFAULT_LABELS = ['de', 'fr', 'en', 'it', 'sg']


class Model:

    def __init__(self, model_name: str, description: str, labels=DEFAULT_LABELS, sanitizer=None):

        with open(path.join(path.dirname(path.realpath(__file__)), '_pickles', model_name), 'br') as f:
            self.pipe = pickle.load(f)

        self.description = description
        self.labels = labels
        self._sanitizer = sanitizer

    # -- predictions

    def predict(self, sentences, min_words=0, return_raw=False) -> List[Tuple[str, int]]:
        sentences_san = self._preprocess(sentences, min_words)
        if len(sentences_san) > 0:
            predicted = self.pipe.predict(sentences_san)
            return list(zip(sentences if return_raw else sentences_san, predicted))
        return []

    def predict_proba(self, sentences, min_words=0, return_raw=False) -> List[Tuple[str, int, List[np.float64]]]:
        sentences_san = self._preprocess(sentences, min_words)
        if len(sentences_san) > 0:
            proba = self.pipe.predict_proba(sentences_san)
            predicted = np.argmax(proba, axis=1).tolist()
            return list(zip(sentences if return_raw else sentences_san, predicted, proba))
        return []

    # -- private methods

    def _preprocess(self, sentences, min_words=0) -> List[str]:
        if self._sanitizer:
            sentences = [self._sanitizer(s) for s in sentences]
        if min_words > 1:
            sentences = [s for s in sentences if len(re.split(r"\s+", s)) >= min_words]
        return sentences
