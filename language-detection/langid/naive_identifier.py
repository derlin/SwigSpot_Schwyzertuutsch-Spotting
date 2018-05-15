from sklearn.feature_extraction.text import TfidfVectorizer
from scipy.sparse import csr_matrix
import numpy as np
from sklearn import feature_extraction
from typing import List


class NaiveIdentifier:
    
    def __init__(self, klass=TfidfVectorizer, **vectorizer_options):
        """
        Create a naive identifier. 
        :param klass: the vectorizer class to use. Default to the sklean TfidfVectorizer.
        :param vectorizer_options: the named arguments to pass to the vectorizer constructor.
            If klass is TfidfVectorizer, default options are: 
                analyzer='char',  
                ngram_range=(3, 5), 
                max_features=3000,
                sublinear_tf=True, 
                use_idf=True, 
                norm='l2'
        """ 
        self.klass = klass
        if klass == TfidfVectorizer:
            # default vectorizer arguments
            self.options = dict(analyzer='char',  ngram_range=(3, 5), max_features=3000,
                    sublinear_tf=True, use_idf=True,  norm='l2')
            # update with arguments
            self.options.update(vectorizer_options)
        else:
            self.options = vectorizer_options 
    
    def fit(self, X_train: List[int], y_train: List[int]):
        """
        Create one vectorizer per class in y_train, training it with all samples from X_train
        having the  same label.
        :param X_train: the training set
        :param y_train: the class of each sample in the training set
        """
        self.vectorizers = [] 
        X_train = np.array(X_train)
        y_train = np.array(y_train)
        
        # create and fit
        for i in range(np.unique(y_train).size): 
            v = self.klass(**self.options)
            v.fit(X_train[y_train == i])  # train using samples of lang i
            self.vectorizers.append(v)
            
        return self # for pipelining 
    
    def fit_predict(self, X_train, y_train):
        """
        Call fit, then predict
        """
        self.fit(X_train, y_train)
        return self.predict(X_train)
        
    def predict(self, X: List[int]) -> csr_matrix:
        """
        Transform the data and sum the feature vectors using each vectorizer
        then return the labels of the vectorizer with the maximal score 
        :param X: the dataset
        :return: the most probable class
        """
        mat = np.hstack([v.transform(X).sum(axis=1) for v in self.vectorizers])
        self.last_scores = mat # for later use, just in case
        return mat.argmax(axis=1).A1