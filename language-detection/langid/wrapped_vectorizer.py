from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np

class WrappedVectorizer:

    def __init__(self, sanitizer=None, sg_only=False,  *args, **kwargs):
        self.sg_only = sg_only 
        self.sanitizer = sanitizer
        self.vectorizer = TfidfVectorizer(*args, **kwargs)
    

    def fit(self, data, labels=None):
        if self.sg_only:
            if labels is None: 
                raise Exception('fit: Labels cannot be None if sg_only=True')
            else:  
                data = np.array(data)[np.array(labels) == 4]
                # print("fitting using %d data" % len(data))
        if self.sanitizer is not None:
            data = self.sanitizer(data)
        
        self.vectorizer.fit(data)
    

    def transform(self, data):
        if self.sanitizer is not None: data = self.sanitizer(data)
        return self.vectorizer.transform(data)
    

    def fit_transform(self, data, labels):
        self.fit(data, labels)
        return self.transform(data)
    

    def set_params(self, **parameters):
        # treat our params
        for key in ['sg_only', 'sanitizer']:
            if key in parameters:
                setattr(self, key, parameters[key])
                del parameters[key]
        # forward the remaining to the scikit vectorizer
        self.vectorizer.set_params(**parameters)
        # don't forget to return self
        # see https://stackoverflow.com/questions/28124366/can-gridsearchcv-be-used-with-a-custom-classifier
        return self
    

    def get_params(self, deep=True):
        if deep:
            return dict(**dict(sg_only=self.sg_only, sanitizer=self.sanitizer), **self.vectorizer.get_params())
        else:
            return dict(sg_only=self.sg_only, sanitizer=self.sanitizer)


    def __repr__(self):
        return "WrappedVectorizer(%s)" % ", ".join([ "%s=%r" % t for t in self.get_params().items()])
