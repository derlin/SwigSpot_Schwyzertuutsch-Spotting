from scipy.sparse import csr_matrix, vstack
from scipy.sparse.linalg import norm as scipy_norm
import numpy as np
from math import log
import re 


class NaiveVectorizer:
    """
    This class is a very naive implementation of an ngram vectorizer.

    During fit, it creates a vocabulary using the X most common ngrams found
    in the samples. This vocabulary is then used to transform a sentence into vector of size
    <vocabulary size>.
    """
    def __init__(self, ngram_range=(3,5), max_features=1000, ignore_non_words=True):
        """
        Create a vectorizer using character ngrams of size :param ngram_range:. Lower and upper bounds
        are inclusive. To use fixed ngrams, use the same value for lower and upper bounds.

        :param ngram_range: range of ngrams to use for the features.
        :param max_features: the maximum number of ngrams to keep.
        :param ignore_non_words: if set, ngrams with no letter at all are discarded from the vocabulary.
        """
        self.nrange = ngram_range
        self.max_features = max_features
        self.ignore_non_words = ignore_non_words

    @staticmethod
    def _ngrams(text, n, lookup=None):
        """
        Returns all ngrams of size :param n: contained in :param text:.
        In case :param lookup: is specified, only ngrams found in lookup are returned.

        :param text: the text to extract ngrams from. It is always transformed to lowercase first.
        :param n: the ngram size.
        :param lookup: an optional dictionary|list of valid ngrams.
        """
        text = text.lower()
        if lookup is not None:
            return [text[i:i+n] for i in range(len(text)-n+1) if text[i:i+n] in lookup and text[i:i+n] ]    
        return [text[i:i+n] for i in range(len(text)-n+1)]

    @staticmethod
    def _ngrams_range(text, n_range, lookup=None):
        """
        Returns all ngrams of size in the :param n_range: bounds (inclusive) contained in :param text:.
        In case :param lookup: is specified, only ngrams found in lookup are returned.
        """
        return sum([NaiveVectorizer._ngrams(text, n, lookup) for n in range(n_range[0], n_range[1]+1)], [])


    def fit(self, trainset, labels=None):
        """
        Train the vectorizer using :param trainset:. 
        Steps:
            - extract all character ngrams from :param trainset:;
            - count the frequency of each ngram;
            - sort ngrams according to their frequency;
            - keep the :param max_features: most frequent ngrams.
        
        :param trainset: the sentences to use for training.
        """
        ngs = [] 
        if self.ignore_non_words:
            reg = re.compile(r"^[\W|\d]+$") # match all ngram with no unicode letter in it
            for sample in trainset: ngs += [ng for ng in NaiveVectorizer._ngrams_range(sample, self.nrange) if not re.match(reg, ng)]
        else:
            for sample in trainset: ngs += NaiveVectorizer._ngrams_range(sample, self.nrange)

        (uniques, cnts) = np.unique(ngs, return_counts=True)
        idx_sorted = (-cnts).argsort()

        self._feature_weights = cnts[idx_sorted][:self.max_features]
        self._feature_names = uniques[idx_sorted][:self.max_features] 

        values = zip(self._feature_weights, range(0, self._feature_names.size+1))
        # features: a dictionary 'N-gram' => (weight, idx)
        self._features = dict(zip(self._feature_names, values))


    def fit_transform(self, trainset, labels=None): # TODO: important to use the pipeline with memory ?
        self.fit(trainset, labels)
        return self.transform(trainset)


    def transform(self, dataset, labels=None):
        """
        Transform a list of sentences into a document-term matrix using the features extracted using
        fit.

        Steps for each sentence:
         - extract and count the frequencies of each ngram of the features contained in the sentence;
         - normalise the frequencies: vec = vec / norm(vec)

        :param dataset: the list of sentences to transform.
        :param labels: unused (bug useful to use the sklearn pipeline)
        :return: a sparse matrix of size (len(dataset), num_features)
        """
        # using vectorize, transform(X_train) went from ~2.13 minutes to ~15 sec !
        mm = np.vectorize(self._transform_row)
        return vstack(mm(dataset))


    def _transform_row(self, d):
        # get all the ngrams part of our features
        d_grams = self._ngrams_range(d, self.nrange, self._features)
        if len(d_grams) == 0:
            # print("no dgram found %s" % d)
            return csr_matrix((1, self._feature_names.size), dtype=np.float64)
        # frequency of the ngrams
        (uniq, freqs) = np.unique(d_grams, return_counts=True)
        
        # vector of "x": logarithm of observed ngrams
        vec = 1 + np.log(np.array(freqs))
        # lookup the index of the observed ngrams in the dictionary
        idx = np.array([ self._features[k][1] for k in uniq])
        mat = csr_matrix((vec,([0]*vec.size, idx)), shape=(1, self._feature_names.size))

        # normalise the result to account for the length of the sentence
        return mat / scipy_norm(mat) 